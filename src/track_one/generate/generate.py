"""Run a Track A prompt and save the three seed responses."""

from __future__ import annotations

import json
from pathlib import Path

from client.openrouter_client import run_prompt
from src.track_one.prompt.v0.prompt import PROMPT_V0


DEFAULT_OUTPUT = Path("src/track_one/generate/output/v0.json")


def generate(
    pert: str,
    gene: str,
    reasoning_effort: str = "medium",
    output_path: Path = DEFAULT_OUTPUT,
) -> Path:
    print("Starting generation...")
    prompt = PROMPT_V0.format(pert=pert, gene=gene)
    responses = run_prompt(prompt, reasoning_effort)
    output = {
        "prompt_version": "v0",
        "reasoning_effort": reasoning_effort,
        "records": [
            {
                "id": f"{pert}_{gene}",
                "pert": pert,
                "gene": gene,
                "prompt": prompt,
                "responses": responses,
            }
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Saved responses to {output_path}")
    return output_path
