#!/usr/bin/env python3
"""
Check if a model's architecture is supported by the installed transformers version.

This script reads a model's config.json and checks if its architecture is available
in the currently installed HuggingFace transformers library. This helps identify
compatibility issues before attempting model conversion.

Usage:
    python check_model_architecture_support.py <model_path> [--debug]

Arguments:
    model_path: Path to the model directory containing config.json
    --debug: Enable debug mode to show full list of supported architectures on failure

Exit codes:
    0: Model architecture is supported
    1: Model architecture is NOT supported or error occurred
"""

import sys
import json
from pathlib import Path


def get_supported_architectures():
    """Get list of supported model architectures from transformers."""
    try:
        import transformers

        # Get all classes from transformers that end with common model suffixes
        model_classes = []
        for name in dir(transformers):
            if any(name.endswith(suffix) for suffix in [
                'ForCausalLM', 'ForConditionalGeneration', 'Model',
                'ForSequenceClassification', 'ForTokenClassification',
                'ForQuestionAnswering', 'ForMaskedLM', 'ForVision2Seq'
            ]):
                model_classes.append(name)

        return sorted(model_classes)
    except Exception:
        return []


def check_architecture_support(model_path: str, debug: bool = False) -> tuple[bool, str, str]:
    """
    Check if model architecture is supported by installed transformers.

    Args:
        model_path: Path to the model directory containing config.json
        debug: If True, show full list of supported architectures on failure

    Returns:
        Tuple of (is_supported, architecture_name, message)
    """
    config_path = Path(model_path) / "config.json"

    if not config_path.exists():
        return False, "unknown", f"❌ Config file not found: {config_path}"

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        return False, "unknown", f"❌ Failed to read config.json: {e}"

    # Get architecture from config
    architectures = config.get("architectures", [])
    if not architectures:
        return False, "unknown", "❌ No architectures found in config.json"

    architecture = architectures[0]

    # Try to import the architecture from transformers
    try:
        import transformers
        transformers_version = transformers.__version__

        # Try to get the model class
        if hasattr(transformers, architecture):
            model_class = getattr(transformers, architecture)
            return True, architecture, (
                f"✅ Model architecture '{architecture}' is supported\n"
                f"   Transformers version: {transformers_version}\n"
                f"   Model class: {model_class.__module__}.{model_class.__name__}"
            )
        else:
            message = (
                f"❌ Model architecture '{architecture}' is NOT supported\n"
                f"   Transformers version: {transformers_version}\n"
                f"   Model path: {model_path}\n"
            )

            # Only show filtered list in debug mode
            if debug:
                supported = get_supported_architectures()
                if supported:
                    # Filter to architectures starting with the same letter
                    first_letter = architecture[0].upper()
                    filtered = [arch for arch in supported if arch[0].upper() == first_letter]

                    if filtered:
                        filtered_list = "\n      - ".join(filtered)
                        message += (
                            f"\n"
                            f"   Supported architectures starting with '{first_letter}' ({len(filtered)} found):\n"
                            f"      - {filtered_list}"
                        )
                    else:
                        message += (
                            f"\n"
                            f"   No supported architectures found starting with '{first_letter}'"
                        )

            return False, architecture, message
    except ImportError as e:
        return False, architecture, f"❌ Failed to import transformers: {e}"
    except Exception as e:
        return False, architecture, f"❌ Error checking architecture support: {e}"


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python check_model_architecture_support.py <model_path> [--debug]", file=sys.stderr)
        sys.exit(1)

    model_path = sys.argv[1]
    debug = len(sys.argv) == 3 and sys.argv[2] == '--debug'

    is_supported, architecture, message = check_architecture_support(model_path, debug)

    print(message)

    if is_supported:
        print(f"\n✅ VALIDATION PASSED: Model can proceed to conversion")
        sys.exit(0)
    else:
        print(f"\n❌ VALIDATION FAILED: Model conversion will likely fail")
        print(f"   Architecture: {architecture}")
        print(f"   Recommendation: Update transformers version or use a different model")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
