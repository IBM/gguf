import sys
import argparse
import time

from typing import List
from huggingface_hub import hf_hub_download
from huggingface_hub.errors import HfHubHTTPError, RepositoryNotFoundError, RevisionNotFoundError, EntryNotFoundError

def download_model_files(models_dir:str="", repo_id:str="", files:List[str]=[]) -> str:
    print(f">>> models_dir: {models_dir}, repo_id: {repo_id}")
    local_dir = models_dir + "/" + repo_id
    download_dir = ""
    # TODO: default to some subset of all files in model repo.
    #files = list_repo_files(repo_id=model_name, token=hf_token)
    for file_name in files:
        download_dir = hf_hub_download(
                repo_id=repo_id,
                filename=file_name,
                local_dir=local_dir,
            )
    return download_dir


def safe_download_file(
    models_dir:str="",
    repo_id:str="",
    file_name:str="",
    hf_token:str="",
) -> str:
    """
    Uses the Hugging Face Hub's `hf_hub_download` function to download a file from a HF repository.

    Args:
        models_dir (str): The directory where the model file will be downloaded to.
        repo_id (str): HF Hub repo. ID (i.e., `repo_namespace/repo_name`) file will be downloaded from.
        file_name (str): The model file name to download.
        hf_token (str): Hugging Face Hub API access token.

    Returns:
        None
    Exit codes:
        0: success
        >0: failure
    """
    if models_dir == "":
        print("Please provide a models_dir")
        sys.exit(1)
    if repo_id == "":
        print("Please provide a repo_id")
        sys.exit(1)
    if file_name == "":
        print("Please provide a file_name")
        sys.exit(1)
    if hf_token == "":
        print("ERROR: Please provide a token")
        sys.exit(1)

    # Validate token format without exposing it
    token_length = len(hf_token)
    if token_length < 10:
        print(f"WARNING: Token seems too short (length: {token_length}). Expected HF token format.")
    else:
        print(f"Token received (length: {token_length} chars, starts with: {hf_token[:4]}...)")

    local_dir = models_dir + "/" + repo_id
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            import datetime
            now = datetime.datetime.now()
            print(now.strftime("BEFORE: %Y-%m-%d %H:%M:%S"))
            if attempt > 0:
                print(f"Retry attempt {attempt + 1}/{max_retries}...")

            download_dir = hf_hub_download(
                repo_id=repo_id,
                repo_type="model",
                filename=file_name,
                local_dir=local_dir,
                token=hf_token,
                resume_download=True,
            )
            now = datetime.datetime.now()
            print(now.strftime("AFTER: %Y-%m-%d %H:%M:%S"))
            return download_dir

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

    # Should not reach here, but just in case
    print("Download failed after all retries")
    sys.exit(2)

def test_empty_string(value:str):
        if not value:
            raise ValueError("Argument must not be an empty string")
        return value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
    try:
        for arg in sys.argv:
            print(arg)

        # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
        parser.add_argument("models_dir", type=test_empty_string, help="The directory where the model file will be downloaded to.")
        parser.add_argument("repo_id", type=test_empty_string, help="HF Hub repo. ID (i.e., `repo_namespace/repo_name`) file will be downloaded from.")
        parser.add_argument("model_file", type=test_empty_string, help="The model file name to download")
        parser.add_argument('hf_token', help='Hugging Face Hub API access token.')
        parser.add_argument('--debug', default=False, action='store_false', help='Enable debug output')
        args = parser.parse_args()

        if(args.debug):
            # Print input variables being used for this run
            print(f">> models_dir='{args.models_dir}', repo_id='{args.repo_id}', model_file='{args.model_file}', hf_token='{args.hf_token}'")

        # invoke fx
        download_dir = safe_download_file(models_dir=args.models_dir, repo_id=args.repo_id, file_name=args.model_file, hf_token=args.hf_token)

        # Print output variables
        print(f"download_dir: {download_dir}")

    except SystemExit as se:
        print(f"Usage: {parser.format_usage()}")
        sys.exit(se.code if se.code is not None else 1)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        sys.exit(2)

    # Exit successfully
    sys.exit(0)