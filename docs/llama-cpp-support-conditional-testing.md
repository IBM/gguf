# Conditional Testing for llama.cpp Support

## Overview

This document explains how the GGUF conversion workflow handles models with architectures that are not yet supported by llama.cpp. This is particularly relevant for newer Granite 4.0 vision models that use custom HuggingFace Transformer architectures.

## Problem Statement

Granite 4.0 vision models (e.g., `granite-4.0-3b-vision`) use new HuggingFace Transformer architectures with custom Python classes defined in the model repository. These architectures are not yet supported by llama.cpp for inference, which means:

- ✅ **Conversion to GGUF format works** - The model can be converted and quantized
- ❌ **Inference testing fails** - BVT and UAT tests cannot run until llama.cpp adds support

## Solution

We've implemented a conditional testing system that:

1. **Allows conversion and quantization** to proceed for all models
2. **Automatically skips BVT/UAT testing** for unsupported models
3. **Can be easily enabled** once llama.cpp adds support (just update the JSON config)

## Implementation

### 1. Collection Mapping Flag

In `resources/json/latest/hf_collection_mapping_gguf.json`, models can specify llama.cpp support:

```json
{
    "type": "model",
    "family": "vision",
    "repo_name": "granite-4.0-3b-vision",
    "default_quant": "q8_0",
    "projector_model": "mmproj-model-f16.gguf",
    "llama_cpp_supported": false
}
```

**Key points:**
- `llama_cpp_supported`: `false` = skip BVT/UAT, `true` or omitted = run tests
- Default is `true` if not specified (backward compatible)
- Only affects testing, not conversion/quantization

### 2. Support Check Script

`scripts/is_model_llama_cpp_supported.py` checks if a model is supported:

```bash
python scripts/is_model_llama_cpp_supported.py \
    resources/json/latest/hf_collection_mapping_gguf.json \
    ibm-granite/granite-4.0-3b-vision
```

**Returns:**
- `"true"` - Model is supported, run all tests
- `"false"` - Model is not supported, skip BVT/UAT

### 3. Workflow Integration

The workflow includes these jobs:

#### a. Check Support (runs early)
```yaml
check-vision-llama-cpp-support:
  needs: [ environment-setup, vision-create-hf-repos ]
  runs-on: ubuntu-latest
  strategy:
    matrix:
      repo_id: ${{ fromJson(needs.environment-setup.outputs.source_vision_repos) }}
  steps:
    - name: Check llama.cpp support
      run: |
        SUPPORTED=$(python ./scripts/is_model_llama_cpp_supported.py ...)
        if [ "$SUPPORTED" = "true" ]; then
          echo "✅ BVT/UAT testing will be enabled"
        else
          echo "⚠️ BVT/UAT testing will be skipped"
        fi
```

#### b. Conditional BVT Check
```yaml
check-bvt-vision-support:
  needs: [ environment-setup, quantize-vision-llm-and-upload-gguf ]
  runs-on: ubuntu-latest
  outputs:
    should_run_bvt: ${{ steps.check.outputs.supported }}
  steps:
    - name: Check if BVT should run
      id: check
      run: |
        SUPPORTED=$(python ./scripts/is_model_llama_cpp_supported.py ...)
        echo "supported=$SUPPORTED" >> $GITHUB_OUTPUT
```

#### c. Conditional BVT Execution
```yaml
bvt-vision-quantized-gguf-models:
  needs: [ environment-setup, check-bvt-vision-support ]
  if: ${{ always() && needs.check-bvt-vision-support.outputs.should_run_bvt == 'true' }}
  uses: IBM/gguf/.github/workflows/reusable-bvt-vision-quantized-models-gguf.yml@main
```

## Workflow Behavior

### For Supported Models (e.g., granite-vision-3.3-2b)

```
1. ✅ Create HF repos
2. ✅ Check support → "true"
3. ✅ Convert to GGUF
4. ✅ Quantize models
5. ✅ Check BVT support → "true"
6. ✅ Run BVT tests
7. ✅ Run UAT tests (if enabled)
8. ✅ Create collections
```

### For Unsupported Models (e.g., granite-4.0-3b-vision)

```
1. ✅ Create HF repos
2. ⚠️ Check support → "false" (logged, continues)
3. ✅ Convert to GGUF
4. ✅ Quantize models
5. ⚠️ Check BVT support → "false"
6. ⏭️ Skip BVT tests
7. ⏭️ Skip UAT tests
8. ✅ Create collections
```

**Result:** Models are converted and uploaded, but not tested until llama.cpp support is added.

## Enabling Support Later

When llama.cpp adds support for a model architecture:

1. **Update the collection mapping:**
   ```json
   {
       "repo_name": "granite-4.0-3b-vision",
       "llama_cpp_supported": true  // Change from false to true
   }
   ```

2. **Re-run the workflow** - BVT/UAT tests will now execute

3. **No code changes needed** - The system automatically detects the change

## Benefits

1. **Non-blocking:** New models can be released even if llama.cpp doesn't support them yet
2. **Automatic:** No manual workflow modifications needed per model
3. **Clear feedback:** Logs clearly indicate why tests are skipped
4. **Easy to enable:** Single JSON change enables testing when ready
5. **Backward compatible:** Existing models without the flag default to supported

## Testing the Feature

### Test with unsupported model:
```bash
# Should return "false"
python scripts/is_model_llama_cpp_supported.py \
    resources/json/latest/hf_collection_mapping_gguf.json \
    ibm-granite/granite-4.0-3b-vision
```

### Test with supported model:
```bash
# Should return "true"
python scripts/is_model_llama_cpp_supported.py \
    resources/json/latest/hf_collection_mapping_gguf.json \
    ibm-granite/granite-vision-3.3-2b
```

