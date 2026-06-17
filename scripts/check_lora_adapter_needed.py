#!/usr/bin/env python3
"""
Check if a model requires a LoRA adapter from the HF collection mapping JSON.

Usage:
    python check_lora_adapter_needed.py --collection-mapping <file> --repo-name <name>
    python check_lora_adapter_needed.py -c <file> -r <name>

Arguments:
    --collection-mapping, -c: Path to the hf_collection_mapping_gguf.json file
    --repo-name, -r: The repository name to search for (e.g., "granite-vision-3.3-2b")

Returns:
    Prints 'true' if LoRA adapter is needed, 'false' otherwise
    Exit code 0 on success
"""

import argparse
import json
import sys


def check_lora_adapter_needed(collection_mapping_file, repo_name):
    """
    Check if a model requires a LoRA adapter based on the collection mapping.

    Args:
        collection_mapping_file: Path to the JSON file
        repo_name: Repository name to search for

    Returns:
        Boolean indicating if LoRA adapter is needed
    """
    try:
        with open(collection_mapping_file, 'r') as f:
            data = json.load(f)

        # Search through all collections and items
        for collection in data.get('collections', []):
            for item in collection.get('items', []):
                if item.get('repo_name') == repo_name:
                    # Return the lora_adapter value, defaulting to False if not present
                    return item.get('lora_adapter', False)

        # If repo not found, return False
        return False

    except FileNotFoundError:
        print(f"Error: File not found: {collection_mapping_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {collection_mapping_file}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--collection-mapping', '-c',
        type=str,
        required=True,
        help='Path to the hf_collection_mapping_gguf.json file'
    )

    parser.add_argument(
        '--repo-name', '-r',
        type=str,
        required=True,
        help='Repository name to search for (e.g., "granite-vision-3.3-2b")'
    )

    try:
        args = parser.parse_args()

        lora_needed = check_lora_adapter_needed(args.collection_mapping, args.repo_name)

        # Print lowercase string for shell script compatibility
        print(str(lora_needed).lower())

    except SystemExit as se:
        sys.exit(se.code if se.code is not None else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()

# Made with Bob
