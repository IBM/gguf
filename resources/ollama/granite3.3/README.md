### Granite 3.3 models

The IBM Granite 2B and 8B models are 128K context length language models that have been fine-tuned for improved reasoning and instruction-following capabilities. These models deliver significant gains on benchmarks for measuring generic performance including AlpacaEval-2.0 and Arena-Hard, and improvements in mathematics, coding, and instruction following. They also supports Fill-in-the-Middle (FIM) for code completion tasks and structured reasoning.

**They are designed to support tool-based use cases** and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Parameter Sizes

##### 2B:

```
ollama run ibm/granite3.3:2b
```

##### 8B:

```
ollama run ibm/granite3.3:8b
```

#### Supported Languages

English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, and Chinese. However, users may finetune this Granite model for languages beyond these 12 languages.

#### Intended Use

These models are designed to handle general instruction-following tasks and can be integrated into AI assistants across various domains, including business applications.

#### Capabilities

- Thinking
- Summarization
- Text classification
- Text extraction
- Question-answering
- Retrieval Augmented Generation (RAG)
- Code related
- Function-calling
- Multilingual dialog use cases
- Long-context tasks including long document/meeting summarization, long document QA, etc.

#### Thinking

To enable thinking, add a message with `"role": "control"` and set `"content"` to `"thinking"`. For example:

```
{
    "messages": [
        {"role": "control", "content": "thinking"},
        {"role": "user", "content": "How do I get to the airport if my car won't start?"}
    ]
}
```

##### Learn more

- Release Date: April 16th, 2025
- License: Apache 2.0
- https://www.ibm.com/granite
