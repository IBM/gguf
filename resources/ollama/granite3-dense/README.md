<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite dense models

The IBM Granite 2B and 8B models are text-only dense LLMs trained on over 12 trillion tokens of data, demonstrated significant improvements over their predecessors in performance and speed in IBM’s initial testing. Granite-8B-Instruct now rivals Llama 3.1 8B-Instruct across both OpenLLM Leaderboard v1 and OpenLLM Leaderboard v2 benchmarks.

**They are designed to support tool-based use cases** and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Running

##### 2B:

```
ollama run ibm/granite3-dense:2b
```

##### 8B:

```
ollama run ibm/granite3-dense:8b
```

#### Supported Languages

English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, Chinese (Simplified)

#### Capabilities

- Summarization
- Text classification
- Text extraction
- Question-answering
- Retrieval Augmented Generation (RAG)
- Code related
- Function-calling
- Multilingual dialog use cases

#### Granite mixture of experts models

The Granite Mixture of Experts (MoE) models are available in 1B and 3B parameter sizes designed for low latency usage.

---

#### Learn more

- Release Date: October 21st, 2024
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
