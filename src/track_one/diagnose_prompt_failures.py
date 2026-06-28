"""Diagnose PROMPT_V0 failures on a balanced train sample."""

from __future__ import annotations

import csv
import json
import random
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from openrouter import OpenRouter
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from tqdm.auto import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from client.openrouter_client import MODEL, PROVIDER, _openrouter_api_key
from src.track_one.prompts.prompt import PROMPT_V0


TRAIN_PATH = Path("data/gepa_splits/gepa_train.csv")
OUTPUT_DIR = Path("src/track_one/metrics/prompt_diagnostics")
LABELS = ["up", "down", "none"]
LETTER_TO_LABEL = {"A": "up", "B": "down", "C": "none"}
ROWS_PER_LABEL = {"up": 17, "down": 17, "none": 16}
RANDOM_SEED = 42
DEFAULT_BATCH_INDEX = 2
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 8_192
REASONING_EFFORT = "high"
MAX_WORKERS = 3
PROMPT_NAME = "PROMPT_V0"
PROMPT_TEMPLATE = PROMPT_V0


def _load_rows() -> list[dict[str, str]]:
    with TRAIN_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _sample_balanced_rows(rows: list[dict[str, str]], batch_index: int) -> list[dict[str, str]]:
    by_label = {label: [row for row in rows if row["label"].strip().lower() == label] for label in LABELS}
    sampled: list[dict[str, str]] = []
    for label in LABELS:
        label_rows = by_label[label]
        rows_needed = ROWS_PER_LABEL[label]
        if len(label_rows) < rows_needed:
            raise ValueError(f"Not enough {label} rows: need {rows_needed}, found {len(label_rows)}")
        shuffled = list(label_rows)
        random.Random(RANDOM_SEED + batch_index * 1009 + LABELS.index(label)).shuffle(shuffled)
        sampled.extend(shuffled[:rows_needed])
    return sampled


def _response_content(response: dict[str, Any]) -> str:
    choices = response.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return message.get("content") or ""


def _parse_prediction(content: str) -> str:
    tail = (content or "")[-2000:]
    patterns = [
        r"<answer>\s*([ABCabc]|up|down|none)\s*</answer>",
        r"\b(?:final\s+answer|answer|prediction|conclusion)\s*[:\-]?\s*\**\s*([ABCabc]|up|down|none)\b",
        r"\*\*\s*([ABCabc])\s*\)",
        r"\b([ABCabc])\s*\)\s*(?:up|down|no significant|none)",
        r"\b(up|down|none)\b",
    ]
    for pattern in patterns:
        matches = list(re.finditer(pattern, tail, re.IGNORECASE))
        if not matches:
            continue
        token = matches[-1].group(1).strip()
        if token.upper() in LETTER_TO_LABEL:
            return LETTER_TO_LABEL[token.upper()]
        token = token.lower()
        if token in LABELS:
            return token
    return "invalid"


def _run_row(client: OpenRouter, row: dict[str, str]) -> dict[str, Any]:
    prompt = PROMPT_TEMPLATE.format(pert=row["pert"], gene=row["gene"])
    response = client.chat.send(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
        reasoning={"effort": REASONING_EFFORT},
        provider={
            "order": [PROVIDER],
            "allow_fallbacks": False,
            "require_parameters": True,
        },
        timeout_ms=240_000,
    )
    response = response.model_dump(mode="json", exclude_unset=True)
    content = _response_content(response)
    predicted_label = _parse_prediction(content)
    true_label = row["label"].strip().lower()
    return {
        "id": row["id"],
        "pert": row["pert"],
        "gene": row["gene"],
        "true_label": true_label,
        "predicted_label": predicted_label,
        "correct": predicted_label == true_label,
        "prompt": prompt,
        "response_content": content,
        "response": response,
    }


