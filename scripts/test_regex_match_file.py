import os
import sys
import re

def test_regex_match(regex_pattern:str, test_file:str) -> bool:
    """
    Tests if a regex pattern matches a given text.

    Args:
        regex_pattern (str): The regex pattern to search for (Use: r"raw string").
        test_file (str): The text to search within.

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
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
    
    match = re.search(regex_pattern, test_string)
    return bool(match)

if __name__ == "__main__":   
    arg_len = len(sys.argv)
    if arg_len < 3:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <regex_pattern> <test_string>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]   
    regex_pattern = sys.argv[1]
    test_file = sys.argv[2]   
     
    # invoke fx
    # NOTE: This script MUST only print True | False to stdout.    
    matched = test_regex_match(regex_pattern=regex_pattern, test_file=test_file)

    # Return result
    print(matched)