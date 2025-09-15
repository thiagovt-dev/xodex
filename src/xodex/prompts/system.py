from pathlib import Path
import os


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


def get_system_prompt():
    """Get the system prompt, prioritizing custom prompt over default."""
    custom_prompt = os.getenv("XODEX_SYSTEM_PROMPT", "")
    if custom_prompt.strip():
        return custom_prompt.strip()
    return load_xodex_cli_prompt()


SYSTEM_PROMPT = get_system_prompt()
