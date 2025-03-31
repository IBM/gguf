#### Survey of Ollama 'built-in" models

##### registry: registry.ollama.ai

| name (basename,finetune) | local name | arch. (ggml model) | Size (MB) | [Quant.](https://github.com/ggerganov/llama.cpp/blob/master/include/llama.h) | Ctx. (embed) Len. |
|:--|:--|---|---|---|---|
| gemma-2-9b-it (none, none) | [gemma2:latest](https://ollama.com/library/gemma2) | gemma2 (llama) | (9B) | Q4_0 (2) | 8192 (3584) |
| (Meta) Llama 3.2 3B Instruct (Llama-3.2, Instruct) | llama3.2:latest | llama (gpt2) | 3B | Q4_K_M (15) | 131072 (3072) |
| Meta Llama 3.1 8B Instruct (Meta-Llama-3.1, Instruct) | llama3.1:latest | llama (gpt2) | 8B | Q4_K_M (15) | 131072 (4096) |
| Mistral-7B-Instruct-v0.3 (N/A) | mistral:latest | llama (llama) | 7B | Q4_0 (2) | 32768 (4096) |
| Qwen2.5 7B Instruct (Qwen2.5, Instruct) | qwen2.5:latest | qwen2 (gpt2) | 7B | Q4_K_M (15) | 32768 (3584) |

| Version (HF collection) | name (basename,finetune) | local name | arch. (ggml model) | Size (MB) | [Quant.](https://github.com/ggerganov/llama.cpp/blob/master/include/llama.h) | Ctx. (embed) Len. |
| :-- |:--|:--|---|---|---|---|
| N/A ([code](https://huggingface.co/collections/ibm-granite/granite-code-models-6624c5cec322e4c148c8b330)) | Granite 8b Code Instruct 128k (granite, code-instruct-128k) | [granite-code:8b](https://ollama.com/library/granite-code) | llama (gpt2) | 8B | **Q4_0** (2) | **128000** (4096) |
| N/A ([code](https://huggingface.co/collections/ibm-granite/granite-code-models-6624c5cec322e4c148c8b330)) | Granite 20b Code Instruct 8k (granite, code-instruct-8k) | [granite-code:20b](https://ollama.com/library/granite-code) | **starcoder** (gpt2) | 20B | **Q4_0** (2) | 8192 (6144) |
| 3.0 ([3.0 language](https://huggingface.co/collections/ibm-granite/granite-30-language-models-66fdb59bbb54785c3512114f)) | Granite 3.0 1b A400M Instruct (granite-3.0, instruct) | [granite3-moe:1b](https://ollama.com/library/granite3-moe) | granitemoe (gpt2) | 1B-a400M | Q4_K_M (15) | 4096 (1024) |
| 3.0 ([3.0 language](https://huggingface.co/collections/ibm-granite/granite-30-language-models-66fdb59bbb54785c3512114f))| Granite 3.0 3b A800M Instruct (granite-3.0, instruct) | [granite3-moe:3b](https://ollama.com/library/granite3-moe) | granitemoe (gpt2) | 3B-a800M | Q4_K_M (15) | 4096 (1536) |
| 3.0 ([guardian](https://huggingface.co/collections/ibm-granite/granite-guardian-models-66db06b1202a56cf7b079562))| Granite Guardian 3.0 8b (granite-guardian-3.0, **none**) | [granite3-guardian:8b](https://ollama.com/library/granite3-guardian) | granite (gpt2) | 8B | **Q5_K_M** (17) | 8192 (4096) |
| 3.0 ([3.0 language](https://huggingface.co/collections/ibm-granite/granite-30-language-models-66fdb59bbb54785c3512114f)) | [Granite 3.0 8b Instruct](https://huggingface.co/ibm-granite/granite-3.0-8b-instruct) (granite-3.0, instruct) | [granite3-dense:8b](https://ollama.com/library/granite3-dense:8b) | granite (gpt2) | 8B | Q4_K_M (15) | 4096 (4096) |
| 3.0 (???)| Granite 3.0 8b Instruct (granite-3.0, instruct) | [granite3-dense:8b-instruct-fp16](https://ollama.com/library/granite3-dense) | granite (gpt2) | 8B | **F16** (1) | 4096 (4096) |


**Notes**

- `latest` is relative to Ollama (proprietary) publishing and is not reflected in GGUF header.
- `basename`, `finetune` may be are different depending on person who created the GGUF even for the same company...
    - e.g., IBM Granite model "Granite 8b Code Instruct 128k" has a `finetune` name that does not match other IBM models (i.e., `code-instruct-128k`).
- `context_buffer` (size) not mentioned in `finetune` for Ollama `granite-code` models which have `8k` buffers, but is listed for `128k` buffers.
- Ollama model `instructlab/granite-7b-lab` is identical to the `granite-7b` model.
- IQ2_XS quant. may have issues on Apple silicon
    - see commentary here: https://www.reddit.com/r/LocalLLaMA/comments/1ba55rj/overview_of_gguf_quantization_methods/

##### registry: huggingface.co (hf.co)

**Note**: "registries" are created using the domain name of the model repo. ref. during a `pull` or `run` command.

| name (basename,finetune) | local name | arch. (ggml model) | Size (MB) | Quant. | Ctx. (embed) Len. |
|:--|:--|---|---|---|---|
| Qwen2.5.1 Coder 7B Instruct (Qwen2.5.1-Coder, Instruct) | bartowski/Qwen2.5.1-Coder-7B-Instruct-GGUF:latest | qwen2 (gpt2) | 7B | Q4_K_M (15) | 32768 (3584) |
| **liuhaotian** (i.e., Llama-3.2-1B-Instruct) (none,none) | hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:latest | llama (llama) | (1B) | Q4_0 (2) | 32768 (4096) |
| **Models** (i.e., Qwen2.5 14B) (none,none) | hf.co/QuantFactory/Qwen2.5-Coder-14B-GGUF:latest | llama (gpt2) | **15B** | **Q2_K** (10) | 32768 (5130) |

**Notes**

- downstream fine tunings or quants. lose identity (in the GGUF file) or drop (pedigree-related) fields or create new ones
    - `general.name`, `general.basename`, `general.finetune`, etc.
        - e.g., `general.name=liuhaotian` is the name of the person who created the downstream GGUF **(not the actual model name)** (and it had no `basename`, nor `finetune`)
    - `.size_label` did not match model declared size.
- when multiple GGUF models are in a repo. Ollama "grabs" the first one (alphanumerically)
    - e.g., `Qwen2.5-14B-Instruct` repo.: https://huggingface.co/QuantFactory/Qwen2.5-14B-Instruct-GGUF/tree/main
        - has 14 quantizations... but it **grabbed the quant. `Q2_K`(least precise)**
