import dspy
from src.track_one.gepa_config import get_feedback_lm

VALID_LABELS = {"up", "down", "none"}
_feedback_lm = None


def _normalize_label(value: object) -> str:
    text = str(value).strip().lower()
    for label in VALID_LABELS:
        if text == label or text.startswith(label):
            return label
    return text


def _get_feedback_lm():
    global _feedback_lm
    if _feedback_lm is None:
        print("Loading DeepSeek feedback model...")
        _feedback_lm = get_feedback_lm()
    return _feedback_lm


def _llm_feedback(
    gold: dspy.Example,
    pred: dspy.Prediction,
    predicted_label: str,
    true_label: str,
) -> str:
    reasoning = getattr(pred, "reasoning", "") or "No reasoning available."
    prompt = f"""You are a feedback model for GEPA prompt optimization.

Task context:
- A student model predicts whether a CRISPRi knockdown perturbation changes a target gene in mouse BMDMs.
- Valid labels are exactly: up, down, none.
- The ground-truth label is provided below. Treat it as correct.
- We do not have a written ground-truth solution, so you must synthesize a concise label-consistent biological solution path.
- The feedback is for the prompt optimizer, not for the student.

Example:
- Perturbation: {gold.pert}
- Target gene: {gold.gene}
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
    response = _get_feedback_lm()(prompt)
    if isinstance(response, list):
        response = response[0]
    if isinstance(response, dict) and "text" in response:
        return str(response["text"])
    return str(response)


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
            feedback=_llm_feedback(
                gold=gold,
                pred=pred,
                predicted_label=predicted_label,
                true_label=true_label,
            ),
        )

    if predicted_label == true_label:
        return dspy.Prediction(
            score=score,
            feedback="Correct. Keep the final label format exact.",
        )

    return dspy.Prediction(
        score=score,
        feedback=_llm_feedback(
            gold=gold,
            pred=pred,
            predicted_label=predicted_label,
            true_label=true_label,
        ),
    )
