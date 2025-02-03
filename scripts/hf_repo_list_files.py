import os
import sys
import requests

from typing import List
from huggingface_hub import list_repo_files
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Files
###########################################

def list_model_files(
    repo_id:str="", 
    test_filename:str="", 
    hf_token:str="",   
) -> List[str]:
    if repo_id == "":
        print("Please provide a repo_id")
        return False   
    if hf_token == "":
        print("Please provide a token")
        return False        
    
    try:
        return list_repo_files(
            repo_id=repo_id,
            repo_type="model",
            token=hf_token,
        )     
        # print(f"file_list: {file_list}")
        # for filename in file_list:
        #     if filename==test_filename:
        #         print("File exists")
        #         return True
        # else:
        #     print("File does not exist")
        #     return False
        
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, repo_id: '{repo_id}'")
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
    return None
 
 
if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 3:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_id:str> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    repo_id = sys.argv[1]  
    hf_token = sys.argv[2]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: repo_id='{repo_id}', hf_token='{hf_token}'")     
    
    # invoke fx
    file_list = list_model_files(repo_id=repo_id, hf_token=hf_token)
    
    # Print output variables
    print(f"file_list: {file_list}") 
    
    # Exit successfully
    sys.exit(0)      