import sys
import argparse
import time
import re
import datetime
from typing import List

from huggingface_hub import hf_hub_download, list_repo_files
from huggingface_hub.errors import HfHubHTTPError, RepositoryNotFoundError, RevisionNotFoundError, EntryNotFoundError


def detect_split_files(repo_id: str, base_pattern: str, hf_token: str) -> List[str]:
    """
    Detect all split files matching a base pattern in a repository.
    
    Args:
        repo_id: HuggingFace repository ID
        base_pattern: Base filename pattern (e.g., "granite-4.1-30b-bf16")
        hf_token: HuggingFace API token
        
    Returns:
        List of filenames that match the split pattern
    """
    try:
        all_files = list_repo_files(repo_id=repo_id, repo_type="model", token=hf_token)
        
        # Pattern to match split files: {base_pattern}-{part}-of-{total}.gguf
        # Example: granite-4.1-30b-bf16-00001-of-00005.gguf
        split_pattern = re.compile(rf"^{re.escape(base_pattern)}-\d{{5}}-of-\d{{5}}\.gguf$")
        
        split_files = [f for f in all_files if split_pattern.match(f)]
        split_files.sort()  # Ensure files are in order
        
        return split_files
    except Exception as exc:
        print(f"Error detecting split files: {exc}")
        return []


def download_split_files(
    models_dir: str,
    repo_id: str,
    base_pattern: str,
    hf_token: str,
    max_retries: int = 3,
    retry_delay: int = 5
) -> List[str]:
    """
    Download all split GGUF files matching a base pattern.
    
    Args:
        models_dir: Directory where files will be downloaded
        repo_id: HuggingFace repository ID
        base_pattern: Base filename pattern (e.g., "granite-4.1-30b-bf16")
        hf_token: HuggingFace API token
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        List of downloaded file paths
    """
    if not models_dir:
        print("ERROR: Please provide a models_dir")
        sys.exit(1)
    if not repo_id:
        print("ERROR: Please provide a repo_id")
        sys.exit(1)
    if not base_pattern:
        print("ERROR: Please provide a base_pattern")
        sys.exit(1)
    if not hf_token:
        print("ERROR: Please provide a token")
        sys.exit(1)

    # Validate token format without exposing it
    token_length = len(hf_token)
    if token_length < 10:
        print(f"WARNING: Token seems too short (length: {token_length}). Expected HF token format.")
    else:
        print(f"Token received (length: {token_length} chars, starts with: {hf_token[:4]}...)")

    local_dir = f"{models_dir}/{repo_id}"
    
    # Detect all split files
    print(f"Detecting split files for pattern: {base_pattern}")
    split_files = detect_split_files(repo_id, base_pattern, hf_token)
    
    if not split_files:
        print(f"ERROR: No split files found matching pattern: {base_pattern}")
        sys.exit(2)
    
    print(f"Found {len(split_files)} split files:")
    for f in split_files:
        print(f"  - {f}")
    
    downloaded_paths = []
    
    # Download each split file
    for file_name in split_files:
        print(f"\nDownloading: {file_name}")
        
        for attempt in range(max_retries):
            try:
                now = datetime.datetime.now()
                print(now.strftime("BEFORE: %Y-%m-%d %H:%M:%S"))
                
                if attempt > 0:
                    print(f"Retry attempt {attempt + 1}/{max_retries}...")

                download_path = hf_hub_download(
                    repo_id=repo_id,
                    repo_type="model",
                    filename=file_name,
                    local_dir=local_dir,
                    token=hf_token,
                    resume_download=True,
                )
                
                now = datetime.datetime.now()
                print(now.strftime("AFTER: %Y-%m-%d %H:%M:%S"))
                print(f"Successfully downloaded: {download_path}")
                downloaded_paths.append(download_path)
                break  # Success, move to next file

            except (RepositoryNotFoundError, EntryNotFoundError) as exc:
                # These are permanent errors, don't retry
                print(f"File not found error: {exc}")
                print(f"repo_id: '{repo_id}', file_name: '{file_name}'")
                sys.exit(2)
            except HfHubHTTPError as exc:
                print(f"HfHubHTTPError: {exc.server_message if hasattr(exc, 'server_message') else exc}")
                print(f"repo_id: '{repo_id}', file_name: '{file_name}'")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Giving up.")
                    sys.exit(2)
            except Exception as exc:
                print(f"Exception: {exc}")
                print(f"Exception type: {type(exc).__name__}")
                print(f"repo_id: '{repo_id}', file_name: '{file_name}'")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Giving up.")
                    sys.exit(2)
    
    print(f"\nSuccessfully downloaded {len(downloaded_paths)} split files")
    return downloaded_paths


def test_empty_string(value: str):
    if not value:
        raise ValueError("Argument must not be an empty string")
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download split GGUF files from HuggingFace",
        exit_on_error=False
    )
    
    try:
        for arg in sys.argv:
            print(arg)

        parser.add_argument(
            "models_dir",
            type=test_empty_string,
            help="The directory where the model files will be downloaded to."
        )
        parser.add_argument(
            "repo_id",
            type=test_empty_string,
            help="HF Hub repo ID (i.e., `repo_namespace/repo_name`) files will be downloaded from."
        )
        parser.add_argument(
            "base_pattern",
            type=test_empty_string,
            help="Base filename pattern for split files (e.g., 'granite-4.1-30b-bf16')"
        )
        parser.add_argument(
            "hf_token",
            help="Hugging Face Hub API access token."
        )
        parser.add_argument(
            "--debug",
            default=False,
            action="store_true",
            help="Enable debug output"
        )
        
        args = parser.parse_args()

        if args.debug:
            # Print input variables being used for this run
            print(f">> models_dir='{args.models_dir}', repo_id='{args.repo_id}', "
                  f"base_pattern='{args.base_pattern}', hf_token='{args.hf_token}'")

        # Invoke function
        downloaded_paths = download_split_files(
            models_dir=args.models_dir,
            repo_id=args.repo_id,
            base_pattern=args.base_pattern,
            hf_token=args.hf_token
        )

        # Print output variables
        print(f"\ndownload_dir: {downloaded_paths[0] if downloaded_paths else 'None'}")
        print(f"downloaded_files: {len(downloaded_paths)}")

    except SystemExit as se:
        print(f"Usage: {parser.format_usage()}")
        sys.exit(se.code if se.code is not None else 1)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        sys.exit(2)

    # Exit successfully
    sys.exit(0)

# Made with Bob
