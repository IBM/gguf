# llama.cpp Build Information

## Build Details
- **llama.cpp Version**: b6808
- **Build Date**: 2026-07-09 21:04:06 UTC
- **Platform**: Linux (linux-arm64)
- **Architecture**: ARM64 (64-bit ARM / aarch64)
- **Minimum OS Version**: N/A (portable Linux arm64 binary)

## Input Parameters
- **llama_cpp_version**: `b6808`
- **target_platform**: `linux-arm64`
- **minimize_acceleration**: `false`
- **enable_metal**: `false`
- **openssl_static**: `true`
- **debug**: `false`

## CMake Compiler Flags Used
```
  -DCMAKE_SYSTEM_NAME=Linux
  -DCMAKE_SYSTEM_PROCESSOR=aarch64
  -DBUILD_SHARED_LIBS=OFF
  -DGGML_NATIVE_DEFAULT=OFF
  -DCMAKE_BUILD_TYPE=Release
  -DLLAMA_BUILD_EXAMPLES=ON
  -DCMAKE_C_FLAGS="-march=armv8.2-a -mtune=generic"
  -DCMAKE_CXX_FLAGS="-march=armv8.2-a -mtune=generic"
  -DGGML_SVE=OFF
  -DLLAMA_CURL=OFF
  -DOPENSSL_USE_STATIC_LIBS=ON
```

## Compiler Flag Explanation
- **-march=armv8.2-a**: Target ARMv8.2-A instruction set (compatible with most modern ARM64 CPUs)
- **-mtune=generic**: Optimize for generic ARM64 processors
- **Result**: Binaries work on any ARMv8.2-A+ Linux arm64 system (AWS Graviton 2+, Ampere Altra, etc.)

## Included Binaries
- **llama-cli**: Main command-line inference tool (conversation mode)
- **llama-completion**: ⚠️ Not included (introduced at b8742)
- **llama-quantize**: Model quantization tool
- **llama-server**: HTTP server for model inference
- **llama-run**: Simple inference runner
- **llama-mtmd-cli**: ⚠️ Not included (introduced at b8742)
- **llama-gguf**: GGUF file inspection and manipulation tool
- **llama-gguf-split**: GGUF file splitting tool for large models
- **llama-embedding**: Embedding generation tool for text embeddings

## Usage
All binaries are statically linked and should run on any modern Linux arm64 system (ARMv8.2-A or newer) without additional dependencies.

## Build Configuration Summary
- Native Linux arm64 build (ubuntu-24.04-arm runner)
- Software-only operations (no GPU acceleration)
- Compatible with AWS Graviton 2/3/4, Ampere Altra, and other ARMv8.2-A+ platforms
- Static linking for portability

---
Built with GitHub Actions workflow: https://github.com/ibm-granite/gguf/actions/runs/29049874668