### Test with model not in mapping:
```bash
# Should return "true" (default)
python scripts/is_model_llama_cpp_supported.py \
    resources/json/latest/hf_collection_mapping_gguf.json \
    ibm-granite/some-new-model
```

## Future Enhancements

Potential improvements:

1. **Architecture detection:** Automatically detect unsupported architectures from model config
2. **Support matrix:** Track which llama.cpp versions support which architectures
3. **Notification system:** Alert when llama.cpp adds support for pending models
4. **Partial testing:** Run only conversion tests, skip inference tests

## Related Files

- `resources/json/latest/hf_collection_mapping_gguf.json` - Model configuration
- `scripts/is_model_llama_cpp_supported.py` - Support check script
- `.github/workflows/granite-4.0-release-test.yml` - Workflow implementation
- `.github/workflows/granite-3.3-release-test.yml` - Reference workflow (all models supported)

## Questions?

For questions or issues with this feature, please refer to:
- GitHub Issues for bug reports
- Pull Requests for enhancements

## BVT Instruct Testing

### Overview

The BVT instruct workflow tests language models using two binaries:
- **llama-cli**: Available in all llama.cpp versions
- **llama-completion**: Available in llama.cpp b8742 and higher (preferred for cleaner output)

### Test Configuration

**Environment Variables:**
```yaml
LLAMA_SYSTEM_PROMPT: "You are a helpful assistant. Please ensure responses are professional, accurate, and safe."
LLAMA_REQUEST_PROMPT: "Why is the sky blue according to science?"
LLAMA_REQUEST_N_PREDICT: 128  # Number of tokens to generate
LLAMA_CLI_TEMP: 0.8           # Temperature for generation
LLAMA_RESPONSE_WORDS: "Rayleigh,scatter,atmosphere"  # Words to validate in response
```

### llama-completion Test (b8742+)

**Command:**
```bash
./bin/b8742/llama-completion \
  -m ./models/granite-3.0-2b-instruct-Q4_K_M.gguf \
  -p "<|start_of_role|>system<|end_of_role|>You are a helpful assistant. Please ensure responses are professional, accurate, and safe.<|end_of_text|><|start_of_role|>user<|end_of_role|>Why is the sky blue according to science?<|end_of_text|><|start_of_role|>assistant<|end_of_role|>" \
  -n 128 \
  --temp 0.8 \
  -no-cnv \
  --no-display-prompt \
  --log-file granite-3.0-2b-instruct-Q4_K_M-llama-completion.log.txt \
  1>granite-3.0-2b-instruct-Q4_K_M-llama-completion.response.txt
```

**Flags:**
- `-m`: Model file path
- `-p`: Prompt with chat template formatting
- `-n`: Number of tokens to predict (128 for faster tests)
- `--temp`: Temperature for generation (0.8 for balanced creativity)
- `-no-cnv`: Disable conversation mode (no ASCII banner, cleaner output)
- `--no-display-prompt`: Suppress prompt echo in output
- `--log-file`: Write verbose logs to separate file
- `1>`: Redirect stdout (response) to file

**Why these flags:**
- `-no-cnv`: Prevents conversation mode overhead and ASCII banner display
- `--no-display-prompt`: Keeps output clean with only the model's response
- Separate log file: Allows debugging without cluttering response output

### llama-cli Test (all versions)

**Command:**
```bash
./bin/b8742/llama-cli \
  -m ./models/granite-3.0-2b-instruct-Q4_K_M.gguf \
  -p "<|start_of_role|>system<|end_of_role|>You are a helpful assistant. Please ensure responses are professional, accurate, and safe.<|end_of_text|><|start_of_role|>user<|end_of_role|>Why is the sky blue according to science?<|end_of_text|><|start_of_role|>assistant<|end_of_role|>" \
  -n 128 \
  --temp 0.8 \
  -cnv \
  --log-file granite-3.0-2b-instruct-Q4_K_M-llama-cli.log.txt \
  1>granite-3.0-2b-instruct-Q4_K_M-llama-cli.response.txt
```

**Flags:**
- `-m`: Model file path
- `-p`: Prompt with chat template formatting
- `-n`: Number of tokens to predict (128 for faster tests)
- `--temp`: Temperature for generation (0.8 for balanced creativity)
- `-cnv`: Enable conversation mode (default for llama-cli)
- `--log-file`: Write verbose logs to separate file
- `1>`: Redirect stdout (response) to file

**Note:** llama-cli always runs in conversation mode and displays an ASCII banner. Use llama-completion for cleaner output when available.

### Response Validation

Both tests validate responses contain at least 2 of 3 expected words:
- "Rayleigh"
- "scatter"
- "atmosphere"

**Validation script:**
```bash
python ./scripts/test_regex_match_file_2.py \
    "granite-3.0-2b-instruct-Q4_K_M-llama-completion.response.txt" \
    "Rayleigh,scatter,atmosphere"
```

Returns `True` if at least 2 words are found (case-insensitive), `False` otherwise.

### Version Detection

The workflow automatically detects if llama-completion is available:

```bash
LLAMACPP_BUILD_TAG="b8742"
if [[ "$LLAMACPP_BUILD_TAG" =~ ^b([0-9]+)$ ]]; then
  VERSION_NUM="${BASH_REMATCH[1]}"
  if [ "$VERSION_NUM" -lt 8742 ]; then
    # Disable llama-completion test for older builds
    TEST_LLAMA_COMPLETION=false
  fi
fi
```

**Result:**
- Builds < b8742: Only llama-cli test runs
- Builds ≥ b8742: Both llama-cli and llama-completion tests run
- This documentation for implementation details