import pickle
import numpy as np

path = "src/track_one/output/gepa_logs/gepa_state.bin"
try:
    with open(path, "rb") as f:
        data = pickle.load(f)

    subscores = data.get('prog_candidate_val_subscores', [])
    print(f"Found {len(subscores)} candidates.")
    
    for i, scores_dict in enumerate(subscores):
        if scores_dict:
            avg = np.mean(list(scores_dict.values()))
            print(f"Candidate {i} Mean Score: {avg:.4f}")
        else:
            print(f"Candidate {i}: No scores yet")
            
    val_pareto = data.get('pareto_front_valset', {})
    if val_pareto:
        avg = np.mean(list(val_pareto.values()))
        print(f"\nPareto Front Best Score: {avg:.4f}")
    else:
        print("\nNo Pareto Front found.")
except Exception as e:
    print(f"Error loading state: {e}")
