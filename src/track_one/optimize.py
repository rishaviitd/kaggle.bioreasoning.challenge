import pandas as pd
import dspy
import contextlib
import io
import json
import logging
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any

from gepa import GEPAResult, optimize
from gepa.strategies.instruction_proposal import InstructionProposalSignature

from dspy.teleprompt.gepa.gepa_utils import DspyAdapter, LoggerAdapter
from dspy.teleprompt.gepa.gepa import DspyGEPAResult

from src.track_one.gepa_config import get_student_lm, get_refiner_lm
from src.track_one.gepa_metric import gepa_exact_match_metric


TRAIN_DATA = Path("data/gepa_splits/gepa_train.csv")
VAL_DATA = Path("data/gepa_splits/gepa_val.csv")
GEPA_LOG_DIR = "src/track_one/metrics/gepa_logs"
OPTIMIZED_STUDENT_PATH = "src/track_one/prompts/optimized_trackA_student.json"
CANDIDATE_EXPORT_DIR = Path("src/track_one/prompts/gepa_candidates")
ARTIFACT_EXPORT_DIR = Path("src/track_one/metrics/gepa_artifacts")
LABELS = ("none", "up", "down")
STRATIFIED_MINIBATCH_COUNTS = {"none": 6, "up": 6, "down": 6}
REFLECTION_MINIBATCH_SIZE = sum(STRATIFIED_MINIBATCH_COUNTS.values())
TRAIN_LIMIT = None
VAL_LIMIT = None
FIRST_RUN_METRIC_CALL_BUDGET = 1500
GEPA_PERFECT_SCORE = 1.0
REFINER_PROMPT_TEMPLATE = """I provided an assistant with the following instructions to perform a task:
```
<curr_instructions>
```

The following are training examples with the assistant's response and feedback:
```
<inputs_outputs_feedback>
```

Write a full replacement instruction for the assistant.

Strict anti-memorization rules:
- Do not include any exact perturbation gene symbol, target gene symbol, or perturbation-target pair from the examples.
- Do not add few-shot examples.
- Do not encode row-specific labels or row-specific decisions.
- Convert feedback into general decision rules only.
- Keep rules applicable to unseen gene pairs.
- If a feedback item mentions a concrete gene, generalize it to the gene's functional class or pathway.

The instruction may include:
- the task definition,
- the valid labels,
- general biological reasoning rules,
- general pathway or mechanism categories,
- output formatting requirements.

Return only the complete new instruction inside ``` blocks."""


def _mean_score(scores: list[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0


def _label(value: object) -> str:
    return str(value).strip().lower()


def _prediction_label(output: Any) -> str:
    if isinstance(output, dict):
        return _label(output.get("prediction", ""))
    if hasattr(output, "get"):
        try:
            return _label(output.get("prediction", ""))
        except Exception:
            pass
    return _label(getattr(output, "prediction", ""))


def _field_value(item: Any, field: str) -> Any:
    if isinstance(item, dict):
        return item.get(field)
    if hasattr(item, "get"):
        try:
            return item.get(field)
        except Exception:
            pass
    return getattr(item, field, None)


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_jsonable(item) for item in value]
    if hasattr(value, "toDict"):
        return _jsonable(value.toDict())
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump(mode="json"))
    return str(value)


def _candidate_instructions(candidate: Any) -> dict[str, str]:
    if isinstance(candidate, dict):
        return {str(key): str(value) for key, value in candidate.items()}
    if hasattr(candidate, "named_predictors"):
        return {
            name: pred.signature.instructions
            for name, pred in candidate.named_predictors()
        }
    return {"candidate": str(candidate)}


