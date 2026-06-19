# Converting Vision Models to GGUF Format

## Overview

This document describes the process for converting Granite vision models from HuggingFace format to GGUF format for use with llama.cpp. Vision models require special handling compared to text-only models due to their multimodal architecture.

## Vision Model Architecture

Granite vision models consist of two main components:

1. **Visual Encoder (mmproj)**: Processes images and projects them into the language model's embedding space
2. **Language Model (LLM)**: Processes text and the projected image embeddings

Both components must be converted separately and then used together during inference.

## Conversion Workflow

The conversion process is handled by the `reusable-convert-hf-vision-to-f16-gguf.yml` workflow, which automatically detects the Granite version and uses the appropriate conversion method.

### Granite 3.x Vision Models

Granite 3.x vision models use the **llava surgery tooling** approach:

1. **Tensor Separation**: Uses `llava_surgery_v2.py` to separate CLIP and projector tensors
2. **Image Encoder Conversion**: Converts the visual encoder using `convert_image_encoder_to_gguf.py`
3. **LLM Extraction**: Extracts the language model from the vision model
4. **LLM Conversion**: Converts the LLM to GGUF format using `convert_hf_to_gguf.py`

### Granite 4.0 and 4.1 Vision Models

**Support Status**: ✅ Fully supported as of llama.cpp build **b9533** and later (currently using **b9704**)

Granite 4.0 and 4.1 vision models use a **unified conversion approach** with `convert_hf_to_gguf.py` and the `--mmproj` flag, which is different from the Granite 3.x llava surgery approach.

**Key Differences Between 4.0 and 4.1**:

| Aspect | Granite 4.0 | Granite 4.1 |
|--------|-------------|-------------|
| **Model Naming** | `granite-4.0-*-vision` (e.g., `granite-4.0-3b-vision`) | `granite-vision-4.1-*` (e.g., `granite-vision-4.1-4b`) |
| **Transformers Version** | 5.8.0+ | 5.8.0+ |
| **llama.cpp Build Tag** | b9704 (minimum: b9533) | b9704 (minimum: b9533) |
| **LoRA Adapter** | ✅ Required | ❌ Not required |
| **Jinja Template** | ✅ Uses jinja chat template | ✅ Uses jinja chat template |
| **Conversion Method** | Direct with `--mmproj` flag | Direct with `--mmproj` flag |

**Conversion Process**:

Both Granite 4.0 and 4.1 vision models follow the same base conversion workflow:

1. **Download Model**: Download the full model snapshot from HuggingFace
2. **Convert Visual Encoder (mmproj)**: Use `convert_hf_to_gguf.py` with `--mmproj` flag to extract and convert the visual encoder to F16 precision
3. **Convert Language Model**: Use `convert_hf_to_gguf.py` to convert the LLM component to BF16 precision
4. **Convert LoRA Adapter** (Granite 4.0 only): Use `convert_lora_to_gguf.py` to convert the LoRA adapter to F16 precision

**LoRA Adapter Requirement**:

- **Granite 4.0**: Requires a LoRA adapter for proper functionality. The adapter is automatically detected and converted by the workflow.
- **Granite 4.1**: Does not require a LoRA adapter.

**Jinja Template Usage**:

Both model versions use jinja chat templates for proper prompt formatting. When testing with `llama-mtmd-cli`, you must include the `--jinja` flag to enable template processing.

## Workflow Configuration

### Input Parameters

- `repo_id`: HuggingFace repository ID (e.g., `ibm-granite/granite-3.2-2b-vision`)
- `transformers_version`: HuggingFace Transformers version (default: `4.52.1`)
- `enable_vision_jobs`: Must be set to `true` to run vision conversion jobs
- `debug`: Enable debug mode to show detailed architecture information on validation failure

### Output Files

The workflow produces the following GGUF files:

**For Granite 3.x models**:
1. **mmproj-model-f16.gguf**: Visual encoder in F16 precision
2. **{model-name}-bf16.gguf**: Language model in BF16 precision

**For Granite 4.0 models**:
1. **mmproj-model-f16.gguf**: Visual encoder in F16 precision
2. **{model-name}-bf16.gguf**: Language model in BF16 precision
3. **{model-name}-LoRA-F16.gguf**: LoRA adapter in F16 precision

**For Granite 4.1 models**:
1. **mmproj-model-f16.gguf**: Visual encoder in F16 precision
2. **{model-name}-bf16.gguf**: Language model in BF16 precision

All files are uploaded to the target HuggingFace repository.

## Version Detection

The workflow automatically detects the Granite version from the repository name:

```yaml
# Granite 4+ vision models use convert_hf_to_gguf.py with --mmproj flag
if [[ "$REPO_NAME" =~ granite-([4-9]|[1-9][0-9]+)\. ]]; then
  use_convert_script_with_mmproj=true
else
  # Granite 3 and earlier use llava_surgery_v2.py tooling
  use_convert_script_with_mmproj=false
fi
```

