# Build llama.cpp Binaries Workflow - Usage Guide

## Overview

The `build-llamacpp-binaries.yml` workflow automates the building of llama.cpp binaries for use in GitHub Actions workflows. It builds statically-linked binaries optimized for GitHub Actions runners on both macOS and Ubuntu platforms.

## Built Binaries

The workflow builds the following 5 binaries:

1. **llama-cli** - Command-line interface for inference
2. **llama-quantize** - Model quantization tool
3. **llama-server** - HTTP server for model serving
4. **llama-mtmd-cli** - Multimodal (MTMD) interface
5. **llama-gguf** - GGUF file inspection and manipulation tool (useful for debugging)

**Note:** `llama-run` was deprecated after llama.cpp release b6808 and is only built for versions b6808 and older.

## Trigger Methods

### 1. Manual Dispatch (Recommended)

Navigate to the Actions tab and manually trigger the workflow:

1. Go to **Actions** → **Build llama.cpp Binaries**
2. Click **Run workflow**
3. Configure inputs:
   - **llama_cpp_version**: Git commit hash or tag (e.g., `b8100`, `b6808`, `master`)
   - **release_tag**: (Optional) Release tag to upload binaries as release assets
   - **debug**: Enable verbose debug output
   - **minimize_acceleration**: Disable all hardware acceleration for maximum compatibility (default: false)
   - **openssl_static**: Force static linking of OpenSSL to avoid runtime dependencies on libssl/libcrypto (default: false)

### 2. Automatic on Release

The workflow automatically runs when a new GitHub release is created or published. Binaries are automatically attached to the release as assets.

### 3. Scheduled Builds

The workflow runs automatically every Sunday at 2 AM UTC to keep binaries up-to-date with the latest llama.cpp version.

## Downloading Built Binaries

### From Workflow Artifacts

1. Navigate to the workflow run in the Actions tab
2. Scroll to the **Artifacts** section at the bottom
3. Download the zip file:
   - `llama-cpp-binaries-{version}.zip`
4. Artifacts are retained for 90 days

### From Release Assets

If the workflow was triggered with a release tag or on a release event:

1. Go to the **Releases** page
2. Find the appropriate release
3. Download the zip files from the **Assets** section
4. Release assets are permanent

## Extracting and Using Binaries

### Extract to bin/ Directory

```bash
# Download and extract the zip file
unzip llama-cpp-b6808.zip -d bin/

# Make binaries executable
chmod +x bin/llama-*
```

### Archive Old Binaries (Optional)

```bash
# Create archive directory with date
mkdir -p bin/archive/$(date +%Y-%m-%d)

# Move old binaries to archive
mv bin/llama-* bin/archive/$(date +%Y-%m-%d)/

# Extract new binaries
unzip llama-cpp-macOS-b6808.zip -d bin/
```

## Build Configuration

### CMake Configuration Flags

The workflow uses the following CMake flags for maximum compatibility across GitHub Actions runners:

```bash
cmake -B build \
  -DBUILD_SHARED_LIBS=OFF \          # Static linking for portability
  -DOPENSSL_USE_STATIC_LIBS=ON \     # Force static OpenSSL (optional, controlled by openssl_static input)
  -DGGML_METAL=OFF \                 # Disable Metal GPU acceleration
  -DGGML_NATIVE_DEFAULT=OFF \        # Disable native CPU optimizations
  -DCMAKE_CROSSCOMPILING=TRUE \      # Cross-compilation compatibility mode
  -DGGML_NO_ACCELERATE=ON \          # Disable Apple Accelerate framework
  -DGGML_SVE=OFF \                   # Disable ARM SVE instructions
  -DCMAKE_BUILD_TYPE=Release \       # Optimized release build
  -DCMAKE_OSX_ARCHITECTURES=arm64 \  # Target ARM64 architecture
  -DCMAKE_OSX_DEPLOYMENT_TARGET=15.0 # Minimum macOS version
```

