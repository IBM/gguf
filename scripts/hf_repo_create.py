import os
import sys
import requests

from huggingface_hub import create_repo, list_repo_files, RepoUrl
from huggingface_hub.utils import HfHubHTTPError

# retrieve secrets
# hf_token=os.environ['HF_TOKEN']

###########################################
# Repos
###########################################

def safe_create_repo_in_namespace(repo_name:str="", private:bool=True, hf_token:str="") -> RepoUrl:
    if repo_name == "":
        print("Please provide a repo_name")
        return False
    if hf_token == "":
        print("Please provide a token")
        return False        
    
    try:
        repo_url = create_repo(
            repo_name, 
            private=private, 
            exist_ok=True, 
            token=hf_token,
        )
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_name: '{repo_name}'")
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
    else: 
        return repo_url
    return None
 
 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len != 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_name:str> <private:bool> <hf_token:str>")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params. 
    fx_name = sys.argv[0]
    repo_name = sys.argv[1]   
    private = bool(sys.argv[2])
    hf_token = sys.argv[3]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: repo_name='{repo_name}', private='{private}', hf_token='{hf_token}'")     
    
    # invoke fx
    repo_url = safe_create_repo_in_namespace(repo_name=repo_name, private=private, hf_token=hf_token)    
    
    # Print output variables for this run
    print(f"repo_url: {repo_url}") 
    
    # Exit successfully
    sys.exit(0)      