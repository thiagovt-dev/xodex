#!/usr/bin/env node
const { spawn, spawnSync } = require("child_process");

function hasCommand(cmd) {
  const which = process.platform === "win32" ? "where" : "which";
  return spawnSync(which, [cmd], { stdio: "ignore", shell: process.platform === "win32" }).status === 0;
}

function getPythonCmd() {
  if (process.platform === "win32") {
    if (hasCommand("py")) return "py";
    if (hasCommand("python")) return "python";
  } else {
    if (hasCommand("python3")) return "python3";
    if (hasCommand("python")) return "python";
  }
  return null;
}

function hasPythonModule(pyCmd, mod) {
  const r = spawnSync(pyCmd, ["-c", `import importlib; importlib.import_module("${mod}")`], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  return r.status === 0;
}

function canRunPipxXodex() {
  if (!hasCommand("pipx")) return false;
  const r = spawnSync("pipx", ["run", "xodex", "--version"], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  return r.status === 0;
}

function runViaPipx(args) {
  const p = spawn("pipx", ["run", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
  p.on("exit", (code) => process.exit(code));
  p.on("error", () => process.exit(1));
}

function installViaPipx() {
  if (!hasCommand("pipx")) return false;
  for (const pkg of ["xodex", "xodex-cli"]) {
    console.log(`[xodex-cli] Instalando via pipx (${pkg})...`);
    const r = spawnSync("pipx", ["install", pkg, "--force", "--pip-args=--no-cache-dir"], {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (r.status === 0) return true;
  }
  return false;
}

function installWithPip(pyCmd, pkg) {
  let r = spawnSync(pyCmd, ["-m", "pip", "install", "--upgrade", "--no-cache-dir", "--user", pkg], {
    stdio: "inherit",
    shell: process.platform === "win32",
  });
  if (r.status === 0) return true;
  if (process.platform !== "win32") {
    r = spawnSync(pyCmd, ["-m", "pip", "install", "--upgrade", "--no-cache-dir", "--break-system-packages", pkg], {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (r.status === 0) return true;
  }
  return false;
}

function tryInstall(pyCmd) {
  console.log("[xodex-cli] Preparando Xodex (Python)...");
  if (installViaPipx()) return true;
  for (const pkg of ["xodex", "xodex-cli"]) {
    console.log(`[xodex-cli] Instalando via python -m pip (${pkg})...`);
    if (installWithPip(pyCmd, pkg)) return true;
  }
  return false;
}

function run() {
  const args = process.argv.slice(2);
  const pyCmd = getPythonCmd();

  if (!pyCmd) {
    console.error(
      "[xodex-cli] Python não encontrado no sistema.\n" +
      "Instale o Python e tente novamente."
    );
    process.exit(1);
  }

  // 1) Se já dá pra rodar com pipx, prefira pipx
  if (canRunPipxXodex()) return runViaPipx(args);

  // 2) Se o Python atual enxerga o módulo, rode com python -m
  if (hasPythonModule(pyCmd, "xodex")) {
    const p = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
    p.on("exit", (code) => process.exit(code));
    p.on("error", () => process.exit(1));
    return;
  }

  // 3) Instalar (pipx -> pip) e executar
  const ok = tryInstall(pyCmd);
  if (ok && hasPythonModule(pyCmd, "xodex")) {
    const p = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
    p.on("exit", (code) => process.exit(code));
    p.on("error", () => process.exit(1));
    return;
  }
  if (canRunPipxXodex()) return runViaPipx(args);

  console.error(
    "\n[xodex-cli] Não foi possível preparar o Xodex automaticamente.\n" +
    "Instale manualmente e tente novamente:\n" +
    "  pipx install xodex   # ou: pipx install xodex-cli\n"
  );
  process.exit(1);
}

run();
