"""
Prepare GRPO training data from the main train CSV.

The GRPO rows keep the same system/user prompt style used in the existing
SFT JSONL, but omit the assistant response. The label is stored separately
for reward computation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_TRAIN_CSV = ROOT_DIR / "data/train.csv"
DEFAULT_SFT_JSONL = ROOT_DIR / "data/sft/cot_label/sft_train.jsonl"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "data/grpo"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build GRPO dataset from train.csv.")
    parser.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN_CSV)
    parser.add_argument("--sft-jsonl", type=Path, default=DEFAULT_SFT_JSONL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def read_first_jsonl(path: Path) -> dict[str, Any]:
    print(f"[load] Reading prompt template from: {path}")
    with path.open("r", encoding="utf-8") as f:
        first_line = f.readline()
    if not first_line:
        raise ValueError(f"No rows found in {path}")
    return json.loads(first_line)


def extract_prompt_templates(sft_row: dict[str, Any]) -> tuple[str, str]:
    messages = sft_row.get("messages", [])
    if len(messages) < 2:
        raise ValueError("SFT row must contain at least system and user messages.")

    system_prompt = messages[0]["content"]
    user_template = messages[1]["content"]

    # Replace the first row's concrete pert/gene values with format slots.
    first_pert = user_template.split("[[ ## pert ## ]]")[1].split("[[ ## gene ## ]]")[0].strip()
    first_gene = user_template.split("[[ ## gene ## ]]")[1].split(
        "Respond with the corresponding output fields"
    )[0].strip()
    user_template = user_template.replace(first_pert, "{pert}", 1)
    user_template = user_template.replace(first_gene, "{gene}", 1)
    return system_prompt, user_template


def build_prompt_messages(system_prompt: str, user_template: str, pert: str, gene: str) -> list[dict[str, str]]:
    user_prompt = user_template.format(pert=pert, gene=gene)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def build_prompt_text(messages: list[dict[str, str]]) -> str:
    return (
        "<|system|>\n"
        f"{messages[0]['content']}\n"
        "<|user|>\n"
        f"{messages[1]['content']}\n"
        "<|assistant|>\n"
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    print(f"[write] Saving JSONL: {path}")
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[load] Reading train CSV: {args.train_csv}")
    train_df = pd.read_csv(args.train_csv)
    required = {"pert", "gene", "label"}
    missing = required - set(train_df.columns)
    if missing:
        raise ValueError(f"Train CSV is missing columns: {sorted(missing)}")

    train_df = train_df.copy()
    train_df["pert"] = train_df["pert"].astype(str).str.strip()
    train_df["gene"] = train_df["gene"].astype(str).str.strip()
    train_df["label"] = train_df["label"].astype(str).str.strip().str.lower()
    train_df = train_df[train_df["label"].isin(["up", "down", "none"])].reset_index(drop=True)

    sft_row = read_first_jsonl(args.sft_jsonl)
    system_prompt, user_template = extract_prompt_templates(sft_row)

    print(f"[build] Building GRPO rows from {len(train_df)} train examples...")
    message_rows: list[dict[str, Any]] = []
    text_rows: list[dict[str, Any]] = []
    for i, row in train_df.iterrows():
        if i and i % 1000 == 0:
            print(f"[build] Processed {i}/{len(train_df)} rows...")

        messages = build_prompt_messages(
            system_prompt=system_prompt,
            user_template=user_template,
            pert=row["pert"],
            gene=row["gene"],
        )
        base = {
            "id": row.get("id", f"{row['pert']}_{row['gene']}"),
            "pert": row["pert"],
            "gene": row["gene"],
            "label": row["label"],
        }
        message_rows.append({**base, "prompt": messages})
        text_rows.append({**base, "prompt": build_prompt_text(messages)})

    messages_path = args.output_dir / "grpo_train_messages.jsonl"
    text_path = args.output_dir / "grpo_train_text.jsonl"
    csv_path = args.output_dir / "grpo_train.csv"
    system_path = args.output_dir / "system_prompt.txt"
    user_template_path = args.output_dir / "user_prompt_template.txt"

    write_jsonl(messages_path, message_rows)
    write_jsonl(text_path, text_rows)
    print(f"[write] Saving CSV: {csv_path}")
    train_df.to_csv(csv_path, index=False)
    print(f"[write] Saving prompt template files...")
    system_path.write_text(system_prompt, encoding="utf-8")
    user_template_path.write_text(user_template, encoding="utf-8")

    print("\n" + "=" * 60)
    print("[done] GRPO dataset ready")
    print("=" * 60)
    print(f"Rows: {len(train_df)}")
    print("Label distribution:")
    for label, count in train_df["label"].value_counts().items():
        print(f"  - {label}: {count}")
    print(f"Messages JSONL: {messages_path}")
    print(f"Text JSONL:     {text_path}")
    print(f"CSV:            {csv_path}")


if __name__ == "__main__":
    main()
