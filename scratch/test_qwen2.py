import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

try:
    resp = client.chat.completions.create(
        model="qwen/qwen3.5-9b",
        messages=[{"role": "user", "content": "Hello, say [[ ## label ## ]] none [[ ## completed ## ]]"}],
        temperature=0.0,
        max_tokens=50,
        logprobs=True,
        top_logprobs=15,
        timeout=10.0
    )
    data = resp.model_dump(mode="json")
    print(f"Content: {data['choices'][0]['message']['content']}")
    print(f"Logprobs present: {'logprobs' in data['choices'][0] and data['choices'][0]['logprobs'] is not None}")
except Exception as e:
    print(f"Error: {e}")
