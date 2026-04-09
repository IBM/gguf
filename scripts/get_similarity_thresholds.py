#!/usr/bin/env python3
"""
Get similarity thresholds for embedding models from configuration.

This script reads the hf_collection_mapping_gguf.json configuration file
and returns the similarity thresholds for a specific embedding model.
"""

import sys
import json
import argparse
from pathlib import Path


def get_similarity_thresholds(config_path, repo_id):
    """
    Get similarity thresholds for a specific embedding model.

    Args:
        config_path: Path to hf_collection_mapping_gguf.json
        repo_id: Repository ID (e.g., 'ibm-granite/granite-embedding-30m-english')

    Returns:
        tuple: (threshold_high, threshold_low) or (None, None) if not found
    """
    # Extract repo name from full repo_id
    if '/' in repo_id:
        repo_name = repo_id.split('/')[-1]
    else:
        repo_name = repo_id

    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Search for the model in collections
    for collection in config.get('collections', []):
        for item in collection.get('items', []):
            if item.get('repo_name') == repo_name and item.get('family') == 'embedding':
                threshold_high = item.get('similarity_threshold_high')
                threshold_low = item.get('similarity_threshold_low')
                return threshold_high, threshold_low

    return None, None


def main():
    parser = argparse.ArgumentParser(
        description='Get similarity thresholds for embedding models from configuration.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get thresholds for a model
  python get_similarity_thresholds.py ibm-granite/granite-embedding-30m-english

  # Get thresholds with custom config path
  python get_similarity_thresholds.py granite-embedding-30m-english \\
    --config resources/json/latest/hf_collection_mapping_gguf.json

  # Output format (stdout): threshold_high threshold_low
  # Example output: 0.6 0.5
        """
    )
    parser.add_argument('repo_id',
                        help='Repository ID (e.g., ibm-granite/granite-embedding-30m-english)')
    parser.add_argument('--config',
                        default='resources/json/latest/hf_collection_mapping_gguf.json',
                        help='Path to configuration file (default: resources/json/latest/hf_collection_mapping_gguf.json)')
    parser.add_argument('--default-high', type=float, default=0.6,
                        help='Default threshold for similar sentences if not found in config (default: 0.6)')
    parser.add_argument('--default-low', type=float, default=0.4,
                        help='Default threshold for dissimilar sentences if not found in config (default: 0.4)')
    parser.add_argument('--verbose', action='store_true',
                        help='Print verbose output to stderr')

    args = parser.parse_args()

    # Check if config file exists
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"[ERROR] Configuration file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    # Get thresholds
    threshold_high, threshold_low = get_similarity_thresholds(config_path, args.repo_id)

    # Use defaults if not found
    if threshold_high is None or threshold_low is None:
        if args.verbose:
            print(f"[WARNING] Thresholds not found for {args.repo_id}, using defaults", file=sys.stderr)
        threshold_high = args.default_high
        threshold_low = args.default_low

    if args.verbose:
        print(f"[INFO] Repository: {args.repo_id}", file=sys.stderr)
        print(f"[INFO] Similarity Threshold (High/Similar): {threshold_high}", file=sys.stderr)
        print(f"[INFO] Similarity Threshold (Low/Dissimilar): {threshold_low}", file=sys.stderr)

    # Output thresholds (space-separated for easy parsing in bash)
    print(f"{threshold_high} {threshold_low}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob