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
ASK_MODE = False  # Nova variável para controlar o modo ask

HELP = (
    "Comandos disponíveis:\n\n"
    "/quit                    sair do CLI\n"
    "/clear                   limpar histórico da conversa\n"
    "/help                    mostrar esta ajuda\n"
    "/status                  status do repositório git\n"
    "/branches                listar branches do git\n"
    "/checkout <branch>       trocar para uma branch\n"
    "/new-branch <nome>       criar e mudar para nova branch\n"
    '/commit "mensagem"       fazer commit com -A\n'
    "/read <arquivo>          ler conteúdo de um arquivo\n"
    "/write <arquivo>         escrever arquivo (terminar com EOF)\n"
    "/run <comando>           executar comando (pede confirmação)\n"
    "/ask <texto>            perguntar ao modelo (sem histórico)\n"
    "/agent                   alternar modo agente\n"
    "/normal                  voltar ao modo normal\n"
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
    global ASK_MODE
    parts = cmd.split(maxsplit=1)
    if len(parts) < 2:
        print("💡 Modo ask ativado. Digite sua pergunta:")
        ASK_MODE = True  # Ativar modo ask quando usado sem argumentos
        return
    question = parts[1]
    
    # Ativar modo ask temporariamente
    ASK_MODE = True
    
    try:
        thinking = ThinkingIndicator()
        thinking.start()
        
        await asyncio.sleep(0.3)
        
        ans = await respond([{"role": "user", "content": question}], stream=False, mode="ask")
        
        await thinking.stop()
        
        # Mostrar resposta de forma mais organizada
        print(f"Xodex> {ans}")
    except Exception as e:
        await thinking.stop()
        print(f"[erro] {e}")
    finally:
        ASK_MODE = False


async def _handle_agent(_: str):
    global AGENT_MODE
    if AGENT_MODE:
        AGENT_MODE = False
        print("✓ Modo agente desativado")
        return
    if await _confirm("Permitir que o agente aplique alterações? [y/N] "):
        AGENT_MODE = True
        print("✓ Modo agente ativado")
    else:
        print("✗ Modo agente não ativado")


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
        # Limpar a linha do thinking
        print("\r\033[K", end="", flush=True)  # Limpa a linha atual

    async def _animate(self):
        thinking_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        print()  # Nova linha para o thinking

        try:
            char_index = 0
            while self.is_running:
                elapsed = int(time.time() - self.start_time)
                char = thinking_chars[char_index % len(thinking_chars)]
                message = f"{char} Pensando... ({elapsed}s)"
                print(f"\r{message}", end="", flush=True)
                char_index += 1
                await asyncio.sleep(0.15)  # Timing balanceado
        except asyncio.CancelledError:
            pass


def _get_mode_indicator():
    """Retorna o indicador visual do modo ativo"""
    if AGENT_MODE:
        return "[AGENT] "
    elif ASK_MODE:
        return "[ASK] "
    else:
        return ""


def _print_welcome():
    current_path = os.getcwd()
    print()
    print("🚀 Bem vindo ao Xodex CLI")
    print()
    print(f"📁 Diretório: {current_path}")
    print()
    print("💡 Dicas:")
    print("   • Descreva uma task ou use um comando")
    print(f"   • Digite \033[96m/help\033[0m para ver todos os comandos")
    print(f"   • Use \033[92m/agent\033[0m para modo agente")
    print(f"   • Use \033[95m/ask\033[0m para perguntas rápidas")
    print()
    print("─" * 50)
    print()


async def start_repl():
    session = PromptSession(history=InMemoryHistory())
    history: List[Message] = []
    _print_welcome()
    while True:
        try:
            mode_indicator = _get_mode_indicator()
            with patch_stdout():
                print()  # Adiciona um espaço acima da mensagem
                line = await session.prompt_async(
                    f"{mode_indicator}",
                    placeholder=HTML(
                        "<ansibrightblack>Digite sua mensagem ou comando...</ansibrightblack>"
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
            print("✓ Histórico limpo")
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
        if text == "/ask" or text.startswith("/ask "):
            await _handle_ask(text)
            continue
        if text == "/normal":
            global ASK_MODE
            ASK_MODE = False
            print("✓ Modo normal ativado")
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

        # Mostrar entrada do usuário de forma mais limpa
        print(f"\n\033[1;34mUser>\033[0m {text}")

        history.append({"role": "user", "content": text})

        thinking = ThinkingIndicator()

        try:
            thinking.start()

            await asyncio.sleep(0.3)  # Pequeno delay para mostrar o thinking

            # Determinar o modo para passar ao respond
            mode = "agent" if AGENT_MODE else "normal"
            stream_obj = await respond(history, stream=True, mode=mode)

            await thinking.stop()

            # Mostrar resposta de forma mais organizada
            print('\n\033[1;36mXodex>\033[0m', end=" ", flush=True)
            
            response_content = ""
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
                            response_content += delta
                except TypeError:
                    async for chunk in stream_obj:
                        try:
                            print(chunk.text, end="", flush=True)
                            response_content += chunk.text
                        except Exception:
                            pass
                print()  # Nova linha após a resposta
                history.append({"role": "assistant", "content": response_content})
            else:
                print(stream_obj)
                history.append({"role": "assistant", "content": str(stream_obj)})
                
        except Exception as e:
            await thinking.stop()
            print(f"\n[erro] {e}")