def _metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    true_labels = [row["true_label"] for row in results]
    predicted_labels = [
        row["predicted_label"] if row["predicted_label"] in LABELS else "none"
        for row in results
    ]
    return {
        "rows": len(results),
        "correct": sum(row["correct"] for row in results),
        "incorrect": sum(not row["correct"] for row in results),
        "accuracy": sum(row["correct"] for row in results) / len(results) if results else None,
        "macro_f1": float(f1_score(true_labels, predicted_labels, labels=LABELS, average="macro", zero_division=0)),
        "macro_precision": float(precision_score(true_labels, predicted_labels, labels=LABELS, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(true_labels, predicted_labels, labels=LABELS, average="macro", zero_division=0)),
        "per_class_f1": dict(zip(LABELS, map(float, f1_score(true_labels, predicted_labels, labels=LABELS, average=None, zero_division=0)))),
        "per_class_precision": dict(zip(LABELS, map(float, precision_score(true_labels, predicted_labels, labels=LABELS, average=None, zero_division=0)))),
        "per_class_recall": dict(zip(LABELS, map(float, recall_score(true_labels, predicted_labels, labels=LABELS, average=None, zero_division=0)))),
        "true_label_counts": dict(Counter(true_labels)),
        "predicted_label_counts": dict(Counter(predicted_labels)),
        "confusion_matrix_labels": LABELS,
        "confusion_matrix": confusion_matrix(true_labels, predicted_labels, labels=LABELS).tolist(),
    }


def _write_artifact(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _artifact_payload(
    results: list[dict[str, Any]],
    batch_index: int,
) -> dict[str, Any]:
    return {
        "prompt_version": PROMPT_NAME,
        "sample": {
            "source": str(TRAIN_PATH),
            "rows_per_label": ROWS_PER_LABEL,
            "random_seed": RANDOM_SEED,
            "batch_index": batch_index,
        },
        "settings": {
            "model": MODEL,
            "provider": PROVIDER,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_tokens": MAX_TOKENS,
            "reasoning_effort": REASONING_EFFORT,
            "max_workers": MAX_WORKERS,
        },
        "metrics": _metrics(results),
        "wrong_rows": [item for item in results if not item["correct"]],
        "rows": sorted(results, key=lambda item: item["id"]),
    }


def diagnose(batch_index: int = DEFAULT_BATCH_INDEX) -> Path:
    rows = _sample_balanced_rows(_load_rows(), batch_index)
    client = OpenRouter(api_key=_openrouter_api_key())
    output_path = OUTPUT_DIR / f"v0_train50_balanced_batch{batch_index:02d}_openrouter.json"

    print(f"Starting {PROMPT_NAME} failure diagnosis...")
    print(f"Train rows: {TRAIN_PATH}")
    print(f"Prompt: {PROMPT_NAME}")
    print(f"Sample: batch={batch_index}, rows_per_label={ROWS_PER_LABEL}, total={len(rows)}")
    print(
        "Student settings: "
        f"model={MODEL}, provider={PROVIDER}, temperature={TEMPERATURE}, top_p={TOP_P}, "
        f"max_tokens={MAX_TOKENS}, reasoning_effort={REASONING_EFFORT}, max_workers={MAX_WORKERS}"
    )

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(_run_row, client, row) for row in rows]
        progress = tqdm(
            as_completed(futures),
            total=len(futures),
            desc=f"Diagnosing {PROMPT_NAME}",
            unit="row",
            dynamic_ncols=True,
        )
        for future in progress:
            results.append(future.result())
            _write_artifact(output_path, _artifact_payload(results, batch_index))

    final = _artifact_payload(results, batch_index)
    _write_artifact(output_path, final)

    print(f"\n{PROMPT_NAME} diagnosis complete")
    print(json.dumps(final["metrics"], indent=2))
    print("\nWrong rows:")
    for row in final["wrong_rows"]:
        print(f"- {row['id']}: true={row['true_label']}, predicted={row['predicted_label']}")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    arg_batch_index = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BATCH_INDEX
    diagnose(arg_batch_index)
