import sys
import argparse
import re
from pathlib import Path
from typing import List

from huggingface_hub import list_repo_files


def detect_split_files(repo_id: str, base_pattern: str, hf_token: str) -> List[str]:
    """
    Return the sorted list of split-shard filenames in `repo_id` that match
    `{base_pattern}-NNNNN-of-NNNNN.gguf`.
    """
    try:
        all_files = list_repo_files(repo_id=repo_id, repo_type="model", token=hf_token)
        split_pattern = re.compile(rf"^{re.escape(base_pattern)}-\d{{5}}-of-\d{{5}}\.gguf$")
        split_files = [f for f in all_files if split_pattern.match(f)]
        split_files.sort()
        return split_files
    except Exception as exc:
        print(f"Error detecting split files: {exc}", file=sys.stderr)
        return []


def test_empty_string(value: str):
    if not value:
        raise ValueError("Argument must not be an empty string")
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Write the sorted list of split GGUF shard filenames in a "
                    "HuggingFace repo to OUTPUT_FILE (one filename per line). "
                    "All logs go to stderr.",
        exit_on_error=False,
    )

    try:
        parser.add_argument(
            "repo_id",
            type=test_empty_string,
            help="HF Hub repo ID (e.g., `repo_namespace/repo_name`).",
        )
        parser.add_argument(
            "base_pattern",
            type=test_empty_string,
            help="Base filename pattern for split files (e.g., 'granite-4.1-30b-bf16').",
        )
        parser.add_argument(
            "hf_token",
            help="Hugging Face Hub API access token.",
        )
        parser.add_argument(
            "output_file",
            type=test_empty_string,
            help="Path to write the shard filenames to (one per line).",
        )
        parser.add_argument(
            "--debug",
            default=False,
            action="store_true",
            help="Enable debug output on stderr.",
        )

        args = parser.parse_args()

        if args.debug:
            print(
                f">> repo_id='{args.repo_id}', base_pattern='{args.base_pattern}', "
                f"output_file='{args.output_file}'",
                file=sys.stderr,
            )

        token_length = len(args.hf_token or "")
        if token_length < 10:
            print(
                f"WARNING: Token seems too short (length: {token_length}). Expected HF token format.",
                file=sys.stderr,
            )

        print(f"Detecting split files for pattern: {args.base_pattern}", file=sys.stderr)
        shards = detect_split_files(args.repo_id, args.base_pattern, args.hf_token)

        if not shards:
            print(
                f"ERROR: No split files found matching pattern: {args.base_pattern}",
                file=sys.stderr,
            )
            sys.exit(2)

        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(shards) + "\n")

        print(
            f"Wrote {len(shards)} shard filename(s) to {output_path}",
            file=sys.stderr,
        )
        for shard in shards:
            print(f"  - {shard}", file=sys.stderr)

    except SystemExit as se:
        if se.code not in (0, 2):
            print(f"Usage: {parser.format_usage()}", file=sys.stderr)
        sys.exit(se.code if se.code is not None else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Usage: {parser.format_usage()}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)
