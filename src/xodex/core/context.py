from pathlib import Path
import glob
from xodex.config import cfg


def build_context() -> str:
    patterns = cfg["context"]["globs"]
    max_chars = cfg["context"]["max_chars"]
    if not patterns:
        return ""
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))
    seen = set()
    picks = []
    total = 0
    for f in files:
        if f in seen:
            continue
        seen.add(f)
        try:
            text = Path(f).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if total + len(text) > max_chars:
            break
        picks.append(f"--- FILE:{f} ---\n{text}")
        total += len(text)
    return "\n\n".join(picks)
