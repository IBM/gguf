#!/bin/bash
set -e # stop execution on error

GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

# Activate the desired Conda environment
readonly CONDA_RUN="conda run -n llama.cpp"
readonly PYTHON_SCRIPT="./scripts/get_partner_model_name.py -p ollama -m "
readonly PYTHON_SCRIPT_DEBUG="./scripts/get_partner_model_name.py --debug -p ollama -m "

# Function to print a success message and exit
success() {
  echo -e "${GREEN}[SUCCESS] $1${RESET}"
  return 0
}

# Function to print an error message and exit with a non-zero status
error() {
  echo -e "${RED}[ERROR] $1${RESET}" # >&2
  return 0
}

##############
# G4
##############

# TODO: nano-1b, nano-1b-base

# h-nano-1b
# input="granite-4.0-h-nano-1b-Q4_K_M.gguf"
# expected="granite4:1b-nano-h-q4_K_M"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input => $output, expected $expected"
#     # Re-run script with --debug (do not need to activate conda env. again)
#     python $PYTHON_SCRIPT_DEBUG $input
# else
#     success "$input => $output"
# fi

# h-nano-1b-base
# input="granite-4.0-h-nano-1b-base-Q4_K_M.gguf"
# expected="granite4:1b-nano-h-base-q4_K_M"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input => $output, expected $expected"
#     # Re-run script with --debug (do not need to activate conda env. again)
#     python $PYTHON_SCRIPT_DEBUG $input
# else
#     success "$input => $output"
# fi

# TODO: nano-300m, nano-300m-base

# TODO: h-nano-300m, h-nano-300m-base

# micro
input="granite-4.0-micro-Q8_0.gguf"
expected="granite4:micro-q8_0"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# micro-base
input="granite-4.0-micro-base-Q4_1.gguf"
expected="granite4:micro-base-q4_1"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# h-micro
input="granite-4.0-h-micro-Q2_K.gguf"
expected="granite4:micro-h-q2_K"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# h-micro-base
input="granite-4.0-h-micro-base-Q5_K_S.gguf"
expected="granite4:micro-h-base-q5_K_S"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# h-tiny
input="granite-4.0-h-tiny-Q5_1.gguf"
expected="granite4:tiny-h-q5_1"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# h-tiny-base
input="granite-4.0-h-tiny-base-Q5_K_M.gguf"
expected="granite4:tiny-h-base-q5_K_M"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# h-small
input="granite-4.0-h-small-Q4_K_M.gguf"
expected="granite4:small-h-q4_K_M"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

# h-small-base
input="granite-4.0-h-small-base-Q4_K_M.gguf"
expected="granite4:small-h-base-q4_K_M"
output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
if ! [[ "$output" == "$expected" ]]; then
    error "$input => $output, expected $expected"
else
    success "$input => $output"
fi

##############
# G3.0
##############

# input="granite-3.0-1b-a400m-base-Q4_1.gguf"
# expected="granite3-moe:1b-base-q4_1"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input => $output, expected $expected"
# else
#     success "$input => $output"
# fi

# input="granite-3.0-1b-a400m-base-Q2_K.gguf"
# expected="granite3-moe:1b-base-q2_K"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input => $output, expected $expected"
# else
#     success "$input => $output"
# fi

# input="granite-guardian-3.0-2b-Q4_K_M.gguf"
# expected="granite3-guardian:2b-q4_K_M"
# output=$($CONDA_RUN python $PYTHON_SCRIPT $input)
# if ! [[ "$output" == $expected ]]; then
#     error "$input => $output, expected $expected"
# else
#     success "$input => $output"
# fi
