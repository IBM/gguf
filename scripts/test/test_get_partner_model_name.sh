#!/bin/bash
set -e # stop execution on error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
LIGHT_GRAY='\033[0;90m'

BRIGHT_WHITE='\033[0;97m'
DEFAULT='\033[0;39m'
RESET='\033[0m'

# Run matrix
RUN_G4_TESTS=0
RUN_G3_3_TESTS=1
RUN_G3_2_TESTS=1

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
  echo -e "${RED}[ERROR] ${LIGHT_GRAY}hf: ${WHITE}$1 ${LIGHT_GRAY}=> ${LIGHT_GRAY}${PARTNER}: ${CYAN}$2 ${LIGHT_GRAY}(expected:${YELLOW}$3 ${RESET}" # >&2
  return 0
}

##############
# G4
##############

if [[ $RUN_G4_TESTS -eq 1 ]]; then

echo -e "${YELLOW}Running Granite 4 tests..."

# TODO: nano-1b, nano-1b-base

# h-nano-1b
# input="granite-4.0-h-nano-1b-Q4_K_M.gguf"
# expected="granite4:1b-nano-h-q4_K_M"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input" "$output" "$expected"
#     # Re-run script with --debug (do not need to activate conda env. again)
#     python $PYTHON_SCRIPT_DEBUG $input
# else
#     success "$input" "$output"
# fi

# h-nano-1b-base
# input="granite-4.0-h-nano-1b-base-Q4_K_M.gguf"
# expected="granite4:1b-nano-h-base-q4_K_M"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input" "$output" "$expected"
#     # Re-run script with --debug (do not need to activate conda env. again)
#     python $PYTHON_SCRIPT_DEBUG $input
# else
#     success "$input" "$output"
# fi

# TODO: nano-300m, nano-300m-base

# TODO: h-nano-300m, h-nano-300m-base

# micro
input="granite-4.0-micro-Q8_0.gguf"
expected="granite4:micro-q8_0"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# micro-base
input="granite-4.0-micro-base-Q4_1.gguf"
expected="granite4:micro-base-q4_1"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# h-micro
input="granite-4.0-h-micro-Q2_K.gguf"
expected="granite4:micro-h-q2_K"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# h-micro-base
input="granite-4.0-h-micro-base-Q5_K_S.gguf"
expected="granite4:micro-h-base-q5_K_S"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# h-tiny
input="granite-4.0-h-tiny-Q5_1.gguf"
expected="granite4:tiny-h-q5_1"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# h-tiny-base
input="granite-4.0-h-tiny-base-Q5_K_M.gguf"
expected="granite4:tiny-h-base-q5_K_M"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# h-small
input="granite-4.0-h-small-Q4_K_M.gguf"
expected="granite4:small-h-q4_K_M"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

# h-small-base
input="granite-4.0-h-small-base-Q4_K_M.gguf"
expected="granite4:small-h-base-q4_K_M"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

fi

##############
# G3.3
##############

if [[ $RUN_G3_3_TESTS -eq 1 ]]; then

echo -e "${YELLOW}Running Granite 3.3 tests..."

input="granite-vision-3.3-2b-embedding-f16.gguf"
expected="granite3.3-vision:2b-f16"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

fi

##############
# G3.2
##############

if [[ $RUN_G3_2_TESTS -eq 1 ]]; then

# Embedding models
echo -e "${YELLOW}Running Granite 3.2 tests..."

input="granite-embedding-30m-english-q8_0.gguf"
expected="granite-embedding:30m-english-q8_0"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

input="granite-embedding-278m-multilingual-q8_0.gguf"
expected="granite-embedding:278m-multilingual-q8_0"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input" "$output" "$expected"
else
    success "$input" "$output"
fi

fi

##############
# G3.0
##############

# input="granite-3.0-1b-a400m-base-Q4_1.gguf"
# expected="granite3-moe:1b-base-q4_1"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input" "$output" "$expected"
# else
#     success "$input" "$output"
# fi

# input="granite-3.0-1b-a400m-base-Q2_K.gguf"
# expected="granite3-moe:1b-base-q2_K"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input" "$output" "$expected"
# else
#     success "$input" "$output"
# fi

# input="granite-guardian-3.0-2b-Q4_K_M.gguf"
# expected="granite3-guardian:2b-q4_K_M"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input" "$output" "$expected"
# else
#     success "$input" "$output"
# fi
