import os
import dspy
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("NVIDIA_API_KEY")
if not api_key:
    raise ValueError("NVIDIA_API_KEY environment variable is missing.")

NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"

def get_student_lm():
    # OpenAI compatible client setup for NVIDIA NIM
    return dspy.LM(
        model="openai/gpt-oss-120b",
        api_base=NVIDIA_API_BASE,
        api_key=api_key,
        max_tokens=4096,
        temperature=1.0,
        model_type="chat"
    )

def get_refiner_lm():
    return dspy.LM(
        model="z-ai/glm-5.1",
        api_base=NVIDIA_API_BASE,
        api_key=api_key,
        max_tokens=4096,
        temperature=1.0,  # High temp for creative feedback/proposals
        model_type="chat"
    )
