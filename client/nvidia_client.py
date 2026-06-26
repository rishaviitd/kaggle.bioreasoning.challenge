"""NVIDIA clients for Track A student inference and prompt refinement."""

from __future__ import annotations

import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


STUDENT_MODEL = "openai/gpt-oss-120b"
REFINER_MODEL = "z-ai/glm-5.1"
BASE_URL = "https://integrate.api.nvidia.com/v1"
SEEDS = (42, 43, 44)
REASONING_EFFORTS = {"low", "medium", "high"}
REQUEST_DELAY_SECONDS = 5
RETRY_BACKOFF_SECONDS = (10, 30, 90)


def _send_with_retries(
    client: OpenAI,
    request: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        try:
            response = client.chat.completions.create(**request)
            return response.model_dump(mode="json")
        except Exception as exc:
            if attempt == len(RETRY_BACKOFF_SECONDS):
                raise

            delay = RETRY_BACKOFF_SECONDS[attempt]
            print(f"Request failed for {label}: {exc}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    raise RuntimeError("unreachable retry state")


def _client() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is missing from the environment")
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def run_prompt(prompt: str, reasoning_effort: str = "medium") -> dict[int, dict[str, Any]]:
    """Run one prompt with fixed NVIDIA Track A settings for all three seeds."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if reasoning_effort not in REASONING_EFFORTS:
        raise ValueError("reasoning_effort must be low, medium, or high")

    client = _client()
    responses: dict[int, dict[str, Any]] = {}

    print(f"Running Track A prompt with {STUDENT_MODEL} on NVIDIA...")
    for index, seed in enumerate(SEEDS):
        if index:
            print(f"Waiting {REQUEST_DELAY_SECONDS} seconds before next request...")
            time.sleep(REQUEST_DELAY_SECONDS)

        print(f"Sending seed {seed}...")
        responses[seed] = _send_with_retries(
            client,
            {
                "model": STUDENT_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 1.0,
                "top_p": 1.0,
                "seed": seed,
                "max_tokens": 65_536,
                "extra_body": {"reasoning": {"effort": reasoning_effort}},
            },
            f"student seed {seed}",
        )
        print(f"Seed {seed} complete.")

    print("All NVIDIA Track A seeds complete.")
    return responses


def refine_prompt(
    prompt: str,
    temperature: float = 0,
    top_p: float = 1.0,
    max_tokens: int = 16_384,
    n: int = 1,
) -> list[dict[str, Any]]:
    """Generate GEPA-style prompt-refinement proposals with GLM-5.1."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if n < 1:
        raise ValueError("n must be at least 1")

    client = _client()
    responses: list[dict[str, Any]] = []

    print(f"Running prompt refiner with {REFINER_MODEL} on NVIDIA...")
    for index in range(n):
        if index:
            print(f"Waiting {REQUEST_DELAY_SECONDS} seconds before next request...")
            time.sleep(REQUEST_DELAY_SECONDS)

        print(f"Sending refiner sample {index + 1}/{n}...")
        responses.append(
            _send_with_retries(
                client,
                {
                    "model": REFINER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens,
                    "extra_body": {"chat_template_kwargs": {"thinking": False}},
                    "stream": False,
                },
                f"refiner sample {index + 1}",
            )
        )
        print(f"Refiner sample {index + 1} complete.")

    print("All NVIDIA refiner samples complete.")
    return responses
