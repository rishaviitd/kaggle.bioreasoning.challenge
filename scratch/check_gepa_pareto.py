import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

cands = data.get('program_candidates', [])
if len(cands) > 0:
    inst = cands[0].get('instruction', '')
    out_path = "src/track_one/output/best_instructions.txt"
    with open(out_path, "w") as f:
        f.write(inst)
    print(f"Successfully extracted Candidate 0 and wrote to {out_path}")
