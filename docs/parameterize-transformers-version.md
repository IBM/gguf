# Parameterizing HuggingFace Transformers Version

## Overview

This document explains how to control the HuggingFace Transformers version used in GGUF conversion workflows. This is important because:

1. **Granite 4.0 models** may require newer transformers versions with custom architecture support
2. **Different model families** may have different transformers requirements
3. **Version control** allows testing with specific transformers versions without code changes

## Implementation

### 1. Reusable Workflow Parameters

Both reusable conversion workflows now accept a `transformers_version` input parameter:

#### `reusable-convert-hf-vision-to-f16-gguf.yml`
```yaml
inputs:
  transformers_version:
    type: string
    required: true
    description: "HuggingFace Transformers version to install (e.g., '4.52.1' or '4.57.3')"
```

#### `reusable-convert-hf-to-bf16-gguf.yml`
```yaml
inputs:
  transformers_version:
    type: string
    required: true
    description: "HuggingFace Transformers version to install (e.g., '4.52.1' or '4.57.3')"
```

**Key points:**
- Parameter is **required** (not optional)
- No default value - must be explicitly provided by parent workflow
- Ensures version is always intentionally specified

### 2. Parent Workflow Configuration

In parent workflows (e.g., `granite-4.0-release-test.yml`), define transformers versions as environment variables:

```yaml
env:
  # HuggingFace Transformers versions
  # Granite 4.0 models use transformers 4.57.3
  TRANSFORMERS_VERSION_LANGUAGE: "4.57.3"
  TRANSFORMERS_VERSION_VISION: "4.57.3"
  TRANSFORMERS_VERSION_GUARDIAN: "4.57.3"
  TRANSFORMERS_VERSION_EMBEDDING: "4.57.3"
  TRANSFORMERS_VERSION_DOCLING: "4.57.3"
```

### 3. Environment-Setup Job Outputs

Since the `env` context is not available in workflow call `with` blocks, we pass versions through the environment-setup job:

```yaml
environment-setup:
  outputs:
    transformers_version_language: "${{ steps.set-vars.outputs.transformers_version_language }}"
    transformers_version_vision: "${{ steps.set-vars.outputs.transformers_version_vision }}"
    # ... other outputs
  steps:
    - name: Set environment variables in GitHub output
      id: set-vars
      run: |
        echo "transformers_version_language=$TRANSFORMERS_VERSION_LANGUAGE" >> "$GITHUB_OUTPUT"
        echo "transformers_version_vision=$TRANSFORMERS_VERSION_VISION" >> "$GITHUB_OUTPUT"
        # ... other variables
```

### 4. Passing Version to Reusable Workflows

#### For Language Models:
```yaml
language-convert-hf-to-f16-gguf:
  needs: [ environment-setup, language-create-hf-repos ]
  uses: IBM/gguf/.github/workflows/reusable-convert-hf-to-bf16-gguf.yml@main
  with:
    debug: ${{ needs.environment-setup.outputs.debug == 'true' }}
    enable_language_jobs: ${{ needs.environment-setup.outputs.enable_language_jobs == 'true' }}
    repo_id: ${{ matrix.repo_id }}
    transformers_version: ${{ needs.environment-setup.outputs.transformers_version_language }}
    # ... other parameters
```

#### For Vision Models:
```yaml
convert-hf-llava-to-f16-gguf:
  needs: [ environment-setup, vision-create-hf-repos, check-vision-llama-cpp-support ]
  uses: IBM/gguf/.github/workflows/reusable-convert-hf-vision-to-f16-gguf.yml@main
  with:
    debug: ${{ needs.environment-setup.outputs.debug == 'true' }}
    enable_vision_jobs: ${{ needs.environment-setup.outputs.enable_vision_jobs == 'true' }}
    repo_id: ${{ matrix.repo_id }}
    transformers_version: ${{ needs.environment-setup.outputs.transformers_version_vision }}
    # ... other parameters
```

**Important:** The `env` context cannot be used directly in workflow call `with` blocks. Environment variables must be passed through job outputs.

## Usage Examples

### Example 1: Granite 4.0 with Specific Version

```yaml
# granite-4.0-release-test.yml
env:
  # Granite 4.0 models use transformers 4.57.3
  TRANSFORMERS_VERSION_LANGUAGE: "4.57.3"
  TRANSFORMERS_VERSION_VISION: "4.57.3"
  TRANSFORMERS_VERSION_GUARDIAN: "4.57.3"
  TRANSFORMERS_VERSION_EMBEDDING: "4.57.3"
  TRANSFORMERS_VERSION_DOCLING: "4.57.3"
```

### Example 2: Granite 3.3 with Specific Version

```yaml
# granite-3.3-release-test.yml
env:
  # Granite 3.3 models use transformers 4.52.1
  TRANSFORMERS_VERSION_LANGUAGE: "4.52.1"
  TRANSFORMERS_VERSION_VISION: "4.52.1"
  TRANSFORMERS_VERSION_GUARDIAN: "4.52.1"
  TRANSFORMERS_VERSION_EMBEDDING: "4.52.1"
  TRANSFORMERS_VERSION_DOCLING: "4.52.1"
```

