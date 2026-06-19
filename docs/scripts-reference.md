# Python Scripts Reference

This document provides comprehensive documentation for the Python utility scripts in the `scripts/` directory. These scripts are used throughout the CI/CD workflows for model conversion, quantization, testing, and Hugging Face Hub operations.

---

## Table of Contents

- [Hugging Face Hub Operations](#hugging-face-hub-operations)
  - [hf_file_download.py](#hf_file_downloadpy)
  - [hf_file_upload.py](#hf_file_uploadpy)
  - [hf_model_download_snapshot.py](#hf_model_download_snapshotpy)
  - [hf_model_upload.py](#hf_model_uploadpy)
  - [hf_model_file_exists.py](#hf_model_file_existspy)
  - [hf_repos_create.py](#hf_repos_createpy)
  - [hf_collections_create.py](#hf_collections_createpy)
- [Model Configuration & Validation](#model-configuration--validation)
  - [check_model_architecture_support.py](#check_model_architecture_supportpy)
  - [check_lora_adapter_needed.py](#check_lora_adapter_neededpy)
  - [get_vision_config_path.py](#get_vision_config_pathpy)
  - [is_model_quant_default.py](#is_model_quant_defaultpy)
- [Vision Model Processing](#vision-model-processing)
  - [torch_llava_save_llm.py](#torch_llava_save_llmpy)
  - [torch_llava_validate_tensors.py](#torch_llava_validate_tensorspy)
- [Testing & Validation](#testing--validation)
  - [test_regex_match_file.py](#test_regex_match_filepy)
  - [test_regex_match_file_2.py](#test_regex_match_file_2py)
  - [test_embedding_model.py](#test_embedding_modelpy)

---

## Hugging Face Hub Operations

### hf_file_download.py

Download files from Hugging Face Hub repositories with automatic retry logic.

**Usage:**
```bash
python scripts/hf_file_download.py <models_dir> <repo_id> <model_file> <hf_token> [--debug]
```

**Arguments:**
- `models_dir`: Local directory where the file will be downloaded
- `repo_id`: Hugging Face repository ID (e.g., `ibm-granite/granite-4.1-3b-GGUF`)
- `model_file`: Name of the file to download from the repository
- `hf_token`: Hugging Face API access token

**Examples:**

Download a quantized GGUF model:
```bash
python scripts/hf_file_download.py \
  ./models \
  ibm-granite/granite-4.1-3b-GGUF \
  granite-4.1-3b-Q4_K_M.gguf \
  $HF_TOKEN
```

Download a vision model quantization:
```bash
python scripts/hf_file_download.py \
  ./models \
  ibm-granite/granite-vision-4.1-4b-GGUF \
  granite-vision-4.1-4b-Q4_K_M.gguf \
  $HF_TOKEN
```

**Features:**
- Automatic retry logic (3 attempts with 5-second delays)
- Resume interrupted downloads
- Token validation
- Detailed error messages and timestamps

---

### hf_file_upload.py

Upload files to Hugging Face Hub repositories with custom commit messages.

**Usage:**
```bash
python scripts/hf_file_upload.py <local_file_path> <repo_id> <hf_token> [options]
```

**Arguments:**
- `local_file_path`: Path to the local file to upload
- `repo_id`: Hugging Face repository ID
- `hf_token`: Hugging Face API access token

**Options:**
- `--path-in-repo`: Destination path in the repository (defaults to basename of local file)
- `--repo-type`: Repository type: `model`, `dataset`, or `space` (default: `model`)
- `--commit-message`: Custom commit message for the upload
- `--debug`: Enable debug output

**Examples:**

Basic upload (filename automatically extracted):
```bash
python scripts/hf_file_upload.py \
  /path/to/granite-4.1-3b-Q4_K_M.gguf \
  ibm-granite/granite-4.1-3b-GGUF \
  $HF_TOKEN
```

Upload vision model with custom commit message:
```bash
python scripts/hf_file_upload.py \
  /path/to/granite-vision-4.1-4b-Q8_0.gguf \
  ibm-granite/granite-vision-4.1-4b-GGUF \
  $HF_TOKEN \
  --commit-message "Upload Q8_0 quantization for granite-vision-4.1-4b"
```

**Features:**
- Automatic retry logic (3 attempts with 5-second delays)
- File existence validation before upload
- File size display
- Support for model, dataset, and space repositories

---

### hf_model_download_snapshot.py

Download complete model snapshots from Hugging Face Hub with optional file filtering.

**Usage:**
```bash
python scripts/hf_model_download_snapshot.py <models_dir> <repo_org> <repo_name> [<hf_token>] [<allow_pattern>]
```

**Arguments:**
- `models_dir`: Local directory where the model will be downloaded
- `repo_org`: Repository organization (e.g., `ibm-granite`)
- `repo_name`: Repository name (e.g., `granite-4.1-3b`)
- `hf_token`: (Optional) Hugging Face API access token
- `allow_pattern`: (Optional) Pattern to filter files (e.g., `*.safetensors`)

**Examples:**

Download complete Granite 4.1 model:
```bash
python scripts/hf_model_download_snapshot.py \
  ./models \
  ibm-granite \
  granite-4.1-3b \
  $HF_TOKEN
```

Download Granite 4.0 vision model:
```bash
python scripts/hf_model_download_snapshot.py \
  ./models \
  ibm-granite \
  granite-4.0-3b-vision \
  $HF_TOKEN
```

Download Granite 3.3 vision model with pattern filter:
```bash
python scripts/hf_model_download_snapshot.py \
  ./models \
  ibm-granite \
  granite-vision-3.3-2b \
  $HF_TOKEN \
  "*.safetensors"
```

**Features:**
- Downloads all files in repository by default
- Optional file pattern filtering
- Exponential backoff retry logic (10s, 20s, 40s)
- Detailed timestamps for tracking download progress

---

### hf_model_upload.py

Upload model files to Hugging Face Hub with workflow tracking metadata.

**Usage:**
```bash
python scripts/hf_model_upload.py <repo_name> <model_file> <hf_token> <workflow_ref> <run_id>
```

**Arguments:**
- `repo_name`: Hugging Face repository ID
- `model_file`: Path to the model file to upload
- `hf_token`: Hugging Face API access token
- `workflow_ref`: GitHub workflow reference for tracking
- `run_id`: GitHub workflow run ID for tracking

**Examples:**

Upload quantized model with workflow tracking:
```bash
python scripts/hf_model_upload.py \
  ibm-granite/granite-4.1-8b-GGUF \
  granite-4.1-8b-Q4_K_M.gguf \
  $HF_TOKEN \
  ${{ github.workflow_ref }} \
  ${{ github.run_id }}
```

Upload vision model mmproj file:
```bash
python scripts/hf_model_upload.py \
  ibm-granite/granite-vision-4.1-4b-GGUF \
  mmproj-model-f16.gguf \
  $HF_TOKEN \
  ${{ github.workflow_ref }} \
  ${{ github.run_id }}
```

**Features:**
- Automatic commit message generation with workflow metadata
- Error handling for HTTP errors
- Returns commit info on success

---

### hf_model_file_exists.py

Check if a specific file exists in a Hugging Face Hub repository.

**Usage:**
```bash
python scripts/hf_model_file_exists.py <repo_id> <file_name> <hf_token>
```

**Arguments:**
- `repo_id`: Hugging Face repository ID
- `file_name`: Name of the file to check
- `hf_token`: Hugging Face API access token

**Output:**
- Prints `True` if file exists, `False` otherwise

**Examples:**

Check if Q4_K_M quantization exists:
```bash
exists=$(python scripts/hf_model_file_exists.py \
  ibm-granite/granite-4.1-3b-GGUF \
  granite-4.1-3b-Q4_K_M.gguf \
  $HF_TOKEN)
echo "File exists: $exists"
```

Check if vision model mmproj exists:
```bash
exists=$(python scripts/hf_model_file_exists.py \
  ibm-granite/granite-4.0-3b-vision-GGUF \
  mmproj-model-f16.gguf \
  $HF_TOKEN)
```

**Features:**
- Simple boolean output for shell script integration
- Error handling for HTTP errors
- Validates token before checking

---

### hf_repos_create.py

Create Hugging Face repositories based on collection configuration with validation.

**Usage:**
```bash
python scripts/hf_repos_create.py <target_owner> <collection_config> <include> <family> <private> <hf_token> [options]
```

**Arguments:**
- `target_owner`: Target HF organization owner for repository creation
- `collection_config`: Path to collection mapping JSON file
- `include`: JSON string list of repository names to include
- `family`: Granite family (e.g., `language`, `vision`, `guardian`)
- `private`: Create repository as private (`True` or `False`)
- `hf_token`: Hugging Face API access token

**Options:**
- `-x, --ext`: Optional repository name extension (e.g., `-GGUF`)
- `--verbose`: Enable verbose output
- `-d, --debug`: Enable debug output

**Examples:**

Create repositories for Granite 4.1 language models:
```bash
python scripts/hf_repos_create.py \
  ibm-granite \
  resources/json/latest/hf_collection_mapping_gguf.json \
  "['ibm-granite/granite-4.1-3b', 'ibm-granite/granite-4.1-8b']" \
  language \
  True \
  $HF_TOKEN \
  --ext -GGUF
```

Create repositories for Granite 4.0 vision models:
```bash
python scripts/hf_repos_create.py \
  ibm-granite \
  resources/json/latest/hf_collection_mapping_gguf.json \
  "['ibm-granite/granite-4.0-3b-vision']" \
  vision \
  True \
  $HF_TOKEN \
  --ext -GGUF
```

**Features:**
- Validates model names against collection configuration
- Creates repositories only for specified family
- Supports repository name extensions
- Detailed validation error messages

---

### hf_collections_create.py

Create and manage Hugging Face collections with items.

**Usage:**
```bash
python scripts/hf_collections_create.py <hf_owner> <collection_config> <family> <private> <hf_token> [options]
```

**Arguments:**
- `hf_owner`: Hugging Face organization or user
- `collection_config`: Path to collection mapping JSON file
- `family`: Granite family to create collection for
- `private`: Create collection as private (`True` or `False`)
- `hf_token`: Hugging Face API access token

**Options:**
- `--verbose`: Enable verbose output
- `-d, --debug`: Enable debug output

**Examples:**

Create collection for Granite 4.1 models:
```bash
python scripts/hf_collections_create.py \
  ibm-granite \
  resources/json/latest/hf_collection_mapping_gguf.json \
  language \
  False \
  $HF_TOKEN
```

**Features:**
- Creates collections if they don't exist
- Adds items to collections
- Supports public and private collections
- Validates collection configuration

---

## Model Configuration & Validation

### check_model_architecture_support.py

Validate that a model's architecture is supported by the installed transformers version.

**Usage:**
```bash
python scripts/check_model_architecture_support.py <model_path> [--debug]
```

**Arguments:**
- `model_path`: Path to the model directory containing config.json
- `--debug`: (Optional) Enable debug mode to show supported architectures on failure

**Exit Codes:**
- `0`: Model architecture is supported
- `1`: Model architecture is NOT supported or error occurred

**Examples:**

Check Granite 4.1 model architecture:
```bash
python scripts/check_model_architecture_support.py \
  models/ibm-granite/granite-4.1-3b
```

Check Granite 4.0 vision model with debug output:
```bash
python scripts/check_model_architecture_support.py \
  models/ibm-granite/granite-4.0-3b-vision \
  --debug
```

Check Granite 3.3 vision model:
```bash
python scripts/check_model_architecture_support.py \
  models/ibm-granite/granite-vision-3.3-2b
```

**Features:**
- Reads model config.json to extract architecture
- Checks if architecture class exists in transformers
- Shows transformers version information
- Debug mode shows filtered list of supported architectures

---

### check_lora_adapter_needed.py

Check if a model requires a LoRA adapter based on collection mapping configuration.

**Usage:**
```bash
python scripts/check_lora_adapter_needed.py --collection-mapping <file> --repo-name <name>
```

**Arguments:**
- `--collection-mapping, -c`: Path to the hf_collection_mapping_gguf.json file
- `--repo-name, -r`: Repository name to search for (e.g., `granite-vision-3.3-2b`)

**Output:**
- Prints `true` if LoRA adapter is needed, `false` otherwise

**Examples:**

Check if Granite 3.3 vision model needs LoRA:
```bash
LORA_NEEDED=$(python scripts/check_lora_adapter_needed.py \
  --collection-mapping resources/json/latest/hf_collection_mapping_gguf.json \
  --repo-name granite-vision-3.3-2b)
echo "LoRA needed: $LORA_NEEDED"
```

Check Granite 4.0 vision model:
```bash
LORA_NEEDED=$(python scripts/check_lora_adapter_needed.py \
  -c resources/json/latest/hf_collection_mapping_gguf.json \
  -r granite-4.0-3b-vision)
```

**Features:**
- Searches through collection configuration
- Returns boolean string for shell script compatibility
- Handles missing or invalid JSON gracefully

---

### get_vision_config_path.py

Extract the vision_config path for a model from the collection mapping configuration.

**Usage:**
```bash
python scripts/get_vision_config_path.py <collection_mapping_file> <repo_id> [default_path]
```

**Arguments:**
- `collection_mapping_file`: Path to the hf_collection_mapping_gguf.json file
- `repo_id`: Repository ID (can be `org/repo` or just `repo`)
- `default_path`: (Optional) Default path to return if vision_config is not found

**Output:**
- Prints the vision_config path if found, otherwise the default_path or empty string

**Examples:**

Get vision config for Granite 3.3 vision model:
```bash
VISION_CONFIG=$(python scripts/get_vision_config_path.py \
  resources/json/latest/hf_collection_mapping_gguf.json \
  ibm-granite/granite-vision-3.3-2b)
echo "Vision config: $VISION_CONFIG"
```

Get vision config for Granite 3.2 with default:
```bash
VISION_CONFIG=$(python scripts/get_vision_config_path.py \
  resources/json/latest/hf_collection_mapping_gguf.json \
  granite-vision-3.2-2b \
  resources/json/granite-3.2/vision_config.json)
```

**Features:**
- Handles both full repo IDs and repo names
- Returns custom vision config path when specified
- Falls back to default path if provided

---

### is_model_quant_default.py

Check if a quantization is the default for a specific model.

**Usage:**
```bash
python scripts/is_model_quant_default.py <collection_config> --model-name <name> --quantization <quant>
```

**Arguments:**
- `collection_config`: Path to the hf_collection_mapping_gguf.json file
- `--model-name, -m`: Model repository name (e.g., `granite-4.1-3b`)
- `--quantization, -q`: Quantization name (e.g., `Q4_K_M`, `f16`)

**Output:**
- Prints `true` if quantization is the default, `false` otherwise

**Examples:**

Check if Q4_K_M is default for Granite 4.1:
```bash
is_default=$(python scripts/is_model_quant_default.py \
  resources/json/latest/hf_collection_mapping_gguf.json \
  --model-name granite-4.1-3b \
  --quantization Q4_K_M)
```

Check if Q8_0 is default for Granite 4.0 vision:
```bash
is_default=$(python scripts/is_model_quant_default.py \
  resources/json/latest/hf_collection_mapping_gguf.json \
  -m granite-4.0-3b-vision \
  -q Q8_0)
```

**Features:**
- Case-insensitive comparison
- Returns boolean string for shell integration
- Validates against collection configuration

---

## Vision Model Processing

### torch_llava_save_llm.py

Extract and save the language model component from a vision model (LLaVA-style architecture).

**Usage:**
```bash
python scripts/torch_llava_save_llm.py <source_repo> <target_repo>
```

**Arguments:**
- `source_repo`: Path to source vision model directory
- `target_repo`: Path to target directory for extracted LLM

**Examples:**

Extract LLM from Granite 3.3 vision model:
```bash
python scripts/torch_llava_save_llm.py \
  models/ibm-granite/granite-vision-3.3-2b \
  granite_vision_llm
```

Extract LLM from Granite 3.2 vision model:
```bash
python scripts/torch_llava_save_llm.py \
  models/ibm-granite/granite-vision-3.2-2b \
  granite_vision_llm
```

**Features:**
- Uses AutoModelForImageTextToText for loading
- Extracts language_model component
- Saves both tokenizer and model
- Handles size mismatches gracefully with `ignore_mismatched_sizes=True`

**Note:** This script is used for Granite 3.x vision models that use the LLaVA surgery approach. Granite 4.x vision models use direct conversion with `--mmproj` flag.

---

### torch_llava_validate_tensors.py

Validate CLIP and projector tensors extracted from vision models.

**Usage:**
```bash
python scripts/torch_llava_validate_tensors.py <clip_path> <projector_path> <output_keys_file>
```

**Arguments:**
- `clip_path`: Path to the CLIP tensor file (llava.clip)
- `projector_path`: Path to the projector tensor file (llava.projector)
- `output_keys_file`: Path to output file for projector keys

**Examples:**

Validate Granite 3.3 vision tensors:
```bash
python scripts/torch_llava_validate_tensors.py \
  models/ibm-granite/granite-vision-3.3-2b/llava.clip \
  models/ibm-granite/granite-vision-3.3-2b/llava.projector \
  projector_keys.txt
```

**Features:**
- Validates tensor file existence
- Extracts and saves projector keys
- Used in vision model conversion pipeline

---

## Testing & Validation

### test_regex_match_file.py

Test if a regex pattern matches content in a file.

**Usage:**
```bash
python scripts/test_regex_match_file.py <regex_pattern> <test_file>
```

**Arguments:**
- `regex_pattern`: The regex pattern to search for
- `test_file`: Path to the file to search within

**Output:**
- Prints `True` if pattern matches, `False` otherwise

**Examples:**

Test BVT response for vision model keywords:
```bash
matched=$(python scripts/test_regex_match_file.py \
  "(cherry|blossoms)+" \
  granite-vision-4.1-4b-Q4_K_M-llama-mtmd-cli.response.txt)
echo "Pattern matched: $matched"
```

Test for specific model output:
```bash
matched=$(python scripts/test_regex_match_file.py \
  "granite" \
  model_output.txt)
```

**Features:**
- Simple regex matching
- File reading with error handling
- Boolean output for shell integration

---

### test_regex_match_file_2.py

Test if a file contains at least two words from a comma-separated list.

**Usage:**
```bash
python scripts/test_regex_match_file_2.py <test_file> <word_list>
```

**Arguments:**
- `test_file`: Path to the file to search
- `word_list`: Comma-separated list of words to search for

**Output:**
- Prints `True` if at least 2 unique words are found, `False` otherwise

**Examples:**

Test BVT response for multiple keywords:
```bash
matched=$(python scripts/test_regex_match_file_2.py \
  granite-vision-4.1-4b-Q4_K_M-llama-mtmd-cli.response.txt \
  "cherry,blossoms,flowers")
echo "Multiple keywords matched: $matched"
```

Test vision model output:
```bash
matched=$(python scripts/test_regex_match_file_2.py \
  model_response.txt \
  "image,picture,photo,visual")
```

**Features:**
- Case-insensitive matching
- Requires at least 2 unique matches
- Prints match details for debugging
- Boolean output for shell integration

---

### test_embedding_model.py

Test Granite embedding models using sparse sentence transformer implementation.

**Usage:**
```bash
python scripts/test_embedding_model.py <model_name_or_path> [test_sentence] [max_tokens] [device] [config_path]
```

**Arguments:**
- `model_name_or_path`: Path to the embedding model
- `test_sentence`: (Optional) Sentence to encode (default: "Artificial intelligence was founded as an academic discipline in 1956.")
- `max_tokens`: (Optional) Maximum number of tokens to return (default: 20)
- `device`: (Optional) Device to use: `cpu` or `cuda` (default: `cpu`)
- `config_path`: (Optional) Path to model config.json

**Examples:**

Test Granite embedding model with default sentence:
```bash
python scripts/test_embedding_model.py \
  models/ibm-granite/granite-embedding-30m-english
```

Test with custom sentence and device:
```bash
python scripts/test_embedding_model.py \
  models/ibm-granite/granite-embedding-125m-english \
  "Machine learning is a subset of artificial intelligence" \
  20 \
  cuda
```

Test with config path:
```bash
python scripts/test_embedding_model.py \
  models/ibm-granite/granite-embedding-30m-english \
  "Natural language processing" \
  15 \
  cpu \
  models/ibm-granite/granite-embedding-30m-english/config.json
```

**Features:**
- Implements sparse sentence transformer
- Supports CPU and CUDA devices
- Returns top-k token expansions with weights
- Validates output format
- Useful for BVT testing of embedding models

---

## Environment Variables Used in Workflows

The scripts reference these common environment variables from GitHub Actions workflows:

- `$HF_TOKEN` or `${{ secrets.HF_TOKEN_IBM_GRANITE }}`: Hugging Face API token
- `${{ github.workflow_ref }}`: GitHub workflow reference for tracking
- `${{ github.run_id }}`: GitHub workflow run ID for tracking
- `$COLLECTION_CONFIG`: Path to collection mapping JSON (typically `resources/json/latest/hf_collection_mapping_gguf.json`)

## Common Model Examples

### Granite 4.1 Models
- Language: `ibm-granite/granite-4.1-3b`, `ibm-granite/granite-4.1-8b`
- Vision: `ibm-granite/granite-vision-4.1-4b`
- Guardian: `ibm-granite/granite-guardian-4.1-8b`
- Quantizations: `Q4_K_M`, `Q8_0`

### Granite 4.0 Models
- Language: `ibm-granite/granite-4.0-1b`, `ibm-granite/granite-4.0-h-1b`
- Vision: `ibm-granite/granite-4.0-3b-vision`
- Quantizations: `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`

### Granite 3.3 Models
- Vision: `ibm-granite/granite-vision-3.3-2b`
- Quantizations: `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`

### Granite 3.2 Models
- Vision: `ibm-granite/granite-vision-3.2-2b`
- Quantizations: `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`

## See Also

- [Main README](../README.md) - Overview and getting started
- [Build llama.cpp Workflow Usage](build-llamacpp-workflow-usage.md) - Building llama.cpp binaries
- [Convert Vision Models](convert-vision-models.md) - Vision model conversion guide
- [Collection Mapping Configuration](../resources/json/latest/hf_collection_mapping_gguf.json) - Model configuration reference

---

## Scripts Requiring argparse Migration

The following scripts currently use `sys.argv` directly and should be updated to use `argparse` for better argument parsing, help messages, and error handling:

1. `array_append_values.py`
2. `hf_collections_repos_delete.py`
3. `hf_file_delete.py`
4. `hf_model_download_snapshot.py`
5. `hf_model_file_exists.py`
6. `hf_model_upload.py`
7. `hf_repo_list_files.py`
8. `test_regex_match_file.py`
9. `test_regex_match_file_2.py`
10. `torch_llava_save_llm.py`
11. `torch_llava_validate_tensors.py`

**Note:** These scripts are marked for update to standardize argument parsing across the codebase and improve maintainability.
