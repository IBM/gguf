<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite 3.2 models

Granite-3.2 is a family of long-context AI models fine-tuned for thinking capabilities. Built on top of Granite-3.1, it has been trained using a mix of permissively licensed open-source datasets and internally generated synthetic data designed for reasoning tasks. The models allow controllability of its thinking capability, ensuring it is applied only when required.

**They are designed to support tool-based use cases** and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Running

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

Use the flag optional boolean flag `--think` with value set to `true`.

```bash
$ ollama run ibm/granite3.2:8b --think=true
>>> Why is the sky blue?
Thinking...
The user is asking about a fundamental scientific phenomenon - why the sky appears blue. This question
involves understanding of physics and optics, particularly the behavior of light in relation to Earth's
atmosphere.

...done thinking.

The sky appears blue due to a specific type of light scattering known as Rayleigh scattering. Let's break it
down step by step:

1. **Composition of Sunlight**: Sunlight is not just white light; it's composed of different colors, each
with its unique wavelength. These include red, orange, yellow, green, blue, indigo, and violet – the
familiar acronym ROYGBIV.

2. **Interaction with Atmosphere**: When sunlight reaches Earth’s atmosphere, it interacts not just with air
molecules (mainly nitrogen and oxygen), but also with tiny particles like dust and water droplets suspended
in the air.

3. **Scattering of Light**: These interactions cause the light to scatter in different directions. There are
two main types of scattering at play here: Mie scattering (for longer wavelengths, like violet and red) and
Rayleigh scattering (for shorter wavelengths).

...

So, essentially, all this scattered blue light entering our atmosphere from various directions makes the sky
appear blue to us. This fascinating phenomenon is a practical demonstration of physics at work in our
everyday lives!
```

---

#### Learn more

- Release Date: February 26th, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
