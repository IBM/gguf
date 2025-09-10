<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite 3.3 models

The IBM Granite 2B and 8B models are 128K context length language models that have been fine-tuned for improved reasoning and instruction-following capabilities. These models deliver significant gains on benchmarks for measuring generic performance including AlpacaEval-2.0 and Arena-Hard, and improvements in mathematics, coding, and instruction following. They also supports Fill-in-the-Middle (FIM) for code completion tasks and structured reasoning.

**They are designed to support tool-based use cases** and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Running

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

To enable "thinking" for this model, follow the tooling-specific instructions below.

##### Ollama Python Library

From the Python chat client, which is part of the Ollama Python Library (i.e., https://github.com/ollama/ollama-python), use the `think` keyword argument with value `True`:

```python
model = "ibm/granite3.3:8b"
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

```bash
$ ollama run ibm/granite3.3:8b --think=true
>>> Why is the sky blue?
Thinking...
The question seeks an explanation for why the sky appears blue. This phenomenon involves the principles of
optics, particularly Rayleigh scattering. Here's a breakdown:

1. Light from the sun reaches Earth in various colors due to its composition of different wavelengths (a
spectrum ranging from violet to red).
2. When sunlight enters Earth’s atmosphere, it interacts with molecules and tiny particles like nitrogen and
oxygen.
3. According to Rayleigh scattering, shorter wavelength light (such as blue and violet) is scattered in all
directions more than longer wavelengths (like red and orange).

...

This explanation aligns with fundamental principles in physics and atmospheric science.
...done thinking.

### Why is the Sky Blue?

The sky appears blue primarily because of a phenomenon called Rayleigh scattering. Here’s how it works:

1. **Sunlight Composition**: Sunlight consists of different colors or wavelengths, forming a spectrum that
ranges from violet (shortest wavelength, about 380-450 nm) to red (longest wavelength, about 620-750 nm).

2. **Atmospheric Interaction**: As sunlight reaches Earth’s atmosphere, it encounters gas molecules (mostly
nitrogen and oxygen) and tiny particles.

3. **Rayleigh Scattering**: This scattering effect is influenced by the wavelength of light. Shorter
wavelengths, like those in the blue portion of the spectrum (approximately 450-495 nm), are scattered about
ten times more than longer wavelengths such as red light.

...

In summary, the sky appears blue because Earth’s atmosphere scatters short wavelengths (blue and violet)
more than long wavelengths (red and orange), and our eyes are more sensitive to blue light.</response>

```

---

#### Learn more

- Release Date: April 16th, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