### Complete CMake Configuration Flags Reference

This section documents all CMake configuration flags used in the workflow, organized by category.

#### Core Build Configuration

| Flag | Default | Description | When to Use |
|------|---------|-------------|-------------|
| `-DCMAKE_BUILD_TYPE=Release` | Release | Build type (Release/Debug/RelWithDebInfo) | Always use Release for production binaries |
| `-DBUILD_SHARED_LIBS=OFF` | OFF | Static vs dynamic linking | Keep OFF for portable binaries |
| `-DCMAKE_CROSSCOMPILING=TRUE` | FALSE | Enable cross-compilation mode | Required when building for different architecture |
| `-DLLAMA_BUILD_EXAMPLES=ON` | ON | Build example binaries (llama-cli, etc.) | Keep ON to build the binaries we need |

#### Platform-Specific Configuration (macOS)

| Flag | Value | Description | When to Use |
|------|-------|-------------|-------------|
| `-DCMAKE_OSX_ARCHITECTURES=arm64` | arm64 | Target architecture | Building for Apple Silicon (M1/M2/M3/M4) |
| `-DCMAKE_OSX_DEPLOYMENT_TARGET=15.0` | 15.0 | Minimum macOS version | Set to lowest macOS version you need to support |
| `-DCMAKE_SYSTEM_NAME=Darwin` | Darwin | Target operating system | Required for macOS cross-compilation |
| `-DCMAKE_SYSTEM_PROCESSOR=arm64` | arm64 | Target processor architecture | Must match CMAKE_OSX_ARCHITECTURES |

#### Compiler Flags

| Flag | Value | Description | When to Use |
|------|-------|-------------|-------------|
| `-DCMAKE_C_FLAGS="-march=armv8-a -mtune=generic"` | Custom | C compiler flags | For maximum ARM64 compatibility |
| `-DCMAKE_CXX_FLAGS="-march=armv8-a -mtune=generic"` | Custom | C++ compiler flags | Applied when minimize_acceleration is enabled |

**Compiler Flag Explanation:**
- `-march=armv8-a`: Target baseline ARMv8-A instruction set (compatible with ALL ARM64 CPUs)
- `-mtune=generic`: Optimize for generic ARM processors (not chip-specific like M1/M2/M3/M4)
- **Result**: Binaries work on any ARMv8-A system (Apple Silicon, AWS Graviton, etc.) with reasonable performance

#### Hardware Acceleration Flags

| Flag | Default | Description | When to Disable |
|------|---------|-------------|-----------------|
| `-DGGML_METAL=OFF` | ON | Apple Metal GPU acceleration | Always OFF for CI/portability |
| `-DGGML_METAL_EMBED_LIBRARY=OFF` | ON | Embed Metal library in binary | When minimize_acceleration is enabled |
| `-DGGML_ACCELERATE=OFF` | ON | Apple Accelerate framework (BLAS) | When minimize_acceleration is enabled |
| `-DGGML_BLAS=OFF` | OFF | Generic BLAS support | When minimize_acceleration is enabled |
| `-DGGML_NATIVE_DEFAULT=OFF` | ON | Native CPU optimizations | Always OFF for portability |
| `-DGGML_NO_ACCELERATE=ON` | OFF | Explicitly disable Accelerate | Always ON for CI builds |
| `-DGGML_SVE=OFF` | OFF | ARM SVE (Scalable Vector Extension) | Always OFF for baseline ARM64 |

#### GPU/Accelerator Backend Flags

These flags control various GPU and accelerator backends. All are disabled in the workflow for maximum compatibility:

| Flag | Default | Description | Workflow Setting |
|------|---------|-------------|------------------|
| `-DGGML_CUDA=OFF` | OFF | NVIDIA CUDA support | Always OFF (no CUDA on macOS) |
| `-DGGML_VULKAN=OFF` | OFF | Vulkan GPU support | Always OFF for portability |
| `-DGGML_KOMPUTE=OFF` | OFF | Kompute GPU compute | Always OFF for portability |
| `-DGGML_SYCL=OFF` | OFF | Intel SYCL support | Always OFF for portability |

