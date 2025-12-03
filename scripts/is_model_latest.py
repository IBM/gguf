import sys
import argparse
import json

if __name__ == "__main__":
    try:
        # print(f"argv: {sys.argv}")

        # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("collection_config", help="The input text to search within")
        parser.add_argument('--model-name', "-m", type=str, required=True, help='model repo. name (e.g., \'granite-3.3-2b-instruct\')')
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', "-d", default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        # read the HF collection config. file
        with open(args.collection_config, "r") as file:
            json_data = json.load(file)
            formatted_json = json.dumps(json_data, indent=4)
            if(args.debug):
                print(formatted_json)

        collections_defn = json_data["collections"]
        for collection_defn in collections_defn:
            collection_items = collection_defn["items"]

            # upload all models associated with the collection
            for item_defn in collection_items:
                repo_name = item_defn["repo_name"]
                if repo_name.lower() == args.model_name.lower():
                    # is_latest = item_defn["is_latest"]
                    formatted_item_defn = json.dumps(item_defn, indent=4)
                    print(f"item_defn: '{formatted_item_defn}'", file=sys.stderr)
                    is_latest = item_defn.get("is_latest",False)
                    print(f"is_latest: '{is_latest}'", file=sys.stderr)
                    if is_latest:
                        print('true')
                        sys.exit(0)
                    else:
                        print('false')
                        sys.exit(0)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        print(f"Usage: {parser.format_usage()}")
        sys.exit(1)

    print(f"[ERROR] Unrecognized --model-name: '{args.model_name}'", file=sys.stderr)
    sys.exit(1)
