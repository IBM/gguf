# Quick Start: Building llama.cpp Binaries

## TL;DR

```bash
# 1. Go to GitHub Actions → Build llama.cpp Binaries → Run workflow
# 2. Enter version: b8216 (or latest)
# 3. Wait for build to complete
# 4. Download artifacts and extract:

unzip llama-cpp-macOS-b8216.zip -d bin/
# or
unzip llama-cpp-Linux-b8216.zip -d bin/
```

## What Gets Built

5 binaries optimized for GitHub Actions runners:

- `llama-cli` - Inference CLI
- `llama-quantize` - Quantization tool
- `llama-server` - HTTP server
- `llama-llava-cli` - LLaVA multimodal
- `llama-mtmd-cli` - MTMD multimodal

## Common Tasks

### Update to Latest Version

```bash
# 1. Run workflow with version "b8216" (or newer)
# 2. Download both platform zips
# 3. Archive old binaries
mkdir -p bin/archive/$(date +%Y-%m-%d)
mv bin/llama-* bin/archive/$(date +%Y-%m-%d)/

# 4. Extract new binaries
unzip llama-cpp-macOS-b8216.zip -d bin/
chmod +x bin/llama-*
```

### Build for Release

```bash
# 1. Run workflow with:
#    - version: b8216
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

**Build failed?**
- Check llama.cpp version exists
- Enable debug mode
- Review workflow logs

**Binary not working?**
- Verify file permissions: `chmod +x bin/llama-*`
- Check platform (macOS vs Linux)
- Test with `--help` flag

## More Information

- [Full Usage Guide](./build-llamacpp-workflow-usage.md)
- [Technical Plan](./build-llamacpp-workflow-plan.md)
- [Main README](../README.md)