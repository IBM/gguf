# Quick Start: Building llama.cpp Binaries

## TL;DR

```bash
# 1. Go to GitHub Actions → Build llama.cpp Binaries → Run workflow
# 2. Enter version: b6808 (or latest)
# 3. Wait for build to complete
# 4. Download artifact and extract:

unzip llama-cpp-b6808.zip -d bin/
```

## What Gets Built

5 binaries optimized for GitHub Actions runners:

- `llama-cli` - Inference CLI
- `llama-quantize` - Quantization tool
- `llama-server` - HTTP server
- `llama-mtmd-cli` - MTMD multimodal
- `llama-gguf` - GGUF file inspection and manipulation tool

**Note:** `llama-run` was deprecated after llama.cpp release b6808 and is only built for b6808 and older versions.

## Common Tasks

### Update to Latest Version

```bash
# 1. Run workflow with version "b6808" (or newer)
# 2. Download zip file
# 3. Archive old binaries
mkdir -p bin/archive/$(date +%Y-%m-%d)
mv bin/llama-* bin/archive/$(date +%Y-%m-%d)/

# 4. Extract new binaries
unzip llama-cpp-b6808.zip -d bin/
chmod +x bin/llama-*
```

### Build for Release

```bash
# 1. Run workflow with:
#    - version: b6808
#    - release_tag: v1.0.0
# 2. Binaries automatically attached to release
# 3. Download from Releases page
```

### Test New Binaries

```bash
# Quick test
./bin/llama-cli --version
./bin/llama-quantize --help
./bin/llama-server --version

# Full test: Run a quantization workflow
```

## Troubleshooting

### Build Failed?
- Check llama.cpp version exists
- Enable debug mode
- Review workflow logs

### Binary Not Working?
- Verify file permissions: `chmod +x bin/llama-*`
- Test with `--help` flag
- Check if binary is compatible with your system

### OpenSSL Dynamic Library Error

**Problem**: You get an error when running binaries that says it cannot dynamically load the OpenSSL library:

```
dyld[12345]: Library not loaded: '@rpath/libssl.3.dylib'
  Referenced from: '/path/to/llama-cli'
  Reason: tried: '/usr/local/lib/libssl.3.dylib' (no such file),
  '/System/Volumes/Preboot/Cryptexes/OS/usr/local/lib/libssl.3.dylib' (no such file),
  '/usr/local/lib/libssl.3.dylib' (no such file)
```

or

```
dyld[12345]: Library not loaded: '@rpath/libcrypto.3.dylib'
  Referenced from: '/path/to/llama-server'
  Reason: tried: '/usr/local/lib/libcrypto.3.dylib' (no such file),
  '/System/Volumes/Preboot/Cryptexes/OS/usr/local/lib/libcrypto.3.dylib' (no such file),
  '/usr/local/lib/libcrypto.3.dylib' (no such file)
```

**Solution**: Rebuild the binaries with static OpenSSL linking enabled:

1. Go to **Actions** → **Build llama.cpp Binaries** → **Run workflow**
2. Enter your desired version (e.g., `b8100`)
3. **Enable the `openssl_static` parameter** (set to `true`)
4. Wait for build to complete
5. Download and extract the new binaries

**What this does**: The `openssl_static` parameter adds the `-DOPENSSL_USE_STATIC_LIBS=ON` CMake flag, which forces static linking of OpenSSL libraries. This embeds the OpenSSL code directly into the binary, eliminating the need for system-installed OpenSSL libraries.

**Why this happens**: By default, binaries are dynamically linked to OpenSSL, which means they depend on OpenSSL being installed on your system at the expected location. If OpenSSL is missing, in a different location, or a different version, the binary won't run.

**Trade-offs**:
- ✅ **Pro**: Binaries work on any system without requiring OpenSSL installation
- ✅ **Pro**: No version compatibility issues
- ❌ **Con**: Slightly larger binary size
- ❌ **Con**: Security updates require rebuilding binaries

### Understanding Build Configuration

The workflow supports several configuration options that affect how binaries are built:

- **`openssl_static`**: Force static linking of OpenSSL (solves dynamic library errors)
- **`minimize_acceleration`**: Disable all hardware acceleration for maximum compatibility
- **`debug`**: Enable verbose debug output in workflow logs

For a complete reference of all CMake configuration flags and their effects, see the [CMake Configuration Flags section](./build-llamacpp-workflow-usage.md#cmake-configuration-flags) in the Full Usage Guide.

## More Information

- [Full Usage Guide](./build-llamacpp-workflow-usage.md) - Complete documentation including all CMake flags
- [Technical Plan](./build-llamacpp-workflow-plan.md) - Detailed technical implementation
- [Main README](../README.md) - Repository overview