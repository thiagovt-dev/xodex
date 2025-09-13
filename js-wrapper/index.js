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
  const res = spawnSync(pyCmd, ["-c", `import importlib; importlib.import_module("${mod}")`], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  return res.status === 0;
}

function installWithPip(pyCmd, pkg) {
  // 1) user install
  let r = spawnSync(pyCmd, ["-m", "pip", "install", "--user", pkg], {
    stdio: "inherit",
    shell: process.platform === "win32",
  });
  if (r.status === 0) return true;

  // 2) se falhou e estamos em Linux (ambiente externally-managed), tenta break-system-packages
  if (process.platform !== "win32") {
    r = spawnSync(pyCmd, ["-m", "pip", "install", "--break-system-packages", pkg], {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (r.status === 0) return true;
  }
  return false;
}

function tryInstall(pyCmd) {
  console.log("[xodex-cli] Módulo Python 'xodex' não encontrado. Tentando instalar...");

  // 0) pipx (preferível quando disponível)
  if (hasCommand("pipx")) {
    for (const pkg of ["xodex", "xodex-cli"]) {
      console.log(`[xodex-cli] Instalando via pipx (${pkg})...`);
      const r = spawnSync("pipx", ["install", pkg], { stdio: "inherit", shell: process.platform === "win32" });
      if (r.status === 0) return true;
    }
    console.log("[xodex-cli] pipx falhou, tentando pip...");
  }

  // 1) python -m pip (garante mesmo interpretador)
  for (const pkg of ["xodex", "xodex-cli"]) {
    console.log(`[xodex-cli] Instalando via python -m pip (${pkg})...`);
    if (installWithPip(pyCmd, pkg)) return true;
  }

  console.error(
    "\n[xodex-cli] Falha ao instalar automaticamente.\n" +
    "Instale manualmente e tente de novo:\n" +
    "  pipx install xodex        # ou: pipx install xodex-cli\n" +
    `  ${pyCmd || "python"} -m pip install --user xodex   # ou: xodex-cli\n` +
    (process.platform !== "win32" ? `  ${pyCmd || "python"} -m pip install --break-system-packages xodex\n` : "")
  );
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
      "  • macOS:   brew install python  (ou baixe do site)\n" +
      "  • Linux:   use o gerenciador de pacotes da sua distro\n"
    );
    process.exit(1);
  }

  // Garante que o módulo exista; senão, instala
  if (!hasPythonModule(pyCmd, "xodex")) {
    const ok = tryInstall(pyCmd);
    if (!ok || !hasPythonModule(pyCmd, "xodex")) process.exit(1);
  }

  // Executa SEM recursão: python -m xodex ...
  const proc = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
  proc.on("exit", (code) => process.exit(code));
  proc.on("error", () => process.exit(1));
}

run();
