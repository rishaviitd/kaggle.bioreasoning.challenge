import json

file_path = "src/track_one/output/gepa_logs/raw_outputs.jsonl"
with open(file_path, "r") as f:
    lines = f.readlines()

for line in lines[:2]:
    data = json.loads(line)
    print("========================================")
    print(data["response"])

