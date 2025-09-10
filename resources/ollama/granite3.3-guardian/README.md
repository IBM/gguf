<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite guardian models

The IBM Granite Guardian 3.3 models are designed to detect risks in prompts and/or responses. They can help with risk detection along many key dimensions catalogued in the [IBM AI Risk Atlas](https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas). They are trained on unique data comprising human annotations and synthetic data informed by internal red-teaming, and they outperform other open-source models in the same space on standard benchmarks.

#### Granite Guardian 3.3 8b

Granite Guardian 3.3 8b is a specialized Granite 3.3 8B model designed to judge if the input prompts and the output responses of an LLM based system meet specified criteria. The model comes pre-baked with certain criteria including but not limited to: jailbreak attempts, profanity, and hallucinations related to tool calls and retrieval augmented generation in agent-based systems. Additionally, the model also allows users to bring their own criteria and tailor the judging behavior to specific use-cases.

This version of Granite Guardian is a hybrid thinking model that allows the user to operate in thinking or non-thinking model. In thinking mode, the model produces detailed reasoning traces though <think> ... </think> and <score> ... </score> tags. In non-thinking mode, the model only produces the judgement score though the <score> ... </score> tags.

It is trained on unique data comprising human annotations and synthetic data informed by internal red-teaming. It outperforms other open-source models in the same space on standard benchmarks.

#### Running

```
ollama run ibm/granite3.3-guardian:8b >>> /set system violence
```

#### Supported use cases

- Risk detection in prompt text or model response (i.e. as guardrails), such as:

  - Harm (`harm`): content considered generally harmful.
    - *Note: this is the default setting for the model's chat template.*
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

#### Thinking

To enable "thinking" for this model, follow the tooling-specific instructions below.

##### Ollama Python Library

From the Python chat client, which is part of the Ollama Python Library (i.e., https://github.com/ollama/ollama-python), use the `think` keyword argument with value `True`:

```python
model = "ibm/granite3.3-guardian:8b"
messages = [
  {
    "role": "user",
    "content": "hello world",
  },
]

# Note: for Guardian models, the "temperature" parameter must be set to zero (0) to assure accurate assessment and scoring.
response = ollama.chat(
    model=model,
    think=True,
    messages=messages,
    options={"temperature": 0}
)
```

##### Ollama Command Line Interface (CLI)

Use the flag optional boolean flag `--think` with value set to `true`.  In addition, the specific `system` type can be used with the `/set` command once the client is started with the supported values listed above (e.g.,  `harm` `violence`, etc.)

```bash
$ ollama run ibm/granite3.3-guardian:8b --think=true
>>> /set system harm
Set system message.
>>> You suck
Thinking...
To determine whether the provided text "you suck" is universally harmful, I need to analyze it in the
context of potential harm across all contexts and audiences. The term "suck" is generally considered
derogatory and can be offensive or hurtful to individuals. However, the level of harm it poses can vary
depending on the context in which it is used. For instance, in a casual conversation among friends, it might
be seen as playful banter, while in a professional setting, it would be inappropriate and harmful.
...

...done thinking.

<score> yes </score>
```

where a `yes` value within the `<score>` delimiter means the last user message was considered "harmful".

---

#### Learn more

- Release Date: 01 August 2025
- License: Apache 2.0
- https://www.ibm.com/granite
