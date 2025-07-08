import sys
import argparse

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--filename", "-f", type=str, required=True, help="file to read and store the contents of')")
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        with open(args.filename, 'r') as file:
            file_contents = file.read()
        print("File contents stored in string variable:")
        print(file_contents)
    except FileNotFoundError:
        print(f"Error: The file '{args.filename}' was not found.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(2)