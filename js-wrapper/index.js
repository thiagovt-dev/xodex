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
  // tenta --user sem cache
  let r = spawnSync(pyCmd, ["-m", "pip", "install", "--upgrade", "--no-cache-dir", "--user", pkg], {
    stdio: "inherit",
    shell: process.platform === "win32",
  });
  if (r.status === 0) return true;

  // em Linux com PEP 668, tenta --break-system-packages
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
  console.log("[xodex-cli] Módulo Python 'xodex' não encontrado. Tentando instalar...");

  // 1) pipx (preferido)
  if (installViaPipx()) return true;

  // 2) python -m pip (xodex -> xodex-cli)
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
      "Instale o Python e tente novamente:\n" +
      "  • Windows: https://www.python.org/downloads/windows/ (marque 'Add Python to PATH')\n" +
      "  • macOS:   brew install python\n" +
      "  • Linux:   use o gerenciador de pacotes da sua distro\n"
    );
    process.exit(1);
  }

  // 1) Se o módulo 'xodex' já está acessível pelo Python atual → use-o
  if (hasPythonModule(pyCmd, "xodex")) {
    const p = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
    p.on("exit", (code) => process.exit(code));
    p.on("error", () => process.exit(1));
    return;
  }

  // 2) Se pipx consegue rodar → use pipx run
  if (canRunPipxXodex()) {
    return runViaPipx(args);
  }

  // 3) Tentar instalar (pipx → pip)
  const ok = tryInstall(pyCmd);

  // 4) Após instalar: preferir Python do sistema; se não deu, tentar pipx run
  if (ok && hasPythonModule(pyCmd, "xodex")) {
    const p = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
    p.on("exit", (code) => process.exit(code));
    p.on("error", () => process.exit(1));
    return;
  }
  if (canRunPipxXodex()) {
    return runViaPipx(args);
  }

  console.error(
    "\n[xodex-cli] Não foi possível preparar o Xodex automaticamente.\n" +
    "Opções manuais:\n" +
    "  pipx install xodex       # ou: pipx install xodex-cli\n" +
    `  ${pyCmd || "python"} -m pip install --user xodex   # ou: xodex-cli\n` +
    (process.platform !== "win32" ? `  ${pyCmd || "python"} -m pip install --break-system-packages xodex\n` : "")
  );
  process.exit(1);
}

run();
