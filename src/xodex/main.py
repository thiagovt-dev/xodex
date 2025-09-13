#!/usr/bin/env python3
import asyncio
from xodex.repl import start_repl
from xodex.config import cfg
from xodex.setup import ensure_config_ready, run_first_time_setup


def run_interactive():
    ensure_config_ready()
    print(
        f"Xodex inicializado (provider: {cfg['provider']} | modelo: {cfg[cfg['provider']]['model']})"
    )
    asyncio.run(start_repl())


# compat
def main():
    run_interactive()


if __name__ == "__main__":
    main()
