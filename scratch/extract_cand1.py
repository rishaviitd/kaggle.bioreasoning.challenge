import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"

with open(path, "rb") as f:
    data = pickle.load(f)
    
cands = data.get('program_candidates', [])
if len(cands) > 1:
    inst = cands[1].get('instruction', '')
    out_path = "src/track_one/output/best_instructions.txt"
    with open(out_path, "w") as out_f:
        out_f.write(inst)
    print("Extracted Candidate 1 (Score: 0.6256) to best_instructions.txt")
