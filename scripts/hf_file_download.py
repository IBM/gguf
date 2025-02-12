import os
import sys
import requests

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
        file_name (str): The file name to download.
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

 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 5:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <models_dir> <repo_id> <model_file> <hf_token>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
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