import json

file_path = "src/track_one/output/gepa_logs/feedback_history.jsonl"
try:
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    print(f"\n========================================================")
    print(f"🧠  TEACHER CRITIQUES ACCUMULATED FOR REFLECTION LLM")
    print(f"========================================================\n")
    
    for i, line in enumerate(lines[:1]):
        data = json.loads(line)
        print(f"\033[1;95m--- Failure {i+1}: {data['pert']} -> {data['gene']} ---\033[0m")
        print(f"True: {data['true_label']} | Pred: {data['predicted_label']}\n")
        
        print(f"\033[1;93mTeacher Critique:\033[0m")
        # I MUST use the correct 'critique' key this time!
        print(data.get('critique', 'FAILED TO LOAD KEY'))
        print("\n" + "-"*60 + "\n")
        
except FileNotFoundError:
    print("No feedback generated yet, wait a few more seconds...")
