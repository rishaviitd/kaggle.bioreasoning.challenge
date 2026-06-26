"""Run a Track A prompt and save the three seed responses."""

from __future__ import annotations

import json
from pathlib import Path

from src.track_one.prompts.prompt import PROMPT_V0


DEFAULT_PROVIDER = "openrouter"
OUTPUT_DIR = Path("src/track_one/output")


def _run_prompt(prompt: str, reasoning_effort: str, provider: str) -> dict:
    if provider == "openrouter":
        from client.openrouter_client import run_prompt

        return run_prompt(prompt, reasoning_effort)
    if provider == "nvidia":
        from client.nvidia_client import run_prompt

        return run_prompt(prompt, reasoning_effort)
    raise ValueError("provider must be openrouter or nvidia")


def generate(
    pert: str,
    gene: str,
    reasoning_effort: str = "medium",
    provider: str = DEFAULT_PROVIDER,
    output_path: Path | None = None,
) -> Path:
    print("Starting generation...")
    prompt = PROMPT_V0.format(pert=pert, gene=gene)
    responses = _run_prompt(prompt, reasoning_effort, provider)
    output_path = output_path or OUTPUT_DIR / f"v0_{provider}.json"
    output = {
        "prompt_version": "v0",
        "provider": provider,
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
