# Embedding Similarity Thresholds Configuration

## Overview

The embedding model BVT (Build Verification Tests) use cosine similarity to verify that embedding models correctly capture semantic relationships. The tests compare:

1. **Similar sentences** - Should have HIGH similarity (e.g., "AI was founded in 1956" vs "AI started in the 1950s")
2. **Dissimilar sentences** - Should have LOW similarity (e.g., "AI was founded in 1956" vs "I enjoy pizza")

## Problem

Quantized models, especially smaller models with short test sentences, can exhibit more variance in their embeddings. A hardcoded threshold of `0.4` for dissimilar sentences was too strict for some models like `granite-embedding-30m-english`, causing false test failures.

## Solution

We've implemented a **per-model configurable threshold system** that allows each embedding model to have custom similarity thresholds based on its characteristics.

### Configuration File

Thresholds are defined in `resources/json/latest/hf_collection_mapping_gguf.json` for each embedding model:

```json
{
    "type": "model",
    "family": "embedding",
    "version": "3.3",
    "repo_name": "granite-embedding-30m-english",
    "default_quant": "f16",
    "similarity_threshold_high": 0.6,
    "similarity_threshold_low": 0.5
}
```

**Fields:**
- `similarity_threshold_high`: Minimum similarity for "similar" sentences (default: 0.6)
- `similarity_threshold_low`: Maximum similarity for "dissimilar" sentences (default: 0.4)

### Script: get_similarity_thresholds.py

A new Python script reads the configuration and returns model-specific thresholds:

```bash
# Get thresholds for a specific model
python3 scripts/get_similarity_thresholds.py ibm-granite/granite-embedding-30m-english

# Output: 0.6 0.5
```

**Features:**
- Extracts repo name from full repo ID
- Returns space-separated thresholds for easy bash parsing
- Falls back to defaults if model not found in config
- Supports custom default values via CLI arguments

### Workflow Integration

The reusable workflow `reusable-bvt-embedding-quantized-models-gguf.yml` now:

1. **Checks out the config file** and script during sparse checkout
2. **Dynamically sets thresholds** before running similarity tests:
   ```yaml
   - name: set-similarity-thresholds
     run: |
       THRESHOLDS=$(python3 ./scripts/get_similarity_thresholds.py "${{ inputs.repo_id }}" --verbose)
       THRESHOLD_HIGH=$(echo $THRESHOLDS | awk '{print $1}')
       THRESHOLD_LOW=$(echo $THRESHOLDS | awk '{print $2}')
       echo "SIMILARITY_THRESHOLD_HIGH=$THRESHOLD_HIGH" >> $GITHUB_ENV
       echo "SIMILARITY_THRESHOLD_LOW=$THRESHOLD_LOW" >> $GITHUB_ENV
   ```
3. **Uses the dynamic thresholds** in similarity tests

## Configuring Thresholds for New Models

When adding a new embedding model, consider:

1. **Model size**: Smaller models (e.g., 30M parameters) may need more lenient thresholds
2. **Quantization**: Heavily quantized models may have more variance
3. **Test sentences**: Short sentences may show more variance than longer ones

### Recommended Thresholds

| Model Size | Quantization | High Threshold | Low Threshold |
|------------|--------------|----------------|---------------|
| < 50M      | Q4_K_M or lower | 0.6 | 0.5 |
| 50M - 200M | Q4_K_M or lower | 0.6 | 0.4 |
| > 200M     | Q4_K_M or lower | 0.6 | 0.4 |
| Any        | F16/BF16 | 0.6 | 0.4 |

### Example: Adding a New Model

```json
{
    "type": "model",
    "family": "embedding",
    "version": "4.0",
    "repo_name": "granite-embedding-new-model",
    "default_quant": "f16",
    "similarity_threshold_high": 0.6,
    "similarity_threshold_low": 0.45
}
```

## Testing

Test the script locally:

```bash
# Test with verbose output
python3 scripts/get_similarity_thresholds.py granite-embedding-30m-english --verbose

# Test fallback behavior
python3 scripts/get_similarity_thresholds.py non-existent-model --verbose

# Test with custom defaults
python3 scripts/get_similarity_thresholds.py some-model --default-high 0.7 --default-low 0.3
```

## Benefits

1. **Flexibility**: Each model can have appropriate thresholds
2. **Maintainability**: Thresholds are centralized in one config file
3. **Backward compatibility**: Falls back to sensible defaults
4. **Transparency**: Thresholds are logged during test execution
5. **Reusability**: Same config file used across all workflows

## Related Files

- `resources/json/latest/hf_collection_mapping_gguf.json` - Configuration file
- `scripts/get_similarity_thresholds.py` - Threshold extraction script
- `.github/workflows/reusable-bvt-embedding-quantized-models-gguf.yml` - Workflow using thresholds
- `scripts/test_embedding_similarity.py` - Similarity testing script

## Future Enhancements

Potential improvements:
- Add per-quantization thresholds (e.g., different thresholds for Q4_K_M vs F16)
- Support test-sentence-specific thresholds
- Add threshold validation in CI
- Create threshold tuning tools based on empirical data