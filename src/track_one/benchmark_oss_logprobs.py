"""Benchmark OpenRouter GPT-OSS logprob probabilities on a val subset."""

from __future__ import annotations

import csv
import json
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from openrouter import OpenRouter
from tqdm.auto import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from client.openrouter_client import MODEL, PROVIDER, _openrouter_api_key
from src.track_one.evaluate import LABELS, _calculate_full_metrics, _seed_probabilities
from src.track_one.prompts.prompt import PROMPT_V0


VAL_PATH = Path("data/gepa_splits/gepa_val.csv")
OUTPUT_DIR = Path("src/track_one/metrics/oss_logprob_benchmarks")
DEFAULT_ROWS = 75
SEED = 42
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 8_192
REASONING_EFFORT = "high"
TOP_LOGPROBS = 20
MAX_WORKERS = 3
PARSER_VERSION = "final_label_token_v3"
PROMPT_NAME = "PROMPT_V0"
PROMPT_TEMPLATE = PROMPT_V0


def _load_val_rows() -> list[dict[str, str]]:
    with VAL_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _stratified_val_subset(rows: list[dict[str, str]], n_rows: int) -> list[dict[str, str]]:
    if n_rows >= len(rows):
        return rows

    by_label = {label: [row for row in rows if row["label"].strip().lower() == label] for label in LABELS}
    raw_counts = {label: n_rows * len(by_label[label]) / len(rows) for label in LABELS}
    counts = {label: int(raw_counts[label]) for label in LABELS}
    remaining = n_rows - sum(counts.values())
    for label in sorted(LABELS, key=lambda item: raw_counts[item] - counts[item], reverse=True):
        if remaining <= 0:
            break
        counts[label] += 1
        remaining -= 1

    subset: list[dict[str, str]] = []
    for label in LABELS:
        subset.extend(by_label[label][: counts[label]])
    return subset


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _row_id(row: dict[str, str]) -> str:
    return row.get("id") or f"{row['pert']}_{row['gene']}"


def _send_one(client: OpenRouter, row: dict[str, str]) -> dict[str, Any]:
    prompt = PROMPT_TEMPLATE.format(pert=row["pert"], gene=row["gene"])
    start = time.monotonic()
    response = client.chat.send(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        top_p=TOP_P,
        seed=SEED,
        max_tokens=MAX_TOKENS,
        reasoning={"effort": REASONING_EFFORT},
        logprobs=True,
        top_logprobs=TOP_LOGPROBS,
        provider={
            "order": [PROVIDER],
            "allow_fallbacks": False,
            "require_parameters": True,
        },
        timeout_ms=240_000,
    )
    data = response.model_dump(mode="json", exclude_unset=True)
    data["elapsed_seconds"] = time.monotonic() - start
    return data


def _process_row(client: OpenRouter, row: dict[str, str]) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, str] | None]:
    row_id = _row_id(row)
    try:
        response = _send_one(client, row)
        evaluated = _evaluate_response(row, response)
        record = {
            "id": row_id,
            "pert": row["pert"],
            "gene": row["gene"],
            "label": row["label"],
            "response": response,
            "evaluated": evaluated,
        }
        if evaluated is None:
            return record, None, {"id": row_id, "reason": "logprob_extraction_failed"}
        return record, evaluated, None
    except Exception as exc:
        return (
            {
                "id": row_id,
                "pert": row["pert"],
                "gene": row["gene"],
                "label": row["label"],
                "response": None,
                "evaluated": None,
                "error": str(exc),
            },
            None,
            {"id": row_id, "reason": str(exc)},
        )


def _evaluate_response(row: dict[str, str], response: dict[str, Any]) -> dict[str, Any] | None:
    probabilities = _seed_probabilities(response)
    if probabilities is None:
        return None

    true_label = row["label"].strip().lower()
    predicted_label = max(LABELS, key=lambda label: probabilities[label])
    confidence = probabilities[predicted_label]
    entropy = -sum(prob * math.log(max(prob, 1e-15)) for prob in probabilities.values())

    return {
        "id": _row_id(row),
        "true_label": true_label,
        "predicted_label": predicted_label,
        "correct": predicted_label == true_label,
        "seed_agreement": True,
        "probabilities": probabilities,
        "true_label_probability": probabilities[true_label],
        "confidence": confidence,
        "entropy": entropy,
    }


