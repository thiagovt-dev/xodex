import asyncio
import os
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
from typing import List, Dict
from xodex.core.agent import respond
from xodex.core import tools as Tools


Message = Dict[str, str]

AGENT_MODE = False

HELP = (
    "\033[1mComandos disponíveis:\033[0m\n\n"
    "\033[36m/quit\033[0m                    sair do CLI\n"
    "\033[36m/clear\033[0m                   limpar histórico da conversa\n"
    "\033[36m/help\033[0m                    mostrar esta ajuda\n"
    "\033[36m/status\033[0m                  status do repositório git\n"
    "\033[36m/branches\033[0m                listar branches do git\n"
    "\033[36m/checkout <branch>\033[0m       trocar para uma branch\n"
    "\033[36m/new-branch <nome>\033[0m       criar e mudar para nova branch\n"
    '\033[36m/commit "mensagem"\033[0m      fazer commit com -A\n'
    "\033[36m/read <arquivo>\033[0m          ler conteúdo de um arquivo\n"
    "\033[36m/write <arquivo>\033[0m         escrever arquivo (terminar com EOF)\n"
    "\033[36m/run <comando>\033[0m           executar comando (pede confirmação)\n"
    "\033[36m/ask <texto>\033[0m            perguntar ao modelo (sem histórico)\n"
    "\033[36m/agent\033[0m                   alternar modo agente\n"
)


async def _confirm(prompt: str) -> bool:
    session = PromptSession()
    try:
        with patch_stdout():
            ans = (await session.prompt_async(prompt)).strip().lower()
        return ans in ("y", "yes", "s", "sim")
    except Exception:
        return False


