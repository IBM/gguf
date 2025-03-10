#!/bin/bash
set -x

executable_path="./gen_context"
chat_ml_template="templates/llama.cpp/granite-guardian-chatml.test.txt"
messages_path="messages/granite/guardian/"
message_test_files=("user-harm.json"
    "user-asst-harm.json" \
    "user-asst-evasiveness.json" \
    "user-harm-social-bias.json" \
    "rag-context-relevance.json" \
    "rag-function-calling.json" \
    "config-custom-risk-name-and-defn.json" \
    "config-existing-risk-name-and-no-defn.json")

# TODO: exception tests
# config-custom-risk-no-defn.json
# config-existing-risk-name-and-new-defn.json


for test_file in "${message_test_files[@]}"; do
  echo "$test_file"
  $executable_path \
    -f  $chat_ml_template \
    -m "${messages_path}${test_file}" \
    -o "${test_file}.out.txt" \
    -d
done
