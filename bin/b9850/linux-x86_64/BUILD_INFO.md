# llama.cpp Build Information

## Build Details
- **llama.cpp Version**: b9850
- **Build Date**: 2026-07-17 19:53:24 UTC
- **Platform**: Linux (linux-x86_64)
- **Architecture**: x86_64 (Intel/AMD 64-bit)
- **Minimum OS Version**: N/A (portable Linux binary)

## Input Parameters
- **llama_cpp_version**: `b9850`
- **target_platform**: `linux-x86_64`
- **minimize_acceleration**: `false`
- **enable_metal**: `false`
- **openssl_static**: `true`
- **debug**: `false`

## CMake Compiler Flags Used
```
  -DCMAKE_SYSTEM_NAME=Linux
  -DCMAKE_SYSTEM_PROCESSOR=x86_64
  -DBUILD_SHARED_LIBS=OFF
  -DGGML_NATIVE_DEFAULT=OFF
  -DCMAKE_C_FLAGS="-march=x86-64 -mtune=generic"
  -DCMAKE_CXX_FLAGS="-march=x86-64 -mtune=generic"
  -DCMAKE_BUILD_TYPE=Release
  -DLLAMA_BUILD_EXAMPLES=ON
  -DGGML_AVX=ON
  -DGGML_AVX2=ON
  -DGGML_FMA=ON
  -DLLAMA_CURL=OFF
  -DOPENSSL_USE_STATIC_LIBS=ON
```

## Compiler Flag Explanation
- **-march=x86-64**: Target baseline x86-64 instruction set (compatible with ALL x86_64 CPUs)
- **-mtune=generic**: Optimize for generic x86_64 processors
- **Result**: Binaries work on any x86_64 Linux system with reasonable performance

## Included Binaries
- **llama-cli**: Main command-line inference tool (conversation mode)
- **llama-completion**: Simple completion tool (no conversation mode, no banner)
- **llama-quantize**: Model quantization tool
- **llama-server**: HTTP server for model inference
- **llama-run**: ⚠️ Not included (removed after b6808)
- **llama-mtmd-cli**: Multi-turn multi-document CLI tool
- **llama-gguf**: GGUF file inspection and manipulation tool
- **llama-gguf-split**: GGUF file splitting tool for large models
- **llama-embedding**: Embedding generation tool for text embeddings

## Usage
All binaries are statically linked and should run on any modern Linux x86_64 system without additional dependencies.

## Build Configuration Summary
- Native Linux x86_64 build
- Software-only operations (hardware acceleration settings per minimize_acceleration flag)
- Maximum compatibility across x86_64 platforms
- Static linking for portability

---
Built with GitHub Actions workflow: https://github.com/ibm-granite/gguf/actions/runs/29608746140
