#!/bin/bash

# Test script to simulate the workflow validation step locally
# This tests the bash compatibility fix for the regex validation
# Usage: ./test/responses/test_workflow_validation.sh

echo "=== Testing Workflow Regex Validation Step ==="
echo ""

# Use the existing test file
TEST_FILE="test/responses/sky_blue_1.txt"
WORDS_TO_MATCH="Rayleigh,scatter,atmosphere"

if [ ! -f "$TEST_FILE" ]; then
    echo "❌ ERROR: Test file not found: $TEST_FILE"
    exit 1
fi

echo "Test file: $TEST_FILE"
echo "Words to match: $WORDS_TO_MATCH"
echo ""
echo "--- File Content ---"
cat "$TEST_FILE"
echo ""
echo "--- Running Validation ---"
echo ""

# Test the Python script (same as workflow)
python_output=$(python ./scripts/test_regex_match_file_2.py "$TEST_FILE" "$WORDS_TO_MATCH")
echo "Full Python Output: $python_output"
echo ""

# Extract the last line of the output, which contains "True" or "False"
return_value=$(echo "$python_output" | tail -n 1)
echo "Return value: '$return_value'"
echo ""

# Use the extracted "boolean" string in a conditional
# Check for both "True" and "true" for compatibility (same as workflow)
if [[ "$return_value" == "True" ]] || [[ "$return_value" == "true" ]]; then
  echo "✅ [SUCCESS]: Validation passed - required words found in response"
  exit_code=0
else
  echo "❌ [FAILURE]: Validation failed - required words not found in response"
  exit_code=1
fi

echo ""
echo "=== Test Complete (exit code: $exit_code) ==="
exit $exit_code

# Made with Bob
