import argparse
import base64
import sys

DELIM_BEGIN="-----BEGIN OPENSSH PRIVATE KEY-----"
DELIM_END="-----END OPENSSH PRIVATE KEY-----"

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

        # Remove any newline characters that openssl might add
        normalized_string = args.value.replace('\n', '')

        # Decode the base64 string to bytes
        decoded_bytes = base64.b64decode(normalized_string)

        # Decode the bytes to a string (assuming UTF-8 encoding)
        decoded_string = decoded_bytes.decode('utf-8')

        if decoded_string:
            with open(args.output_file, "w", encoding="utf-8") as file:
                if add_delimiters:
                    decoded_string.write(DELIM_BEGIN + "\n")
                file.write(decoded_string)
                if add_delimiters:
                    decoded_string.write(DELIM_END + "\n")
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
