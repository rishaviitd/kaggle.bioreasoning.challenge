"""Generate a resumable Track A Kaggle submission with GPT-OSS logprobs."""

from __future__ import annotations

import csv
import json
import math
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import dspy
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from client.nvidia_client import _client, chat_completion, STUDENT_MODEL as MODEL
from src.track_one.utils.evaluate import _response_content, _seed_probabilities
from src.track_one.prompts.prompt import PROMPT_V5


TEST_PATH = Path("data/test.csv")
SAMPLE_SUBMISSION_PATH = Path("data/submission_format/sample_submission_track_a.csv")
OUTPUT_DIR = Path("outputs/track_a/kaggle_submission")
SUBMISSION_PATH = OUTPUT_DIR / "submission.csv"
PROMPT_PATH = OUTPUT_DIR / "prompt.txt"
CACHE_PATH = OUTPUT_DIR / "responses_cache.json"
FAILURES_PATH = OUTPUT_DIR / "failures.json"
ZIP_PATH = OUTPUT_DIR / "submission_track_a.zip"

SEEDS = (42, 43, 44)
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 65_536
REASONING_EFFORT = "medium"
TOP_LOGPROBS = 20
MAX_RETRIES = 3
TIMEOUT_MS = 240_000
ROW_WORKERS = 1

FALLBACK_UP = 0.306165
FALLBACK_DOWN = 0.140947
FALLBACK_TRACE = (
    "Fallback used: all three seed calls failed probability extraction; "
    "filled with exact train-label priors."
)

SUBMISSION_COLUMNS = [
    "id",
    "prediction_up",
    "prediction_down",
    "prediction_up_seed42",
    "prediction_down_seed42",
    "reasoning_trace_seed42",
    "prediction_up_seed43",
    "prediction_down_seed43",
    "reasoning_trace_seed43",
    "prediction_up_seed44",
    "prediction_down_seed44",
    "reasoning_trace_seed44",
    "tokens_used",
    "prompt_tokens",
    "model_name",
]


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Could not read {path}; starting with empty state.", flush=True)
        return default


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class SimpleClassificationSignature(dspy.Signature):
    __doc__ = PROMPT_V5.split("### Query")[0].strip()
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")


class KaggleTaskLM(dspy.LM):
    def __init__(self, seed: int, client: OpenAI):
        super().__init__("openai/gpt-oss-120b")
        self.seed = seed
        self.client = client
        
    def __call__(self, prompt=None, messages=None, **kwargs):
        if messages:
            content = "\n\n".join([m["content"] for m in messages])
            api_messages = [{"role": "user", "content": content}]
        else:
            api_messages = [{"role": "user", "content": prompt}]
            
        request = {
            "model": MODEL,
            "messages": api_messages,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "seed": self.seed,
            "max_tokens": MAX_TOKENS,
            "logprobs": True,
            "top_logprobs": 5,
            "extra_body": {"reasoning": {"effort": REASONING_EFFORT}},
        }
        response = chat_completion(self.client, request)
        text = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        self.history.append({
            "prompt": prompt, 
            "messages": messages,
            "response": text, 
            "kwargs": kwargs, 
            "raw_response": response
        })
        return [text]


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=SUBMISSION_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _rough_prompt_tokens(prompt: str) -> int:
    return math.ceil(len(prompt) / 4)


def _seed_done(cached: dict[str, Any], seed: int) -> bool:
    return (
        f"prediction_up_seed{seed}" in cached
        and f"prediction_down_seed{seed}" in cached
        and f"reasoning_trace_seed{seed}" in cached
    )


def _row_done(cached: dict[str, Any]) -> bool:
    return all(_seed_done(cached, seed) for seed in SEEDS)


