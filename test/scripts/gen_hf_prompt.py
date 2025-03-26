import argparse
import json
from transformers import AutoTokenizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", "-m", required=True, help="The path to the model repository directory")
    parser.add_argument("--chat-template", "-t", required=True, help="The path to the jinja chat template file")
    parser.add_argument("--prompt-inputs", "-p", required=True, help="The path to the json prompt input file")
    parser.add_argument('--verbose', default=True, action='store_true', help='Enable verbose output')
    parser.add_argument('--debug', default=False, action='store_false', help='Enable debug output')
    args = parser.parse_args()


    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    tokenizer.chat_template = open(args.chat_template, "r").read()

    with open(args.prompt_inputs, 'r') as file:
        json_data = json.load(file)
        if args.debug:
            print(f"json data:\n{json.dumps(json_data, indent=4)}")

    if "messages" in json_data:
        messages = json_data['messages']
    if args.debug:
        print(f"messages: {messages}")

    guardian_config = None
    if "guardian_config" in json_data:
        guardian_config = json_data['guardian_config']
    if args.debug:
        print(f"guardian_config: {guardian_config}")

    tools = None
    if "tools" in json_data:
        tools = json_data['tools']
    if args.debug:
        print(f"tools: {tools}")

    add_gen_prompt:bool = True
    if "add_generation_prompt" in json_data:
        add_gen_prompt = json_data['add_generation_prompt']
    if args.debug:
        print(f"add_gen_prompt: {add_gen_prompt}")

    chat = tokenizer.apply_chat_template(messages, guardian_config = guardian_config, tokenize=False, add_generation_prompt=True)

    print(f"==============\n{chat}\n==============\n")
