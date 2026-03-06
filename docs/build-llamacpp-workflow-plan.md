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
  - `llama_cpp_version`: Git commit hash or tag (default: `b8216` or later)
  - `release_tag`: Optional release tag to upload binaries as release assets
  - `debug`: Boolean to enable verbose output (default: `false`)
- **On release**: Automatically build when a new release is created
- **Scheduled** (optional): Weekly builds to keep binaries up-to-date

### Build Matrix Strategy
Build on two platforms simultaneously:
- `macos-latest` runner
- `ubuntu-latest` runner

### Required Binaries
1. `llama-cli` - Command-line interface for inference
2. `llama-quantize` - Model quantization tool
3. `llama-server` - HTTP server for model serving
4. `llama-llava-cli` - LLaVA multimodal interface
5. `llama-mtmd-cli` - Multimodal (MTMD) interface

### CMake Build Configuration

#### CMake Configuration Flags (from README)
```bash
cmake -B build \
  -DBUILD_SHARED_LIBS=OFF \
  -DGGML_METAL=OFF \
  -DGGML_NATIVE_DEFAULT=OFF \
  -DCMAKE_CROSSCOMPILING=TRUE \
  -DGGML_NO_ACCELERATE=ON
```

**Flag Explanations:**
- `-DBUILD_SHARED_LIBS=OFF`: Build static libraries for portability
- `-DGGML_METAL=OFF`: Disable Metal GPU support (not available in GitHub runners)
- `-DGGML_NATIVE_DEFAULT=OFF`: Disable native CPU optimizations for broader compatibility
- `-DCMAKE_CROSSCOMPILING=TRUE`: Treat as cross-compilation for maximum compatibility
- `-DGGML_NO_ACCELERATE=ON`: Disable macOS Accelerate framework for consistency

#### Build Command
```bash
cmake --build build --config Release
```

### Workflow Steps

#### Job: build-binaries
**Matrix:** `[macos-latest, ubuntu-latest]`

1. **Checkout repository**
   - Use `actions/checkout@v4`

2. **Install dependencies**
   - macOS: Ensure CMake is available (pre-installed)
   - Ubuntu: Install build essentials and CMake
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
     -DGGML_METAL=OFF \
     -DGGML_NATIVE_DEFAULT=OFF \
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
   ./build/bin/llama-llava-cli --version
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
llama-cpp-binaries-macOS-b8216/
└── llama-cpp-macOS-b8216.zip

llama-cpp-binaries-Linux-b8216/
└── llama-cpp-Linux-b8216.zip
```

### Zip Contents
```
llama-cpp-macOS-b8216.zip:
├── llama-cli
├── llama-quantize
├── llama-server
├── llama-llava-cli
└── llama-mtmd-cli

llama-cpp-Linux-b8216.zip:
├── llama-cli
├── llama-quantize
├── llama-server
├── llama-llava-cli
└── llama-mtmd-cli
```

### Release Assets (permanent)
When triggered with a release tag or on release event:
- `llama-cpp-macos-b8216.zip`
- `llama-cpp-linux-b8216.zip`

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
2. **Download zip artifacts** from workflow run or release assets
3. **Extract binaries** to `bin/` directory manually or via script
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
5. Download zip artifacts from the workflow run or release page

The workflow builds binaries for both macOS and Ubuntu with flags optimized for GitHub Actions runners. Binaries are packaged as zip files for easy distribution.
```

## Future Enhancements
1. Add Windows support if needed
2. Implement automatic version detection from llama.cpp releases
3. Add performance benchmarks for built binaries
4. Create reusable workflow for other repositories to use
5. Add automated script to extract and update `bin/` directory

## Success Criteria
- [ ] Workflow successfully builds all required binaries on both platforms
- [ ] Binaries pass smoke tests
- [ ] Zip archives are created correctly
- [ ] Workflow artifacts are uploaded with 90-day retention
- [ ] Release assets are uploaded when release tag is provided
- [ ] Documentation is clear and complete
- [ ] Existing workflows continue to function with extracted binaries