#### OpenSSL Configuration

| Flag | Default | Description | When to Enable |
|------|---------|-------------|----------------|
| `-DOPENSSL_USE_STATIC_LIBS=ON` | OFF | Force static OpenSSL linking | Enable via `openssl_static` input when you get OpenSSL dynamic library errors |

**Important**: This flag is controlled by the `openssl_static` workflow input parameter. Enable it if you encounter errors like:
```
dyld: Library not loaded: /opt/homebrew/opt/openssl@3/lib/libssl.3.dylib
dyld: Library not loaded: /opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib
```

### Workflow Input Parameters

The workflow provides several input parameters that control which CMake flags are applied:

| Input Parameter | Type | Default | Effect |
|----------------|------|---------|--------|
| `llama_cpp_version` | string | b8100 | llama.cpp version to build (commit hash or tag) |
| `release_tag` | string | (empty) | Optional release tag for uploading binaries |
| `debug` | boolean | false | Enable verbose debug output in workflow |
| `minimize_acceleration` | boolean | false | Disable ALL hardware acceleration (adds GGML_METAL_EMBED_LIBRARY, GGML_ACCELERATE, GGML_BLAS, GGML_CUDA, GGML_VULKAN, GGML_KOMPUTE, GGML_SYCL flags) |
| `openssl_static` | boolean | false | Force static linking of OpenSSL (adds OPENSSL_USE_STATIC_LIBS flag) |

### Flag Combinations and Use Cases

#### Standard Build (Default)
```bash
# Input parameters: (all defaults)
# Result: Portable binaries with basic optimizations
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DGGML_METAL=OFF \
  -DGGML_NATIVE_DEFAULT=OFF \
  -DGGML_NO_ACCELERATE=ON \
  -DGGML_SVE=OFF
```

#### Maximum Compatibility Build
```bash
# Input parameters: minimize_acceleration=true
# Result: Works on any ARM64 system, no hardware dependencies
cmake -B build \
  [standard flags...] \
  -DGGML_METAL_EMBED_LIBRARY=OFF \
  -DGGML_ACCELERATE=OFF \
  -DGGML_BLAS=OFF \
  -DGGML_CUDA=OFF \
  -DGGML_VULKAN=OFF \
  -DGGML_KOMPUTE=OFF \
  -DGGML_SYCL=OFF
```

#### Fully Portable Build (No External Dependencies)
```bash
# Input parameters: openssl_static=true
# Result: No runtime dependencies on system libraries
cmake -B build \
  [standard flags...] \
  -DOPENSSL_USE_STATIC_LIBS=ON
```

### Why These Flags Matter

These flags are specifically chosen to prevent common issues when running binaries across different systems:

- **Prevents "Illegal instruction" errors**: Older systems may not support advanced SIMD instructions (AVX512, SVE, etc.)
- **Ensures cross-platform compatibility**: Binaries work on both local development machines and CI environments
- **Avoids GPU-specific code**: GitHub runners typically don't have GPU access or Metal support
- **Eliminates runtime dependencies**: Static linking ensures binaries work without requiring specific libraries
- **Maximizes portability**: Binaries can run on a wide range of ARM64 systems without modification

### Understanding Static vs Dynamic Linking

**Dynamic Linking (Default for OpenSSL)**:
- Binary depends on system-installed libraries (e.g., libssl.dylib, libcrypto.dylib)
- Smaller binary size
- Requires matching library versions on target system
- Can cause "Library not loaded" errors if libraries are missing or incompatible

**Static Linking (With `-DOPENSSL_USE_STATIC_LIBS=ON`)**:
- All library code embedded in binary
- Larger binary size
- No external dependencies
- Works on any system regardless of installed libraries
- Recommended for maximum portability

