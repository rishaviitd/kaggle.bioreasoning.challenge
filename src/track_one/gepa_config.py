import os
import sys
import threading
import time
import dspy
from dotenv import load_dotenv

try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None


NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
REQUEST_GAP_SECONDS = 2
RATE_LIMIT_BACKOFF_SECONDS = (30, 60, 120)
DEEPSEEK_MAX_COMPLETION_TOKENS = 384_000
_request_lock = threading.Lock()
_last_request_started = 0.0


class RateLimitedLM(dspy.LM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._progress_label = None
        self._progress_total = 0
        self._progress_count = 0
        self._progress_bar = None

    def start_progress(self, label: str, total: int) -> None:
        self.close_progress()
        self._progress_label = label
        self._progress_total = total
        self._progress_count = 0
        if tqdm is not None:
            self._progress_bar = tqdm(
                total=total,
                desc=f"NVIDIA {label}",
                unit="req",
                dynamic_ncols=True,
                leave=False,
                position=0,
                file=sys.stderr,
            )
        else:
            print(f"NVIDIA {label}: 0/{total} requests", file=sys.stderr)

    def has_progress(self) -> bool:
        return self._progress_label is not None

    def close_progress(self) -> None:
        if self._progress_bar is not None:
            self._progress_bar.close()
        self._progress_label = None
        self._progress_total = 0
        self._progress_count = 0
        self._progress_bar = None

    def _log(self, message: str) -> None:
        if self._progress_bar is not None:
            self._progress_bar.write(message)
        else:
            print(message, file=sys.stderr)

    def _advance_progress(self):
        if not self._progress_label:
            return

        self._progress_count += 1
        if self._progress_bar is not None:
            self._progress_bar.update(1)
        else:
            print(
                f"NVIDIA {self._progress_label}: "
                f"{self._progress_count}/{self._progress_total} requests",
                file=sys.stderr,
            )

        if self._progress_count >= self._progress_total:
            self.close_progress()

    def _wait_for_slot(self):
        global _last_request_started

        with _request_lock:
            elapsed = time.monotonic() - _last_request_started
            if _last_request_started and elapsed < REQUEST_GAP_SECONDS:
                delay = REQUEST_GAP_SECONDS - elapsed
                time.sleep(delay)
            _last_request_started = time.monotonic()

    def forward(self, prompt=None, messages=None, **kwargs):
        for attempt in range(len(RATE_LIMIT_BACKOFF_SECONDS) + 1):
            self._wait_for_slot()
            try:
                response = super().forward(prompt=prompt, messages=messages, **kwargs)
                self._advance_progress()
                return response
            except Exception as exc:
                is_rate_limit = "429" in str(exc) or "Too Many Requests" in str(exc)
                if not is_rate_limit or attempt == len(RATE_LIMIT_BACKOFF_SECONDS):
                    raise

                delay = RATE_LIMIT_BACKOFF_SECONDS[attempt]
                self._log(f"NVIDIA rate limit hit. Retrying in {delay}s...")
                time.sleep(delay)

        raise RuntimeError("unreachable NVIDIA retry state")


def _nvidia_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY environment variable is missing.")
    return api_key


def _openrouter_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is missing.")
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


def _get_deepseek_lm(role_name: str, temperature: float):
    print(f"Using OpenRouter DeepSeek {role_name} model...")
    return dspy.LM(
        model="openrouter/deepseek/deepseek-v4-pro",
        api_base=OPENROUTER_API_BASE,
        api_key=_openrouter_api_key(),
        max_tokens=DEEPSEEK_MAX_COMPLETION_TOKENS,
        temperature=temperature,
        top_p=1.0,
        extra_body={"reasoning": {"enabled": True, "effort": "high"}},
        num_retries=0,
        model_type="chat",
    )


def get_feedback_lm():
    return _get_deepseek_lm(role_name="feedback", temperature=1.0)


def get_refiner_lm():
    return _get_deepseek_lm(role_name="refiner", temperature=1.0)
