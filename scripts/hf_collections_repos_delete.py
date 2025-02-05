import os
import sys
import requests

from huggingface_hub import list_collections, delete_collection, Collection
from huggingface_hub import delete_repo
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Collections
###########################################

def safe_delete_repo(repo_id:str="", repo_type:str="model", hf_token:str="") -> None:
    if repo_id == "":
        print("Please provide a repo_id")
        return None
    if hf_token == "":
        print("Please provide a token")
        return None        
    
    try:
        delete_repo(
            repo_id, 
            repo_type=repo_type, 
            token=hf_token,
            missing_ok=True,
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
    return None


def get_collections_in_namespace(hf_owner:str="", hf_token:str="") -> None:
    if hf_owner == "":
        print("Please provide an owner (username or organization) for the collection")
        return False    
    if hf_token == "":
        print("Please provide a token")
        return False  
    
    collections = list_collections(owner=hf_owner, token=hf_token)
    return collections


def get_collection_by_title(hf_owner:str="", title:str="", hf_token:str="") -> Collection:
    if hf_owner == "":
        print("Please provide an owner (username or organization) for the collection")
        return False
    if title == "":
        print("Please provide a title for the new collection")
        return False      
    if hf_token == "":
        print("Please provide a token")
        return False          
    
    collections = get_collections_in_namespace(hf_owner=hf_owner, hf_token=hf_token)
    for c in collections:
        if c.title == title:
            return c
    return None


def safe_delete_collection_in_namespace(hf_owner:str="", title:str="", hf_token:str="") -> Collection:
    if hf_owner == "":
        print("Please provide an owner (username or organization) for the collection")
        return False 
    if title == "":
        print("Please provide a title for the collection")
        return False     
    if hf_token == "":
        print("Please provide a token")
        return False           
    
    try:
        # We want to test if the collection already exists before creating it (and not rely on exceptions)
        collection = get_collection_by_title(hf_owner=hf_owner, title=title, hf_token=hf_token)
        print(f"[INFO] Deleting collection '{title}' in namespace '{hf_owner}'...")
        if collection is not None:
            collection = delete_collection(
                collection.slug,
                missing_ok = True,
                token=hf_token,
        )
        else:
            print(f"[WARNING] Collection '{title}' not found in namespace '{hf_owner}'")
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, collection.title: '{title}'")
    except requests.exceptions.HTTPError as exc:
        print(f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print(f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print(f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"RequestException: {exc}")
    else: 
        return collection
    return None


if __name__ == "__main__":       
    arg_len = len(sys.argv)
    if arg_len < 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <target_owner:str> <collection_config:str> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    target_owner = sys.argv[1]  
    # TODO: "private should default to True (confirmed by "pre" tags); 
    # if workflow was started with a "release" tag, then change to False
    collection_config = sys.argv[2]
    hf_token = sys.argv[3]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: owner='{target_owner}', config='{collection_config}', hf_token='{hf_token}'")     
    
    # invoke fx
    import json   
    with open(collection_config, "r") as file:
        json_data = json.load(file)
        formatted_json = json.dumps(json_data, indent=4)
        print(formatted_json)

    collections_defn = json_data["collections"]
    for collection_defn in collections_defn:
        # formatted_defn = json.dumps(collection_defn, indent=4)
        # print(f"collection ({type(collection_defn)})='{formatted_defn}'")
        collection_title = collection_defn["title"]
        collection_desc = collection_defn["description"]
        collection_items = collection_defn["items"]
        print(f"title='{collection_title}', description='{collection_desc}'")
        print(f"items='{collection_items}")
    
        # upload all models associated with the collection
        for item_defn in collection_items:
            print(f"item_defn: '{item_defn}'")
            item_type = item_defn["type"]
            repo_id = item_defn["repo_id"]             
                                
            safe_delete_repo( 
                repo_id=repo_id, 
                repo_type=item_type,
                hf_token=hf_token) 
    
    # Exit successfully
    sys.exit(0) 
    