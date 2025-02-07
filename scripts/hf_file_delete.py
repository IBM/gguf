import os
import sys
import requests

from huggingface_hub import delete_file
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Files
###########################################

def safe_delete_file(
    repo_id:str="", 
    file_name:str="", 
    hf_token:str="",    
) -> None:   
    if repo_id == "":
        print("Please provide a repo_id")
        return False
    if file_name == "":
        print("Please provide a file_name")
        return False    
    if hf_token == "":
        print("Please provide a token")
        return False        
    
    try:
        import datetime
        now = datetime.datetime.now()
        print(now.strftime("BEFORE: %Y-%m-%d %H:%M:%S"))
        download_dir = delete_file(
            repo_id=repo_id,
            path_in_repo=file_name,
            repo_type="model",
            filename=file_name,
            token=hf_token,   
        )  
        now = datetime.datetime.now()
        print(now.strftime("AFTER: %Y-%m-%d %H:%M:%S"))
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_id: '{repo_id}', file_name: '{file_name}'")
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
    return None
 
 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_id> <model_file> <hf_token>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
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