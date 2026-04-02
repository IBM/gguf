#!/usr/bin/env python3
"""
Test embedding similarity for dense embedding models.
Computes cosine similarity between test sentences to verify semantic understanding.

This script can be used for:
1. Embedding model BVT - verify semantic similarity is captured
2. LLM quantization drift analysis - compare embeddings before/after quantization
3. Model evaluation - test against benchmark datasets
"""

import sys
import json
import argparse
import numpy as np
from pathlib import Path


def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.

    Args:
        vec1: First vector (list or numpy array)
        vec2: Second vector (list or numpy array)

    Returns:
        float: Cosine similarity score between -1 and 1
    """
    vec1 = np.array(vec1, dtype=np.float32)
    vec2 = np.array(vec2, dtype=np.float32)

    # Compute dot product
    dot_product = np.dot(vec1, vec2)

    # Compute magnitudes
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # Compute cosine similarity
    similarity = dot_product / (norm1 * norm2)

    return float(similarity)


def load_embedding(filepath):
    """
    Load embedding from JSON file.

    Args:
        filepath: Path to JSON file containing embedding array

    Returns:
        numpy array: The embedding vector
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected list, got {type(data)}")

    # Handle nested arrays - take first embedding if multiple present
    if len(data) > 0 and isinstance(data[0], list):
        embedding = data[0]
    else:
        embedding = data

    return np.array(embedding, dtype=np.float32)


def test_similarity_pairs(embedding_files, labels=None, expected_similar=True, threshold=0.6, verbose=True):
    """
    Test similarity between pairs of embeddings.

    Args:
        embedding_files: List of paths to JSON files containing embedding arrays
        labels: Optional list of labels for each embedding (for display)
        expected_similar: Whether embeddings should be similar (True) or dissimilar (False)
        threshold: Similarity threshold for pass/fail
        verbose: Print detailed output

    Returns:
        tuple: (passed: bool, avg_similarity: float, similarities: list)
    """
    if len(embedding_files) < 2:
        raise ValueError("Need at least 2 embedding files to compare")

    if labels is None:
        labels = [f"Embedding {i+1}" for i in range(len(embedding_files))]

    if verbose:
        print(f"[INFO] Loading {len(embedding_files)} embeddings...")
        print()

    # Load all embeddings
    embeddings = []
    for i, filepath in enumerate(embedding_files):
        try:
            embedding = load_embedding(filepath)
            embeddings.append(embedding)

            if verbose:
                print(f"[INFO] Loaded {labels[i]}: {filepath}")
                print(f"       Dimensions: {len(embedding)}")
                print(f"       L2 Norm: {np.linalg.norm(embedding):.4f}")
                print()
        except Exception as e:
            print(f"[ERROR] Failed to load {filepath}: {e}")
            raise

    if verbose:
        print(f"{'='*80}")
        print("Similarity Analysis")
        print(f"{'='*80}")

    # Compute pairwise similarities
    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            similarities.append(sim)

            if verbose:
                print(f"{labels[i]} vs {labels[j]}:")
                print(f"  Cosine Similarity: {sim:.4f}")
                print()

    # Compute average similarity
    avg_similarity = float(np.mean(similarities))

    if verbose:
        print(f"Average Similarity: {avg_similarity:.4f}")
        print(f"Min Similarity: {min(similarities):.4f}")
        print(f"Max Similarity: {max(similarities):.4f}")
        print(f"{'='*80}")
        print()

    # Determine pass/fail
    if expected_similar:
        # Embeddings should be similar (high similarity)
        passed = avg_similarity >= threshold
        if verbose:
            if passed:
                print(f"[SUCCESS] ✓ Embeddings are similar (avg: {avg_similarity:.4f} >= {threshold})")
                print("[INFO] This indicates the model correctly captures semantic similarity")
            else:
                print(f"[FAILURE] ✗ Embeddings are not similar enough (avg: {avg_similarity:.4f} < {threshold})")
                print("[INFO] Expected similar sentences to have high similarity")
    else:
        # Embeddings should be dissimilar (low similarity)
        # For dissimilar test, threshold represents the maximum acceptable similarity
        passed = avg_similarity < threshold
        if verbose:
            if passed:
                print(f"[SUCCESS] ✓ Embeddings are dissimilar (avg: {avg_similarity:.4f} < {threshold})")
                print("[INFO] This indicates the model correctly distinguishes different topics")
            else:
                print(f"[FAILURE] ✗ Embeddings are too similar (avg: {avg_similarity:.4f} >= {threshold})")
                print("[INFO] Expected dissimilar sentences to have low similarity")

    return passed, avg_similarity, similarities


def main():
    parser = argparse.ArgumentParser(
        description='Test embedding similarity for dense embedding models and quantization drift analysis.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test that two similar sentences have high similarity
  python test_embedding_similarity.py emb1.json emb2.json --similar --threshold 0.6

  # Test that two dissimilar sentences have low similarity
  python test_embedding_similarity.py emb1.json emb3.json --dissimilar --threshold 0.4

  # Compare multiple embeddings with labels
  python test_embedding_similarity.py emb1.json emb2.json emb3.json \\
    --labels "Original" "Quantized Q4" "Quantized Q8" --similar

  # Quantization drift analysis
  python test_embedding_similarity.py original.json quantized.json \\
    --labels "BF16" "Q4_K_M" --similar --threshold 0.95
        """
    )
    parser.add_argument('embedding_files', nargs='+',
                        help='JSON files containing embedding arrays (at least 2 required)')
    parser.add_argument('--labels', nargs='+',
                        help='Labels for each embedding (for display purposes)')
    parser.add_argument('--similar', dest='expected_similar', action='store_true',
                        help='Expect embeddings to be similar (default)')
    parser.add_argument('--dissimilar', dest='expected_similar', action='store_false',
                        help='Expect embeddings to be dissimilar')
    parser.add_argument('-t', '--threshold', type=float, default=0.6,
                        help='Similarity threshold for pass/fail (default: 0.6)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress detailed output, only show pass/fail')

    parser.set_defaults(expected_similar=True)

    args = parser.parse_args()

    # Validate arguments
    if args.threshold < 0 or args.threshold > 1:
        print("[ERROR] Threshold must be between 0 and 1")
        sys.exit(1)

    if args.labels and len(args.labels) != len(args.embedding_files):
        print(f"[ERROR] Number of labels ({len(args.labels)}) must match number of files ({len(args.embedding_files)})")
        sys.exit(1)

    # Run similarity test
    try:
        passed, avg_sim, similarities = test_similarity_pairs(
            args.embedding_files,
            labels=args.labels,
            expected_similar=args.expected_similar,
            threshold=args.threshold,
            verbose=not args.quiet
        )

        sys.exit(0 if passed else 1)

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob