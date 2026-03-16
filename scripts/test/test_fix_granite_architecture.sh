#!/bin/bash

# Test script for fix-granite-architecture-in-config logic
# Usage: ./scripts/test_fix_granite_architecture.sh <path_to_config.json>

if [ $# -eq 0 ]; then
  echo "Usage: $0 <path_to_config.json>"
  echo "Example: $0 /tmp/llm_export/config.json"
  exit 1
fi

CONFIG_FILE="$1"

# Check if config.json exists
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Config file not found: $CONFIG_FILE"
  exit 1
fi

echo "Testing architecture fix logic on: $CONFIG_FILE"
echo ""

# Print config.json contents before any logic
echo "=== Contents of config.json before fix ==="
cat "$CONFIG_FILE"
echo "=========================================="
echo ""

# Extract architecture from config.json
# Force no color and strip any ANSI codes that slip through
ARCHITECTURE=$(GREP_COLORS='' grep --color=never -A 1 '"architectures"' "$CONFIG_FILE" | grep --color=never -o '"[^"]*"' | tail -1 | tr -d '"' | sed $'s/\x1b\\[[0-9;]*m//g' | sed $'s/\x1b\\[K//g')

echo "Extracted architecture: '$ARCHITECTURE'"
echo "Architecture length: ${#ARCHITECTURE}"

# Show hex dump to detect any hidden characters
echo "Architecture (hex dump):"
printf '%s' "$ARCHITECTURE" | hexdump -C | head -3
echo ""

# Debug: show the raw grep output
echo "Debug - raw architectures section:"
grep -A 2 '"architectures"' "$CONFIG_FILE"
echo ""

# Determine output file path
CONFIG_DIR=$(dirname "$CONFIG_FILE")
NEW_CONFIG_FILE="${CONFIG_DIR}/config.new.json"

# Check if architecture needs fixing
if [ "$ARCHITECTURE" = "GraniteModel" ]; then
  echo "✓ Found incorrect architecture 'GraniteModel', fixing to 'GraniteForCausalLM'..."

  # Debug: Check if the pattern exists in the source file
  echo "Debug: Checking if pattern exists in source file..."
  if grep -q '"GraniteModel"' "$CONFIG_FILE"; then
    echo "✓ Pattern \"GraniteModel\" found in source file"
  else
    echo "✗ WARNING: Pattern \"GraniteModel\" NOT found in source file!"
  fi

  # Run sed and capture output
  echo "Running sed command..."
  sed 's/"GraniteModel"/"GraniteForCausalLM"/g' "$CONFIG_FILE" > "$NEW_CONFIG_FILE"
  SED_EXIT=$?

  echo "Sed exit code: $SED_EXIT"
  echo "New file size: $(wc -c < "$NEW_CONFIG_FILE") bytes"

  # Show what sed actually produced
  echo "Debug: First 5 lines of new file:"
  head -5 "$NEW_CONFIG_FILE"
  echo "..."

  echo "Architecture section in new file:"
  grep --color=never -A 2 '"architectures"' "$NEW_CONFIG_FILE" || echo "No architectures section found!"
  echo ""
  echo "Original preserved: $CONFIG_FILE"
  echo "Updated file created: $NEW_CONFIG_FILE"

  # Verify the change was made
  if grep -q '"GraniteForCausalLM"' "$NEW_CONFIG_FILE"; then
    echo "✓ SUCCESS: Architecture successfully changed to GraniteForCausalLM"
  else
    echo "✗ ERROR: Architecture was NOT changed. Still shows GraniteModel"
    echo "Debug: Checking what's actually in the new file..."
    if grep -q '"GraniteModel"' "$NEW_CONFIG_FILE"; then
      echo "  - GraniteModel is still present (sed didn't replace it)"
    fi
    if [ ! -s "$NEW_CONFIG_FILE" ]; then
      echo "  - New file is empty or zero-length!"
    fi
  fi
elif [ "$ARCHITECTURE" != "GraniteForCausalLM" ] && [ -n "$ARCHITECTURE" ]; then
  echo "✓ Found architecture '$ARCHITECTURE', replacing with 'GraniteForCausalLM'..."

  # First, copy the file
  cp "$CONFIG_FILE" "$NEW_CONFIG_FILE"
  echo "File copied. Size: $(wc -c < "$NEW_CONFIG_FILE") bytes"

  # Escape special characters in architecture name for sed
  ESCAPED_ARCH=$(echo "$ARCHITECTURE" | sed 's/[]\/$*.^[]/\\&/g')
  echo "Escaped architecture for sed: '$ESCAPED_ARCH'"

  # Try sed replacement with error checking
  if sed "s/\"${ESCAPED_ARCH}\"/\"GraniteForCausalLM\"/g" "$CONFIG_FILE" > "${NEW_CONFIG_FILE}.tmp"; then
    mv "${NEW_CONFIG_FILE}.tmp" "$NEW_CONFIG_FILE"
    echo "Sed replacement completed successfully"
  else
    echo "ERROR: sed command failed with exit code $?"
    rm -f "${NEW_CONFIG_FILE}.tmp"
  fi

  echo "New file size: $(wc -c < "$NEW_CONFIG_FILE") bytes"
  echo "Architecture in new file:"
  grep -A 2 '"architectures"' "$NEW_CONFIG_FILE"
  echo ""
  echo "Original preserved: $CONFIG_FILE"
  echo "Updated file created: $NEW_CONFIG_FILE"

  # Verify the change was made
  if grep -q '"GraniteForCausalLM"' "$NEW_CONFIG_FILE"; then
    echo "✓ SUCCESS: Architecture successfully changed to GraniteForCausalLM"
  else
    echo "✗ ERROR: Architecture was NOT changed. Still shows $ARCHITECTURE"
  fi
else
  echo "✓ Architecture is already 'GraniteForCausalLM', no fix needed"
  echo "No new file created."
fi

echo ""
echo "=== Test complete ==="

# Made with Bob
