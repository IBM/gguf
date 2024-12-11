
from huggingface_hub import hf_hub_download

# Specify the model repository ID and filename
repo_org = "ibm-granite"
repo_name = "granite-rag-3.0-8b-lora"
repo_id = repo_org + "/" + repo_name
# filename = "config.json"

# Download the file
hf_hub_download(repo_id=repo_id)

# lora_folder = huggingface_hub.snapshot_download(repo_id="ibm-granite/granite-rag-3.0-8b-lora")
# base_folder = huggingface_hub.snapshot_download(repo_id="ibm-granite/granite-3.0-8b-instruct", allow_patterns="*.json")