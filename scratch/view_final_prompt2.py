import dspy
from src.track_one.optimization.run_gepa_optimization import NvidiaTaskLM

lm = NvidiaTaskLM()
dspy.settings.configure(lm=lm)

with open("src/track_one/output/best_instructions.txt", "r") as f:
    instruction_src = f.read().strip()
escaped_instruction = instruction_src.replace("{", "{{").replace("}", "}}")

class SimpleClassificationSignature(dspy.Signature):
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")
SimpleClassificationSignature.__doc__ = escaped_instruction

predictor = dspy.Predict(SimpleClassificationSignature)
try:
    predictor(pert="Spi1", gene="Tlr4")
except Exception as e:
    pass

last_call = lm.history[-1]
print("\n" + "="*80)
print("EXACT MESSAGES SENT OVER THE WIRE TO THE LLM:")
print("="*80)
for msg in last_call["messages"]:
    print(f"\n[{msg['role'].upper()} MESSAGE]:\n{msg['content']}")
