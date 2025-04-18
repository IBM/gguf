import os
import sys
import requests

from huggingface_hub import create_repo, RepoUrl
from huggingface_hub.utils import HfHubHTTPError

# retrieve secrets
# hf_token=os.environ['HF_TOKEN']

###########################################
# Repos
###########################################

def safe_create_repo_in_namespace(repo_id:str="", private:bool=True, hf_token:str=None) -> RepoUrl:
    if repo_id == "":
        print("Please provide a repo_id")
        return None
    if hf_token == "":
        print("Please provide a token")
        return None        
    
    try:
        #print(f"[DEBUG] repo_id='{repo_id}")        
        repo_url = create_repo(
            repo_id, 
            private=private, 
            exist_ok=True, 
            token=hf_token,
        )
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_id: '{repo_id}'")
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
        print(f"Usage: python {script_name} <repo_id:str> <private:bool> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params. 
    fx_name = sys.argv[0]
    repo_id = sys.argv[1]   
    private = bool(sys.argv[2])
    hf_token = sys.argv[3]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: repo_id='{repo_id}', private='{private}' ({type(private)}), hf_token='{hf_token}'")     
    
    # private needs to be a boolean
    if type(private) is str:
        print(f"[WARNING] private='{private}' is a string. Converting to boolean...") 
        if private.lower() == "true":
            private = True
        else:
            private = False            
    
    # invoke fx
    repo_url = safe_create_repo_in_namespace(repo_id=repo_id, private=private, hf_token=hf_token)    
    
    # Print output variables for this run
    print(f"[INFO] Created repository. repo_url: {repo_url}") 
    
    # Exit successfully
    sys.exit(0)      