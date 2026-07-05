import pickle
import numpy as np
import difflib

path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

# Get all subscores
subscores = data.get('prog_candidate_val_subscores', [])
scores = []
for i, scores_dict in enumerate(subscores):
    if scores_dict:
        avg = np.mean(list(scores_dict.values()))
        scores.append((i, avg))

# Best candidate is Cand 6 (0.6405)
best_idx = 6
cands = data.get('program_candidates', [])
best_prompt = cands[best_idx].get('instruction', '')

# Worst candidates (bottom 3)
scores.sort(key=lambda x: x[1])
worst_cands = scores[:3]

print(f"Comparing Best (Cand {best_idx}) against the worst performing candidates:\n")

for i, score in worst_cands:
    worst_prompt = cands[i].get('instruction', '')
    
    matcher = difflib.SequenceMatcher(None, best_prompt, worst_prompt)
    similarity = matcher.ratio()
    pct_change = (1.0 - similarity) * 100
    
    print(f"\n{'='*80}")
    print(f"CANDIDATE {i} (Score: {score:.4f})")
    print(f"Content Change vs Best: {pct_change:.1f}%")
    print(f"{'='*80}\n")
    
    # Let's extract the actual diffs
    diff = list(difflib.unified_diff(
        best_prompt.splitlines(), 
        worst_prompt.splitlines(),
        n=0 # 0 lines of context to just see the raw additions/deletions
    ))
    
    additions = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
    deletions = [line for line in diff if line.startswith('-') and not line.startswith('---')]
    
    print("WHAT THEY ADDED (that failed):")
    for line in additions[:5]: # just show a sample
        print("  " + line)
    if len(additions) > 5: print(f"  ... and {len(additions)-5} more lines")
        
    print("\nWHAT THEY DELETED (that was important):")
    for line in deletions[:5]:
        print("  " + line)
    if len(deletions) > 5: print(f"  ... and {len(deletions)-5} more lines")