async def _handle_read(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("uso: /read <arquivo>")
        return
    res = Tools.read_file(parts[1])
    if res.get("ok"):
        print(res.get("output", ""))
    else:
        print("[erro]", res.get("error"))


async def _handle_write(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("uso: /write <arquivo>")
        return
    path = parts[1]
    print("Digite o conteúdo. Finalize com uma linha contendo apenas 'EOF'.")
    lines: List[str] = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    content = "\n".join(lines)
    if AGENT_MODE:
        ok = await _confirm(f"Confirmar escrita em {path}? [y/N] ")
        if not ok:
            print("(cancelado)")
            return
    res = Tools.write_file(path, content)
    if res.get("ok"):
        print(res.get("output"))
    else:
        print("[erro]", res.get("error"))


async def _handle_run(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("uso: /run <comando>")
        return
    cmdline = parts[1]
    if await _confirm(f"Confirmar execução de: {cmdline}? [y/N] "):
        res = Tools.run(cmdline)
        if res.get("ok"):
            print(res.get("output", ""))
        else:
            print("[erro]", res.get("error"))
    else:
        print("(cancelado)")


async def _handle_status():
    res = Tools.git_status()
    print(res.get("output", res.get("error", "")))


async def _handle_branches():
    res = Tools.git_branches()
    print(res.get("output", res.get("error", "")))


async def _handle_checkout(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("uso: /checkout <branch>")
        return
    if AGENT_MODE:
        ok = await _confirm(f"Confirmar checkout para {parts[1]}? [y/N] ")
        if not ok:
            print("(cancelado)")
            return
    res = Tools.git_checkout(parts[1])
    print(res.get("output", res.get("error", "")))


async def _handle_new_branch(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("uso: /new-branch <nome>")
        return
    if AGENT_MODE:
        ok = await _confirm(f"Confirmar criação da branch {parts[1]}? [y/N] ")
        if not ok:
            print("(cancelado)")
            return
    res = Tools.git_new_branch(parts[1])
    print(res.get("output", res.get("error", "")))


async def _handle_commit(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print('uso: /commit "mensagem"')
        return
    msg = parts[1].strip()
    if not (msg.startswith('"') and msg.endswith('"')):
        print('coloque a mensagem entre aspas: /commit "minha msg"')
        return
    msg = msg[1:-1]
    if AGENT_MODE:
        ok = await _confirm(f"Confirmar commit: {msg}? [y/N] ")
        if not ok:
            print("(cancelado)")
            return
    res = Tools.git_commit(msg, add_all=True)
    print(res.get("output", res.get("error", "")))


async def _handle_ask(cmd: str):
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("uso: /ask <texto>")
        return
    question = parts[1]
    try:
        ans = await respond([{"role": "user", "content": question}], stream=False)
        print(f"\033[36mXodex\033[0m> {ans}")
    except Exception as e:
        print(f"[erro] {e}")


async def _handle_agent(_: str):
    global AGENT_MODE
    if AGENT_MODE:
        AGENT_MODE = False
        print("Modo agente desativado.")
        return
    if await _confirm("Permitir que o agente aplique alterações? [y/N] "):
        AGENT_MODE = True
        print("Modo agente ativado.")
    else:
        print("(modo agente não ativado)")


class ThinkingIndicator:
    def __init__(self):
        self.is_running = False
        self.start_time = None
        self.task = None

    def start(self):
        """Inicia o indicador de thinking"""
        self.is_running = True
        self.start_time = time.time()
        self.task = asyncio.create_task(self._animate())
        return self.task

    async def stop(self):
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        print("\r" + " " * 50 + "\r", end="", flush=True)

    async def _animate(self):
        thinking_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        print()

        try:
            char_index = 0
            while self.is_running:
                elapsed = int(time.time() - self.start_time)
                char = thinking_chars[char_index % len(thinking_chars)]
                print(
                    f"\r\033[90m▌ {char} Working ({elapsed}s • Esc to interrupt)\033[0m",
                    end="",
                    flush=True,
                )
                char_index += 1
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass


def _print_welcome():
    current_path = os.getcwd()
    print()
    print("🚀 Bem vindo ao Xodex CLI")
    print()
    print(f"Você está usando o Xodex CLI em \033[90m{current_path}\033[0m")
    print()
    print("\033[90mPara iniciar, descreva uma task ou tente um dos comandos:\033[0m")
    print("\033[90m/status - mostra status do repositório git\033[0m")
    print("\033[90m/help - mostra todos os comandos disponíveis\033[0m")
    print("\033[90m/run - executa um comando\033[0m")
    print("\033[90m/ask - pergunta ao modelo\033[0m")
    print("\033[90m/agent - alterna modo agente\033[0m")
    print("\033[90m/quit - sai do CLI\033[0m")
    print()


async def start_repl():
    session = PromptSession(history=InMemoryHistory())
    history: List[Message] = []
    _print_welcome()
    while True:
        try:
            with patch_stdout():
                line = await session.prompt_async(
                    "\n",
                    placeholder=HTML(
                        "<ansibrightblack>Pergunte algo ao Xodex</ansibrightblack>"
                    ),
                )
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break
        text = (line or "").strip()
        if not text:
            continue

        if text == "/quit" or text == "/q":
            print("Até mais!")
            break
        if text == "/clear":
            history.clear()
            print("(histórico limpo)")
            continue
        if text == "/help":
            print(HELP)
            continue
        if text == "/status":
            await _handle_status()
            continue
        if text == "/branches":
            await _handle_branches()
            continue
        if text == "/agent":
            await _handle_agent(text)
            continue
        if text.startswith("/ask "):
            await _handle_ask(text)
            continue
        if text.startswith("/checkout "):
            await _handle_checkout(text)
            continue
        if text.startswith("/new-branch "):
            await _handle_new_branch(text)
            continue
        if text.startswith("/commit "):
            await _handle_commit(text)
            continue
        if text.startswith("/read "):
            await _handle_read(text)
            continue
        if text.startswith("/write "):
            await _handle_write(text)
            continue
        if text.startswith("/run "):
            await _handle_run(text)
            continue

        print(f"\n\033[34mUser\033[0m> {text}")

        history.append({"role": "user", "content": text})

        thinking = ThinkingIndicator()

        try:
            thinking.start()

            await asyncio.sleep(0.2)

            stream_obj = await respond(history, stream=True)

            await thinking.stop()

            print("\033[36mXodex\033[0m>", end=" ", flush=True)
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
                                s = (
                                    chunk.decode("utf-8")
                                    if isinstance(chunk, bytes)
                                    else chunk
                                )
                            except Exception:
                                s = ""
                            if s:
                                delta = s
                        if delta:
                            print(delta, end="", flush=True)
                except TypeError:
                    async for chunk in stream_obj:
                        try:
                            print(chunk.text, end="", flush=True)
                        except Exception:
                            pass
                print()
            else:
                print(stream_obj)
                history.append({"role": "assistant", "content": str(stream_obj)})
        except Exception as e:
            await thinking.stop()
            print(f"\n[erro] {e}")
