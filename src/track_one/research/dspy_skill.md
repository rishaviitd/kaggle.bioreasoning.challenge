---
name: DSPy GEPA Optimizer
description: Using the DSPy GEPA (Genetic-Pareto) algorithm for reflective prompt evolution  https://huggingface.co/learn/cookbook/en/dspy_gepa
---

# DSPy GEPA: Reflective Prompt Optimizer

**GEPA** (Genetic-Pareto) is an advanced optimizer in DSPy that adaptively evolves textual components (such as prompts) of systems. It is proposed in the paper "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning".

Unlike standard optimizers that only use a scalar score, GEPA takes **textual feedback** along with a scalar score. This provides the optimizer with visibility into _why_ a prompt performed poorly, allowing GEPA to introspect and propose high-performing prompts in very few iterations.

## How it Works

1. **Traces & Execution:** GEPA captures full execution traces of your DSPy module.
2. **Metric & Feedback:** You provide a metric function that returns both a score and a string of feedback explaining what was good or bad about the output.
3. **Reflection & Proposal:** The GEPA `reflection_lm` (often a strong model like GPT-4 or GPT-5) analyzes the feedback for failed examples and writes a proposed prompt addressing the specific failures.
4. **Pareto Selection:** GEPA maintains a candidate pool and stochastically selects from the Pareto frontier of validation scores to find the best instructions.

## Basic Usage

To use GEPA, you first define a custom metric that returns a scalar score and optional textual feedback:

```python
from dspy import Example, Prediction
from typing import Optional, Union
from dspy.teleprompt.gepa.gepa_utils import ScoreWithFeedback

def my_metric(
    gold: Example,
    pred: Prediction,
    trace: Optional[object] = None,
    pred_name: Optional[str] = None,
    pred_trace: Optional[object] = None,
) -> Union[float, ScoreWithFeedback]:
    """
    Evaluate the prediction against the gold label.
    Return a float, or a dictionary: {'score': float, 'feedback': str}
    """
    score = 1.0 if pred.answer == gold.label else 0.0

    if score == 1.0:
        feedback = "Perfect!"
    else:
        feedback = f"The model predicted {pred.answer}, but the correct label is {gold.label}. It failed because it ignored the biological pathway constraint."

    return {'score': score, 'feedback': feedback}
```

Then you compile your DSPy program using the GEPA optimizer:

```python
import dspy

# Provide a very capable model for the reflection steps (e.g. Claude 3.5 Sonnet or GPT-4o)
reflection_lm = dspy.LM(model="gpt-4o", temperature=1.0)

gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=reflection_lm,
    auto="medium",          # Optimization budget: "light", "medium", "heavy"
    track_stats=True
)

# student is your unoptimized DSPy module
optimized_program = gepa.compile(student, trainset=train_examples)
```

## Advanced Features

- **Custom Instruction Proposers:** By default, GEPA uses a built-in instruction proposer that feeds the prompt and error logs to the reflection LM. You can write custom proposers (e.g., `MultiModalInstructionProposer` for images or RAG-enhanced proposers to look up domain guidelines).
- **Batch Inference-time Search:** Pass `valset=batch_of_tasks` and `track_best_outputs=True` to use GEPA to perform test-time search/optimization.
- **Log Directories:** Pass `log_dir="logs/"` to save candidates and allow resuming optimization from checkpoints.
