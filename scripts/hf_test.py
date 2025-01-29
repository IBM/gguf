import os
import sys
import requests

from huggingface_hub import list_collections, create_collection, add_collection_item, Collection, CollectionItem
from huggingface_hub import create_repo, list_repo_files, RepoUrl
from huggingface_hub import upload_file, CommitInfo
from huggingface_hub.utils import HfHubHTTPError

# retrieve secrets
hf_token=os.environ['HF_TOKEN']

###########################################
# Repos
###########################################

def safe_create_repo_in_namespace(repo_name:str="", private:bool=True, hf_token:str=hf_token) -> RepoUrl:
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

###########################################
# Files
###########################################

def safe_upload_file(repo_name:str="", model_file:str="", hf_token:str=hf_token) -> CommitInfo:
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
        commit_info = upload_file(
            path_or_fileobj=model_file,
            path_in_repo="test.gguf",
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

###########################################
# Collections
###########################################

def get_collections_in_namespace(hf_owner:str="", hf_token:str=hf_token) -> None:
    collections = list_collections(owner=hf_owner, token=hf_token)
    return collections


def get_collection_by_title(hf_owner:str="", title:str="", hf_token:str=hf_token) -> Collection:
    if hf_owner == "":
        print("Please provide an owner (username or organization) for the collection")
        return False
    if title == "":
        print("Please provide a title for the new collection")
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


def safe_create_collection_in_namespace(hf_owner:str="", title:str="", description:str="", private:bool=True, hf_token:str=hf_token) -> Collection:
    if hf_owner == "":
        print("Please provide an owner (username or organization) for the collection")
        return False
    if title == "":
        print("Please provide a title for the collection")
        return False
    if description == "":
        print("Please provide a description for the collection")
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


def add_update_collection_model(collection_slug:str="", repo_name:str="", note:str="", hf_token:str=hf_token) -> Collection:
    if collection_slug == "":
        print("Please provide a slug (ID) for the collection.")
        return False
    if repo_name == "":
        print("Please provide a repo_name for the model repo.")
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
    # Test private repo.
    collections = get_collections_in_namespace(hf_owner="mrutkows", hf_token=hf_token)  
    list_collection_attributes(collections=collections, list_items=True)    
    existing_collection = get_collection_by_title(hf_owner="mrutkows", title="Granite 3.2.0", hf_token=hf_token)
    if existing_collection is not None:
        list_collection_items(existing_collection) 
     
    # Test ibm-granite
    collections = get_collections_in_namespace(hf_owner="ibm-granite", hf_token=hf_token) 
    list_collection_attributes(collections=collections, list_items=True)
    existing_collection = get_collection_by_title(hf_owner="ibm-granite", title="Granite 3.1 Language Models", hf_token=hf_token)
    if existing_collection is not None:
        list_collection_items(existing_collection)     

    # Test private repo.         
    collection_title = "Granite 3.2.0"
    collection_note = "Test Granite collection"
    repo_name = "mrutkows/test-q2-k-gguf"    
    repo_owner = "mrutkows" 
    model_file = "test/repos/repo1/model1/test.gguf.zip"
    
    repo_url = safe_create_repo_in_namespace(repo_name=repo_name, hf_token=hf_token)
    commit_info = safe_upload_file(repo_name, model_file, hf_token=hf_token) 
    
    collection = safe_create_collection_in_namespace(hf_owner=repo_owner, title=collection_title, description="IBM Granite 3.2.0", hf_token=hf_token)            
    
    if collection is not None:
        list_collection_items(collection)  
        add_update_collection_model(
            collection_slug=collection.slug, 
            repo_name=repo_name, 
            note=collection_note,
            hf_token=hf_token)
        list_collection_items(collection)  
