"""Fixed OpenRouter client for Track A inference."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from openrouter import OpenRouter


MODEL = "openai/gpt-oss-120b"
PROVIDER = "WandB"
SEEDS = (42, 43, 44)
REASONING_EFFORTS = {"low", "medium", "high"}


def run_prompt(prompt: str, reasoning_effort: str = "medium") -> dict[int, dict[str, Any]]:
    """Run one prompt with the fixed Track A settings for all three seeds."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if reasoning_effort not in REASONING_EFFORTS:
        raise ValueError("reasoning_effort must be low, medium, or high")

    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing from the environment")

    client = OpenRouter(api_key=api_key)
    responses: dict[int, dict[str, Any]] = {}

    print(f"Running Track A prompt with {MODEL} on {PROVIDER}...")
    for seed in SEEDS:
        print(f"Sending seed {seed}...")
        response = client.chat.send(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            top_p=1.0,
            seed=seed,
            max_tokens=65_536,
            reasoning={"effort": reasoning_effort},
            logprobs=True,
            top_logprobs=20,
            provider={
                "order": [PROVIDER],
                "allow_fallbacks": False,
                "require_parameters": True,
            },
            timeout_ms=240_000,
        )
        responses[seed] = response.model_dump(mode="json", exclude_unset=True)
        print(f"Seed {seed} complete.")

    print("All Track A seeds complete.")
    return responses
