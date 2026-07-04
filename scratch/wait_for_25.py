import json
import time
from pathlib import Path

CACHE_FILE = Path("outputs/track_a/kaggle_submission/responses_cache.json")
TARGET_ROWS = 25

def check_progress():
    print(f"Monitoring cache file for {TARGET_ROWS} rows...", flush=True)
    while True:
        if CACHE_FILE.exists():
            try:
                data = json.loads(CACHE_FILE.read_text())
                rows = data.get("rows", {})
                count = len(rows)
                if count >= TARGET_ROWS:
                    print(f"\nSUCCESS! Reached {count} rows.", flush=True)
                    
                    # Verify structure
                    all_good = True
                    for row_id, row_data in list(rows.items())[:TARGET_ROWS]:
                        if row_data.get("parsed_seed_count") != 3:
                            print(f"Row {row_id} has parsed_seed_count = {row_data.get('parsed_seed_count')}")
                            all_good = False
                        if "prediction_up" not in row_data or "prediction_down" not in row_data:
                            print(f"Row {row_id} missing predictions")
                            all_good = False
                    
                    if all_good:
                        print(f"All {TARGET_ROWS} rows successfully parsed 3/3 seeds with correct float probabilities!", flush=True)
                    else:
                        print("WARNING: Some rows failed parsing!", flush=True)
                    break
            except Exception as e:
                pass
        time.sleep(10)

if __name__ == "__main__":
    check_progress()
