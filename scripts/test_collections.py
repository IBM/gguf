import os
import sys
from huggingface_hub import hf_hub_download, snapshot_download, list_repo_files
from typing import List
import requests

from huggingface_hub import list_collections, create_collection, Collection, CollectionItem

# retrieve secrets
hf_token=os.environ['HF_TOKEN']

def get_collection_by_title(hf_owner:str="", hf_token:str=hf_token, title:str="") -> Collection:
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
        print(f"---")
        if list_items:
            list_collection_items(collection=collection) 

def list_collection_items(collection:Collection=None) -> None:
    if collection is None:
        print("Please provide a valid collection")
        return
    num_items = len(collection.items)
    if num_items > 0:
        print(f"items ({num_items}): {collection.items}")
    else:
        print(f"None")

def get_collections_in_namespace(hf_owner:str="", hf_token:str=hf_token) -> None:
    collections = list_collections(owner=hf_owner, token=hf_token)
    return collections

def create_collection_in_namespace(hf_owner:str="", title:str="", description:str="", private:bool=True, hf_token:str=hf_token) -> Collection:
    if title == "":
        print("Please provide a title for the new collection")
        return False
    if description == "":
        print("Please provide a description for the new collection")
        return False        
    
    try:
        collection = create_collection(
            title=title,
            description=description,
            private=private,
            token=hf_token,
        )
    # except huggingface_hub.HfHubHTTPError as exc:
    #     print (f"HTTPError: {exc}")
    except requests.exceptions.HTTPError as exc:
        has_attribute = hasattr(exc, "server_message")
        if has_attribute:
            print(f"HfHubHTTPError: {exc.server_message}")
        else:
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
    
    # Test ibm-granite
    collections = get_collections_in_namespace(hf_owner="ibm-granite", hf_token=hf_token) 
    list_collection_attributes(collections=collections, list_items=True)
   
    #collection = create_collection_in_namespace(hf_owner="mrutkows", title="Granite 3.2.0", description="IBM Granite 3.2.0", hf_token=hf_token)
   
    existing_collection = get_collection_by_title(hf_owner="mrutkows", title="Granite 3.2.0", hf_token=hf_token)
    if existing_collection is not None:
        print("Collection already exists!")
        list_collection_items(existing_collection) 
