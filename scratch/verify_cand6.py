import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"

with open(path, "rb") as f:
    data = pickle.load(f)

cands = data.get('program_candidates', [])
if len(cands) > 6:
    inst = cands[6].get('instruction', '')
    print(inst[:200])
