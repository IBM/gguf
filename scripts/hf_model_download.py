import os
import sys
from huggingface_hub import hf_hub_download, snapshot_download, list_repo_files
from typing import List

# Constants (defaults)
DEFAULT_MODEL_DIR = "models"
DEFAULT_REPO_ORG = "ibm-granite"


# TODO: minimize downloaded files to only those needed for conversion
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
    
    
def download_model_snapshot(models_dir:str="", repo_id:str="") -> str:
    print(f">>> models_dir='{models_dir}', repo_id='{repo_id}'")
    if models_dir == "":
        print("models_dir is empty")
        return    
    if repo_id == "":
        print("repo_id is empty")
        return
    local_dir = models_dir + "/" + repo_id
    print(f"local_dir: {local_dir}")
    download_dir = snapshot_download(
            repo_id=repo_id, 
            local_dir=local_dir,
        )  
    return download_dir 


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len != 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <models_dir> <repo_org> <repo_name>")
        # Exit with an error code
        sys.exit(1)
    
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    models_dir = sys.argv[1]
    repo_org = sys.argv[2]
    repo_name = sys.argv[3]
    repo_id = repo_org + "/" + repo_name
    
    # Print input variables being used for this run
    print(f">> {fx_name}: models_dir='{models_dir}', repo_org='{repo_org}', repo_name='{repo_name}'")
    
    # Note: this downloads everything... TODO: download only the necessary files.
    download_dir = download_model_snapshot(models_dir=models_dir, repo_id=repo_id)
    
    # Print output variables for this run
    print(f"download_dir: {download_dir}") 
    
    # Exit successfully
    sys.exit(0)
