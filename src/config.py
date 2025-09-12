import os
from dotenv import load_dotenv

load_dotenv()

cfg = {
    "provider": os.getenv("AGENT_PROVIDER", "openai"),
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    },
    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "model": os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
    },
    "grok": {
        "api_key": os.getenv("GROK_API_KEY", ""),
        "model": os.getenv("GROK_MODEL", "grok-2"),
        "base_url": os.getenv("GROK_BASE_URL", "https://api.x.ai/v1"),
    },
    "context": {
        "globs": [s.strip() for s in os.getenv("CONTEXT_GLOBS", "").split(",") if s.strip()],
        "max_chars": int(os.getenv("MAX_CONTEXT_CHARS", "20000")),
    },
}
