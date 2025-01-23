import os
import sys
from huggingface_hub import hf_hub_download, snapshot_download, list_repo_files
from typing import List
import requests

from huggingface_hub import list_collections

hf_token=os.environ['HF_TOKEN']

collections = list_collections(owner="mrutkows", token=hf_token)

for collection in collections:
  print(f"title: `{collection.title}`, private: {collection.private}, description: `{collection.description}`, slug: `{collection.slug}`")

from huggingface_hub import create_collection

try:
    collection = create_collection(
        title="Test 3.3",
        description="Foo too",
        private=True,
        token=hf_token,
    )
except requests.exceptions.HTTPError as exc:
    print (f"HTTP Error: {exc}")
except requests.exceptions.ConnectionError as exc:
    print (f"Connection Error: {exc}")
except requests.exceptions.Timeout as exc:
    print (f"Timeout Error: {exc}")
except requests.exceptions.RequestException as exc:
    print (f"Something went wrong: {exc}")
else:
    # This block executes if no exception occurs
    print("Request was successful!")

for collection in collections:
  print(f"title: `{collection.title}`, private: {collection.private}, description: `{collection.description}`, slug: `{collection.slug}`")

