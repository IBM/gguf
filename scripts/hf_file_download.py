import sys
import requests
import argparse

from typing import List
from huggingface_hub import hf_hub_download
from huggingface_hub.utils import HfHubHTTPError

def download_model_files(models_dir:str="", repo_id:str="", files:List[str]=[]) -> str:
    print(f">>> models_dir: {models_dir}, repo_id: {repo_id}")
    local_dir = models_dir + "/" + repo_id
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
        print("Please provide a token")
        sys.exit(1)

    try:
        local_dir = models_dir + "/" + repo_id

        import datetime
        now = datetime.datetime.now()
        print(now.strftime("BEFORE: %Y-%m-%d %H:%M:%S"))
        download_dir = hf_hub_download(
            repo_id=repo_id,
            repo_type="model",
            filename=file_name,
            local_dir=local_dir,
            token=hf_token,
        )
        now = datetime.datetime.now()
        print(now.strftime("AFTER: %Y-%m-%d %H:%M:%S"))

    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_id: '{repo_id}', file_name: '{file_name}'")
        sys.exit(2)
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
        sys.exit(2)
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
        sys.exit(2)
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
        sys.exit(2)
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
        sys.exit(2)
    return download_dir

def test_empty_string(value:str):
        if not value:
            raise ValueError("Argument must not be an empty string")
        return value

if __name__ == "__main__":
    try:
        # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
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
        exit(se)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        exit(2)

    # Exit successfully
    sys.exit(0)