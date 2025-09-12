import subprocess
from pathlib import Path
from typing import Dict, Any

ToolResult = Dict[str, Any]


def read_file(path: str) -> ToolResult:
    try:
        return {"ok": True, "output": Path(path).read_text(encoding="utf-8")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def write_file(path: str, content: str) -> ToolResult:
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content, encoding="utf-8")
        return {"ok": True, "output": f"written:{path}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def run(cmd: str, cwd: str | None = None) -> ToolResult:
    try:
        proc = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return {
            "ok": proc.returncode == 0,
            "output": proc.stdout,
            "error": proc.stderr if proc.returncode != 0 else None,
            "code": proc.returncode,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ----------------------
# GIT UTILITIES (básico)
# ----------------------


def git_status(cwd: str | None = None) -> ToolResult:
    return run("git status --porcelain=v1 -b", cwd)


def git_checkout(branch: str, cwd: str | None = None) -> ToolResult:
    return run(f"git checkout {branch}", cwd)


def git_new_branch(name: str, cwd: str | None = None) -> ToolResult:
    return run(f"git checkout -b {name}", cwd)


def git_commit(
    message: str, add_all: bool = True, cwd: str | None = None
) -> ToolResult:
    if add_all:
        add_res = run("git add -A", cwd)
        if not add_res.get("ok"):
            return {"ok": False, "error": add_res.get("error") or "git add failed"}
    return run(f"git commit -m {shell_quote(message)}", cwd)


def git_branches(cwd: str | None = None) -> ToolResult:
    return run("git branch --list", cwd)


# Helper para quotes simples
def shell_quote(s: str) -> str:
    return "'" + s.replace("'", "'''") + "'"
