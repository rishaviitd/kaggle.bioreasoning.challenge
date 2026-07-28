import pandas as pd
import json
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[3]
INPUT_CSV = ROOT_DIR / "data/local/local_train_solution.csv"
GLOBAL_TRAIN_CSV = ROOT_DIR / "data/train.csv"

# New SFT directory paths
SFT_DIR = ROOT_DIR / "data/sft"
VAL_CSV = SFT_DIR / "sft_val.csv"
TRAIN_CSV_OUT = SFT_DIR / "sft_train.csv"
TRAIN_JSONL_OUT = SFT_DIR / "sft_train.jsonl"
VAL_JSONL_OUT = SFT_DIR / "sft_val.jsonl"

RANDOM_SEED = 42

def format_row_to_json(row):
    """Converts a single row into the ChatML format with DSPy inputs and <think> tags."""
    pert = str(row['pert']).strip()
    gene = str(row['gene']).strip()
    reasoning = str(row['reasoning']).strip()
    label = str(row['label']).strip().lower()
    
    system_prompt = """Your input fields are:
1. `pert` (str): The knocked-out perturbation gene
2. `gene` (str): The target gene to predict
Your output fields are:
1. `label` (str): Final label: exactly 'up', 'down', or 'none'

All interactions will be structured in the following way, with the appropriate values filled in.
[[ ## pert ## ]]
{pert}
[[ ## gene ## ]]
{gene}
[[ ## label ## ]]
{label}
[[ ## completed ## ]]

In adhering to this structure, your objective is: 
You are an expert computational biologist analyzing Perturb-seq data from mouse bone-marrow-derived macrophages (BMDMs) stimulated with LPS. Your task is to predict if a CRISPR knockout of a perturbation gene causes a reproducible increase ('up'), decrease ('down'), or no consistent change ('none') in a target gene. 

You MUST output the final label exactly according to the strict bracketed format `[[ ## label ## ]]` and `[[ ## completed ## ]]` as defined at the top of these instructions."""

    user_prompt = (
        "[[ ## pert ## ]]\n"
        f"{pert}\n\n"
        "[[ ## gene ## ]]\n"
        f"{gene}\n\n"
        "Respond with the corresponding output fields, starting with the field `[[ ## label ## ]]`, "
        "and then ending with the marker for `[[ ## completed ## ]]`."
    )
    
    assistant_response = f"<think>\n{reasoning}\n</think>\n\n[[ ## label ## ]]\n{label}\n\n[[ ## completed ## ]]"
    
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_response}
        ]
    }

def save_jsonl(df, output_path):
    """Saves a dataframe to JSONL format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            f.write(json.dumps(format_row_to_json(row)) + '\n')

def prepare_sft_data():
    SFT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load and format validation data (if exists) to ensure no leakage
    val_pairs = set()
    if VAL_CSV.exists():
        print(f"Reading Validation Set from {VAL_CSV.name}...")
        val_df = pd.read_csv(VAL_CSV)
        val_df['label'] = val_df['label'].str.strip().str.lower()
        val_pairs = set(zip(val_df['pert'], val_df['gene']))
    else:
        print(f"WARNING: Validation set not found at {VAL_CSV}")
    
    # 2. Load GPT-OSS Generated Reasoning (The Pool)
    print(f"\nReading GPT-OSS Solution Pool from {INPUT_CSV.name}...")
    pool_df = pd.read_csv(INPUT_CSV)
    pool_df['label'] = pool_df['label'].str.strip().str.lower()
    pool_df = pool_df[~pool_df['reasoning'].astype(str).str.contains("ERROR:")]
    pool_df = pool_df.dropna(subset=['reasoning', 'label'])
    
    # 3. Filter out Validation Leakage
    original_pool_size = len(pool_df)
    pool_df = pool_df[~pool_df.apply(lambda row: (row['pert'], row['gene']) in val_pairs, axis=1)]
    print(f"Removed {original_pool_size - len(pool_df)} overlapping validation rows from the candidate pool.")
    
    # 4. BALANCED Sampling: use minority class count as target for ALL classes
    label_counts = pool_df['label'].value_counts()
    min_class_count = label_counts.min()
    print(f"\nBalanced sampling: {min_class_count} rows per class (capped by minority class 'down')")
    
    sampled_dfs = []
    for label in ['none', 'up', 'down']:
        label_pool = pool_df[pool_df['label'] == label]
        sampled_dfs.append(label_pool.sample(n=min_class_count, random_state=RANDOM_SEED))
            
    sft_train_df = pd.concat(sampled_dfs).sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    
    # 6. Save Train Outputs
    sft_train_df.to_csv(TRAIN_CSV_OUT, index=False)
    save_jsonl(sft_train_df, TRAIN_JSONL_OUT)
    
    # 6. Final Validation Printout
    print("\n" + "="*50)
    print("🎯 DATASET VALIDATION REPORT")
    print("="*50)
    print(f"Generated SFT Train Rows: {len(sft_train_df)}")
    print(f"Generated SFT Val Rows:   {len(val_df) if VAL_CSV.exists() else 0}")
        
    print("\n📊 New SFT Train Distribution (BALANCED):")
    train_proportions = sft_train_df['label'].value_counts(normalize=True)
    for label, count in sft_train_df['label'].value_counts().items():
        prop = train_proportions[label]
        print(f"  - {label.upper():<5}: {prop*100:.1f}% ({count} rows)")
        
    if VAL_CSV.exists():
        print("\n📊 SFT Val Distribution (sft_val.csv):")
        val_proportions = val_df['label'].value_counts(normalize=True)
        for label, count in val_df['label'].value_counts().items():
            prop = val_proportions[label]
            print(f"  - {label.upper():<5}: {prop*100:.1f}% ({count} rows)")
    
    print("\n✅ Leakage Check: Training pairs intersecting Validation pairs: ", end="")
    final_train_pairs = set(zip(sft_train_df['pert'], sft_train_df['gene']))
    overlap = len(final_train_pairs.intersection(val_pairs))
    if overlap == 0:
        print("0 (Clean!)")
    else:
        print(f"FAILED! Found {overlap} overlapping pairs.")

if __name__ == "__main__":
    prepare_sft_data()
