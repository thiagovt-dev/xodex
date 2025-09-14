from pathlib import Path


def load_xodex_cli_prompt():
    """Load the Xodex CLI prompt from the xodex-cli.txt file."""
    current_dir = Path(__file__).parent
    prompt_file = current_dir / "xodex-cli.txt"

    if prompt_file.exists():
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # Fallback prompt if file is not found
        return "You are Xodex, a coding agent. Please help with the task."


SYSTEM_PROMPT = load_xodex_cli_prompt()
