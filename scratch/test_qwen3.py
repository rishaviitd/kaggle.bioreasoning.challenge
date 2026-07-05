import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

try:
    resp = client.chat.completions.create(
        model="qwen/qwen3.5-9b",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.0,
        max_tokens=50,
        timeout=10.0
    )
    print(json.dumps(resp.model_dump(mode="json"), indent=2))
except Exception as e:
    print(f"Error: {e}")
