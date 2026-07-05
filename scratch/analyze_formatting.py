import pickle
import numpy as np

path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

subscores = data.get('prog_candidate_val_subscores', [])
scores = {}
for i, scores_dict in enumerate(subscores):
    if scores_dict:
        scores[i] = np.mean(list(scores_dict.values()))

cands = data.get('program_candidates', [])

print(f"{'Cand':<6} | {'Score':<8} | {'Bullets (- or *)':<18} | {'Bolds (**)':<12} | {'Headers (###)':<15}")
print("-" * 70)

# Sort by score descending
sorted_cands = sorted(scores.items(), key=lambda x: x[1], reverse=True)

for i, score in sorted_cands:
    inst = cands[i].get('instruction', '')
    
    bullets = inst.count('- ') + inst.count('* ')
    bolds = inst.count('**') // 2  # pair of asterisks
    headers = inst.count('### ')
    
    print(f"{i:<6} | {score:.4f}   | {bullets:<18} | {bolds:<12} | {headers:<15}")

