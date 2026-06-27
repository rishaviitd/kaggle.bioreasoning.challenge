"""Fixed OpenRouter client for Track A inference, feedback, and refinement."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from openrouter import OpenRouter


MODEL = "openai/gpt-oss-120b"
FEEDBACK_MODEL = "deepseek/deepseek-v4-pro"
REFINER_MODEL = "deepseek/deepseek-v4-pro"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
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


def _openrouter_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing from the environment")
    return api_key


def _run_openrouter_chat(
    prompt: str,
    role_name: str,
    model: str,
    temperature: float = 0,
    top_p: float = 1.0,
    max_tokens: int = 16_384,
    reasoning_enabled: bool = True,
) -> dict[str, Any]:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=_openrouter_api_key())

    print(f"Running {role_name} prompt with {model} on OpenRouter...", flush=True)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        extra_body={"reasoning": {"enabled": reasoning_enabled}},
        timeout=240,
    )
    print(f"OpenRouter {role_name} call complete.", flush=True)
    return response.model_dump(mode="json")


def run_feedback_prompt(
    prompt: str,
    temperature: float = 0,
    top_p: float = 1.0,
    max_tokens: int = 16_384,
    reasoning_enabled: bool = True,
) -> dict[str, Any]:
    """Run a mistake-analysis feedback prompt with DeepSeek on OpenRouter."""
    return _run_openrouter_chat(
        prompt=prompt,
        role_name="feedback",
        model=FEEDBACK_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        reasoning_enabled=reasoning_enabled,
    )


def run_refiner_prompt(
    prompt: str,
    temperature: float = 0,
    top_p: float = 1.0,
    max_tokens: int = 16_384,
    reasoning_enabled: bool = True,
) -> dict[str, Any]:
    """Run an instruction-rewrite refiner prompt with DeepSeek on OpenRouter."""
    return _run_openrouter_chat(
        prompt=prompt,
        role_name="refiner",
        model=REFINER_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        reasoning_enabled=reasoning_enabled,
    )
