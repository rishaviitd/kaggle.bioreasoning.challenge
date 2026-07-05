"""Benchmark specific Qwen models on the exact 300 valset using DSPy-equivalent prompts.

Usage:
    python src/track_one/benchmarking/benchmark_frontier_models.py
"""

from __future__ import annotations

import csv
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics import f1_score, roc_auc_score

from src.track_one.utils.evaluate import LABELS, _final_answer_label, _seed_probabilities, _response_content

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "nvidia/nemotron-nano-9b-v2:free"
MODEL_CLEAN = MODEL.split("/")[-1].replace(".", "_").replace(":", "_")
MAX_TOKENS = 8192
REQUEST_TIMEOUT = 300.0
MAX_RETRIES = 5
MAX_WORKERS = 2 if ":free" in MODEL else 24

API_LOCK = threading.Lock()
LAST_REQ_TIME = 0.0

def _wait_for_rate_limit() -> None:
    global LAST_REQ_TIME
    with API_LOCK:
        now = time.monotonic()
        # Free models have a strict 15-20 RPM limit, so wait 4.0s between requests.
        delay = 4.0 if ":free" in MODEL else 0.5
        elapsed = now - LAST_REQ_TIME
        if elapsed < delay:
            time.sleep(delay - elapsed)
        LAST_REQ_TIME = time.monotonic()

DATA_PATH = ROOT_DIR / "data/train.csv"
OUTPUT_DIR = ROOT_DIR / "src/track_one/metrics/refiner_benchmarks"
RAW_CSV = OUTPUT_DIR / f"benchmark_{MODEL_CLEAN}_raw.csv"
METRICS_CSV = OUTPUT_DIR / "benchmark_frontier_metrics.csv"

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Your input fields are:
1. `pert` (str): The knocked-out perturbation gene
2. `gene` (str): The target gene to predict
Your output fields are:
1. `reasoning` (str): Step-by-step biological reasoning
2. `label` (str): Final label: exactly 'up', 'down', or 'none'
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## pert ## ]]
{pert}

