"""Benchmark OpenRouter models on the Track One validation split."""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from tqdm.auto import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.track_one.prompts.prompt import PROMPT_V0


VAL_PATH = Path("data/gepa_splits/gepa_val.csv")
OUTPUT_DIR = Path("src/track_one/metrics/model_benchmarks")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MAX_TOKENS = 30_000
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_WORKERS = 4
LABELS = ["up", "down", "none"]
LETTER_TO_LABEL = {"A": "up", "B": "down", "C": "none"}
MODEL_OVERRIDES = {
    "openai/gpt-5.4-mini": {
        "reasoning_effort": "medium",
        "max_tokens": 30_000,
    },
    "deepseek/deepseek-v4-pro": {
        "reasoning_effort": "high",
        "max_tokens": 8_000,
    },
}


def _model_slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", model).strip("_")


def _reasoning_effort(model: str) -> str | None:
    return MODEL_OVERRIDES.get(model, {}).get("reasoning_effort")


def _max_tokens(model: str) -> int:
    return int(MODEL_OVERRIDES.get(model, {}).get("max_tokens", DEFAULT_MAX_TOKENS))


def _load_val_rows() -> list[dict[str, str]]:
    with VAL_PATH.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _client() -> OpenAI:
    load_dotenv(Path(".env"))
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing from .env")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def _parse_prediction(content: str) -> str:
    text = content or ""
    tail = text[-2000:]

    patterns = [
        r"<answer>\s*([ABCabc]|up|down|none)\s*</answer>",
        r"\bfinal answer\s*[:\-]?\s*([ABCabc]|up|down|none)\b",
        r"\banswer\s*[:\-]?\s*([ABCabc]|up|down|none)\b",
        r"\bprediction\s*[:\-]?\s*([ABCabc]|up|down|none)\b",
        r"\b([ABCabc])\)\s*(up|down|none|up-regulated|down-regulated|no significant effect)",
    ]
    for pattern in patterns:
        match = re.search(pattern, tail, re.IGNORECASE)
        if not match:
            continue
        token = match.group(1).strip()
        if token.upper() in LETTER_TO_LABEL:
            return LETTER_TO_LABEL[token.upper()]
        token = token.lower()
        if token in LABELS:
            return token

    label_matches = list(re.finditer(r"\b(up|down|none)\b", tail, re.IGNORECASE))
    if label_matches:
        return label_matches[-1].group(1).lower()
    return "invalid"


def _send_one(client: OpenAI, model: str, row: dict[str, str]) -> dict[str, Any]:
    row_id = row.get("id") or f"{row['pert']}_{row['gene']}"
    prompt = PROMPT_V0.format(pert=row["pert"], gene=row["gene"])
    reasoning_effort = _reasoning_effort(model)
    max_tokens = _max_tokens(model)
    request = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": max_tokens,
        "timeout": 300,
    }
    if reasoning_effort:
        request["extra_body"] = {"reasoning": {"enabled": True, "effort": reasoning_effort}}

    start = time.monotonic()
    try:
        response = client.chat.completions.create(**request)
        data = response.model_dump(mode="json")
        content = ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
        predicted_label = _parse_prediction(content)
        return {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "true_label": row["label"].strip().lower(),
            "predicted_label": predicted_label,
            "correct": predicted_label == row["label"].strip().lower(),
            "elapsed_seconds": time.monotonic() - start,
            "usage": data.get("usage") or {},
            "response": content,
            "raw_response": data,
            "error": None,
        }
    except Exception as exc:
        return {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "true_label": row["label"].strip().lower(),
            "predicted_label": "invalid",
            "correct": False,
            "elapsed_seconds": time.monotonic() - start,
            "usage": {},
            "response": "",
            "raw_response": None,
            "error": str(exc),
        }


