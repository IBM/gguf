### Granite embedding models

The IBM Granite Embedding 30M and 278M models are text-only dense bi-encoder embedding models, with 30M available in English only and 278M serving multilingual use cases. These models are designed to produce fixed length vector representations for a given text chunk, which can be used for text similarity, retrieval, and search applications.

#### Parameter Sizes

##### 30M:

```
ollama run granite-embedding:30m
```

##### 278M:

```
ollama run granite-embedding:278m
```

#### Supported Languages

30M: English 278M: English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, Chinese (Simplified)

#### Granite dense models

The Granite dense models are available in 2B and 8B parameter sizes designed to support tool-based use cases and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Granite mixture of experts models

The Granite mixture of experts models are available in 1B and 3B parameter sizes designed for low latency usage.

##### Learn more

- Release Date: December 18th, 2024
- License: Apache 2.0
- https://www.ibm.com/granite