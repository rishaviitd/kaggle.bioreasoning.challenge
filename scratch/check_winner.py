import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"

with open(path, "rb") as f:
    data = pickle.load(f)

# The actual winning program is stored here
winner_dict = data.get('program_at_pareto_front_valset', {})
if winner_dict:
    print(winner_dict.keys())
    # usually maps pareto objective index -> candidate ID or something
    
# Let's just calculate the mean of all candidates again
import numpy as np
subscores = data.get('prog_candidate_val_subscores', [])
for i, scores_dict in enumerate(subscores):
    if scores_dict:
        avg = np.mean(list(scores_dict.values()))
        print(f"Cand {i}: {avg:.4f}")
