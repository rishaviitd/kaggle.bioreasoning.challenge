import dspy
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.track_one.gepa_config import get_feedback_lm

VALID_LABELS = {"up", "down", "none"}
CORRECT_FEEDBACK = "Correct. Keep the final label format exact."
OPENROUTER_FEEDBACK_WORKERS = 3
_feedback_lm = None
_feedback_lm_lock = threading.Lock()


def _normalize_label(value: object) -> str:
    text = str(value).strip().lower()
    for label in VALID_LABELS:
        if text == label or text.startswith(label):
            return label
    return text


def _get_feedback_lm():
    global _feedback_lm
    if _feedback_lm is None:
        with _feedback_lm_lock:
            if _feedback_lm is None:
                print("Loading DeepSeek feedback model...")
                _feedback_lm = get_feedback_lm()
    return _feedback_lm


def _extract_feedback_response(response: object) -> str:
    if isinstance(response, list | tuple):
        return _extract_feedback_response(response[0]) if response else ""
    if isinstance(response, dict):
        for key in ("text", "content", "output", "response"):
            if key in response and response[key] is not None:
                return str(response[key])
    return str(response)


def build_feedback_prompt(
    pert: str,
    gene: str,
    reasoning: str,
    predicted_label: str,
    true_label: str,
) -> str:
    return f"""You are a feedback model for GEPA prompt optimization.

Task context:
- A student model predicts whether a CRISPRi knockdown perturbation changes a target gene in mouse BMDMs.
- Valid labels are exactly: up, down, none.
- The ground-truth label is provided below. Treat it as correct.
- We do not have a written ground-truth solution, so you must synthesize a concise label-consistent biological solution path.
- The feedback is for the prompt optimizer, not for the student.

Example:
- Perturbation: {pert}
- Target gene: {gene}
- True label: {true_label}
- Student predicted: {predicted_label}

Student reasoning:
{reasoning}

Write feedback in the same spirit as a worked solution: state the correct answer, explain why the model answer is wrong, provide the biological reasoning path consistent with the label, and give one reusable takeaway.

Constraints:
- Do not question the true label.
- Do not invent row-specific few-shot rules or memorize this exact gene pair.
- Make the takeaway reusable for unseen perturbation-target pairs.
- Be concrete; avoid vague phrases like "consider biology better."
- If the true label is none, emphasize why the student's proposed regulation is too weak, indirect, unsupported, or directionally uncertain.
- If the true label is up or down, explain what type of loss-of-function mechanism could plausibly produce that direction.

Return exactly four bullets:
- Correct label: {true_label}
- Why the prediction is incorrect: <one sentence comparing the student prediction to the true label>
- Label-consistent biological explanation: <a concise but complete plausible solution path consistent with the true label>
- Takeaway rule: <one general prompt rule that would prevent this mistake on unseen gene pairs>
"""


def generate_feedback(request: dict[str, str]) -> str:
    prompt = build_feedback_prompt(**request)
    return _extract_feedback_response(_get_feedback_lm()(prompt))


def generate_feedback_batch(
    requests: list[dict[str, str]],
    max_workers: int = OPENROUTER_FEEDBACK_WORKERS,
) -> list[str]:
    if not requests:
        return []

    print(
        "  feedback: generating "
        f"{len(requests)} OpenRouter calls with {max_workers} workers..."
    )
    results = [""] * len(requests)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(generate_feedback, request): index
            for index, request in enumerate(requests)
        }
        completed = 0
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            results[index] = future.result()
            completed += 1
            print(f"  feedback: {completed}/{len(requests)} complete")
    return results


def gepa_exact_match_metric(
    gold: dspy.Example,
    pred: dspy.Prediction,
    trace=None,
    pred_name=None,
    pred_trace=None,
):
    """
    Row-level exact-match metric with LLM-generated error feedback.

    The optimizer adapter converts row-level exact matches into batch macro F1.
    DeepSeek explains mistakes after receiving the true label, predicted label,
    and student reasoning.
    """
    predicted_label = _normalize_label(getattr(pred, "prediction", ""))
    true_label = _normalize_label(gold.label)
    score = float(predicted_label in VALID_LABELS and predicted_label == true_label)

    if pred_name is None:
        return score

    if predicted_label not in VALID_LABELS:
        return dspy.Prediction(
            score=0.0,
            feedback="Needs label-consistent feedback.",
        )

    if predicted_label == true_label:
        return dspy.Prediction(
            score=score,
            feedback=CORRECT_FEEDBACK,
        )

    return dspy.Prediction(
        score=score,
        feedback="Needs label-consistent feedback.",
    )