def _safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _mean_present(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return sum(present) / len(present) if present else None


def _metric_text(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def _binary_recall(rows: list[dict[str, Any]], positive_fn, predicted_positive_fn) -> float | None:
    positives = [row for row in rows if positive_fn(row["true_label"])]
    if not positives:
        return None
    return sum(float(predicted_positive_fn(row["predicted_label"])) for row in positives) / len(positives)


def _evaluation_diagnostics(
    inputs: list[Any],
    outputs: list[Any],
    scores: list[float],
) -> dict[str, Any]:
    rows = []
    for index, (example, output, score) in enumerate(zip(inputs, outputs, scores, strict=False)):
        true_label = _label(_field_value(example, "label"))
        predicted_label = _prediction_label(output)
        rows.append(
            {
                "index": index,
                "pert": _field_value(example, "pert"),
                "gene": _field_value(example, "gene"),
                "true_label": true_label,
                "predicted_label": predicted_label,
                "correct": predicted_label == true_label,
                "row_score": score,
            }
        )

    total = len(rows)
    accuracy = _safe_divide(sum(float(row["correct"]) for row in rows), total)
    true_counts = Counter(row["true_label"] for row in rows)
    predicted_counts = Counter(row["predicted_label"] for row in rows)
    confusion = {
        true_label: {
            predicted_label: sum(
                1
                for row in rows
                if row["true_label"] == true_label and row["predicted_label"] == predicted_label
            )
            for predicted_label in LABELS
        }
        for true_label in LABELS
    }

    per_class = {}
    for label in LABELS:
        tp = sum(1 for row in rows if row["true_label"] == label and row["predicted_label"] == label)
        fp = sum(1 for row in rows if row["true_label"] != label and row["predicted_label"] == label)
        fn = sum(1 for row in rows if row["true_label"] == label and row["predicted_label"] != label)
        precision = _safe_divide(tp, tp + fp) or 0.0
        recall = _safe_divide(tp, tp + fn) or 0.0
        f1 = 0.0
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        per_class[label] = {
            "support": true_counts.get(label, 0),
            "predicted": predicted_counts.get(label, 0),
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    non_de_recall = _binary_recall(rows, lambda label: label == "none", lambda pred: pred == "none")
    de_recall = _binary_recall(rows, lambda label: label in {"up", "down"}, lambda pred: pred in {"up", "down"})
    up_recall = _binary_recall(rows, lambda label: label == "up", lambda pred: pred == "up")
    down_recall = _binary_recall(rows, lambda label: label == "down", lambda pred: pred == "down")
    de_hard_score = _mean_present([non_de_recall, de_recall])
    dir_hard_score = _mean_present([up_recall, down_recall])
    hard_proxy_score = _mean_present([de_hard_score, dir_hard_score])

    return {
        "summary": {
            "primary_score": _mean_score(scores),
            "score_sum": sum(scores),
            "accuracy": accuracy,
            "macro_precision": _mean_present([per_class[label]["precision"] for label in LABELS]),
            "macro_recall": _mean_present([per_class[label]["recall"] for label in LABELS]),
            "macro_f1": _mean_present([per_class[label]["f1"] for label in LABELS]),
            "de_hard_score": de_hard_score,
            "dir_hard_score": dir_hard_score,
            "hard_proxy_score": hard_proxy_score,
            "non_de_recall": non_de_recall,
            "de_recall": de_recall,
            "up_recall": up_recall,
            "down_recall": down_recall,
        },
        "per_class": per_class,
        "true_label_counts": dict(true_counts),
        "predicted_label_counts": dict(predicted_counts),
        "confusion": confusion,
        "rows": rows,
    }


def _call_reflection_lm(prompt: str) -> str:
    response = dspy.settings.lm(prompt)
    if isinstance(response, list):
        return str(response[0])
    return str(response)


def anti_memorization_instruction_proposer(
    candidate: dict[str, str],
    reflective_dataset: dict[str, list[dict[str, Any]]],
    components_to_update: list[str],
) -> dict[str, str]:
    new_texts = {}
    for name in components_to_update:
        if name not in reflective_dataset or not reflective_dataset[name]:
            continue
        new_texts[name] = InstructionProposalSignature.run(
            lm=_call_reflection_lm,
            input_dict={
                "current_instruction_doc": candidate[name],
                "dataset_with_feedback": reflective_dataset[name],
                "prompt_template": REFINER_PROMPT_TEMPLATE,
            },
        )["new_instruction"]
    return new_texts


class StratifiedLabelBatchSampler:
    def __init__(self, counts_per_label: dict[str, int], seed: int = 42):
        self.counts_per_label = dict(counts_per_label)
        self.rng = random.Random(seed)
        self._pools: dict[str, list[int]] = {}
        self._cursor: dict[str, int] = {}
        self._loader_size: int | None = None

    def _refresh(self, loader) -> None:
        ids = list(loader.all_ids())
        examples = loader.fetch(ids)
        pools = {label: [] for label in self.counts_per_label}
        for data_id, example in zip(ids, examples, strict=False):
            label = _label(getattr(example, "label", ""))
            if label in pools:
                pools[label].append(data_id)

        for label, required_count in self.counts_per_label.items():
            if len(pools[label]) < required_count:
                raise ValueError(
                    f"Need at least {required_count} '{label}' rows for a stratified "
                    f"minibatch, found {len(pools[label])}."
                )
            self.rng.shuffle(pools[label])

        self._pools = pools
        self._cursor = {label: 0 for label in self.counts_per_label}
        self._loader_size = len(loader)

    def _take(self, label: str, count: int) -> list[int]:
        selected = []
        pool = self._pools[label]
        while len(selected) < count:
            cursor = self._cursor[label]
            if cursor >= len(pool):
                self.rng.shuffle(pool)
                cursor = 0
            remaining = count - len(selected)
            available = min(remaining, len(pool) - cursor)
            selected.extend(pool[cursor:cursor + available])
            self._cursor[label] = cursor + available
        return selected

    def next_minibatch_ids(self, loader, state) -> list[int]:
        if self._loader_size != len(loader):
            self._refresh(loader)

        batch = []
        for label, count in self.counts_per_label.items():
            batch.extend(self._take(label, count))
        self.rng.shuffle(batch)
        return batch


class GEPASummaryLogger:
    def __init__(
        self,
        candidate_dir: Path,
        artifact_dir: Path,
        student_lm: Any | None = None,
        valset_size: int = 0,
        valset: list[Any] | None = None,
    ):
        self.candidate_dir = candidate_dir
        self.artifact_dir = artifact_dir
        self.student_lm = student_lm
        self.valset_size = valset_size
        self.valset = valset or []
        self._eval_inputs: dict[tuple[int, int | None, bool], list[Any]] = {}
        self._current_scores: dict[int, list[float]] = {}
        self._new_scores: dict[int, list[float]] = {}
        self._proposed_instructions: dict[int, dict[str, str]] = {}

    def _score_text(self, score: float) -> str:
        return f"{score:.3f}".replace(".", "p")

    def _write_json(self, root: Path, filename: str, payload: dict[str, Any]) -> None:
        root.mkdir(parents=True, exist_ok=True)
        path = root / filename
        path.write_text(json.dumps(_jsonable(payload), indent=2), encoding="utf-8")

    def _write_candidate(self, filename: str, payload: dict[str, Any]) -> None:
        self._write_json(self.candidate_dir, filename, payload)

    def _write_artifact(self, filename: str, payload: dict[str, Any]) -> None:
        self._write_json(self.artifact_dir, filename, payload)

    def on_optimization_start(self, event: dict[str, Any]) -> None:
        print(
            "\nGEPA start: "
            f"train={event['trainset_size']}, val={event['valset_size']}, "
            f"minibatch={REFLECTION_MINIBATCH_SIZE}"
        )

    def on_candidate_selected(self, event: dict[str, Any]) -> None:
        print(
            f"\nIteration {event['iteration']}: "
            f"selected candidate {event['candidate_idx']} "
            f"(val score={event['score']:.3f})"
        )

    def on_minibatch_sampled(self, event: dict[str, Any]) -> None:
        row_ids = ", ".join(str(row_id) for row_id in event["minibatch_ids"])
        batch_text = ", ".join(
            f"{count} {label}" for label, count in STRATIFIED_MINIBATCH_COUNTS.items()
        )
        print(
            "  train minibatch: "
            f"{len(event['minibatch_ids'])} rows "
            f"({batch_text}) [{row_ids}]"
        )

    def on_evaluation_start(self, event: dict[str, Any]) -> None:
        key = (event["iteration"], event["candidate_idx"], event["capture_traces"])
        self._eval_inputs[key] = event["inputs"]

    def on_budget_updated(self, event: dict[str, Any]) -> None:
        remaining = event["metric_calls_remaining"]
        remaining_text = "unknown" if remaining is None else str(remaining)
        print(
            "  budget: "
            f"used={event['metric_calls_used']}, "
            f"delta={event['metric_calls_delta']}, "
            f"remaining={remaining_text}"
        )

    def on_evaluation_end(self, event: dict[str, Any]) -> None:
        iteration = event["iteration"]
        scores = [float(score) for score in event["scores"]]
        if event["candidate_idx"] is not None:
            inputs = self._eval_inputs.get((iteration, event["candidate_idx"], True), [])
            diagnostics = _evaluation_diagnostics(inputs, event["outputs"], scores)
            self._current_scores[iteration] = scores
            self._write_artifact(
                f"iter_{iteration:04d}_generate_current_score_{self._score_text(_mean_score(scores))}.json",
                {
                    "stage": "generate_current",
                    "iteration": iteration,
                    "candidate_idx": event["candidate_idx"],
                    "batch_size": len(inputs) or len(scores),
                    "scores": scores,
                    "diagnostics": diagnostics,
                    "inputs": inputs,
                    "outputs": event["outputs"],
                    "has_trajectories": event["has_trajectories"],
                },
            )
            summary = diagnostics["summary"]
            print(
                "  current prompt macro_f1 score: "
                f"{_mean_score(scores):.3f} "
                f"(acc={_metric_text(summary['accuracy'])}, "
                f"macro_f1={_metric_text(summary['macro_f1'])}, rows={len(scores)})"
            )
        else:
            inputs = self._eval_inputs.get((iteration, None, False), [])
            diagnostics = _evaluation_diagnostics(inputs, event["outputs"], scores)
            self._new_scores[iteration] = scores
            self._write_artifact(
                f"iter_{iteration:04d}_evaluate_proposed_score_{self._score_text(_mean_score(scores))}.json",
                {
                    "stage": "evaluate_proposed",
                    "iteration": iteration,
                    "batch_size": len(inputs) or len(scores),
                    "scores": scores,
                    "diagnostics": diagnostics,
                    "inputs": inputs,
                    "outputs": event["outputs"],
                },
            )
            summary = diagnostics["summary"]
            print(
                "  proposed prompt macro_f1 score: "
                f"{_mean_score(scores):.3f} "
                f"(acc={_metric_text(summary['accuracy'])}, "
                f"macro_f1={_metric_text(summary['macro_f1'])}, rows={len(scores)})"
            )
            old_scores = self._current_scores.get(iteration, [])
            old_sum = sum(old_scores)
            new_sum = sum(scores)
            if new_sum > old_sum and self.valset_size:
                print(
                    "  proposed prompt improved on minibatch: "
                    f"{_mean_score(old_scores):.3f} -> {_mean_score(scores):.3f}"
                )
                print(f"  validating proposed candidate on {self.valset_size} val rows next...")
                if hasattr(self.student_lm, "start_progress"):
                    self.student_lm.start_progress(
                        f"candidate validation iter {iteration}",
                        self.valset_size,
                    )

    def on_reflective_dataset_built(self, event: dict[str, Any]) -> None:
        feedback_count = sum(len(items) for items in event["dataset"].values())
        self._write_artifact(
            f"iter_{event['iteration']:04d}_feedback_examples_{feedback_count:03d}.json",
            {
                "stage": "feedback",
                "iteration": event["iteration"],
                "candidate_idx": event["candidate_idx"],
                "components": event["components"],
                "feedback_examples": event["dataset"],
            },
        )
        print(f"  feedback examples prepared: {feedback_count}")
        print("  refiner: requesting updated instruction text...")

    def on_proposal_end(self, event: dict[str, Any]) -> None:
        self._proposed_instructions[event["iteration"]] = dict(event["new_instructions"])
        self._write_artifact(
            f"iter_{event['iteration']:04d}_refine_proposal.json",
            {
                "stage": "refine",
                "iteration": event["iteration"],
                "new_instructions": event["new_instructions"],
            },
        )
        print("  refiner proposed updated instruction text")

    def on_candidate_accepted(self, event: dict[str, Any]) -> None:
        print(
            f"  accepted candidate {event['new_candidate_idx']} "
            f"(macro_f1 batch sum={event['new_score']:.3f})"
        )

    def on_candidate_rejected(self, event: dict[str, Any]) -> None:
        iteration = event["iteration"]
        new_scores = self._new_scores.get(iteration, [])
        old_scores = self._current_scores.get(iteration, [])
        new_avg = _mean_score(new_scores) if new_scores else 0.0
        old_avg = _mean_score(old_scores) if old_scores else 0.0

        if iteration in self._proposed_instructions:
            filename = (
                f"iter_{iteration:04d}_rejected_"
                f"batch_{self._score_text(new_avg)}_"
                f"old_{self._score_text(old_avg)}.json"
            )
            self._write_candidate(
                filename,
                {
                    "status": "rejected",
                    "iteration": iteration,
                    "old_batch_score": old_avg,
                    "new_batch_score": new_avg,
                    "old_batch_sum": event["old_score"],
                    "new_batch_sum": event["new_score"],
                    "instructions": self._proposed_instructions[iteration],
                    "reason": event["reason"],
                },
            )

        print(
            "  rejected proposal: "
            f"old macro_f1 sum={event['old_score']:.3f}, "
            f"new macro_f1 sum={event['new_score']:.3f}"
        )

    def on_valset_evaluated(self, event: dict[str, Any]) -> None:
        outputs_by_row = event["outputs_by_val_id"] or {}
        scores_by_row = event["scores_by_val_id"]
        ordered_ids = sorted(int(row_id) for row_id in scores_by_row)
        outputs = [outputs_by_row.get(row_id) for row_id in ordered_ids]
        outputs = [
            output if output is not None else outputs_by_row.get(str(row_id))
            for row_id, output in zip(ordered_ids, outputs, strict=False)
        ]
        scores = [
            float(scores_by_row.get(row_id, scores_by_row.get(str(row_id))))
            for row_id in ordered_ids
        ]
        inputs = [
            self.valset[row_id]
            for row_id in ordered_ids
            if row_id < len(self.valset)
        ]
        diagnostics = (
            _evaluation_diagnostics(inputs, outputs, scores)
            if inputs and event["outputs_by_val_id"]
            else None
        )
        filename = (
            f"iter_{event['iteration']:04d}_candidate_{event['candidate_idx']:03d}_"
            f"val_{self._score_text(event['average_score'])}.json"
        )
        self._write_candidate(
            filename,
            {
                "status": "validated",
                "iteration": event["iteration"],
                "candidate_idx": event["candidate_idx"],
                "val_score": event["average_score"],
                "num_examples_evaluated": event["num_examples_evaluated"],
                "total_valset_size": event["total_valset_size"],
                "is_best_program": event["is_best_program"],
                "parent_ids": event["parent_ids"],
                "val_scores_by_row": event["scores_by_val_id"],
                "val_outputs_by_row": event["outputs_by_val_id"],
                "diagnostics": diagnostics,
                "instructions": event["candidate"],
            },
        )
        metric_text = ""
        if diagnostics:
            summary = diagnostics["summary"]
            metric_text = (
                f", acc={_metric_text(summary['accuracy'])}, "
                f"macro_f1={_metric_text(summary['macro_f1'])}"
            )
        print(
            "\n  val evaluation: "
            f"candidate {event['candidate_idx']} macro_f1={event['average_score']:.3f} "
            f"({event['num_examples_evaluated']}/{event['total_valset_size']} rows{metric_text})"
        )

    def on_optimization_end(self, event: dict[str, Any]) -> None:
        print(
            "\nGEPA summary: "
            f"best_candidate={event['best_candidate_idx']}, "
            f"iterations={event['total_iterations']}, "
            f"metric_calls={event['total_metric_calls']}"
        )


class PredictInteraction(dspy.Signature):
    """You are a biological reasoning assistant. You must predict whether the biological perturbation regulates the target gene. Think step by step about known biological pathways. Your final prediction must be exactly one of: 'up', 'down', or 'none'."""

    pert = dspy.InputField(desc="The CRISPRi knockdown gene.")
    gene = dspy.InputField(desc="The target gene whose expression is predicted.")

    reasoning = dspy.OutputField(desc="Reasoning about the pathway and interaction.")
    prediction = dspy.OutputField(desc="The interaction label. Must be exactly 'up', 'down', or 'none'.")


class TrackAStudent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(PredictInteraction)

    def forward(self, pert: str, gene: str):
        return self.predict(pert=pert, gene=gene)


class MacroF1DspyAdapter(DspyAdapter):
    def __init__(
        self,
        *args,
        progress_lm: Any | None = None,
        minibatch_size: int = REFLECTION_MINIBATCH_SIZE,
        valset_size: int = 0,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.progress_lm = progress_lm
        self.minibatch_size = minibatch_size
        self.valset_size = valset_size

    def _progress_label(self, batch_size: int, capture_traces: bool) -> str:
        if capture_traces:
            return "current minibatch"
        if batch_size == self.minibatch_size:
            return "proposed minibatch"
        if batch_size == self.valset_size:
            return "candidate validation"
        return "student batch"

    def evaluate(self, batch, candidate, capture_traces=False):
        if (
            self.progress_lm is not None
            and hasattr(self.progress_lm, "start_progress")
            and not getattr(self.progress_lm, "has_progress", lambda: False)()
        ):
            self.progress_lm.start_progress(
                self._progress_label(len(batch), capture_traces),
                len(batch),
            )
        with contextlib.redirect_stdout(io.StringIO()):
            result = super().evaluate(batch, candidate, capture_traces=capture_traces)
        diagnostics = _evaluation_diagnostics(batch, result.outputs, result.scores)
        macro_f1 = diagnostics["summary"]["macro_f1"] or 0.0
        result.scores = [macro_f1 for _ in result.scores]
        return result


class MacroF1GEPA(dspy.GEPA):
    def compile(
        self,
        student: dspy.Module,
        *,
        trainset: list[dspy.Example],
        teacher: dspy.Module | None = None,
        valset: list[dspy.Example] | None = None,
    ) -> dspy.Module:
        assert trainset is not None and len(trainset) > 0, "Trainset must be provided and non-empty"
        assert teacher is None, "Teacher is not supported in DspyGEPA yet."

        if self.max_metric_calls is None:
            raise ValueError("MacroF1GEPA currently expects max_metric_calls to be set.")

        valset = valset or trainset
        rng = random.Random(self.seed)

        def feedback_fn_creator(pred_name: str, predictor):
            def feedback_fn(
                predictor_output: dict[str, Any],
                predictor_inputs: dict[str, Any],
                module_inputs: dspy.Example,
                module_outputs: dspy.Prediction,
                captured_trace,
            ):
                trace_for_pred = [(predictor, predictor_inputs, predictor_output)]
                result = self.metric_fn(
                    module_inputs,
                    module_outputs,
                    captured_trace,
                    pred_name,
                    trace_for_pred,
                )
                if hasattr(result, "feedback"):
                    if result["feedback"] is None:
                        result["feedback"] = f"This trajectory got a score of {result['score']}."
                    return result
                return dict(score=result, feedback=f"This trajectory got a score of {result}.")

            return feedback_fn

        feedback_map = {name: feedback_fn_creator(name, predictor) for name, predictor in student.named_predictors()}
        adapter = MacroF1DspyAdapter(
            student_module=student,
            metric_fn=self.metric_fn,
            feedback_map=feedback_map,
            failure_score=self.failure_score,
            num_threads=self.num_threads,
            add_format_failure_as_feedback=self.add_format_failure_as_feedback,
            rng=rng,
            reflection_lm=self.reflection_lm,
            custom_instruction_proposer=self.custom_instruction_proposer,
            warn_on_score_mismatch=False,
            reflection_minibatch_size=self.reflection_minibatch_size,
            progress_lm=dspy.settings.lm,
            minibatch_size=REFLECTION_MINIBATCH_SIZE,
            valset_size=len(valset),
        )

        seed_candidate = {name: pred.signature.instructions for name, pred in student.named_predictors()}
        gepa_result: GEPAResult = optimize(
            seed_candidate=seed_candidate,
            trainset=trainset,
            valset=valset,
            adapter=adapter,
            reflection_lm=(lambda x: adapter.stripped_lm_call(x)[0]) if self.reflection_lm is not None else None,
            candidate_selection_strategy=self.candidate_selection_strategy,
            skip_perfect_score=self.skip_perfect_score,
            reflection_minibatch_size=self.reflection_minibatch_size,
            module_selector=self.component_selector,
            perfect_score=self.perfect_score,
            use_merge=self.use_merge,
            max_merge_invocations=self.max_merge_invocations,
            max_metric_calls=self.max_metric_calls,
            logger=LoggerAdapter(logging.getLogger("dspy.teleprompt.gepa.gepa")),
            run_dir=self.log_dir,
            use_wandb=self.use_wandb,
            wandb_api_key=self.wandb_api_key,
            wandb_init_kwargs=self.wandb_init_kwargs,
            use_mlflow=self.use_mlflow,
            track_best_outputs=self.track_best_outputs,
            display_progress_bar=False,
            raise_on_exception=True,
            seed=self.seed,
            **self.gepa_kwargs,
        )

        optimized_program = adapter.build_program(gepa_result.best_candidate)
        if self.track_stats:
            optimized_program.detailed_results = DspyGEPAResult.from_gepa_result(gepa_result, adapter)
        return optimized_program


def _balanced_limit(df: pd.DataFrame, limit: int | None) -> pd.DataFrame:
    if limit is None:
        return df

    per_label = limit // len(LABELS)
    remainder = limit % len(LABELS)
    parts = []
    for index, label in enumerate(LABELS):
        n = per_label + int(index < remainder)
        label_rows = df[df["label"].map(_label) == label]
        if len(label_rows) < n:
            raise ValueError(f"Requested {n} '{label}' rows, but only found {len(label_rows)}.")
        parts.append(label_rows.sample(n=n, random_state=42))
    return pd.concat(parts).sample(frac=1, random_state=42).reset_index(drop=True)


def _print_label_distribution(name: str, examples: list[dspy.Example]) -> None:
    counts = Counter(_label(example.label) for example in examples)
    print(f"{name} label distribution: {dict(counts)}")


def load_data(filepath: Path, limit: int | None = None, balanced_limit: bool = False):
    df = pd.read_csv(filepath)
    df["label"] = df["label"].map(_label)

    if balanced_limit:
        df = _balanced_limit(df, limit)
    elif limit is not None:
        df = df.head(limit)

    counts = Counter(df["label"])
    missing = [label for label in LABELS if counts.get(label, 0) == 0]
    if missing:
        raise ValueError(f"{filepath} is missing labels needed for macro F1 scoring: {missing}")

    examples = []
    for _, row in df.iterrows():
        ex = dspy.Example(
            pert=str(row['pert']),
            gene=str(row['gene']),
            label=str(row['label'])
        ).with_inputs("pert", "gene")
        examples.append(ex)
    return examples


def one_pass_upper_bound_budget(train_size: int, val_size: int, minibatch_size: int) -> int:
    num_minibatches = math.ceil(train_size / minibatch_size)
    base_val_cost = val_size
    accepted_mutation_cost = (2 * minibatch_size) + val_size
    return base_val_cost + (num_minibatches * accepted_mutation_cost)


def _has_resumable_gepa_state(log_dir: str) -> bool:
    state_path = Path(log_dir) / "gepa_state.bin"
    return state_path.exists() and state_path.stat().st_size > 0


def run_optimization(
    train_limit: int | None = TRAIN_LIMIT,
    val_limit: int | None = VAL_LIMIT,
    max_metric_calls: int | None = FIRST_RUN_METRIC_CALL_BUDGET,
    log_dir: str = GEPA_LOG_DIR,
    candidate_export_dir: Path = CANDIDATE_EXPORT_DIR,
    artifact_export_dir: Path = ARTIFACT_EXPORT_DIR,
    optimized_student_path: str = OPTIMIZED_STUDENT_PATH,
):
    logging.getLogger("dspy.teleprompt.gepa.gepa").setLevel(logging.WARNING)
    logging.getLogger("dspy.evaluate.evaluate").setLevel(logging.WARNING)
    logging.getLogger("gepa").setLevel(logging.WARNING)

    print("Setting up models...")
    student_lm = get_student_lm()
    refiner_lm = get_refiner_lm()
    print("Student model: NVIDIA openai/gpt-oss-120b, temperature=1.0, top_p=1.0, max_tokens=65536, reasoning=off")
    print("Feedback model: OpenRouter deepseek/deepseek-v4-pro, temperature=1.0, top_p=1.0, max_tokens=384000, reasoning_effort=high")
    print("Refiner model: OpenRouter deepseek/deepseek-v4-pro, temperature=1.0, top_p=1.0, max_tokens=384000, reasoning_effort=high")
    print("NVIDIA request policy: 1 at a time, 2s gap, retries on 429 with 30s/60s/120s backoff")
    print("GEPA mode: reflective mutations only, merge disabled for clearer attribution")
    print(
        "GEPA selection: current_best, "
        f"stratified reflection minibatch={REFLECTION_MINIBATCH_SIZE} "
        f"({', '.join(f'{count} {label}' for label, count in STRATIFIED_MINIBATCH_COUNTS.items())})"
    )
    print("GEPA metric: macro F1 exact-label objective")

    dspy.settings.configure(lm=student_lm)

    print("Loading datasets...")
    trainset = load_data(TRAIN_DATA, limit=train_limit, balanced_limit=True)
    valset = load_data(VAL_DATA, limit=val_limit)

    print(f"Loaded {len(trainset)} training examples and {len(valset)} validation examples.")
    _print_label_distribution("Train", trainset)
    _print_label_distribution("Validation", valset)
    if max_metric_calls is None:
        max_metric_calls = one_pass_upper_bound_budget(
            train_size=len(trainset),
            val_size=len(valset),
            minibatch_size=REFLECTION_MINIBATCH_SIZE,
        )
        print(
            "Using one-pass upper-bound GEPA budget: "
            f"{max_metric_calls} metric calls "
            f"(minibatch={REFLECTION_MINIBATCH_SIZE})."
        )
    else:
        print(f"Using explicit GEPA budget: {max_metric_calls} metric calls.")

    print("Initializing GEPA Optimizer...")
    gepa = MacroF1GEPA(
        metric=gepa_exact_match_metric,
        reflection_lm=refiner_lm,
        max_metric_calls=max_metric_calls,
        reflection_minibatch_size=None,
        candidate_selection_strategy="current_best",
        perfect_score=GEPA_PERFECT_SCORE,
        num_threads=1,
        add_format_failure_as_feedback=True,
        use_merge=False,
        instruction_proposer=anti_memorization_instruction_proposer,
        track_stats=True,
        track_best_outputs=True,
        log_dir=log_dir,
        gepa_kwargs={
            "batch_sampler": StratifiedLabelBatchSampler(STRATIFIED_MINIBATCH_COUNTS),
            "callbacks": [
                GEPASummaryLogger(
                    candidate_export_dir,
                    artifact_export_dir,
                    student_lm=student_lm,
                    valset_size=len(valset),
                    valset=valset,
                )
            ],
            "use_cloudpickle": True,
        },
    )

    student_module = TrackAStudent()

    print("Starting optimization... (This will take a while, making calls to NVIDIA API)")
    is_resuming = _has_resumable_gepa_state(log_dir)
    if is_resuming:
        print("Resuming from existing GEPA checkpoint; skipping base validation progress bar.")
    elif hasattr(student_lm, "start_progress"):
        student_lm.start_progress("base validation", len(valset))
    try:
        optimized_student = gepa.compile(
            student_module,
            trainset=trainset,
            valset=valset
        )
    finally:
        if hasattr(student_lm, "close_progress"):
            student_lm.close_progress()

    print("\nOptimization Complete!")
    Path(optimized_student_path).parent.mkdir(parents=True, exist_ok=True)
    optimized_student.save(optimized_student_path)
    print(f"Saved optimized module to {optimized_student_path}")
    if hasattr(optimized_student, "detailed_results"):
        details = optimized_student.detailed_results
        summary_path = artifact_export_dir / "gepa_final_summary.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        final_summary = {
            "best_candidate_idx": details.best_idx,
            "best_val_score": details.val_aggregate_scores[details.best_idx],
            "total_metric_calls": details.total_metric_calls,
            "num_full_val_evals": details.num_full_val_evals,
            "log_dir": details.log_dir,
            "seed": details.seed,
            "val_aggregate_scores": details.val_aggregate_scores,
            "parents": details.parents,
            "discovery_eval_counts": details.discovery_eval_counts,
            "candidates": [
                {
                    "candidate_idx": idx,
                    "val_score": details.val_aggregate_scores[idx],
                    "instructions": _candidate_instructions(candidate),
                }
                for idx, candidate in enumerate(details.candidates)
            ],
            "per_val_instance_best_candidates": details.per_val_instance_best_candidates,
            "best_outputs_valset": details.best_outputs_valset,
        }
        summary_path.write_text(json.dumps(_jsonable(final_summary), indent=2), encoding="utf-8")
        print(
            "Final GEPA scores: "
            f"best_candidate={details.best_idx}, "
            f"best_val_score={details.val_aggregate_scores[details.best_idx]:.3f}, "
            f"candidates={len(details.candidates)}"
        )
        print(f"Saved final GEPA summary to {summary_path}")
    return optimized_student


def main():
    run_optimization()

if __name__ == "__main__":
    main()
