#!/usr/bin/env bash -x

model=""
name=""
tag="local"
license_file=""
quantization="Q4_K_M"
workdir=""
docker="0"
_inside_docker="0"

# Detail env override to allow for podman
# DOCKER_CMD=podman DOCKER_RUN_ARGS="--security-opt label=disable"
docker_cmd="${DOCKER_CMD:-"docker"}"
docker_run_args="${DOCKER_RUN_ARGS:-""}"
docker_image="${DOCKER_IMAGE:-"ghcr.io/ggerganov/llama.cpp:full"}"

help_str="Usage: $0 <options>

Options:
    -h, --help                Show this help message.
    -m, --model <path, hf>    File path (gguf), directory path (HF download), HF name to import.
    -n, --name <name>         Name of the model to use in ollama.
    -t, --tag <tag>           Tag of the model to use in ollama.
    -l, --license-file <path> Path to the license file (optional).
    -q, --quantization <mode> Quantization mode (Q4_K_M).
    -w, --working-dir <path>  Working directory path.
    -d, --docker              Use the dockerized version of llama.cpp
"
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -h|--help)
            echo "$help_str"
            exit 0
            ;;
        -m|--model)
            model="$2"
            shift
            ;;
        -n|--name)
            name="$2"
            shift
            ;;
        -t|--model-tag)
            tag="$2"
            shift
            ;;
        -l|--license-file)
            license_file="$2"
            shift
            ;;
        -q|--quantization)
            quantization="$2"
            shift
            ;;
        -w|--workdir)
            workdir="$2"
            shift
            ;;
        -d|--docker)
            docker="1"
            ;;
        # Hidden arg for running inside docker
        --_inside_docker)
            _inside_docker="1"
            ;;
        *)
            if [ "$model" != "" ]
            then
                echo "Unknown argument $1"
                exit 1
            fi
            model="$1"
            ;;
    esac
    shift
done

if [ "$model" == "" ]
then
    echo "Missing required argument -m|--model"
    exit 1
fi

# If the file is not already pre-downloaded and quantized, and the user has
# requested running dockerized, run all of the pre-import steps in docker
if ! [ -f $model ] && [ "$docker" == "1" ]
then
    $docker_cmd inspect $docker_image &>/dev/null ||  $docker_cmd pull $docker_image
    script_path=${BASH_SOURCE[0]}
    if readlink $script_path
    then
        script_path="$(readlink $script_path)"
    fi
    script_name=$(basename $script_path)

    # Convert the file path to the container's filesystem
    if [ -e $model ]
    then
        mount_base="$(dirname $model)"
        model="/working/$(basename $model)"
    else
        mount_base="$PWD"
    fi

    # Set up the args to run internally
    docker_args="--model $model --tag $tag --quantization $quantization"
    if [ "$name" != "" ]
    then
        docker_args="$docker_args --name $name"
    fi

    # Run pre-import steps wrapped in docker
    $docker_cmd run --rm -it $docker_run_args \
        -v "$script_path:/app/$script_name" \
        -v $mount_base:/working \
        -w /working \
        --entrypoint $script_name \
        -e "PATH=/app/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
        $docker_image --_inside_docker $docker_args

    # Update the model to point to the gguf file created in docker
    model="$(cat $mount_base/.model)"
    rm $mount_base/.model
fi

# If the model doesn't exist at all, try to download it from huggingface
if ! [ -e "$model" ]
then
    echo "Downloading model from huggingface..."
    if [ "$save_path" == "" ]
    then
        save_path=$(basename $model)
    fi
    huggingface-cli download $model --local-dir $save_path
    model=$save_path
fi

# If the model is a directory, it's a raw transformers model and needs to be
# converted and quantized
if [ -d "$model" ]
then
    echo "Converting raw transformers model to GGUF format..."
    convert_script="llama-convert-hf-to-gguf.py"
    if [ "$_inside_docker" == "1" ] || ! which $convert_script 2>/dev/null
    then
        convert_script="convert_hf_to_gguf.py"
    fi
    $convert_script "$model"
    echo "Quantizing GGUF Model [$quantization]"
    f16_fname=$(ls $model | grep -i "f16.gguf")
    llama-quantize $model/$f16_fname $quantization
    quant_gguf_target="$model/$(basename $model).$quantization.gguf"
    quant_fname=$(ls $model | grep -i "$quantization.gguf")
    mv "$model/$quant_fname" "$quant_gguf_target"
    model="$quant_gguf_target"
fi

# Short-circuit if running inside docker so the ollama import can happen outside
if [ "$_inside_docker" == "1" ]
then
    echo $model > .model
    exit 0
fi

# Use an absolute path
model="$(realpath $model)"


# Check if name is empty and assign file name as name if true
if [ "$name" == "" ]
then
    name=$(basename $model)
    name="${name%.*}"
fi

# Append the model label to the model name
name="$name:$tag"
echo "name: $name"

# Create a temporary directory for working
if [ "$workdir" == "" ]
then
    workdir=$(mktemp -d)
fi
mkdir -p $workdir 2>/dev/null
echo "Working Dir: $workdir"

# Write the file path to Modelfile in the temporary directory
echo "FROM $model" > $workdir/Modelfile

# If a license file is given, add it to the modelfile
if [ "$license_file" != "" ]
then
    license_text="$(cat $license_file)"
    echo "Adding LICENSE"
    echo -e "$license_text" | head -n3
    echo "..."
    echo "LICENSE \"\"\"${license_text}\"\"\"" >> $workdir/Modelfile
fi

# Import the model using ollama create command
echo "importing model $name"
ollama create $name -f $workdir/Modelfile
