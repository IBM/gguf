import os
import sys
import argparse
import requests

from huggingface_hub import list_collections, create_collection, add_collection_item, Collection, CollectionItem
from huggingface_hub.utils import HfHubHTTPError

# Constants
HF_COLLECTION_DESC_MAX_LEN = 150

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
            print(f"[INFO] Creating collection '{title}' ({'private' if private else 'public'}) in namespace '{hf_owner}'...")
            collection = create_collection(
                namespace=hf_owner,
                title=title,
                description=description,
                private=private,
                token=hf_token,
        )
        else:
            print(f"[WARNING] Collection '{title}' already exists in namespace '{hf_owner}'")
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


def add_update_collection_item(collection_slug:str="", repo_id:str="", item_type:str="model", hf_token:str="") -> Collection:
    if collection_slug == "":
        print("Please provide a slug (ID) for the collection item.")
        return False
    if repo_id == "":
        print("Please provide a repo_id for the collection item.")
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
            item_id=repo_id,
            item_type=item_type,
            exists_ok=True,
            token=hf_token,
        )
    except HfHubHTTPError as exc:
        print(f"HfHubHTTPError: {exc.server_message}, item_id: '{repo_id}'")
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
    # print(f"argv: {sys.argv}")

    # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
    parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
    parser.add_argument("target_owner", help="Target HF organization owner for repo. create")
    parser.add_argument("collection_config", help="The input text to search within")
    parser.add_argument('family', help='Granite family (i.e., instruct|vision|guardian)')
    parser.add_argument('private', default="True", help='Create the repo. as private')
    parser.add_argument('hf_token', help='HF access token')
    parser.add_argument('-x', '--ext', type=str, default="", help='optional repo. name extension (e.g., \'-GGUF\')')
    parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
    parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')

    # parse argv[] values
    args = parser.parse_args()

    if(args.debug):
        # Print input variables being used for this run
        print(f">> target_owner='{args.target_owner}', collection_config='{args.collection_config}', family='{args.family}', private='{args.private}' ({type(args.private)}), hf_token='{args.hf_token}', ext='{args.ext}'")

    # private needs to be a boolean
    if type(args.private) is str:
        print(f"[WARNING] private='{args.private}' is a string. Converting to boolean...")
        if args.private.lower() == "true":
            private = True
        else:
            private = False

    # invoke fx
    import json
    with open(args.collection_config, "r") as file:
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
        # Test for known HF field constraints
        # TODO: lint for this length early in CI (or even in PR workflow)
        if len(collection_desc) > HF_COLLECTION_DESC_MAX_LEN:
            print(f"[ERROR] title='{collection_desc}' exceeds {HF_COLLECTION_DESC_MAX_LEN} character limit.")
            sys.exit(2)

        # Create the actual collection
        collection = safe_create_collection_in_namespace(
            hf_owner=args.target_owner,
            title=collection_title,
            description=collection_desc,
            hf_token=args.hf_token,
        )
        # Fail fast if the collection was not created
        if collection is None:
            # Something went wrong creating
            print(f"[ERROR] Collection '{collection_title}' not created in namespace '{args.target_owner}'")
            sys.exit(1)

        print(f"[INFO] Collection: '{collection}' created in namespace '{args.target_owner}'")

        # upload all models associated with the collection
        for item_defn in collection_items:
            item_type = item_defn["type"]
            repo_name = item_defn["repo_name"]
            item_family = item_defn["family"]

            # construct the full HF repo. ID
            repo_id = "/".join([args.target_owner, repo_name]) + args.ext

            if args.family == item_family:
                print(f"[INFO] >> Adding item: '{item_defn}'")
                add_update_collection_item(
                    collection_slug=collection.slug,
                    repo_id=repo_id,
                    hf_token=args.hf_token)

    # Exit successfully
    sys.exit(0)
