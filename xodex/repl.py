import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
from typing import List, Dict
from xodex.core.agent import respond
from xodex.core import tools as Tools

Message = Dict[str, str]

HELP = (
    "Comandos:\n"
    ":q                      sair\n"
    ":clear                  limpar histórico\n"
    ":help                   ajuda\n"
    ":tool read <path>       lê arquivo\n"
    ":tool write <path>      escreve arquivo (terminar com uma linha contendo apenas EOF)\n"
    ":tool run <cmd>         executa comando (pede confirmação)\n"
    ":git status             status do repositório\n"
    ":git branches           lista branches\n"
    ":git checkout <name>    troca para branch\n"
    ":git new-branch <name>  cria e muda para nova branch\n"
    ":git commit \"msg\"       commit com -A\n"
)

async def _confirm(prompt: str) -> bool:
    session = PromptSession()
    try:
        with patch_stdout():
            ans = (await session.prompt_async(prompt)).strip().lower()
        return ans in ("y", "yes", "s", "sim")
    except Exception:
        return False

async def _handle_tool(cmd: str):
    parts = cmd.split(maxsplit=2)
    if len(parts) < 2:
        print("uso: :tool <read|write|run> ..."); return
    sub = parts[1]
    if sub == "read":
        if len(parts) < 3:
            print("uso: :tool read <path>"); return
        res = Tools.read_file(parts[2])
        if res.get("ok"): print(res.get("output", ""))
        else: print("[erro]", res.get("error"))
    elif sub == "write":
        if len(parts) < 3:
            print("uso: :tool write <path>"); return
        path = parts[2]
        print("Digite o conteúdo. Finalize com uma linha contendo apenas 'EOF'.")
        lines: List[str] = []
        while True:
            line = input()
            if line.strip() == "EOF": break
            lines.append(line)
        content = "\n".join(lines)
        res = Tools.write_file(path, content)
        if res.get("ok"): print(res.get("output"))
        else: print("[erro]", res.get("error"))
    elif sub == "run":
        if len(parts) < 3:
            print("uso: :tool run <cmd>"); return
        cmdline = parts[2]
        if await _confirm(f"Confirmar execução de: {cmdline}? [y/N] "):
            res = Tools.run(cmdline)
            if res.get("ok"):
                print(res.get("output", ""))
            else:
                print("[erro]", res.get("error"))
        else:
            print("(cancelado)")
    else:
        print("subcomando desconhecido para :tool")

async def _handle_git(cmd: str):
    parts = cmd.split(maxsplit=2)
    if len(parts) < 2:
        print("uso: :git <status|branches|checkout|new-branch|commit> ..."); return
    sub = parts[1]
    if sub == "status":
        res = Tools.git_status()
        print(res.get("output", res.get("error", "")))
    elif sub == "branches":
        res = Tools.git_branches()
        print(res.get("output", res.get("error", "")))
    elif sub == "checkout":
        if len(parts) < 3:
            print("uso: :git checkout <branch>"); return
        res = Tools.git_checkout(parts[2])
        print(res.get("output", res.get("error", "")))
    elif sub == "new-branch":
        if len(parts) < 3:
            print("uso: :git new-branch <name>"); return
        res = Tools.git_new_branch(parts[2])
        print(res.get("output", res.get("error", "")))
    elif sub == "commit":
        if len(parts) < 3:
            print('uso: :git commit "mensagem"'); return
        msg = parts[2].strip()
        if not (msg.startswith('"') and msg.endswith('"')):
            print('coloque a mensagem entre aspas: :git commit "minha msg"'); return
        msg = msg[1:-1]
        res = Tools.git_commit(msg, add_all=True)
        print(res.get("output", res.get("error", "")))
    else:
        print("subcomando desconhecido para :git")

async def start_repl():
    session = PromptSession(history=InMemoryHistory())
    history: List[Message] = []
    print("\n🚀 Xodex – REPL (Python)\nDigite :help para comandos.\n")
    while True:
        try:
            with patch_stdout():
                line = await session.prompt_async("you> ")
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break
        text = (line or "").strip()
        if not text:
            continue
        if text == ":q":
            print("Até mais!")
            break
        if text == ":clear":
            history.clear()
            print("(histórico limpo)")
            continue
        if text == ":help":
            print(HELP)
            continue
        if text.startswith(":tool "):
            await _handle_tool(text)
            continue
        if text.startswith(":git "):
            await _handle_git(text)
            continue

        history.append({"role": "user", "content": text})

        try:
            stream_obj = await respond(history, stream=True)
            print("assistant>", end=" ", flush=True)

            if hasattr(stream_obj, "__aiter__") or hasattr(stream_obj, "__iter__"):
                try:
                    for chunk in stream_obj:  # type: ignore
                        delta = None
                        if hasattr(chunk, "choices"):
                            ch0 = chunk.choices[0]
                            delta = getattr(ch0.delta, "content", None)
                        if delta is None and hasattr(chunk, "text"):
                            try:
                                delta = chunk.text
                            except Exception:
                                delta = None
                        if delta is None and isinstance(chunk, (bytes, str)):
                            try:
                                s = chunk.decode("utf-8") if isinstance(chunk, bytes) else chunk
                            except Exception:
                                s = ""
                            if s:
                                delta = s
                        if delta:
                            print(delta, end="", flush=True)
                except TypeError:
                    async for chunk in stream_obj:  # type: ignore
                        try:
                            print(chunk.text, end="", flush=True)
                        except Exception:
                            pass
                print()
            else:
                print(stream_obj)
                history.append({"role": "assistant", "content": str(stream_obj)})
        except Exception as e:
            print(f"\n[erro] {e}")
