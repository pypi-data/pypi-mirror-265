# Checol

This tool is designed to analyze Git repository diffs and generate related text responses using the AI model. It enables you to get detailed explanations or clarifications on Git changes from AI.

## Prerequisites

- Python 3.8 or higher
- Access to a Git local repository

## Installation

```
pip install checol
```

## Configuration

1. Set your Anthropic API key in the environment variable `ANTHROPIC_API_KEY`.

    ```
    export ANTHROPIC_API_KEY='your_api_key_here'
    ```

2. (Optional) If you want to change the default AI model, also set `ANTHROPIC_API_MODEL`.

    ```
    export ANTHROPIC_API_MODEL='claude-3-haiku-20240307'
    ```

## Usage

1. Use the `diff` command to analyze Git diffs and start interacting with Claude.

    ```
    checol diff [git diff options]
    ```

2. Follow the prompts to input your description or questions regarding the Git diffs.

3. Review the response from Claude and continue the interaction as desired.

## License

This project is released under the [MIT License](LICENSE)
