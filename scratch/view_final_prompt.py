import dspy
from src.track_one.optimization.run_gepa_optimization import NvidiaTaskLM

# 1. Setup the exact model we are using in the pipeline
lm = NvidiaTaskLM()
dspy.settings.configure(lm=lm)

# 2. Load the exact instructions from the file
with open("src/track_one/output/best_instructions.txt", "r") as f:
    instruction_src = f.read().strip()
escaped_instruction = instruction_src.replace("{", "{{").replace("}", "}}")

# 3. Create the exact Signature
class SimpleClassificationSignature(dspy.Signature):
    f"""{escaped_instruction}"""
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")

# 4. Make a prediction (this triggers the ChatAdapter)
predictor = dspy.Predict(SimpleClassificationSignature)
print("Sending test prediction to capture prompt formatting...")
try:
    predictor(pert="Spi1", gene="Tlr4")
except Exception as e:
    pass

# 5. Extract the exact messages sent to the API
last_call = lm.history[-1]
print("\n" + "="*80)
print("EXACT MESSAGES SENT OVER THE WIRE TO THE LLM:")
print("="*80)
if "messages" in last_call:
    for i, msg in enumerate(last_call["messages"]):
        print(f"\n[{msg['role'].upper()} MESSAGE]:\n{msg['content']}")
else:
    print(f"\n[RAW PROMPT STRING]:\n{last_call.get('prompt', '')}")
print("="*80 + "\n")
