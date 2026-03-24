#!/usr/bin/env python3
"""
Validate and display embedding data from llama-embedding JSON output.
Handles raw llama-embedding output by extracting JSON from the log.
"""

import sys
import json


def extract_json_from_log(content):
    """
    Extract JSON object from llama-embedding log output.
    Strips all non-JSON lines before and after the JSON object.

    Args:
        content: Raw file content that may contain log lines and JSON

    Returns:
        str: Extracted JSON string, or None if not found
    """
    # Find the first occurrence of '{'
    start_idx = content.find('{')
    if start_idx == -1:
        return None

    # Find the matching closing brace by counting braces
    brace_count = 0
    in_string = False
    escape_next = False

    for i in range(start_idx, len(content)):
        char = content[i]

        # Handle string escaping
        if escape_next:
            escape_next = False
            continue

        if char == '\\':
            escape_next = True
            continue

        # Track if we're inside a string
        if char == '"':
            in_string = not in_string
            continue

        # Only count braces outside of strings
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    # Found the matching closing brace
                    return content[start_idx:i+1]

    return None


def validate_embedding_structure(data):
    """
    Validate the structure of embedding JSON data.

    Args:
        data: Parsed JSON object

    Returns:
        int: 0 if valid, 1 if invalid
    """
    # Validate structure
    if 'data' not in data:
        print("[ERROR] JSON does not contain 'data' field")
        return 1

    if not isinstance(data['data'], list):
        print("[ERROR] 'data' field is not an array")
        return 1

    if len(data['data']) == 0:
        print("[ERROR] 'data' array is empty")
        return 1

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
        # Read the file content
        with open(json_file, 'r') as f:
            content = f.read()

        if not content.strip():
            print("[ERROR] File is empty")
            sys.exit(1)

        # Try to parse as JSON directly first
        try:
            data = json.loads(content)
            print("[INFO] File contains valid JSON")
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from log output
            print("[INFO] File is not pure JSON, attempting to extract JSON from log output...")
            json_str = extract_json_from_log(content)

            if json_str is None:
                print("[ERROR] Could not find JSON object in file")
                print("[INFO] File content preview (first 500 chars):")
                print(content[:500])
                sys.exit(1)

            print(f"[INFO] Extracted JSON object ({len(json_str)} characters)")
            data = json.loads(json_str)
            print("[INFO] Extracted JSON is valid")

        # Validate the embedding structure
        result = validate_embedding_structure(data)
        sys.exit(result)

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_file}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob