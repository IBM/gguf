import os
import sys
import requests

from huggingface_hub import upload_file, CommitInfo
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Files
###########################################

def safe_upload_file(
    repo_id:str="", 
    model_file:str="", 
    hf_token:str="", 
    commit_msg:str=None, 
    commit_desc:str=None,
    workflow_ref="",
    run_id="",    
) -> CommitInfo:
    if repo_id == "":
        print("Please provide a repo_id")
        return False
    if model_file == "":
        print("Please provide a model_file")
        return False    
    if hf_token == "":
        print("Please provide a token")
        return False        
    
    try:
        target_file_name = os.path.basename(model_file)
        
        # Note: commit_message MUST NOT be empty or None
        if commit_msg is None or commit_msg == "":
            # construct a default message...
            commit_msg = f"Uploading model: run_id: {run_id}, workflow_ref: {workflow_ref}"
        
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
    except HfHubHTTPError as exc:
        print(f"[ERROR] HfHubHTTPError: {exc.server_message}, repo_name: '{repo_id}', model_file: '{model_file}'")
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
    if arg_len < 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_name:str> <model_file:str> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    repo_name = sys.argv[1]
    model_file = sys.argv[2]   
    hf_token = sys.argv[3]
    workflow_ref = sys.argv[4]
    run_id = sys.argv[5]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: repo_name='{repo_name}', model_file='{model_file}', hf_token='{hf_token}', workflow_ref='{workflow_ref}', run_id='{run_id}'")     
    
    # invoke fx
    commit_info = safe_upload_file(repo_id=repo_name, model_file=model_file, hf_token=hf_token, workflow_ref=workflow_ref, run_id=run_id)
    
    # Print output variables
    if commit_info is None:
        sys.exit(1)
    
    # Exit successfully
    print(f"commit_info: {commit_info}")  
    sys.exit(0)      