import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

subscores = data.get('prog_candidate_val_subscores', [])
for i, scores_dict in enumerate(subscores):
    if scores_dict:
        # scores_dict usually maps metric_name -> score_value
        print(f"Candidate {i}: {scores_dict}")
    else:
        print(f"Candidate {i}: No scores")
