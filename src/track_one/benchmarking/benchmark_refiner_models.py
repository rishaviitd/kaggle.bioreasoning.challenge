"""Benchmark NVIDIA NIM refiner models on the val set using PROMPT_V7 (CRISPR knockout).

Usage:
    python -B src/track_one/benchmark_refiner_models.py           # full run (150 rows)
    python -B src/track_one/benchmark_refiner_models.py --smoke   # smoke test (3 rows, 1st model)
    python -B src/track_one/benchmark_refiner_models.py 50        # custom row count

Outputs (in src/track_one/metrics/refiner_benchmarks/):
    benchmark_refiner_raw.csv     — per-question reasoning + final answers per model
    benchmark_refiner_metrics.csv — per-model evaluation metrics (F1, accuracy, etc.)
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

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics import f1_score

from src.track_one.utils.evaluate import LABELS, _final_answer_label
from src.track_one.prompts.prompt import PROMPT_V3

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "https://integrate.api.nvidia.com/v1"
TEMPERATURE = 0.0        # non-thinking models: deterministic
TEMPERATURE_THINKING = 1.0   # gpt-oss thinking models
TEMPERATURE_NEMOTRON = 0.6   # nemotron thinking on (NVIDIA recommended)
TOP_P = 1.0
TOP_P_NEMOTRON = 0.95        # nemotron thinking on (NVIDIA recommended)
MAX_TOKENS = 4096
REQUEST_TIMEOUT = 300.0
REASONING_EFFORT = "medium"
MAX_RETRIES = 3

# Empirically confirmed thinking models.
# gpt-oss-*: always think, use extra_body reasoning effort
# nemotron-ultra: thinking toggled via system prompt, use specific temp/top_p
GPT_OSS_MODELS = {
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
}
NEMOTRON_MODELS = {
    "nvidia/nemotron-3-ultra-550b-a55b",
}
# All other models: plain chat at temp=0, no thinking overrides needed.

# 40 RPM free tier limit. To be safe, we strictly enforce 1.6s between API calls globally (37.5 RPM).
MAX_WORKERS = 5
API_LOCK = threading.Lock()
LAST_REQ_TIME = 0.0

def _wait_for_rate_limit() -> None:
    """Strictly enforce a minimum of 1.6 seconds between API calls across all threads."""
    global LAST_REQ_TIME
    with API_LOCK:
        now = time.monotonic()
        elapsed = now - LAST_REQ_TIME
        if elapsed < 1.6:
            time.sleep(1.6 - elapsed)
        LAST_REQ_TIME = time.monotonic()

DATA_PATH = ROOT_DIR / "data/gepa_splits/gepa_val.csv"
OUTPUT_DIR = ROOT_DIR / "src/track_one/metrics/refiner_benchmarks"
RAW_CSV = OUTPUT_DIR / "benchmark_refiner_raw.csv"
METRICS_CSV = OUTPUT_DIR / "benchmark_refiner_metrics.csv"

# Ordered from fastest to slowest based on smoke test latency:
MODELS: list[str] = [
    # "qwen/qwen3.5-122b-a10b",                      # tested: 29s
    "openai/gpt-oss-120b",                          # tested: 34s
    # "nvidia/nemotron-3-ultra-550b-a55b",           # tested: 278s
    # --- Disabled ---
    # "minimaxai/minimax-m2.7",
    # "mistralai/mistral-medium-3.5-128b",
    # "moonshotai/kimi-k2.6",
    # "google/gemma-4-31b-it",
    # "meta/llama-3.3-70b-instruct",
    # "deepseek-ai/deepseek-v4-pro",
    # "deepseek-ai/deepseek-v4-flash",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _nvidia_client() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is missing from the environment")
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def _load_rows(n_rows: int) -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if n_rows >= len(rows):
        return rows
    # Stratified sample across labels
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


def _send_one(client: OpenAI, model: str, row: dict[str, str]) -> dict[str, Any]:
    """Send one request to NVIDIA and return the response dict."""
    prompt = PROMPT_V3.format(pert=row["pert"], gene=row["gene"])

    if model in NEMOTRON_MODELS:
        # Thinking ON via system prompt; NVIDIA recommended settings
        kwargs: dict[str, Any] = dict(
            model=model,
            messages=[
                {"role": "system", "content": "detailed thinking on"},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE_NEMOTRON,
            top_p=TOP_P_NEMOTRON,
            max_tokens=MAX_TOKENS,
            timeout=REQUEST_TIMEOUT,
        )
    elif model in GPT_OSS_MODELS:
        # Thinking ON via extra_body reasoning effort
        kwargs = dict(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE_THINKING,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,
            timeout=REQUEST_TIMEOUT,
            extra_body={"reasoning": {"effort": REASONING_EFFORT}},
        )
    else:
        # Plain chat, no thinking
        kwargs = dict(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,
            timeout=REQUEST_TIMEOUT,
        )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(**kwargs)
            return response.model_dump(mode="json", exclude_unset=True)
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise e
            # Exponential backoff: 2s, 4s, 8s...
            time.sleep(2 ** attempt)


def _extract_text(data: dict[str, Any]) -> tuple[str, str]:
    """Return (reasoning, content) strings from a raw API response."""
    choices = data.get("choices") or []
    message = choices[0].get("message") or {} if choices else {}
    reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    content = message.get("content") or ""
    return str(reasoning).strip(), str(content).strip()


def _process_one_row(
    client: OpenAI,
    model: str,
    row: dict[str, str],
) -> dict[str, Any]:
    """Run one row for one model, strictly adhering to the global rate limit."""
    _wait_for_rate_limit()
    row_id = _row_id(row)
    try:
        data = _send_one(client, model, row)
        reasoning, content = _extract_text(data)
        final_answer = _final_answer_label(content) or _final_answer_label(reasoning)
        return {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "correct_answer": row["label"].strip().lower(),
            "reasoning": reasoning,
            "content": content,
            "final_answer": final_answer or "PARSE_FAIL",
            "ok": final_answer is not None,
        }
    except Exception as exc:
        return {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "correct_answer": row["label"].strip().lower(),
            "reasoning": "",
            "content": "",
            "final_answer": "REQUEST_FAIL",
            "ok": False,
            "error": str(exc),
        }


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def _load_raw_csv() -> dict[str, dict[str, str]]:
    """Load existing raw CSV into a dict keyed by question_id."""
    if not RAW_CSV.exists():
        return {}
    with RAW_CSV.open(newline="", encoding="utf-8") as f:
        return {row["question_id"]: dict(row) for row in csv.DictReader(f)}


def _save_raw_csv(
    data: dict[str, dict[str, str]],
    all_columns: list[str],
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with RAW_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def _append_metrics_row(metrics_row: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = ["model", "accuracy", "macro_f1", "f1_up", "f1_down", "f1_none",
                  "parse_failure_rate", "request_failure_rate", "n_rows", "avg_latency_s"]
    write_header = not METRICS_CSV.exists()
    with METRICS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(metrics_row)


def _compute_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute macro F1, per-class F1, accuracy, parse/request failure rates."""
    y_true, y_pred = [], []
    parse_fails = 0
    request_fails = 0

    for r in results:
        true = r["correct_answer"]
        pred = r["final_answer"]
        if pred == "REQUEST_FAIL":
            request_fails += 1
            continue
        if pred == "PARSE_FAIL":
            parse_fails += 1
            continue
        y_true.append(true)
        y_pred.append(pred)

    n = len(results)
    if not y_true:
        return {
            "accuracy": 0.0, "macro_f1": 0.0,
            "f1_up": 0.0, "f1_down": 0.0, "f1_none": 0.0,
            "parse_failure_rate": parse_fails / n if n else 0.0,
            "request_failure_rate": request_fails / n if n else 0.0,
        }

    label_order = ["up", "down", "none"]
    f1_per_class = f1_score(y_true, y_pred, labels=label_order, average=None, zero_division=0)
    macro_f1 = f1_score(y_true, y_pred, labels=label_order, average="macro", zero_division=0)
    accuracy = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)

    return {
        "accuracy": round(accuracy, 4),
        "macro_f1": round(float(macro_f1), 4),
        "f1_up": round(float(f1_per_class[0]), 4),
        "f1_down": round(float(f1_per_class[1]), 4),
        "f1_none": round(float(f1_per_class[2]), 4),
        "parse_failure_rate": round(parse_fails / n, 4),
        "request_failure_rate": round(request_fails / n, 4),
    }


