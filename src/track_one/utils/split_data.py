import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold
import os

def create_splits():
    # Load original training data
    df = pd.read_csv("data/train.csv")
    
    # We want roughly 60% Train, 20% Val, 20% Test
    # StratifiedGroupKFold doesn't take percentages directly, it takes number of splits (n_splits).
    # If we use n_splits=5, each fold is 20%.
    # We can assign Fold 0 to Val, Fold 1 to Test, and Folds 2-4 to Train.
    
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    
    # We need a numeric label for stratification
    label_map = {"none": 0, "up": 1, "down": 2}
    y_numeric = df["label"].map(label_map)
    
    # Generate the folds
    folds = list(sgkf.split(df, y_numeric, groups=df["pert"]))
    
    # Fold 0 will be Validation (20%)
    val_idx = folds[0][1]
    
    # Fold 1 will be Test (20%)
    test_idx = folds[1][1]
    
    # Folds 2-4 will be Train (60%)
    # We can just take the remaining indices
    train_idx = list(set(df.index) - set(val_idx) - set(test_idx))
    
    # Create the dataframes
    train_df = df.iloc[train_idx].copy()
    val_df = df.iloc[val_idx].copy()
    test_df = df.iloc[test_idx].copy()
    
    # Save them
    os.makedirs("data/local", exist_ok=True)
    train_df.to_csv("data/local/local_train.csv", index=False)
    val_df.to_csv("data/local/local_val.csv", index=False)
    test_df.to_csv("data/local/local_test.csv", index=False)
    
    print("Splits created successfully!")
    print("-" * 30)
    print(f"Local Train: {len(train_df)} rows ({len(train_df)/len(df)*100:.1f}%) | Unique Perts: {train_df['pert'].nunique()}")
    print(f"Local Val:   {len(val_df)} rows ({len(val_df)/len(df)*100:.1f}%) | Unique Perts: {val_df['pert'].nunique()}")
    print(f"Local Test:  {len(test_df)} rows ({len(test_df)/len(df)*100:.1f}%) | Unique Perts: {test_df['pert'].nunique()}")
    print("-" * 30)
    
    # Verify Stratification
    print("\nLabel Distributions:")
    print("Global:")
    print(df["label"].value_counts(normalize=True).round(3))
    print("\nLocal Train:")
    print(train_df["label"].value_counts(normalize=True).round(3))
    print("\nLocal Val:")
    print(val_df["label"].value_counts(normalize=True).round(3))
    print("\nLocal Test:")
    print(test_df["label"].value_counts(normalize=True).round(3))
    
    # Verify OOD (Zero Leakage)
    train_perts = set(train_df["pert"])
    val_perts = set(val_df["pert"])
    test_perts = set(test_df["pert"])
    
    print("\nLeakage Check:")
    print(f"Train-Val Pert Overlap:  {len(train_perts.intersection(val_perts))}")
    print(f"Train-Test Pert Overlap: {len(train_perts.intersection(test_perts))}")
    print(f"Val-Test Pert Overlap:   {len(val_perts.intersection(test_perts))}")

if __name__ == "__main__":
    create_splits()
