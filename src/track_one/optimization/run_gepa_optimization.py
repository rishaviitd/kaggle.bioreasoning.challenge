import os
import pandas as pd
import dspy

from gepa import optimize
from gepa.adapters.dspy_full_program_adapter.full_program_adapter import DspyAdapter

from client.nvidia_client import run_task_lm, run_feedback_lm
from src.track_one.utils.evaluate import _seed_probabilities, _final_answer_label

SKIP_FEEDBACK = False

# 1. Custom DSPy LMs for GEPA Adapter

class NvidiaTaskLM(dspy.LM):
    def __init__(self, model="openai/gpt-oss-120b"):
        super().__init__(model)
        self.provider = "default"
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        response = run_task_lm(prompt=prompt, messages=messages, temperature=0.0)
        text = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        self.history.append({
            "prompt": prompt, 
            "messages": messages,
            "response": text, 
            "kwargs": kwargs, 
            "raw_response": response
        })
        return [text]

class NvidiaReflectionLM(dspy.LM):
    def __init__(self, model="openai/gpt-oss-120b"):
        super().__init__(model)
        self.provider = "default"
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        # Enforce lean changes and safety bounds for the 4096 token limit
        constraint = """
        
CRITICAL CONSTRAINTS FOR YOUR NEW PROMPT:
1. LEAN CHANGES: This task is highly sensitive to massive prompt rewrites. You must only make lean, incremental updates to the rules based on the failures. Do NOT write a massive, bloated prompt.
2. TOKEN LIMIT: Your proposed prompt MUST be under 1500 words. We have a strict 4096 token limit, and the model needs at least 2000 tokens leftover to output its step-by-step biological reasoning.
"""
        if prompt is not None:
            prompt += constraint
            
        # Use temperature 0.7 for the reflection step to allow creative brainstorming
        response = run_task_lm(prompt=prompt, messages=messages, temperature=0.7)
        text = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        self.history.append({
            "prompt": prompt, 
            "messages": messages,
            "response": text, 
            "kwargs": kwargs
        })
        return text

# 2. Data Loader for GEPA

from sklearn.model_selection import train_test_split
import random
import dspy

_original_sample = random.sample

def _stratified_sample(population, k, *, counts=None):
    if len(population) > 0 and hasattr(population[0], "label") and isinstance(population[0], dspy.Example):
        labels = [ex.label for ex in population]
        try:
            sampled, _ = train_test_split(population, train_size=k, stratify=labels)
            return sampled
        except Exception:
            return _original_sample(population, k)
    if counts is not None:
        return _original_sample(population, k, counts=counts)
    return _original_sample(population, k)

random.sample = _stratified_sample

def load_stratified_splits(train_size=350, val_size=200):
    train_df = pd.read_csv("data/local/local_train.csv")
    sol_df = pd.read_csv("data/local/local_train_solution.csv")
    
    # Merge reasoning
    full_df = train_df.merge(sol_df[['id', 'reasoning']], on='id', how='left')
    full_df.rename(columns={'reasoning': 'gt_reasoning'}, inplace=True)
    
    # Sample 550 rows stratified by label
    total_size = train_size + val_size
    sampled_df, _ = train_test_split(full_df, train_size=total_size, stratify=full_df['label'], random_state=42)
    
    # Split the 550 rows into train and val stratified by label
    train_split, val_split = train_test_split(sampled_df, train_size=train_size, stratify=sampled_df['label'], random_state=42)
    
    def df_to_dspy(df):
        examples = []
        for _, row in df.iterrows():
            ex = dspy.Example(
                pert=row['pert'],
                gene=row['gene'],
                label=row['label'],
                gt_reasoning=row.get('gt_reasoning', '')
            ).with_inputs('pert', 'gene')
            examples.append(ex)
        return examples
        
    return df_to_dspy(train_split), df_to_dspy(val_split)

# 3. Metric Function for GEPA (Per-example scoring & 20B Feedback)

