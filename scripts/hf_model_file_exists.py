import os
import sys
import time

from huggingface_hub import file_exists
from huggingface_hub.errors import HfHubHTTPError

###########################################
# Files
###########################################

# Transient HTTP status codes that warrant a retry.
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}

# Retry policy: (delay_seconds, ...) — one entry per retry attempt.
_RETRY_DELAYS = (5, 15, 30)


def model_file_exists(
    repo_id:str="",
    test_filename:str="",
    hf_token:str="",
) -> bool:
    if repo_id == "":
        print("Please provide a repo_id")
        return False
    if test_filename == "":
        print("Please provide a test_filename")
        return False
    if hf_token == "":
        print("Please provide a token")
        return False

    last_exc = None
    attempts = 1 + len(_RETRY_DELAYS)          # initial + retries

    for attempt in range(attempts):
        try:
            return file_exists(
                repo_id=repo_id,
                filename=test_filename,
                repo_type="model",
                token=hf_token,
            )

        except HfHubHTTPError as exc:
            status = exc.response.status_code if (hasattr(exc, 'response') and exc.response) else None
            if status in _RETRYABLE_STATUS and attempt < attempts - 1:
                delay = _RETRY_DELAYS[attempt]
                print(
                    f"HfHubHTTPError ({status}) checking file existence for repo_id: '{repo_id}', "
                    f"test_file_name: '{test_filename}' — retrying in {delay}s "
                    f"(attempt {attempt + 1}/{attempts})"
                )
                time.sleep(delay)
                last_exc = exc
                continue

            # Non-retryable error or final attempt — print details and return False.
            print(f"HfHubHTTPError checking file existence for repo_id: '{repo_id}', test_file_name: '{test_filename}'")
            print(f"  Error: {exc}")
            if hasattr(exc, 'server_message') and exc.server_message:
                print(f"  Server message: {exc.server_message}")
            if hasattr(exc, 'response') and exc.response:
                print(f"  Response status: {exc.response.status_code}")
                print(f"  Response text: {exc.response.text}")
            return False

        except Exception as exc:
            print(f"Exception checking file existence for repo_id: '{repo_id}', test_file_name: '{test_filename}'")
            print(f"  Error: {exc}")
            return False

    # Exhausted retries on a retryable error.
    if last_exc is not None:
        print(f"HfHubHTTPError checking file existence for repo_id: '{repo_id}', test_file_name: '{test_filename}'")
        print(f"  Error: {last_exc}")
        if hasattr(last_exc, 'response') and last_exc.response:
            print(f"  Response status: {last_exc.response.status_code}")
            print(f"  Response text: {last_exc.response.text}")
    return False


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 4:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_id:str> <file_name:str> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)

    # Parse input arguments into named params.
    fx_name = sys.argv[0]
    repo_id = sys.argv[1]
    test_filename = sys.argv[2]
    hf_token = sys.argv[3]

    # invoke fx
    exists = model_file_exists(repo_id=repo_id, test_filename=test_filename, hf_token=hf_token)

    if exists:
        print("True")
    else:
        print("False")

    # Exit successfully
    sys.exit(0)
