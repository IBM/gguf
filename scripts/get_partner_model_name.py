import sys
import argparse
from enum import StrEnum

MODEL_NAME_SEP = "-"
MODEL_FAMILY = "granite"
MODEL_FORMAT_GGUF = "gguf"

class SUPPORTED_PARTNERS(StrEnum):
    OLLAMA = "ollama"

class SUPPORTED_MODEL_MODALITIES(StrEnum):
    BASE = "base"
    INSTRUCT = "instruct"
    GUARDIAN = "guardian"
    VISION = "vision"
    EMBEDDING = "embedding"

class SUPPORTER_MODEL_VERSIONS(StrEnum):
    GRANITE_3_1  = "3.1"
    GRANITE_3_2  = "3.2"
    GRANITE_3_3  = "3.3"
    GRANITE_4_0  = "4.0"
    GRANITE_4_1  = "4.1"

class SUPPORTED_MODEL_PARAMETER_SIZES(StrEnum):
    B1  = "1b"
    B2  = "2b"
    B7  = "7b"
    B8  = "8b"
    B30 = "30b"
    T1  = "1t"

class SUPPORTED_MODEL_QUANTIZATIONS(StrEnum):
    F32     = "f32"
    F16     = "f16"
    Q2_K    = "q2_K"
    Q3_K_S  = "q3_K_S"
    Q3_K_M  = "q3_K_M"
    Q3_K_L  = "q3_K_L"
    Q4_0    = "q4_0"
    Q4_K_S  = "q4_K_S"
    Q4_K_M  = "q4_K_M"
    Q4_K_L  = "q4_K_L"
    Q5_0    = "q5_0"
    Q5_K_S  = "q5_K_S"
    Q5_K_M  = "q5_K_M"
    Q5_K_L  = "q5_K_L"
    Q6_K    = "q6_K"
    Q8_0    = "q8_0"

class SUPPORTED_MODEL_ACTIVE_PARAMETER_COUNTS(StrEnum):
    A400M = "a400m"
    A800M = "a800m"

class MODEL_LAYER_CONNECTION_TYPES(StrEnum):
    DENSE = "dense"
    SPARSE = "sparse"

def enum_contains(enum_type, value):
    try:
        enum_type(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--hf-model-name", "-m", type=str, required=True, help="IBM Hugging face model name pattern (e.g., 'granite-3.2-2b-instruct')")
        parser.add_argument("--partner", "-p", type=str, required=True, help="Partner name (e.g., 'ollama')")
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_false', help='Enable debug output')
        args = parser.parse_args()

        if(args.debug):
            # Print input variables being used for this run
            print(f">> hf_model_name='{args.hf_model_name}', partner='{args.partner}'")

        normalized_model_name = args.hf_model_name.lower()

        # verify partner (output format) is known
        if args.partner not in SUPPORTED_PARTNERS.__members__.values():
            raise ValueError(f"invalid --partner. Model family '{SUPPORTED_PARTNERS}' not found.")

        # verify model family name
        if MODEL_FAMILY not in normalized_model_name:
            raise NameError(f"invalid --hf-model-name. Model family '{MODEL_FAMILY}' not found.")

        # strip model format (if present)
        normalized_model_name = normalized_model_name.replace(MODEL_NAME_SEP+MODEL_FORMAT_GGUF, "")

        model_family = MODEL_FAMILY.lower()
        model_version = ""
        model_modality = ""
        model_parameter_size = "" # e.g., 2B, 8B, 1T
        model_quantization = ""  # e.g., q8_0, q4_K_M
        model_active_parameter_count = "" # e.g., a800m, a400m

        for modality in SUPPORTED_MODEL_MODALITIES:
           if modality in normalized_model_name:
               model_modality = modality
               #print(f"model_name contains modality: '{model_modality}'", file=sys.stderr)
               break

        for version in SUPPORTER_MODEL_VERSIONS:
           if version in normalized_model_name:
               model_version = version
               #print(f"model_name contains version: '{model_version}'", file=sys.stderr)
               break

        for param_size in SUPPORTED_MODEL_PARAMETER_SIZES:
           if param_size in normalized_model_name:
               model_parameter_size = param_size
               #print(f"model_name contains parameter size: '{model_parameter_size}'", file=sys.stderr)
               break

        for active_param_count in SUPPORTED_MODEL_ACTIVE_PARAMETER_COUNTS:
           if active_param_count in normalized_model_name:
               model_active_parameter_count = active_param_count
               #print(f"model_name contains parameter size: '{model_parameter_size}'", file=sys.stderr)
               break

        for quantization in SUPPORTED_MODEL_QUANTIZATIONS:
           if quantization.lower() in normalized_model_name:
               model_quantization = quantization
               #print(f"model_name contains quantization: '{model_quantization}'", file=sys.stderr)
               break

        # TODO: support "sparse" for embedding models (if we ever publish them) and also:
        # NOTE: "dense" is default and is not currently included in the model name
        if args.partner == SUPPORTED_PARTNERS.OLLAMA:
            model_version = model_version.replace(".", "")
            model_version = model_version.replace("v", "")
            partner_model_base = f"{model_family}{model_version}-{model_modality}"

            # TODO: determine if we need to append this for partner models:
            # if model_active_parameter_count is not None:
            #     partner_model_base += f"-{model_active_parameter_count}"

            partner_model_name = f"{partner_model_base}:{model_parameter_size}"
            if model_quantization is not None:
                partner_model_name += f"-{model_quantization}"

        # NOTE: This script MUST only return a string
        print(partner_model_name)
    except SystemExit as se:
        print(f"Usage: {parser.format_usage()}", file=sys.stderr)
        exit(se)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Usage: {parser.format_usage()}", file=sys.stderr)
        exit(2)

    # Exit successfully
    sys.exit(0)