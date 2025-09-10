<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite-4.0 models (preview)

Granite-4-Tiny-Preview is a 7B parameter fine-grained hybrid mixture-of-experts (MoE) instruct model fine-tuned from Granite-4.0-Tiny-Base-Preview using a combination of open source instruction datasets with permissive license and internally collected synthetic datasets tailored for solving long context problems. This model is developed using a diverse set of techniques with a structured chat format, including supervised fine-tuning, and model alignment using reinforcement learning.

#### Running

Running the default model (i.e., with quantization of Q4_K_M):

```
ollama run ibm/granite4.0-preview:tiny
```

To run other quantizations (e.g., F16):

```
ollama run ibm/granite4.0-preview:tiny-instruct-f16
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

To enable "thinking" for this model, follow the tooling-specific instructions below.

##### Ollama Python Library

From the Python chat client, which is part of the Ollama Python Library (i.e., https://github.com/ollama/ollama-python), use the `think` keyword argument with value `True`:

```python
model = "ibm/granite4.0-preview:tiny"
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
$ ollama run ibm/granite4.0-preview:tiny --think=true
>>> Why is the sky blue?
Thinking...
The question "Why is the sky blue?" is a classic one that can be answered from both scientific and
philosophical perspectives. From a scientific standpoint, the reason the sky appears blue is due to the
interaction of sunlight with Earth's atmosphere. Here’s why:

1. **Light Composition**: Sunlight is composed of different colors (wavelengths), which together form a
spectrum. This light travels in waves and can be separated into its constituent wavelengths, much like a
rainbow does when it passes through water droplets or prisms. The visible spectrum includes red, orange,
yellow, green, blue, indigo, and violet (ROYGBIV).

2. **Rayleigh Scattering**: When sunlight reaches Earth's atmosphere, it is scattered in all directions by
the gases, dust particles, and water molecules present. The amount of scattering depends on several factors,
including the wavelength of light:
   - Shorter (blue) wavelengths are scattered more effectively than longer (red) wavelengths because they
interact with smaller atmospheric particles more frequently. This phenomenon is known as Rayleigh
scattering.

...

Philosophically speaking, the question "Why is the sky blue?" invites deeper contemplation about how our
senses perceive and interpret physical phenomena. It highlights the interplay between light, atmospheric
conditions, and human vision.
...done thinking.

<response>### Why Is the Sky Blue?

The sky appears blue due to a scientific process known as Rayleigh scattering. Here's a breakdown of why
this occurs:

1. **Composition of Sunlight**: Sunlight is not just one color but a mixture of all visible colors, each
with different wavelengths ranging from red (longest) to violet (shortest). These colors form the spectrum
we see when light passes through a prism or rainbow.

2. **Atmospheric Scattering**: As sunlight travels through Earth's atmosphere, it encounters molecules of
gases such as nitrogen and oxygen, along with dust particles and water droplets. When these tiny particles
interact with the light waves, they scatter them in various directions.

...

5. **Atmospheric Variations**: The appearance of the sky can change due to atmospheric conditions like
pollution or scattering by water droplets in clouds, which alter how sunlight is dispersed and thus affect
our perception of the sky's hue.</response>
```

---

#### Learn more

- Release Date: May 2nd, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
