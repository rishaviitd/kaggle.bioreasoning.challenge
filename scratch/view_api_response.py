from src.track_one.optimization.run_gepa_optimization import NvidiaTaskLM

# Initialize our LLM
lm = NvidiaTaskLM()

# Send a tiny prompt to get a raw response
print("Sending test prompt to API...\n")
response_text = lm("What is 2+2? Answer in one word.")

# Grab the raw response history from the LM object
raw_response = lm.history[-1]["raw_response"]

print("RAW RESPONSE CONTENT STRING:")
print(raw_response["choices"][0]["message"]["content"])
print("\n" + "="*50 + "\n")

print("LAST 5 TOKENS IN THE RAW NEURAL NETWORK ARRAY:")
tokens = raw_response["choices"][0]["logprobs"]["content"]
for token in tokens[-5:]:
    print(f"Token: '{token['token']}'")
    for top in token["top_logprobs"][:3]: # Just print top 3 alternatives for brevity
        print(f"   -> alternative: '{top['token']}', logprob: {top['logprob']}")
