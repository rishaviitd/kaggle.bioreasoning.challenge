import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

print(f"prog_candidate_val_subscores: {data.get('prog_candidate_val_subscores')}")
print(f"best_score (if any): {data.get('best_score')}")

if "best_outputs_valset" in data:
    best_out = data["best_outputs_valset"]
    if isinstance(best_out, dict):
        print(f"Keys in best_outputs_valset: {list(best_out.keys())}")
