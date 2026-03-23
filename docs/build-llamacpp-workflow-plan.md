# Build llama.cpp Workflow Plan

## Overview
This document outlines the plan for creating a GitHub Actions workflow to build llama.cpp binaries that are compatible with GitHub Actions runners (macOS and Ubuntu).

## Objectives
1. Build llama.cpp binaries for both macOS and Ubuntu platforms
2. Ensure binaries work reliably in GitHub Actions workflows
3. Use CMake flags that prevent GPU dependencies (since GitHub runners don't have GPU access)
4. Provide artifacts for download and optional PR creation to update `bin/` directory

## Workflow Design

### Workflow Name
`build-llamacpp-binaries.yml`

### Trigger Options
- **Manual dispatch** (`workflow_dispatch`) with inputs:
  - `llama_cpp_version`: Git commit hash or tag (default: `b8100` or later)
  - `release_tag`: Optional release tag to upload binaries as release assets
  - `debug`: Boolean to enable verbose output (default: `false`)
  - `minimize_acceleration`: Disable all hardware acceleration for maximum compatibility (default: `false`)
  - `openssl_static`: Force static linking of OpenSSL to avoid runtime dependencies (default: `false`)
- **On release**: Automatically build when a new release is created
- **Scheduled** (optional): Weekly builds to keep binaries up-to-date

### Build Strategy
Build on a single platform:
- `ubuntu-latest` runner

### Required Binaries
1. `llama-cli` - Command-line interface for inference
2. `llama-quantize` - Model quantization tool
3. `llama-server` - HTTP server for model serving
4. `llama-mtmd-cli` - Multimodal (MTMD) interface
5. `llama-gguf` - GGUF file inspection and manipulation tool (useful for debugging)

**Note:** `llama-run` was deprecated after llama.cpp release b6808 and is only built for versions b6808 and older.

### CMake Build Configuration

#### CMake Configuration Flags
```bash
cmake -B build \
  -DBUILD_SHARED_LIBS=OFF \
  -DOPENSSL_USE_STATIC_LIBS=ON \  # Optional, controlled by openssl_static input
  -DCMAKE_CROSSCOMPILING=TRUE \
  -DGGML_NO_ACCELERATE=ON
```

**Flag Explanations:**
- `-DBUILD_SHARED_LIBS=OFF`: Build static libraries for portability
- `-DOPENSSL_USE_STATIC_LIBS=ON`: Force static linking of OpenSSL (optional, avoids runtime dependencies on libssl/libcrypto)
- `-DCMAKE_CROSSCOMPILING=TRUE`: Treat as cross-compilation for maximum compatibility
- `-DGGML_NO_ACCELERATE=ON`: Disable platform-specific accelerations for consistency

#### Build Command
```bash
cmake --build build --config Release
```

### Workflow Steps

#### Job: build-binaries
**Runner:** `ubuntu-latest`

1. **Checkout repository**
   - Use `actions/checkout@v4`

2. **Install dependencies**
   - Install build essentials and CMake
   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential cmake
   ```

3. **Clone llama.cpp**
   ```bash
   git clone --depth 1 --branch ${{ inputs.llama_cpp_version }} https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   ```

4. **Configure CMake**
   ```bash
   cmake -B build \
     -DBUILD_SHARED_LIBS=OFF \
     -DCMAKE_CROSSCOMPILING=TRUE \
     -DGGML_NO_ACCELERATE=ON
   ```

5. **Build binaries**
   ```bash
   cmake --build build --config Release
   ```

6. **Verify binaries exist**
   ```bash
   ls -lh build/bin/
   ```

7. **Run smoke tests**
   - Test each binary with `--version` or `--help` flag
   ```bash
   ./build/bin/llama-cli --version
   ./build/bin/llama-quantize --help
   ./build/bin/llama-server --version
   ./build/bin/llama-mtmd-cli --version
   ```

8. **Create zip archive**
   - Zip binaries for distribution
   ```bash
   cd build/bin
   zip -r llama-cpp-${{ runner.os }}-${{ inputs.llama_cpp_version }}.zip llama-*
   ```

9. **Upload workflow artifacts**
   - Use `actions/upload-artifact@v4`
   - Artifact name: `llama-cpp-binaries-${{ runner.os }}-${{ inputs.llama_cpp_version }}`
   - Path: `build/bin/llama-cpp-${{ runner.os }}-${{ inputs.llama_cpp_version }}.zip`
   - Retention: 90 days

#### Job: upload-release-assets (conditional)
**Depends on:** `build-binaries`
**Condition:** `if: inputs.release_tag != '' || github.event_name == 'release'`

1. **Download all artifacts**
   - Use `actions/download-artifact@v4`
   - Download both macOS and Linux zip files

2. **Upload to release**
   - Use `softprops/action-gh-release@v1`
   - Upload both zip files as release assets
   - Asset names:
     - `llama-cpp-macos-${{ inputs.llama_cpp_version }}.zip`
     - `llama-cpp-linux-${{ inputs.llama_cpp_version }}.zip`

## Artifact Structure

### Workflow Artifacts (90-day retention)
```
llama-cpp-binaries-b8216/
└── llama-cpp-b8216.zip
```

### Zip Contents
```
llama-cpp-b8216.zip:
├── llama-cli
├── llama-quantize
├── llama-server
└── llama-mtmd-cli
```

### Release Assets (permanent)
When triggered with a release tag or on release event:
- `llama-cpp-b8216.zip`

## Integration with Existing Workflows

### Current Usage Pattern
Existing workflows use pre-built binaries from `bin/` directory:
```yaml
- name: quantize-gguf
  run: |
    sudo ./bin/llama-quantize ${{ env.LOCAL_FNAME_CONVERTED_GGUF }} ...
```

### After Implementation
1. **Manual workflow run** to build new binaries
2. **Download zip artifact** from workflow run or release assets
3. **Extract binaries** to `bin/` directory
4. **Existing workflows** continue to use binaries from `bin/` directory

## Testing Strategy

### Smoke Tests (in workflow)
- Verify each binary executes without error
- Check version output matches expected llama.cpp version

### Integration Tests (manual)
- Run quantization workflow with new binaries
- Verify model conversion works correctly
- Test on both macOS and Ubuntu runners

## Documentation Updates

### README.md Updates
Add new section under "Updating Tools > llama.cpp":

```markdown
#### Automated Build Workflow

A GitHub Actions workflow is available to build llama.cpp binaries:

1. Navigate to Actions > Build llama.cpp Binaries
2. Click "Run workflow"
3. Enter the llama.cpp version (commit hash or tag)
4. Optionally provide a release tag to upload as release assets
5. Download zip artifact from the workflow run or release page

The workflow builds binaries on Ubuntu with minimal CMake flags for maximum compatibility. Binaries are packaged as a zip file for easy distribution.
```

## Future Enhancements
1. Add macOS or Windows builds if platform-specific binaries are needed
2. Implement automatic version detection from llama.cpp releases
3. Add performance benchmarks for built binaries
4. Create reusable workflow for other repositories to use
5. Add automated script to extract and update `bin/` directory

## Success Criteria
- [ ] Workflow successfully builds all required binaries
- [ ] Binaries pass smoke tests
- [ ] Zip archive is created correctly
- [ ] Workflow artifact is uploaded with 90-day retention
- [ ] Release asset is uploaded when release tag is provided
- [ ] Documentation is clear and complete
- [ ] Existing workflows continue to function with extracted binaries