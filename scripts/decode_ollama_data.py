import argparse
import base64
import sys

def test_empty_string(value:str):
        if not value:
            raise ValueError("Argument must not be an empty string")
        return value

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--value", "-v", type=test_empty_string, required=True, help="")
        parser.add_argument("--output-file", "-f", type=test_empty_string, required=True, help="")
        parser.add_argument('--add-delimiters', "-a", default=False, action='store_true', help="")
        parser.add_argument('--debug', default=False, action='store_false', help="Enable debug output")
        args = parser.parse_args()

        if(args.debug):
            # Print input variables being used for this run
            print(f">> value='{args.value}', output-file='{args.output_file}', add-delimiters='{args.add_delimiters}'")

        add_delimiters = False
        # private needs to be a boolean
        if type(args.add_delimiters) is str:
            print(f"[WARNING] add_delimiters='{args.add_delimiters}' is a string. Converting to boolean...")
            if args.private.lower() == "true":
                add_delimiters = True
            else:
                add_delimiters = False

        # Encode the string to bytes using ASCII
        encoded_bytes = args.value.encode('ascii')
        print(f"encoded_bytes='{encoded_bytes}'")
        # Decode the Base64 string to bytes
        decoded_bytes = base64.b64decode(encoded_bytes)
        # Decode the bytes to a string using UTF-8
        decoded_string = decoded_bytes.decode('utf-8')

        if decoded_string:
            with open(args.output_file, "w", encoding="utf-8") as file:
                file.write(decoded_string)
            if args.debug:
                print(f"Decoded string saved to '{args.output_file}'")

    except SystemExit as se:
        print(f"Usage: {parser.format_usage()}")
        exit(se)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        exit(2)

    # Exit successfully
    sys.exit(0)
