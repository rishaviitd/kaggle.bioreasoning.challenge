"""NVIDIA clients for Track A student inference and prompt refinement."""

from __future__ import annotations

import os
import time
import threading
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

# Global Rate Limiting for NVIDIA (40 RPM limit)
API_LOCK = threading.Lock()
LAST_REQ_TIME = 0.0

def _wait_for_rate_limit() -> None:
    """Strictly enforce a minimum of 1.6 seconds between API calls across all threads."""
    global LAST_REQ_TIME
    with API_LOCK:
        now = time.monotonic()
        elapsed = now - LAST_REQ_TIME
        if elapsed < 1.6:
            time.sleep(1.6 - elapsed)
        LAST_REQ_TIME = time.monotonic()

def chat_completion(client: OpenAI, request: dict[str, Any]) -> dict[str, Any]:
    """Robust thread-safe chat completion with rate limiting and backoff."""
    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        _wait_for_rate_limit()
        try:
            response = client.chat.completions.create(**request)
            return response.model_dump(mode="json", exclude_unset=True)
        except Exception as exc:
            if attempt == len(RETRY_BACKOFF_SECONDS):
                raise
            delay = RETRY_BACKOFF_SECONDS[attempt]
            print(f"\n[API Error] {exc}. Retrying in {delay}s...")
            time.sleep(delay)
            
    raise RuntimeError("unreachable retry state")


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


def run_task_lm(prompt: str | None = None, messages: list | None = None, temperature: float = 0.0, max_tokens: int = 65536, reasoning_effort: str = "medium") -> dict[str, Any]:
    """Runs the 120B task model and requests logprobs for the output."""
    client = _client()
    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    request = {
        "model": STUDENT_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "logprobs": True,
        "top_logprobs": 5,
        "extra_body": {"reasoning": {"effort": reasoning_effort}},
    }
    return chat_completion(client, request)


def run_feedback_lm(prompt: str | None = None, messages: list | None = None, temperature: float = 0.0, max_tokens: int = 65536, reasoning_effort: str = "medium") -> str:
    """Runs the 20B feedback model."""
    client = _client()
    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    request = {
        "model": "openai/gpt-oss-20b",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "extra_body": {"reasoning": {"effort": reasoning_effort}},
    }
    resp = chat_completion(client, request)
    return resp["choices"][0]["message"]["content"]