def _send_seed(
    client: OpenAI,
    row: dict[str, str],
    seed: int,
) -> tuple[dict[str, Any] | None, dict[str, float] | None, dict[str, Any] | None]:
    started = time.monotonic()
    try:
        lm = KaggleTaskLM(seed=seed, client=client)
        with dspy.context(lm=lm):
            program = dspy.ChainOfThought(SimpleClassificationSignature)
            pred = program(pert=row["pert"], gene=row["gene"])
        
        data = lm.history[-1]["raw_response"]
        data["elapsed_seconds"] = time.monotonic() - started
        probabilities = _seed_probabilities(data)
        if probabilities is None:
            return data, None, {"seed": seed, "reason": "logprob_extraction_failed"}
        return data, probabilities, None
    except Exception as exc:
        return None, None, {"seed": seed, "reason": str(exc)}


def _run_seed_with_retries(
    client: OpenAI,
    row: dict[str, str],
    seed: int,
) -> dict[str, Any]:
    errors = []
    for attempt in range(1, MAX_RETRIES + 1):
        response, probabilities, failure = _send_seed(client, row, seed)
        if probabilities is not None:
            usage = (response or {}).get("usage") or {}
            choices = (response or {}).get("choices") or []
            message = choices[0].get("message") or {} if choices else {}
            reasoning = message.get("reasoning") or message.get("reasoning_content") or ""
            content = message.get("content") or ""
            trace = f"{reasoning}\n\n{content}".strip()
            return {
                "seed": seed,
                "ok": True,
                "probabilities": probabilities,
                "response": response,
                "usage": usage,
                "trace": trace or "none",
                "attempts": attempt,
            }

        errors.append(
            {
                "attempt": attempt,
                "failure": failure,
                "response": response,
            }
        )
        if attempt < MAX_RETRIES:
            time.sleep(2 ** (attempt - 1))

    return {
        "seed": seed,
        "ok": False,
        "errors": errors,
        "attempts": MAX_RETRIES,
    }


def _average_probabilities(results: list[dict[str, Any]]) -> tuple[float, float]:
    successful = [result for result in results if result.get("ok")]
    if not successful:
        return FALLBACK_UP, FALLBACK_DOWN

    up = sum(result["probabilities"]["up"] for result in successful) / len(successful)
    down = sum(result["probabilities"]["down"] for result in successful) / len(successful)
    return up, down


def _usage_total(results: list[dict[str, Any]], key: str) -> int:
    total = 0
    for result in results:
        usage = result.get("usage") or {}
        total += int(usage.get(key) or 0)
    return total


def _usage_max(results: list[dict[str, Any]], key: str) -> int:
    values = []
    for result in results:
        usage = result.get("usage") or {}
        if usage.get(key) is not None:
            values.append(int(usage[key]))
    return max(values) if values else 0


