#!/usr/bin/env python3
import sys
from xodex.repl import start_repl
from xodex.config import cfg
from xodex.setup import ensure_config_ready, run_first_time_setup


def main():
    if len(sys.argv) > 1 and sys.argv[1] in {"setup", "config"}:
        run_first_time_setup()
        return
    ensure_config_ready()
    print(
        f"Xodex inicializado (provider: {cfg['provider']} | modelo: {cfg[cfg['provider']]['model']})"
    )
    import asyncio

    asyncio.run(start_repl())


if __name__ == "__main__":
    main()
