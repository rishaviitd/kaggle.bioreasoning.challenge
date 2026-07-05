import pandas as pd
from sklearn.metrics import classification_report

df = pd.read_csv("src/track_one/metrics/refiner_benchmarks/benchmark_ministral-8b-2512_raw.csv")

# Filter out any parse fails if there were any
valid_idx = df['final_answer'].isin(['up', 'down', 'none'])
df = df[valid_idx]

report = classification_report(df['correct_answer'], df['final_answer'], labels=['up', 'down', 'none'], output_dict=True)
print(f"F1 (up):   {report['up']['f1-score']:.4f}")
print(f"F1 (down): {report['down']['f1-score']:.4f}")
print(f"F1 (none): {report['none']['f1-score']:.4f}")
print(f"Macro F1:  {report['macro avg']['f1-score']:.4f}")
