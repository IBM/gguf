#!/bin/bash
# set -x

executable_path="./gen_context"
chat_ml_template="templates/llama.cpp/granite-guardian-chatml.test.txt"
messages_path="messages/granite/guardian/"
output_dir=temp/

message_test_files=( \
  "1-1-user-harm.json" \
  "1-1-user-asst-harm.json" \
  "1-2-user-harm-social-bias.json" \
  "1-8-user-asst-evasiveness.json" \
  "3-1-rag-context-relevance.json" \
  "4-1-rag-function-calling.json" \
  "5-1-config-custom-risk-name-and-defn.json" \
  "5-2-config-existing-risk-name-and-no-defn.json" \
)

message_test_files_with_errors=( \
  "5-err-1-config-custom-risk-no-defn.json" \
  "5-err-2-config-existing-risk-name-and-new-defn.json" \
)

mkdir $output_dir

for test_file in "${message_test_files[@]}"; do
  echo "$test_file"
  $executable_path \
    -f  $chat_ml_template \
    -m "${messages_path}${test_file}" \
    -o "${output_dir}${test_file}.out.txt" 2>"${output_dir}${test_file}.err.txt"
  echo $?
done

for test_file in "${message_test_files_with_errors[@]}"; do
  echo "$test_file"
  $executable_path \
    -f  $chat_ml_template \
    -m "${messages_path}${test_file}" \
    -o "${output_dir}${test_file}.out.txt" 2>"${output_dir}${test_file}.err.txt"
  echo $?    
done
