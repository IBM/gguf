import os
import sys
import re

def test_regex_match(test_file:str, words_list:list[str]) -> bool:
    """
    Tests if a string contains at least two of the specified words using regex.

    Args:
        text (str): The string to search.
        words_list (list): A list of words to look for.

    Returns:
        bool: True if the string contains at least two words from the list,
              False otherwise.
    """
    try:
        with open(test_file, 'r') as file:
            test_string = file.read()
    except FileNotFoundError:
        print(f"[ERROR]: File not found at path: '{test_file}'")
        return False
    except Exception as exc:
         print(f"[ERROR] An error occurred: '{exc}'")
         return False

    # Create the regex pattern: \b(word1|word2|word3)\b
    # The '|' acts as an OR operator.
    pattern = r'\b(' + '|'.join(re.escape(word) for word in words_list) + r')\b'

    # re.findall() returns a list of all non-overlapping matches
    matches = re.findall(pattern, test_string,flags=re.IGNORECASE)
    print(f"matches: '{matches}'")
    unique_matches = set(matches)
    print(f"unique_matches: '{unique_matches}'")

    return len(unique_matches) >= 2

if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len < 3:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <regex_pattern> <test_string>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        sys.exit(1)

    # Parse input arguments into named params.
    fx_name = sys.argv[0]
    test_file = sys.argv[1]
    word_list = sys.argv[2]

    # invoke fx
    # NOTE: This script MUST only print True | False to stdout.
    # matched = test_regex_match(regex_pattern=regex_pattern, test_file=test_file)
    # target_words = ["Rayleigh", "scatter", "atmosphere"]
    target_words = word_list.split(',')
    matched = test_regex_match(test_file=test_file,words_list=target_words)

    # Return result
    print(matched)