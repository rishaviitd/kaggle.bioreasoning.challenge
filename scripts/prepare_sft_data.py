import json
import re
from pathlib import Path

import pandas as pd


INPUT_CSV = Path("data/rejection_sampled_train_phase_one.csv")
OUTPUT_JSONL = Path("data/sft_rejection_sampled_train_phase_one.jsonl")
VAL_FRACTION = 0.10
SPLIT_SEED = 42


SYSTEM_PROMPT_V0 = """Your input fields are:
1. `pert` (str): The knocked-down perturbation gene
2. `gene` (str): The target gene to predict
Your output fields are:
1. `label` (str): Final label: exactly 'up', 'down', or 'none'

All interactions will be structured in the following way, with the appropriate values filled.
[[ ## pert ## ]]
{pert}
[[ ## gene ## ]]
{gene}
[[ ## label ## ]]
{label}
[[ ## completed ## ]]

In adhering to this structure, your objective is: 
You are an expert molecular and cellular biology expert analyzing Perturb-seq data from mouse bone-marrow-derived macrophages (BMDMs) stimulated with LPS. Your task is to predict if a CRISPR knockdown of a perturbation gene causes a reproducible increase ('up'), decrease ('down'), or no consistent change ('none') in a target gene. Consider relevant pathways (e.g., cell-type specific biology, ribosome biogenesis, transcription, mitochondrial function, stress response), gene interactions, and cell-specific context.

First, determine if there is any significant, reproducible directional effect between `pert` and `gene` in this cell context; if no clear or direct effect exists, select 'none'.
If a directional effect is present, then determine whether that effect is an increase ('up') or a decrease ('down') in target gene expression.

You MUST output the final label exactly according to the strict bracketed format `[[ ## label ## ]]` and `[[ ## completed ## ]]` as defined at the top of these instructions."""


def make_user_prompt(pert: str, gene: str) -> str:
    return f"""[[ ## pert ## ]]
**{pert}**

[[ ## gene ## ]]
**{gene}**

Analyze the regulatory effect of knocking down **{pert}** on **{gene}** in single-cell mouse BMDMs using CRISPR interference.

Please reason step by step. After completing your reasoning, output exactly
one `[[ ## label ## ]]` field, followed by `[[ ## completed ## ]]`.
Do not add any text after `[[ ## completed ## ]]`."""


def canonicalize_assistant_trace(trace: str, label: str) -> tuple[str, bool, bool]:
    """Move post-think rationale inside the closing think tag and normalize output."""
    label_marker = "[[ ## label ## ]]"
    closing_position = trace.find("</think>")
    if closing_position < 0:
        raise ValueError("Assistant trace is missing the closing think tag.")

    after_think = trace[closing_position + len("</think>"):]
    marker_position = after_think.find(label_marker)
    if marker_position < 0:
        raise ValueError("Assistant trace is missing the label marker.")

    reasoning_before_close = trace[:closing_position]
    # Remove any structured answer block emitted inside the reasoning before
    # the closing tag; one canonical block is written below.
    reasoning_before_close = re.sub(
        r"\[\[\s*##\s*label\s*##\s*\]\].*?"
        r"\[\[\s*##\s*completed\s*##\s*\]\]",
        "",
        reasoning_before_close,
        flags=re.DOTALL,
    ).rstrip()
    post_think_text = after_think[:marker_position].strip()
    moved_post_think_text = bool(post_think_text)
    reasoning = reasoning_before_close
    if post_think_text:
        reasoning += f"\n\n{post_think_text}"

    canonical_trace = (
        f"{reasoning}\n\n</think>\n\n{label_marker}\n"
        f"{label}\n\n[[ ## completed ## ]]"
    )
    return canonical_trace, canonical_trace != trace, moved_post_think_text


def main() -> None:
    print(f"Loading resolved examples from {INPUT_CSV}...")
    dataframe = pd.read_csv(INPUT_CSV)
    resolved = dataframe[dataframe["accepted_trial"].notna()]
    print(f"Resolved examples found: {len(resolved)}")

    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)

    examples = []
    print("Preparing SFT examples...")
    for _, row in resolved.iterrows():
            trial_number = int(row["accepted_trial"])
            reasoning_trace = row[f"trial_{trial_number}"]

            if not isinstance(reasoning_trace, str) or not reasoning_trace.strip():
                raise ValueError(
                    f"Missing reasoning trace for row_id={row['row_id']}"
                )

            # One source trace was truncated immediately before the completed
            # marker. Repair only that unambiguous final-token truncation.
            reasoning_trace = reasoning_trace.strip()
            if "[[ ## completed ## ]]" not in reasoning_trace:
                if reasoning_trace.endswith("[["):
                    reasoning_trace += " ## completed ## ]]"
                    print(
                        f"Repaired truncated completed marker for "
                        f"row_id={int(row['row_id'])}."
                    )
                else:
                    raise ValueError(
                        f"Trace for row_id={row['row_id']} is missing the "
                        "completed marker and cannot be repaired safely."
                    )

            normalized_label = str(row["label"]).lower().strip()
            reasoning_trace, was_normalized, moved_post_think_text = canonicalize_assistant_trace(
                reasoning_trace,
                normalized_label,
            )
            if was_normalized:
                if moved_post_think_text:
                    print(
                        f"Moved post-think rationale inside closing tag for "
                        f"row_id={int(row['row_id'])}."
                    )

            example = {
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT_V0,
                    },
                    {
                        "role": "user",
                        "content": make_user_prompt(
                            str(row["pert"]),
                            str(row["gene"]),
                        ),
                    },
                    {
                        "role": "assistant",
                        "content": reasoning_trace,
                    },
                ],
                "row_id": int(row["row_id"]),
                "label": normalized_label,
                "accepted_trial": trial_number,
            }

            examples.append(example)

            if len(examples) % 500 == 0:
                print(f"Prepared {len(examples)}/{len(resolved)} examples...")

    examples_df = pd.DataFrame(examples)
    validation_indices = []

    # Sample independently within each label so all classes retain their
    # original proportions in both train and validation sets.
    for label, group in examples_df.groupby("label", sort=True):
        count = max(1, int(round(len(group) * VAL_FRACTION)))
        sampled = group.sample(n=count, random_state=SPLIT_SEED)
        validation_indices.extend(sampled.index.tolist())
        print(
            f"{label}: {len(group)} total, "
            f"{count} validation, {len(group) - count} training"
        )

    validation_index_set = set(validation_indices)
    for index, example in enumerate(examples):
        example["split"] = (
            "val" if index in validation_index_set else "train"
        )

    print(f"Writing combined SFT dataset to {OUTPUT_JSONL}...")
    with OUTPUT_JSONL.open("w", encoding="utf-8") as output_file:
        for example in examples:
            output_file.write(json.dumps(example, ensure_ascii=False) + "\n")

    training_count = len(examples) - len(validation_indices)

    print(f"Finished. Wrote {len(examples)} total SFT examples.")
    print(f"Training examples: {training_count}")
    print(f"Validation examples: {len(validation_indices)}")
    print(f"Saved combined dataset to: {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
