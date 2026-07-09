# llama.cpp Build b6569

## Build Information

- **llama.cpp Version:** b6569
- **Release Date:** September 24, 2025
- **Release URL:** https://github.com/ggml-org/llama.cpp/releases/tag/b6569

## Description

This directory contains llama.cpp binaries built from the b6569 release tag. These binaries are used for GGUF model conversion, quantization, and testing in the IBM Granite GGUF workflows.

## Verified Compatibility

This build version has been successfully tested with:
- **Granite 4.0 Language Models** (see top-level README.md for full list)
- **HuggingFace Transformers:** 4.57.3

## Binaries

The following llama.cpp tools are included in this directory:
- `llama-cli` - Command-line interface for model inference
- `llama-quantize` - Model quantization tool
- `llama-run` - Model runner utility
- `llama-server` - HTTP server for model serving

## Usage

These binaries are referenced by the GitHub Actions workflows for automated model conversion and testing. They can also be used locally for manual model operations.

For more information about llama.cpp, visit: https://github.com/ggml-org/llama.cpp