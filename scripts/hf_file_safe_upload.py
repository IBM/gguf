import datetime
import os
import sys
import time

from huggingface_hub import upload_file, CommitInfo
from huggingface_hub.errors import HfHubHTTPError, RepositoryNotFoundError

###########################################
# Files
###########################################

def safe_upload_file(
    repo_id:str="",
    model_file:str="",
    hf_token:str="",
    commit_msg:str="",
    commit_desc:str="",
    workflow_ref="",
    run_id="",
) -> CommitInfo | None:
    if repo_id == "":
        print("Please provide a repo_id")
        return None
    if model_file == "":
        print("Please provide a model_file")
        return None
    if hf_token == "":
        print("Please provide a token")
        return None

    # Validate token format without exposing it
    token_length = len(hf_token)
    if token_length < 10:
        print(f"WARNING: Token seems too short (length: {token_length}). Expected HF token format.")
    else:
        print(f"Token received (length: {token_length} chars, starts with: {hf_token[:4]}...)")

    # Check if local file exists
    if not os.path.exists(model_file):
        print(f"[ERROR] Local file not found: {model_file}")
        return None

    file_size = os.path.getsize(model_file)
    print(f"File to upload: {model_file} (size: {file_size:,} bytes)")

    target_file_name = os.path.basename(model_file)

    # Note: commit_message MUST NOT be empty or None
    if commit_msg is None or commit_msg == "":
        # construct a default message...
        commit_msg = f"Uploading model: run_id: {run_id}, workflow_ref: {workflow_ref}"

    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            print(datetime.datetime.now().strftime("BEFORE: %Y-%m-%d %H:%M:%S"))
            if attempt > 0:
                print(f"Retry attempt {attempt + 1}/{max_retries}...")

            # Note: repo_type is always "model" for now
            commit_info = upload_file(
                path_or_fileobj=model_file,
                path_in_repo=target_file_name,
                repo_id=repo_id,
                repo_type="model",
                commit_message=commit_msg,
                commit_description=commit_desc,
                token=hf_token,
            )
            print(datetime.datetime.now().strftime("AFTER: %Y-%m-%d %H:%M:%S"))
            return commit_info

        except RepositoryNotFoundError as exc:
            # Repository doesn't exist — permanent error, don't retry
            print(f"[ERROR] Repository not found: '{repo_id}'")
            print(f"  Make sure the repository exists and you have write access to it.")
            print(f"  Error: {exc}")
            return None
        except HfHubHTTPError as exc:
            print(f"[ERROR] HfHubHTTPError uploading to repo_id: '{repo_id}', model_file: '{model_file}'")
            if hasattr(exc, 'server_message') and exc.server_message:
                print(f"  Server message: {exc.server_message}")
            if hasattr(exc, 'response') and exc.response:
                print(f"  Response status: {exc.response.status_code}")
                print(f"  Response text: {exc.response.text}")
            if attempt < max_retries - 1:
                print(f"  Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("  Max retries reached. Giving up.")
        except Exception as exc:
            print(f"[ERROR] Exception uploading to repo_id: '{repo_id}', model_file: '{model_file}'")
            print(f"  Error type: {type(exc).__name__}")
            print(f"  Error: {exc}")
            if attempt < max_retries - 1:
                print(f"  Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("  Max retries reached. Giving up.")

    return None


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 4:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_name:str> <model_file:str> <hf_token:str> <workflow_ref:str> <run_id:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)

    # Parse input arguments into named params.
    fx_name = sys.argv[0]
    repo_name = sys.argv[1]
    model_file = sys.argv[2]
    hf_token = sys.argv[3]
    workflow_ref = sys.argv[4] if arg_len > 4 else ""
    run_id = sys.argv[5] if arg_len > 5 else ""

    # Print input variables being used for this run
    print(f">> {fx_name}: repo_name='{repo_name}', model_file='{model_file}', workflow_ref='{workflow_ref}', run_id='{run_id}'")

    # invoke fx
    commit_info = safe_upload_file(repo_id=repo_name, model_file=model_file, hf_token=hf_token, workflow_ref=workflow_ref, run_id=run_id)

    # Print output variables
    if commit_info is None:
        sys.exit(1)

    # Exit successfully
    print(f"commit_info: {commit_info}")
    sys.exit(0)