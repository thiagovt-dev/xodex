#!/usr/bin/env python3
def main():
    import asyncio
    from xodex.repl import start_repl
    from xodex.config import cfg
    print(f"Xodex inicializado (provider: {cfg['provider']})")
    asyncio.run(start_repl())
if __name__ == "__main__":
    main()
