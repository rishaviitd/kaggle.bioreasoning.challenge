import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
with open(path, "rb") as f:
    data = pickle.load(f)

if "program_candidates" in data and len(data["program_candidates"]) > 0:
    cand = data["program_candidates"][0]
    print(f"Candidate keys: {list(cand.keys())}")
    
    # Check if there is another structure tracking scores, maybe 'score' is buried inside a dictionary
    for i, c in enumerate(data["program_candidates"]):
        if "score" in c:
            print(f"Candidate {i} score: {c['score']}")
        elif "_score" in c:
            print(f"Candidate {i} _score: {c['_score']}")
        else:
            # try to print the values of all keys that might look like a score
            for k, v in c.items():
                if isinstance(v, (int, float)):
                    print(f"Candidate {i} {k}: {v}")
