<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite guardian models

The IBM Granite Guardian 3.1 2B and 8B models are designed to detect risks in prompts and/or responses. They can help with risk detection along many key dimensions catalogued in the [IBM AI Risk Atlas](https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas). They are trained on unique data comprising human annotations and synthetic data informed by internal red-teaming, and they outperform other open-source models in the same space on standard benchmarks.

#### Running

##### 2B:

```
ollama run ibm/granite3.1-guardian:2b >>> /set system profanity
```

##### 8B:

```
ollama run ibm/granite3.1-guardian:8b >>> /set system violence
```

The model will produce a single output token, either `Yes` or `No`. By default, the general-purpose `harm` category is used, but other categories can be selected by setting the system prompt.

#### Supported use cases

- Risk detection in prompt text or model response (i.e. as guardrails), such as:
  - Harm (`harm`): content considered generally harmful
  - Social Bias (`social_bias`): prejudice based on identity or characteristics
  - Jailbreaking (`jailbreak`): deliberate instances of manipulating AI to generate harmful, undesired, or inappropriate content
  - Violence (`violence`): content promoting physical, mental, or sexual harm
  - Profanity (`profanity`): use of offensive language or insults
  - Sexual Content (`sexual_content`): explicit or suggestive material of a sexual nature
  - Unethical Behavior (`unethical_behavior`): actions that violate moral or legal standards

- RAG (retrieval-augmented generation) to assess:
  - Context relevance (`relevance`): whether the retrieved context is relevant to the query
  - Groundedness (`groundedness`): whether the response is accurate and faithful to the provided context
  - Answer relevance (`answer_relevance`): whether the response directly addresses the user’s query

- Agentic Workflows to assess:

    - Function Calling Hallucination (`function_calling`) : validates use of function calls for syntactic and semantic hallucination.

#### Granite dense models

The Granite dense models are designed to support tool-based use cases and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Granite mixture of experts models

The Granite MoE models are designed for low latency usage and to support deployment in on-device applications or situations requiring instantaneous inference.

---

#### Learn more

- Release Date: 21 January 2025
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- https://www.ibm.com/granite
