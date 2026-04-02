#!/usr/bin/env python3
"""
Test embedding baseline using original HuggingFace model.
Generates embeddings and computes similarity scores to establish baseline metrics
before GGUF conversion and quantization.

This script:
1. Loads the original HF model with transformers
2. Generates embeddings for test sentences
3. Computes cosine similarity
4. Saves results to JSON for comparison with quantized models
"""

import sys
import json
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    vec1 = np.array(vec1, dtype=np.float32)
    vec2 = np.array(vec2, dtype=np.float32)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def load_model_and_tokenizer(model_path, trust_remote_code=True):
    """Load HuggingFace model and tokenizer."""
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch

        print(f"[INFO] Loading model from: {model_path}")
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=trust_remote_code)
        model = AutoModel.from_pretrained(model_path, trust_remote_code=trust_remote_code)

        # Move to CPU and set to eval mode
        model = model.cpu()
        model.eval()

        print(f"[INFO] Model loaded successfully")
        print(f"[INFO] Model type: {type(model).__name__}")

        return tokenizer, model
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        raise


def generate_embedding(text, tokenizer, model, normalize=True):
    """Generate embedding for a text using HuggingFace model."""
    import torch

    # Tokenize
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Generate embedding
    with torch.no_grad():
        outputs = model(**inputs)

        # Use mean pooling on last hidden state
        # Shape: (batch_size, seq_len, hidden_size)
        last_hidden_state = outputs.last_hidden_state

        # Mean pooling: average over sequence length
        # Shape: (batch_size, hidden_size)
        embedding = torch.mean(last_hidden_state, dim=1)

        # Convert to numpy
        embedding = embedding.cpu().numpy()[0]

        # Normalize if requested
        if normalize:
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

    return embedding.tolist()


def run_baseline_tests(model_path, test_sentences, output_file=None, trust_remote_code=True):
    """
    Run baseline similarity tests on original HF model.

    Args:
        model_path: Path to HuggingFace model
        test_sentences: List of test sentences
        output_file: Optional path to save results JSON
        trust_remote_code: Whether to trust remote code for model loading

    Returns:
        dict: Test results including embeddings and similarity scores
    """
    print("[INFO] ==========================================")
    print("[INFO] Baseline Embedding Test (HuggingFace)")
    print("[INFO] ==========================================")
    print(f"[INFO] Model: {model_path}")
    print(f"[INFO] Test sentences: {len(test_sentences)}")
    print("[INFO] ==========================================")
    print()

    # Load model
    tokenizer, model = load_model_and_tokenizer(model_path, trust_remote_code)

    # Generate embeddings
    print("[INFO] Generating embeddings...")
    embeddings = []
    for i, sentence in enumerate(test_sentences, 1):
        print(f"[INFO] Sentence {i}: {sentence}")
        embedding = generate_embedding(sentence, tokenizer, model)
        embeddings.append(embedding)
        print(f"       Dimensions: {len(embedding)}")
        print(f"       L2 Norm: {np.linalg.norm(embedding):.4f}")
        print()

    # Compute similarities
    print("[INFO] ==========================================")
    print("[INFO] Computing Similarity Scores")
    print("[INFO] ==========================================")

    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            similarities.append({
                "sentence1_idx": i,
                "sentence2_idx": j,
                "sentence1": test_sentences[i],
                "sentence2": test_sentences[j],
                "similarity": sim
            })
            print(f"Sentence {i+1} vs Sentence {j+1}:")
            print(f"  Cosine Similarity: {sim:.4f}")
            print()

    # Prepare results
    results = {
        "model_path": model_path,
        "model_type": "huggingface_baseline",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "test_sentences": test_sentences,
        "embedding_dimension": len(embeddings[0]),
        "embeddings": embeddings,
        "similarities": similarities,
        "summary": {
            "avg_similarity": float(np.mean([s["similarity"] for s in similarities])),
            "min_similarity": float(np.min([s["similarity"] for s in similarities])),
            "max_similarity": float(np.max([s["similarity"] for s in similarities]))
        }
    }

    print("[INFO] ==========================================")
    print("[INFO] Summary")
    print("[INFO] ==========================================")
    print(f"Average Similarity: {results['summary']['avg_similarity']:.4f}")
    print(f"Min Similarity: {results['summary']['min_similarity']:.4f}")
    print(f"Max Similarity: {results['summary']['max_similarity']:.4f}")
    print("[INFO] ==========================================")

    # Save results
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"[INFO] Results saved to: {output_file}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Test embedding baseline using original HuggingFace model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with default sentences
  python test_embedding_baseline_hf.py ibm-granite/granite-embedding-30m-english

  # Test with custom sentences and save results
  python test_embedding_baseline_hf.py ibm-granite/granite-embedding-30m-english \\
    --sentences "AI is great" "Machine learning" "Pizza" \\
    --output baseline_results.json

  # Test with local model path
  python test_embedding_baseline_hf.py ./models/granite-embedding-30m-english \\
    --output results.json
        """
    )
    parser.add_argument('model_path',
                        help='Path to HuggingFace model (local or hub)')
    parser.add_argument('--sentences', nargs='+',
                        help='Test sentences (default: AI, AI similar, Pizza)')
    parser.add_argument('-o', '--output',
                        help='Output JSON file for results')
    parser.add_argument('--no-trust-remote-code', action='store_true',
                        help='Do not trust remote code (default: trust)')

    args = parser.parse_args()

    # Default test sentences
    if args.sentences:
        test_sentences = args.sentences
    else:
        test_sentences = [
            "Artificial intelligence was founded as an academic discipline in 1956.",
            "AI started as an academic field in the 1950s.",
            "I enjoy eating pizza for dinner."
        ]

    try:
        results = run_baseline_tests(
            args.model_path,
            test_sentences,
            output_file=args.output,
            trust_remote_code=not args.no_trust_remote_code
        )

        print()
        print("[SUCCESS] Baseline test completed successfully!")
        sys.exit(0)

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob