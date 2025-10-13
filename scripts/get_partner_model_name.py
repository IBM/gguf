import sys
import argparse
from enum import StrEnum

MODEL_NAME_SEP = ":"
MODEL_ATTRIBUTE_SEP = "-"
MODEL_FAMILY = "granite"
MODEL_FORMAT_GGUF = "gguf"

class SUPPORTED_PARTNERS(StrEnum):
    OLLAMA = "ollama"

class SUPPORTED_MODEL_MODALITIES(StrEnum):
    BASE = "base"
    INSTRUCT = "instruct"
    GUARDIAN = "guardian"
    VISION = "vision"
    SPEECH = "speech"
    EMBEDDING = "embedding"

MINOR_VERSION_POINT_ZERO = ".0"
class SUPPORTER_MODEL_VERSIONS(StrEnum):
    GRANITE_3_0  = "3.0"
    GRANITE_3_1  = "3.1"
    GRANITE_3_2  = "3.2"
    GRANITE_3_3  = "3.3"
    GRANITE_4_0  = "4.0"
    GRANITE_4_1  = "4.1"

class SUPPORTED_MODEL_PARAMETER_SIZES(StrEnum):
    M30  = "30m"
    M38  = "38m"
    M84  = "84m"  # "medical"
    M107 = "107m"
    M125 = "125m"
    M278 = "278m"
    M300 = "300m"
    B1   = "1b"
    B2   = "2b"
    B3   = "3b"
    B5   = "5b"
    B7   = "7b"
    B8   = "8b"
    B20  = "20b"  # "function-calling"
    B30  = "30b"
    T1   = "1t"

class ABSTRACT_MODEL_PARAMETER_SIZES(StrEnum):
    NANO    = "nano"
    MICRO   = "micro"
    TINY    = "tiny"  # NOTE: for v4.0 models we declare relative sizes using names (e.g., tiny ~= 7B)
    SMALL   = "small"
    MEDIUM  = "medium"
    LARGE   = "large"

class SUPPORTED_MODEL_QUANTIZATIONS(StrEnum):
    F32     = "f32"
    F16     = "f16"
    FP16    = "fp16"
    Q2_K    = "q2_K"
    Q3_K_S  = "q3_K_S"
    Q3_K_M  = "q3_K_M"
    Q3_K_L  = "q3_K_L"
    Q4_0    = "q4_0"
    Q4_1    = "q4_1"
    Q4_K_S  = "q4_K_S"
    Q4_K_M  = "q4_K_M"
    Q4_K_L  = "q4_K_L"
    Q5_0    = "q5_0"
    Q5_1    = "q5_1"
    Q5_K_S  = "q5_K_S"
    Q5_K_M  = "q5_K_M"
    Q5_K_L  = "q5_K_L"
    Q6_K    = "q6_K"
    Q8_0    = "q8_0"

class SUPPORTED_MODEL_ACTIVE_PARAMETER_COUNTS(StrEnum):
    A400M = "a400m"
    A800M = "a800m"

class MODEL_LAYER_DESCRIPTIVE_TYPES(StrEnum):
    DENSE = "dense"
    SPARSE = "sparse"
    MOE = "moe"

class MODEL_ARCH_DESCRIPTIVE_TYPES(StrEnum):
    HYBRID = "h" # IBM Granite 4.0 chose to use simply "h" for hybrid (mamba2)

class SUPPORTED_MODEL_LANGUAGES(StrEnum):
    ENGLISH = "english"
    CHINESE = "chinese"
    MULTILINGUAL = "multilingual"

class SUPPORTED_RELEASE_STAGES(StrEnum):
    PREVIEW = "preview"

def enum_contains(enum_type, value):
    try:
        enum_type(value)
        return True
    except ValueError:
        return False

def model_name_append_attribute(current_model_name: str, attribute: str, base_sep: str, attr_sep:str) -> str:
    # if this is not the first attribute after the designated separator
    if attribute:
        if not current_model_name.endswith(base_sep):
            current_model_name += attr_sep
        updated_model_name = f"{current_model_name}{attribute}"
        return updated_model_name
    return current_model_name

def ollama_append_attribute(current_model_name: str, attribute: str) -> str:
    return model_name_append_attribute(current_model_name, attribute, MODEL_NAME_SEP, MODEL_ATTRIBUTE_SEP)

