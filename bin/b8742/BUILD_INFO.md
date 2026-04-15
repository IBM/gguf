# llama.cpp Build Information

## Build Details
- **llama.cpp Version**: b8742
- **Build Date**: 2026-04-15 14:52:14 UTC
- **Platform**: macOS (darwin-arm64)
- **Architecture**: ARM64 (Apple Silicon - M1 optimized)
- **Minimum OS Version**: 15.0 (Sequoia)

## Input Parameters
- **llama_cpp_version**: `b8742`
- **target_platform**: `macos-arm64`
- **minimize_acceleration**: `false`
- **enable_metal**: `true`
- **openssl_static**: `true`
- **debug**: `true`

## CMake Compiler Flags Used
```
  -DCMAKE_OSX_ARCHITECTURES=arm64
  -DCMAKE_OSX_DEPLOYMENT_TARGET=15.0
  -DCMAKE_SYSTEM_NAME=Darwin
  -DCMAKE_SYSTEM_PROCESSOR=arm64
  -DBUILD_SHARED_LIBS=OFF
  -DGGML_METAL=ON
  -DGGML_METAL_EMBED_LIBRARY=ON
  -DGGML_NATIVE_DEFAULT=OFF
  -DCMAKE_CROSSCOMPILING=TRUE
  -DGGML_NO_ACCELERATE=OFF
  -DGGML_ACCELERATE=ON
  -DCMAKE_C_FLAGS="-march=armv8.2-a -mtune=apple-m1"
  -DGGML_SVE=OFF
  -DCMAKE_BUILD_TYPE=Release
  -DLLAMA_BUILD_EXAMPLES=ON
  -DOPENSSL_USE_STATIC_LIBS=ON
```

## Compiler Flag Explanation
- **-march=armv8.2-a**: Target ARMv8.2-A instruction set (M1 baseline, compatible with M1/M2/M3/M4)
- **-mtune=apple-m1**: Optimize for Apple M1 CPU characteristics
- **GGML_ACCELERATE=ON**: Apple Accelerate framework enabled (CPU-optimized BLAS, 2-4x faster)
- **GGML_METAL=ON**: Metal GPU acceleration enabled (10-50x faster on Apple Silicon)
- **GGML_METAL_EMBED_LIBRARY=ON**: Metal shaders embedded in binary (self-contained, no external files)
- **Result**: GPU-accelerated binaries with automatic runtime detection and fallback

## Included Binaries
- **llama-cli**: Main command-line inference tool (conversation mode)
- **llama-completion**: Simple completion tool (no conversation mode, no banner)
- **llama-quantize**: Model quantization tool
- **llama-server**: HTTP server for model inference
- **llama-run**: ⚠️ Not included (removed after b6808)
- **llama-mtmd-cli**: Multi-turn multi-document CLI tool
- **llama-gguf**: GGUF file inspection and manipulation tool
- **llama-embedding**: Embedding generation tool for text embeddings

## Usage
All binaries are statically linked and GPU-accelerated for Apple Silicon. Metal acceleration is automatically detected at runtime - uses GPU on M1/M2/M3/M4, falls back to CPU on other platforms.

## Build Configuration Summary
- Cross-compiled from x86_64 macOS to ARM64 target
- Metal GPU acceleration enabled with embedded shaders
- Apple Accelerate framework enabled for CPU operations
- Automatic runtime detection (GPU on Apple Silicon, CPU fallback elsewhere)
- Optimized for GitHub Actions M1 runners (2026 configuration)
- Compatible with all Apple Silicon (M1/M2/M3/M4)
- Static linking for portability

---
Built with GitHub Actions workflow: https://github.com/IBM/gguf/actions/runs/24460955505
