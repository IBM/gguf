from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import argparse
import sys

# Specify the model name
model_name = "ibm-granite/granite-4.0-1b"
model_path = "~/models/ibm-granite/granite-4.0-1b"

# Define the input prompt
prompt = "Why is the sky blue according to science?"

def model_generate(model_path, prompt):
    # Load tokenizer and model
    # Set device_map="cpu" to ensure it runs on CPU, not GPU
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cpu")

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to("cpu")

    # Set up the GenerationConfig with the required parameters
    # min_new_tokens: The minimum number of tokens to generate
    # no_repeat_ngram_size: Avoids repeating n-grams of a certain size
    # do_sample: Set to False for greedy decoding (equivalent to temp=0)
    # num_beams=1: Standard greedy decoding
    # generation_config = GenerationConfig(
    #     min_new_tokens=99,
    #     max_length=512,
    #     no_repeat_ngram_size=3,
    #     do_sample=False,
    #     num_beams=1,
    # )
    # generation_config=generation_config

    # Generate text (using default generation parameters)
    output = model.generate(input_ids,
        # min_new_tokens=99,
        # max_length=128,
        no_repeat_ngram_size=3,
        do_sample=False,
        num_beams=1,
    )

    # Decode the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # TODO if needed, prevent prompt from appearing in the response
    if generated_text.startswith(prompt):
        response = generated_text[len(prompt):].strip()
    else:
        response = generated_text.strip()

    return response

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__, exit_on_error=False)
        parser.add_argument("--model-path", "-m", type=str, required=True, help="path to local HF model repo.')")
        parser.add_argument("--repo-id", "-r", type=str, required=False, help="HF model repo. ID.')")
        parser.add_argument("--prompt", "-p", type=str, required=True, help="prompt to tokenize and input to model")
        parser.add_argument("--output-file", "-o", type=str, required=False, help="The name of the output file to save the generated response text.")
        parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
        parser.add_argument('--debug', default=False, action='store_true', help='Enable debug output')
        args = parser.parse_args()

        print(f"--model-path: '{args.model_path}'")
        print(f"--repo-id: '{args.repo_id}'")
        print(f"--prompt: '{args.prompt}'")

        generated_text = model_generate(args.model_path, args.prompt)

        print(f"Inference complete:\n{generated_text}")

        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(generated_text)
        else:
            print(generated_text)

    except IOError as e:
        print(f"Error: Unable to write to file '{args.output_file}': {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(2)
