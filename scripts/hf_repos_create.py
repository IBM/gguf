import sys
import argparse
import requests
import ast
import json

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

def is_repo_name_in_list(repo_name, repo_list) -> bool:
    for i in range(len(repo_list)):
        if repo_name in repo_list[i]:
            return True
    return False

if __name__ == "__main__":
    try:
        print(f"argv: {sys.argv}")

        # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("target_owner", type=test_empty_string, help="Target HF organization owner for repo. create")
        parser.add_argument("collection_config", help="The input text to search within")
        parser.add_argument('include', type=str, help='A string representation of a list of repo. names to include')
        parser.add_argument('family', help='Granite family (i.e., instruct|vision|guardian)')
        parser.add_argument('private', default="True", help='Create the repo. as private')
        parser.add_argument('hf_token', help='Hugging Face Hub API access token.')
        parser.add_argument('-x', '--ext', type=str, default="", help='optional repo. name extension (e.g., \'-GGUF\')')
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', "-d", default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        if(args.debug):
            # Print input variables being used for this run
            print(f">> include='{args.include}', Type: {type(args.include)}")
            print(f">> target_owner='{args.target_owner}', collection_config='{args.collection_config}', family='{args.family}', private='{args.private}' ({type(args.private)}), hf_token='{args.hf_token}', ext='{args.ext}'")

        # The repo. array string needs to use double quotes for list items
        # or it will not parse to JSON
        normalized_include = args.include.replace("'", '"')
        repo_list = json.loads(normalized_include)
        # print(f"repo_list: {repo_list}, type: {type(repo_list)}")

        if len(repo_list) == 0:
            print(f"[INFO] repo_list empty. Exiting...")
            sys.exit(0)

        # private needs to be a boolean
        if type(args.private) is str:
            print(f"[WARNING] private='{args.private}' is a string. Converting to boolean...")
            if args.private.lower() == "true":
                private = True
            else:
                private = False

        # read the HF collection config. file
        with open(args.collection_config, "r") as file:
            json_data = json.load(file)
            formatted_json = json.dumps(json_data, indent=4)
            if(args.debug):
                print(formatted_json)

        collections_defn = json_data["collections"]
        for collection_defn in collections_defn:
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
                item_family = item_defn["family"]

                # Only create the repo. if the family matches the input family
                # AND if it appears in the "include" list (i.e., in the build matrix)
                if (args.family == item_family) and is_repo_name_in_list(repo_name, repo_list):
                    if args.family == item_family:
                        # construct the full HF repo. ID
                        repo_id = "/".join([args.target_owner, repo_name]) + args.ext
                        if args.verbose:
                            print(f"[INFO] Creating repo: repo_id: '{repo_id}'...")

                        repoUrl = safe_create_repo_in_namespace(
                            repo_id=repo_id,
                            private=private,
                            hf_token=args.hf_token,
                        )

                        if repoUrl is None:
                            # Something went wrong creating
                            print(f"[ERROR] Repo: repo_id: '{repo_id}' not created.")
                            sys.exit(1)
                        if args.verbose:
                            print(f"[SUCCESS] Repo. created. repoUrl: '{repoUrl}')")
                else:
                    print(f"[INFO] Skipping repo_name='{repo_name}'...")

    except SystemExit as se:
        if se.code != 0:
            print(f"Usage: {parser.format_usage()}")
            exit(se)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        exit(2)

    # Exit successfully
    sys.exit(0)