def _metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    true_labels = [row["true_label"] for row in results]
    predicted_labels = [
        row["predicted_label"] if row["predicted_label"] in LABELS else "none"
        for row in results
    ]
    return {
        "rows": len(results),
        "errors": sum(bool(row["error"]) for row in results),
        "invalid_predictions": sum(row["predicted_label"] not in LABELS for row in results),
        "true_label_counts": dict(Counter(true_labels)),
        "predicted_label_counts": dict(Counter(predicted_labels)),
        "accuracy": float(accuracy_score(true_labels, predicted_labels)),
        "macro_f1": float(f1_score(true_labels, predicted_labels, labels=LABELS, average="macro", zero_division=0)),
        "macro_precision": float(precision_score(true_labels, predicted_labels, labels=LABELS, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(true_labels, predicted_labels, labels=LABELS, average="macro", zero_division=0)),
        "per_class_f1": dict(zip(LABELS, map(float, f1_score(true_labels, predicted_labels, labels=LABELS, average=None, zero_division=0)))),
        "per_class_precision": dict(zip(LABELS, map(float, precision_score(true_labels, predicted_labels, labels=LABELS, average=None, zero_division=0)))),
        "per_class_recall": dict(zip(LABELS, map(float, recall_score(true_labels, predicted_labels, labels=LABELS, average=None, zero_division=0)))),
        "confusion_matrix_labels": LABELS,
        "confusion_matrix": confusion_matrix(true_labels, predicted_labels, labels=LABELS).tolist(),
        "total_tokens": sum(int((row["usage"] or {}).get("total_tokens") or 0) for row in results),
        "prompt_tokens": sum(int((row["usage"] or {}).get("prompt_tokens") or 0) for row in results),
        "completion_tokens": sum(int((row["usage"] or {}).get("completion_tokens") or 0) for row in results),
        "total_cost": sum(float((row["usage"] or {}).get("cost") or 0) for row in results),
        "mean_elapsed_seconds": sum(float(row["elapsed_seconds"]) for row in results) / len(results) if results else None,
    }


def benchmark(model: str) -> Path:
    rows = _load_val_rows()
    client = _client()
    reasoning_effort = _reasoning_effort(model)
    max_tokens = _max_tokens(model)
    reasoning_slug = reasoning_effort or "none"
    output_path = OUTPUT_DIR / (
        f"{_model_slug(model)}__prompt_v0__val__reasoning_{reasoning_slug}"
        f"__max_tokens_{max_tokens}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Benchmarking model: {model}")
    print(f"Rows: {len(rows)} from {VAL_PATH}")
    print(f"Prompt: PROMPT_V0")
    print(
        "Settings: "
        f"temperature={TEMPERATURE}, top_p={TOP_P}, max_tokens={max_tokens}, "
        f"reasoning_effort={reasoning_effort or 'none'}"
    )
    print(f"OpenRouter parallel workers: {MAX_WORKERS}")

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(_send_one, client, model, row) for row in rows]
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Benchmark {model}", unit="row", dynamic_ncols=True):
            results.append(future.result())
            partial = {
                "model": model,
                "prompt_version": "PROMPT_V0",
                "settings": {
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "max_tokens": max_tokens,
                    "max_workers": MAX_WORKERS,
                    "reasoning_effort": reasoning_effort,
                },
                "summary": _metrics(results),
                "rows": sorted(results, key=lambda row: row["id"]),
            }
            output_path.write_text(json.dumps(partial, indent=2), encoding="utf-8")

    final = {
        "model": model,
        "prompt_version": "PROMPT_V0",
        "settings": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_tokens": max_tokens,
            "max_workers": MAX_WORKERS,
            "reasoning_effort": reasoning_effort,
        },
        "summary": _metrics(results),
        "rows": sorted(results, key=lambda row: row["id"]),
    }
    output_path.write_text(json.dumps(final, indent=2), encoding="utf-8")
    print("\nBenchmark complete")
    print(json.dumps(final["summary"], indent=2))
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: .venv/bin/python -B src/track_one/benchmark.py <openrouter-model-id> [more-model-ids...]")
    for model_id in sys.argv[1:]:
        benchmark(model_id)
