import json

with open("src/track_one/output/gepa_logs/raw_outputs.jsonl", "r") as f:
    first_line = f.readline()

data = json.loads(first_line)
raw_response = data["raw_response"]

print("RAW RESPONSE CONTENT STRING:")
print(raw_response["choices"][0]["message"]["content"])
print("\n" + "="*50 + "\n")

print("LAST 5 TOKENS IN THE LOGPROBS ARRAY:")
tokens = raw_response["choices"][0]["logprobs"]["content"]
for token in tokens[-5:]:
    print(f"Token: '{token['token']}'")
    for top in token["top_logprobs"][:3]: # Just print top 3 alternatives for brevity
        print(f"   -> alternative: '{top['token']}', logprob: {top['logprob']}")

