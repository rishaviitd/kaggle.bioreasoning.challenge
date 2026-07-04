import pickle
from sklearn.metrics import classification_report

with open("src/track_one/output/gepa_logs/gepa_state.bin", "rb") as f:
    state = pickle.load(f)

# The eval cache in GEPA stores results by candidate hash or candidate signature.
# Since we know Candidate 1 was evaluated on the valset, let's find the cache entry
# that has exactly 300 evaluations.

try:
    cache = state["evaluation_cache"]
    scores_dict = getattr(cache, "scores_by_id", {})
    outputs_dict = getattr(cache, "outputs_by_id", {})
    
    # We want the candidate that has len() == 300
    candidate_val_preds = None
    for cand_hash, evals in outputs_dict.items():
        if len(evals) == 300: # Full valset
            # Let's check if this is candidate 1
            # Actually, let's just grab the one with the highest macro f1
            pass
            
    print("Found eval cache:", len(outputs_dict), "entries.")
    for cand_hash, evals in outputs_dict.items():
        print(f"Hash: {cand_hash}, Evals: {len(evals)}")
        
except Exception as e:
    print("Error parsing eval cache:", e)
