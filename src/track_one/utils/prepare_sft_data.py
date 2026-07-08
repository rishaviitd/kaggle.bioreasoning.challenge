import pandas as pd
import json
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[3]
INPUT_CSV = ROOT_DIR / "data/local/local_train_solution.csv"
OUTPUT_JSONL = ROOT_DIR / "data/local/sft_training_data.jsonl"

def format_sft_data():
    print(f"Reading {INPUT_CSV}...")
    df = pd.read_csv(INPUT_CSV)
    
    # Drop rows where GPT-OSS failed to generate reasoning
    df = df[~df['reasoning'].astype(str).str.contains("ERROR:")]
    df = df.dropna(subset=['reasoning', 'label'])
    
    print(f"Found {len(df)} valid rows for Knowledge Injection.")
    
    system_prompt = (
        "You are an expert computational biologist analyzing Perturb-seq data from mouse "
        "bone-marrow-derived macrophages (BMDMs) stimulated with LPS. Your task is to predict "
        "if a CRISPRi knockdown of a perturbation gene causes a reproducible increase ('up'), "
        "decrease ('down'), or no consistent change ('none') in a target gene. Output your "
        "biological reasoning inside <think> tags, and then output exactly one word as the final label: up, down, or none."
    )
    
    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            pert = str(row['pert']).strip()
            gene = str(row['gene']).strip()
            reasoning = str(row['reasoning']).strip()
            label = str(row['label']).strip().lower()
            
            # The User prompt provides the variables
            user_prompt = f"Predict the effect of CRISPRi knockdown of {pert} on the expression of {gene}."
            
            # The Assistant response injects the knowledge into <think> tags, followed by the label
            assistant_response = f"<think>\n{reasoning}\n</think>\n{label}"
            
            # Construct the ShareGPT / OpenAI ChatML format
            json_row = {
                "messages": [
                    {"role": "system", "content": "You are an expert computational biologist analyzing Perturb-seq data from mouse bone-marrow-derived macrophages (BMDMs) stimulated with LPS. Your task is to predict if a CRISPRi knockdown of a perturbation gene causes a reproducible increase ('up'), decrease ('down'), or no consistent change ('none') in a target gene. Output your biological reasoning inside <think> tags, and then output exactly one word as the final label: up, down, or none."},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": assistant_response}
                ]
            }
            
            f.write(json.dumps(json_row) + '\n')
            
    print(f"Successfully saved cleanly formatted JSONL to {OUTPUT_JSONL}")

if __name__ == "__main__":
    format_sft_data()
