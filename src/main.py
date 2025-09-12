#!/usr/bin/env python3
import asyncio
from src.repl import start_repl
from src.config import cfg

print(f"Iniciando CLI com provider: {cfg['provider']}")
asyncio.run(start_repl())
