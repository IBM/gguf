#!/bin/bash
set -e # stop execution on error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
# BLUE='\033[0;34m'
# MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
LIGHT_GRAY='\033[0;90m'
# BRIGHT_WHITE='\033[0;97m'
# DEFAULT='\033[0;39m'
RESET='\033[0m'

# Run matrix
RUN_G4_TESTS=1
RUN_G4_PREVIEW_TESTS=1
RUN_G3_3_TESTS=1
RUN_G3_2_TESTS=1
RUN_G3_1_TESTS=1
RUN_G3_0_TESTS=1

# Activate the desired Conda environment
readonly PARTNER="ollama"
readonly CONDA_RUN="conda run -n llama.cpp"
readonly PYTHON_SCRIPT="./scripts/get_partner_model_name.py -p ${PARTNER} -m "
readonly PYTHON_SCRIPT_DEBUG="./scripts/get_partner_model_name.py --debug -p ${PARTNER} -m "

# Function to print a success message and exit
success() {
  echo -e "${GREEN}[SUCCESS] ${LIGHT_GRAY}hf: ${WHITE}$1 ${LIGHT_GRAY}=> ${LIGHT_GRAY}${PARTNER}: ${CYAN}$2 ${RESET}"
  return 0
}

# Function to print an error message and exit with a non-zero status
error() {
  echo -e "${RED}[ERROR] ${LIGHT_GRAY}hf: ${WHITE}$1 ${LIGHT_GRAY}=> ${LIGHT_GRAY}${PARTNER}: ${CYAN}$2 ${LIGHT_GRAY}(expected:${YELLOW}$3${LIGHT_GRAY}) ${RESET}" # >&2
  return 0
}

test() {
  output=$($CONDA_RUN python $PYTHON_SCRIPT $1)
  if ! [[ $output == $2 ]]; then
    error $1 $output $2
    python $PYTHON_SCRIPT_DEBUG $1
    exit 1
  else
    success $1 $output
  fi
}

##############
# G4
##############

if [[ $RUN_G4_TESTS -eq 1 ]]; then
echo -e "${YELLOW}Running Granite 4 tests..."

# nano-300m, nano-300m-base
input="granite-4.0-nano-300m-Q4_K_M.gguf"
expected="granite4:300m-nano-q4_K_M"
test "$input" "$expected"

input="granite-4.0-nano-300m-base-Q4_K_M.gguf"
expected="granite4:300m-nano-base-q4_K_M"
test "$input" "$expected"

# h-nano-300m, h-nano-300m-base
input="granite-4.0-h-nano-300m-Q4_K_M.gguf"
expected="granite4:300m-nano-h-q4_K_M"
test "$input" "$expected"

input="granite-4.0-h-nano-300m-base-Q4_K_M.gguf"
expected="granite4:300m-nano-h-base-q4_K_M"
test "$input" "$expected"

# nano-1b, nano-1b-base
input="granite-4.0-nano-1b-Q4_K_M.gguf"
expected="granite4:1b-nano-q4_K_M"
test "$input" "$expected"

input="granite-4.0-nano-1b-base-Q4_K_M.gguf"
expected="granite4:1b-nano-base-q4_K_M"
test "$input" "$expected"

# h-nano-1b, h-nano-1b-base
input="granite-4.0-h-nano-1b-Q4_K_M.gguf"
expected="granite4:1b-nano-h-q4_K_M"
test "$input" "$expected"

input="granite-4.0-h-nano-1b-base-Q5_0.gguf"
expected="granite4:1b-nano-h-base-q5_0"
test "$input" "$expected"

# micro
input="granite-4.0-micro-Q8_0.gguf"
expected="granite4:micro-q8_0"
test "$input" "$expected"

# micro-base
input="granite-4.0-micro-base-Q4_1.gguf"
expected="granite4:micro-base-q4_1"
test "$input" "$expected"

# h-micro
input="granite-4.0-h-micro-Q2_K.gguf"
expected="granite4:micro-h-q2_K"
test "$input" "$expected"

# h-micro-base
input="granite-4.0-h-micro-base-Q5_K_S.gguf"
expected="granite4:micro-h-base-q5_K_S"
test "$input" "$expected"

# h-tiny
input="granite-4.0-h-tiny-Q5_1.gguf"
expected="granite4:tiny-h-q5_1"
test "$input" "$expected"

# h-tiny-base
input="granite-4.0-h-tiny-base-Q5_K_M.gguf"
expected="granite4:tiny-h-base-q5_K_M"
test "$input" "$expected"

# h-small
input="granite-4.0-h-small-Q4_K_M.gguf"
expected="granite4:small-h-q4_K_M"
test "$input" "$expected"

# h-small-base
input="granite-4.0-h-small-base-Q4_K_M.gguf"
expected="granite4:small-h-base-q4_K_M"
test "$input" "$expected"

fi

##############
# G4 Preview
##############

if [[ $RUN_G4_PREVIEW_TESTS -eq 1 ]]; then
echo -e "${YELLOW}Running Granite 4 Preview tests..."

input="granite-4.0-tiny-preview-Q4_K_M.gguf"
expected="granite4.0-preview:tiny-instruct-q4_K_M"
test "$input" "$expected"

