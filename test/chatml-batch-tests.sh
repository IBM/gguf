#!/bin/bash
# set -x

executable_path="./bin/gen_minja_prompt"
chat_ml_template="templates/llama.cpp/granite-guardian-chatml.j2"
messages_path="messages/granite/guardian/"
output_dir=temp/

# Note: there must be no trailing whitespace after each line continuation char('\')
# AND only 1 space char. before.
message_test_files=( \
  "1-1-harm-user-asst-harm-no-system.json" \
  "1-1-harm-user-asst-harm.json" \
  "1-1-harm-user-harm.json" \
  "1-2-harm-user-social-bias.json" \
  "1-3-harm-user-jailbreak.json" \
  "1-4-harm-user-profanity.json" \
  "1-5-harm-user-unethical-behavior.json" \
  "1-6-harm-user-violence.json" \
  "1-7-harm-user-engagement.json" \
  "1-8-harm-user-asst-evasiveness.json" \
  "2-1-harm-user-asst-harm.json" \
  "2-2-harm-user-social-bias.json" \
  "2-3-harm-user-profanity.json" \
  "2-4-harm-user-unethical-behavior.json" \
  "2-5-harm-user-violence.json" \
  "2-6-harm-user-engagement.json" \
  "2-7-harm-user-asst-evasiveness.json" \
  "3-1-rag-context-relevance.json" \
  "3-2-rag-groundedness.json" \
  "3-3-rag-answer-relevance.json" \
  "3-1-rag-context-relevance.json" \
  "4-1-rag-function-calling.json" \
  "5-1-config-custom-risk-name-and-defn.json" \
  "5-2-config-existing-risk-name-and-no-defn.json" \
)

message_test_files_with_errors=( \
  "1-err-2-harm-invalid-primary.json" \
  "1-err-4-harm-invalid-system-risk-name.json" \
  "1-err-1-harm-no-primary-role.json" \
  "1-err-3-harm-invalid-secondary-role.json" \
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
