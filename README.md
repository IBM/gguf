# gguf

This repository contains the canonical information to use when converting IBM AI models to the GGUF format. It includes conversion scripts and testing requirements.  Aspirationally, this repo. wil include and automated CI/CD process to convert, test and deploy models to the official IBM GGUF collection in Hugging Face.

---

### Target IBM Models

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

#### Supported IBM Granite models

Specifically, the following Granite model repositories are currently supported in GGUF format (by collection) with listed:

###### Language (instruct)

| HF (llama.cpp) Architecture | Source Repo. ID | Target Repo. ID |
| --- | --- | --- |
| GraniteForCausalLM (gpt2) | ibm-granite/granite-3.2-2b-instruct | ibm-research |
| GraniteForCausalLM (gpt2) | ibm-granite/granite-3.2-8b-instruct | ibm-research |

- Supported quantizations: `fp16`, `Q2_K`, `Q3_K_L`, `Q3_K_M`, `Q3_K_S`, `Q4_0`, `Q4_1`, `Q4_K_M`, `Q4_K_S`, `Q5_0`, `Q5_1`, `Q5_K_M`, `Q5_K_S`, `Q6_K`, `Q8_0`

###### Guardian

| HF (llama.cpp) Architecture | Source Repo. ID | Target Repo. ID |
| --- | --- | --- |
| GraniteMoeForCausalLM (granitemoe) | ibm-granite/granite-guardian-3.2-3b-a800m | ibm-research |
| GraniteMoeForCausalLM (granitemoe) | ibm-granite/granite-guardian-3.2-5b | ibm-research |

- Supported quantizations: `fp16`, `Q4_K_M`, `Q5_K_M`, `Q6_K`, `Q8_0`

###### Vision

| HF (llama.cpp) Architecture | Source Repo. ID | Target Repo. ID |
| --- | --- | --- |
| GraniteForCausalLM (granite), LlavaNextForConditionalGeneration | ibm-granite/granite-vision-3.2-2b | ibm-research |

- Supported quantizations: `fp16`, `Q4_K_M`, `Q5_K_M`, `Q8_0`

###### Embedding (dense)

| HF (llama.cpp) Architecture | Source Repo. ID | Target Repo. ID |
| --- | --- | --- |
| Roberta (roberta-bpe) | ibm-granite/granite-embedding-30m-english | ibm-research |
| Roberta (roberta-bpe) | ibm-granite/granite-embedding-125m-english | ibm-research |
| Roberta (roberta-bpe) | ibm-granite/granite-embedding-107m-multilingual | ibm-research |
| Roberta (roberta-bpe) | ibm-granite/granite-embedding-278m-multilingual | ibm-research |

- Supported quantizations: `fp16`, `Q8_0`

**Note**: Sparse model architecture (i.e., RobertaMaskedLM) is not currently supported; therefore, there is no conversion for `ibm-granite/granite-embedding-30m-sparse`.

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

#### Alternatives (planned)

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
- Similar to Ollama CLI, the web UI supports only a subset of quantizations.

---

### GGUF Verification Testing

As a baseline, each converted model MUST successfully be run in the following providers:

##### llama.cpp testing

[llama.cpp](https://github.com/ggerganov/llama.cpp) - As the core implementation of the GGUF format which is either a direct dependency or utilized as forked code in most all downstream GGUF providers, testing is essential. Specifically, testing to verify the model can be hosted using the `llama-server` service.
    - *See the specific section on `llama.cpp` for more details on which version is considered "stable" and how the same version will be used in both conversion and testing.*

##### Ollama testing

[Ollama](https://github.com/ollama/ollama) - As a key model service provider supported by higher level frameworks and platforms (e.g., [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm), [LM Studio](https://github.com/lmstudio-ai) etc.), testing the ability to `pull` and `run` the model is essential.

**Notes**

- *The official Ollama Docker image [ollama/ollama](https://hub.docker.com/r/ollama/ollama) is available on Docker Hub.*
- Ollama does not yet support sharded GGUF models
    - "Ollama does not support this yet. Follow this issue for more info: https://github.com/ollama/ollama/issues/5245"
    - e.g., `ollama pull hf.co/Qwen/Qwen2.5-14B-Instruct-GGUF`


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

- Huggingface Granite
    - Bartowski: https://huggingface.co/bartowski?search_models=granite