### Example 3: Testing with Specific Version

To test a specific transformers version:

1. **Update the parent workflow:**
   ```yaml
   env:
     TRANSFORMERS_VERSION_VISION: "4.59.0"  # Test new version
   ```

2. **Run the workflow** - it will use the specified version

3. **No code changes needed** in reusable workflows

### Example 4: Per-Model Version Control

For fine-grained control, you could extend this to use the collection mapping:

```json
{
    "repo_name": "granite-4.0-3b-vision",
    "transformers_version": "4.58.0",
    "llama_cpp_supported": false
}
```

Then create a script similar to `get_vision_config_path.py` to retrieve the version.

## Installation Process

The workflows install transformers as follows:

```yaml
- name: Install Python dependencies
  run: |
    pip install -r ./llama.cpp/requirements/requirements-convert_hf_to_gguf.txt
    pip uninstall --yes transformers
    pip install transformers==${{ inputs.transformers_version }}
    echo "✅ Installed transformers version: ${{ inputs.transformers_version }}"
    pip list
```

**Key steps:**
1. Install llama.cpp requirements (includes transformers)
2. Uninstall the default transformers version
3. Install the specified version
4. Log the installed version
5. List all packages for verification

## Version Format

Transformers versions should be specified **without the 'v' prefix**:

- ✅ **Correct**: `"4.57.3"`, `"4.52.1"`
- ❌ **Avoid**: `"v4.57.3"` (may cause issues with pip)

Use the standard semantic version format for consistency.

## Benefits

1. **Flexibility**: Different model families can use different transformers versions
2. **Testing**: Easy to test new transformers versions without code changes
3. **Compatibility**: Ensures models use compatible transformers versions
4. **Documentation**: Clear which version is used for each model family
5. **Rollback**: Easy to revert to previous versions if issues arise

## Workflow Changes Summary

### Modified Files:

1. **`.github/workflows/reusable-convert-hf-vision-to-f16-gguf.yml`**
   - Added `transformers_version` input parameter (required, no default)
   - Removed hardcoded `HF_TRANSFORMERS_VERSION` env var
   - Updated install commands to use `${{ inputs.transformers_version }}`
   - Added logging for installed version

2. **`.github/workflows/reusable-convert-hf-to-bf16-gguf.yml`**
   - Added `transformers_version` input parameter (required, no default)
   - Removed hardcoded `HF_TRANSFORMERS_VERSION` env var
   - Updated install commands to use `${{ inputs.transformers_version }}`
   - Added logging for installed version

3. **`.github/workflows/granite-4.0-release-test.yml`**
   - Added `TRANSFORMERS_VERSION_*` environment variables (all set to "4.57.3")
   - Added environment-setup outputs for transformers versions
   - Updated workflow calls to pass `transformers_version` parameter

4. **`.github/workflows/granite-3.3-release-test.yml`**
   - Added `TRANSFORMERS_VERSION_*` environment variables (all set to "4.52.1")

## Implementation Status

✅ **Complete:**
- Reusable workflows accept required `transformers_version` parameter
- Granite 4.0 workflow configured with version 4.57.3
- Granite 3.3 workflow configured with version 4.52.1
- Language and vision workflow calls updated with `transformers_version`
- Environment-setup job passes versions through outputs
- Documentation updated

⚠️ **Pending:**
- Guardian, embedding, and docling workflow calls need `transformers_version` parameter added
- Other parent workflows (granite-3.0, granite-3.1, granite-3.2) need similar updates
- Testing to verify correct versions are installed

## Next Steps

1. **Complete remaining workflow calls** in Granite 4.0 and 3.3:
   - Add `transformers_version` to guardian conversion calls
   - Add `transformers_version` to embedding conversion calls
   - Add `transformers_version` to docling conversion calls

2. **Update other parent workflows** (granite-3.0, granite-3.1, granite-3.2, etc.)

3. **Test the workflows** to ensure versions are correctly installed

4. **Monitor for transformers updates** and adjust versions as needed

## Troubleshooting

### Issue: Wrong transformers version installed

**Check:**
- Workflow logs show: `✅ Installed transformers version: X.X.X`
- Verify the version matches your configuration

**Solution:**
- Update the `TRANSFORMERS_VERSION_*` variable in parent workflow
- Re-run the workflow

### Issue: Model conversion fails with transformers error

**Possible causes:**
- Model requires newer transformers version
- Custom architecture not supported in current version

**Solution:**
- Check model's HuggingFace page for transformers requirements
- Update `TRANSFORMERS_VERSION_*` to required version
- If architecture is unsupported, set `llama_cpp_supported: false` in collection mapping

## Related Documentation

- [Conditional Testing for llama.cpp Support](./llama-cpp-support-conditional-testing.md)
- [Vision Config Dynamic Loading](../README.md)
- [HuggingFace Transformers Releases](https://github.com/huggingface/transformers/releases)

## Questions?

For questions or issues:
- Check workflow logs for transformers version confirmation
- Verify version format (with or without 'v' prefix)
- Consult HuggingFace Transformers documentation for version compatibility