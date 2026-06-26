import dspy
from src.track_one.evaluate.gepa_config import get_refiner_lm

# Initialize the refiner LM for judging
refiner_lm = get_refiner_lm()

def gepa_kaggle_metric(gold: dspy.Example, pred: dspy.Prediction, trace=None):
    """
    Binary scoring metric for GEPA with LLM-as-a-judge for failed cases.
    Returns ScoreWithFeedback: {'score': float, 'feedback': str}
    """
    predicted_label = str(pred.prediction).strip().lower()
    true_label = str(gold.label).strip().lower()
    
    # We strictly enforce only the 3 valid labels
    valid_labels = {"up", "down", "none"}
    
    # Check for correct prediction
    if predicted_label == true_label:
        return {'score': 1.0, 'feedback': "Perfect prediction!"}
        
    # If the model fails, we invoke the Judge (GLM-5.1) to explain why
    
    # Give judge the context
    feedback_prompt = f"""
    The student model was asked to predict the interaction between perturbation '{gold.pert}' and gene '{gold.gene}'.
    The correct ground-truth interaction is '{true_label}'.
    The student model incorrectly guessed '{predicted_label}'.
    
    Student's reasoning trace (if available):
    {pred.reasoning if hasattr(pred, 'reasoning') else 'No reasoning available.'}
    
    Analyze why the student might have failed. Did it hallucinate a pathway? Did it ignore the directionality? Did it hallucinate a valid category?
    Be concise. Suggest a specific rule or context to add to the system instruction to prevent this failure mode.
    """
    
    with dspy.context(lm=refiner_lm):
        # We just query the LM directly
        judge_response = refiner_lm(feedback_prompt)
        
    # Assuming judge_response returns a list of strings
    feedback_text = judge_response[0] if isinstance(judge_response, list) else str(judge_response)
    
    return {'score': 0.0, 'feedback': feedback_text}
