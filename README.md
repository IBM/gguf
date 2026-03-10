# gguf

This repository provides an automated CI/CD process to convert, test and deploy IBM Granite models, in safetensor format, from the `ibm-granite` organization to IBM GGUF versions (with various supported quantizations) within model repositories respectively named with the `-GGUF` extension.  These GGUF model repositories are also included to the [Granite Quantized Model](https://huggingface.co/collections/ibm-granite/granite-quantized-models) collection for convenience.

#### Topic index

- [Target IBM models for format conversion](#target-ibm-models-for-format-conversion)
  - [Supported IBM Granite models (GGUF)](#supported-ibm-granite-models-gguf)
    - [Language](#language)
    - [Guardian](#guardian)
    - [Vision](#vision)
    - [Embedding](#embedding-dense)
- [GGUF Conversion & Quantization](#gguf-conversion--quantization)
- [GGUF Verification Testing](#gguf-verification-testing)
- [References](#references)
- [Releasing GGUF model conversions & quantizations](#releasing-gguf-model-conversions--quantizations)

---

### Target IBM models for format conversion

Format conversions (i.e., GGUF) and  quantizations will only be provided for  model repositories hosted within the official `ibm-granite` organization.

Additionally, only a select set of IBM models from these orgs. will be converted based upon the following general criteria:

- The IBM GGUF model can be supported by local or hosted model provider service that is an IBM partner.
    - *For example, [Ollama](https://ollama.com/), [LM Studio](https://lmstudio.ai/) or a hosted service such as [Replicate](https://replicate.com/).*

    This typically means the model's architecture is supported by the the following projects/libraries:
    - [llama.cpp](https://github.com/ggml-org/llama.cpp)
    - [Hugging Face Transformers](https://github.com/huggingface/transformers)

- The GGUF model is referenced by a public blog, tutorial, demo, or other public use case.
    - Specifically, if the model is referenced in an  IBM [Granite Snack Cookbook](https://github.com/ibm-granite-community/granite-snack-cookbook)

Select quantizations of a model will only be made available when:

- **Small form-factor** is justified:
    - *e.g., Reduced model size intended running locally on small form-factor devices such as watches and mobile devices.*
- **Performance** provides significant benefit without compromising on accuracy (or enabling hallucination).

#### Supported IBM Granite models (GGUF)

Specifically, the following Granite model repositories are currently supported in GGUF format (by collection) with listed:

###### Language

Typically, this model category includes "instruct" models.

| Source Repo. ID | HF (llama.cpp) Architecture | Target Repo. ID |
| --- | --- | --- |
| ibm-granite/granite-3.2-2b-instruct | GraniteForCausalLM (gpt2) | ibm-research |
| ibm-granite/granite-3.2-8b-instruct | GraniteForCausalLM (gpt2) | ibm-research |

- Supported quantizations: `fp16`, `Q2_K`, `Q3_K_L`, `Q3_K_M`, `Q3_K_S`, `Q4_0`, `Q4_1`, `Q4_K_M`, `Q4_K_S`, `Q5_0`, `Q5_1`, `Q5_K_M`, `Q5_K_S`, `Q6_K`, `Q8_0`

###### Guardian

| Source Repo. ID | HF (llama.cpp) Architecture | Target HF Org. |
| --- | --- | --- |
| ibm-granite/granite-guardian-3.2-3b-a800m | GraniteMoeForCausalLM (granitemoe) | ibm-research |
| ibm-granite/granite-guardian-3.2-5b | GraniteMoeForCausalLM (granitemoe) | ibm-research |

- Supported quantizations: `fp16`, `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`

###### Vision

| HF (llama.cpp) Architecture | Source Repo. ID | Target HF Org. |
| --- | --- | --- |
| ibm-granite/granite-vision-3.2-2b | GraniteForCausalLM (granite), LlavaNextForConditionalGeneration | ibm-research |

- Supported quantizations: `fp16`, `Q4_K_M`, `Q5_K_M`, `Q8_0`

###### Embedding (dense)

| Source Repo. ID | HF (llama.cpp) Architecture | Target HF Org. |
| --- | --- | --- |
| ibm-granite/granite-embedding-30m-english | Roberta (roberta-bpe) | ibm-research |
| ibm-granite/granite-embedding-125m-english | Roberta (roberta-bpe) | ibm-research |
| ibm-granite/granite-embedding-107m-multilingual | Roberta (roberta-bpe) | ibm-research |
| ibm-granite/granite-embedding-278m-multilingual | Roberta (roberta-bpe) | ibm-research |

- Supported quantizations: `fp16`, `Q8_0`

**Note**: Sparse model architecture (i.e., HF `RobertaMaskedLM`) is not currently supported; therefore, there is no conversion for `ibm-granite/granite-embedding-30m-sparse`.

###### RAG LoRA support**

- LoRA support is currently in plan (no date).

---

### GGUF Conversion & Quantization

The GGUF format is defined in the [GGUF specification](https://github.com/ggerganov/gguf/blob/main/spec.md). The specification describes the structure of the file, how it is encoded, and what information is included.

Currently, the primary means to convert from HF SafeTensors format to GGUF will be the canonical llama.cpp tool `convert-hf-to-gguf.py`.

for example:

```
python llama.cpp/convert-hf-to-gguf.py ./<model_repo> --outfile output_file.gguf --outtype q8_0
```

#### Alternatives

##### Ollama CLI (future)

- https://github.com/ollama/ollama/blob/main/docs/import.md#quantizing-a-model

    ```
    $ ollama create --quantize q4_K_M mymodel
    transferring model data
    quantizing F16 model to Q4_K_M
    creating new layer sha256:735e246cc1abfd06e9cdcf95504d6789a6cd1ad7577108a70d9902fef503c1bd
    creating new layer sha256:0853f0ad24e5865173bbf9ffcc7b0f5d56b66fd690ab1009867e45e7d2c4db0f
    writing manifest
    success
    ```

**Note**: The Ollama CLI tool only supports a subset of quantizations:
    - (rounding): `q4_0`, `q4_1`, `q5_0`, `q5_1`, `q8_0`
    - k-means: `q3_K_S`, `q3_K_M`, `q3_K_L`, `q4_K_S`, `q4_K_M`, `q5_K_S`, `q5_K_M`, `q6_K`

##### Hugging Face endorsed tool "ggml-org/gguf-my-repo"

- https://huggingface.co/spaces/ggml-org/gguf-my-repo

**Note**:
- Similar to Ollama CLI, the web UI supports only a subset of quantizations.

---

### GGUF Verification Testing

As a baseline, each converted model MUST successfully be run in the following providers:

##### llama.cpp testing

[llama.cpp](https://github.com/ggerganov/llama.cpp) - As the core implementation of the GGUF format which is either a direct dependency or utilized as forked code in most all downstream GGUF providers, testing is essential. Specifically, testing to verify the model can be hosted using the `llama-server` service.
    - *See the specific section on `llama.cpp` for more details on which version is considered "stable" and how the same version will be used in both conversion and testing.*

##### Ollama testing (future)

[Ollama](https://github.com/ollama/ollama) - As a key model service provider supported by higher level frameworks and platforms (e.g., [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm), [LM Studio](https://github.com/lmstudio-ai) etc.), testing the ability to `pull` and `run` the model is essential.

**Notes**

- *The official Ollama Docker image [ollama/ollama](https://hub.docker.com/r/ollama/ollama) is available on Docker Hub.*
- Ollama does not yet support sharded GGUF models
    - "Ollama does not support this yet. Follow this issue for more info: https://github.com/ollama/ollama/issues/5245"
    - e.g., `ollama pull hf.co/Qwen/Qwen2.5-14B-Instruct-GGUF`

---

## References

- GGUF format
    - Huggingface: [GGUF](https://huggingface.co/docs/hub/gguf) - describes the format and some of the header structure.
    - llama.cpp:
        - [GGUF Quantization types (*`ggml_ftype`*)](https://github.com/ggerganov/llama.cpp/blob/master/ggml/include/ggml.h#L355) - `ggml/include/ggml.h`
        - [GGUF Quantization types (*`LlamaFileType`*)](https://github.com/ggerganov/llama.cpp/blob/master/gguf-py/gguf/constants.py#L1480) - `gguf-py/gguf/constants.py`

- GGUF Examples
    - [llama.cpp/examples/quantize](https://github.com/ggerganov/llama.cpp/tree/master/examples/quantize#quantize)

- GGUF tools
    - [GGUF-my-repo](https://huggingface.co/spaces/ggml-org/gguf-my-repo) - Hugging Face space to build your own quants. without any setup. *(ref. by llama.cpp example docs.)*
    - [CISCai/gguf-editor](https://huggingface.co/spaces/CISCai/gguf-editor) - batch conversion tool for HF model repos. GGUF models.

- llama.cpp Tutorials
    - [How to convert any HuggingFace Model to gguf file format?](https://www.geeksforgeeks.org/how-to-convert-any-huggingface-model-to-gguf-file-format/) - using the `llama.cpp/convert-hf-to-gguf.py` conversion script.

- Ollama tutorials
    - [Importing a model](https://github.com/ollama/ollama/blob/main/docs/import.md) - includes Safetensors, GGUF.
    - [Use Ollama with any GGUF Model on Hugging Face Hub](https://huggingface.co/docs/hub/en/ollama)
    - [Using Ollama models from Langchain](https://ollama.com/library/gemma2) - This example uses the `gemma2` model supported by Ollama.

---

## Releasing GGUF model conversions & quantizations

This repository uses GitHub workflows and actions to convert IBM Granite models hosted on Huggingface to GGUF format, quantize them, run build-verification tests on the resultant models and publish them to target GGUF collections in IBM owned Huggingface organizations (e.g., `ibm-research` and `ibm-granite`).

### Types of releases

There are 3 types of releases that can be performed on this repository:

1. **Test** (private) - releases GGUF models to a test (or private) repo. on Huggingface.
2. **Preview** (private) - releases GGUF models to a GGUF collection within the `ibm-granite` HF organization for time-limited access to select IBM partners (typically for pre-release testing and integration).
3. **Public** - releases GGUF models to a public GGUF collection within the `ibm-research` HF organization for general use.

**Note**: *The Huggingface (HF) term "private" means that repos. and collections created in the target HF organization are only visible to organization contributors and not visible (or hidden) from normal users.*

### Configuring a release

Prior to "triggering" release workflows, some files need to be configured depending on the release type.

#### Github secrets

Project maintainers for this repo. are able to access the secrets (tokens) that are made available to the CI/CD release workflows/actions:

[https://github.com/IBM/gguf/settings/secrets/actions](https://github.com/IBM/gguf/settings/secrets/actions)

Secrets are used to authenticate with Github and Huggingface (HF) and are already configured for the `ibm-granite` and `ibm-research` HF organizations for "preview" and "public" release types.

For "test" (or private) builds, users can fork the repo. and add a repository secret named `HF_TOKEN_TEST` with a token (value) created on their test (personal, private) HF organization account with appropriate privileges to allow write access to repos. and collections.

##### Base64 encoding

If you need to encode information for project CI GitHub workflows, please use the following macos command and assure there are no line breaks:

```
base64 -i <input_file> > <output_file>
```

#### Collection mapping files (JSON)

Each release uses a model collection mapping file that defines which models repositories along with titles, descriptions and family designations belong to that collection. Family designations allow granular control over the which model families are included in a release which allows for "staggered" releases typically by model architecture (e.g., `vision`, `embedding`, etc.).

Originally, different IBM Granite releases had their own collection mapping file; however, we now use a single collection mapping file for all releases of GGUF model formats for simpler downstream consumption:

- **Unified mapping**: (all release types) [resources/json/latest/hf_collection_mapping_gguf.json](resources/json/latest/hf_collection_mapping_gguf.json)

###### What to update

The JSON collection mapping files have the following structure using the "Public" release as an example:

```json
{
    "collections": [
        {
            "title": "Granite GGUF Models",
            "description": "GGUF-formatted versions of IBM Granite models. Licensed under the Apache 2.0 license.",
            "items": [
                {
                    "type": "model",
                    "family": "instruct",
                    "repo_name": "granite-3.3-8b-instruct"
                },
                ...
                {
                    "type": "model",
                    "family": "vision",
                    "repo_name": "granite-vision-3.2-2b"
                },
                ...
                {
                    "type": "model",
                    "family": "guardian",
                    "repo_name": "granite-guardian-3.2-3b-a800m"
                },
                ...
                {
                    "type": "model",
                    "family": "embedding",
                    "repo_name": "granite-embedding-30m-english"
                },
                ...
            ]
        }
    ]
}
```

Simple add a new object under the `items` array for each new IBM Granite repo. you want added to the corresponding (GGUF) collection.

Currently, the only HF item type supported is `model` and valid families (which have supported workflows) include: `instruct` (language), `vision`, `guardian` and `embedding`.

**Note**: If you need to change the HF collection description, please know that *HF limits this string to **150 chars.** or less*.

#### Release workflow files

Each release type has a corresponding (parent, master) workflow that configures and controls which model family (i.e., `instruct` (language), `vision`, `guardian` and `embedding`) are executed for a given GitHub (tagged) release.

For example, a `3.2` versioned release uses the following files which correspond to one of the release types (i.e., `Test`, `Preview` or `Public`):

- **Test**: [.github/workflows/granite-3.2-release-test.yml](.github/workflows/granite-3.2-release-test.yml)
- **Preview**: [.github/workflows/granite-3.2-release-preview-ibm-granite.yml](.github/workflows/granite-3.2-release-preview-ibm-granite.yml)
- **Public**: [.github/workflows/granite-3.2-release-ibm-research.yml](.github/workflows/granite-3.2-release-ibm-research.yml)

###### Workflow Environment Variables

The YAML GitHub workflow files use environment variables to control which model families are processed, which source repositories to convert, and which quantizations to generate. Below is a comprehensive guide using the `granite-4.0-tagged-test-release` workflow as an example.

**Control Variables**

These boolean flags enable or disable specific model family jobs:

```yaml
env:
  DEBUG: true                      # Enable debug output in workflows
  TRACE: false                     # Enable trace-level logging (very verbose)
  ENABLE_LANGUAGE_JOBS: false      # Process language/instruct models
  ENABLE_VISION_JOBS: false        # Process vision models
  ENABLE_GUARDIAN_JOBS: false      # Process guardian models
  ENABLE_EMBEDDING_JOBS: false     # Process embedding models
  ENABLE_DOCLING_JOBS: true        # Process docling models
```

**Target Repository Configuration**

These variables control where GGUF model repositories are uploaded and what collections to create:

```yaml
  TARGET_HF_REPO_NAME_EXT: -GGUF           # Suffix added to repo names
  TARGET_HF_REPO_OWNER: <HF org. name>           # HuggingFace organization/user
  TARGET_HF_REPO_PRIVATE: true             # true for private, false for public
  COLLECTION_CONFIG: "resources/json/latest/hf_collection_mapping_gguf.json"
```

**Artifact Configuration**

These variables control workflow artifact storage:

```yaml
  DEFAULT_ARTIFACTS_DIR: 'artifacts'       # Directory for storing artifacts
  ARTIFACT_LOGS_NAME: 'bvt-logs'          # Name for log artifacts
  ARTIFACT_RESPONSES_NAME: 'bvt-responses' # Name for response artifacts
  EXT_LOG: '.log.txt'                      # Log file extension
  EXT_RESPONSE: '.response.txt'            # Response file extension
```

**Model Family Configuration**

Each model family has two environment variables:
1. `SOURCE_*_REPOS` - List of source HuggingFace repository IDs to convert
2. `TARGET_*_QUANTIZATIONS` - List of quantization formats to generate

**Language Models (Instruct)**

```yaml
  SOURCE_LANGUAGE_REPOS: "[
      'ibm-granite/granite-4.0-8b',
      'ibm-granite/granite-4.0-8b-base'
    ]"
  TARGET_LANGUAGE_QUANTIZATIONS: "[
      'Q4_K_M',
      'Q8_0',
      'F16'
    ]"
```

**Guardian Models**

```yaml
  SOURCE_GUARDIAN_REPOS: "[
      'ibm-granite/granite-guardian-3.3-8b'
    ]"
  TARGET_GUARDIAN_QUANTIZATIONS: "[
      'Q4_K_M',
      'Q5_K_M',
      'Q6_K',
      'Q8_0'
    ]"
```

**Vision Models**

```yaml
  SOURCE_VISION_REPOS: "[
      'ibm-granite/granite-vision-3.3-2b'
    ]"
  TARGET_VISION_QUANTIZATIONS: "[
      'Q4_K_M',
      'Q5_K_M',
      'Q6_K',
      'Q8_0'
    ]"
```

**Embedding Models**

```yaml
  SOURCE_EMBEDDING_REPOS: "[
      'ibm-granite/granite-embedding-125m-english'
    ]"
  TARGET_EMBEDDING_QUANTIZATIONS: "[
      'Q8_0',
      'F16'
    ]"
```

**Docling Models**

```yaml
  SOURCE_DOCLING_REPOS: "[
      'ibm-granite/granite-docling-258M'
    ]"
  TARGET_DOCLING_QUANTIZATIONS: "[
      'Q8_0',
      'F16'
    ]"
```

**Disabling Model Families**

To disable a model family, set its repos to `'None'`:

```yaml
  SOURCE_VISION_REPOS: "[
      'None'
    ]"
  TARGET_VISION_QUANTIZATIONS: "[
      'None'
    ]"
```

**Available Quantization Types**

Common quantization formats (from highest to lowest quality/size):
- `F16` - Full 16-bit floating point (largest, highest quality)
- `Q8_0` - 8-bit quantization
- `Q6_K` - 6-bit k-quant
- `Q5_K_M`, `Q5_K_S` - 5-bit k-quant (medium/small)
- `Q4_K_M`, `Q4_K_S` - 4-bit k-quant (medium/small)
- `Q3_K_L`, `Q3_K_M`, `Q3_K_S` - 3-bit k-quant (large/medium/small)
- `Q2_K` - 2-bit quantization (smallest, lowest quality)

**Important Notes:**
- Array items must be properly indented (6 spaces from the start of the line)
- Closing bracket must be indented (4 spaces from the start of the line)
- Each repo ID must be a valid HuggingFace repository path
- The `COLLECTION_CONFIG` file must exist and contain valid JSON mapping
- Set `ENABLE_*_JOBS` to `false` to skip processing that model family entirely

### Updating Tools

#### llama.cpp

##### Automated Build Workflow (Recommended)

A GitHub Actions workflow is available to automatically build llama.cpp binaries:

1. Navigate to **Actions** → **Build llama.cpp Binaries**
2. Click **Run workflow**
3. Enter the llama.cpp version (commit hash or tag, e.g., `b6808`)
4. Optionally provide a release tag to upload binaries as release assets
5. Download the zip artifact from the workflow run or release page
6. Extract binaries to the `bin/` directory

**Benefits:**
- Consistent build environment (Ubuntu)
- Automated testing with smoke tests
- Minimal CMake flags for maximum compatibility
- Zip packaging for easy distribution
- 90-day artifact retention

For detailed usage instructions, see [Build llama.cpp Workflow Usage Guide](docs/build-llamacpp-workflow-usage.md).

##### Manual Build (Alternative)

If you prefer to build locally, clone and build the following llama.cpp binaries using these build/link flags:

###### Build intermediate CMake build files

The following command will create the proper CMake `build` files with minimal flags for maximum compatibility:

```
cmake -B build \
  -DBUILD_SHARED_LIBS=OFF \
  -DGGML_METAL=OFF \
  -DGGML_NATIVE_DEFAULT=OFF \
  -DCMAKE_CROSSCOMPILING=TRUE \
  -DGGML_NO_ACCELERATE=ON \
  -DGGML_SVE=OFF \
  -DCMAKE_C_FLAGS="-march=armv8-a -mtune=generic" \
  -DCMAKE_CXX_FLAGS="-march=armv8-a -mtune=generic"
```

**Flag Explanations:**
- `-DBUILD_SHARED_LIBS=OFF`: Build static libraries for portability
- `-DGGML_METAL=OFF`: Disable Metal GPU acceleration (prevents "Illegal instruction" errors on systems without Metal support or in virtualized environments)
- `-DGGML_NATIVE_DEFAULT=OFF`: Disable native CPU optimizations (prevents embedding CPU-specific instructions that may not be available on all target systems)
- `-DCMAKE_CROSSCOMPILING=TRUE`: Treat as cross-compilation for maximum compatibility
- `-DGGML_NO_ACCELERATE=ON`: Disable platform-specific accelerations for consistency
- `-DGGML_SVE=OFF`: Disable ARM Scalable Vector Extension (SVE) instructions (prevents "Illegal instruction" errors on older ARM CPUs that don't support SVE)
- `-DCMAKE_C_FLAGS="-march=armv8-a -mtune=generic"`: Compiler flags for C code:
  - `-march=armv8-a`: Target baseline ARMv8-A instruction set (compatible with ALL ARM64 CPUs: M1/M2/M3/M4, Graviton, etc.)
  - `-mtune=generic`: Optimize for generic ARM processors (not chip-specific), ensuring reasonable performance across all ARM64 systems
- `-DCMAKE_CXX_FLAGS="-march=armv8-a -mtune=generic"`: Compiler flags for C++ code (same as C flags above)

###### Build release binaries

Use this command to build all llama.cpp tool binaries to `build/bin` directory:

```
cmake --build build --config Release
```

###### Copy built binaries and push to `bin`

Once built locally, copy the following files from your `build/bin` directory to this repository's `bin` directory:

- llama-cli
- llama-quantize
- llama-server
- llama-mtmd-cli

**Note:** Archive old binaries to `bin/archive/$(date +%Y-%m-%d)/` before updating.

###### Manual Testing

After building or downloading llama.cpp binaries, you can test them locally with GGUF models before running full CI/CD workflows.

**Testing Language Models (Instruct)**

Use `llama-cli` to test language/instruct models with a simple prompt:

```bash
./bin/llama-cli -no-cnv \
  -m models/granite-3.3-8b-instruct-Q8_0.gguf \
  -sys "You are a helpful assistant. Please ensure responses are professional, accurate, and safe." \
  -p "Why is the sky blue according to science?" \
  -n 128 \
  --temp 0.8 \
  --verbose \
  --log-file test.log.txt 1>test.response.txt
```

**Parameters:**
- `-m`: Path to the quantized GGUF model file
- `-sys`: System prompt to set assistant behavior
- `-p`: User prompt/question
- `-n`: Maximum number of tokens to generate (128 for quick tests)
- `--temp`: Temperature for sampling (0.8 for balanced creativity)
- `--verbose`: Enable detailed logging
- `--log-file`: Save detailed logs to file
- `-no-cnv`: Disable conversation mode

**Expected output:** The response should contain scientific terms like "Rayleigh", "scatter", or "atmosphere".

**Testing Vision Models**

Use `llama-mtmd-cli` to test vision models with image inputs:

```bash
./bin/llama-mtmd-cli \
  -m models/granite-vision-3.3-2b-Q8_0.gguf \
  --mmproj models/mmproj-model-f16.gguf \
  -c 16384 \
  -p "<|user|><image>What type of flowers are in this picture?<|assistant|>" \
  --temp 0 \
  --verbose \
  --image test/images/cherry_blossom.jpg \
  --log-file test-vision.log.txt 1>test-vision.response.txt
```

**Parameters:**
- `-m`: Path to the quantized vision LLM GGUF file
- `--mmproj`: Path to the multimodal projector model (f16 format)
- `-c`: Context size (16384 for vision models)
- `-p`: Prompt with `<image>` placeholder for image insertion
- `--temp`: Temperature (0 for deterministic output in tests)
- `--image`: Path to test image file
- `--verbose`: Enable detailed logging
- `--log-file`: Save detailed logs to file

**Expected output:** The response should mention "cherry" and/or "blossoms" when analyzing the test image.

**Testing Docling Models**

Docling models use the same `llama-mtmd-cli` tool with document-specific prompts:

```bash
./bin/llama-mtmd-cli \
  -m models/granite-docling-1b-Q8_0.gguf \
  --mmproj models/mmproj-model-f16.gguf \
  -c 16384 \
  -p "<|user|><image>Extract the text from this document.<|assistant|>" \
  --temp 0 \
  --verbose \
  --image test/images/old_newspaper.png \
  --log-file test-docling.log.txt 1>test-docling.response.txt
```

**Verifying Test Results**

Check the response files for expected content:

```bash
# Check word count
wc -w test.response.txt

# Search for expected keywords
grep -i "rayleigh\|scatter\|atmosphere" test.response.txt

# View full response
cat test.response.txt
```

For vision/docling models, verify the response contains relevant image descriptions or extracted text.

### Triggering a release

This section contains the steps required to successfully "trigger" a release workflow for one or more supported Granite models families (i.e., `instruct` (language), `vision`, `guardian` and `embedding`).

1. Click the [`Releases`](https://github.com/IBM/gguf/releases) link from the right column of the repo. home page which should be the URL [https://github.com/IBM/gguf/releases](https://github.com/IBM/gguf/releases).
1. Click the "Draft a new release" button near the top of the releases page.
1. Click the "Choose a tag" drop-down menu and enter a tag name that starts with one of the following strings relative to which release type you want to "trigger":

    - **Test**: `test-v3.3` (private HF org.)
    - **Preview**: `preview-v3.3` (IBM Granite, private/hidden)
    - **Public**: `v3.3`  (IBM Granite)

    Treat these strings as "prefixes" which you must append a unique build version.  For example:

    - `v3.3-rc-01` *for a release candidate version 01 under the IBM Granite org. on Hugging Face Hub.*

1. "Create a new tag: on publish" near the bottom of the drop-down list.

1.  By convention, add the same "tag" name you created in the previous step into the "Release title" entry field.

1. Adjust the "Set as a pre-release" and "Set as the latest release" checkboxes to your desired settings.

1. Click the "Publish release" button.

At this point, you can observe the CI/CD workflows being run by the GitHub service "runners". *Please note that during heavy traffic times, assignment of a "runner" (for each workflow job) may take longer.*

To observe the CI/CD process in action, please navigate to the following URL:

- https://github.com/IBM/gguf/actions

and look for the name of the `tag` you entered for the release (above) in the workflow run title.

> [!NOTE]
> It is common to occasionally see some jobs "fail" due to network or scheduling timeout errors.  In these cases, you can go into the failed workflow run and click on the "Re-run failed jobs" button to re-trigger the failed job(s).