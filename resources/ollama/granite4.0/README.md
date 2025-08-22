### Granite-4.0 models

Granite-4-Tiny-Preview is a 7B parameter fine-grained hybrid mixture-of-experts (MoE) instruct model fine-tuned from Granite-4.0-Tiny-Base-Preview using a combination of open source instruction datasets with permissive license and internally collected synthetic datasets tailored for solving long context problems. This model is developed using a diverse set of techniques with a structured chat format, including supervised fine-tuning, and model alignment using reinforcement learning.

##### running tiny-preview

```
ollama run granite4.0:7b
```

#### Supported Languages

English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, and Chinese. However, users may fine-tune this Granite model for languages beyond these 12 languages.

#### Intended Use

This model is designed to handle general instruction-following tasks and can be integrated into AI assistants across various domains, including business applications.

#### Capabilities

- Thinking
- Summarization
- Text classification
- Text extraction
- Question-answering
- Retrieval Augmented Generation (RAG)
- Code related tasks
- Function-calling tasks
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

- Release Date: May 2nd, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
