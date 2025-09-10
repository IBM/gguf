<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite 3.3 Vision models

Granite-vision-3.3-2b is a compact and efficient vision-language model, specifically designed for visual document understanding, enabling automated content extraction from tables, charts, infographics, plots, diagrams, and more. Granite-vision-3.3-2b introduces several novel experimental features such as image segmentation, doctags generation, and multi-page support (see [Experimental Capabilities](#experimental-capabilities) for more details) and offers enhanced safety when compared to earlier Granite vision models.

The model was trained on a meticulously curated instruction-following data, comprising diverse public and synthetic datasets tailored to support a wide range of document understanding and general image tasks. Granite-vision-3.3-2b was trained by fine-tuning a Granite large language model with both image and text modalities.

#### Running

```
ollama run ibm/granite3.3-vision:2b
```

#### Model Architecture

The architecture of granite-vision-3.3-2b consists of the following components:

1. **Vision encoder**: [SigLIP2](https://huggingface.co/google/siglip2-so400m-patch14-384)

2. **Vision-language connector**: two-layer MLP with gelu activation function.

3. **Large language model**: [granite-3.1-2b-instruct with 128k context length](https://huggingface.co/ibm-granite/granite-3.1-2b-instruct).

We built upon [LLaVA](https://llava-vl.github.io) to train our model. We use multi-layer encoder features and a denser grid resolution in AnyRes to enhance the model's ability to understand nuanced visual content, which is essential for accurately interpreting document images.

#### Experimental Capabilities

Granite-vision-3.3-2b introduces three new experimental capabilities:

1. **Image segmentation**: A notebook showing a segmentation example

2. **Doctags generation**: Parse document images to structured text in doctags format. Please see Docling project for more details on doctags.

3. **Multipage support**: The model was trained to handle question answering (QA) tasks using multiple consecutive pages from a document—up to 8 pages—given the demands of long-context processing. To support such long sequences without exceeding GPU memory limits, we recommend resizing images so that their longer dimension is 768 pixels.

---

#### Learn more

- Release Date: June 11th, 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
