import dspy
from src.track_one.gepa_config import get_refiner_lm

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
        print("Loading GLM feedback model...")
        _feedback_lm = get_refiner_lm()
    return _feedback_lm


def _llm_feedback(
    gold: dspy.Example,
    pred: dspy.Prediction,
    predicted_label: str,
    true_label: str,
) -> str:
    reasoning = getattr(pred, "reasoning", "") or "No reasoning available."
    prompt = f"""You are the feedback model for GEPA prompt optimization.

The student model is predicting CRISPRi perturbation effects in mouse BMDMs.
The ground-truth label is already known. Do not judge correctness from scratch.
Explain where the student's reasoning likely failed and what prompt instruction
would prevent similar mistakes.

Perturbation: {gold.pert}
Target gene: {gold.gene}
True label: {true_label}
Student predicted: {predicted_label}
Student reasoning:
{reasoning}

Return concise feedback for the optimizer. Include:
1. the failure mode,
2. the likely reasoning mistake,
3. one concrete prompt-improvement instruction.
"""
    print(f"Generating GLM feedback for {gold.pert}_{gold.gene}...")
    response = _get_feedback_lm()(prompt)
    if isinstance(response, list):
        return str(response[0])
    return str(response)


def gepa_kaggle_metric(
    gold: dspy.Example,
    pred: dspy.Prediction,
    trace=None,
    pred_name=None,
    pred_trace=None,
):
    """
    GEPA metric with label-based score and GLM-generated error feedback.

    The score comes only from ground-truth labels. GLM explains mistakes after
    receiving the true label, predicted label, and student reasoning.
    """
    predicted_label = _normalize_label(getattr(pred, "prediction", ""))
    true_label = _normalize_label(gold.label)

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
            score=1.0,
            feedback="Correct. Keep the final label format exact.",
        )

    return dspy.Prediction(
        score=0.0,
        feedback=_llm_feedback(
            gold=gold,
            pred=pred,
            predicted_label=predicted_label,
            true_label=true_label,
        ),
    )
