import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

if isinstance(data, dict):
    print("Keys in state:", list(data.keys()))
    if "program_candidates" in data:
        print("Number of candidates:", len(data["program_candidates"]))
    if "best_score" in data:
        print("Best Score:", data["best_score"])
    if "best_program" in data:
        print("Best Program exists.")
