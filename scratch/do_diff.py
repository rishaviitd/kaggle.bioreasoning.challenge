import pickle
from src.track_one.utils.prompt_diff import compare_prompts

path = "src/track_one/output/gepa_logs/gepa_state.bin"

with open(path, "rb") as f:
    data = pickle.load(f)
    
cands = data.get('program_candidates', [])
if len(cands) > 6:
    prompt_old = cands[1].get('instruction', '')
    prompt_new = cands[6].get('instruction', '')
    
    sim, diff = compare_prompts(prompt_old, prompt_new)
    print(f"Similarity: {sim:.4f}")
    print("\nDIFF:")
    print(diff)
