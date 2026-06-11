<center><img src="https://ollama.com/assets/library/granite3.2/90c5e567-0004-425c-a17a-1b846c2b5d3d" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="200" /></center>

### Granite Guardian 4.1 8B

Granite Guardian 4.1 8B is a specialized safety model fine-tuned from ibm-granite/granite-4.1-8b, designed to judge if the input prompts and the output responses of an LLM-based system meet specified criteria. The model comes pre-baked with certain criteria including but not limited to: jailbreak attempts, profanity, and hallucinations related to tool calls and retrieval augmented generation in agent-based systems. Additionally, the model also allows users to bring their own criteria and tailor the judging behavior to specific use cases.

This version of Granite Guardian is a hybrid thinking model that allows the user to operate in thinking or non-thinking mode. In thinking mode, the model produces detailed reasoning traces through `<think>` ... `</think>` and `<score>` ... `</score>` tags. In non-thinking mode, the model only produces the judgement score through the `<score>` ... `</score>` tags.

It is trained on unique data comprising human annotations and synthetic data informed by internal red-teaming. It outperforms other open-source models in the same space on standard benchmarks.

Key improvements over Granite Guardian 3.3:

- **BYOC capability**: Large gains on instruction-following benchmarks. For example, IFEval multi-constraint BAcc improves from 0.458 to 0.844 (no-think), InfoBench (Human) from 0.535 to 0.706, InfoBench (GPT-4) from 0.585 to 0.726.
- **Best-of-N reward model**: When used as a reward model for best-of-N selection on the verifiable tasks in the JETTS benchmark, Granite Guardian 4.1 8B achieves an overall score of 70.29, outperforming all tested reward models up to 70B parameters.
- **Hybrid thinking**: Supports both thinking mode (with detailed reasoning traces) and non-thinking mode (low-latency yes/no judgements).
- **Function calling**: Stronger hallucination detection in agentic workflows: BAcc improves from 0.74 to 0.79 (no-think).
- **Maintained safety and groundedness**: Competitive with prior releases on OOD safety (F1 0.79 no-think) and RAG groundedness (Avg BAcc 0.76 think).

#### Running

Example of running the default model (i.e., typically, this is the `Q4_K_M` quantization):

```
ollama run ibm/granite4.1-guardian:8b
```

To run other quantizations (e.g., `Q8_0`):

```
ollama run ibm/granite4.1-guardian:8b-q8_0
```

#### Enable Thinking and setting criteria

Use the flag optional boolean flag `--think` with value set to `true`. For example:

```bash
ollama run ibm/granite4.1-guardian:8b-q4_K_M --think=false
```

In addition, the specific `system` criteria type can be specified within the chat session using the `/set` command, once the client is started, with the built-in criteria values listed below (e.g.,  `harm`, `violence`, `"my custom criteria"`, etc.).

##### List of Built-in Criteria {criteria_text}

The model is trained to judge if a text meets any of the criteria below:

- **Harm** (`harm`): Texts deemed universally harmful are those that pose harm across all contexts and audiences.
  - **Social Bias** (`social_bias`): Social bias reflects systemic prejudice against groups defined by shared identity or characteristics. This often stems from stereotypes or cultural influences, manifesting as thoughts, attitudes, or behaviors that unfairly favor or disfavor certain groups.
  - **Jailbreaking** (`jailbreak`): A jailbreak text refers to the deliberate evasion of an AI system's built-in safeguards or ethical boundaries. This practice often involves crafting specific prompts or scenarios intended to manipulate the AI into producing restricted or inappropriate content.
  - **Violence** (`violence`): Violence refers to content that promotes or depicts physical harm to individuals or groups. This includes depictions of assault, self-harm, or the creation of a hostile environment through threats or intimidation.
  - **Profanity** (`profanity`): Profanity refers to the use of language deemed offensive or socially unacceptable in a given context. This primarily includes curse words, swear words, and crude expressions, though it typically excludes slurs or derogatory terms specifically targeting certain groups.
  - **Unethical Behavior**  (`unethical_behavior`): Unethical behavior refers to actions that violate moral or professional standards, particularly those involving exploitation for personal gain or a disregard for others' well-being. This category excludes physical violence or explicit bias and instead encompasses activities like fraud, theft, or the abuse of power.

The model also assesses hallucination within RAG pipelines:

- **Context Relevance** (`context_relevance`): A document is deemed irrelevant when it doesn't contain information pertinent to the query's specific needs. This means the retrieved or provided content fails to adequately address the question at hand. Irrelevant information could be on a different topic, originate from an unrelated field, or simply not offer any valuable insights for crafting a suitable response.
- **Groundedness** (`groundedness`): A text is considered ungrounded or unfaithful if it includes information lacking support from, or directly contradicting, the provided document(s). This risk arises when the text fabricates details, misinterprets the content, or makes unsupported extrapolations beyond what is explicitly stated in the document(s).
- **Answer Relevance**  (`answer_relevance`): A text is considered inadequate if it fails to address or adequately respond to the posed query. This includes providing off-topic information, misinterpreting the query, or omitting key details requested in the query. Information, even if factually sound, is irrelevant if it fails to directly answer or meet the specific intent of the query.

The model is also equipped to detect hallucinations in agentic workflows:

- **Function Calling Hallucination** (`function_call`): Function call hallucination occurs when a text includes function calls that either don't adhere to the correct format defined by the available tools or are inconsistent with the query's requirements. This risk arises from function calls containing incorrect argument names, values, or types that clash with the tool definitions or the query itself. Common examples include calling functions not present in the tool definitions, providing invalid argument values, or attempting to use parameters that don't exist.

**Bring Your Own Criteria (BYOC)** (`"add your custom criteria here"`)

A key improvement in Granite Guardian 4.1 is stronger support for user-defined judging criteria. Beyond the pre-baked safety and hallucination criteria, users can specify arbitrary evaluation rules, such as checking whether a response follows specific formatting instructions, adheres to domain constraints, or satisfies complex multi-part requirements. The model is trained to faithfully apply these custom criteria and return calibrated yes/no judgements.

#### Intended Use

The guardian model must be used strictly for the prescribed scoring mode, which generates yes/no outputs based on the specified template. Any deviation from this intended use may lead to unexpected, potentially unsafe, or harmful outputs. The model may also be prone to such behavior via adversarial attacks.

---

#### Learn more

- Developers: IBM Research
- Release Date: April, 2026
- GitHub Repository: [ibm-granite/granite-guardian](https://github.com/ibm-granite/granite-guardian)
- Website: [https://www.ibm.com/granite/docs/models/guardian](https://www.ibm.com/granite/docs/models/guardian)
- License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
