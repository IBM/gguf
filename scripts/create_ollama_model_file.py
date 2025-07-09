import os
import sys
import argparse
import json
from enum import StrEnum

class MODELFILE_INSTRUCTIONS(StrEnum):
    FROM      = "FROM"
    PARAMETER = "PARAMETER"
    TEMPLATE  = "TEMPLATE"
    SYSTEM    = "SYSTEM"
    ADAPTER   = "ADAPTER"
    LICENSE   = "LICENSE"
    MESSAGE   = "MESSAGE"

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--model-file", "-m", type=str, required=True, help="Path to gguf model file.")
        parser.add_argument("--output-file", "-o", type=str, required=True, help="Path to output (Ollama Modelfile).")
        parser.add_argument("--metadata-path", "-p", type=str, required=True, help="Path to model metadata files.")
        parser.add_argument("--template-file", "-tf", type=str, required=False, help="")
        parser.add_argument("--system-file", "-sf", type=str, required=False, help="")
        parser.add_argument("--params-file", "-pf", type=str, required=False, help="")
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        if args.debug:
            print(f"[DEBUG] args.output_file='{args.output_file}'")
            print(f"[DEBUG] args.metadata_path='{args.metadata_path}'")
            print(f"[DEBUG] args.template_file='{args.template_file}'")
            print(f"[DEBUG] args.system_file='{args.system_file}'")
            print(f"[DEBUG] args.params_file='{args.params_file}'")

        template_file_contents = ""
        system_file_contents = ""
        params_file_contents = ""

        if args.verbose:
            print(f"Creating output Modelfile ('{args.output_file}')...")

        with open(args.output_file, 'w') as modelfile:

            if args.model_file is not None:
                if not os.path.isfile(args.model_file):
                    raise FileNotFoundError(f"The --model-file '{args.model_file}' does not exist.")
                modelfile.write(f"{MODELFILE_INSTRUCTIONS.FROM} {args.model_file}\n")

            if args.template_file is not None:
                filename = args.metadata_path + "/" + args.template_file
                with open(filename, 'r') as file:
                    template_file_contents = file.read()
                if args.debug:
                    print(f"args.template_file ({args.template_file}):")
                    print('"""'+template_file_contents+'"""')
                modelfile.write(f"{MODELFILE_INSTRUCTIONS.TEMPLATE} \"\"\"{template_file_contents}\"\"\"\n")

            if args.system_file is not None:
                filename = args.metadata_path + "/" + args.system_file
                with open(filename, 'r') as file:
                    system_file_contents = file.read()
                if args.debug:
                    print(f"args.system_file ({args.system_file}):")
                    print('"""'+system_file_contents+'"""')
                modelfile.write(f"{MODELFILE_INSTRUCTIONS.SYSTEM} \"\"\"{system_file_contents}\"\"\"\n")

            if args.params_file is not None:
                filename = args.metadata_path + "/" + args.params_file
                with open(filename, 'r') as file:
                    params_dict = json.load(file)
                    for key, value in params_dict.items():
                        if args.debug:
                            print(f"{key}: {value}")
                        modelfile.write(f"{MODELFILE_INSTRUCTIONS.PARAMETER} {key} {value}\n")

    except IOError as e:
        print(f"Error: unable to write to file: {e}")
        # Cleanup Modelfile if unable to write to
        if os.path.exists(args.model_file):
            os.remove(args.model_file)
            print(f">> Deleting '{args.model_file}' due to write error.")
        exit(1)
    except FileNotFoundError:
        print(f"Error: The file '{args.filename}' was not found.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(2)