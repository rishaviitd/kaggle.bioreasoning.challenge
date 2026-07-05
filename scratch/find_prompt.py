import json

path = "src/track_one/output/gepa_logs/raw_outputs.jsonl"
prompts_found = []

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            # The Reflection LM outputs the new prompt in its response
            # Let's look for responses that contain 'Decision‑making workflow' or 'Direct regulatory evidence'
            if "response" in data:
                resp = data["response"]
                if "Direct regulatory evidence" in resp or "Decision-making workflow" in resp or "Decision‑making workflow" in resp:
                    prompts_found.append(resp)
        except:
            continue

print(f"Found {len(prompts_found)} generated prompts in the raw outputs log.")
if prompts_found:
    print("\n--- LATEST PROMPT IN LOGS ---\n")
    print(prompts_found[-1][:1000] + "...\n[TRUNCATED]")
