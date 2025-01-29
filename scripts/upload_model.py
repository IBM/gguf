import os
import sys
import requests

from huggingface_hub import upload_file, CommitInfo
from huggingface_hub.utils import HfHubHTTPError

# retrieve secrets
# hf_token=os.environ['HF_TOKEN']

###########################################
# Files
###########################################

def safe_upload_file(repo_name:str="", model_file:str="", hf_token:str="") -> CommitInfo:
    if repo_name == "":
        print("Please provide a repo_name")
        return False
    if model_file == "":
        print("Please provide a model_file")
        return False    
    if hf_token == "":
        print("Please provide a token")
        return False        
    
    try:
        target_file_name = os.path.basename(model_file)
        commit_info = upload_file(
            path_or_fileobj=model_file,
            path_in_repo=target_file_name,
            repo_id=repo_name,
            repo_type="model",
            commit_message="Test upload GGUF file as model",
            commit_description="Test upload",
            token=hf_token,
        )
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_name: '{repo_name}', model_file: '{model_file}'")
        return False
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
    else: 
        return commit_info
    return None
 
 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len != 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_name:str> <model_file:str> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Test private repo.   
    fx_name = sys.argv[0]
    repo_name = sys.argv[1]
    model_file = sys.argv[2]   
    hf_token = sys.argv[3]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: repo_name='{repo_name}', model_file='{model_file}', hf_token='{hf_token}'")     
    
    # invoke fx
    commit_info = safe_upload_file(repo_name=repo_name, model_file=model_file, hf_token=hf_token)    
    
    # Print output variables
    print(f"commit_info: {commit_info}") 
    
    # Exit successfully
    sys.exit(0)      