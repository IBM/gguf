# gguf
IBM GGUF-encoded AI models and conversion scripts


---

### Target IBM Models

Only a select set of IBM models will be converted to GGUF format based upon the following criteria:

- The IBM GGUF model needs to be referenced by an AI provider service (i.e., a local AI provider service) as a "supported" model. 
- The GGUF model is referenced by a public blog, tutorial, demo, or other public use case.

### GGUF Format

The GGUF format is defined in the [GGUF specification](https://github.com/ggerganov/gguf/blob/main/spec.md). The specification describes the structure of the file, how it is encoded, and what information is included.

### GGUF Conversion

TBD

### GGUF Verification Testing

As a baseline, each converted model MUST successfully be run in the following providers:

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - As the core implementation of the GGUF format which is either a direct dependency or utilized as forked code in most all downstream GGUF providers, testing is essential. Specifically, testing to verify the model can be hosted using the `llama-server` service.
    - *See the specific section on `llama.cpp` for more details on which version is considered "stable" and how the same version will be used in both conversion and testing.* 
- [Ollama]() - 


####

