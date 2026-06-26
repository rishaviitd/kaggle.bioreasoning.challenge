#!/usr/bin/env python3
"""Tiny NVIDIA GPT-OSS-120B smoke test without logprobs."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


MODEL = "openai/gpt-oss-120b"
BASE_URL = "https://integrate.api.nvidia.com/v1"
OUTPUT_PATH = Path("tests/logs/nvidia_gpt_oss_120b_smoke_response.json")
PROMPT = "What is the capital of France? Answer in one short sentence."
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def main() -> int:
    load_dotenv(ENV_PATH)
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        print("Missing NVIDIA_API_KEY.")
        return 1

    client = OpenAI(base_url=BASE_URL, api_key=api_key)
    print("Starting NVIDIA GPT-OSS smoke test...")
    print(f"Model: {MODEL}")
    print("Sending request...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1024,
        )
    except Exception as exc:
        print(f"Request failed: {exc}")
        return 1

    data = response.model_dump(mode="json")
    print("Response received.")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved raw JSON response to {OUTPUT_PATH}")

    content = data["choices"][0]["message"].get("content") or ""
    print("Content:")
    print(content if content else "(empty)")
    print("NVIDIA smoke test finished successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
