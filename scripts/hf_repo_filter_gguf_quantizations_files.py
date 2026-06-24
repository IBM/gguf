import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

from huggingface_hub import list_repo_files
from huggingface_hub.errors import HfHubHTTPError


SPLIT_PATTERN = re.compile(r"^(.+)-(\d{5})-of-(\d{5})\.gguf$")


def parse_exclude_quantizations(value: Optional[str]) -> List[str]:
    if not value:
        return []
    tokens = [t.strip().lower() for t in value.split(",")]
    tokens = [t for t in tokens if t]
    if tokens:
        print(f"[INFO] Excluding quantizations: {', '.join(tokens)}", file=sys.stderr)
    return tokens


def filename_matches_excluded_quantization(filename: str, excluded: List[str]) -> Optional[str]:
    lowered = filename.lower()
    for token in excluded:
        if token in lowered:
            return token
    return None


def list_gguf_files(repo_id: str, hf_token: str) -> List[str]:
    try:
        all_files = list_repo_files(repo_id=repo_id, repo_type="model", token=hf_token)
    except HfHubHTTPError as exc:
        print(f"ERROR: HfHubHTTPError listing '{repo_id}': {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"ERROR: failed to list files in '{repo_id}': {exc}", file=sys.stderr)
        sys.exit(2)
    return [f for f in all_files if f.endswith(".gguf")]


def quantization_from_base(base: str, model_name: str, source_filename: str) -> Optional[str]:
    if not base.startswith(model_name):
        print(
            f"[WARNING] '{source_filename}' does not start with model name '{model_name}', skipping",
            file=sys.stderr,
        )
        return None
    suffix = base[len(model_name):]
    if suffix.startswith("-"):
        suffix = suffix[1:]
    if not suffix:
        print(
            f"[WARNING] Could not extract quantization from '{source_filename}', skipping",
            file=sys.stderr,
        )
        return None
    return suffix


def served_model_name(target_repo_owner: str, model_name: str, quantization: str) -> str:
    return f"{target_repo_owner}/{model_name}-{quantization.replace('_', '')}-gguf"


def build_quantizations(
    files: List[str],
    model_name: str,
    target_repo_owner: str,
    excluded_quantizations: List[str],
    skip_split: bool,
) -> List[Dict]:
    quantizations: List[Dict] = []
    split_groups: Dict[str, Dict] = {}
    excluded_count = 0
    skipped_split_count = 0

    for gguf_file in files:
        matched_token = filename_matches_excluded_quantization(gguf_file, excluded_quantizations)
        if matched_token:
            print(
                f"[INFO] Excluding file (quantization '{matched_token}' in name): {gguf_file}",
                file=sys.stderr,
            )
            excluded_count += 1
            continue

        split_match = SPLIT_PATTERN.match(gguf_file)
        if split_match:
            base_pattern = split_match.group(1)
            total_parts = split_match.group(3)

            if skip_split:
                if base_pattern not in split_groups:
                    split_groups[base_pattern] = {"skipped": True}
                    skipped_split_count += 1
                    print(f"[INFO] Skipping split GGUF group: {base_pattern}", file=sys.stderr)
                continue

            if base_pattern in split_groups:
                continue
            split_groups[base_pattern] = {"total_parts": total_parts, "first_file": gguf_file}

            quantization = quantization_from_base(base_pattern, model_name, gguf_file)
            if not quantization:
                continue

            print(
                f"[INFO] Detected split GGUF group: {base_pattern} ({total_parts} parts)",
                file=sys.stderr,
            )
            quantizations.append({
                "quantization": quantization,
                "served_model_name": served_model_name(target_repo_owner, model_name, quantization),
                "filename": gguf_file,
                "is_split": True,
                "split_base_pattern": base_pattern,
                "total_parts": int(total_parts),
            })
            continue

        base_name = gguf_file[:-len(".gguf")]
        quantization = quantization_from_base(base_name, model_name, gguf_file)
        if not quantization:
            continue

        quantizations.append({
            "quantization": quantization,
            "served_model_name": served_model_name(target_repo_owner, model_name, quantization),
            "filename": gguf_file,
            "is_split": False,
        })

    print(f"[INFO] Total GGUF files scanned: {len(files)}", file=sys.stderr)
    print(f"[INFO] Files excluded by quantization list: {excluded_count}", file=sys.stderr)
    print(f"[INFO] Split GGUF groups skipped: {skipped_split_count}", file=sys.stderr)
    print(f"[INFO] Quantizations to process: {len(quantizations)}", file=sys.stderr)
    return quantizations


def test_empty_string(value: str) -> str:
    if not value:
        raise ValueError("Argument must not be an empty string")
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "List GGUF quantizations in a HuggingFace repo and write a JSON array to OUTPUT_FILE. "
            "Each entry: {quantization, served_model_name, filename, is_split, [split_base_pattern, total_parts]}. "
            "All logs go to stderr."
        ),
        exit_on_error=False,
    )

    try:
        parser.add_argument("repo_id", type=test_empty_string, help="HF repo ID (e.g. 'ibm-granite/granite-4.1-3b-GGUF').")
        parser.add_argument("model_name", type=test_empty_string, help="Model name prefix used in filenames (e.g. 'granite-4.1-3b').")
        parser.add_argument("hf_token", help="Hugging Face Hub API access token.")
        parser.add_argument("output_file", type=test_empty_string, help="Path to write the quantization JSON array to.")
        parser.add_argument("--target-repo-owner", default="ibm-granite", help="Owner used to build served_model_name. Default: ibm-granite.")
        parser.add_argument(
            "--exclude-quantizations",
            default="",
            help=(
                "Comma-separated list of quantization names to exclude (case-insensitive substring match against filename). "
                "Example: 'Q4_K_M,Q5_K_S' skips any file whose name contains 'Q4_K_M' or 'Q5_K_S'."
            ),
        )
        parser.add_argument("--skip-split", default=False, action="store_true", help="Skip split (multi-shard) GGUF files entirely.")
        parser.add_argument("--debug", default=False, action="store_true", help="Enable debug output on stderr.")

        args = parser.parse_args()

        if args.debug:
            print(
                f">> repo_id='{args.repo_id}', model_name='{args.model_name}', "
                f"output_file='{args.output_file}', target_repo_owner='{args.target_repo_owner}', "
                f"exclude_quantizations='{args.exclude_quantizations}', skip_split={args.skip_split}",
                file=sys.stderr,
            )

        token_length = len(args.hf_token or "")
        if token_length < 10:
            print(
                f"WARNING: Token seems too short (length: {token_length}). Expected HF token format.",
                file=sys.stderr,
            )

        gguf_files = list_gguf_files(args.repo_id, args.hf_token)
        excluded_quantizations = parse_exclude_quantizations(args.exclude_quantizations)
        quantizations = build_quantizations(
            files=gguf_files,
            model_name=args.model_name,
            target_repo_owner=args.target_repo_owner,
            excluded_quantizations=excluded_quantizations,
            skip_split=args.skip_split,
        )

        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(quantizations))

        print(
            f"Wrote {len(quantizations)} quantization entr{'y' if len(quantizations) == 1 else 'ies'} to {output_path}",
            file=sys.stderr,
        )
        for entry in quantizations:
            print(f"  - {entry['filename']} (is_split={entry['is_split']})", file=sys.stderr)

    except SystemExit as se:
        code = se.code if se.code is not None else 1
        if code not in (0, 2):
            print(f"Usage: {parser.format_usage()}", file=sys.stderr)
        sys.exit(code)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print(f"Usage: {parser.format_usage()}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)
