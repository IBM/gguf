# Granite Guardian Bin Tools

## gen_minja_prompt

A Jinja template processor for generating prompts for Granite Guardian models.

### Description

`gen_minja_prompt` is a Mach-O 64-bit executable (ARM64) that applies Jinja templates to message files to generate formatted prompts. This tool is useful for testing different prompt formats and chat templates with Granite Guardian models.

### Usage

```bash
gen_minja_prompt [options]
```

### Options

- `-f, --template-file <filename>` - Path to the Jinja template file
- `-m, --message-file <filename>` - Path to the message file (typically JSON format with chat messages)
- `-o, --output-file <filename>` - Path to the output file for the generated prompt
- `-h, --help` - Show help message
- `-v, --verbose` - Enable verbose output
- `-d, --debug` - Enable debug output

### Example

```bash
./gen_minja_prompt \
  --template-file ../guardian_template.jinja \
  --message-file ../../messages/granite/guardian/1-1-harm-user-harm.json \
  --output-file output_prompt.txt
```

### Platform

- **Architecture:** ARM64 (Apple Silicon)
- **Format:** Mach-O 64-bit executable
- **Platform:** macOS

### Notes

- This is a compiled binary executable, not a script
- The tool is designed for local testing and development
- Message files are typically located in `test/messages/granite/guardian/`
- Template files may use Jinja2 syntax for dynamic prompt generation