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

Granite 4.x and later vision models use the **direct conversion with --mmproj flag** approach:

1. **mmproj Conversion**: Converts the visual encoder directly using `convert_hf_to_gguf.py --mmproj`
2. **LLM Conversion**: Converts the language model using `convert_hf_to_gguf.py`

## Custom Code Requirement (Granite 4.x+)

### The Problem

Granite 4 vision models include custom Python code in their HuggingFace repository that defines the model architecture. This custom code must be executed to properly load the model. Without allowing this code to run, the conversion fails with:

```
WARNING:hf-to-gguf:Failed to load model config from models/ibm-granite/granite-4.0-3b-vision:
The repository models/ibm-granite/granite-4.0-3b-vision contains custom code which must be
executed to correctly load the model. You can inspect the repository content at
https://hf.co/models/ibm-granite/granite-4.0-3b-vision.
Please pass the argument `trust_remote_code=True` to allow custom code to be run.
```

### The Solution

The `--trust-remote-code` flag must be passed to `convert_hf_to_gguf.py` for Granite 4+ vision models:

```bash
python convert_hf_to_gguf.py /path/to/model \
  --outfile output.gguf \
  --outtype f16 \
  --mmproj \
  --trust-remote-code \
  --verbose
```

### Security Considerations

The `--trust-remote-code` flag allows execution of arbitrary Python code from the model repository. This is safe for official IBM Granite models but should be used with caution for untrusted sources:

- ✅ **Safe**: Official IBM Granite models from `ibm-granite` organization
- ⚠️ **Caution**: Third-party or community models
- ❌ **Avoid**: Unknown or untrusted sources

Always inspect the repository content before enabling `trust_remote_code` for non-official models.

## Workflow Configuration

### Input Parameters

- `repo_id`: HuggingFace repository ID (e.g., `ibm-granite/granite-4.0-3b-vision`)
- `transformers_version`: HuggingFace Transformers version (default: `4.52.1`)
- `enable_vision_jobs`: Must be set to `true` to run vision conversion jobs

### Output Files

The workflow produces two GGUF files:

1. **mmproj-model-f16.gguf**: Visual encoder in F16 precision
2. **{model-name}-bf16.gguf**: Language model in BF16 precision

Both files are uploaded to the target HuggingFace repository.

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

### Granite 4+ Vision Models

```bash
# 1. Download the model
python scripts/hf_model_download_snapshot.py models ibm-granite granite-4.0-3b-vision $HF_TOKEN

# 2. Convert visual encoder (mmproj)
python llama.cpp/convert_hf_to_gguf.py models/ibm-granite/granite-4.0-3b-vision \
  --outfile mmproj-model-f16.gguf \
  --outtype f16 \
  --mmproj \
  --trust-remote-code \
  --verbose

# 3. Convert language model
python llama.cpp/convert_hf_to_gguf.py models/ibm-granite/granite-4.0-3b-vision \
  --outfile granite-4.0-3b-vision-bf16.gguf \
  --outtype bf16 \
  --trust-remote-code \
  --verbose
```

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

## Troubleshooting

### Error: "contains custom code which must be executed"

**Solution**: Add `--trust-remote-code` flag to the conversion command.

### Error: "Model architecture not supported"

**Possible causes**:
1. Missing `--trust-remote-code` flag (Granite 4+)
2. Incorrect transformers version
3. Model architecture not yet supported by llama.cpp

**Solution**:
- Ensure `--trust-remote-code` is used for Granite 4+ models
- Check transformers version compatibility
- Verify llama.cpp version supports the model architecture

### Error: "Tensor dimensions not divisible by 32"

This occurs when trying to quantize the visual encoder. Granite vision models use SigLIP as the visual encoder, which has tensor dimensions that are not divisible by 32.

**Solution**: Keep the visual encoder in F16 precision (do not quantize).

## Best Practices

1. **Always use F16 for visual encoders**: Do not quantize mmproj models
2. **Use BF16 for language models**: Provides good balance of quality and size
3. **Verify transformers version**: Use the version specified in the workflow (default: 4.52.1)
4. **Test converted models**: Always validate converted models work correctly before deployment
5. **Keep both files together**: The mmproj and LLM files must be used together

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