import os
import sys
import requests

from typing import List
from huggingface_hub import hf_hub_download
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Files
###########################################

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
    if models_dir == "":
        print("Please provide a models_dir")
        return False    
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
        
        local_dir = models_dir + "/" + repo_id
   
        download_dir = hf_hub_download(
            repo_id=repo_id,
            filename=file_name,
            local_dir=local_dir,
            token=hf_token,   
        )  

    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_id: '{repo_id}', file_name: '{file_name}'")
        return None
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
    else: 
        return download_dir
    return None
 
 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 5:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <models_dir:str> <repo_id:str> <model_file:str> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    models_dir = sys.argv[1]    
    repo_id = sys.argv[2]
    file_name = sys.argv[3]   
    hf_token = sys.argv[4]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: models_dir='{models_dir}', repo_id='{repo_id}', file_name='{file_name}', hf_token='{hf_token}'")     
    
    # invoke fx
    download_dir = safe_download_file(models_dir=models_dir, repo_id=repo_id, file_name=file_name, hf_token=hf_token)
    
    # Print output variables
    print(f"download_dir: {download_dir}") 
    
    # Exit successfully
    sys.exit(0)      