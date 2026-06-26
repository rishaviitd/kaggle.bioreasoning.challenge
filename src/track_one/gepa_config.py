import os
import dspy
from dotenv import load_dotenv


NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"


def _nvidia_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY environment variable is missing.")
    return api_key


def get_student_lm():
    return dspy.LM(
        model="openai/gpt-oss-120b",
        api_base=NVIDIA_API_BASE,
        api_key=_nvidia_api_key(),
        max_tokens=65_536,
        temperature=1.0,
        top_p=1.0,
        model_type="chat",
    )


def get_refiner_lm():
    return dspy.LM(
        model="z-ai/glm-5.1",
        api_base=NVIDIA_API_BASE,
        api_key=_nvidia_api_key(),
        max_tokens=16_384,
        temperature=0,
        top_p=1.0,
        model_type="chat",
    )
