import os
import sys
import json

def encode_file_with_whitespace(input_filepath, output_filepath):
    """
    Encodes the contents of a file into a string, preserving whitespace,
    and saves the encoded string to another file.
    """
    try:
        with open(input_filepath, 'r') as input_file:
            print(f"Reading file: {input_filepath}...")            
            content = input_file.read()
            encoded_content = json.dumps(content)
            
        with open(output_filepath, 'w') as output_file:
            print(f"Saving file: {output_filepath}...")
            output_file.write(encoded_content)

    except FileNotFoundError:
        print(f"[ERROR] input_file '{input_filepath}' or output_file '{output_filepath}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":

    arg_len = len(sys.argv)
    if arg_len < 3:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <input_filename> <output_filename>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        sys.exit(1)
        
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]   
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Affirm parameter assignments
    print(f"input file: {input_file}, output file: {output_file}")

    encode_file_with_whitespace(input_file, output_file)
    print(f"File '{input_file}' encoded and saved to '{output_file}'.")
