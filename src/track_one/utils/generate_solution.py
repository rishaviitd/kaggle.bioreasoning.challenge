"""Generate reasoning solutions for the local train set using GPT-OSS-120B on NVIDIA."""

import csv
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from client.nvidia_client import _client, chat_completion
from src.track_one.prompts.prompt import SOLUTION_GENERATION_V0

INPUT_CSV = ROOT_DIR / "data/local/local_train.csv"
OUTPUT_CSV = ROOT_DIR / "data/local/local_train_solution.csv"

MODEL = "openai/gpt-oss-120b"
MAX_WORKERS = 5

# Global counters for logging
completed_lock = threading.Lock()
completed_count = 0


def _process_one_row(client, row: dict[str, str]) -> dict[str, str]:
    """Send one request and return the row with populated reasoning."""
    prompt = SOLUTION_GENERATION_V0.format(
        pert=row["pert"],
        gene=row["gene"],
        true_label=row["label"].strip().lower()
    )

    request = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "extra_body": {"reasoning": {"effort": "high"}},
    }

    try:
        response_data = chat_completion(client, request)
        
        # Extract reasoning (We want the final generated content, NOT the internal thought process)
        choices = response_data.get("choices") or []
        message = choices[0].get("message") or {} if choices else {}
        final_content = message.get("content") or ""
        
        row["reasoning"] = str(final_content).strip()
        
    except Exception as e:
        row["reasoning"] = f"ERROR: {e}"
        
    return row


def generate_solutions(smoke: bool = False):
    global completed_count
    
    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} not found.")
        return

    # 1. Load Input Data
    with INPUT_CSV.open(newline="", encoding="utf-8") as f:
        all_rows = list(csv.DictReader(f))

    # 2. Load Existing Progress
    processed_keys = set()
    output_exists = OUTPUT_CSV.exists()
    
    if output_exists:
        with OUTPUT_CSV.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Use pert+gene as a unique key
                processed_keys.add(f"{row['pert']}_{row['gene']}")

    # 3. Filter Remaining
    remaining_rows = []
    for row in all_rows:
        key = f"{row['pert']}_{row['gene']}"
        if key not in processed_keys:
            remaining_rows.append(row)

    if smoke:
        remaining_rows = remaining_rows[:5]
        print(f"--- SMOKE TEST MODE (5 rows) ---")

    total_remaining = len(remaining_rows)
    print(f"Found {len(all_rows)} total rows.")
    print(f"Already processed: {len(processed_keys)} rows.")
    print(f"Remaining to process: {total_remaining} rows.")
    print(f"{'─' * 50}")

    if total_remaining == 0:
        print("All rows processed! Exiting.")
        return

    client = _client()
    completed_count = 0

    # 4. Process and Incremental Save
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    
    # We define the columns we want to save
    fieldnames = list(all_rows[0].keys()) + ["reasoning"]

    # Open file in append mode. If it didn't exist, write the header.
    with OUTPUT_CSV.open("a", newline="", encoding="utf-8") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=fieldnames, extrasaction="ignore")
        if not output_exists:
            writer.writeheader()

        print(f"Starting {MAX_WORKERS} workers...")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Map futures to their rows
            futures = {
                executor.submit(_process_one_row, client, row.copy()): row
                for row in remaining_rows
            }

            for future in as_completed(futures):
                result_row = future.result()
                
                # Write to disk immediately
                writer.writerow(result_row)
                out_f.flush() # Force flush to disk
                
                # Thread-safe progress update
                with completed_lock:
                    completed_count += 1
                    print(f"\rProgress: [{completed_count}/{total_remaining}] rows completed.    ", end="", flush=True)

    print("\n\nDone! All rows processed.")

if __name__ == "__main__":
    is_smoke = "--smoke" in sys.argv
    generate_solutions(smoke=is_smoke)