def _build_cache_row(
    row: dict[str, str],
    results: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    successful_count = sum(1 for result in results if result.get("ok"))
    final_up, final_down = _average_probabilities(results)
    prompt_tokens = _usage_max(results, "prompt_tokens") or 0

    cached: dict[str, Any] = {
        "id": row["id"],
        "pert": row["pert"],
        "gene": row["gene"],
        "prediction_up": final_up,
        "prediction_down": final_down,
        "tokens_used": _usage_total(results, "total_tokens"),
        "prompt_tokens": prompt_tokens,
        "model_name": MODEL,
        "parsed_seed_count": successful_count,
    }

    failures = []
    for result in sorted(results, key=lambda item: item["seed"]):
        seed = result["seed"]
        if result.get("ok"):
            probabilities = result["probabilities"]
            cached[f"prediction_up_seed{seed}"] = probabilities["up"]
            cached[f"prediction_down_seed{seed}"] = probabilities["down"]
            cached[f"reasoning_trace_seed{seed}"] = result.get("trace") or "none"
            cached[f"tokens_seed{seed}"] = int((result.get("usage") or {}).get("total_tokens") or 0)
            continue

        cached[f"prediction_up_seed{seed}"] = final_up
        cached[f"prediction_down_seed{seed}"] = final_down
        cached[f"reasoning_trace_seed{seed}"] = FALLBACK_TRACE
        cached[f"tokens_seed{seed}"] = 0
        failures.append(
            {
                "id": row["id"],
                "pert": row["pert"],
                "gene": row["gene"],
                "seed": seed,
                "errors": result.get("errors") or [],
            }
        )

    return cached, failures


def _submission_rows(test_rows: list[dict[str, str]], cache_rows: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in test_rows:
        cached = cache_rows.get(row["id"]) or {}
        rows.append(
            {
                "id": row["id"],
                "prediction_up": cached.get("prediction_up", FALLBACK_UP),
                "prediction_down": cached.get("prediction_down", FALLBACK_DOWN),
                "prediction_up_seed42": cached.get("prediction_up_seed42", FALLBACK_UP),
                "prediction_down_seed42": cached.get("prediction_down_seed42", FALLBACK_DOWN),
                "reasoning_trace_seed42": cached.get("reasoning_trace_seed42", FALLBACK_TRACE),
                "prediction_up_seed43": cached.get("prediction_up_seed43", FALLBACK_UP),
                "prediction_down_seed43": cached.get("prediction_down_seed43", FALLBACK_DOWN),
                "reasoning_trace_seed43": cached.get("reasoning_trace_seed43", FALLBACK_TRACE),
                "prediction_up_seed44": cached.get("prediction_up_seed44", FALLBACK_UP),
                "prediction_down_seed44": cached.get("prediction_down_seed44", FALLBACK_DOWN),
                "reasoning_trace_seed44": cached.get("reasoning_trace_seed44", FALLBACK_TRACE),
                "tokens_used": int(cached.get("tokens_used") or 0),
                "prompt_tokens": int(cached.get("prompt_tokens") or 0),
                "model_name": cached.get("model_name", MODEL),
            }
        )
    return rows


def _write_submission_artifacts(test_rows: list[dict[str, str]], cache_rows: dict[str, Any]) -> None:
    submission_rows = _submission_rows(test_rows, cache_rows)
    _write_csv(SUBMISSION_PATH, submission_rows)
    PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROMPT_PATH.write_text(PROMPT_V5, encoding="utf-8")
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(SUBMISSION_PATH, "submission.csv")
        archive.write(PROMPT_PATH, "prompt.txt")


def _validate_sample_columns() -> None:
    sample_rows = _load_csv(SAMPLE_SUBMISSION_PATH)
    if not sample_rows:
        raise RuntimeError(f"{SAMPLE_SUBMISSION_PATH} is empty")
    sample_columns = list(sample_rows[0].keys())
    if sample_columns != SUBMISSION_COLUMNS:
        raise RuntimeError(
            "Track A sample submission columns changed.\n"
            f"Expected: {SUBMISSION_COLUMNS}\n"
            f"Found:    {sample_columns}"
        )


def _existing_seed_results(cached: dict[str, Any]) -> list[dict[str, Any]]:
    existing_results = []
    for seed in SEEDS:
        if _seed_done(cached, seed):
            existing_results.append(
                {
                    "seed": seed,
                    "ok": True,
                    "probabilities": {
                        "up": float(cached[f"prediction_up_seed{seed}"]),
                        "down": float(cached[f"prediction_down_seed{seed}"]),
                        "none": max(
                            0.0,
                            1.0
                            - float(cached[f"prediction_up_seed{seed}"])
                            - float(cached[f"prediction_down_seed{seed}"]),
                        ),
                    },
                    "usage": {"total_tokens": int(cached.get(f"tokens_seed{seed}") or 0)},
                    "trace": cached.get(f"reasoning_trace_seed{seed}") or "none",
                }
            )
    return existing_results


def _row_cost(results: list[dict[str, Any]]) -> float:
    total_cost = 0.0
    for result in results:
        response = result.get("response") or {}
        usage = response.get("usage") or {}
        total_cost += float(usage.get("cost") or 0.0)
    return total_cost


def _process_row(
    client: OpenAI,
    row: dict[str, str],
    cached: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], float]:
    print(f"Row {row['id']} | sending missing seed calls...", flush=True)
    with ThreadPoolExecutor(max_workers=len(SEEDS)) as executor:
        future_to_seed = {
            executor.submit(_run_seed_with_retries, client, row, seed): seed
            for seed in SEEDS
            if not _seed_done(cached, seed)
        }
        results = []
        for future in as_completed(future_to_seed):
            result = future.result()
            results.append(result)
            status = "parsed" if result.get("ok") else "failed"
            print(
                f"Row {row['id']} | seed {result['seed']} {status} "
                f"after {result['attempts']} attempt(s)",
                flush=True,
            )

    all_results = _existing_seed_results(cached) + results
    cache_row, row_failures = _build_cache_row(row, all_results)
    return cache_row, row_failures, _row_cost(results)


def generate() -> None:
    print("Starting Track A Kaggle submission generation...", flush=True)
    print(f"Input test rows: {TEST_PATH}", flush=True)
    print(f"Output dir: {OUTPUT_DIR}", flush=True)
    print(f"Model: {MODEL}", flush=True)
    print(
        "Settings: "
        f"seeds={SEEDS}, temperature={TEMPERATURE}, top_p={TOP_P}, "
        f"max_tokens={MAX_TOKENS}, reasoning_effort={REASONING_EFFORT}, "
        f"top_logprobs={TOP_LOGPROBS}, row_workers={ROW_WORKERS}, "
        f"max_in_flight_requests={ROW_WORKERS * len(SEEDS)}",
        flush=True,
    )

    # _validate_sample_columns()
    test_rows = _load_csv(TEST_PATH)[:50]
    cache = _load_json(CACHE_PATH, {"rows": {}})
    failures = _load_json(FAILURES_PATH, [])
    cache_rows = cache.setdefault("rows", {})
    client = _client()

    _write_submission_artifacts(test_rows, cache_rows)
    total = len(test_rows)
    print(f"Loaded {total} test rows.", flush=True)
    print(f"Already completed rows: {sum(1 for row in test_rows if _row_done(cache_rows.get(row['id'], {})))}", flush=True)

    pending_rows = []
    for index, row in enumerate(test_rows, start=1):
        cached = cache_rows.get(row["id"]) or {}
        if _row_done(cached):
            print(f"Row {index}/{total} {row['id']} | cache hit", flush=True)
            continue
        pending_rows.append((index, row, cached))

    print(f"Rows left to process: {len(pending_rows)}", flush=True)
    completed_this_run = 0
    with ThreadPoolExecutor(max_workers=ROW_WORKERS) as row_executor:
        future_to_item = {
            row_executor.submit(_process_row, client, row, cached): (index, row)
            for index, row, cached in pending_rows
        }
        for future in as_completed(future_to_item):
            index, row = future_to_item[future]
            cache_row, row_failures, row_cost = future.result()
            cache_rows[row["id"]] = cache_row
            failures.extend(row_failures)
            completed_this_run += 1

            _write_json(CACHE_PATH, cache)
            _write_json(FAILURES_PATH, failures)
            _write_submission_artifacts(test_rows, cache_rows)

            print(
                f"Row {index}/{total} {row['id']} | "
                f"parsed={cache_row['parsed_seed_count']}/3 | "
                f"up={cache_row['prediction_up']:.6f} "
                f"down={cache_row['prediction_down']:.6f} | "
                f"tokens={cache_row['tokens_used']} | "
                f"row_cost=${row_cost:.6f} | "
                f"completed_this_run={completed_this_run}/{len(pending_rows)} | "
                f"failures_total={len(failures)}",
                flush=True,
            )

    _write_submission_artifacts(test_rows, cache_rows)
    print("Track A submission generation complete.", flush=True)
    print(f"Wrote {SUBMISSION_PATH}", flush=True)
    print(f"Wrote {PROMPT_PATH}", flush=True)
    print(f"Wrote {FAILURES_PATH}", flush=True)
    print(f"Wrote {ZIP_PATH}", flush=True)


if __name__ == "__main__":
    generate()
