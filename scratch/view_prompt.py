import json
import dspy

file_path = "/Users/rishavkumar/.gemini/antigravity/brain/8ae001dd-f17e-4d81-8b85-8b42a0db8967/.system_generated/tasks/task-6721.log"
with open(file_path, "r") as f:
    text = f.read()
    
# Find the prompt that was sent to the model that caused the crash
import re
match = re.search(r"🚀 STEP: EVALUATING PROMPT ON MINI-BATCH \(50 examples\).*?🚀 STEP: EVALUATING PROMPT ON VALSET \(300 examples\)", text, re.DOTALL)
if match:
    print(match.group(0))
