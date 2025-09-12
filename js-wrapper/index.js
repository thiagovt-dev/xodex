#!/usr/bin/env node
// Encaminha qualquer comando para o executável Python "xodex"
const { spawn } = require("child_process");

const bin = process.platform === "win32" ? "xodex.exe" : "xodex";
const args = process.argv.slice(2);

const proc = spawn(bin, args, { stdio: "inherit", shell: true });

proc.on("error", (err) => {
  console.error(
    `[xodex-cli] Não encontrei o binário "${bin}".\n` +
    `Instale o Xodex (Python) com:\n` +
    `  pipx install xodex   # recomendado\n` +
    `  # ou\n` +
    `  python -m pip install --user xodex\n`
  );
  process.exit(1);
});

proc.on("exit", (code) => process.exit(code));
