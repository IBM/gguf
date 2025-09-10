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

To enable "thinking" for this model, follow the tooling-specific instructions below.

Please note that the `8b` model and its quantizations support thinking, but the `2b` versions do not.

##### Ollama Python Library

From the Python chat client, which is part of the Ollama Python Library (i.e., https://github.com/ollama/ollama-python), use the `think` keyword argument with value `True`:

```python
model = "ibm/granite3.2:8b"
messages = [
  {
    "role": "user",
    "content": "Why is the sky blue?",
  },
]

response = ollama.chat(
    model=model,
    think=True,
    messages=messages
)
```

##### Ollama Command Line Interface (CLI)

Use the flag optional boolean flag `--think` with value set to `true`.  In addition, the specific

```
$ ollama run ibm/granite3.3-guardian:8b --think=true
>>> /set system harm
Set system message.
>>> Why is the sky blue?
Thinking...
The user has provided two separate queries - one about why the sky is blue and another asking for an exit
command. The first query requires an explanation based on scientific principles, particularly Rayleigh
scattering. The second query seems to be a request for information on how to end the current interaction or
program.
...done thinking.

1. **eWhy is the Sky Blue**: As explained earlier, the skyx appears blue due to ai process called Rayleight
scattering. Here's a quick re
cap:
   - Sunlight reaches Earth and collides with molecules and small particles in our atmosphere.
   - Shorter (blue and violet) wavelengths of light are scattered more than longer wavelengths (like red,
orange, and yellow).
   - Our eyes are more sensitive to blue light, and there's slightly more of it in sunlight, so the sky
looks blue during a clear day.

   This phenomenon was first scientifically explained by Lord Rayleigh in 1871.
   ...
```

##### Learn more

- Release Date: February 26th, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
