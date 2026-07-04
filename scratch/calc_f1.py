import re
from sklearn.metrics import classification_report

log_path = "/Users/rishavkumar/.gemini/antigravity/brain/8ae001dd-f17e-4d81-8b85-8b42a0db8967/.system_generated/tasks/task-3876.log"

with open(log_path, "r") as f:
    content = f.read()

# Split by the header
blocks = content.split("EVALUATING PROMPT ON VALSET (300 examples)")

# We want the second block (index 1), which corresponds to Candidate 1 (the 0.4351 score)
# wait, actually let's just find the block that ends with "0.3965 ➔ 0.4351"
candidate_1_block = None
for block in blocks:
    if "0.3965 ➔ 0.4351" in block:
        candidate_1_block = block
        break

if not candidate_1_block:
    # If not found by string, it's the second block if it exists
    if len(blocks) > 2:
        candidate_1_block = blocks[2] # blocks[0] is before the first header, blocks[1] is baseline, blocks[2] is Candidate 1

y_true = []
y_pred = []

# Pattern to extract Pred and True
# Example: ✅ CORRECT |  Snx14 -> Lmna   | Pred: none  | True: none  | Score: 1.00
pattern = r"Pred:\s*(\w+)\s*\|\s*True:\s*(\w+)"

for line in candidate_1_block.split("\n"):
    match = re.search(pattern, line)
    if match:
        pred = match.group(1).strip().lower()
        true = match.group(2).strip().lower()
        y_pred.append(pred)
        y_true.append(true)

print(f"Extracted {len(y_pred)} predictions for Candidate 1.")
print("\nClassification Report for 0.4351 Candidate:")
print(classification_report(y_true, y_pred, labels=["none", "up", "down"], digits=4))
