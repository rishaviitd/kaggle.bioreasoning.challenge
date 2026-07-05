import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

try:
    resp = client.chat.completions.create(
        model="mistralai/ministral-8b-2512",
        messages=[{"role": "user", "content": "Say 'hello'"}],
        temperature=0.0,
        max_tokens=50,
        logprobs=True,
        top_logprobs=15,
        extra_body={
            "provider": {
                "require_parameters": True
            }
        }
    )
    data = resp.model_dump(mode="json")
    print("Provider:", data.get("provider"))
    print("Logprobs Support:", data["choices"][0].get("logprobs") is not None)
except Exception as e:
    print(f"Error: {e}")
