### Granite guardian models

The IBM Granite Guardian 3.0 2B and 8B models are designed to detect risks in prompts and/or responses. They can help with risk detection along many key dimensions catalogued in the [IBM AI Risk Atlas](https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas). They are trained on unique data comprising human annotations and synthetic data informed by internal red-teaming, and they outperform other open-source models in the same space on standard benchmarks.

#### Parameter Sizes

The model will produce a single output token, either `Yes` or `No`. By default, the general-purpose `harm` category is used, but other categories can be selected by setting the system prompt.

##### 2B:

```
ollama run granite3-guardian:2b
>>> /set system profanity
```

##### 8B:

```
ollama run granite3-guardian:8b
>>> /set system violence
```

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

#### Granite dense models

The Granite dense models are available in 2B and 8B parameter sizes designed to support tool-based use cases and for retrieval augmented generation (RAG), streamlining code generation, translation and bug fixing.

#### Granite mixture of experts models

The Granite MoE models are available in 1B and 3B parameter sizes designed for low latency usage and to support deployment in on-device applications or situations requiring instantaneous inference.

##### Learn more

- Release Date: 21 October 2024
- License: Apache 2.0
- https://www.ibm.com/granite
