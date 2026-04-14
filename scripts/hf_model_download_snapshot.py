import os
import sys
import time
from typing import Optional
from huggingface_hub import snapshot_download

def download_model_snapshot(models_dir:str="", repo_id:str="", allow_patterns:Optional[str]=None, hf_token:Optional[str]=None, max_retries:int=3) -> str:
    print(f">>> models_dir='{models_dir}', repo_id='{repo_id}'")
    if models_dir == "":
        print("models_dir is empty")
        return ""
    if repo_id == "":
        print("repo_id is empty")
        return ""
    local_dir = models_dir + "/" + repo_id
    print(f"local_dir: {local_dir}")

    import datetime

    # Retry logic with exponential backoff
    for attempt in range(max_retries):
        try:
            now = datetime.datetime.now()
            print(now.strftime(f"ATTEMPT {attempt + 1}/{max_retries} - BEFORE: %Y-%m-%d %H:%M:%S"))
            download_dir = snapshot_download(
                    repo_id=repo_id,
                    local_dir=local_dir,
                    allow_patterns=allow_patterns,
                    token=hf_token,
                    resume_download=True,  # Resume partial downloads
                )
            now = datetime.datetime.now()
            print(now.strftime("AFTER: %Y-%m-%d %H:%M:%S"))
            print(f"✅ Download completed successfully on attempt {attempt + 1}")
            return download_dir
        except Exception as e:
            now = datetime.datetime.now()
            print(now.strftime(f"FAILED: %Y-%m-%d %H:%M:%S"))
            print(f"❌ Attempt {attempt + 1}/{max_retries} failed with error: {type(e).__name__}: {str(e)}")

            if attempt < max_retries - 1:
                # Exponential backoff: 10s, 20s, 40s
                wait_time = 10 * (2 ** attempt)
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"❌ All {max_retries} attempts failed. Giving up.")
                raise

    return ""


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len <4:
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <models_dir> <repo_org> <repo_name> [<hf_token>] [<allow_pattern>]")
        # Exit with an error code
        sys.exit(1)

    # Parse input arguments into named params.
    fx_name = sys.argv[0]
    models_dir = sys.argv[1]
    repo_org = sys.argv[2]
    repo_name = sys.argv[3]
    if arg_len >= 5:
        hf_token = sys.argv[4]
    else:
        hf_token = None
    if arg_len == 6:
        allow_patterns = sys.argv[5]
    else:
        allow_patterns = None
    repo_id = repo_org + "/" + repo_name

    # Print input variables being used for this run
    print(f">> {fx_name}: models_dir='{models_dir}', repo_org='{repo_org}', repo_name='{repo_name}', hf_token='{hf_token}', allow_patterns='{allow_patterns}'")

    # Note: this downloads everything... TODO: download only the necessary files.
    download_dir = download_model_snapshot(models_dir=models_dir, repo_id=repo_id, hf_token=hf_token, allow_patterns=allow_patterns)

    # Print output variables for this run
    print(f"download_dir: {download_dir}")

    # Exit successfully
    sys.exit(0)
