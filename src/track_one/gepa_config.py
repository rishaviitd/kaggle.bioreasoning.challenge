import os
import threading
import time
import dspy
from dotenv import load_dotenv


NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
REQUEST_GAP_SECONDS = 12
RATE_LIMIT_BACKOFF_SECONDS = (30, 60, 120)
_request_lock = threading.Lock()
_last_request_started = 0.0


class RateLimitedLM(dspy.LM):
    def _wait_for_slot(self):
        global _last_request_started

        with _request_lock:
            elapsed = time.monotonic() - _last_request_started
            if _last_request_started and elapsed < REQUEST_GAP_SECONDS:
                delay = REQUEST_GAP_SECONDS - elapsed
                print(f"Waiting {delay:.1f}s before next NVIDIA request...")
                time.sleep(delay)
            _last_request_started = time.monotonic()

    def forward(self, prompt=None, messages=None, **kwargs):
        for attempt in range(len(RATE_LIMIT_BACKOFF_SECONDS) + 1):
            self._wait_for_slot()
            try:
                return super().forward(prompt=prompt, messages=messages, **kwargs)
            except Exception as exc:
                is_rate_limit = "429" in str(exc) or "Too Many Requests" in str(exc)
                if not is_rate_limit or attempt == len(RATE_LIMIT_BACKOFF_SECONDS):
                    raise

                delay = RATE_LIMIT_BACKOFF_SECONDS[attempt]
                print(f"NVIDIA rate limit hit. Retrying in {delay}s...")
                time.sleep(delay)

        raise RuntimeError("unreachable NVIDIA retry state")


def _nvidia_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY environment variable is missing.")
    return api_key


def get_student_lm():
    return RateLimitedLM(
        model="openai/openai/gpt-oss-120b",
        api_base=NVIDIA_API_BASE,
        api_key=_nvidia_api_key(),
        max_tokens=65_536,
        temperature=1.0,
        top_p=1.0,
        num_retries=0,
        model_type="chat",
    )


def get_refiner_lm():
    return RateLimitedLM(
        model="openai/z-ai/glm-5.1",
        api_base=NVIDIA_API_BASE,
        api_key=_nvidia_api_key(),
        max_tokens=16_384,
        temperature=0,
        top_p=1.0,
        extra_body={"chat_template_kwargs": {"thinking": False}},
        num_retries=0,
        model_type="chat",
    )
