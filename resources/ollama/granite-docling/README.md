# Granite Docling

<center>
<img src="https://huggingface.co/ibm-granite/granite-docling-258M/resolve/main/granite_docling.png" data-canonical-src="https://huggingface.co/ibm-granite/granite-docling-258M/resolve/main/granite_docling.png" width="200" />
</center>

Granite Docling is a multimodal Image-Text-to-Text model engineered for efficient document conversion. It preserves the core features of Docling while maintaining seamless integration with [DoclingDocuments](https://docling-project.github.io/docling) to ensure full compatibility.

## Model Summary

Granite Docling 258M builds upon the Idefics3 architecture, but introduces two key modifications: it replaces the vision encoder with siglip2-base-patch16-512 and substitutes the language model with a Granite 165M LLM.

Granite-docling-258M is fully integrated into the Docling pipelines, which leverages all its capabilities for a one-shot prediction of all Docling features.

### Features

- 🏷️ **DocTags for Efficient Tokenization** – Introduces DocTags an efficient and minimal representation for documents that is fully compatible with **DoclingDocuments**.
- 🔍 **OCR (Optical Character Recognition)** – Extracts text accurately from images.
- 📐 **Layout and Localization** – Preserves document structure and document element **bounding boxes**.
- 💻 **Code Recognition** – Detects and formats code blocks including indentation.
- 🔢 **Formula Recognition** – [Enhanced] Identifies and processes mathematical expressions.
- 🧮 **Inline Equations** – Better inline math recognition
- 📊 **Chart Recognition** – Extracts and interprets chart data.
- 📑 **Table Recognition** – Supports column and row headers for structured table extraction.
- 🖼️ **Figure Classification** – Differentiates figures and graphical elements.
- 📝 **Caption Correspondence** – Links captions to relevant images and figures.
- 📜 **List Grouping** – Organizes and structures list elements correctly.
- 📄 **Full-Page Conversion** – Processes entire pages for comprehensive document conversion including all page elements (code, equations, tables, charts etc.)
- 🧩 **Flexible Inference Modes** – Choose between full-page inference, bbox-guided region inference
- 📂 **General Document Processing** – Trained for both scientific and non-scientific documents.
- 🧾 **Document Element QA** – Answer questions about a document's structure such as the presence and order of document elements
- 🌍 **Multi-language** – Japanese, Arabic and Chinese support (_experimental_)
- 💨 **Fast inference using VLLM** – Avg of 0.35 secs per page on A100 GPU.

## Intended Use
Granite-Docling is designed to complement the Docling library, not replace it. It integrates as a component within the larger Docling library, consolidating the functions of multiple single-purpose models into a single, compact VLM.
However, Granite-Docling is **not** intended for general image understanding. For tasks focused solely on image-text input, we recommend using [Granite Vision models](https://huggingface.co/collections/ibm-granite/granite-vision-models-67b3bd4ff90c915ba4cd2800), which are purpose-built and optimized for image-text processing.


## Supported Instructions

<table>
  <tr>
    <th>Description</th>
    <th>Instruction</th>
    <th>Short Instruction</th>
  </tr>
  <tr>
    <td><b>Full conversion</b></td>
    <td>Convert this page to docling.</td>
    <td>-</td>
  </tr>
  <tr>
    <td><b>Chart</b></td>
    <td>Convert chart to table.</td>
    <td><code>&lt;chart&gt;</code></td>
  </tr>
  <tr>
    <td><b>Formula</b></td>
    <td>Convert formula to LaTeX.</td>
    <td><code>&lt;formula&gt;</code></td>
  </tr>
  <tr>
    <td><b>Code</b></td>
    <td>Convert code to text.</td>
    <td><code>&lt;code&gt;</code></td>
  </tr>
  <tr>
    <td><b>Table</b></td>
    <td>Convert table to OTSL. (<a href="https://arxiv.org/pdf/2305.03393">Lysak et al., 2023</a>)</td>
    <td><code>&lt;otsl&gt;</code></td>
  </tr>
  <tr>
    <td rowspan="4"><b>Actions and Pipelines</b></td>
    <td>OCR the text in a specific location: &lt;loc_155&gt;&lt;loc_233&gt;&lt;loc_206&gt;&lt;loc_237&gt;</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Identify element at: &lt;loc_247&gt;&lt;loc_482&gt;&lt;loc_252&gt;&lt;loc_486&gt;</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Find all 'text' elements on the page, retrieve all section headers.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Detect footer elements on the page.</td>
    <td>-</td>
  </tr>
</table>


## Learn more

- Developers: IBM Research
- Website: [Docling](https://docling.ai)
- Model: [ibm-granite/granite-docling-258M](https://huggingface.co/ibm-granite/granite-docling-258M)
- GitHub Repository: [docling-project/docling](https://github.com/docling-project/docling)
- Release Date: September 17, 2025
- License: Apache 2.0
