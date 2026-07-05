import pickle
import numpy as np

path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

subscores = data.get('prog_candidate_val_subscores', [])
for i, scores_dict in enumerate(subscores):
    if scores_dict:
        avg = np.mean(list(scores_dict.values()))
        print(f"Candidate {i} Mean Score: {avg:.4f}")

val_pareto = data.get('pareto_front_valset', {})
if val_pareto:
    best_idx = max(val_pareto.keys(), key=lambda k: val_pareto[k])
    print(f"\nval_pareto dict: {val_pareto}")
    print(f"Best Idx in Pareto: {best_idx}")
    
trace = data.get('full_program_trace', {})
for i, step in trace.items():
    if 'selected_program_candidate' in step:
        print(f"Trace Step {i} -> Candidate {step['selected_program_candidate']}")
