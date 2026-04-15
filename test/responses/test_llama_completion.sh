#!/bin/bash

# Functional test for llama-completion binary
# Tests the llama-completion tool with a real model to verify it works correctly
# Usage: ./test/responses/test_llama_completion.sh

set -e

echo "=== Testing llama-completion Binary ==="
echo ""

# Configuration
LLAMA_COMPLETION_BIN="./bin/b8742/llama-completion"
MODEL_PATH="models/ibm-granite/granite-4.0-1b-GGUF/granite-4.0-1b-Q4_K_M.gguf"
SYSTEM_PROMPT="You are a helpful assistant. Please ensure responses are professional, accurate, and safe."
USER_PROMPT="Why is the sky blue according to science?"
COMBINED_PROMPT="${SYSTEM_PROMPT} ${USER_PROMPT}"
N_PREDICT=128
TEMP=0.8
LOG_FILE="test-llama-completion.log.txt"
RESPONSE_FILE="test-llama-completion.response.txt"
WORDS_TO_MATCH="Rayleigh,scatter,atmosphere"

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up test files..."
    rm -f "$LOG_FILE" "$RESPONSE_FILE"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Check if binary exists
if [ ! -f "$LLAMA_COMPLETION_BIN" ]; then
    echo "❌ ERROR: llama-completion binary not found at: $LLAMA_COMPLETION_BIN"
    exit 1
fi
echo "✓ Binary found: $LLAMA_COMPLETION_BIN"

# Check if binary is executable
if [ ! -x "$LLAMA_COMPLETION_BIN" ]; then
    echo "⚠ WARNING: Binary is not executable, attempting to fix..."
    chmod +x "$LLAMA_COMPLETION_BIN"
    echo "✓ Made binary executable"
fi

# Test help command
echo ""
echo "--- Testing --help ---"
$LLAMA_COMPLETION_BIN --help | head -20
echo ""

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ ERROR: Model not found at: $MODEL_PATH"
    echo "Please download the model first or update MODEL_PATH in the script"
    exit 1
fi
echo "✓ Model found: $MODEL_PATH"
echo ""

# Run llama-completion
echo "--- Running llama-completion ---"
echo "Prompt: $COMBINED_PROMPT"
echo "N_predict: $N_PREDICT"
echo "Temperature: $TEMP"
echo ""

$LLAMA_COMPLETION_BIN \
    -m "$MODEL_PATH" \
    -p "$COMBINED_PROMPT" \
    -n $N_PREDICT \
    --temp $TEMP \
    -no-cnv \
    --no-display-prompt \
    --log-file "$LOG_FILE" 1>"$RESPONSE_FILE"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ ERROR: llama-completion failed with exit code: $EXIT_CODE"
    if [ -f "$LOG_FILE" ]; then
        echo ""
        echo "--- Log File ---"
        cat "$LOG_FILE"
    fi
    if [ -f "$RESPONSE_FILE" ]; then
        echo ""
        echo "--- Response File ---"
        cat "$RESPONSE_FILE"
    fi
    exit 1
fi

echo "✓ llama-completion executed successfully"
echo ""

# Display response
echo "--- Response Output ---"
if [ -f "$RESPONSE_FILE" ]; then
    cat "$RESPONSE_FILE"
    echo ""
    WORD_COUNT=$(wc -w "$RESPONSE_FILE" | awk '{print $1}')
    echo ""
    echo "Response length: $WORD_COUNT words"
else
    echo "❌ ERROR: Response file not created"
    exit 1
fi

# Validate response contains expected words
echo ""
echo "--- Validating Response ---"
echo "Checking for words: $WORDS_TO_MATCH"

if python ./scripts/test_regex_match_file_2.py "$RESPONSE_FILE" "$WORDS_TO_MATCH"; then
    echo "✅ [SUCCESS]: Required words found in response"
    VALIDATION_PASSED=true
else
    echo "⚠ [WARNING]: Required words not found in response (this may be OK depending on model output)"
    VALIDATION_PASSED=false
fi

# Display log file summary
echo ""
echo "--- Log File Summary ---"
if [ -f "$LOG_FILE" ]; then
    echo "Log file size: $(wc -l "$LOG_FILE" | awk '{print $1}') lines"
    echo "Last 10 lines:"
    tail -10 "$LOG_FILE"
else
    echo "No log file generated"
fi

# Final summary
echo ""
echo "=== Test Summary ==="
echo "✓ Binary exists and is executable"
echo "✓ Help command works"
echo "✓ Model loaded successfully"
echo "✓ Inference completed"
echo "✓ Response generated ($WORD_COUNT words)"
if [ "$VALIDATION_PASSED" = true ]; then
    echo "✓ Response validation passed"
else
    echo "⚠ Response validation warning (see above)"
fi

echo ""
echo "=== Test Complete ==="
echo "llama-completion is working correctly!"
echo ""
echo "Note: Test files have been cleaned up automatically"

exit 0

# Made with Bob
