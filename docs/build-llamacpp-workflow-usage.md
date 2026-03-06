# Build llama.cpp Binaries Workflow - Usage Guide

## Overview

The `build-llamacpp-binaries.yml` workflow automates the building of llama.cpp binaries for use in GitHub Actions workflows. It builds statically-linked binaries optimized for GitHub Actions runners on both macOS and Ubuntu platforms.

## Built Binaries

The workflow builds the following 4 binaries:

1. **llama-cli** - Command-line interface for inference
2. **llama-quantize** - Model quantization tool
3. **llama-server** - HTTP server for model serving
4. **llama-mtmd-cli** - Multimodal (MTMD) interface

## Trigger Methods

### 1. Manual Dispatch (Recommended)

Navigate to the Actions tab and manually trigger the workflow:

1. Go to **Actions** → **Build llama.cpp Binaries**
2. Click **Run workflow**
3. Configure inputs:
   - **llama_cpp_version**: Git commit hash or tag (e.g., `b8216`, `master`)
   - **release_tag**: (Optional) Release tag to upload binaries as release assets
   - **debug**: Enable verbose debug output

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
unzip llama-cpp-b8216.zip -d bin/

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
unzip llama-cpp-macOS-b8216.zip -d bin/
```

## Build Configuration

### CMake Flags

The workflow uses the following minimal CMake flags for maximum compatibility:

```bash
cmake -B build \
  -DBUILD_SHARED_LIBS=OFF \          # Static linking for portability
  -DCMAKE_CROSSCOMPILING=TRUE \      # Maximum compatibility
  -DGGML_NO_ACCELERATE=ON \          # Consistent behavior
  -DCMAKE_BUILD_TYPE=Release         # Optimized release build
```

### Why These Flags?

- **Static linking**: Ensures binaries work without external dependencies
- **Cross-compilation mode**: Produces binaries that work across different environments
- **No Accelerate**: Ensures consistent behavior without platform-specific optimizations

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

- **Production**: Use stable release tags (e.g., `b8216`)
- **Testing**: Use specific commit hashes for reproducibility
- **Latest**: Use `master` branch (not recommended for production)

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
# 1. Trigger workflow manually with version b8216
# (Use GitHub Actions UI)

# 2. Download artifact after workflow completes
cd ~/Downloads
unzip llama-cpp-b8216.zip

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

# 8. Commit changes
git add bin/
git commit -m "Update llama.cpp binaries to version b8216"
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