import os
import sys
import requests

from huggingface_hub import create_repo, RepoUrl
from huggingface_hub.utils import HfHubHTTPError

# Constants
HF_COLLECTION_DESC_MAX_LEN = 150

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
    if arg_len < 5:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <target_owner:str> <collection_config:str> <family:str> <private:bool> <hf_token:str>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        # Exit with an error code
        sys.exit(1)

    # Parse input arguments into named params.
    fx_name = sys.argv[0]
    target_owner = sys.argv[1]
    # TODO: "private should default to True (confirmed by "pre" tags);
    # if workflow was started with a "release" tag, then change to False
    collection_config = sys.argv[2]
    family = sys.argv[3]
    private = sys.argv[4]
    hf_token = sys.argv[5]

    # Print input variables being used for this run
    print(f">> {fx_name}: owner='{target_owner}', config='{collection_config}', family='{family}', private='{private}' ({type(private)}), hf_token='{hf_token}'")

    # private needs to be a boolean
    if type(private) is str:
        print(f"[WARNING] private='{private}' is a string. Converting to boolean...")
        if private.lower() == "true":
            private = True
        else:
            private = False

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
            item_family = item_defn["family"]
            if family == item_family:
                repo_org, repo_name = os.path.split(repo_id)
                print(f"[INFO] Creating repo: repo_id: '{repo_id}'...")
                print(f"[INFO] Creating repo: repo_org: '{repo_org}', repo_name: '{repo_name}'...")

                repoUrl = safe_create_repo_in_namespace(
                    repo_id=repo_id,
                    private=private,
                    hf_token=hf_token,
                )

                if repoUrl is None:
                    # Something went wrong creating
                    print(f"[ERROR] Repo: repo_id: '{repo_id}' not created.")
                    sys.exit(1)

                print(f"repoUrl: '{repoUrl}')")

    # Exit successfully
    sys.exit(0)
