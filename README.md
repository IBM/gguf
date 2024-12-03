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

TBD

### GGUF Verification Testing

As a baseline, each converted model MUST successfully be run in the following providers:

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - As the core implementation of the GGUF format which is either a direct dependency or utilized as forked code in most all downstream GGUF providers, testing is essential. Specifically, testing to verify the model can be hosted using the `llama-server` service.
    - *See the specific section on `llama.cpp` for more details on which version is considered "stable" and how the same version will be used in both conversion and testing.* 
- [Ollama](https://github.com/ollama/ollama) - As a key model service provider supported by higher level frameworks and platforms (e.g., [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm), [LM Studio](https://github.com/lmstudio-ai) etc.), testing the ability to `pull` and `run` the model is essential.
    - **Note**: *The official Ollama Docker image [ollama/ollama](https://hub.docker.com/r/ollama/ollama) is available on Docker Hub.*


####

