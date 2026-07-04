import dspy
import collections
from collections import Counter
from typing import Any, List, Dict
import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.track_one.prompts.prompt import PROMPT_V5

instruction = PROMPT_V5.split("### Query")[0].strip()

class SimpleClassificationSignature(dspy.Signature):
    __doc__ = instruction
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")

program = dspy.ChainOfThought(SimpleClassificationSignature)

class DummyLM(dspy.LM):
    def __init__(self, model="dummy"):
        super().__init__(model)
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        print("--- EXACT DSPY MESSAGES START ---")
        print(json.dumps(messages, indent=2))
        print("--- EXACT DSPY MESSAGES END ---")
        return ["{\"reasoning\": \"dummy reasoning\", \"label\": \"up\"}"]

dspy.settings.configure(lm=DummyLM())
program(pert="{pert}", gene="{gene}")
