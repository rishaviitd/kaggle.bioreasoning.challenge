from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
INPUT_CSV = ROOT_DIR / "data" / "test.csv"
OUTPUT_JSONL = ROOT_DIR / "data" / "openai_batch_test_chat_completions.jsonl"

# Override with OPENAI_BATCH_MODEL when submitting the batch.
MODEL = os.getenv("OPENAI_BATCH_MODEL", "gpt-5.6-luna")

SYSTEM_PROMPT = """Your input fields are:
1. `pert` (str): The knocked-down perturbation gene
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
You are an expert molecular and cellular biology expert analyzing Perturb-seq data from mouse bone-marrow-derived macrophages (BMDMs) stimulated with LPS. Your task is to predict if a CRISPR knockdown of a perturbation gene causes a reproducible increase ('up'), decrease ('down'), or no consistent change ('none') in a target gene. Consider relevant pathways (e.g., cell-type specific biology, ribosome biogenesis, transcription, mitochondrial function, stress response), gene interactions, and cell-specific context.

You MUST output the final label exactly according to the strict bracketed format `[[ ## label ## ]]` and `[[ ## completed ## ]]` as defined at the top of these instructions."""


def build_user_prompt(pert: str, gene: str) -> str:
    return f"""[[ ## pert ## ]]
{pert}

[[ ## gene ## ]]
{gene}

Analyze the regulatory effect of knocking down {pert} on {gene} in single-cell LPS-stimulated mouse BMDMs using CRISPR interference.

Respond with the corresponding output fields, starting with the field `[[ ## label ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`."""


def main() -> None:
    print("Loading test data...")
    df = pd.read_csv(INPUT_CSV)

    required_columns = {"id", "pert", "gene"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)

    print(f"Rows: {len(df)}")
    print(f"Model: {MODEL}")
    print(f"Writing: {OUTPUT_JSONL}")

    with OUTPUT_JSONL.open("w", encoding="utf-8") as output_file:
        for row_number, row in enumerate(df.itertuples(index=False), start=1):
            request = {
                "custom_id": f"track-c-{row_number}-{row.id}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": MODEL,
                    "max_completion_tokens": 1024,
                    "reasoning_effort": "medium",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": build_user_prompt(
                                str(row.pert),
                                str(row.gene),
                            ),
                        },
                    ],
                },
            }
            output_file.write(json.dumps(request, ensure_ascii=False) + "\n")

    with OUTPUT_JSONL.open("r", encoding="utf-8") as input_file:
        lines = [json.loads(line) for line in input_file]

    assert len(lines) == len(df)
    assert len({line["custom_id"] for line in lines}) == len(lines)
    assert all(line["method"] == "POST" for line in lines)
    assert all(line["url"] == "/v1/chat/completions" for line in lines)

    print("Batch JSONL created and validated.")
    print(f"Requests written: {len(lines)}")
    print("First request:")
    print(json.dumps(lines[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
