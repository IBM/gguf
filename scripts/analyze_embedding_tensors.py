#!/usr/bin/env python3
"""
Analyze embedding tensor data from JSON file.
Loads tensor arrays into PyTorch tensors and displays shape and sample data.
"""

import sys
import json
import argparse


def analyze_tensors(json_file, num_rows=5):
    """
    Load tensor data from JSON file and display analysis.

    Args:
        json_file: Path to JSON file containing tensor arrays
        num_rows: Number of rows to display from start and end

    Returns:
        int: 0 if successful, 1 if error
    """
    try:
        import torch
    except ImportError:
        print("[ERROR] PyTorch is not installed. Please install it with: pip install torch")
        return 1

    print(f"[INFO] Loading tensor data from: {json_file}")

    try:
        with open(json_file, 'r') as f:
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
                tensor = torch.tensor(embedding_array, dtype=torch.float32)
            except Exception as e:
                print(f"[ERROR] Failed to convert embedding {idx} to tensor: {e}")
                continue

            # Display tensor information
            print(f"Tensor Shape: {tensor.shape}")
            print(f"Tensor Dtype: {tensor.dtype}")
            print(f"Tensor Device: {tensor.device}")
            print(f"Number of Elements: {tensor.numel()}")
            print()

            # Display statistics
            print(f"Statistics:")
            print(f"  Min value: {tensor.min().item():.6f}")
            print(f"  Max value: {tensor.max().item():.6f}")
            print(f"  Mean value: {tensor.mean().item():.6f}")
            print(f"  Std deviation: {tensor.std().item():.6f}")
            print()

            # Display first N rows
            if len(tensor.shape) == 1:
                # 1D tensor
                print(f"First {min(num_rows, len(tensor))} values:")
                print(tensor[:num_rows])
                print()

                if len(tensor) > num_rows * 2:
                    print(f"Last {min(num_rows, len(tensor))} values:")
                    print(tensor[-num_rows:])
                    print()
            elif len(tensor.shape) == 2:
                # 2D tensor
                print(f"First {min(num_rows, tensor.shape[0])} rows:")
                print(tensor[:num_rows])
                print()

                if tensor.shape[0] > num_rows * 2:
                    print(f"Last {min(num_rows, tensor.shape[0])} rows:")
                    print(tensor[-num_rows:])
                    print()
            else:
                # Multi-dimensional tensor
                print(f"First {num_rows} elements (flattened view):")
                print(tensor.flatten()[:num_rows])
                print()

                if tensor.numel() > num_rows * 2:
                    print(f"Last {num_rows} elements (flattened view):")
                    print(tensor.flatten()[-num_rows:])
                    print()

        print(f"{'='*80}")
        print("[SUCCESS] Tensor analysis completed successfully!")
        return 0

    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_file}")
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
        description='Analyze embedding tensor data from JSON file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze with default 5 rows
  python analyze_embedding_tensors.py tensors.json

  # Analyze with custom number of rows
  python analyze_embedding_tensors.py tensors.json --num-rows 10
        """
    )
    parser.add_argument('json_file', help='Input JSON file containing tensor arrays')
    parser.add_argument('-n', '--num-rows', type=int, default=5,
                        help='Number of rows to display from start and end (default: 5)')

    args = parser.parse_args()

    if args.num_rows < 1:
        print("[ERROR] num-rows must be at least 1")
        sys.exit(1)

    result = analyze_tensors(args.json_file, args.num_rows)
    sys.exit(result)


if __name__ == "__main__":
    main()

# Made with Bob