import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"

try:
    with open(path, "rb") as f:
        data = pickle.load(f)
        
    cands = data.get('program_candidates', [])
    found = False
    for i, c in enumerate(cands):
        inst = c.get('instruction', '')
        if 'Splicing' in inst or 'splicing' in inst:
            print(f"FOUND IN CANDIDATE {i}!")
            out_path = f"src/track_one/output/candidate_{i}.txt"
            with open(out_path, "w") as out_f:
                out_f.write(inst)
            print(f"Wrote to {out_path}")
            found = True
            
    if not found:
        print("Could not find 'Splicing' in any program_candidates instruction.")
        # Print a snippet of each to see what they look like
        for i, c in enumerate(cands):
            inst = c.get('instruction', '')
            print(f"Cand {i} snippet: {inst[:100]}")
except Exception as e:
    print(e)
