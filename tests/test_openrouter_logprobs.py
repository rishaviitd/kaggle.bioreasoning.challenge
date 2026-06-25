#!/usr/bin/env python3
"""Tiny OpenRouter logprobs smoke test for Track A settings."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openrouter import OpenRouter

MODEL = "openai/gpt-oss-120b"
PROVIDER = "WandB"
PERT = "Psmd4"
GENE = "Anxa2"
TRUE_LABEL = "down"
PROMPT = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

Question: If you knockdown Psmd4 using CRISPRi in mouse BMDMs, what is the effect on Anxa2?

Your answer must be one of:
A) Knockdown of Psmd4 results in up-regulation of Anxa2.
B) Knockdown of Psmd4 results in down-regulation of Anxa2.
C) Knockdown of Psmd4 does not significantly affect Anxa2.

End with exactly one final answer tag:
<answer>A</answer>, <answer>B</answer>, or <answer>C</answer>

Answer:"""
OUTPUT_PATH = Path("tests/logs/openrouter_logprobs_train_psmd4_anxa2_response.json")


def main() -> int:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Missing OPENROUTER_API_KEY.")
        return 1

    client = OpenRouter(api_key=api_key)
    print("Starting OpenRouter logprobs smoke test...")
    print(f"Model: {MODEL}")
    print(f"Provider: {PROVIDER}")
    print(f"Track A row: {PERT}_{GENE}")
    print(f"Known train label: {TRUE_LABEL}")
    print("Sending request...")

    try:
        response = client.chat.send(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=1.0,
            top_p=1.0,
            seed=42,
            max_tokens=65536,
            reasoning={"effort": "medium"},
            logprobs=True,
            top_logprobs=20,
            provider={
                "order": [PROVIDER],
                "allow_fallbacks": False,
                "require_parameters": True,
            },
            timeout_ms=240_000,
        )
    except Exception as exc:
        print(f"Request failed: {exc}")
        return 1

    data = response.model_dump(mode="json", exclude_unset=True)
    print("Response received.")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved raw JSON response to {OUTPUT_PATH}")

    usage = data.get("usage", {}) or {}
    print(f"Usage: {json.dumps(usage, indent=2)}")

    choices = data.get("choices", [])
    if not choices:
        print("No choices returned.")
        print(json.dumps(data, indent=2)[:4000])
        return 1

    choice = choices[0]
    message = choice.get("message", {}) or {}
    reasoning = message.get("reasoning") or ""
    content = message.get("content") or ""

    print("\nReasoning:")
    print(reasoning if reasoning else "(none)")
    print("\nContent:")
    print(content if content else "(empty)")

    logprobs = choice.get("logprobs") or {}
    token_items = logprobs.get("content") or []
    print(f"\nLogprob token count: {len(token_items)}")
    if not token_items:
        print("No logprobs returned.")
        print(json.dumps(choice, indent=2)[:4000])
        return 1

    print("\nGenerated tokens with top logprobs:")
    for idx, item in enumerate(token_items):
        token = item.get("token")
        logprob = item.get("logprob")
        print(f"\n[{idx}] token={token!r} logprob={logprob}")

        top = item.get("top_logprobs") or []
        for alt in top[:20]:
            print(f"    {alt.get('token')!r}: {alt.get('logprob')}")

    print("\nSmoke test finished successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
