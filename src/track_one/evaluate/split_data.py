import pandas as pd
import numpy as np
from pathlib import Path

TRAIN_CSV = Path("data/train.csv")
OUTPUT_DIR = Path("data/splits")

def main():
    df = pd.read_csv(TRAIN_CSV)
    
    unique_perts = df['pert'].unique()
    unique_genes = df['gene'].unique()
    
    print(f"Total rows: {len(df)}")
    print(f"Unique perts: {len(unique_perts)}")
    print(f"Unique genes: {len(unique_genes)}")
    
    # Randomly shuffle and split perts and genes
    # To maximize the number of edges retained, we'll try an 80/10/10 split
    np.random.seed(42)
    shuffled_perts = np.random.permutation(unique_perts)
    shuffled_genes = np.random.permutation(unique_genes)
    
    n_perts = len(shuffled_perts)
    n_genes = len(shuffled_genes)
    
    # Split Perts: 80% train, 10% val, 10% test
    p_train_end = int(n_perts * 0.8)
    p_val_end = p_train_end + int(n_perts * 0.1)
    
    perts_train = set(shuffled_perts[:p_train_end])
    perts_val = set(shuffled_perts[p_train_end:p_val_end])
    perts_test = set(shuffled_perts[p_val_end:])
    
    # Split Genes: 60% train, 20% val, 20% test (from kaggle dataset specs)
    g_train_end = int(n_genes * 0.6)
    g_val_end = g_train_end + int(n_genes * 0.2)
    
    genes_train = set(shuffled_genes[:g_train_end])
    genes_val = set(shuffled_genes[g_train_end:g_val_end])
    genes_test = set(shuffled_genes[g_val_end:])
    
    # Filter rows
    def assign_split(row):
        p, g = row['pert'], row['gene']
        if p in perts_train and g in genes_train:
            return 'train'
        elif p in perts_val and g in genes_val:
            return 'val'
        elif p in perts_test and g in genes_test:
            return 'test'
        return 'discard'
        
    df['split'] = df.apply(assign_split, axis=1)
    
    pool_train = df[df['split'] == 'train'].copy()
    pool_val = df[df['split'] == 'val'].copy()
    pool_test = df[df['split'] == 'test'].copy()
    
    print(f"\nCandidate Pools Available:")
    print(f"Train pool: {len(pool_train)} rows")
    print(f"Val pool: {len(pool_val)} rows")
    print(f"Test pool: {len(pool_test)} rows")
    
    # Now, sample from these pools based on our balancing/stratification rules
    # 1. Val Set: Stratified
    # Let's see the class distribution in val pool
    val_counts = pool_val['label'].value_counts(normalize=True)
    print(f"\nVal pool class distribution:\n{val_counts}")
    
    # We want ~200 val rows, stratified. If pool is smaller, we take what we can.
    val_size = min(200, len(pool_val))
    if val_size < 100:
        print("WARNING: Val pool is very small. We might need to adjust the split ratios.")
        
    # Same for test pool
    test_size = min(400, len(pool_test))
    
    # Train pool: Balanced (equal number of up, down, none)
    train_min_class = pool_train['label'].value_counts().min()
    train_target_per_class = min(200, train_min_class)
    
    print(f"\nSampling {train_target_per_class} per class for GEPA training set...")
    gepa_train = pd.concat([
        pool_train[pool_train['label'] == 'up'].sample(n=train_target_per_class, random_state=42),
        pool_train[pool_train['label'] == 'down'].sample(n=train_target_per_class, random_state=42),
        pool_train[pool_train['label'] == 'none'].sample(n=train_target_per_class, random_state=42)
    ]).sample(frac=1, random_state=42) # Shuffle
    
    # Stratified sampling for val and test
    def stratified_sample(pool_df, n_samples):
        # Fallback to a random sample if pool is smaller than n_samples
        n_samples = min(n_samples, len(pool_df))
        return pool_df.groupby('label', group_keys=False).apply(
            lambda x: x.sample(n=int(np.round(n_samples * len(x) / len(pool_df))), random_state=42)
        ).sample(frac=1, random_state=42)
        
    gepa_val = stratified_sample(pool_val, val_size)
    local_test = stratified_sample(pool_test, test_size)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    gepa_train.drop(columns=['split']).to_csv(OUTPUT_DIR / "gepa_train.csv", index=False)
    gepa_val.drop(columns=['split']).to_csv(OUTPUT_DIR / "gepa_val.csv", index=False)
    local_test.drop(columns=['split']).to_csv(OUTPUT_DIR / "local_test.csv", index=False)
    
    print(f"\nFinal Splits Saved to {OUTPUT_DIR}:")
    print(f"gepa_train.csv: {len(gepa_train)} rows (Distribution: {dict(gepa_train['label'].value_counts())})")
    print(f"gepa_val.csv: {len(gepa_val)} rows (Distribution: {dict(gepa_val['label'].value_counts())})")
    print(f"local_test.csv: {len(local_test)} rows (Distribution: {dict(local_test['label'].value_counts())})")

if __name__ == "__main__":
    main()
