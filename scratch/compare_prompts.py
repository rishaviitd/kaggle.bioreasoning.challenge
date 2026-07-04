import dspy
from src.track_one.prompts.prompt import PROMPT_V5
import sys

class TestGEPALM(dspy.LM):
    def __init__(self):
        super().__init__("openai/gpt-oss-120b")
        self.provider = "default"  # This is what NvidiaTaskLM had!
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        if messages is None:
            # GEPA run_task_lm logic when prompt is a string
            api_messages = [{"role": "user", "content": prompt}]
        else:
            api_messages = messages
        
        # We just want to extract what GEPA actually sent to the API
        with open("scratch/gepa_api_messages.txt", "w") as f:
            if isinstance(api_messages, list):
                f.write(repr(api_messages))
            else:
                f.write(str(api_messages))
        return ["{\"reasoning\": \"ok\", \"label\": \"up\"}"]

lm = TestGEPALM()
dspy.settings.configure(lm=lm)
class SimpleClassificationSignature(dspy.Signature):
    __doc__ = PROMPT_V5.split("### Query")[0].strip()
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")
try:
    dspy.ChainOfThought(SimpleClassificationSignature)(pert="Slc35b1", gene="Pdia6")
except Exception:
    pass

class TestKaggleLM(dspy.LM):
    def __init__(self):
        super().__init__("openai/gpt-oss-120b")
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        if messages:
            content = "\n\n".join([m["content"] for m in messages])
            api_messages = [{"role": "user", "content": content}]
        else:
            api_messages = [{"role": "user", "content": prompt}]
            
        with open("scratch/kaggle_api_messages.txt", "w") as f:
            f.write(repr(api_messages))
        return ["{\"reasoning\": \"ok\", \"label\": \"up\"}"]

lm2 = TestKaggleLM()
dspy.settings.configure(lm=lm2)
try:
    dspy.ChainOfThought(SimpleClassificationSignature)(pert="Slc35b1", gene="Pdia6")
except Exception:
    pass