## Manual Conversion

### Granite 3.x Vision Models

```bash
# 1. Download the model
python scripts/hf_model_download_snapshot.py models ibm-granite granite-3.2-2b-vision $HF_TOKEN

# 2. Separate CLIP and projector tensors
python llama.cpp/tools/mtmd/legacy-models/llava_surgery_v2.py \
  -C -m models/ibm-granite/granite-3.2-2b-vision

# 3. Convert image encoder
mkdir visual_encoder
cp models/ibm-granite/granite-3.2-2b-vision/llava.projector visual_encoder/
cp models/ibm-granite/granite-3.2-2b-vision/llava.clip visual_encoder/pytorch_model.bin
cp resources/json/granite-3.2/vision_config.json visual_encoder/config.json

python llama.cpp/tools/mtmd/legacy-models/convert_image_encoder_to_gguf.py \
  -m visual_encoder \
  --llava-projector visual_encoder/llava.projector \
  --output-dir visual_encoder \
  --clip-model-is-vision \
  --clip-model-is-siglip \
  --image-mean 0.5 0.5 0.5 \
  --image-std 0.5 0.5 0.5

# 4. Extract and convert LLM
python scripts/torch_llava_save_llm.py \
  models/ibm-granite/granite-3.2-2b-vision \
  granite_vision_llm

python llama.cpp/convert_hf_to_gguf.py granite_vision_llm \
  --outfile granite-3.2-2b-vision-bf16.gguf \
  --outtype bf16 \
  --verbose
```

### Granite 4.0 Vision Models

```bash
# 1. Download the model
python scripts/hf_model_download_snapshot.py models ibm-granite granite-4.0-3b-vision $HF_TOKEN

# 2. Convert visual encoder (mmproj) with --mmproj flag
mkdir visual_encoder
python llama.cpp/convert_hf_to_gguf.py models/ibm-granite/granite-4.0-3b-vision \
  --outfile visual_encoder/mmproj-model-f16.gguf \
  --outtype f16 \
  --mmproj \
  --verbose

# 3. Convert language model
python llama.cpp/convert_hf_to_gguf.py models/ibm-granite/granite-4.0-3b-vision \
  --outfile granite-4.0-3b-vision-bf16.gguf \
  --outtype bf16 \
  --verbose

# 4. Convert LoRA adapter (required for Granite 4.0)
python llama.cpp/convert_lora_to_gguf.py models/ibm-granite/granite-4.0-3b-vision \
  --outfile granite-4.0-3b-vision-LoRA-F16.gguf \
  --outtype f16 \
  --trust-remote-code \
  --verbose
```

### Granite 4.1 Vision Models

```bash
# 1. Download the model
python scripts/hf_model_download_snapshot.py models ibm-granite granite-vision-4.1-4b $HF_TOKEN

# 2. Convert visual encoder (mmproj) with --mmproj flag
mkdir visual_encoder
python llama.cpp/convert_hf_to_gguf.py models/ibm-granite/granite-vision-4.1-4b \
  --outfile visual_encoder/mmproj-model-f16.gguf \
  --outtype f16 \
  --mmproj \
  --verbose

# 3. Convert language model
python llama.cpp/convert_hf_to_gguf.py models/ibm-granite/granite-vision-4.1-4b \
  --outfile granite-vision-4.1-4b-bf16.gguf \
  --outtype bf16 \
  --verbose

# Note: No LoRA adapter needed for Granite 4.1
```

## Architecture Validation

The workflow includes a validation step that checks if the model's architecture is supported before attempting conversion:

```bash
python scripts/check_model_architecture_support.py <model_path> [--debug]
```

This script:
- Reads the model's `config.json` to identify the architecture
- Checks if the architecture class exists in the installed transformers library
- Provides detailed error messages with architecture name and transformers version
- In debug mode, lists all supported architectures to help identify alternatives

## BVT Testing Examples

After conversion, you can test the models using `llama-mtmd-cli` (or `llama-cli` for older builds). Both Granite 4.0 and 4.1 models require the `--jinja` flag for proper prompt formatting.

### Granite 4.0 Vision Model Testing

```bash
# Test with quantized model (e.g., Q4_K_M)
llama-mtmd-cli \
  -m models/ibm-granite/granite-4.0-3b-vision-GGUF/granite-4.0-3b-vision-Q4_K_M.gguf \
  --mmproj models/ibm-granite/granite-4.0-3b-vision-GGUF/mmproj-model-f16.gguf \
  --lora models/ibm-granite/granite-4.0-3b-vision-GGUF/granite-4.0-3b-vision-LoRA-F16.gguf \
  --image test/images/cherry_blossom.jpg \
  -p "What type of flowers are in this picture?" \
  --jinja \
  --temp 0
```

**Key parameters for Granite 4.0**:
- `-m`: Path to the quantized language model
- `--mmproj`: Path to the visual encoder (always F16)
- `--lora`: Path to the LoRA adapter (required for 4.0)
- `--image`: Path to the test image
- `-p`: User prompt (without `</image>` tag - automatically handled)
- `--jinja`: Enable jinja template processing (required)
- `--temp`: Temperature setting (0 for deterministic output)

### Granite 4.1 Vision Model Testing

```bash
# Test with quantized model (e.g., Q4_K_M)
llama-mtmd-cli \
  -m models/ibm-granite/granite-vision-4.1-4b-GGUF/granite-vision-4.1-4b-Q4_K_M.gguf \
  --mmproj models/ibm-granite/granite-vision-4.1-4b-GGUF/mmproj-model-f16.gguf \
  --image test/images/cherry_blossom.jpg \
  -p "What type of flowers are in this picture?" \
  --jinja \
  --temp 0
```

**Key parameters for Granite 4.1**:
- `-m`: Path to the quantized language model
- `--mmproj`: Path to the visual encoder (always F16)
- `--image`: Path to the test image
- `-p`: User prompt (without `</image>` tag - automatically handled)
- `--jinja`: Enable jinja template processing (required)
- `--temp`: Temperature setting (0 for deterministic output)
- **Note**: No `--lora` flag needed for 4.1

### BVT Workflow Testing

The `reusable-bvt-vision-quantized-models-gguf.yml` workflow automatically tests converted models with:
- **Test Image**: `test/images/cherry_blossom.jpg`
- **Test Prompt**: `"What type of flowers are in this picture?"`
- **Expected Response**: Contains words like "cherry" or "blossoms"
- **llama.cpp Build**: b9704 (supports both 4.0 and 4.1)

## Troubleshooting

### Error: "Model architecture not supported"

**For Granite 4.0/4.1 vision models with older versions**:
- This error occurs when using llama.cpp builds older than **b9533** or transformers versions older than **5.8.0**
- **Solution**: Update to llama.cpp build b9533 or later (recommended: b9704) and transformers 5.8.0+

**For other models**:
1. Check if you're using the correct transformers version
2. Update the `transformers_version` input parameter to a newer version
3. Consult the [HuggingFace transformers documentation](https://huggingface.co/docs/transformers/en/model_doc/auto) for architecture support

### Error: "Tensor dimensions not divisible by 32"

This occurs when trying to quantize the visual encoder. Granite vision models use SigLIP as the visual encoder, which has tensor dimensions that are not divisible by 32.

**Solution**: Keep the visual encoder in F16 precision (do not quantize).

### Missing LoRA adapter for Granite 4.0

If you get poor results or errors with Granite 4.0 models, ensure you're using the LoRA adapter:
- The LoRA adapter file should be named `{model-name}-LoRA-F16.gguf`
- Use the `--lora` flag when running `llama-mtmd-cli`
- The workflow automatically detects and converts LoRA adapters for 4.0 models

### Jinja template errors

If you get template-related errors or unexpected output:
- Always use the `--jinja` flag with both Granite 4.0 and 4.1 vision models
- Do not include `</image>` tags in your prompt - they are automatically inserted by the jinja template
- The `--image` flag automatically handles image token placement

## Best Practices

1. **Always use F16 for visual encoders**: Do not quantize mmproj models
2. **Use BF16 for language models**: Provides good balance of quality and size
3. **Verify transformers version**: Use version 5.8.0+ for Granite 4.0/4.1 vision models
4. **Use correct llama.cpp build**: Use build b9533 or later (recommended: b9704) for Granite 4.0/4.1
5. **Include LoRA adapter for Granite 4.0**: Always use the `--lora` flag when testing Granite 4.0 models
6. **Always use --jinja flag**: Required for both Granite 4.0 and 4.1 vision models
7. **Test converted models**: Always validate converted models work correctly before deployment
8. **Keep all files together**: The mmproj, LLM, and LoRA (if applicable) files must be used together
9. **Enable debug mode**: Use `debug: true` in workflow inputs to see detailed architecture information on failures

## Related Documentation

- [Build llama.cpp Workflow Usage](./build-llamacpp-workflow-usage.md)
- [Workflow Plan](./build-llamacpp-workflow-plan.md)
- [llama.cpp Vision Models Documentation](https://github.com/ggerganov/llama.cpp/tree/master/examples/llava)

## Support

For issues or questions:

1. Check workflow logs in the Actions tab
2. Review this documentation
3. Consult the [llama.cpp repository](https://github.com/ggerganov/llama.cpp)
4. Open an issue in this repository