"""Fixed NVIDIA client for Track A inference."""

from __future__ import annotations

import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


MODEL = "openai/gpt-oss-120b"
BASE_URL = "https://integrate.api.nvidia.com/v1"
SEEDS = (42, 43, 44)
REASONING_EFFORTS = {"low", "medium", "high"}
REQUEST_DELAY_SECONDS = 5
RETRY_BACKOFF_SECONDS = (10, 30, 90)


def _send_with_retries(
    client: OpenAI,
    prompt: str,
    reasoning_effort: str,
    seed: int,
) -> dict[str, Any]:
    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=1.0,
                top_p=1.0,
                seed=seed,
                max_tokens=65_536,
                reasoning={"effort": reasoning_effort},
            )
            return response.model_dump(mode="json")
        except Exception as exc:
            if attempt == len(RETRY_BACKOFF_SECONDS):
                raise

            delay = RETRY_BACKOFF_SECONDS[attempt]
            print(f"Request failed for seed {seed}: {exc}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    raise RuntimeError("unreachable retry state")


def run_prompt(prompt: str, reasoning_effort: str = "medium") -> dict[int, dict[str, Any]]:
    """Run one prompt with fixed NVIDIA Track A settings for all three seeds."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if reasoning_effort not in REASONING_EFFORTS:
        raise ValueError("reasoning_effort must be low, medium, or high")

    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is missing from the environment")

    client = OpenAI(base_url=BASE_URL, api_key=api_key)
    responses: dict[int, dict[str, Any]] = {}

    print(f"Running Track A prompt with {MODEL} on NVIDIA...")
    for index, seed in enumerate(SEEDS):
        if index:
            print(f"Waiting {REQUEST_DELAY_SECONDS} seconds before next request...")
            time.sleep(REQUEST_DELAY_SECONDS)

        print(f"Sending seed {seed}...")
        responses[seed] = _send_with_retries(client, prompt, reasoning_effort, seed)
        print(f"Seed {seed} complete.")

    print("All NVIDIA Track A seeds complete.")
    return responses
