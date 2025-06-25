import argparse
import sys
import urllib.request

def url_file_exists(url):
    try:
        # Attempt to open the URL
        response = urllib.request.urlopen(url)
        # If the request is successful, check the status code
        if response.getcode() == 200:
            return True
        else:
            return False
    except Exception:
        # If any error occurs (e.g., file not found, network error), return False
        return False

# file_url = "https://www.example.com/some_file.txt"
# if check_url_file_exists(file_url):
#     print(f"File exists at: {file_url}")
# else:
#     print(f"File does not exist at: {file_url}")

def test_empty_string(value:str):
        if not value:
            raise ValueError("Argument must not be an empty string")
        return value

if __name__ == "__main__":
    try:
        # TODO: change 'private' arg. (i.e., a positional, string) to a boolean flag (i.e., --private)
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("url", type=test_empty_string, help="URL to check")
        parser.add_argument('--debug', default=False, action='store_false', help='Enable debug output')
        args = parser.parse_args()

        if(args.debug):
            # Print input variables being used for this run
            print(f">> url='{args.url}'")

        if url_file_exists(args.url):
            print(f"File exists at: {args.url}")
            sys.exit(0)
        else:
            print(f"File does NOTE exist at: {args.url}")
            sys.exit(1)

    except Exception as exc:
        print(f"Exception: {exc}")
        sys.exit(1)

# Store in a variable. Otherwise, it will be overwritten after the next command
# exit_status=$?
# if [ "${exit_status}" -ne 0 ];
# then
#     echo "exit ${exit_status}"
# fi
# echo "EXIT 0"
