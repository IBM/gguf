#!/usr/bin/env python3
"""
Extract keywords from embedding tensor data using tokenizer.
Converts embedding logits to top-k keywords using sparse sentence transformer approach.
"""

import sys
import json
import argparse
import os


def extract_keywords(tensor_file, model_repo_id, max_tokens=20, hf_token=None):
    """
    Extract keywords from embedding tensors using the model's tokenizer.

    Args:
        tensor_file: Path to JSON file containing tensor arrays
        model_repo_id: HuggingFace model repository ID (e.g., 'ibm-granite/granite-embedding-30m-english')
        max_tokens: Number of top keywords to extract
        hf_token: Optional HuggingFace token for private repos

    Returns:
        int: 0 if successful, 1 if error
    """
    try:
        import torch
        from transformers.models.auto.tokenization_auto import AutoTokenizer
    except ImportError as e:
        print(f"[ERROR] Required library not installed: {e}")
        print("[INFO] Please install with: pip install torch transformers")
        return 1

    print(f"[INFO] Loading tensor data from: {tensor_file}")
    print(f"[INFO] Loading tokenizer from HuggingFace: {model_repo_id}")
    print(f"[INFO] Max tokens to extract: {max_tokens}")
    print()

    try:
        # Load the tokenizer from HuggingFace Hub
        # This only downloads tokenizer files (config, vocab, etc.), not model weights
        print("[INFO] Loading tokenizer from HuggingFace Hub...")
        tokenizer = AutoTokenizer.from_pretrained(model_repo_id, token=hf_token)
        print(f"[SUCCESS] Tokenizer loaded (vocab size: {tokenizer.vocab_size})")
        print()

        # Load tensor data
        with open(tensor_file, 'r') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("[ERROR] Expected JSON file to contain a list of embedding arrays")
            return 1

        if len(data) == 0:
            print("[ERROR] JSON file contains empty list")
            return 1

        print(f"[INFO] Found {len(data)} embedding array(s)")
        print()

        # Process each embedding array
        for idx, embedding_array in enumerate(data):
            print(f"{'='*80}")
            print(f"Embedding Array {idx}")
            print(f"{'='*80}")

            if not isinstance(embedding_array, list):
                print(f"[WARNING] Embedding at index {idx} is not a list, skipping...")
                continue

            # Convert to PyTorch tensor
            try:
                # The embedding from llama-embedding is already the processed logits
                # We treat it as the hidden_state output (vocabulary-sized vector)
                hidden_state = torch.tensor(embedding_array, dtype=torch.float32)
                print(f"Tensor shape: {hidden_state.shape}")
                print(f"Tensor dtype: {hidden_state.dtype}")
                print()
            except Exception as e:
                print(f"[ERROR] Failed to convert embedding {idx} to tensor: {e}")
                continue

            # Apply sparse sentence transformer logic
            # The embedding is already the vocabulary-sized logits
            # Apply log(1 + relu(x)) transformation
            maxarg = torch.log(1.0 + torch.relu(hidden_state))

            # Get top-k values and indices
            topk_values, topk_indices = torch.topk(maxarg, k=min(max_tokens, len(maxarg)))

            # Decode indices to keywords
            keywords = []
            for i in range(len(topk_indices)):
                token_id = int(topk_indices[i])
                weight = float(topk_values[i])

                # Decode the token
                try:
                    keyword = tokenizer.decode([token_id])
                    keywords.append((keyword, weight, token_id))
                except Exception as e:
                    print(f"[WARNING] Failed to decode token {token_id}: {e}")
                    keywords.append((f"<token_{token_id}>", weight, token_id))

            # Display results
            print(f"Top {len(keywords)} Keywords (with weights):")
            print(f"{'-'*80}")
            for rank, (keyword, weight, token_id) in enumerate(keywords, 1):
                print(f"{rank:3d}. {keyword:30s} | weight: {weight:8.4f} | token_id: {token_id}")
            print(f"{'-'*80}")
            print()

            # Display just the keywords
            keyword_list = [kw for kw, _, _ in keywords]
            print(f"Keywords only: {keyword_list}")
            print()

        print(f"{'='*80}")
        print("[SUCCESS] Keyword extraction completed successfully!")
        return 0

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Extract keywords from embedding tensor data using tokenizer from HuggingFace.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract with default 20 keywords
  python extract_embedding_keywords.py tensors.json ibm-granite/granite-embedding-30m-english

  # Extract with custom number of keywords
  python extract_embedding_keywords.py tensors.json ibm-granite/granite-embedding-30m-english --max-tokens 50

  # Use HuggingFace token for private repos
  python extract_embedding_keywords.py tensors.json org/private-model --hf-token $HF_TOKEN
        """
    )
    parser.add_argument('tensor_file', help='Input JSON file containing tensor arrays')
    parser.add_argument('model_repo_id', help='HuggingFace model repository ID (e.g., ibm-granite/granite-embedding-30m-english)')
    parser.add_argument('-m', '--max-tokens', type=int, default=20,
                        help='Maximum number of keywords to extract (default: 20)')
    parser.add_argument('--hf-token', dest='hf_token',
                        help='HuggingFace token for private repos (or use HF_TOKEN env var)')

    args = parser.parse_args()

    if args.max_tokens < 1:
        print("[ERROR] max-tokens must be at least 1")
        sys.exit(1)

    # Get HF token from args or environment
    hf_token = args.hf_token or os.environ.get('HF_TOKEN')

    result = extract_keywords(args.tensor_file, args.model_repo_id, args.max_tokens, hf_token)
    sys.exit(result)


if __name__ == "__main__":
    main()

# Made with Bob