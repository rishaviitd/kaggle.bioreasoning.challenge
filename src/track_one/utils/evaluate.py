"""Evaluate generated Track A responses against labeled training rows."""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path
from typing import Any

from sklearn.metrics import f1_score, precision_score, roc_auc_score


DEFAULT_GENERATION = Path("src/track_one/output/v0.json")
DEFAULT_METRICS = Path("src/track_one/metrics/v0.json")
TRAIN_DATA = Path("data/train.csv")
LABELS = ("up", "down", "none")
TOKEN_TO_LABEL = {"A": "up", "B": "down", "C": "none"}


def _answer_token_label(token: str, allow_decorated_letter: bool = False) -> str | None:
    stripped = token.strip()
    lowered = stripped.lower()
    if lowered in LABELS:
        return lowered
    if stripped in TOKEN_TO_LABEL:
        return TOKEN_TO_LABEL[stripped]
    if allow_decorated_letter:
        cleaned = stripped.strip('`*_#>"\'<>()[]{}:;,.')
        if cleaned != stripped and len(cleaned) == 1 and cleaned.upper() in TOKEN_TO_LABEL:
            return TOKEN_TO_LABEL[cleaned.upper()]
    return None


def _final_answer_label(content: str) -> str | None:
    exact = _answer_token_label(content)
    if exact:
        return exact

    patterns = [
        # Original patterns
        r"<answer>\s*(up|down|none|[ABCabc])\s*</answer>",
        r"\b(?:final\s+output|final\s+answer|answer|prediction|conclusion|label)\s*[:\-]?\s*\**\s*(up|down|none|[ABCabc])\b",
        r"\*\*\s*([ABCabc])\s*\)",
        r"\b([ABCabc])\s*\)\s*(?:up|down|no significant|none)",
        # Handles newline between keyword and letter, and trailing text like (down-regulated)
        r"\b(?:final\s+(?:output|answer|prediction)|predicted\s+\w+|answer|prediction|conclusion|result|outcome|label)\b[^\n]*\n*\s*[:\-]?\s*\**\s*(up|down|none|[ABCabc])\**\b",
        # Handles bold-wrapped letter after arrow or colon:
        r"(?:→|:)\s*\**\s*(up|down|none|[ABCabc])\**(?:[^a-zA-Z]|$)",
    ]
    for pattern in patterns:
        matches = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
        if matches:
            return _answer_token_label(matches[-1].group(1))

    # Last resort: scan the final 300 chars for a standalone bare letter on its own line, or a bolded letter
    tail = content[-300:] if len(content) > 300 else content
    tail_matches = list(re.finditer(r"(?:^|\n)\s*\**\s*(up|down|none|[ABCabc])\**\s*(?:\n|$)", tail, re.MULTILINE | re.IGNORECASE))
    if tail_matches:
        return _answer_token_label(tail_matches[-1].group(1))
        
    tail_bold_matches = list(re.finditer(r"\*\*\s*(up|down|none|[ABCabc])\s*\*\*", tail, re.IGNORECASE))
    if tail_bold_matches:
        return _answer_token_label(tail_bold_matches[-1].group(1))

    return None


def _probabilities_from_token_item(
    item: dict[str, Any],
    actual_label: str | None,
) -> dict[str, float] | None:
    probabilities: dict[str, float] = {}
    if actual_label and item.get("logprob") is not None:
        probabilities[actual_label] = float(item["logprob"])

    for alternative in item.get("top_logprobs") or []:
        label = _answer_token_label(
            str(alternative.get("token", "")),
            allow_decorated_letter=True,
        )
        logprob = alternative.get("logprob")
        if label and logprob is not None:
            probabilities[label] = max(
                float(logprob),
                probabilities.get(label, float("-inf")),
            )

    if not probabilities:
        return None

    floor = min(probabilities.values()) - 20.0
    logits = [probabilities.get(label, floor) for label in LABELS]
    maximum = max(logits)
    values = [math.exp(value - maximum) for value in logits]
    total = sum(values)
    return {
        label: value / total
        for label, value in zip(LABELS, values)
    }


def _seed_probabilities(response: dict[str, Any]) -> dict[str, float] | None:
    choices = response.get("choices") or []
    if not choices:
        return None

    content = _response_content(response)
    final_label = _final_answer_label(content)
    token_items = (choices[0].get("logprobs") or {}).get("content") or []

    if final_label:
        for item in reversed(token_items):
            actual_label = _answer_token_label(
                str(item.get("token", "")),
                allow_decorated_letter=True,
            )
            if actual_label == final_label:
                return _probabilities_from_token_item(item, actual_label)

    return None


