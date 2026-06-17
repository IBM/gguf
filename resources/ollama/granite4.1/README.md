<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite 4 models

Granite 4.1 language models are a family of state-of-the-art open foundation models featuring dense decoder-only architectures in three sizes — 3B, 8B, and 30B. They natively support multilingual capabilities, a wide range of coding tasks, retrieval-augmented generation (RAG), tool usage, and structured JSON output.

Our models are trained from scratch on approximately 15 trillion tokens through a five-phase strategy designed to progressively refine data quality and model capabilities. The first two phases cover pre-training proper, before transitioning into mid-training in Phases 3 and 4 with high-quality data annealing. The fifth and final phase performs long-context extension, scaling the context window up to 512K tokens through a staged process.

All models are publicly released under the Apache 2.0 license, allowing free use for both research and commercial purposes. The data curation and training processes were specifically designed for enterprise scenarios and customization, incorporating governance, risk, and compliance (GRC) evaluations alongside IBM's standard data clearance and document quality review procedures.

We provide both base models (checkpoints after pre-training) and instruct models (checkpoints fine-tuned for dialogue, instruction following, helpfulness, and safety).

  - *Please note that `instruct` models do not have the `base` qualifier in their name (e.g., `ibm-granite/granite4.1:8b` vs. `ibm-granite/granite4.1:8b-base`).*

#### Running

Example of running the default model (i.e., typically, this is the `Q4_K_M` quantization):

```
ollama run ibm/granite4.1:8b
```

To run other quantizations (e.g., `Q8_0`):

```
ollama run ibm/granite4.1:8b-q8_0
```

#### Supported Languages

Supported Languages: English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, and Chinese. Users may finetune Granite 4.1 models for languages beyond these languages.

#### Intended Use

This model is designed to handle general instruction-following tasks and can be integrated into AI assistants across various domains, including business applications.

The model is designed to respond to general instructions and can be used to build AI assistants for multiple domains, including business applications.

#### Capabilities

- Summarization
- Text classification
- Text extraction
- Question-answering
- Retrieval Augmented Generation (RAG)
- Code related tasks
- Function-calling tasks
- Multilingual dialog use cases
- Fill-In-the-Middle (FIM) code completions

---

#### Learn more

- Developers: Granite Team, IBM
- Website: [Granite Docs](https://www.ibm.com/granite/docs)
- GitHub Repository: [ibm-granite/granite-4.1-language-models](https://github.com/ibm-granite/granite-4.1-language-models)
- Release Date: April 28th, 2026
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
