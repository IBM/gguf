<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite 4 models

Granite 4 `base` models are developed using a diverse set of techniques with a structured chat format, including supervised finetuning, model alignment using reinforcement learning, and model merging.

Granite 4 `instruct` models are finetuned from their base models using a combination of open source instruction datasets with permissive license and internally collected synthetic datasets. They feature improved instruction following (IF) and tool-calling capabilities, making them more effective in enterprise applications.
  - *Please note that `instruct` models do not have the `base` qualifier in their name (e.g., `ibm-granite/granite4:micro-h` vs. `mrutkows/granite4:micro-h-base`).*

#### Sizes

- **micro**: 3B parameters. These models are trained from scratch on approximately *15 trillion* tokens following a four-stage training strategy: 10 trillion tokens in the first stage, 2 trillion in the second, another 2 trillion in the third, and 0.5 trillion in the final stage.
- **tiny**: 7B parameters. These models are trained from scratch on approximately *23 trillion* tokens following a four-stage training strategy: 15 trillion tokens in the first stage, 5 trillion in the second, 2 trillion in the third, and 0.5 trillion in the final stage.
- **small**: 32B parameters. The model is trained from scratch on approximately *23 trillion* tokens following a four-stage training strategy: 15 trillion tokens in the first stage, 5 trillion in the second, 2 trillion in the third, and 0.5 trillion in the final stage.

#### Running

Example of running the default `tiny` model (i.e., with quantization of Q4_K_M):

```
ollama run ibm/granite4:tiny-h
```

To run other quantizations (e.g., F16):

```
ollama run ibm/granite4:tiny-h-q8_0
```

#### Supported Languages

Supported Languages: English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, and Chinese. Users may finetune Granite 4.0 models for languages beyond these languages.

#### Intended Use

This model is designed to handle general instruction-following tasks and can be integrated into AI assistants across various domains, including business applications.

Intended use: The model is designed to respond to general instructions and can be used to build AI assistants for multiple domains, including business applications.

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
- GitHub Repository: [ibm-granite/granite-4.0-language-models](https://github.com/ibm-granite/granite-4.0-language-models)
- Release Date: October 2nd, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
