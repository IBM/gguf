import os
import sys
from huggingface_hub import hf_hub_download, snapshot_download, list_repo_files
from typing import List
import requests

from huggingface_hub import list_collections, create_collection, Collection, CollectionItem

# retrieve secrets
hf_token=os.environ['HF_TOKEN']

def list_collections_in_org(hf_owner:str="", hf_token:str=hf_token) -> None:
    collections = list_collections(owner=hf_owner, token=hf_token)
    for collection in collections:
        print(f"title: `{collection.title}`, private: {collection.private}, description: `{collection.description}`, slug: `{collection.slug}`")
        print(f"items: {collection.items}")
        print(f"---")

def create_collection_in_org(hf_owner:str="", title:str="", description:str="", private:bool=True, hf_token:str=hf_token) -> bool:
    
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
    except requests.exceptions.HTTPError as exc:
        print (f"HTTPError: {exc}")
    except requests.exceptions.ConnectionError as exc:
        print (f"ConnectionError: {exc}")
    except requests.exceptions.Timeout as exc:
        print (f"Timeout: {exc}")
    except requests.exceptions.RequestException as exc:
        print (f"RequestException: {exc}")
    else:
        # This block executes if no exception occurs
        print("Create collection was successful!")
        # Verify collection was added
        list_collections_in_org(hf_owner=hf_owner, hf_token=hf_token)    
        return True

if __name__ == "__main__":
    success = create_collection_in_org(hf_owner="mrutkows", title="Granite 3.2.0", description="IBM Granite 3.2.0", hf_token=hf_token)
    list_collections_in_org(hf_owner="mrutkows")
    list_collections_in_org(hf_owner="ibm-granite",hf_token=None)  
