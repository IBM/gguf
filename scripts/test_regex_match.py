import argparse
import re

def test_regex_match(regex_pattern, test_string) -> bool:
    """
    Tests if a regex pattern matches a given text.

    Args:
        regex_pattern (str): The regex pattern to search for (Note: can use: r"raw string").
        test_string (str): The text to search within.

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
    """
    match = re.search(regex_pattern, test_string)
    return bool(match)

if __name__ == "__main__":
    """
    Tests if a regex pattern matches a given text.

    Args:
        regex-pattern (str): The regex pattern to search for.
        text (str): The text to search within.

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
    """
    parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
    parser.add_argument("--regex-pattern", "-r", required=True, help="The regex pattern to search for")
    parser.add_argument("--text", "-t", required=True, help="The input text to search within")
    parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
    parser.add_argument('--debug', default=False, action='store_false', help='Enable debug output')

    # try:
    args = parser.parse_args()
    # NOTE: This script MUST only print True | False to stdout.
    matched = test_regex_match(regex_pattern=args.regex_pattern, test_string=args.text)
    print(matched)
    # except SystemExit as se:
    #     print(f"Usage: {parser.format_usage()}")
    #     print("False")
    #     exit(se)
    # except Exception as e:
    #     print(f"Error: {e}")
    #     print(f"Usage: {parser.format_usage()}")
    #     exit(2)
