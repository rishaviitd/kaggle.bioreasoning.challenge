import dspy
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.track_one.prompts.prompt import PROMPT_V5

class SimpleClassificationSignature(dspy.Signature):
    __doc__ = PROMPT_V5.split("### Query")[0].strip()
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")

program = dspy.ChainOfThought(SimpleClassificationSignature)

class DummyLM(dspy.LM):
    def __init__(self, model="dummy"):
        super().__init__(model)
        self.captured_messages = []
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        self.captured_messages = messages
        return ["{\"reasoning\": \"dummy reasoning\", \"label\": \"up\"}"]

lm = DummyLM()
dspy.settings.configure(lm=lm)
program(pert="Slc35b1", gene="Pdia6")

output = "# Exact DSPy Prompt Payload\n\nThis is the exact JSON payload being sent to the NVIDIA client for each row.\n\n"
for i, msg in enumerate(lm.captured_messages):
    output += f"### Message {i+1} (Role: `{msg['role']}`)\n"
    output += f"```text\n{msg['content']}\n```\n\n"

with open("/Users/rishavkumar/.gemini/antigravity/brain/8ae001dd-f17e-4d81-8b85-8b42a0db8967/final_prompt.md", "w") as f:
    f.write(output)
