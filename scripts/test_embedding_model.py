#!/usr/bin/env python3
"""
Test script for Granite embedding models using Hugging Face transformers.
This script implements a sparse sentence transformer for testing embedding models.
"""

import sys
import json
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer


class SparseSentenceTransformer:
    def __init__(self, model_name_or_path, device: str = 'cpu', config_path: str = None):
        # If config_path is provided, load it to get model_type
        if config_path:
            print(f"[INFO] Loading config from: {config_path}")
            with open(config_path, 'r') as f:
                config = json.load(f)
            model_type = config.get('model_type', None)
            print(f"[INFO] Model type from config: {model_type}")

        self.model = AutoModelForMaskedLM.from_pretrained(model_name_or_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.device = device
        self.model.to(device)
        if device == "cuda":
            self.model = self.model.cuda()
            self.model = self.model.bfloat16()

    @torch.no_grad()
    def encode(self, sentences, max_tokens=20):
        if type(sentences) == str:
            sentences = [sentences]

        input_dict = self.tokenizer(sentences, max_length=512, padding=True, return_tensors='pt', truncation=True)
        attention_mask = input_dict['attention_mask']  # (bs,seqlen)

        if self.device == "cuda":
            input_dict['input_ids'] = input_dict['input_ids'].cuda()
            input_dict['attention_mask'] = input_dict['attention_mask'].cuda()
            if 'token_type_ids' in input_dict:
                input_dict['token_type_ids'] = input_dict['token_type_ids'].cuda()

        hidden_state = self.model(**input_dict)[0]

        maxarg = torch.log(1.0 + torch.relu(hidden_state))

        input_mask_expanded = attention_mask.unsqueeze(-1).to(maxarg.device)  # bs * seqlen * voc
        maxdim1 = torch.max(maxarg * input_mask_expanded, dim=1).values  # bs * voc

        # get topk high weights
        topk, indices = torch.topk(maxdim1, k=max_tokens)  # (weight - (bs * max_terms), index - (bs * max_terms))

        expansions = [[(self.tokenizer.decode(int(indices[sidx][tidx])), float(topk[sidx][tidx])) for tidx in range(topk.shape[1])] for sidx in range(topk.shape[0])]

        return expansions


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_embedding_model.py <model_name_or_path> [test_sentence] [max_tokens] [device] [config_path]")
        sys.exit(1)

    model_name_or_path = sys.argv[1]
    test_sentence = sys.argv[2] if len(sys.argv) > 2 else "Artificial intelligence was founded as an academic discipline in 1956."
    max_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    device = sys.argv[4] if len(sys.argv) > 4 else "cpu"
    config_path = sys.argv[5] if len(sys.argv) > 5 else None

    print(f"[INFO] Testing embedding model: {model_name_or_path}")
    print(f"[INFO] Device: {device}")
    print(f"[INFO] Test sentence: {test_sentence}")
    print(f"[INFO] Max tokens: {max_tokens}")
    if config_path:
        print(f"[INFO] Config path: {config_path}")
    print()

    try:
        # Initialize the sparse sentence transformer
        sparse_model = SparseSentenceTransformer(model_name_or_path, device=device, config_path=config_path)

        # Encode the test sentence
        print("[INFO] Encoding sentence...")
        result = sparse_model.encode([test_sentence], max_tokens=max_tokens)

        # Print the results
        print("\n[SUCCESS] Embedding model test completed successfully!")
        print("\n[RESULT] Top-k expansion results:")
        print("=" * 80)
        for expansion in result:
            print(expansion)
        print("=" * 80)

        # Verify the output format
        if result and len(result) > 0 and len(result[0]) > 0:
            print(f"\n[INFO] Generated {len(result[0])} token expansions")
            print(f"[INFO] First expansion: {result[0][0]}")
            print("\n[SUCCESS] Output format validation passed!")
            return 0
        else:
            print("\n[ERROR] Output format validation failed - empty result")
            return 1

    except Exception as e:
        print(f"\n[ERROR] Failed to test embedding model: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
