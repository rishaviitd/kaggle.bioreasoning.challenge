import pickle
path = "src/track_one/output/gepa_logs/gepa_state.bin"
out_path = "src/track_one/output/best_instructions.txt"

with open(path, "rb") as f:
    data = pickle.load(f)

val_pareto = data.get('pareto_front_valset', {})
if val_pareto:
    best_idx = max(val_pareto.keys(), key=lambda k: val_pareto[k])
    best_score = val_pareto[best_idx]
    
    trace = data.get('full_program_trace', {})
    if best_idx in trace:
        prog = trace[best_idx].get('program')
        if prog:
            inst = ""
            if isinstance(prog, dict):
                inst = prog.get('instruction', '')
            else:
                try:
                    # Depending on DSPy version, instruction might be accessible differently
                    # If it's a DSPy module, it usually wraps a predictor that has instructions
                    # Try converting the module's signature to string or just get __doc__
                    inst = prog.predictors()[0].signature.instructions
                except:
                    try:
                        inst = prog.predictors()[0].signature.__doc__
                    except:
                        inst = str(prog)
            
            with open(out_path, "w") as f:
                f.write(inst)
            print(f"Successfully wrote prompt with score {best_score} to {out_path}")
            print("\nPreview of the prompt:\n")
            print(inst[:500] + "...")
        else:
            print("No program found for that index.")
    else:
        print("Index not found in trace.")
