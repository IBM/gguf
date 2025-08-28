### Granite dense models

The IBM Granite 1B and 3B models are the first mixture of experts (MoE) Granite models from IBM designed for low latency usage.

The models are trained on over 10 trillion tokens of data, the Granite MoE models are ideal for deployment in on-device applications or situations requiring instantaneous inference.

#### Parameter Sizes

##### 1B:

```
ollama run ibm/granite3-moe:1b
```

##### 3B:

```
ollama run ibm/granite3-moe:3b
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

#### Granite dense models

The Granite dense models are available in 2B and 8B parameter sizes designed to support tool-based use cases and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

##### Learn more

- Release Date: October 21st, 2024
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
