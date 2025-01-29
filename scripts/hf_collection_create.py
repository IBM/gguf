import os
import sys
import requests

from huggingface_hub import list_collections, create_collection, add_collection_item, Collection, CollectionItem
from huggingface_hub.utils import HfHubHTTPError

###########################################
# Collections
###########################################

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


def list_collection_attributes(collections:Collection=None, list_items:bool=False) -> None:
    if collections is None:
        print("Please provide a valid collections iterator")
        return
    for collection in collections:
        print(f"---")
        print(f"title: `{collection.title}`, private: {collection.private}, description: `{collection.description}`, slug: `{collection.slug}`")
        if list_items:
            list_collection_items(collection=collection) 


def list_collection_items(collection:Collection=None) -> None:
    if collection is None:
        print("Please provide a valid collection")
        return
    num_items = len(collection.items)
    if num_items > 0:
        for item in collection.items:
            print(f"item_id: '{item.item_id}' ({item.item_type}), position: '{item.position}', item_object_id: '{item.item_object_id}'")        
            if item.note is not None:
                print(f"\t| {item.note}")
    else:
        print(f"(no items)")


def safe_create_collection_in_namespace(hf_owner:str="", title:str="", description:str="", private:bool=True, hf_token:str="") -> Collection:
    if hf_owner == "":
        print("Please provide an owner (username or organization) for the collection")
        return False
    if title == "":
        print("Please provide a title for the collection")
        return False
    if description == "":
        print("Please provide a description for the collection")
        return False   
    if hf_token == "":
        print("Please provide a token")
        return False           
    
    try:
        # We want to test if the collection already exists before creating it (and not rely on exceptions)
        collection = get_collection_by_title(hf_owner=hf_owner, title=title, hf_token=hf_token)
        if collection is None:
            collection = create_collection(
                title=title,
                description=description,
                private=private,
                token=hf_token,
        )
        else:
            print(f"Collection '{title}' already exists in namespace '{hf_owner}'")
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


def add_update_collection_model(collection_slug:str="", repo_name:str="", note:str="", hf_token:str="") -> Collection:
    if collection_slug == "":
        print("Please provide a slug (ID) for the collection.")
        return False
    if repo_name == "":
        print("Please provide a repo_name for the collection.")
        return False   
    if note == "":
        print("Please provide a note for the collection.")
        return False     
    if hf_token == "":
        print("Please provide a token")
        return False      
    
    # If an item already exists in a collection (same item_id/item_type pair), 
    # an HTTP 409 error will be raised. 
    # You can choose to ignore this error by setting exists_ok=True    
    try:
        collection = add_collection_item(
            collection_slug,
            item_id=repo_name,
            item_type="model",
            note=note,
            exists_ok=True,
            token=hf_token,
        )
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
   
   if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 6:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <repo_owner:str> <title:str> <description:str> <private:bool> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    repo_owner = sys.argv[1]
    title = sys.argv[2]  
    description = sys.argv[3]  
    private = sys.argv[4] 
    hf_token = sys.argv[5]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: owner='{repo_owner}', title='{title}', desc='{description}', private='{private}', hf_token='{hf_token}'")     
    
    # invoke fx
    collection = safe_create_collection_in_namespace(hf_owner=repo_owner, title=title, description=description, hf_token=hf_token)            
       
       
    import json   
    with open("resources/json/hf_collection_mapping.json", "r") as file:
        json_data = json.load(file)
        formatted_json = json.dumps(json_data, indent=4)
        print(formatted_json)

    collections = json_data["collections"]
    # print(f"collections='{collections}' ({type(collection)})")
    for collection in collections:
        c = json.dumps(collection, indent=4)
        print(f"collection='{c}'")
       
    existing_collection = get_collection_by_title(hf_owner=repo_owner, title=title, hf_token=hf_token)
    if existing_collection is not None:
        list_collection_items(existing_collection) 
    else:
        print(f"Collection '{title}' not found in namespace '{repo_owner}'")
        
    add_update_collection_model(
        collection_slug=collection.slug, 
        repo_name="mrutkows/granite-3.0-2b-instruct-GGUF", 
        note="test note",
        hf_token=hf_token)
    
    if existing_collection is not None:
        list_collection_items(existing_collection) 
    else:
        print(f"Collection '{title}' not found in namespace '{repo_owner}'")
         
    # Print output variables
    print(f"collection: {collection}") 
    
    # Exit successfully
    sys.exit(0) 
    