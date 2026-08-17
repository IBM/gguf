import sys
import argparse
import time
import os

from typing import Optional
from huggingface_hub import HfApi, upload_file
from huggingface_hub.errors import HfHubHTTPError, RepositoryNotFoundError

def safe_upload_file(
    local_file_path: str = "",
    repo_id: str = "",
    path_in_repo: Optional[str] = None,
    hf_token: str = "",
    repo_type: str = "model",
    commit_message: Optional[str] = None,
) -> str:
    """
    Uses the Hugging Face Hub's `upload_file` function to upload a file to a HF repository.

    Args:
        local_file_path (str): The local path to the file to upload.
        repo_id (str): HF Hub repo. ID (i.e., `repo_namespace/repo_name`) file will be uploaded to.
        path_in_repo (str): Optional. The path where the file will be stored in the repository.
                           If not provided, uses the basename of local_file_path.
        hf_token (str): Hugging Face Hub API access token.
        repo_type (str): Type of repository (default: "model"). Can be "model", "dataset", or "space".
        commit_message (str): Optional commit message for the upload.

    Returns:
        str: The URL of the uploaded file.
    Exit codes:
        0: success
        >0: failure
    """
    if local_file_path == "":
        print("Please provide a local_file_path")
        sys.exit(1)
    if repo_id == "":
        print("Please provide a repo_id")
        sys.exit(1)
    if hf_token == "":
        print("ERROR: Please provide a token")
        sys.exit(1)

    # If path_in_repo not provided, use the basename of the local file
    if path_in_repo is None or path_in_repo == "":
        path_in_repo = os.path.basename(local_file_path)
        print(f"Using filename from local path: {path_in_repo}")

    # Validate token format without exposing it
    token_length = len(hf_token)
    if token_length < 10:
        print(f"WARNING: Token seems too short (length: {token_length}). Expected HF token format.")
    else:
        print(f"Token received (length: {token_length} chars, starts with: {hf_token[:4]}...)")

    # Check if local file exists
    if not os.path.exists(local_file_path):
        print(f"ERROR: Local file not found: {local_file_path}")
        sys.exit(1)

    file_size = os.path.getsize(local_file_path)
    print(f"File to upload: {local_file_path} (size: {file_size:,} bytes)")

    max_retries = 3
    retry_delay = 5  # seconds

    # Set default commit message if not provided
    if commit_message is None:
        commit_message = f"Upload {os.path.basename(local_file_path)}"

    for attempt in range(max_retries):
        try:
            import datetime
            now = datetime.datetime.now()
            print(now.strftime("BEFORE: %Y-%m-%d %H:%M:%S"))
            if attempt > 0:
                print(f"Retry attempt {attempt + 1}/{max_retries}...")

            upload_url = upload_file(
                path_or_fileobj=local_file_path,
                path_in_repo=path_in_repo,
                repo_id=repo_id,
                repo_type=repo_type,
                token=hf_token,
                commit_message=commit_message,
            )
            now = datetime.datetime.now()
            print(now.strftime("AFTER: %Y-%m-%d %H:%M:%S"))
            return upload_url

        except RepositoryNotFoundError as exc:
            # Repository doesn't exist - permanent error, don't retry
            print(f"Repository not found error: {exc}")
            print(f"repo_id: '{repo_id}'")
            print(f"Make sure the repository exists and you have write access to it.")
            sys.exit(2)
        except HfHubHTTPError as exc:
            print(f"HfHubHTTPError: {exc.server_message if hasattr(exc, 'server_message') else exc}")
            print(f"repo_id: '{repo_id}', path_in_repo: '{path_in_repo}'")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Giving up.")
                sys.exit(2)
        except Exception as exc:
            print(f"Exception: {exc}")
            print(f"Exception type: {type(exc).__name__}")
            print(f"repo_id: '{repo_id}', path_in_repo: '{path_in_repo}'")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Giving up.")
                sys.exit(2)

    # Should not reach here, but just in case
    print("Upload failed after all retries")
    sys.exit(2)

def test_empty_string(value: str):
    if not value:
        raise ValueError("Argument must not be an empty string")
    return value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
    try:
        for arg in sys.argv:
            print(arg)

        parser.add_argument("local_file_path", type=test_empty_string, help="The local path to the file to upload.")
        parser.add_argument("repo_id", type=test_empty_string, help="HF Hub repo. ID (i.e., `repo_namespace/repo_name`) file will be uploaded to.")
        parser.add_argument('hf_token', help='Hugging Face Hub API access token.')
        parser.add_argument('--path-in-repo', default=None, help='Optional. The path where the file will be stored in the repository. Defaults to the basename of local_file_path.')
        parser.add_argument('--repo-type', default='model', choices=['model', 'dataset', 'space'], help='Type of repository (default: model)')
        parser.add_argument('--commit-message', default=None, help='Optional commit message for the upload')
        parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        if args.debug:
            # Print input variables being used for this run
            print(f">> local_file_path='{args.local_file_path}', repo_id='{args.repo_id}', path_in_repo='{args.path_in_repo}', repo_type='{args.repo_type}'")

        # invoke fx
        upload_url = safe_upload_file(
            local_file_path=args.local_file_path,
            repo_id=args.repo_id,
            path_in_repo=args.path_in_repo,
            hf_token=args.hf_token,
            repo_type=args.repo_type,
            commit_message=args.commit_message,
        )

        # Print output variables
        print(f"Upload successful!")
        print(f"File URL: {upload_url}")

    except SystemExit as se:
        print(f"Usage: {parser.format_usage()}")
        sys.exit(se.code if se.code is not None else 1)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        sys.exit(2)

    # Exit successfully
    sys.exit(0)
