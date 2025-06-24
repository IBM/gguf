import os
import sys
import requests

from huggingface_hub import file_exists
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Files
###########################################

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

    try:
        return file_exists(
            repo_id=repo_id,
            filename=test_filename,
            repo_type="model",
            token=hf_token,
        )

    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_id: '{repo_id}', test_file_name: '{test_filename}'")
        return False
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
    except Exception as exc:
        print(f"Exception: {exc}")
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

    # Print input variables being used for this run
    # print(f">> {fx_name}: repo_id='{repo_id}', test_filename='{test_filename}', hf_token='{hf_token}'")

    # invoke fx
    exists = model_file_exists(repo_id=repo_id, test_filename=test_filename, hf_token=hf_token)

    # Print output variables
    # print(f"{fx_name}: returns: {exists}")
    if exists:
        print("True")
    else:
        print("False")

    # Exit successfully
    sys.exit(0)