import sys
import argparse
import json
import os
import re
import subprocess
import tempfile
from typing import Optional

def test_empty_string(value: str):
    if not value:
        raise ValueError("Argument must not be an empty string")
    return value

def extract_version_from_repo_name(repo_name: str) -> str:
    """
    Extract granite major and minor version from repo name.
    e.g., 'granite-4.2-8b' -> '4.2'
    """
    match = re.search(r'granite-(\d+\.\d+)', repo_name)
    return match.group(1) if match else ''

def generate_and_upload_readmes(
    readme_template: str,
    target_repos_json: str,
    target_owner: str,
    name_ext: str,
    hf_token: str,
    debug: bool = False,
) -> None:
    """
    Generate README files from template and upload them to target repositories.
    
    Args:
        readme_template: Path to README template file
        target_repos_json: JSON string representation of target repos list
        target_owner: Target HF organization owner
        name_ext: Repository name extension (e.g., '-GGUF')
        hf_token: Hugging Face Hub API access token
        debug: Enable debug output
    """
    
    # Load the template
    if not os.path.exists(readme_template):
        print(f"ERROR: README template not found: {readme_template}")
        sys.exit(1)
    
    with open(readme_template) as f:
        template = f.read()
    
    if debug:
        print(f"[DEBUG] Loaded template from: {readme_template}")
    
    # Parse the repos JSON
    try:
        repos = json.loads(target_repos_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse repos JSON: {e}")
        sys.exit(1)
    
    if not isinstance(repos, list):
        print(f"ERROR: Expected repos to be a list, got {type(repos)}")
        sys.exit(1)
    
    if len(repos) == 0:
        print("[INFO] No repositories to process")
        return
    
    # Process each source repository
    for source_repo in repos:
        try:
            # source_repo: e.g., 'ibm-granite/granite-4.2-8b'
            repo_name = source_repo.split('/')[-1]  # 'granite-4.2-8b'
            target_repo_id = f'{target_owner}/{repo_name}{name_ext}'  # e.g., 'ibm-granite/granite-4.2-8b-GGUF'
            base_model_url = f'https://huggingface.co/{source_repo}'
            
            # Extract version from repo name
            effective_version = extract_version_from_repo_name(repo_name)
            
            if debug:
                print(f"[DEBUG] Processing: source_repo={source_repo}")
                print(f"[DEBUG]   repo_name={repo_name}")
                print(f"[DEBUG]   target_repo_id={target_repo_id}")
                print(f"[DEBUG]   effective_version={effective_version}")
            
            # Generate README content
            readme_content = (template
                .replace('${GRANITE_MODEL_VERSION}', effective_version)
                .replace('${HUGGINGFACE_MODEL_ORG_REPO_NAME}', source_repo)
                .replace('${HUGGINGFACE_MODEL_REPO_NAME}', repo_name)
                .replace('${HUGGINGFACE_BASE_MODEL_URL}', base_model_url)
            )
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
                tmp.write(readme_content)
                tmp_path = tmp.name
            
            print(f'[INFO] Generated README for {target_repo_id}:')
            print(readme_content)
            
            # Upload via hf_model_file_upload.py
            result = subprocess.run(
                [
                    'python', './scripts/hf_model_file_upload.py',
                    target_repo_id,
                    tmp_path,
                    hf_token,
                    '--path-in-repo', 'README.md',
                    '--commit-message', 'Add README.md from IBM Granite GGUF CI',
                ],
                capture_output=False,
            )
            
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except Exception as e:
                print(f"[WARNING] Failed to remove temporary file {tmp_path}: {e}")
            
            if result.returncode != 0:
                print(f'[ERROR] Failed to upload README to {target_repo_id} (exit {result.returncode})')
                sys.exit(result.returncode)
            
            print(f'[SUCCESS] README uploaded to {target_repo_id}')
        
        except Exception as e:
            print(f"[ERROR] Exception processing repo {source_repo}: {e}")
            sys.exit(1)
    
    print('[INFO] All READMEs generated and uploaded successfully.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and upload README files to HuggingFace repositories",
        exit_on_error=False
    )
    
    try:
        if len(sys.argv) > 1:
            print(f"[DEBUG] argv: {sys.argv}")
        
        parser.add_argument(
            "readme_template",
            type=test_empty_string,
            help="Path to README template file"
        )
        parser.add_argument(
            "target_repos",
            type=test_empty_string,
            help="JSON string representation of target repositories list"
        )
        parser.add_argument(
            "target_owner",
            type=test_empty_string,
            help="Target HuggingFace organization owner"
        )
        parser.add_argument(
            "hf_token",
            type=test_empty_string,
            help="Hugging Face Hub API access token"
        )
        parser.add_argument(
            "--name-ext",
            type=test_empty_string,
            default="",
            help="Repository name extension (e.g., '-GGUF')"
        )
        parser.add_argument(
            "--debug",
            default=False,
            action='store_true',
            help="Enable debug output"
        )
        
        args = parser.parse_args()
        
        if args.debug:
            print(f">> readme_template='{args.readme_template}'")
            print(f">> target_repos='{args.target_repos}'")
            print(f">> target_owner='{args.target_owner}'")
            print(f">> name_ext='{args.name_ext}'")
            print(f">> hf_token='***' (length: {len(args.hf_token)})")
        
        generate_and_upload_readmes(
            readme_template=args.readme_template,
            target_repos_json=args.target_repos,
            target_owner=args.target_owner,
            name_ext=args.name_ext,
            hf_token=args.hf_token,
            debug=args.debug,
        )
    
    except SystemExit as se:
        if se.code != 0:
            print(f"Usage: {parser.format_usage()}")
            sys.exit(se.code if se.code is not None else 1)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Usage: {parser.format_usage()}")
        sys.exit(2)
    
    sys.exit(0)
