#!/usr/bin/env python3
"""
Test embedding model quality using Milvus for RAG (Retrieval-Augmented Generation).

This script:
1. Sets up Milvus Lite (lightweight, no Docker required)
2. Creates embeddings for a test document corpus
3. Performs semantic search queries
4. Validates retrieval quality with human-readable results

Usage:
    python test_embedding_rag_milvus.py <model_path> --llama-embedding-bin <path>

Example:
    python test_embedding_rag_milvus.py models/granite-embedding.gguf \
        --llama-embedding-bin ./bin/llama-embedding \
        --top-k 3 \
        --min-score 0.5
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple

try:
    from pymilvus import MilvusClient, DataType
except ImportError:
    print("ERROR: pymilvus not installed. Install with: pip install pymilvus")
    sys.exit(1)


# Test corpus: Documents covering different topics
TEST_CORPUS = [
    {
        "id": 1,
        "topic": "AI",
        "text": "Artificial intelligence was founded as an academic discipline in 1956. It focuses on creating intelligent machines that can simulate human thinking."
    },
    {
        "id": 2,
        "topic": "AI",
        "text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed."
    },
    {
        "id": 3,
        "topic": "AI",
        "text": "Deep learning uses neural networks with multiple layers to progressively extract higher-level features from raw input data."
    },
    {
        "id": 4,
        "topic": "Food",
        "text": "Pizza is a popular Italian dish consisting of a flat round base of dough topped with tomato sauce, cheese, and various toppings."
    },
    {
        "id": 5,
        "topic": "Food",
        "text": "Sushi is a traditional Japanese dish featuring vinegared rice combined with raw fish, vegetables, and sometimes tropical fruits."
    },
    {
        "id": 6,
        "topic": "Sports",
        "text": "Basketball is a team sport where two teams of five players try to score points by throwing a ball through a hoop."
    },
    {
        "id": 7,
        "topic": "Sports",
        "text": "Soccer, also known as football, is the world's most popular sport played between two teams of eleven players with a spherical ball."
    },
    {
        "id": 8,
        "topic": "Technology",
        "text": "Cloud computing delivers computing services including servers, storage, databases, networking, and software over the internet."
    },
]

# Test queries with expected relevant document topics
TEST_QUERIES = [
    {
        "query": "What is artificial intelligence?",
        "expected_topics": ["AI"],
        "unexpected_topics": ["Food", "Sports"],
        "description": "AI-related query should retrieve AI documents"
    },
    {
        "query": "Tell me about machine learning and neural networks",
        "expected_topics": ["AI"],
        "unexpected_topics": ["Food", "Sports"],
        "description": "ML/DL query should retrieve AI documents"
    },
    {
        "query": "What are some popular foods?",
        "expected_topics": ["Food"],
        "unexpected_topics": ["AI", "Sports"],
        "description": "Food query should retrieve food documents"
    },
    {
        "query": "Which sports involve a ball?",
        "expected_topics": ["Sports"],
        "unexpected_topics": ["Food"],
        "description": "Sports query should retrieve sports documents"
    },
]


def generate_embedding(model_path: str, text: str, llama_bin: str, output_format: str = "json") -> List[float]:
    """Generate embedding for text using llama-embedding binary."""
    try:
        # Run llama-embedding
        result = subprocess.run(
            [llama_bin, "-m", model_path, "--embd-output-format", output_format, "-p", text],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse JSON output
        output = result.stdout.strip()
        data = json.loads(output)

        # Extract embedding array
        if isinstance(data, list) and len(data) > 0:
            if "embedding" in data[0]:
                return data[0]["embedding"]

        raise ValueError(f"Unexpected output format: {output[:200]}")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: llama-embedding failed: {e.stderr}")
        raise
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON output: {e}")
        print(f"Output: {result.stdout[:500]}")
        raise


def setup_milvus_collection(client: MilvusClient, collection_name: str, dimension: int):
    """Create Milvus collection for storing embeddings."""
    # Drop existing collection if it exists
    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    # Create collection with schema
    client.create_collection(
        collection_name=collection_name,
        dimension=dimension,
        metric_type="COSINE",  # Use cosine similarity
        auto_id=False
    )

    print(f"✓ Created Milvus collection: {collection_name} (dimension: {dimension})")


def insert_documents(client: MilvusClient, collection_name: str, documents: List[Dict],
                     model_path: str, llama_bin: str) -> int:
    """Generate embeddings for documents and insert into Milvus."""
    print(f"\n[INFO] Generating embeddings for {len(documents)} documents...")

    data = []
    for doc in documents:
        print(f"  - Processing doc {doc['id']}: {doc['text'][:60]}...")
        embedding = generate_embedding(model_path, doc['text'], llama_bin)

        data.append({
            "id": doc["id"],
            "vector": embedding,
            "text": doc["text"],
            "topic": doc["topic"]
        })

    # Insert into Milvus
    client.insert(collection_name=collection_name, data=data)

    dimension = len(data[0]["vector"])
    print(f"✓ Inserted {len(data)} documents (embedding dimension: {dimension})")

    return dimension


def search_and_validate(client: MilvusClient, collection_name: str, query_info: Dict,
                       model_path: str, llama_bin: str, top_k: int, min_score: float) -> Tuple[bool, str]:
    """Perform semantic search and validate results."""
    query = query_info["query"]
    expected_topics = query_info["expected_topics"]
    unexpected_topics = query_info["unexpected_topics"]
    description = query_info["description"]

    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print(f"Expected: {', '.join(expected_topics)} | Unexpected: {', '.join(unexpected_topics)}")
    print(f"{'='*80}")

    # Generate query embedding
    query_embedding = generate_embedding(model_path, query, llama_bin)

    # Search in Milvus
    results = client.search(
        collection_name=collection_name,
        data=[query_embedding],
        limit=top_k,
        output_fields=["text", "topic"]
    )

    # Analyze results
    print(f"\nTop {top_k} Retrieved Documents:")
    print("-" * 80)

    retrieved_topics = []
    all_passed = True
    messages = []

    for i, hit in enumerate(results[0], 1):
        score = hit["distance"]  # Cosine similarity (higher is better)
        text = hit["entity"]["text"]
        topic = hit["entity"]["topic"]
        retrieved_topics.append(topic)

        # Check if score meets minimum threshold
        score_status = "✓" if score >= min_score else "✗"

        print(f"{i}. [Score: {score:.4f}] {score_status} Topic: {topic}")
        print(f"   Text: {text[:100]}...")

        if score < min_score:
            all_passed = False
            messages.append(f"Document {i} score {score:.4f} below threshold {min_score}")

    # Validate topic relevance
    print(f"\n{'='*80}")
    print("Validation Results:")
    print("-" * 80)

    # Check if expected topics are present
    expected_found = any(topic in retrieved_topics for topic in expected_topics)
    if expected_found:
        print(f"✓ PASS: Found expected topics: {', '.join(set(retrieved_topics) & set(expected_topics))}")
    else:
        print(f"✗ FAIL: Expected topics not found: {', '.join(expected_topics)}")
        all_passed = False
        messages.append(f"Expected topics {expected_topics} not in retrieved topics {retrieved_topics}")

    # Check if unexpected topics are absent
    unexpected_found = [topic for topic in unexpected_topics if topic in retrieved_topics]
    if unexpected_found:
        print(f"✗ FAIL: Found unexpected topics: {', '.join(unexpected_found)}")
        all_passed = False
        messages.append(f"Unexpected topics found: {unexpected_found}")
    else:
        print(f"✓ PASS: No unexpected topics found")

    # Overall result
    if all_passed:
        print(f"\n✓ OVERALL: PASS - {description}")
        return True, f"PASS: {description}"
    else:
        print(f"\n✗ OVERALL: FAIL - {description}")
        return False, f"FAIL: {description} | " + " | ".join(messages)


def main():
    parser = argparse.ArgumentParser(
        description="Test embedding model quality using Milvus RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("model_path", help="Path to GGUF embedding model")
    parser.add_argument("--llama-embedding-bin", required=True, help="Path to llama-embedding binary")
    parser.add_argument("--top-k", type=int, default=3, help="Number of documents to retrieve (default: 3)")
    parser.add_argument("--min-score", type=float, default=0.5, help="Minimum similarity score (default: 0.5)")
    parser.add_argument("--collection-name", default="test_embeddings", help="Milvus collection name")

    args = parser.parse_args()

    # Validate inputs
    if not Path(args.model_path).exists():
        print(f"ERROR: Model file not found: {args.model_path}")
        sys.exit(1)

    if not Path(args.llama_embedding_bin).exists():
        print(f"ERROR: llama-embedding binary not found: {args.llama_embedding_bin}")
        sys.exit(1)

    print("="*80)
    print("Milvus RAG Testing for Embedding Models")
    print("="*80)
    print(f"Model: {args.model_path}")
    print(f"Binary: {args.llama_embedding_bin}")
    print(f"Top-K: {args.top_k}")
    print(f"Min Score: {args.min_score}")
    print("="*80)

    # Setup Milvus Lite (uses local file storage)
    with tempfile.TemporaryDirectory() as tmpdir:
        milvus_db = Path(tmpdir) / "milvus_demo.db"
        print(f"\n[INFO] Initializing Milvus Lite: {milvus_db}")

        client = MilvusClient(str(milvus_db))

        # Generate embeddings and get dimension
        print("\n[INFO] Step 1: Generating embeddings for test corpus...")
        dimension = insert_documents(client, args.collection_name, TEST_CORPUS,
                                     args.model_path, args.llama_embedding_bin)

        # Run test queries
        print("\n[INFO] Step 2: Running semantic search queries...")
        results = []

        for query_info in TEST_QUERIES:
            passed, message = search_and_validate(
                client, args.collection_name, query_info,
                args.model_path, args.llama_embedding_bin,
                args.top_k, args.min_score
            )
            results.append((passed, message))

        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)

        passed_count = sum(1 for passed, _ in results if passed)
        total_count = len(results)

        for i, (passed, message) in enumerate(results, 1):
            status = "✓" if passed else "✗"
            print(f"{status} Test {i}: {message}")

        print("-" * 80)
        print(f"Results: {passed_count}/{total_count} tests passed")

        if passed_count == total_count:
            print("\n✓ SUCCESS: All RAG tests passed!")
            print("The embedding model successfully retrieves relevant documents for queries.")
            return 0
        else:
            print(f"\n✗ FAILURE: {total_count - passed_count} test(s) failed")
            print("The embedding model may not be suitable for RAG applications.")
            return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
