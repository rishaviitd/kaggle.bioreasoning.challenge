"""Tiny OpenRouter feedback smoke test."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from client.openrouter_client import run_feedback_prompt


OUTPUT_PATH = Path("tests/logs/openrouter_deepseek_feedback_response.json")


def main():
    prompt = """You are the feedback model for prompt optimization.

The student predicted: up
The true label is: down
The task is CRISPRi perturbation effect prediction in mouse BMDMs.

Return one concise sentence explaining the likely failure mode and one concrete
prompt-improvement instruction.
"""
    print("Starting OpenRouter feedback smoke test...", flush=True)
    response = run_feedback_prompt(prompt, max_tokens=512)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(response, indent=2), encoding="utf-8")
    print(f"Saved response JSON to {OUTPUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
