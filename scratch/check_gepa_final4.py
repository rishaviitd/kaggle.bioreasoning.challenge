import pickle
import numpy as np

path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

subscores = data.get('prog_candidate_val_subscores', [])
candidates = data.get('program_candidates', [])

for i, scores_dict in enumerate(subscores):
    if scores_dict:
        # Calculate the mean of all the individual row scores
        avg_score = np.mean(list(scores_dict.values()))
        print(f"Candidate {i} Mean Score: {avg_score:.4f}")
    else:
        print(f"Candidate {i} Mean Score: No scores")

print("\nBest Candidate (Index 4) Prompt:")
if len(candidates) > 4:
    print(candidates[4].get("instruction", "No instruction found"))
