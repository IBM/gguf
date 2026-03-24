#!/usr/bin/env python3
"""
Validate and display embedding data from llama-embedding JSON output.
"""

import sys
import json


def main():
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python validate_embedding_json.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]

    # Validate that filename is not empty
    if not json_file or json_file.strip() == "":
        print("[ERROR] Filename argument is empty")
        sys.exit(1)

    print(f"[INFO] Validating JSON file: {json_file}")

    try:
        # Load JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)

        print("[INFO] JSON file loaded successfully")

        # Validate structure
        if 'data' not in data:
            print("[ERROR] JSON does not contain 'data' field")
            sys.exit(1)

        if not isinstance(data['data'], list):
            print("[ERROR] 'data' field is not an array")
            sys.exit(1)

        if len(data['data']) == 0:
            print("[ERROR] 'data' array is empty")
            sys.exit(1)

        print(f"[SUCCESS] Found {len(data['data'])} embedding(s) in data array")
        print()

        # Process each embedding in the data array
        for idx, item in enumerate(data['data']):
            print(f"=== Embedding at index {idx} ===")

            if 'index' in item:
                print(f"  Index field: {item['index']}")

            if 'object' in item:
                print(f"  Object type: {item['object']}")

            if 'embedding' not in item:
                print(f"  [ERROR] No 'embedding' field found at index {idx}")
                continue

            embedding = item['embedding']

            if not isinstance(embedding, list):
                print(f"  [ERROR] 'embedding' is not an array at index {idx}")
                continue

            print(f"  Embedding dimensions: {len(embedding)}")
            print(f"  First 10 values: {embedding[:10]}")
            print(f"  Last 10 values: {embedding[-10:]}")

            # Calculate some statistics
            if len(embedding) > 0:
                min_val = min(embedding)
                max_val = max(embedding)
                avg_val = sum(embedding) / len(embedding)
                print(f"  Min value: {min_val:.6f}")
                print(f"  Max value: {max_val:.6f}")
                print(f"  Average value: {avg_val:.6f}")

            print()

        print("[SUCCESS] All embeddings validated successfully")
        return 0

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
        return 1
    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_file}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob