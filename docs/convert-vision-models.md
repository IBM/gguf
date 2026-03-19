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

### Granite 4.x+ Vision Models

**Important Note**: Granite 4 vision models use the `Granite4VisionForConditionalGeneration` architecture, which requires custom code found in the model repository. This architecture is not currently supported by llama.cpp's conversion script or HuggingFace Transformers' standard AutoModel classes.

**Current Status**:
- ❌ Conversion is **not currently possible** with the existing llama.cpp tooling
- 🔄 Built-in support may be added to both llama.cpp and HuggingFace Transformers in the future (no specific dates available)
- ✅ The workflow includes architecture validation to detect this issue early and provide clear error messages

The workflow will:
1. **Architecture Validation**: Check if the model architecture is supported by the installed transformers version
2. **Early Failure**: Stop processing if the architecture is not supported, saving time and resources
3. **Clear Messaging**: Provide detailed error messages explaining the compatibility issue

## Workflow Configuration

### Input Parameters

- `repo_id`: HuggingFace repository ID (e.g., `ibm-granite/granite-3.2-2b-vision`)
- `transformers_version`: HuggingFace Transformers version (default: `4.52.1`)
- `enable_vision_jobs`: Must be set to `true` to run vision conversion jobs
- `debug`: Enable debug mode to show detailed architecture information on validation failure

### Output Files

For **Granite 3.x models**, the workflow produces two GGUF files:

1. **mmproj-model-f16.gguf**: Visual encoder in F16 precision
2. **{model-name}-bf16.gguf**: Language model in BF16 precision

Both files are uploaded to the target HuggingFace repository.

For **Granite 4.x models**, the workflow will fail during architecture validation with a clear error message.

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

### Granite 4.x+ Vision Models

**Manual conversion is not currently possible** for Granite 4 vision models due to the custom architecture requirements. The workflow will automatically detect this and fail with a clear error message during the architecture validation step.

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

## Troubleshooting

### Error: "Model architecture not supported"

**For Granite 4 vision models**: This is expected. The `Granite4VisionForConditionalGeneration` architecture is not currently supported by llama.cpp or standard HuggingFace Transformers AutoModel classes.

**For other models**:
1. Check if you're using the correct transformers version
2. Update the `transformers_version` input parameter to a newer version
3. Consult the [HuggingFace transformers documentation](https://huggingface.co/docs/transformers/en/model_doc/auto) for architecture support

### Error: "Tensor dimensions not divisible by 32"

This occurs when trying to quantize the visual encoder. Granite vision models use SigLIP as the visual encoder, which has tensor dimensions that are not divisible by 32.

**Solution**: Keep the visual encoder in F16 precision (do not quantize).

## Best Practices

1. **Always use F16 for visual encoders**: Do not quantize mmproj models
2. **Use BF16 for language models**: Provides good balance of quality and size
3. **Verify transformers version**: Use the version specified in the workflow (default: 4.52.1)
4. **Test converted models**: Always validate converted models work correctly before deployment
5. **Keep both files together**: The mmproj and LLM files must be used together
6. **Enable debug mode**: Use `debug: true` in workflow inputs to see detailed architecture information on failures

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