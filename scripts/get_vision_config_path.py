#!/usr/bin/env python3
"""
Get the vision_config path for a model from the HF collection mapping JSON.

Usage:
    python get_vision_config_path.py <collection_mapping_file> <repo_name> [default_path]

Arguments:
    collection_mapping_file: Path to the hf_collection_mapping_gguf.json file
    repo_name: The repository name to search for (e.g., "granite-vision-3.3-2b")
    default_path: Optional default path to return if vision_config is not found

Returns:
    The vision_config path if found, otherwise the default_path or empty string
"""

import json
import sys


def get_vision_config_path(collection_mapping_file, repo_name, default_path=""):
    """
    Extract the vision_config path for a given repo_name from the collection mapping.

    Args:
        collection_mapping_file: Path to the JSON file
        repo_name: Repository name to search for
        default_path: Default path to return if not found

    Returns:
        The vision_config path or default_path
    """
    try:
        with open(collection_mapping_file, 'r') as f:
            data = json.load(f)

        # Search through all collections and items
        for collection in data.get('collections', []):
            for item in collection.get('items', []):
                if item.get('repo_name') == repo_name:
                    vision_config = item.get('vision_config')
                    if vision_config:
                        return vision_config
                    else:
                        return default_path

        # If repo not found, return default
        return default_path

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
    if len(sys.argv) < 3:
        print("Usage: python get_vision_config_path.py <collection_mapping_file> <repo_name> [default_path]", file=sys.stderr)
        sys.exit(1)

    collection_mapping_file = sys.argv[1]
    repo_name = sys.argv[2]
    default_path = sys.argv[3] if len(sys.argv) > 3 else ""

    vision_config_path = get_vision_config_path(collection_mapping_file, repo_name, default_path)
    print(vision_config_path)


if __name__ == "__main__":
    main()

# Made with Bob
