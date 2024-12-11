import sys
from huggingface_hub import hf_hub_download, snapshot_download

# Specify the model repository ID and filename
TEST_REPO_ORG = "ibm-granite"
TEST_REPO_NAME = "granite-rag-3.0-8b-lora"
models_dir = "models"

# Download the file
def download_model(models_dir=models_dir, repo_id=""):
    print(f">>> models_dir: {models_dir}, repo_id: {repo_id}")
    if repo_id == "":
        print("repo_id is empty")
        return
    local_dir = models_dir + "/" + repo_id
    print(f"local_dir: {local_dir}")
    folder = snapshot_download(repo_id=repo_id, local_dir=local_dir)
    print(f"folder: {folder}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_model_from_hf.py <repo_org> <repo_name>")
    else:
        repo_org = sys.argv[1]
        repo_name = sys.argv[2]
        repo_id = repo_org + "/" + repo_name
        print(f">>> repo_org: {repo_org}, repo_name: {repo_name}, repo_id: {repo_id}")
        download_model(models_dir=models_dir, repo_id=repo_id)
