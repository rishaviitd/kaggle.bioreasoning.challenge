import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"

with open(path, "rb") as f:
    data = pickle.load(f)
    
cands = data.get('program_candidates', [])
if len(cands) > 6:
    inst = cands[6].get('instruction', '')
    out_path = "src/track_one/output/best_instructions.txt"
    with open(out_path, "w") as out_f:
        out_f.write(inst)
    print("Extracted Candidate 6 (Score: 0.6405) to best_instructions.txt")
