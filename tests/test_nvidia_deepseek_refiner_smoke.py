#!/usr/bin/env python3
"""Tiny parallel NVIDIA refiner smoke test."""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

import httpx
from dotenv import load_dotenv


BASE_URL = "https://integrate.api.nvidia.com/v1"
CHAT_URL = f"{BASE_URL}/chat/completions"
OUTPUT_PATH = Path("tests/logs/nvidia_refiner_models_smoke_response.json")
PROMPT = "Say ready in one short sentence."
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
MODELS = [
    "deepseek-ai/deepseek-v4-flash",
    "z-ai/glm-5.1",
    "minimaxai/minimax-m2.7",
    "moonshotai/kimi-k2.6",
    "nvidia/nemotron-3-ultra-550b-a55b",
]


def test_model(api_key: str, model: str) -> dict:
    started = perf_counter()
    print(f"Sending request to {model}...")
    try:
        response = httpx.post(
            CHAT_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": PROMPT}],
                "temperature": 0,
                "top_p": 1.0,
                "max_tokens": 16_384,
                "chat_template_kwargs": {"thinking": False},
                "stream": False,
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"].get("content") or ""
        return {
            "model": model,
            "ok": True,
            "latency_seconds": round(perf_counter() - started, 3),
            "content": content,
            "raw_response": data,
        }
    except Exception as exc:
        return {
            "model": model,
            "ok": False,
            "latency_seconds": round(perf_counter() - started, 3),
            "error": str(exc),
        }


def main() -> int:
    load_dotenv(ENV_PATH)
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        print("Missing NVIDIA_API_KEY.")
        return 1

    print("Starting parallel NVIDIA refiner smoke test...")
    with ThreadPoolExecutor(max_workers=len(MODELS)) as executor:
        futures = [executor.submit(test_model, api_key, model) for model in MODELS]
        results = [future.result() for future in as_completed(futures)]

    results.sort(key=lambda item: (not item["ok"], item["latency_seconds"]))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved model comparison to {OUTPUT_PATH}")

    for result in results:
        status = "ok" if result["ok"] else "failed"
        print(f"{result['model']}: {status} in {result['latency_seconds']}s")
        if result["ok"]:
            print(f"  {result['content']}")
        else:
            print(f"  {result['error']}")

    return 0 if any(result["ok"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
