import dspy
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.track_one.prompts.prompt import PROMPT_V5
from client.nvidia_client import _client, STUDENT_MODEL

# Define the exact LM class used in the generator
class KaggleTaskLM(dspy.LM):
    def __init__(self, seed: int):
        super().__init__(STUDENT_MODEL)
        self.seed = seed
        self.client = _client()
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        request = {
            "model": STUDENT_MODEL,
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": 65536,
            "top_p": 1.0,
            "seed": self.seed,
            "logprobs": True,
            "top_logprobs": 20,
        }
        
        response = self.client.chat.completions.create(**request)
        raw_dict = response.model_dump()
        
        # Save it for inspection
        with open("scratch/raw_api_output.json", "w") as f:
            json.dump(raw_dict, f, indent=2)
            
        content = raw_dict["choices"][0]["message"]["content"]
        self.history.append({"prompt": prompt, "messages": messages, "response": content, "raw_response": raw_dict})
        return [content]

# Set up the pipeline exactly like generate_kaggle_sub.py
class SimpleClassificationSignature(dspy.Signature):
    __doc__ = PROMPT_V5.split("### Query")[0].strip()
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")

lm = KaggleTaskLM(seed=42)
dspy.settings.configure(lm=lm)
program = dspy.ChainOfThought(SimpleClassificationSignature)

print("Sending request to NVIDIA API...")
program(pert="Slc35b1", gene="Pdia6")
print("Done! Raw response saved to scratch/raw_api_output.json")