def _write_artifact(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def benchmark(n_rows: int = DEFAULT_ROWS) -> Path:
    rows = _stratified_val_subset(_load_val_rows(), n_rows)
    client = OpenRouter(api_key=_openrouter_api_key())
    output_path = OUTPUT_DIR / f"gpt_oss_120b_val{len(rows)}_seed{SEED}_prompt_v0_logprobs.json"

    print("Starting GPT-OSS OpenRouter logprob benchmark...")
    print(f"Rows: {len(rows)} from {VAL_PATH}")
    print(f"Model: {MODEL}")
    print(f"Provider: {PROVIDER}")
    print(f"Prompt: {PROMPT_NAME}")
    print(
        "Settings: "
        f"temperature={TEMPERATURE}, top_p={TOP_P}, seed={SEED}, "
        f"max_tokens={MAX_TOKENS}, reasoning_effort={REASONING_EFFORT}, "
        f"top_logprobs={TOP_LOGPROBS}"
    )
    print(f"OpenRouter parallel workers: {MAX_WORKERS}")

    evaluated_rows: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    total_cost = 0.0
    total_tokens = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(_process_row, client, row) for row in rows]
        progress = tqdm(
            as_completed(futures),
            total=len(futures),
            desc="GPT-OSS logprob benchmark",
            unit="row",
            dynamic_ncols=True,
        )
        for future in progress:
            record, evaluated, failure = future.result()
            response = record.get("response") or {}
            usage = response.get("usage") or {}
            total_cost += float(usage.get("cost") or 0.0)
            total_tokens += int(usage.get("total_tokens") or 0)
            records.append(record)
            if failure is not None:
                failures.append(failure)
            if evaluated is not None:
                evaluated_rows.append(evaluated)

            progress.set_postfix(
                parsed=len(evaluated_rows),
                failures=len(failures),
                refresh=False,
            )

            metrics = _calculate_full_metrics(evaluated_rows)
            partial = {
                "model": MODEL,
                "provider": PROVIDER,
                "prompt_version": PROMPT_NAME,
                "settings": {
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "seed": SEED,
                    "max_tokens": MAX_TOKENS,
                    "reasoning_effort": REASONING_EFFORT,
                    "top_logprobs": TOP_LOGPROBS,
                    "max_workers": MAX_WORKERS,
                    "parser_version": PARSER_VERSION,
                },
                "rows_requested": len(rows),
                "rows_evaluated": len(evaluated_rows),
                "failures": failures,
                "total_cost": total_cost,
                "total_tokens": total_tokens,
                "metrics": metrics,
                "records": sorted(records, key=lambda item: item["id"]),
            }
            _write_artifact(output_path, partial)

    final_metrics = _calculate_full_metrics(evaluated_rows)
    final = {
        "model": MODEL,
        "provider": PROVIDER,
        "prompt_version": PROMPT_NAME,
        "settings": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "seed": SEED,
            "max_tokens": MAX_TOKENS,
            "reasoning_effort": REASONING_EFFORT,
            "top_logprobs": TOP_LOGPROBS,
            "max_workers": MAX_WORKERS,
            "parser_version": PARSER_VERSION,
        },
        "rows_requested": len(rows),
        "rows_evaluated": len(evaluated_rows),
        "extraction_rate": len(evaluated_rows) / len(rows) if rows else 0.0,
        "failures": failures,
        "total_cost": total_cost,
        "total_tokens": total_tokens,
        "metrics": final_metrics,
        "correct_prediction_ids": [row["id"] for row in evaluated_rows if row["correct"]],
        "incorrect_prediction_ids": [row["id"] for row in evaluated_rows if not row["correct"]],
        "records": sorted(records, key=lambda item: item["id"]),
    }
    _write_artifact(output_path, final)

    print("\nGPT-OSS logprob benchmark complete")
    print(json.dumps(final["metrics"], indent=2))
    print(f"Rows evaluated: {len(evaluated_rows)}/{len(rows)}")
    print(f"Parsing/request failures: {len(failures)}")
    if failures:
        print("Failure ids:")
        for failure in failures:
            print(f"- {failure['id']}: {failure['reason']}")
    print(f"Total tokens: {total_tokens}")
    print(f"Total cost: {total_cost:.6f}")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    rows = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROWS
    benchmark(rows)