def _load_labels(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as file:
        return {row["id"]: row["label"] for row in csv.DictReader(file)}


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _response_content(response: dict[str, Any]) -> str:
    choices = response.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    content = message.get("content") or ""
    if reasoning and content:
        return f"{reasoning}\n\n{content}"
    return reasoning or content


def _content_label(response: dict[str, Any]) -> str | None:
    content = _response_content(response)
    return _final_answer_label(content)


def _calculate_full_metrics(rows: list[dict[str, Any]]) -> dict[str, float | None]:
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


def _calculate_cost_efficient_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "macro_f1": None,
        "accuracy": None,
        "macro_precision": None,
        "per_class_f1": {label: None for label in LABELS},
        "per_class_precision": {label: None for label in LABELS},
        "per_class_accuracy": {label: None for label in LABELS},
        "seed_agreement_rate": None,
    }
    if not rows:
        return metrics

    true_labels = [row["true_label"] for row in rows]
    predicted_labels = [row["predicted_label"] for row in rows]
    per_class = f1_score(
        true_labels,
        predicted_labels,
        labels=list(LABELS),
        average=None,
        zero_division=0,
    )
    per_class_precision = precision_score(
        true_labels,
        predicted_labels,
        labels=list(LABELS),
        average=None,
        zero_division=0,
    )

    metrics["macro_f1"] = float(
        f1_score(
            true_labels,
            predicted_labels,
            labels=list(LABELS),
            average="macro",
            zero_division=0,
        )
    )
    metrics["accuracy"] = _mean([float(row["correct"]) for row in rows])
    metrics["macro_precision"] = float(
        precision_score(
            true_labels,
            predicted_labels,
            labels=list(LABELS),
            average="macro",
            zero_division=0,
        )
    )
    metrics["per_class_f1"] = {
        label: float(score) for label, score in zip(LABELS, per_class)
    }
    metrics["per_class_precision"] = {
        label: float(score) for label, score in zip(LABELS, per_class_precision)
    }
    metrics["per_class_accuracy"] = {
        label: _mean(
            [
                float(row["correct"])
                for row in rows
                if row["true_label"] == label
            ]
        )
        for label in LABELS
    }
    metrics["seed_agreement_rate"] = _mean(
        [float(row["seed_agreement"]) for row in rows]
    )
    return metrics


def evaluate(
    generation_path: Path = DEFAULT_GENERATION,
    metrics_path: Path = DEFAULT_METRICS,
    train_path: Path = TRAIN_DATA,
    evaluation_type: str = "full",
) -> tuple[dict[str, Any], list[str], list[str]]:
    if evaluation_type not in {"full", "cost_efficient"}:
        raise ValueError("evaluation_type must be full or cost_efficient")

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

        seed_predictions = []
        for seed in (42, 43, 44):
            response = (record.get("responses") or {}).get(str(seed))
            if evaluation_type == "full":
                prediction = _seed_probabilities(response or {})
                failure_reason = f"logprob_extraction_failed_seed_{seed}"
            else:
                prediction = _content_label(response or {})
                failure_reason = f"answer_extraction_failed_seed_{seed}"

            if prediction is None:
                failures.append({"id": row_id, "reason": failure_reason})
                seed_predictions = []
                break

            seed_predictions.append(prediction)
            usage = response.get("usage") or {}
            total_cost += float(usage.get("cost") or 0.0)
            total_tokens += int(usage.get("total_tokens") or 0)

        if len(seed_predictions) != 3:
            continue

        if evaluation_type == "full":
            probabilities = {
                label: _mean([item[label] for item in seed_predictions])
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
                for item in seed_predictions
            ]
            row_extra = {
                "probabilities": probabilities,
                "true_label_probability": probabilities[true_label],
                "confidence": confidence,
                "entropy": entropy,
            }
        else:
            seed_labels = seed_predictions
            predicted_label = max(
                LABELS,
                key=lambda label: (
                    seed_labels.count(label),
                    -LABELS.index(label),
                ),
            )
            row_extra = {"seed_predictions": seed_predictions}

        evaluated_rows.append(
            {
                "id": row_id,
                "true_label": true_label,
                "predicted_label": predicted_label,
                "correct": predicted_label == true_label,
                "seed_agreement": len(set(seed_labels)) == 1,
                **row_extra,
            }
        )

    print(f"Evaluated {len(evaluated_rows)} rows.")
    if evaluation_type == "full":
        metrics = _calculate_full_metrics(evaluated_rows)
        primary_score_name = "kaggle_score"
    else:
        metrics = _calculate_cost_efficient_metrics(evaluated_rows)
        primary_score_name = "macro_f1"
    primary_score = metrics[primary_score_name]
    metrics = {
        "primary_score_name": primary_score_name,
        "primary_score": primary_score,
        **metrics,
    }
    correct_ids = [row["id"] for row in evaluated_rows if row["correct"]]
    incorrect_ids = [row["id"] for row in evaluated_rows if not row["correct"]]

    result = {
        "prompt_version": generation.get("prompt_version", "v0"),
        "evaluation_type": evaluation_type,
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
