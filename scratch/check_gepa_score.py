import json
import pickle

path = "src/track_one/output/gepa_logs/gepa_state.bin"

try:
    with open(path, "rb") as f:
        data = pickle.load(f)
        print("Loaded as pickle.")
except Exception as e:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print("Loaded as JSON.")

if isinstance(data, dict) and "program_candidates" in data:
    candidates = data["program_candidates"]
    scores = [(c.get("score"), idx) for idx, c in enumerate(candidates) if c.get("score") is not None]
    if scores:
        best_score = max(scores, key=lambda x: x[0])
        print(f"Best Score: {best_score[0]} (Candidate {best_score[1]})")
        
        # Print the prompt for the best score
        best_cand = candidates[best_score[1]]
        if "instructions" in best_cand:
            print("\nBest Instructions:")
            print(best_cand["instructions"])
        elif "program" in best_cand:
            print(f"Has program object: {type(best_cand['program'])}")
    else:
        print("No scores found in program_candidates.")
else:
    print(f"Data type: {type(data)}")
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())}")
