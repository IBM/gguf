# gguf

This repository provides an automated CI/CD process to convert, test and deploy IBM Granite models, in safetensor format, from the `ibm-granite` organization to versioned IBM GGUF collections in Hugging Face Hub under the [`ibm-research` organization](https://huggingface.co/collections/ibm-research). This includes:

- [Granite 3.2 Models (GGUF)](https://huggingface.co/collections/ibm-research/granite-32-models-gguf-67bf411f8eb52909dde3532b)


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

Format conversions (i.e., GGUF) and  quantizations will only be provided for canonically hosted model repositories hosted in an official IBM Huggingface organization.

Currently, this includes the following organizations:

- https://huggingface.co/ibm-granite
- https://huggingface.co/ibm-research

Additionally, only a select set of IBM models from these orgs. will be converted based upon the following general criteria:

- The IBM GGUF model needs to be referenced by an AI provider service as a "supported" model.
    - *For example, a local AI provider service such as [Ollama](https://ollama.com/) or a hosted service such as [Replicate](https://replicate.com/).*

- The GGUF model is referenced by a public blog, tutorial, demo, or other public use case.
    - Specifically, if the model is referenced in an  IBM [Granite Snack Cookbook](https://github.com/ibm-granite-community/granite-snack-cookbook)

Select quantization will only be made available when:

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

###### What to update

The YAML GitHub workflow files have a few environment variables that may need to be updated to reflect which collections, models and quantizations should be included on the next, subsequent GitHub (tagged)release. Using the "Public" release YAML file as an example:

```yaml
env:
  ENABLE_INSTRUCT_JOBS: false
  ENABLE_VISION_JOBS: false
  ENABLE_GUARDIAN_JOBS: true
  SOURCE_INSTRUCT_REPOS: "[
    'ibm-granite/granite-3.2-2b-instruct',
    ...
  ]"
  TARGET_INSTRUCT_QUANTIZATIONS: "[
    'Q4_K_M',
    ...
  ]"
  SOURCE_GUARDIAN_REPOS: "[
    'ibm-granite/granite-guardian-3.2-3b-a800m',
    ...
  ]"
  TARGET_GUARDIAN_QUANTIZATIONS: "[
    'Q4_K_M',
    ...
  ]"
  SOURCE_VISION_REPOS: "[
    'ibm-granite/granite-vision-3.2-2b',
    ...
  ]"
  TARGET_VISION_QUANTIZATIONS: "[
    'Q4_K_M',
    ...
  ]"
  ...
  COLLECTION_CONFIG: "resources/json/latest/hf_collection_mapping_gguf.json"
```

**Note**: that the `COLLECTION_CONFIG` env. var. provides the relative path to the collection configuration file, which is located in the `resources/json` directory of the repository for the specific Granite release.

### Updating Tools

#### llama.cpp

Clone and build the following llama.cpp binaries using these build/link flags:

##### Build intermediate CMake build files

The following command will create the proper CMake `build` files for generating code that will run within both `macos` and `ubuntu` container images.  They also assure that the llama.cpp libraries will not attempt to use GPUs since the current GitHub Virtual Machines for both operating systems do not support this.

```
cmake -B build -DBUILD_SHARED_LIBS=OFF -DGGML_METAL=OFF -DGGML_NATIVE_DEFAULT=OFF -DCMAKE_CROSSCOMPILING=TRUE -DGGML_NO_ACCELERATE=ON
```

**Note**: As flags have changed often, the following minimal set of flags MAY work but needs testing:

```
cmake -B build -DBUILD_SHARED_LIBS=OFF -DGGML_NO_ACCELERATE=ON -DCMAKE_CROSSCOMPILING=TRUE
```

##### Build release binaries

Use this command to build all llama.cpp tool binaries to `build/bin` directory:

```
cmake --build build --config Release
```

##### Copy built binaries and push to `bin`

Once built locally, copy the following files from your `build/bin` directory to this repository's `bin` directory:

- llama-cli
- llama-quantize
- llama-run
- llama-server
- llama-llava-cli *(May no longer be needed/supported as of May 2025 as llava support has been rolled into general libs under multimodal support aka. `mtmd` )*

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