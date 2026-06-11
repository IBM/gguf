# Granite 4.0 3B Vision

**Model Summary:**
Granite-4.0-3B-Vision is a vision-language model (VLM) designed for enterprise-grade
document data extraction. It focuses on specialized, complex extraction tasks that
ultracompact models often struggle with:

- **Chart extraction:** Converting charts into structured, machine-readable formats (Chart2CSV, Chart2Summary, and Chart2Code)
- **Table extraction:** Accurately extracting tables with complex layouts from document images to JSON, HTML, or OTSL
- **Semantic Key-Value Pair (KVP) extraction:** Extracting values based on key names and descriptions across diverse document layouts

The model is delivered as a LoRA adapter on top of [Granite 4.0 Micro](https://huggingface.co/ibm-granite/granite-4.0-micro), with a 3.5B base LLM and 0.5B LoRA adapters. This enables a single
deployment to support both multimodal document understanding and text-only workloads —
the base model handles text-only requests without loading the adapter. See [Model Architecture](#model-architecture) for details.

The methodology and data (ChartNet) used for this model are described in the paper [ChartNet: A Million-Scale, High-Quality Multimodal Dataset for Robust Chart Understanding](https://huggingface.co/papers/2603.27064).

While our focus is on specialized document extraction tasks, the current model preserves and extends the capabilities of Granite-Vision-3.3 2B, ensuring that existing users can adopt it seamlessly with no changes to their workflow.

It continues to support vision‑language tasks such as producing detailed natural‑language descriptions from images (image‑to‑text).

The model can be used standalone and integrates seamlessly with [Docling](https://github.com/DS4SD/docling) to enhance document processing pipelines with deep visual understanding capabilities.

- **Developer:** IBM Research
- **GitHub Repository:** https://github.com/ibm-granite
- **Release Date:** March 27th, 2026
- **License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Supported Tasks

The model supports specialized extraction tasks, each activated by a simple task tag in the user message. The chat template automatically expands tags into the full prompt — no need to write verbose instructions.

| Tag | Task | Output |
|-----|------|--------|
| `<chart2csv>` | Chart to CSV | CSV table with headers and numeric values |
| `<chart2code>` | Chart to Python code | Python code that recreates the chart |
| `<chart2summary>` | Chart to summary | Natural-language description of the chart |
| `<tables_json>` | Table extraction (JSON) | Structured JSON with dimensions and cells |
| `<tables_html>` | Table extraction (HTML) | HTML `<table>` markup |
| `<tables_otsl>` | Table extraction (OTSL) | OTSL markup with cell/merge tags |
| KVP (see prompt instructions below) | Schema based Key-Value pairs extraction | JSON with nested dictionaries and arrays |


## Model Performance

### Benchmark Results

We compare Granite-4.0-3B-Vision against leading small VLMs across multiple extraction benchmarks.

#### Chart Extraction

We evalute chart extraction using the human-verified test-set from [ChartNet](https://huggingface.co/datasets/ibm-granite/ChartNet).

The models are evaluated using LLM-as-a-judge (GPT4o) comparing the model prediction against the ground-truth.

We report the average scores 0-100 on chart2csv and chart2summary extraction tasks.

<div style="display: flex; gap: 10px;">
  <img src="charts.jpg" width="100%">
</div>

#### Table Extraction

To benchmark table extraction, we construct a unified evaluation suite spanning multiple datasets and settings to assess end-to-end table extraction capabilities of vision-language models:

1. **[TableVQA-Extract](https://arxiv.org/abs/2404.19205)** — Converts the original visual table QA benchmark into a cropped table extraction task.
2. **[OmniDocBench-tables](https://arxiv.org/abs/2412.07626)** — A document parsing benchmark over diverse PDF types with detailed annotations for layout, text, formulas, and tables. We use the subset of pages that contain one or more tables to evaluate table extraction in full-page settings.
3. **[PubTablesV2](https://arxiv.org/abs/2512.10888)** — A large-scale table extraction benchmark evaluated in both cropped-table and full-page document settings.

To unify evaluation, we replace each dataset’s original annotations (e.g., Q&A pairs) with a single instruction: *extract the table(s) from the image in HTML format*, using the corresponding HTML as ground truth. For full-page inputs, only tabular elements are considered; when multiple tables appear, they are aggregated into a Python list.

We report results using **TEDS** ([Tree-Edit Distance-based Similarity](https://arxiv.org/abs/2208.00385)), which measures structural and content similarity between predicted and ground-truth HTML tables.

Results are presented separately for cropped-table and full-page settings to highlight performance across controlled and realistic document scenarios.

<div style="display: flex; gap: 10px;">
  <img src="tables-cropped.jpg" width="75%">
</div>
<div style="display: flex; gap: 10px;">
  <img src="tables-full-page.jpg" width="75%">
</div>

#### Key-Value Pair (KVP) Extraction
We evaluate on [VAREX](https://udibarzi.github.io/varex-bench/), a benchmark for
multimodal structured extraction from documents. Granite-4.0-3B-Vision achieves 85.5% exact-match accuracy (zero-shot), ranking 3rd among 2-4B
parameter models as of March 2026 (view results [here](https://udibarzi.github.io/varex-bench/#leaderboard)).

## Training Data

The model was fine-tuned on a curated mixture of extraction-focused datasets spanning chart understanding, complex table parsing, and document KVP extraction, supplemented by the general-purpose [Granite Vision instruction-following dataset](https://arxiv.org/abs/2502.09927) for broad visual understanding.

Chart understanding data was created through a novel code‑guided augmentation methodology that produces diverse, semantically aligned chart samples containing rendering code, chart images, underlying data CSVs, and natural‑language summaries.

Using this pipeline, we are also releasing [ChartNet](https://huggingface.co/datasets/ibm-granite/ChartNet), a comprehensive million‑scale multimodal dataset enriched with real‑world, human‑annotated, safety, and grounding subsets. The dataset and its methodology are detailed in the paper [ChartNet: A Million-Scale, High-Quality Multimodal Dataset for Robust Chart Understanding](https://huggingface.co/papers/2603.27064).

## Model Architecture

1. **SigLIP2 Vision encoder:** `google/siglip2-so400m-patch16-384`. Input images are tiled into 384×384 patches (with a base downscaled view always included), and each tile is encoded independently.
2. **Window Q-Former projectors:** Visual features are compressed 4× using windowed Q-Former projectors: each 4×4 patch window is reduced to 2×2 tokens via cross-attention, where the queries are initialized from a downsampled version of the window features. This reduces the visual token count fed to the LLM.
3. **Feature injection:** A variant of [Deepstack](https://arxiv.org/abs/2406.04334) where visual features are additively injected into the LLM hidden states at multiple layers through two complementary mechanisms:
   - *LayerDeepstack:* Features from 4 vision encoder depths are each projected and injected into a different LLM layer. The Q-Former queries are initialized from downsampled features. The mapping is reversed — the deepest (most semantic) vision features feed the earliest LLM layers, providing strong semantic grounding from the start.
   - *SpatialDeepstack:* The deepest vision features at full resolution are split into 4 complementary spatial groups. Each group's Q-Former queries are initialized from the corresponding spatial subset, and injected at a separate later LLM layer, providing fine-grained spatial detail.

   In total, **8 vision-to-LLM injection points** distribute visual information across the network for stronger visual grounding.
4. **Language model:** Granite 4.0 Micro (3B) with LoRA (rank 256) across all self-attention projections and MLP layers.

**Supported input:** English instructions and images (PNG, JPEG).


## Infrastructure

Granite 4.0 Vision was trained on IBM's Blue Vela supercomputing cluster, outfitted with NVIDIA H100 GPUs. The training was done on 32 GPUs for approximately 200 hours.


## Ethical Considerations and Limitations

The use of vision-language models involves certain risks that should be considered before deployment:

- **Task scope:** The model is specifically designed for structured extraction tasks and may not generalize well to open-ended vision-language tasks.
- **Hallucination:** As with all generative models, outputs should be validated before use in automated pipelines, particularly for high-stakes document processing.
- **Language:** The model is trained on English instructions only and may produce degraded results for documents in other languages.

To enhance safety in enterprise deployments, we recommend using Granite 4.0 Vision alongside [Granite Guardian](https://huggingface.co/ibm-granite/granite-guardian-3.2-5b), a model designed to detect and flag risks in inputs and outputs across key dimensions outlined in the IBM AI Risk Atlas.


## Resources

- ⭐️ Learn about the latest updates with Granite: https://www.ibm.com/granite
- 🚀 Get started with tutorials, best practices, and prompt engineering advice: https://www.ibm.com/granite/docs/
- 💡 Granite learning resources: https://ibm.biz/granite-learning-resources
