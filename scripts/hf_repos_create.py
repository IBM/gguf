import os
import sys
import argparse
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

def test_empty_string(value:str):
        if not value:
            raise ValueError("Argument must not be an empty string")
        return value

if __name__ == "__main__":
    try:

        print(f"argv: {sys.argv}")

        # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("target_owner", type=test_empty_string, help="Target HF organization owner for repo. create")
        parser.add_argument("collection_config", help="The input text to search within")
        parser.add_argument('family', help='Granite family (i.e., instruct|vision|guardian)')
        parser.add_argument('private', default="True", help='Create the repo. as private')
        parser.add_argument('hf_token', help='HF access token')
        parser.add_argument('--repo-ext', default="", help='optional repo. name extension (e.g., \'-GGUF\')')
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_false', help='Enable debug output')

        # parse argv[] values
        args = parser.parse_args()

        # Print input variables being used for this run
        print(f">> target_owner='{args.target_owner}', collection_config='{args.collection_config}', family='{args.family}', private='{args.private}' ({type(args.private)}), hf_token='{args.hf_token}', repo_ext='{args.repo_ext}'")

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

            # upload all models associated with the collection
            for item_defn in collection_items:
                if(args.debug):
                    print(f"item_defn: '{item_defn}'")

                item_type = item_defn["type"]
                repo_name = item_defn["repo_name"]
                repo_id = item_defn["repo_id"]
                item_family = item_defn["family"]

                repo_id_2 = "/".join([args.target_owner, repo_name])

                if args.repo_ext:
                    repo_id_2 += ("-" + args.repo_ext)

                if args.family == item_family:
                    repo_org, repo_name = os.path.split(repo_id)
                    if args.verbose:
                        print(f"[INFO] Creating repo_id_2: repo_id: '{repo_id_2}'...")
                        print(f"[INFO] Creating repo: repo_id: '{repo_id}'...")
                        print(f"[INFO] Creating repo: repo_org: '{repo_org}', repo_name: '{repo_name}'...")

                    repoUrl = safe_create_repo_in_namespace(
                        repo_id=repo_id_2,
                        private=private,
                        hf_token=args.hf_token,
                    )

                    if repoUrl is None:
                        # Something went wrong creating
                        print(f"[ERROR] Repo: repo_id: '{repo_id}' not created.")
                        sys.exit(1)
                    if args.verbose:
                        print(f"[SUCCESS] Repo. created. repoUrl: '{repoUrl}')")

    except SystemExit as se:
        print(f"Usage: {parser.format_usage()}")
        exit(se)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        exit(2)

    # Exit successfully
    sys.exit(0)
