# llama.cpp Build Information

## Build Details
- **llama.cpp Version**: b7951
- **Build Date**: 2026-04-08 21:33:01 UTC
- **Platform**: macOS (darwin-arm64)
- **Architecture**: ARM64 (Apple Silicon compatible)
- **Minimum macOS Version**: 15.0 (Sequoia)

## Input Parameters
- **llama_cpp_version**: `b7951`
- **minimize_acceleration**: `false`
- **openssl_static**: `true`
- **debug**: `true`

## CMake Compiler Flags Used
```
  -DCMAKE_OSX_ARCHITECTURES=arm64
  -DCMAKE_OSX_DEPLOYMENT_TARGET=15.0
  -DCMAKE_SYSTEM_NAME=Darwin
  -DCMAKE_SYSTEM_PROCESSOR=arm64
  -DBUILD_SHARED_LIBS=OFF
  -DGGML_METAL=OFF
  -DGGML_NATIVE_DEFAULT=OFF
  -DCMAKE_CROSSCOMPILING=TRUE
  -DGGML_NO_ACCELERATE=ON
  -DGGML_SVE=OFF
  -DCMAKE_C_FLAGS="-march=armv8-a -mtune=generic"
  -DCMAKE_BUILD_TYPE=Release
  -DLLAMA_BUILD_EXAMPLES=ON
  -DOPENSSL_USE_STATIC_LIBS=ON
```

## Compiler Flag Explanation
- **-march=armv8-a**: Target baseline ARMv8-A instruction set (compatible with ALL ARM64 CPUs)
- **-mtune=generic**: Optimize for generic ARM processors (not chip-specific like M1/M2/M3/M4)
- **Result**: Binaries work on any ARMv8-A system (Apple Silicon, AWS Graviton, etc.) with reasonable performance

## Included Binaries
- **llama-cli**: Main command-line inference tool
- **llama-quantize**: Model quantization tool
- **llama-server**: HTTP server for model inference
- **llama-run**: ⚠️ Not included (removed after b6808)
- **llama-mtmd-cli**: Multi-turn multi-document CLI tool
- **llama-gguf**: GGUF file inspection and manipulation tool
- **llama-embedding**: Embedding generation tool for text embeddings

## Usage
All binaries are statically linked and should run on any macOS 15.0+ ARM64 system without additional dependencies.

## Build Configuration Summary
- Cross-compiled from x86_64 macOS to ARM64 target
- Software-only operations (hardware acceleration settings per minimize_acceleration flag)
- Maximum compatibility across ARM64 platforms
- Static linking for portability

---
Built with GitHub Actions workflow: https://github.com/IBM/gguf/actions/runs/24159597917
