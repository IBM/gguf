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
    # for collection in collections:
    print(f"---")
    print(f"title: `{collection.title}`, private: {collection.private}, description: `{collection.description}`, slug: `{collection.slug}`")
    print(f"list_items: {list_items} ({type(list_items)})")
    if list_items is not None:
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
            # TODO: set namespace to "hf_owner"
            collection = create_collection(
                namespace=hf_owner,
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


def add_update_collection_item(collection_slug:str="", repo_name:str="", item_type:str="model", hf_token:str="") -> Collection:
    if collection_slug == "":
        print("Please provide a slug (ID) for the collection.")
        return False
    if repo_name == "":
        print("Please provide a repo_name for the collection.")
        return False      
    if hf_token == "":
        print("Please provide a token")
        return False      
    
    # If an item already exists in a collection (same item_id/item_type pair), 
    # an HTTP 409 error will be raised. 
    # You can choose to ignore this error by setting exists_ok=True   
    # TODO: do we need to support "note" arg.? It is Optional; not sure where this appears in HF UI. 
    try:
        collection = add_collection_item(
            collection_slug,
            item_id=repo_name,
            item_type=item_type,
            exists_ok=True,
            token=hf_token,
        )
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, collection.title: '{collection_title}'")
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
    if arg_len < 4:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <target_owner:str> <collection_config:str> <private:bool> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]
    target_owner = sys.argv[1]  
    # TODO: "private should default to True (confirmed by "pre" tags); 
    # if workflow was started with a "release" tag, then change to False
    collection_config = sys.argv[2]
    private = sys.argv[3] 
    hf_token = sys.argv[4]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: owner='{target_owner}', config='{collection_config}', private='{private}', hf_token='{hf_token}'")     
    
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
        collection = safe_create_collection_in_namespace(
            hf_owner=target_owner, 
            title=collection_title, 
            description=collection_desc, 
            hf_token=hf_token,
        )
       
        # verify collection has been created
        # print(f"DEBUG........................................................")
        # existing_collection = get_collection_by_title(
        #     hf_owner=target_owner, 
        #     title=collection_title, 
        #     hf_token=hf_token,
        # )
                
        # # Assure items in collection exist
        # if existing_collection is not None:
        #     list_collection_attributes(existing_collection,True)
        # else:
        #     print(f"Collection '{collection_title}' not found in namespace '{target_owner}'")
        # print(f"DEBUG........................................................")
                
        if collection is None:
            # Something went wrong creating
            print(f"ERROR: Collection '{collection_title}' not created in namespace '{target_owner}'")
            sys.exit(1)
            
        # upload all models associated with the collection
        for item_defn in collection_items:
            print(f"item ('{type(item_defn)}')='{item_defn}'")
            item_type = item_defn["type"]
            repo_name = item_defn["repo_name"]
            item_type = item_defn["type"]
                                
            add_update_collection_item(
                collection_slug=collection.slug, 
                repo_name=repo_name, 
                hf_token=hf_token)
         
    # Print output variables
    print(f"collection: {collection}") 
    
    # Exit successfully
    sys.exit(0) 
    