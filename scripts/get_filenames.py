import sys
import argparse

from pathlib import Path

def get_files_with_extension(path, extension):
    """
    Retrieves a space-separated string of file paths matching a specified extension,
    recursively from a given root path.

    Args:
        path (str): The starting directory path.
        extension (str): The desired file extension (e.g., '.txt', '.py').

    Returns:
        str: A space-separated string of matching file paths.
    """
    directory_path = Path(path)
    if not directory_path.is_dir():
        return ""

    # Use rglob to recursively find files matching the pattern
    # The pattern includes the extension (e.g., "*.txt")
    file_paths = [str(file) for file in directory_path.rglob(f"*{extension}")]
    return " ".join(file_paths)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--path", "-p", type=str, required=True, help="path to search')")
        parser.add_argument("--extension", "-x", type=str, required=True, help="file to read and store the contents of')")
        parser.add_argument("--output-file", "-o", type=str, required=True, help="The name of the output file to create or overwrite.")
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        file_list = get_files_with_extension(args.path, args.extension)

        with open(args.output_file, 'w') as f:
            f.write(file_list)

    except IOError as e:
        print(f"Error: Unable to write to file '{args.output_file}': {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(2)