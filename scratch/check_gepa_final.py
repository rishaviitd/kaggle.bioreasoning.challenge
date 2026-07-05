import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

if "prog_candidate_objective_scores" in data:
    scores = data["prog_candidate_objective_scores"]
    print(f"Scores array: {scores}")
