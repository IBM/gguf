# gguf

This repository contains the canonical information to use when converting IBM AI models to the GGUF format. It includes conversion scripts and testing requirements.  Aspirationally, this repo. wil include and automated CI/CD process to convert, test and deploy models to the official IBM GGUF collection in Hugging Face.


---

### Target IBM Models

Only a select set of IBM models will be converted to GGUF format based upon the following criteria:

- The IBM GGUF model needs to be referenced by an AI provider service (i.e., a local AI provider service) as a "supported" model. 
- The GGUF model is referenced by a public blog, tutorial, demo, or other public use case.

In addition, models should be canonically hosted in an official IBM's repository. Currently, this includes the following:

- **Hugging Face**
    - https://huggingface.co/ibm-granite

The following tables list the current target set of IBM models along with commentary on the rationale for inclusion:


#### IBM Granite Collection

See: https://huggingface.co/ibm-granite

##### Granite 3.0 Language Models

These models are found in the [Granite 3.0 Language Models collection](https://huggingface.co/collections/ibm-granite/granite-30-language-models-66fdb59bbb54785c3512114f) and are designed to respond to general instructions and can be used to build AI assistants for multiple domains, including business applications.


| Name | Architecture | Rationale | Details |
| --- | --- | --- | -- |
| [granite-3.0-8b-instruct](https://huggingface.co/ibm-granite/granite-3.0-8b-instruct) | GraniteForCausalLM | Consensus default | Models of ~8B size appear as defaults for most local AI providers. |
| [granite-3.0-2b-instruct](https://huggingface.co/ibm-granite/granite-3.0-2b-instruct)| GraniteForCausalLM | Consensus default | Models of ~2B or 3B size are offered as  built-in alternatives for most local AI providers.
| [granite-3.0-3b-a800m-base ](https://huggingface.co/ibm-granite/granite-3.0-3b-a800m-base) | GraniteMoeForCausalLM | Small form-factor | Model highlights Granite's capabilities when run on small form-factor CPUs/memory. | 

where:
- Consensus default:
    - Comparable size to default models already referenced by multiple downstream providers and frameworks. 
    - Size ideal for local CPU/GPU serving.
- Small form-factor:
    - Model size intended running locally on small form-factor devices such as watches and mobile devices.

---

### GGUF Format

The GGUF format is defined in the [GGUF specification](https://github.com/ggerganov/gguf/blob/main/spec.md). The specification describes the structure of the file, how it is encoded, and what information is included.

### GGUF Conversion

Currently, the primary means to convert from HF SafeTensors format to GGUF will be the canonical llama.cpp tool `convert-hf-to-gguf.py`.

for example:

```
python llama.cpp/convert-hf-to-gguf.py ./models/modelrepo --outfile output_file.gguf --outtype q8_0
```

#### Alternatives TODO: investigate

##### Ollama CLI

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
- Access control to source repo. required???
- Similar to Ollama CLI, the web UI supports only a subset of quantizations.

---


### GGUF Verification Testing

As a baseline, each converted model MUST successfully be run in the following providers:

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - As the core implementation of the GGUF format which is either a direct dependency or utilized as forked code in most all downstream GGUF providers, testing is essential. Specifically, testing to verify the model can be hosted using the `llama-server` service.
    - *See the specific section on `llama.cpp` for more details on which version is considered "stable" and how the same version will be used in both conversion and testing.* 
- [Ollama](https://github.com/ollama/ollama) - As a key model service provider supported by higher level frameworks and platforms (e.g., [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm), [LM Studio](https://github.com/lmstudio-ai) etc.), testing the ability to `pull` and `run` the model is essential.
    - **Note**: *The official Ollama Docker image [ollama/ollama](https://hub.docker.com/r/ollama/ollama) is available on Docker Hub.*

---

#### Survey of existing Ollama 'built-in" models

##### registry: registry.ollama.ai

| Name (ftune) | sname | Arch. (ggml model) | Size (MB) | Quant. | Ctx. (embed) Len. |
|:--|:--|---|---|---|---|
| Meta Llama 3.1 8B Instruct (Meta-Llama-3.1, Instruct) | llama3.1:latest | llama (gpt2) | 8B | Q8_K (15) | 131072 (4096) |
| Llama 3.2 3B Instruct (Llama-3.2, Instruct) | llama3.2:latest | llama (gpt2) | 3B | Q8_K (15) | 131072 (3072) |
| Mistral-7B-Instruct-v0.3 (N/A) | mistral:latest | llama (llama) | 7B | Q4_0 (2) | 32768 (4096) |
| Granite 8b Code Instruct 128k (granite, code-instruct-128k) | granite-code:8b | llama (gpt2) | 8B | **Q4_0** (2) | 128000 (4096) |
| Granite 20b Code Instruct 8k (granite, code-instruct-8k) | granite-code:20b | **starcoder** (gpt2) | 20B | **Q4_0** (2) | 8192 (6144) |
| Granite 3.0 1b A400M Instruct (granite-3.0, instruct) | granite3-moe:1b | granitemoe (gpt2) | 1B-a400M | Q8_K (15) | 4096 (1024) |
| Granite 3.0 3b A800M Instruct (granite-3.0, instruct) | granite3-moe:3b | granitemoe (gpt2) | 3B-a800M | Q8_K (15) | 4096 (1536) |
| Qwen2.5 7B Instruct (Qwen2.5, Instruct) | qwen2.5:latest | qwen2 (gpt2) | 7B | Q8_K (15) | 32768 (3584) |


##### registry: huggingface.co

| Name (ftune) | sname | Arch. | Size (MB) | Quant. | Ctx. (embed) Len. |
|:--|:--|---|---|---|---|
| Qwen2.5.1 Coder 7B Instruct (Qwen2.5.1-Coder, Instruct) | bartowski/Qwen2.5.1-Coder-7B-Instruct-GGUF:latest | qwen2 (gpt2) | 7B | ? | |

##### registry: hu.co

| Name (ftune) | sname | Arch. | Size (MB) | Quant. | Ctx. (embed) Len. |
|:--|:--|---|---|---|---|
| Qwen2.5 14B (none) | (Qwen/Qwen2.5-14B) | qwen2 | 14B | Q8_K (15) | 131072 (5120) |
---