# def test_empty_string(value:str):
#         if not value:
#             raise ValueError("Argument must not be an empty string")
#         return value

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--hf-model-name", "-m", type=str, required=True, help="IBM Hugging face model name pattern (e.g., 'granite-3.2-2b-instruct')")
        parser.add_argument("--partner", "-p", type=str, required=True, help="Partner name (e.g., 'ollama')")
        parser.add_argument('--default-quant',  default=False, action='store_true', help='Model selected as the default quantization')
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        if(args.debug):
            # Print input variables being used for this run
            print(f">> hf_model_name='{args.hf_model_name}', partner='{args.partner}', default_quant='{args.default_quant}'")

        normalized_model_name = args.hf_model_name.lower()

        # verify partner (output format) is known
        if args.partner not in SUPPORTED_PARTNERS.__members__.values():
            raise ValueError(f"invalid --partner. Model family '{SUPPORTED_PARTNERS}' not found.")

        # verify model family name
        if MODEL_FAMILY not in normalized_model_name:
            raise NameError(f"invalid --hf-model-name. Model family '{MODEL_FAMILY}' not found.")

        # strip model format (if present)
        normalized_model_name = normalized_model_name.replace(MODEL_ATTRIBUTE_SEP+MODEL_FORMAT_GGUF, "")

        model_family = MODEL_FAMILY.lower()
        model_version = ""
        model_layer_desc = "" # e.g., "dense", "moe" (only used for 3.0, 3.1 legacy)
        model_arch_desc = "" # e.g., "hybrid" or "h"
        model_modality = "" # e.g., "instruct", "vision"
        model_language = "" # e.g., "english", "multilingual"
        model_parameter_size = "" # e.g., 2B, 8B, 1T
        model_abstract_size = "" # e.g., micro, tiny, small
        model_quantization = ""  # e.g., q8_0, q4_K_M
        model_active_parameter_count = "" # e.g., a800m, a400m
        model_release_stage = "" # Not used in name for now... e.g., preview

        for modality in SUPPORTED_MODEL_MODALITIES:
           if modality in normalized_model_name:
               model_modality = modality
               break

        for version in SUPPORTER_MODEL_VERSIONS:
           if version in normalized_model_name:
               model_version = version
               break

        # NOTE: Have to test strictly for "-h" as ANY "h" occurrence will be found in model name
        for arch_desc in MODEL_ARCH_DESCRIPTIVE_TYPES:
           if MODEL_ATTRIBUTE_SEP+arch_desc in normalized_model_name:
               model_arch_desc = arch_desc
               break

        for param_size in SUPPORTED_MODEL_PARAMETER_SIZES:
           if param_size in normalized_model_name:
               model_parameter_size = param_size
               break

        for abstract_param_size in ABSTRACT_MODEL_PARAMETER_SIZES:
           if abstract_param_size in normalized_model_name:
               model_abstract_size = abstract_param_size
               break

        for active_param_count in SUPPORTED_MODEL_ACTIVE_PARAMETER_COUNTS:
           if active_param_count in normalized_model_name:
               model_active_parameter_count = active_param_count
               break

        for quantization in SUPPORTED_MODEL_QUANTIZATIONS:
           if quantization.lower() in normalized_model_name:
               model_quantization = quantization
               break

        for language in SUPPORTED_MODEL_LANGUAGES:
           if language.lower() in normalized_model_name:
               model_language = language
               break

        # Not used currently
        for stage in SUPPORTED_RELEASE_STAGES:
           if stage.lower() in normalized_model_name:
               model_release_stage = stage
               break

        # Granite 4.0 fixup: as this version's HF model names do not include "instruct" (i.e., assumed default)
        # For now, we use the presence of an abstract "size" as an indicator of this case (assuming
        # this abstract naming will continue post v4).
        if model_modality == "" and (model_abstract_size in ABSTRACT_MODEL_PARAMETER_SIZES):
            if model_release_stage == SUPPORTED_RELEASE_STAGES.PREVIEW:
                # HACK: for "tiny-preview"
                model_modality = SUPPORTED_MODEL_MODALITIES.INSTRUCT

        # if model_parameter_size == "":
        #     raise ValueError(f"Parameter size not found in model name: `{normalized_model_name}`")

        if model_quantization == "":
            raise ValueError(f"Quantization not found in model name: `{normalized_model_name}`")

        if model_release_stage != "":
            if args.debug:
                print(f"DEBUG: Model stage found in model name: `{normalized_model_name}`")

        if args.debug:
            print(f"model_family='{model_family}'\n \
                model_layer_desc='{model_layer_desc}'\n \
                model_arch_desc='{model_arch_desc}'\n \
                model_modality='{model_modality}'\n \
                model_version='{model_version}'\n \
                model_parameter_size='{model_parameter_size}'\n \
                model_abstract_size='{model_abstract_size}'\n \
                model_active_parameter_count='{model_active_parameter_count}'\n \
                model_quantization='{model_quantization}'\n \
                model_language='{model_language}'\n \
                model_release_stage='{model_release_stage}'")

        # TODO: support "sparse" for embedding models (if we ever publish them) and also:
        # NOTE: "dense" is default and is not currently included in the model name
        if args.partner == SUPPORTED_PARTNERS.OLLAMA:

            partner_model_base = ""

            # Establish Granite version for Ollama:

            # Strip "v" from semver.
            model_version = model_version.replace("v", "")

            # Note: Special casing legacy names for Ollama ONLY
            # For "x.0" versions it was decided to leave off the minor version (i.e., ".0")
            if model_version.endswith(MINOR_VERSION_POINT_ZERO):
                # HACK: for original g4.0 preview we used the ".0"
                if model_release_stage != SUPPORTED_RELEASE_STAGES.PREVIEW:
                    model_major_version = model_version.removesuffix(MINOR_VERSION_POINT_ZERO)
                    partner_model_base = f"{model_family}{model_major_version}"

            if partner_model_base == "":
                partner_model_base = f"{model_family}{model_version}"

            # Note: Special casing legacy names for Ollama ONLY
            # "instruct" => "dense" or "moe" depending on parameter size (implies underlying arch.)
            if (model_modality == SUPPORTED_MODEL_MODALITIES.INSTRUCT or
                model_modality == SUPPORTED_MODEL_MODALITIES.BASE ):
                if (model_version == SUPPORTER_MODEL_VERSIONS.GRANITE_3_0 or
                    model_version == SUPPORTER_MODEL_VERSIONS.GRANITE_3_1):
                    if (model_parameter_size == SUPPORTED_MODEL_PARAMETER_SIZES.B1 or
                        model_parameter_size == SUPPORTED_MODEL_PARAMETER_SIZES.B3):
                        model_layer_desc = MODEL_LAYER_DESCRIPTIVE_TYPES.MOE
                    elif (model_parameter_size == SUPPORTED_MODEL_PARAMETER_SIZES.B2 or
                        model_parameter_size == SUPPORTED_MODEL_PARAMETER_SIZES.B8):
                        model_layer_desc = MODEL_LAYER_DESCRIPTIVE_TYPES.DENSE

            # Append model layer description if it exists
            if model_layer_desc != "":
                partner_model_base = ollama_append_attribute(partner_model_base, model_layer_desc)

            # Append modality
            # Note: Special case for models that are "instruct" or "base" language models
            # where we leave off the modality classifier (i.e., "language" is implied)
            if model_modality != "" and (model_modality != SUPPORTED_MODEL_MODALITIES.BASE and
                model_modality != SUPPORTED_MODEL_MODALITIES.INSTRUCT):
                partner_model_base = f"{partner_model_base}-{model_modality}"

            # Append build/release stage
            if model_release_stage != "":
                partner_model_base = ollama_append_attribute(partner_model_base, model_release_stage)

            # TODO: determine if we need to append this for partner models:
            # if model_active_parameter_count is not None:
            #     partner_model_base += f"-{model_active_parameter_count}"

            # ==========================POST MODEL_NAME_SEP==============================

            # For Ollama the model name-modality/version defines the model
            # everything that follows are model attributes that appear after a colon ":"
            partner_model_name = f"{partner_model_base}{MODEL_NAME_SEP}"

            if model_parameter_size:
                partner_model_name = ollama_append_attribute(partner_model_name, model_parameter_size)

            if model_abstract_size:
                partner_model_name = ollama_append_attribute(partner_model_name, model_abstract_size)

            if model_arch_desc:
                partner_model_name = ollama_append_attribute(partner_model_name, model_arch_desc)

            # HACK: for one-time exception to g4.0 "preview" model names which used instruct
            if model_modality == "" and (model_version == SUPPORTER_MODEL_VERSIONS.GRANITE_4_0 and
                model_release_stage == SUPPORTED_RELEASE_STAGES.PREVIEW):
                    model_modality = SUPPORTED_MODEL_MODALITIES.INSTRUCT

            # for "instruct" and "base" language models, we add the modality classifier after the
            # parameter size to follow established conventions (if not the default quant.).
            if ((model_modality == SUPPORTED_MODEL_MODALITIES.BASE or
                model_modality == SUPPORTED_MODEL_MODALITIES.INSTRUCT) and
                not args.default_quant):
                partner_model_name = ollama_append_attribute(partner_model_name, model_modality)

            # Note: used to trick registry into applying parameter size tag
            if not args.default_quant:
                if model_language:
                    partner_model_name = ollama_append_attribute(partner_model_name, model_language)

                if model_quantization:
                    partner_model_name = ollama_append_attribute(partner_model_name, model_quantization)

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