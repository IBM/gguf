#!/usr/bin/env python3
"""
Check if a model is supported by llama.cpp based on collection mapping.

This script reads the HF collection mapping and checks if a specific model
has llama.cpp support enabled. This is used to conditionally skip BVT/UAT
testing for models with unsupported architectures.

Usage:
    python scripts/is_model_llama_cpp_supported.py <collection_mapping_file> <repo_id>

Returns:
    - "true" if model is supported (or if llama_cpp_supported is not specified, defaults to true)
    - "false" if model is explicitly marked as unsupported
    - Exit code 0 on success, 1 on error
"""

import json
import sys
import os


def is_model_llama_cpp_supported(collection_mapping_file, repo_id, default_supported=True):
    """
    Check if a model is supported by llama.cpp.

    Args:
        collection_mapping_file: Path to the collection mapping JSON file
        repo_id: Full repository ID (e.g., "ibm-granite/granite-4.0-3b-vision")
        default_supported: Default value if llama_cpp_supported is not specified

    Returns:
        bool: True if supported, False otherwise
    """
    # Extract repo_name from repo_id (e.g., "ibm-granite/granite-4.0-3b-vision" -> "granite-4.0-3b-vision")
    repo_name = repo_id.split('/')[-1] if '/' in repo_id else repo_id

    try:
        with open(collection_mapping_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Collection mapping file not found: {collection_mapping_file}", file=sys.stderr)
        return default_supported
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in collection mapping file: {e}", file=sys.stderr)
        return default_supported

    # Search through collections for matching repo_name
    for collection in data.get('collections', []):
        for item in collection.get('items', []):
            if item.get('repo_name') == repo_name:
                # Return the llama_cpp_supported value, defaulting to True if not specified
                supported = item.get('llama_cpp_supported', default_supported)
                return supported

    # If model not found in mapping, default to supported
    return default_supported


def main():
    if len(sys.argv) < 3:
        print("Usage: python is_model_llama_cpp_supported.py <collection_mapping_file> <repo_id>", file=sys.stderr)
        sys.exit(1)

    collection_mapping_file = sys.argv[1]
    repo_id = sys.argv[2]

    # Check if file exists
    if not os.path.exists(collection_mapping_file):
        print(f"Error: Collection mapping file not found: {collection_mapping_file}", file=sys.stderr)
        sys.exit(1)

    # Get support status
    is_supported = is_model_llama_cpp_supported(collection_mapping_file, repo_id)

    # Output as string for GitHub Actions
    print("true" if is_supported else "false")

    return 0


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
