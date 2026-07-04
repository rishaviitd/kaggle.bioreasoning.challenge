"""OpenRouter client for GEPA Refiner Models (Claude, DeepSeek, etc.)."""

import os
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI
from openrouter import OpenRouter

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Currently testing with Claude Sonnet 5, but can be seamlessly swapped to DeepSeek or others.
DEFAULT_REFINER_MODEL = "anthropic/claude-sonnet-5"

def run_openrouter_prompt(
    prompt: str | None = None,
    messages: list | None = None,
    model: str = DEFAULT_REFINER_MODEL,
    temperature: float = 0.0,
    max_tokens: int = 16_384,
    reasoning_enabled: bool = False,
) -> str:
    """
    Run a prompt on OpenRouter and return the text content.
    Designed to be called in one line from other files without complications.
    """
    if messages is None:
        if not prompt or not prompt.strip():
            raise ValueError("prompt must not be empty")
        messages = [{"role": "user", "content": prompt}]

    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing from the environment")

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    # DeepSeek and others use this, Claude does not.
    if reasoning_enabled:
        kwargs["extra_body"] = {"reasoning": {"enabled": True}}

    print(f"Running prompt with {model} on OpenRouter...", flush=True)
    response = client.chat.completions.create(**kwargs)
    print("OpenRouter call complete.", flush=True)
    
    return response.choices[0].message.content


# -----------------------------------------------------------------------------
# Legacy Track A Inference (Retained for backward compatibility)
# -----------------------------------------------------------------------------
def run_track_a_inference(prompt: str, reasoning_effort: str = "medium") -> dict[int, dict[str, Any]]:
    """Run one prompt with the fixed Track A settings for all three seeds."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing")

    client = OpenRouter(api_key=api_key)
    responses: dict[int, dict[str, Any]] = {}
    
    model = "openai/gpt-oss-120b"
    provider = "WandB"

    print(f"Running Track A prompt with {model} on {provider}...")
    for seed in (42, 43, 44):
        print(f"Sending seed {seed}...")
        response = client.chat.send(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            seed=seed,
            max_tokens=65_536,
            reasoning={"effort": reasoning_effort},
            logprobs=True,
            top_logprobs=20,
            provider={"order": [provider], "allow_fallbacks": False, "require_parameters": True},
            timeout_ms=240_000,
        )
        responses[seed] = response.model_dump(mode="json", exclude_unset=True)
        print(f"Seed {seed} complete.")

    return responses
