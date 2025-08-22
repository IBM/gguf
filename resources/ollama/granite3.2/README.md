### Granite 3.2 models

Granite-3.2 is a family of long-context AI models fine-tuned for thinking capabilities. Built on top of Granite-3.1, it has been trained using a mix of permissively licensed open-source datasets and internally generated synthetic data designed for reasoning tasks. The models allow controllability of its thinking capability, ensuring it is applied only when required.

**They are designed to support tool-based use cases** and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Parameter Sizes

##### 2B:

```
ollama run ibm/granite3.2:2b
```

##### 8B:

```
ollama run ibm/granite3.2:8b
```

#### Supported Languages

English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, and Chinese. However, users may finetune this Granite model for languages beyond these 12 languages.

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

- Release Date: February 26th, 2025
- License: Apache 2.0
- https://www.ibm.com/granite
