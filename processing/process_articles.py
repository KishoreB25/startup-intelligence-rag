import os
import json
import time
from llm_processing import extract_structured_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw", "news")
OUT_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(OUT_DIR, exist_ok=True)

# ---- CONFIG ----
SLEEP_BETWEEN_CALLS = 1.5   # seconds
MIN_TEXT_LENGTH = 300

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if len(text) < MIN_TEXT_LENGTH:
        print(f"⚠️ Skipping short file: {os.path.basename(file_path)}")
        return None

    try:
        return extract_structured_data(text)
    except Exception as e:
        return {
            "error": str(e),
            "source_file": os.path.basename(file_path)
        }


def main():
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".txt")]

    print(f"🔍 Found {len(files)} files to process...\n")

    for idx, filename in enumerate(files, start=1):
        input_path = os.path.join(RAW_DIR, filename)
        output_path = os.path.join(OUT_DIR, filename.replace(".txt", ".json"))

        # Skip if already processed
        if os.path.exists(output_path):
            print(f"⏭️ Skipped (already processed): {filename}")
            continue

        print(f"🔄 [{idx}/{len(files)}] Processing: {filename}")

        result = process_file(input_path)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        time.sleep(SLEEP_BETWEEN_CALLS)

    print("\n✅ Processing complete!")


if __name__ == "__main__":
    main()
