import ollama

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GRAY = "\033[90m"
WHITE = "\033[37m"
OFF_WHITE = "\033[38;5;253m"

BACKGROUND_BLACK = "\033[40m"
BACKGROUND_RED = "\033[41m"
BACKGROUND_GREEN = "\033[42m"
BACKGROUND_YELLOW = "\033[43m"
BACKGROUND_BLUE = "\033[44m"
BACKGROUND_MAGENTA = "\033[45m"
BACKGROUND_CYAN = "\033[46m"
BACKGROUND_WHITE = "\033[47m"

messages = [
    {
        "role": "user",
        "content": "hello world",
    },
]

models = [
    # "ibm/granite3.2-guardian:3b",
    # "ibm/granite3.2-guardian:5b",
    # "ibm/granite4.0-preview:tiny-instruct-q5_K_M"
]

models = [
    "ibm/granite3.2:2b",
    "ibm/granite3.2:8b",
    "ibm/granite3.3-guardian:8b",
    "ibm/granite3.3:2b",
    "ibm/granite3.3:8b",
    "bm/granite4.0-preview:tiny"
]

try:
    for model in models:
        print(f"{BACKGROUND_CYAN}{WHITE}--[{model}]---------------\n{RESET}",)
        # Note: for Guardian models, the "temperature" parameter must be set to zero (0) to assure accurate assessment and scoring.
        response = ollama.chat(
            model=model,
            think=True,
            messages=messages,
            options={"temperature": 0}
        )
        msg_thinking = response["message"]["thinking"]
        msg_content = response["message"]["content"]
        print(f"{GRAY}Thinking...\n\t\"{msg_thinking}\"\n...done Thinking.{RESET}")
        print(f"{CYAN}Content:\n\t{msg_content}...end Content\n{RESET}")
except Exception as exc:
    print(f"exception: {exc}")
