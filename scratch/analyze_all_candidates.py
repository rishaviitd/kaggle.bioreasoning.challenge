import pickle
import numpy as np
import difflib

path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

subscores = data.get('prog_candidate_val_subscores', [])
scores = {}
for i, scores_dict in enumerate(subscores):
    if scores_dict:
        avg = np.mean(list(scores_dict.values()))
        scores[i] = avg

best_idx = 6
cands = data.get('program_candidates', [])
best_prompt = cands[best_idx].get('instruction', '')

print(f"{'='*80}")
print(f"COMPREHENSIVE ANALYSIS: ALL CANDIDATES vs BEST (Candidate {best_idx} - Score: {scores[best_idx]:.4f})")
print(f"{'='*80}\n")

# Sort by score descending to present in a logical order
sorted_cands = sorted(scores.items(), key=lambda x: x[1], reverse=True)

for i, score in sorted_cands:
    if i == best_idx:
        continue
        
    worst_prompt = cands[i].get('instruction', '')
    
    matcher = difflib.SequenceMatcher(None, best_prompt, worst_prompt)
    similarity = matcher.ratio()
    pct_change = (1.0 - similarity) * 100
    
    print(f"[{'#'*20}] CANDIDATE {i} (Score: {score:.4f}) | Content Change: {pct_change:.1f}%")
    
    diff = list(difflib.unified_diff(
        best_prompt.splitlines(), 
        worst_prompt.splitlines(),
        n=0
    ))
    
    additions = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
    deletions = [line for line in diff if line.startswith('-') and not line.startswith('---')]
    
    print(f"  -> Added {len(additions)} lines | Deleted {len(deletions)} lines")
    if len(additions) > 0:
        print("  -> Snippet of what they ADDED (and failed):")
        for line in additions[:3]: print("      " + line[:120])
    if len(deletions) > 0:
        print("  -> Snippet of what they DELETED (that was important):")
        for line in deletions[:3]: print("      " + line[:120])
    print()