def metric_fn(example, pred, trace=None):
    predicted_label = _final_answer_label(pred.label)
    if predicted_label is None:
        predicted_label = "invalid"

    true_label = example.label.lower()
    score = 1.0 if predicted_label == true_label else 0.0
    
    is_correct = (predicted_label == true_label)
    
    # ANSI Color Codes for beautiful logs
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    
    status = f"{GREEN}✅ CORRECT{RESET}" if is_correct else f"{RED}❌ INCORRECT{RESET}"
    # Single atomic print to avoid thread interleaving
    log_str = f"--------------------------------------------------\n{status} | {CYAN}{example.pert:>6} -> {example.gene:<6}{RESET} | Pred: {YELLOW}{predicted_label:<5}{RESET} | True: {BLUE}{true_label:<5}{RESET} | Score: {MAGENTA}{score:.2f}{RESET}"
    print(log_str, flush=True)
    
    if is_correct:
        feedback_text = "Correct biological reasoning and classification."
    elif SKIP_FEEDBACK:
        feedback_text = f"Incorrect prediction. True label is '{true_label}'."
    else:
        print(f"\033[38;5;208m⏳ Teacher Model is writing critique for {example.pert} -> {example.gene}...\033[0m", flush=True)
        feedback_prompt = f"""You are a computational biology mentor. A student model incorrectly predicted a Perturb-seq outcome.

Perturbation: {example.pert}
Target Gene: {example.gene}
True Label: {true_label}
Student Predicted: {predicted_label}

Student's Reasoning:
{pred.reasoning}

Ground Truth Reasoning:
{example.gt_reasoning}

Critique the student's reasoning. You MUST structure your response exactly using the following three headers:

[FAILURE CATEGORY]
(Categorize the core biological error in 6-10 words. For example: "Missed compensatory signaling pathway activation", "Ignored secondary metabolic stress response", etc. NOTE: These are just examples, generate a highly accurate category based on the specific failure.)

[STUDENT FLAW]
(Explain exactly what biological fact the student missed, misinterpreted, or got backwards when reasoning about the perturbation's effect on the target gene.)

[MISSING GENERALIZED PRINCIPLE]
(Draft a highly specific, generalized biological rule that explains the Ground Truth mechanism. Do NOT use specific gene names; abstract it so it applies universally to similar pathways.)"""
        
        critique = run_feedback_lm(feedback_prompt, temperature=0.0, max_tokens=65536)
        feedback_text = f"Incorrect prediction. True label is '{true_label}'. Critique: {critique}"
        
        import json
        import os
        os.makedirs("src/track_one/output/gepa_logs", exist_ok=True)
        with open("src/track_one/output/gepa_logs/feedback_history.jsonl", "a") as f:
            log_entry = {
                "pert": example.pert,
                "gene": example.gene,
                "true_label": true_label,
                "predicted_label": predicted_label,
                "student_reasoning": pred.reasoning,
                "gt_reasoning": example.gt_reasoning,
                "critique": critique
            }
            f.write(json.dumps(log_entry) + "\n")
        
    return dspy.Prediction(score=score, feedback=feedback_text)

# 4. Main GEPA Loop