[[ ## gene ## ]]
{gene}

[[ ## reasoning ## ]]
{reasoning}

[[ ## label ## ]]
{label}

[[ ## completed ## ]]
In adhering to this structure, your objective is: 
        You are an expert molecular biologist who studies how genes are related using Perturb-seq.
        
        Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.
        
        The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs)."""

USER_PROMPT = """[[ ## pert ## ]]
{pert}

[[ ## gene ## ]]
{gene}

Respond with the corresponding output fields, starting with the field `[[ ## reasoning ## ]]`, then `[[ ## label ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`."""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _client() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY missing in .env")
        sys.exit(1)
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def _load_valset() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    
    # Strictly stratify exactly 300 rows (same logic as GEPA evaluate)
    n_rows = 300
    by_label = {label: [r for r in rows if r["label"].strip().lower() == label] for label in LABELS}
    raw_counts = {label: n_rows * len(by_label[label]) / len(rows) for label in LABELS}
    counts = {label: int(raw_counts[label]) for label in LABELS}
    remaining = n_rows - sum(counts.values())
    for label in sorted(LABELS, key=lambda l: raw_counts[l] - counts[l], reverse=True):
        if remaining <= 0:
            break
        counts[label] += 1
        remaining -= 1
        
    subset: list[dict[str, str]] = []
    for label in LABELS:
        subset.extend(by_label[label][: counts[label]])
    return subset


def _row_id(row: dict[str, str]) -> str:
    return row.get("id") or f"{row['pert']}_{row['gene']}"


def _send_one(client: OpenAI, row: dict[str, str]) -> dict[str, Any]:
    sys_msg = SYSTEM_PROMPT.replace("{pert}", "{pert}").replace("{gene}", "{gene}")
    sys_msg = sys_msg.replace("{reasoning}", "{reasoning}").replace("{label}", "{label}")
    
    user_msg = USER_PROMPT.format(pert=row["pert"], gene=row["gene"])

    kwargs = dict(
        model=MODEL,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.0,
        max_tokens=MAX_TOKENS,
        timeout=REQUEST_TIMEOUT,
        logprobs=True,
        top_logprobs=15
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(**kwargs)
            return response.model_dump(mode="json", exclude_unset=True)
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise e
            time.sleep(2 ** attempt)


def _process_one_row(client: OpenAI, row: dict[str, str]) -> dict[str, Any]:
    _wait_for_rate_limit()
    row_id = _row_id(row)
    try:
        data = _send_one(client, row)
        
        import json
        with open(ROOT_DIR / f"debug_{MODEL_CLEAN}_raw_responses.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        
        # Parse using DSPy identical logic
        choices = data.get("choices") or []
        message = choices[0].get("message") or {} if choices else {}
        content = _response_content(data)
        
        # Regex pull out the label
        import re
        matches = list(re.finditer(r"\[\[ ## label ## \]\]\s*(up|down|none)\s*(?:\[\[|$)", content, re.IGNORECASE))
        final_answer = matches[-1].group(1).strip().lower() if matches else "PARSE_FAIL"
        
        # Grab probabilities using evaluate.py logic
        probs = _seed_probabilities(data)
        
        # Fallback to _final_answer_label if regex misses
        if final_answer == "PARSE_FAIL":
            final_answer = _final_answer_label(content) or "PARSE_FAIL"
            
        # If API does not support logprobs, fake the probabilities to allow AUROC math
        if not probs and final_answer in ["up", "down", "none"]:
            probs = {"up": 0.0, "down": 0.0, "none": 0.0}
            probs[final_answer] = 1.0
        return {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "correct_answer": row["label"].strip().lower(),
            "content": content,
            "final_answer": final_answer,
            "probs": probs,
            "ok": final_answer in ["up", "down", "none"],
        }
    except Exception as e:
        print(f"\n[API ERROR]: {e}\n")
        return {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "correct_answer": row["label"].strip().lower(),
            "content": "",
            "final_answer": "REQUEST_FAIL",
            "probs": None,
            "ok": False,
            "error": str(e),
        }

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run() -> None:
    print(f"Running OpenRouter Qwen ({MODEL}) on 300 GEPA Valset rows...")
    print(f"{'─' * 70}")

    rows = _load_valset()
    client = _client()

    results: list[dict[str, Any]] = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(_process_one_row, client, row): row for row in rows}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            # Print streaming result to console exactly like GEPA
            pert, gene = result["pert"], result["gene"]
            pred, true = result["final_answer"], result["correct_answer"]
            probs = result.get("probs")
            
            p_str = ""
            if probs:
                p_str = f"P(U):{probs.get('up', 0.0)} P(D):{probs.get('down', 0.0)}"
            
            if pred == true:
                print(f"✅ CORRECT | {pert:>7} -> {gene:<6} | Pred: {pred:<5} | True: {true:<5} | {p_str}")
            else:
                print(f"❌ INCORRECT | {pert:>7} -> {gene:<6} | Pred: {pred:<5} | True: {true:<5} | {p_str}")
            print("-" * 50)

    # Compute metrics
    valid_results = [r for r in results if r["final_answer"] in ["up", "down", "none"] and r.get("probs")]
    y_true, y_pred = [], []
    de_true, de_score = [], []
    direction_rows = []
    
    for r in valid_results:
        true_lbl = r["correct_answer"]
        pred_lbl = r["final_answer"]
        probs = r["probs"]
        
        y_true.append(true_lbl)
        y_pred.append(pred_lbl)
        
        de_true.append(int(true_lbl != "none"))
        de_score.append(probs.get("up", 0.0) + probs.get("down", 0.0))
        
        if true_lbl != "none":
            direction_rows.append(r)
            
    if y_true:
        label_order = ["up", "down", "none"]
        macro_f1 = f1_score(y_true, y_pred, labels=label_order, average="macro", zero_division=0)
        accuracy = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)
        
        de_auroc = roc_auc_score(de_true, de_score) if len(set(de_true)) == 2 else 0.0
        
        direction_true = [int(r["correct_answer"] == "up") for r in direction_rows]
        direction_score = [r["probs"].get("up", 0.0) / max(r["probs"].get("up", 0.0) + r["probs"].get("down", 0.0), 1e-15) for r in direction_rows]
        direction_auroc = roc_auc_score(direction_true, direction_score) if len(set(direction_true)) == 2 else 0.0
        
        kaggle_score = (de_auroc + direction_auroc) / 2
        
        print(f"\nFinal Macro F1: {macro_f1:.4f} | Accuracy: {accuracy:.4f}")
        print(f"Kaggle Score: {kaggle_score:.4f} (DE AUROC: {de_auroc:.4f}, Dir AUROC: {direction_auroc:.4f})")
    
    # Save CSV
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with RAW_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "pert", "gene", "correct_answer", "final_answer", "probs", "content", "ok", "error"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

if __name__ == "__main__":
    run()
