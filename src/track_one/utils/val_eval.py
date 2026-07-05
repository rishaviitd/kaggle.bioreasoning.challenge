"""Evaluate PROMPT_V5 on the 300-row Validation Set with KaggleTaskLM."""

import sys
from pathlib import Path
import json
import math
import time

import dspy
from sklearn.metrics import f1_score

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from client.nvidia_client import _client, chat_completion, STUDENT_MODEL as MODEL
from src.track_one.utils.evaluate import _seed_probabilities, _final_answer_label, _calculate_full_metrics
from src.track_one.prompts.prompt import PROMPT_V5
from src.track_one.optimization.run_gepa_optimization import load_stratified_splits

TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 65_536
REASONING_EFFORT = "medium"
TOP_LOGPROBS = 20

class KaggleTaskLM(dspy.LM):
    def __init__(self, seed: int):
        super().__init__("openai/gpt-oss-120b")
        self.seed = seed
        self.client = _client()
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        if messages:
            content = "\n\n".join([m["content"] for m in messages])
            api_messages = [{"role": "user", "content": content}]
        else:
            api_messages = [{"role": "user", "content": prompt}]
            
        request = {
            "model": MODEL,
            "messages": api_messages,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "seed": self.seed,
            "max_tokens": MAX_TOKENS,
            "logprobs": True,
            "top_logprobs": TOP_LOGPROBS,
            "extra_body": {"reasoning": {"effort": REASONING_EFFORT}},
        }
        response = chat_completion(self.client, request)
        text = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        self.history.append({
            "prompt": prompt, 
            "messages": messages,
            "api_messages": api_messages,
            "response": text, 
            "kwargs": kwargs, 
            "raw_response": response
        })
        return [text]

class SimpleClassificationSignature(dspy.Signature):
    __doc__ = PROMPT_V5.split("### Query")[0].strip()
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")

def main():
    print("Loading stratified datasets...", flush=True)
    _, valset = load_stratified_splits(train_size=1000, val_size=300)
    print(f"Loaded {len(valset)} validation rows.", flush=True)
    valset = valset[:25]
    print(f"Limiting to {len(valset)} rows for testing.", flush=True)

    lm = KaggleTaskLM(seed=42)
    dspy.settings.configure(lm=lm)
    program = dspy.ChainOfThought(SimpleClassificationSignature)

    evaluated_rows = []
    y_true = []
    y_pred = []

    print("Evaluating 300 rows...", flush=True)
    
    # We load cache if exists so we can resume if it breaks
    cache_path = Path("scratch/val_eval_cache.json")
    if cache_path.exists():
        with open(cache_path, "r") as f:
            evaluated_rows = json.load(f)
            y_true = [row["true_label"] for row in evaluated_rows]
            y_pred = [row["predicted_label"] for row in evaluated_rows]
            print(f"Resumed {len(evaluated_rows)} rows from cache.", flush=True)
    
    processed_count = len(evaluated_rows)
    remaining_valset = valset[processed_count:]
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    def process_row(example, idx):
        try:
            with dspy.context(lm=lm):
                pred = program(pert=example.pert, gene=example.gene)
            data = None
            for entry in reversed(lm.history):
                prompt_str = ""
                if "messages" in entry and entry["messages"]:
                    prompt_str = "\n".join([m.get("content", "") for m in entry["messages"]])
                elif "prompt" in entry and entry["prompt"]:
                    prompt_str = entry["prompt"]
                
                if example.pert in prompt_str and example.gene in prompt_str:
                    data = entry["raw_response"]
                    break
                    
            if data is None:
                raise ValueError(f"Could not find matching API response in history for {example.pert}_{example.gene}")
            
            probs = _seed_probabilities(data)
            if probs is None:
                print(f"Warning: probability extraction failed for {example.pert}_{example.gene}", flush=True)
                probs = {"up": 0.306165, "down": 0.140947, "none": 1 - 0.306165 - 0.140947}
                
            true_label = example.label.lower()
            predicted_label = _final_answer_label(pred.label) or "none"
            
            for label in ("up", "down", "none"):
                if label not in probs:
                    probs[label] = 0.0
                    
            row_data = {
                "id": getattr(example, 'id', f"{example.pert}_{example.gene}"),
                "true_label": true_label,
                "predicted_label": predicted_label,
                "correct": true_label == predicted_label,
                "probabilities": probs,
                "true_label_probability": probs.get(true_label, 0.0),
                "reasoning_trace": pred.reasoning,
                "raw_api_request": lm.history[-1].get("api_messages", []),
                "raw_api_response": data
            }
            return idx, example, row_data, None
        except Exception as e:
            return idx, example, None, e
            
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_row, ex, i): ex for i, ex in enumerate(remaining_valset, start=processed_count + 1)}
        
        for future in as_completed(futures):
            idx, example, row_data, err = future.result()
            if err:
                print(f"Error on {example.pert}_{example.gene}: {err}", flush=True)
                continue
                
            evaluated_rows.append(row_data)
            y_true.append(row_data["true_label"])
            y_pred.append(row_data["predicted_label"])
            
            with open(cache_path, "w") as f:
                json.dump(evaluated_rows, f)
                
            print(f"[{len(evaluated_rows)}/{len(valset)}] {example.pert}_{example.gene} | True: {row_data['true_label']} | Pred: {row_data['predicted_label']} | Correct: {row_data['correct']}", flush=True)
            
    print("\n--- RESULTS ---")
    de_true = [int(row["true_label"] != "none") for row in evaluated_rows]
    de_score = [row["probabilities"]["up"] + row["probabilities"]["down"] for row in evaluated_rows]
    from sklearn.metrics import roc_auc_score
    de_auroc = float(roc_auc_score(de_true, de_score))

    direction_rows = [row for row in evaluated_rows if row["true_label"] != "none"]
    direction_true = [int(row["true_label"] == "up") for row in direction_rows]
    direction_score = [row["probabilities"]["up"] / (row["probabilities"]["up"] + row["probabilities"]["down"] + 1e-15) for row in direction_rows]
    direction_auroc = float(roc_auc_score(direction_true, direction_score))

    kaggle_score = (de_auroc + direction_auroc) / 2
    
    print(f"DE AUROC: {de_auroc:.4f}", flush=True)
    print(f"DIR AUROC: {direction_auroc:.4f}", flush=True)
    print(f"Final Kaggle Score: {kaggle_score:.4f}", flush=True)
    
if __name__ == "__main__":
    main()
