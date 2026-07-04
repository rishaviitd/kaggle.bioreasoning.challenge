import pickle

try:
    with open("src/track_one/output/gepa_logs/gepa_state.bin", "rb") as f:
        state = pickle.load(f)

    candidates = state.get("program_candidates", [])
    with open("scratch/current_prompts.txt", "w") as f:
        for i, c in enumerate(candidates):
            f.write(f"\n{'='*80}\n")
            f.write(f"CANDIDATE {i}\n")
            f.write(f"{'='*80}\n")
            f.write(c["instruction"])
            f.write("\n")
    print(f"Extracted {len(candidates)} prompts.")
except Exception as e:
    print(f"Error: {e}")