# ---------------------------------------------------------------------------
# Per-model benchmark
# ---------------------------------------------------------------------------

def _benchmark_model(
    client: OpenAI,
    model: str,
    rows: list[dict[str, str]],
    raw_data: dict[str, dict[str, str]],
    all_columns: list[str],
    model_idx: int,
    total_models: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Run all rows for a single model, update raw_data in-place, return results."""
    safe_name = model.replace("/", "__")
    reasoning_col = f"{safe_name}_reasoning"
    answer_col = f"{safe_name}_final_answer"

    for col in [reasoning_col, answer_col]:
        if col not in all_columns:
            all_columns.append(col)

    short_name = model.split("/")[-1][:40]
    tag = f"  [{model_idx:>2}/{total_models}] {short_name:<40}"

    # Print "running..." at start — stays on same line until overwritten
    print(f"{tag}  running...", end="\r", flush=True)

    results: list[dict[str, Any]] = []
    t_start = time.monotonic()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_process_one_row, client, model, row): row
            for row in rows
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            row_id = result["id"]
            if row_id not in raw_data:
                raw_data[row_id] = {
                    "question_id": row_id,
                    "pert": result["pert"],
                    "gene": result["gene"],
                    "correct_answer": result["correct_answer"],
                }
            raw_data[row_id][reasoning_col] = result["reasoning"]
            raw_data[row_id][answer_col] = result["final_answer"]

    elapsed = time.monotonic() - t_start
    metrics = _compute_metrics(results)
    metrics["model"] = model
    metrics["n_rows"] = len(rows)
    metrics["avg_latency_s"] = round(elapsed / len(rows), 1)

    # Overwrite "running..." with final summary — ends with \n so next model goes below
    fail_str = ""
    if metrics["parse_failure_rate"] > 0:
        fail_str += f"  parse_fail={metrics['parse_failure_rate']:.0%}"
    if metrics["request_failure_rate"] > 0:
        fail_str += f"  req_fail={metrics['request_failure_rate']:.0%}"

    print(
        f"{tag}  "
        f"F1={metrics['macro_f1']:.3f}  "
        f"up={metrics['f1_up']:.2f}  down={metrics['f1_down']:.2f}  none={metrics['f1_none']:.2f}  "
        f"acc={metrics['accuracy']:.2f}{fail_str}  [{elapsed:.0f}s]"
    )

    return results, metrics


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run(n_rows: int = 150, smoke: bool = False) -> None:
    if smoke:
        n_rows = 15
        models = MODELS
        tag = f"SMOKE ({n_rows} rows × {len(models)} models)"
    else:
        models = MODELS
        tag = f"{n_rows} rows × {len(models)} models"

    print(f"NVIDIA Refiner Benchmark  |  {tag}  |  PROMPT_V3")
    print(f"{'─' * 70}")

    rows = _load_rows(n_rows)
    client = _nvidia_client()

    # Load existing raw CSV (for resume support)
    raw_data = _load_raw_csv()

    # Base columns (always present)
    base_cols = ["question_id", "pert", "gene", "correct_answer"]
    all_columns: list[str] = list(base_cols)

    # Seed base rows from val data (ensures all question IDs exist even before first model)
    for row in rows:
        rid = _row_id(row)
        if rid not in raw_data:
            raw_data[rid] = {
                "question_id": rid,
                "pert": row["pert"],
                "gene": row["gene"],
                "correct_answer": row["label"].strip().lower(),
            }

    all_metrics: list[dict[str, Any]] = []

    for idx, model in enumerate(models, start=1):
        results, metrics = _benchmark_model(
            client=client,
            model=model,
            rows=rows,
            raw_data=raw_data,
            all_columns=all_columns,
            model_idx=idx,
            total_models=len(models),
        )
        all_metrics.append(metrics)

        # Incrementally write both CSVs after each model completes
        _save_raw_csv(raw_data, all_columns)
        _append_metrics_row(metrics)

    print(f"\n=== All models complete ===")
    print(f"Raw outputs:  {RAW_CSV}")
    print(f"Metrics:      {METRICS_CSV}")

    if smoke:
        print("\n[SMOKE OK] All checks passed.")


if __name__ == "__main__":
    smoke_mode = "--smoke" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    n = int(args[0]) if args else 150
    run(n_rows=n, smoke=smoke_mode)
