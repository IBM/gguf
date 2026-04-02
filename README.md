# gguf

This repository provides an automated CI/CD process to convert, test and deploy IBM Granite models, in safetensor format, from the `ibm-granite` organization to IBM GGUF versions (with various supported quantizations) within model repositories respectively named with the `-GGUF` extension.  These GGUF model repositories are also included to the [Granite Quantized Model](https://huggingface.co/collections/ibm-granite/granite-quantized-models) collection for convenience.

#### Topic index

- [Criteria for IBM Granite model format conversion and quantization](#criteria-for-ibm-granite-model-format-conversion-and-quantization)
- [Supported IBM Granite models (GGUF)](#supported-ibm-granite-models-gguf)
  - [Language](#language)
  - [Guardian](#guardian)
  - [Vision](#vision)
  - [Embedding](#embedding-dense)
  - [Docling](#docling)
- [GGUF Conversion & Quantization](#gguf-conversion--quantization)
- [GGUF Verification Testing](#gguf-verification-testing)
- [Releasing GGUF model conversions & quantizations](#releasing-gguf-model-conversions--quantizations)
- [Partner Registry Build, Test & Delivery](#partner-registry-build-test--delivery)
  - [Ollama](#ollama)
  - [Docker Model Factory](#docker-model-factory)
- [References](#references)

---

### Criteria for IBM Granite model format conversion and quantization

Format conversions (i.e., GGUF) and quantizations will only be provided for model repositories hosted within the official `ibm-granite` organization.

Additionally, only a select set of IBM models from these orgs. will be converted based upon the following general criteria:

- The IBM GGUF model can be supported by a local or hosted model provider service that is an IBM partner.
    - *For example, [Ollama](https://ollama.com/), [LM Studio](https://lmstudio.ai/) or a hosted service such as [Replicate](https://replicate.com/).*

    This typically means the model's architecture is supported by the following projects/libraries:
    - [llama.cpp](https://github.com/ggml-org/llama.cpp)
    - [Hugging Face Transformers](https://github.com/huggingface/transformers)

- The GGUF model is referenced by a public blog, tutorial, demo, or other public use case.
    - Specifically, if the model is referenced in an IBM [Granite Snack Cookbook](https://github.com/ibm-granite-community/granite-snack-cookbook)

Select quantizations of a model will only be made available when:

- **Small form-factor** is justified:
    - *e.g., Reduced model size intended for running locally, especially on small form-factor devices such as watches and mobile devices.*
- **Performance** provides significant benefit without compromising on accuracy (or enabling hallucination).

---

### Supported IBM Granite models (GGUF)

Specifically, the following Granite model repositories are currently supported in GGUF format (by model type):

#### Language

Typically, this model category includes "base" and "instruct" models.

| Source Repo. ID | Architecture (HF) | Architecture Description | HF Transformers* | llama.cpp* |
| --- | --- | --- | --- | --- |
| ibm-granite/granite-3.0-2b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.0-8b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.0-1b-a400m-base | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.0-3b-a800m-base | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.0-2b-instruct | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.0-8b-instruct | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.0-1b-a400m-instruct | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.0-3b-a800m-instruct | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.1-2b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.1-8b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.1-1b-a400m-base | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.1-3b-a800m-base | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.1-2b-instruct | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.1-8b-instruct | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.1-1b-a400m-instruct | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.1-3b-a800m-instruct | GraniteMoeForCausalLM | MoE (Mixture of Experts) | | |
| ibm-granite/granite-3.2-2b-instruct | GraniteForCausalLM | Dense Transformer (gpt2) | | |
| ibm-granite/granite-3.2-8b-instruct | GraniteForCausalLM | Dense Transformer (gpt2) | | |
| ibm-granite/granite-3.3-2b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.3-8b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.3-2b-instruct | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-3.3-8b-instruct | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-4.0-tiny-preview | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-tiny-base-preview | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-350m | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-4.0-350m-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-4.0-h-350m | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-h-350m-base | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-1b | GraniteForCausalLM | Dense Transformer | 4.57.3 | b6569 |
| ibm-granite/granite-4.0-1b-base | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-4.0-h-1b | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-h-1b-base | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-micro | GraniteMoeHybridForCausalLM | Dense Transformer (3B) | | |
| ibm-granite/granite-4.0-micro-base | GraniteMoeHybridForCausalLM | Dense Transformer (3B) | | |
| ibm-granite/granite-4.0-h-micro | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer (3B) | | |
| ibm-granite/granite-4.0-h-micro-base | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer (3B) | | |
| ibm-granite/granite-4.0-h-tiny | GraniteMoeHybridForCausalLM | Hybrid MoE Mamba-2/Transformer (7B, 1B active) | | |
| ibm-granite/granite-4.0-h-tiny-base | GraniteMoeHybridForCausalLM | Hybrid MoE Mamba-2/Transformer (7B, 1B active) | | |
| ibm-granite/granite-4.0-h-small | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-h-small-base | GraniteMoeHybridForCausalLM | Hybrid Mamba-2/Transformer | | |
| ibm-granite/granite-4.0-8b | GraniteForCausalLM | Dense Transformer | | |
| ibm-granite/granite-4.0-8b-base | GraniteForCausalLM | Dense Transformer | | |

- Supported quantizations: `F16`, `Q2_K`, `Q3_K_L`, `Q3_K_M`, `Q3_K_S`, `Q4_0`, `Q4_1`, `Q4_K_M`, `Q4_K_S`, `Q5_0`, `Q5_1`, `Q5_K_M`, `Q5_K_S`, `Q6_K`, `Q8_0`

**\* Last known successful build versions:** The HF Transformers and llama.cpp columns indicate the last versions used to successfully convert, quantize, and test these models in the full release workflow.

#### Guardian

| Source Repo. ID | Architecture (HF) | Architecture Description |
| --- | --- | --- |
| ibm-granite/granite-guardian-3.0-2b | GraniteForCausalLM | Dense Transformer |
| ibm-granite/granite-guardian-3.0-8b | GraniteForCausalLM | Dense Transformer |
| ibm-granite/granite-guardian-3.1-2b | GraniteForCausalLM | Dense Transformer |
| ibm-granite/granite-guardian-3.1-8b | GraniteForCausalLM | Dense Transformer |
| ibm-granite/granite-guardian-3.2-3b-a800m | GraniteMoeForCausalLM | MoE (Mixture of Experts) |
| ibm-granite/granite-guardian-3.2-5b | GraniteMoeForCausalLM | MoE (Mixture of Experts) |
| ibm-granite/granite-guardian-3.3-8b | GraniteForCausalLM | Dense Transformer |

- Supported quantizations: `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`

#### Vision

| Source Repo. ID | Architecture (HF) | Architecture Description |
| --- | --- | --- |
| ibm-granite/granite-vision-3.2-2b | LlavaNextForConditionalGeneration (text: GraniteForCausalLM, vision: siglip_vision_model) | LlavaNext (text: Dense Transformer, vision: SigLIP) |
| ibm-granite/granite-vision-3.3-2b | LlavaNextForConditionalGeneration (text: GraniteForCausalLM, vision: siglip_vision_model) | LlavaNext (text: Dense Transformer, vision: SigLIP) |
| ibm-granite/granite-vision-3.3-2b-chart2csv-preview | LlavaNextForConditionalGeneration (text: GraniteForCausalLM, vision: siglip_vision_model) | LlavaNext (text: Dense Transformer, vision: SigLIP) |
| ibm-granite/granite-4.0-3b-vision ⚠️ | Granite4VisionForConditionalGeneration (custom model) (text: GraniteMoeHybridForCausalLM, vision: siglip_vision_model) | ❌ **Not currently supported** - Requires custom code not available in llama.cpp or HF Transformers. See [Converting Vision Models](docs/convert-vision-models.md) for details. |

- Supported quantizations: `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`, `bf16`

#### Embedding (dense)

| Source Repo. ID | Architecture (HF) | Architecture Description |
| --- | --- | --- |
| ibm-granite/granite-embedding-30m-english | Roberta | roberta-bpe |
| ibm-granite/granite-embedding-125m-english | Roberta | roberta-bpe |
| ibm-granite/granite-embedding-107m-multilingual | Roberta | roberta-bpe |
| ibm-granite/granite-embedding-278m-multilingual | Roberta | roberta-bpe |

- Supported quantizations: `f16`, `Q8_0`

**Note**: Sparse model architecture (i.e., HF `RobertaMaskedLM`) is not currently supported; therefore, there is no conversion for `ibm-granite/granite-embedding-30m-sparse`.

#### Docling

| Source Repo. ID | Architecture (HF) | Architecture Description |
| --- | --- | --- |
| ibm-granite/granite-docling-258M | Idefics3ForConditionalGeneration (text: LlamaForCausalLM, vision: idefics3_vision) | idefics3 (text: llama, vision: idefics3_vision) |

- Supported quantizations: `bf16`

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

## Releasing GGUF model conversions & quantizations

This repository uses GitHub workflows and actions to convert IBM Granite models hosted on Huggingface to GGUF format, quantize them, run build-verification tests on the resultant models and publish them to target GGUF collections in IBM owned Huggingface organizations (e.g., `ibm-research` and `ibm-granite`).

### Types of releases

There are 2 types of releases that can be performed on this repository:

1. **Test** (private) - releases GGUF models to a test (or private) repo. on Huggingface.
2. **Public** - releases GGUF models to a public GGUF collection within the `ibm-granite` HF organization for general use.

**Note**: *The Huggingface (HF) term "private" means that repos. and collections created in the target HF organization are only visible to organization contributors and not visible (or hidden) from normal users.*

### Configuring a release

Prior to "triggering" release workflows, some files need to be configured depending on the release type.

#### Github secrets

Project maintainers for this repo. are able to access the secrets (tokens) that are made available to the CI/CD release workflows/actions:

[https://github.com/IBM/gguf/settings/secrets/actions](https://github.com/IBM/gguf/settings/secrets/actions)

Secrets are used to authenticate with Github and Huggingface (HF) and are already configured for the `ibm-granite` HF organization for "public" release types.

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

##### What to update

The JSON collection mapping files have the following structure:

```json
{
    "collections": [
        {
            "title": "Granite Quantized Models",
            "description": "Quantized versions of IBM Granite models. Licensed under the Apache 2.0 license.",
            "items": [
                {
                    "type": "model",
                    "family": "instruct",
                    "repo_name": "granite-3.3-8b-instruct",
                    "default_quant": "q4_K_M"
                },
                {
                    "type": "model",
                    "family": "vision",
                    "repo_name": "granite-vision-3.3-2b",
                    "default_quant": "q8_0",
                    "projector_model": "mmproj-model-f16.gguf",
                    "vision_config": "VISION_CONFIG: resources/json/granite-3.3/vision_config.json"
                },
                {
                    "type": "model",
                    "family": "guardian",
                    "repo_name": "granite-guardian-3.3-8b",
                    "default_quant": "q6_K"
                },
                {
                    "type": "model",
                    "family": "embedding",
                    "version": "3.2",
                    "repo_name": "granite-embedding-30m-english",
                    "default_quant": "f16"
                },
                {
                    "type": "model",
                    "family": "docling",
                    "repo_name": "granite-docling-258M",
                    "default_quant": "bf16",
                    "projector_model": "mmproj-model-f16.gguf"
                },
                {
                    "type": "model",
                    "size": "mini",
                    "family": "instruct",
                    "repo_name": "granite-4.0-8b",
                    "default_quant": "q4_K_M",
                    "is_latest": true
                }
            ]
        }
    ]
}
```

Simply add a new object under the `items` array for each new IBM Granite repo. you want added to the corresponding (GGUF) collection.

###### Collection fields:

The top-level collection object contains the following fields:

- `title`: The display name of the collection (i.e., "Granite Quantized Models").
- `description`: A brief description of the collection and its contents. **Important:** Hugging Face limits collection descriptions to **150 characters or less**. Keep descriptions concise while clearly conveying the collection's purpose and licensing information.
- `items`: An array of model objects to include in the collection.

###### Item fields:

Each item represents a single source repository and contains the following fields:

*Common fields (all model types):*
- `type`: Currently only `"model"` is supported (required)
- `family`: Valid families include `instruct` (language), `vision`, `guardian`, `embedding`, and `docling` (required)
- `repo_name`: The repository name (required)
- `default_quant`: Default quantization format (e.g., `q4_K_M`, `q8_0`, `f16`, `bf16`) (required)
- `version`: Optional version identifier for models that need explicit versioning
- `size`: Abstract size category (required for models without size designation in repo name). Used by partner registries like Ollama and Docker Model Factory for standardized naming. Valid values from `get_partner_model_name.py`:
  - `nano` - Smallest models (~350M-1B parameters)
  - `micro` - Very small models (~3B parameters)
  - `tiny` - Small models (~7B parameters, 1B active for MoE)
  - `small` - Medium-small models
  - `medium` - Medium models
  - `large` - Large models
  - `mini` - Mini models (~8B parameters)
- `is_latest`: Boolean flag to mark which model should receive the `latest` tag in Docker Hub. Used by Docker Model Factory workflows to identify the primary model for a given repository. Only one model should be marked as `is_latest: true` per repository, and it must use the default quantization. Base models are excluded from receiving the `latest` tag. (optional, defaults to `false`)

*Vision/Docling-specific fields:*
- `projector_model`: Specifies the multimodal projector file (e.g., `mmproj-model-f16.gguf`) (required for vision/docling models)
- `vision_config`: Path to vision configuration JSON file (e.g., `VISION_CONFIG: resources/json/granite-3.3/vision_config.json`) (optional)

**Note:** The `size` field is used by the `get_partner_model_name.py` script to generate standardized model names for partner registries (Ollama, Docker Model Factory) when the model repository name doesn't include an explicit size designation. This ensures consistent naming conventions across different deployment platforms.

#### Release workflow files

Each release type has a corresponding (parent, master) workflow that configures and controls which model families (i.e., `language`, `vision`, `guardian`, `docling` and `embedding`) are executed for a given GitHub (tagged) release.

For example, a `3.3` versioned release uses the following files which correspond to one of the release types (i.e., `test` or `ibm-granite` for public):

- **Test**: [.github/workflows/granite-3.3-release-test.yml](.github/workflows/granite-3.3-release-test.yml)
- **Public**: [.github/workflows/granite-3.3-release-ibm-granite.yml](.github/workflows/granite-3.3-release-ibm-granite.yml)

##### Workflow Environment Variables

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

---

## Partner Registry Build, Test & Delivery

This section describes workflows and processes for building, testing, and delivering IBM Granite GGUF models to partner model registries such as Ollama and Docker Model Factory.

### Ollama

[Ollama](https://github.com/ollama/ollama) is a key model service provider supported by higher level frameworks and platforms (e.g., [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm), [LM Studio](https://github.com/lmstudio-ai) etc.). This repository provides automated workflows to build, test, and publish IBM Granite GGUF models to the Ollama registry.

#### Ollama Publish Workflows

The repository includes version-specific Ollama publish workflows (e.g., `ollama-publish-granite-3.3.yml`, `ollama-publish-granite-4.0.yml`) that orchestrate the entire process of creating and publishing models to Ollama. These workflows:

- Are triggered by Git tags (e.g., `test-ollama-3.3*`, `ollama-4.0*`) or manual workflow dispatch
- Support all model families: language/instruct, vision, guardian, embedding, and docling
- Use a matrix strategy to process multiple models and quantizations in parallel
- Call the reusable workflow `reusable-ollama-create-push-model.yml` for each model/quantization combination

**Key Workflow Configuration:**

Each workflow defines:
- `SOURCE_*_REPOS`: Arrays of Hugging Face repository IDs to process (e.g., `ibm-granite/granite-3.3-8b-instruct`)
- `SOURCE_*_QUANTIZATIONS`: Arrays of quantization formats to publish (e.g., `Q4_K_M`, `Q8_0`, `BF16`)
- `TARGET_OLLAMA_ORG`: Target Ollama organization (typically `ibm`)
- `ENABLE_*_JOBS`: Boolean flags to enable/disable specific model families
- `ENABLE_OLLAMA_PUSH`: Master switch to enable actual pushing to Ollama registry

#### Build, Test, and Release Process

The `reusable-ollama-create-push-model.yml` workflow performs the following steps for each model:

**1. Environment Setup**
- Validates Ollama credentials before starting downloads
- Generates standardized Ollama model names using `get_partner_model_name.py`
- Determines if model requires a projector (for vision/docling models)

**2. Model Download**
- Downloads quantized GGUF model from Hugging Face using `hf_file_download.py`
- Downloads multimodal projector model (f16) for vision/docling models
- Verifies file existence before proceeding

**3. Modelfile Creation**
- Customizes README with model-specific information
- Creates Ollama Modelfile using `create_ollama_model_file.py` with:
  - Model file path
  - Projector model path (if applicable)
  - License file (Apache 2.0)
  - Template file (chat format)
  - System prompt file
  - Parameters file (temperature, context size, etc.)

**4. Local Testing**
- Starts local Ollama server on macOS runner
- Creates model from Modelfile using `ollama create`
- Copies model to target organization namespace
- Verifies model creation with `ollama list`

**5. Publishing**
- Pushes model to Ollama registry using `ollama push`
- For default quantizations: creates and pushes additional tag without quantization suffix
- Tracks push timing for monitoring

**6. Cleanup**
- Stops Ollama server
- Cleans up temporary files

#### Model Naming Convention

Ollama model names are generated using the `get_partner_model_name.py` script, which:
- Converts Hugging Face model names to Ollama-compatible format
- Uses abstract size categories (nano, micro, tiny, small, medium, large, mini) from collection config
- Follows pattern: `granite{version}[-{modality}]:{size}[-{arch}][-{modality}][-{language}][-{quantization}]`
- Examples:
  - `ibm/granite3.3:8b-instruct-q4_k_m` (non-default quantization)
  - `ibm/granite3.3:8b` (default quantization, no suffix)
  - `ibm/granite3.3-vision:2b-q8_0` (vision model)
  - `ibm/granite4:nano-h` (hybrid architecture with abstract size)

#### Supported Quantizations

Ollama workflows support all standard GGUF quantizations plus the initial converted format:
- Rounding: `q4_0`, `q4_1`, `q5_0`, `q5_1`, `q8_0`
- K-means: `q2_K`, `q3_K_S`, `q3_K_M`, `q3_K_L`, `q4_K_S`, `q4_K_M`, `q5_K_S`, `q5_K_M`, `q6_K`
- Full precision: `f16`, `bf16` (initial conversion format)

**Note**: The workflow automatically appends the initial conversion quantization (typically `f16` or `bf16`) to the quantization matrix to ensure the base converted model is also published.

#### Triggering Ollama Releases

To trigger an Ollama release:

1. Ensure GGUF models are already published to Hugging Face (via standard release workflows)
2. Create a Git tag matching the workflow pattern (e.g., `ollama-4.0-rc-01`)
3. Push the tag to trigger the workflow
4. Monitor workflow progress at [https://github.com/IBM/gguf/actions](https://github.com/IBM/gguf/actions)

Alternatively, use workflow dispatch to manually trigger a release from the Actions tab.

#### Notes

- *The official Ollama Docker image [ollama/ollama](https://hub.docker.com/r/ollama/ollama) is available on Docker Hub.*
- Ollama does not yet support sharded GGUF models
    - "Ollama does not support this yet. Follow this issue for more info: https://github.com/ollama/ollama/issues/5245"
    - e.g., `ollama pull hf.co/Qwen/Qwen2.5-14B-Instruct-GGUF`
- All Ollama workflows run on macOS runners for compatibility with Ollama's native tooling
- Models are tested locally before being pushed to ensure they load correctly

### Docker Model Factory

[Docker Model Factory](https://github.com/docker/model-runner) enables packaging and distribution of GGUF models as Docker containers, making them easily deployable across different environments. This repository provides automated workflows to package, test, and publish IBM Granite GGUF models to Docker Hub.

#### Docker Package Push Workflows

The repository includes version-specific Docker package push workflows (e.g., `docker-package-push-granite-4.0-test.yml`) that orchestrate the entire process of packaging and publishing models to Docker Hub. These workflows:

- Are triggered by Git tags (e.g., `test-docker-4.0*`) or manual workflow dispatch
- Currently support language/instruct models (vision, guardian, embedding, and docling support planned)
- Use a matrix strategy to process multiple models and quantizations in parallel
- Call the reusable workflow `reusable-docker-package-push-model.yml` for each model/quantization combination

**Key Workflow Configuration:**

Each workflow defines:
- `SOURCE_*_REPOS`: Arrays of Hugging Face repository IDs to process (e.g., `ibm-granite/granite-4.0-8b`)
- `SOURCE_*_QUANTIZATIONS`: Arrays of quantization formats to publish (e.g., `Q5_K_M`, `BF16`)
- `TARGET_DOCKERHUB_NAMESPACE`: Target Docker Hub namespace (typically `ibmcom`)
- `TARGET_DOCKERHUB_REPOSITORY`: Target Docker Hub repository name
- `ENABLE_*_JOBS`: Boolean flags to enable/disable specific model families
- `ENABLE_DOCKER_PUSH`: Master switch to enable actual pushing to Docker Hub

#### Build, Test, and Release Process

The `reusable-docker-package-push-model.yml` workflow performs the following steps for each model:

**1. Environment Setup**
- Installs latest Docker engine with model plugin support
- Clones and builds Docker Model Runner CLI from source
- Authenticates with Docker Hub using provided credentials
- Generates standardized Docker tags using `get_partner_model_name.py`

**2. Docker Model Runner Installation**
- Clones the [docker/model-runner](https://github.com/docker/model-runner) repository
- Builds the Model Runner CLI tool (`model-cli`)
- Installs the runner plugin into Docker
- Verifies installation with `model-cli help`

**3. Model Download**
- Downloads quantized GGUF model from Hugging Face using `hf_file_download.py`
- Verifies file existence before proceeding
- Prepares absolute paths for Docker packaging

**4. Model Packaging**
- Uses `model-cli package` command to create Docker container image
- Includes GGUF model file in the container
- Adds Apache 2.0 license file to the image
- Tags image with standardized naming convention

**5. Publishing**
- Pushes packaged model to Docker Hub using `--push` flag
- For default quantizations: creates and pushes additional tag without quantization suffix
- For latest models: creates and pushes `latest` tag
- Tracks packaging and push operations in logs

**6. Verification**
- Checks if model is the default quantization using `is_model_quant_default.py`
- Checks if model is marked as latest using `is_model_latest.py`
- Reviews Docker logs with `model-cli logs`

#### Model Naming Convention

Docker model tags are generated using the `get_partner_model_name.py` script with `--partner docker` flag, which:
- Converts Hugging Face model names to Docker-compatible uppercase tags
- Uses abstract size categories from collection config
- Follows pattern: `{SIZE}[-{ARCH}][-{MODALITY}][-{LANGUAGE}][-{QUANTIZATION}]`
- Examples:
  - `8B-Q5_K_M` (non-default quantization)
  - `8B` (default quantization, no suffix)
  - `NANO-H` (hybrid architecture with abstract size)
  - `MICRO-H-BF16` (hybrid micro model with bf16 quantization)

Full Docker image reference: `{namespace}/{repository}:{tag}`
- Example: `ibmcom/granite4-test-2:8B-Q5_K_M`

#### Supported Quantizations

Docker workflows support all standard GGUF quantizations plus the initial converted format:
- Rounding: `q4_0`, `q4_1`, `q5_0`, `q5_1`, `q8_0`
- K-means: `q2_K`, `q3_K_S`, `q3_K_M`, `q3_K_L`, `q4_K_S`, `q4_K_M`, `q5_K_S`, `q5_K_M`, `q6_K`
- Full precision: `f16`, `bf16` (initial conversion format)

**Note**: The workflow automatically appends the initial conversion quantization (typically `bf16` for Granite 4.0 models) to the quantization matrix.

#### Triggering Docker Releases

To trigger a Docker Model Factory release:

1. Ensure GGUF models are already published to Hugging Face (via standard release workflows)
2. Create a Git tag matching the workflow pattern (e.g., `test-docker-4.0-rc-01`)
3. Push the tag to trigger the workflow
4. Monitor workflow progress at [https://github.com/IBM/gguf/actions](https://github.com/IBM/gguf/actions)

Alternatively, use workflow dispatch to manually trigger a release from the Actions tab.

#### Docker Model Usage

Once published, models can be pulled and run using standard Docker commands:

```bash
# Pull the model
docker pull ibmcom/granite4-test-2:8B-Q5_K_M

# Run the model (example)
docker run -p 8080:8080 ibmcom/granite4-test-2:8B-Q5_K_M
```

Refer to [Docker Model Runner documentation](https://github.com/docker/model-runner) for detailed usage instructions.

#### Notes

- All Docker workflows run on Ubuntu runners for compatibility with Docker tooling
- Docker Model Runner CLI is built from source during each workflow run
- Models are packaged with Apache 2.0 license included in the container
- The `latest` tag is only applied to models marked with `is_latest: true` in the collection config and using the default quantization
- Docker Hub credentials are managed via GitHub secrets (`DOCKER_USERNAME`, `DOCKERHUB_TOKEN`)

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