**Note**: `-DBUILD_SHARED_LIBS=OFF` only controls your project's libraries, not external dependencies like OpenSSL. That's why `-DOPENSSL_USE_STATIC_LIBS=ON` is a separate flag.

## Integration with Existing Workflows

Existing workflows in this repository use binaries from the `bin/` directory:

```yaml
- name: quantize-gguf
  run: |
    sudo ./bin/llama-quantize ${{ env.LOCAL_FNAME_CONVERTED_GGUF }} ...
```

After extracting new binaries to `bin/`, existing workflows will automatically use them without modification.

## Troubleshooting

### Binary Not Found Error

If you get "binary not found" errors:

1. Verify the binary was extracted to the correct location
2. Check file permissions: `ls -l bin/llama-*`
3. Make executable if needed: `chmod +x bin/llama-*`

### Build Failures

If the workflow fails:

1. Check the workflow logs for specific error messages
2. Verify the llama.cpp version exists (commit hash or tag)
3. Enable debug mode for more verbose output
4. Check if llama.cpp has breaking changes in the specified version

### Smoke Test Failures

If smoke tests fail but binaries built successfully:

1. The binary may not support `--version` flag
2. Check if the binary requires specific arguments
3. Review the smoke test output in workflow logs

## Version Management

### Recommended Versions

- **Production**: Use stable release tags (e.g., `b8100`, `b6808`)
- **Testing**: Use specific commit hashes for reproducibility
- **Latest**: Use `master` branch (not recommended for production)

### Version-Specific Notes

- **b6808 and older**: Includes `llama-run` binary (deprecated in later versions)
- **b6809 and newer**: `llama-run` is no longer built; use `llama-cli` instead
- **All versions**: Include `llama-gguf` tool for GGUF file inspection and debugging

### Updating to New Versions

1. Run the workflow with the new version
2. Download and test the binaries locally
3. Extract to `bin/` directory
4. Run existing workflows to verify compatibility
5. Archive old binaries for rollback if needed

## Best Practices

1. **Test before deploying**: Always test new binaries with your workflows before committing to `bin/`
2. **Archive old versions**: Keep previous binaries in `bin/archive/` for quick rollback
3. **Document versions**: Note which llama.cpp version is in use in commit messages
4. **Regular updates**: Run scheduled builds to stay current with llama.cpp improvements
5. **Release tagging**: Use release tags for important binary updates

## Example: Complete Update Process

```bash
# 1. Trigger workflow manually with version b8100
# (Use GitHub Actions UI)
# Optional: Enable openssl_static if you need fully portable binaries

# 2. Download artifact after workflow completes
cd ~/Downloads
unzip llama-cpp-b8100-darwin-arm64.zip

# 3. Navigate to repository
cd /path/to/gguf

# 4. Archive old binaries
mkdir -p bin/archive/$(date +%Y-%m-%d)
mv bin/llama-* bin/archive/$(date +%Y-%m-%d)/

# 5. Copy new binaries
cp ~/Downloads/llama-* bin/

# 6. Verify binaries
ls -lh bin/llama-*
./bin/llama-cli --version

# 7. Test with existing workflow
# (Run a quantization workflow to verify)

# 8. Test llama-gguf for debugging (optional)
./bin/llama-gguf --help

# 9. Commit changes
git add bin/
git commit -m "Update llama.cpp binaries to version b8100"
git push
```

## Support

For issues or questions:

1. Check workflow logs in the Actions tab
2. Review this documentation
3. Consult the [llama.cpp repository](https://github.com/ggerganov/llama.cpp)
4. Open an issue in this repository

## Related Documentation

- [Build Plan](./build-llamacpp-workflow-plan.md) - Detailed technical plan
- [README.md](../README.md) - Main repository documentation
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp/tree/master/docs)