input="granite-4.0-tiny-base-preview-Q5_K_S.gguf"
expected="granite4.0-preview:tiny-base-q5_K_S"
test "$input" "$expected"

fi

##############
# G3.3
##############

if [[ $RUN_G3_3_TESTS -eq 1 ]]; then
echo -e "${YELLOW}Running Granite 3.3 tests..."

# language
input="granite-3.3-2b-base-Q4_K_M.gguf"
expected="granite3.3:2b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.3-2b-instruct-Q4_K_M.gguf"
expected="granite3.3:2b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.3-8b-base-Q4_K_M.gguf"
expected="granite3.3:8b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.3-8b-instruct-Q4_K_M.gguf"
expected="granite3.3:8b-instruct-q4_K_M"
test "$input" "$expected"

# Guardian models
input="granite-guardian-3.3-8b-Q5_K_M.gguf"
expected="granite3.3-guardian:8b-q5_K_M"
test "$input" "$expected"

# Vision models
input=" granite-vision-3.3-2b-Q8_0.gguf"
expected="granite3.3-vision:2b-q8_0"
test "$input" "$expected"

# FUTURE: TODO: vision embedding (needs llama.cpp/gguf support)
# input="granite-vision-3.3-2b-embedding"

fi

##############
# G3.2
##############

if [[ $RUN_G3_2_TESTS -eq 1 ]]; then
echo -e "${YELLOW}Running Granite 3.2 tests..."

# Guardian models
input=""
expected="granite3.2-guardian:3b-q4_K_M"

input=""
expected="granite3.2-guardian:5b-q6_K"


# Embedding models
input="granite-embedding-30m-english-q8_0.gguf"
expected="granite-embedding:30m-english-q8_0"
test "$input" "$expected"

input="granite-embedding-125m-english-q8_0.gguf"
expected="granite-embedding:125m-english-q8_0"
test "$input" "$expected"

input="granite-embedding-278m-english-q8_0.gguf"
expected="granite-embedding:278m-english-q8_0"
test "$input" "$expected"

input="granite-embedding-107m-multilingual-q8_0.gguf"
expected="granite-embedding:107m-multilingual-q8_0"
test "$input" "$expected"

input="granite-embedding-278m-multilingual-q8_0.gguf"
expected="granite-embedding:278m-multilingual-q8_0"
test "$input" "$expected"

fi

##############
# G3.1
##############

if [[ $RUN_G3_1_TESTS -eq 1 ]]; then
echo -e "${YELLOW}Running Granite 3.1 tests..."

# language
input="granite-3.1-8b-instruct-Q4_K_M.gguf"
expected="granite3.1-dense:8b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.1-8b-base-Q4_K_M.gguf"
expected="granite3.1-dense:8b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.1-2b-instruct-Q4_K_M.gguf"
expected="granite3.1-dense:2b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.1-2b-base-Q4_K_M.gguf"
expected="granite3.1-dense:2b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.1-3b-a800m-instruct-Q4_K_M.gguf"
expected="granite3.1-moe:3b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.1-3b-a800m-base-Q4_K_M.gguf"
expected="granite3.1-moe:3b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.1-1b-a400m-instruct-Q4_K_M.gguf"
expected="granite3.1-moe:1b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.1-1b-a400m-base-Q4_K_M.gguf"
expected="granite3.1-moe:1b-base-q4_K_M"
test "$input" "$expected"

# Guardian
input="granite-guardian-3.1-8b-Q4_K_M.gguf"
expected="granite3.1-guardian:8b-q4_K_M"
test "$input" "$expected"

input="granite-guardian-3.1-2b-Q5_K_M.gguf"
expected="granite3.1-guardian:2b-q5_K_M"
test "$input" "$expected"

# TODO: vision
# input="granite-vision-3.1-2b-preview"

fi

##############
# G3.0
##############

if [[ $RUN_G3_0_TESTS -eq 1 ]]; then
echo -e "${YELLOW}Running Granite 3.0 tests..."

# language
input="granite-3.0-8b-instruct-Q4_K_M.gguf"
expected="granite3-dense:8b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.0-8b-base-Q4_K_M.gguf"
expected="granite3-dense:8b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.0-2b-instruct-Q4_K_M.gguf"
expected="granite3-dense:2b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.0-2b-base-Q4_K_M.gguf"
expected="granite3-dense:2b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.0-3b-a800m-instruct-Q4_K_M.gguf"
expected="granite3-moe:3b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.0-3b-a800m-base-Q4_K_M.gguf"
expected="granite3-moe:3b-base-q4_K_M"
test "$input" "$expected"

input="granite-3.0-1b-a400m-instruct-Q4_K_M.gguf"
expected="granite3-moe:1b-instruct-q4_K_M"
test "$input" "$expected"

input="granite-3.0-1b-a400m-base-Q4_K_M.gguf"
expected="granite3-moe:1b-base-q4_K_M"
test "$input" "$expected"

# Guardian
ibm-granite/granite-guardian-3.0-8b
ibm-granite/granite-guardian-3.0-2b

input="granite-guardian-3.0-8b-Q4_K_M.gguf"
expected="granite3-guardian:8b-q4_K_M"
test "$input" "$expected"

input="granite-guardian-3.0-2b-Q5_K_M.gguf"
expected="granite3-guardian:2b-q5_K_M"
test "$input" "$expected"

fi
