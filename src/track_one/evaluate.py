"""Evaluate generated Track A responses against labeled training rows."""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path
from typing import Any

from sklearn.metrics import roc_auc_score


DEFAULT_GENERATION = Path("src/track_one/output/v0.json")
DEFAULT_METRICS = Path("src/track_one/metrics/v0.json")
TRAIN_DATA = Path("data/train.csv")
LABELS = ("up", "down", "none")
TOKEN_TO_LABEL = {"A": "up", "B": "down", "C": "none"}


def _answer_letter(token: str) -> str | None:
    match = re.search(r"(?:^|>)([ABC])$", token.strip().upper())
    return match.group(1) if match else None


def _seed_probabilities(response: dict[str, Any]) -> dict[str, float] | None:
    choices = response.get("choices") or []
    if not choices:
        return None

    token_items = (choices[0].get("logprobs") or {}).get("content") or []
    for item in reversed(token_items):
        probabilities: dict[str, float] = {}
        for alternative in item.get("top_logprobs") or []:
            letter = _answer_letter(str(alternative.get("token", "")))
            logprob = alternative.get("logprob")
            if letter and logprob is not None and letter not in probabilities:
                probabilities[letter] = float(logprob)

        if len(probabilities) < 2:
            continue

        floor = min(probabilities.values()) - 20.0
        logits = [probabilities.get(letter, floor) for letter in ("A", "B", "C")]
        maximum = max(logits)
        values = [math.exp(value - maximum) for value in logits]
        total = sum(values)
        return {
            TOKEN_TO_LABEL[letter]: value / total
            for letter, value in zip(("A", "B", "C"), values)
        }

    return None


def _load_labels(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as file:
        return {row["id"]: row["label"] for row in csv.DictReader(file)}


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _calculate_metrics(rows: list[dict[str, Any]]) -> dict[str, float | None]:
    metrics: dict[str, float | None] = {
        "kaggle_score": None,
        "de_auroc": None,
        "direction_auroc": None,
        "accuracy": None,
        "multiclass_log_loss": None,
        "multiclass_brier_score": None,
        "mean_true_label_probability": None,
        "mean_confidence": None,
        "mean_entropy": None,
        "seed_agreement_rate": None,
    }
    if not rows:
        return metrics

    metrics.update(
        {
            "accuracy": _mean([float(row["correct"]) for row in rows]),
            "multiclass_log_loss": _mean(
                [-math.log(max(row["true_label_probability"], 1e-15)) for row in rows]
            ),
            "multiclass_brier_score": _mean(
                [
                    sum(
                        (
                            row["probabilities"][label]
                            - float(label == row["true_label"])
                        )
                        ** 2
                        for label in LABELS
                    )
                    for row in rows
                ]
            ),
            "mean_true_label_probability": _mean(
                [row["true_label_probability"] for row in rows]
            ),
            "mean_confidence": _mean([row["confidence"] for row in rows]),
            "mean_entropy": _mean([row["entropy"] for row in rows]),
            "seed_agreement_rate": _mean(
                [float(row["seed_agreement"]) for row in rows]
            ),
        }
    )

    de_true = [int(row["true_label"] != "none") for row in rows]
    if len(set(de_true)) == 2:
        de_score = [
            row["probabilities"]["up"] + row["probabilities"]["down"]
            for row in rows
        ]
        metrics["de_auroc"] = float(roc_auc_score(de_true, de_score))

    direction_rows = [row for row in rows if row["true_label"] != "none"]
    direction_true = [
        int(row["true_label"] == "up") for row in direction_rows
    ]
    if direction_rows and len(set(direction_true)) == 2:
        direction_score = [
            row["probabilities"]["up"]
            / (row["probabilities"]["up"] + row["probabilities"]["down"])
            for row in direction_rows
        ]
        metrics["direction_auroc"] = float(
            roc_auc_score(direction_true, direction_score)
        )

    if metrics["de_auroc"] is not None and metrics["direction_auroc"] is not None:
        metrics["kaggle_score"] = (
            metrics["de_auroc"] + metrics["direction_auroc"]
        ) / 2

    return metrics


def evaluate(
    generation_path: Path = DEFAULT_GENERATION,
    metrics_path: Path = DEFAULT_METRICS,
    train_path: Path = TRAIN_DATA,
) -> tuple[dict[str, float | None], list[str], list[str]]:
    print(f"Loading generated responses from {generation_path}...")
    generation = json.loads(generation_path.read_text(encoding="utf-8"))
    labels = _load_labels(train_path)

    evaluated_rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    total_cost = 0.0
    total_tokens = 0

    for record in generation.get("records", []):
        row_id = record["id"]
        true_label = labels.get(row_id)
        if true_label is None:
            failures.append({"id": row_id, "reason": "label_not_found"})
            continue

        seed_probabilities = []
        for seed in (42, 43, 44):
            response = (record.get("responses") or {}).get(str(seed))
            probabilities = _seed_probabilities(response or {})
            if probabilities is None:
                failures.append(
                    {"id": row_id, "reason": f"logprob_extraction_failed_seed_{seed}"}
                )
                seed_probabilities = []
                break

            seed_probabilities.append(probabilities)
            usage = response.get("usage") or {}
            total_cost += float(usage.get("cost") or 0.0)
            total_tokens += int(usage.get("total_tokens") or 0)

        if len(seed_probabilities) != 3:
            continue

        probabilities = {
            label: _mean([item[label] for item in seed_probabilities])
            for label in LABELS
        }
        predicted_label = max(LABELS, key=lambda label: probabilities[label])
        confidence = probabilities[predicted_label]
        entropy = -sum(
            probability * math.log(max(probability, 1e-15))
            for probability in probabilities.values()
        )
        seed_labels = [
            max(LABELS, key=lambda label: item[label])
            for item in seed_probabilities
        ]

        evaluated_rows.append(
            {
                "id": row_id,
                "true_label": true_label,
                "predicted_label": predicted_label,
                "correct": predicted_label == true_label,
                "probabilities": probabilities,
                "true_label_probability": probabilities[true_label],
                "confidence": confidence,
                "entropy": entropy,
                "seed_agreement": len(set(seed_labels)) == 1,
            }
        )

    print(f"Extracted probabilities for {len(evaluated_rows)} rows.")
    metrics = _calculate_metrics(evaluated_rows)
    correct_ids = [row["id"] for row in evaluated_rows if row["correct"]]
    incorrect_ids = [row["id"] for row in evaluated_rows if not row["correct"]]

    result = {
        "prompt_version": generation.get("prompt_version", "v0"),
        "source": str(generation_path),
        "rows_requested": len(generation.get("records", [])),
        "rows_evaluated": len(evaluated_rows),
        "extraction_rate": (
            len(evaluated_rows) / len(generation.get("records", []))
            if generation.get("records")
            else 0.0
        ),
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "metrics": metrics,
        "correct_prediction_ids": correct_ids,
        "incorrect_prediction_ids": incorrect_ids,
        "failures": failures,
        "rows": evaluated_rows,
    }

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved prompt quality metrics to {metrics_path}")
    print(f"Correct predictions: {len(correct_ids)}")
    print(f"Incorrect predictions: {len(incorrect_ids)}")
    return metrics, correct_ids, incorrect_ids
