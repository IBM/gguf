import os
import sys
import requests

from huggingface_hub import delete_file
from huggingface_hub.utils import HfHubHTTPError



def safe_delete_file(
    repo_id:str="", 
    file_name:str="", 
    hf_token:str="",    
) -> None:   
    """
    Uses the Hugging Face Hub's `delete_file` function to delete a file from a HF repository.

    Args:
        repo_id (str): HF Hub repo. ID (i.e., `repo_namespace/repo_name`).
        file_name (str): The file name to delete.
        hf_token (str): Hugging Face Hub API access token.

    Returns:
        None
    Exit codes:
        0: success
        >0: failure
    """
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
        delete_file(
            repo_id=repo_id,
            path_in_repo=file_name,
            repo_type="model",
            token=hf_token,   
        )  
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
    except Exception as exc:
        print(f"Other Exception: {exc}")
        sys.exit(2)           
    return None
 
 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_id> <model_file> <hf_token>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]   
    repo_id = sys.argv[1]
    file_name = sys.argv[2]   
    hf_token = sys.argv[3]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: repo_id='{repo_id}', file_name='{file_name}', hf_token='{hf_token}'")     
    
    # invoke fx
    safe_delete_file(repo_id=repo_id, file_name=file_name, hf_token=hf_token)

    # Exit successfully
    sys.exit(0)      