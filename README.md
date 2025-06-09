---
license: apache-2.0
library_name: transformers
tags:
- language
- granite
- gguf
base_model:
- ${{env.REPO_ORG}}/${{env.REPO_NAME}}
---

> [!NOTE]
> This repository contains models that have been converted to the GGUF format with various quantizations from an IBM Granite base model.
>
> Please reference the base model's full model card here:
> https://huggingface.co/${{env.REPO_ORG}}/${{env.REPO_NAME}}