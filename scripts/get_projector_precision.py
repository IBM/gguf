#!/usr/bin/env python3
"""
Get the projector_precision for a model from the HF collection mapping JSON.

Usage:
    python get_projector_precision.py <collection_mapping_file> <repo_name> [default_precision]

Arguments:
    collection_mapping_file: Path to the hf_collection_mapping_gguf.json file
    repo_name: The repository name to search for (e.g., "granite-vision-3.3-2b")
    default_precision: Optional default precision to return if projector_precision is not found (default: "f16")

Returns:
    The projector_precision if found, otherwise the default_precision
"""

import json
import sys


def get_projector_precision(collection_mapping_file, repo_id, default_precision="f16"):
    """
    Extract the projector_precision for a given repo_id from the collection mapping.

    Args:
        collection_mapping_file: Path to the JSON file
        repo_id: Repository ID (can be "org/repo" or just "repo")
        default_precision: Default precision to return if not found

    Returns:
        The projector_precision or default_precision
    """
    try:
        with open(collection_mapping_file, 'r') as f:
            data = json.load(f)

        # Extract just the repo name from repo_id (e.g., "ibm-granite/granite-vision-3.3-2b" -> "granite-vision-3.3-2b")
        repo_name = repo_id.split('/')[-1] if '/' in repo_id else repo_id

        # Search through all collections and items
        for collection in data.get('collections', []):
            for item in collection.get('items', []):
                if item.get('repo_name') == repo_name:
                    projector_precision = item.get('projector_precision')
                    if projector_precision:
                        return projector_precision
                    else:
                        return default_precision

        # If repo not found, return default
        return default_precision

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
        print("Usage: python get_projector_precision.py <collection_mapping_file> <repo_id> [default_precision]", file=sys.stderr)
        sys.exit(1)

    collection_mapping_file = sys.argv[1]
    repo_id = sys.argv[2]
    default_precision = sys.argv[3] if len(sys.argv) > 3 else "f16"

    projector_precision = get_projector_precision(collection_mapping_file, repo_id, default_precision)
    print(projector_precision)


if __name__ == "__main__":
    main()

# Made with Bob