def main():
    import logging
    logging.getLogger("dspy").setLevel(logging.ERROR)
    logging.getLogger("gepa").setLevel(logging.ERROR)
    
    # ULTIMATE KILL-SWITCH FOR DSPY VERBOSITY
    import dspy
    original_eval = dspy.Evaluate.__call__
    def quiet_eval(self, *args, **kwargs):
        self.display_progress = False
        self.display_table = False
        return original_eval(self, *args, **kwargs)
    dspy.Evaluate.__call__ = quiet_eval
    
    print("Setting up DSPy models...")
    task_lm = NvidiaTaskLM()
    dspy.settings.configure(lm=task_lm)
    reflection_lm = NvidiaReflectionLM()
    
    print("Loading stratified datasets...")
    trainset, valset = load_stratified_splits(train_size=1000, val_size=300)
    
    # Load the winning prompt from the previous run
    prompt_path = "src/track_one/output/best_instructions.txt"
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            instruction_src = f.read()
        print(f"Loaded seed prompt from {prompt_path}")
    else:
        print(f"ERROR: {prompt_path} not found. Cannot start optimization.")
        return
    
    class PromptOnlyAdapter:
        def __init__(self, task_lm, metric_fn, reflection_lm, valset, num_threads=5):
            self.inner_adapter = DspyAdapter(task_lm=task_lm, metric_fn=metric_fn, reflection_lm=reflection_lm, num_threads=num_threads)
            self.propose_new_texts = None # Forces GEPA to use InstructionProposalSignature
            self.valset_ids = set(id(ex) for ex in valset)
            self._last_val_score = None
            self._last_mini_score = None
            
        def _build_program_src(self, instruction):
            escaped_instruction = instruction.replace('\"\"\"', '\\\"\\\"\\\"')
            return f'''import dspy
import collections
from collections import Counter
from typing import Any, List, Dict

class SimpleClassificationSignature(dspy.Signature):
    """{escaped_instruction}"""
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")

program = dspy.ChainOfThought(SimpleClassificationSignature)
'''

        def evaluate(self, batch, candidate, capture_traces=False):
            global SKIP_FEEDBACK
            is_valset = all(id(ex) in self.valset_ids for ex in batch)
            batch_name = "VALSET" if is_valset else "MINI-BATCH"
            
            # Disable Teacher Feedback unless GEPA explicitly requests traces
            # (which it only does during make_reflective_dataset)
            SKIP_FEEDBACK = not capture_traces
            
            print(f"\n\033[1;95m{'='*80}\033[0m")
            print(f"\033[1;95m🚀 STEP: EVALUATING PROMPT ON {batch_name} ({len(batch)} examples)\033[0m")
            print(f"\033[1;95m{'='*80}\033[0m\n", flush=True)
            
            program_src = self._build_program_src(candidate["instruction"])
            result = self.inner_adapter.evaluate(batch, {"program": program_src}, capture_traces)
            
            # --- OVERRIDE DSPY ACCURACY WITH MACRO F1 ---
            from sklearn.metrics import f1_score
            y_true = []
            y_pred = []
            
            for ex, pred in zip(batch, result.outputs):
                try:
                    y_true.append(ex.label.strip().lower())
                    
                    if pred is not None and hasattr(pred, "label") and pred.label is not None:
                        parsed = _final_answer_label(pred.label)
                        y_pred.append(parsed if parsed else "none")
                    else:
                        y_pred.append("none")
                except Exception:
                    y_pred.append("none")
                    
            if len(y_true) > 0:
                macro_f1 = f1_score(y_true, y_pred, labels=["up", "down", "none"], average="macro")
            else:
                macro_f1 = 0.0
            
            # Force GEPA to optimize for Macro F1 by overwriting BOTH the scalar and the list of scores
            result.score = macro_f1  
            if hasattr(result, "scores"):
                result.scores = [macro_f1] * len(batch)
                
            current_score = macro_f1
            
            if is_valset:
                if self._last_val_score is not None:
                    print(f"\n\033[1;92m📈 VALSET MACRO F1 SCORE UPDATE: {self._last_val_score:.4f} ➔ {current_score:.4f}\033[0m\n", flush=True)
                else:
                    print(f"\n\033[1;92m🎯 BASELINE VALSET MACRO F1 SCORE ESTABLISHED: {current_score:.4f}\033[0m\n", flush=True)
                self._last_val_score = current_score
            else:
                if self._last_mini_score is not None:
                    print(f"\n\033[1;93m📉 MINI-BATCH MACRO F1 SCORE UPDATE: {self._last_mini_score:.4f} ➔ {current_score:.4f}\033[0m\n", flush=True)
                else:
                    print(f"\n\033[1;93m🎯 BASELINE MINI-BATCH MACRO F1 SCORE ESTABLISHED: {current_score:.4f}\033[0m\n", flush=True)
                self._last_mini_score = current_score
                
            return result
            
        def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
            print(f"\n\033[1;96m{'='*80}\033[0m")
            print(f"\033[1;96m🧠 STEP: FINDING PATTERNS OF FAILURES ON MINI-BATCH AND PROPOSING A BETTER PROMPT (120B is reflecting...)\033[0m")
            print(f"\033[1;96m{'='*80}\033[0m\n", flush=True)
            
            program_src = self._build_program_src(candidate["instruction"])
            inner_dataset = self.inner_adapter.make_reflective_dataset({"program": program_src}, eval_batch, ["program"])
            return {"instruction": inner_dataset["program"]}
    
    adapter = PromptOnlyAdapter(
        task_lm=task_lm,
        metric_fn=metric_fn,
        reflection_lm=reflection_lm,
        valset=valset,
        num_threads=5,
    )
    
    # 5. Run GEPA Optimization
    print("Starting GEPA Optimization...")
    import shutil
    shutil.rmtree("src/track_one/output/gepa_logs", ignore_errors=True)
    os.makedirs("src/track_one/output/gepa_logs", exist_ok=True)
    
    CUSTOM_REFLECTION_TEMPLATE = """I provided an assistant with the following biological reasoning instructions to predict Perturb-seq outcomes:
```
<curr_instructions>
```

The following are examples where the assistant's predictions FAILED on our validation dataset. You will see the inputs, the assistant's incorrect response, and a Teacher's critique on exactly why the biological reasoning failed:
```
<inputs_outputs_feedback>
```

CRITICAL WARNING: The current instructions `<curr_instructions>` FAILED TO GENERALIZE on the validation set. 

Your task is to mathematically UPDATE the assistant's instructions to fix the systemic failure patterns shown above.

STEP 1: ROOT CAUSE ANALYSIS
Before writing the new instructions, carefully read all the Teacher critiques provided in the feedback samples above. Identify the top 2-3 most highly occurring common failure patterns across all the samples. Focus exclusively on the systemic biological blindspots that are causing the majority of the validation failures.

STEP 2: EDIT PLANNING
Think about exactly how you will modify the current instructions to fix the root causes. Explicitly list out:
- WHAT TO EDIT (surgical modifications to existing instructions)
- WHAT TO ADD (new generalized instructions)
- WHAT TO DELETE (flawed, biased, or overfitted instructions)

CRITICAL CONSTRAINTS FOR YOUR UPDATE:
1. RETAIN WORKING LOGIC: Existing instructions that do not conflict with the feedback must be preserved. Only delete or modify an instruction if it directly contributes to the systemic failures identified in Step 1.
2. GENERALIZE THE BIOLOGY: Abstract the highly occurring failure patterns into generalized biological pathways. Do not restrict new instructions to specific gene names.
3. SURGICAL CHANGES: Make your updates highly targeted. You must preserve and output the entire instruction rulebook from top to bottom without truncating it. The total length of the new instruction MUST NOT exceed 1,500 words.
4. CRITICAL ANTI-TRUNCATION RULE: You MUST output the ENTIRE rulebook starting from "You are an expert molecular biologist..." all the way to the end. If you output only the example template, or use ellipses (...) to skip sections, the student model will fail completely.

STEP 3: NEW INSTRUCTIONS
You MUST wrap your fully updated instruction rulebook inside a single pair of ``` blocks. 
Failure to wrap the ENTIRE text in a single giant ``` block will cause a critical parsing error.
Example format:
```
You are an expert molecular biologist...
[Your full instructions]
```"""
    
    result = optimize(
        seed_candidate={"instruction": instruction_src},
        trainset=trainset,
        valset=valset,
        adapter=adapter,
        reflection_lm=reflection_lm,
        reflection_minibatch_size=50,
        max_metric_calls=20000,
        run_dir="src/track_one/output/gepa_logs", # Saves all proposals, traces, and metrics
        display_progress_bar=False,
        reflection_prompt_template=CUSTOM_REFLECTION_TEMPLATE,
    )
    
    print("Optimization Complete!")
    best_candidate = result.best_candidate
    print("Best Instruction:", best_candidate["instruction"])
    
    os.makedirs("src/track_one/output", exist_ok=True)
    with open("src/track_one/output/best_gepa_instruction.txt", "w") as f:
        f.write(best_candidate["instruction"])

if __name__ == "__main__":
    main()
