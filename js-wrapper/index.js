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
  const res = spawnSync(pyCmd, ["-c", `import importlib, sys; importlib.import_module("${mod}")`], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  return res.status === 0;
}

function tryInstall(pyCmd) {
  console.log("[xodex-cli] Módulo Python 'xodex' não encontrado. Tentando instalar...");

  // Try pipx first (recommended for externally managed environments)
  if (hasCommand("pipx")) {
    console.log("[xodex-cli] Instalando via pipx...");
    const r = spawnSync("pipx", ["install", "xodex-cli"], { stdio: "inherit", shell: process.platform === "win32" });
    if (r.status === 0) return true;
    console.log("[xodex-cli] pipx falhou, tentando outras opções...");
  }

  // Try pip with --break-system-packages flag (for externally managed environments)
  if (hasCommand("pip")) {
    console.log("[xodex-cli] Instalando via pip com --break-system-packages...");
    const r = spawnSync("pip", ["install", "--break-system-packages", "xodex-cli"], { stdio: "inherit", shell: process.platform === "win32" });
    if (r.status === 0) return true;
  }

  // Try python -m pip with --break-system-packages flag
  if (pyCmd) {
    console.log("[xodex-cli] Instalando via 'python -m pip' com --break-system-packages...");
    const r = spawnSync(pyCmd, ["-m", "pip", "install", "--break-system-packages", "xodex-cli"], {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (r.status === 0) return true;
  }

  // Try traditional user installation as last resort
  if (hasCommand("pip")) {
    console.log("[xodex-cli] Tentando instalação tradicional (modo usuário)...");
    const r = spawnSync("pip", ["install", "--user", "xodex-cli"], { stdio: "inherit", shell: process.platform === "win32" });
    if (r.status === 0) return true;
  }

  if (pyCmd) {
    console.log("[xodex-cli] Tentando instalação tradicional via 'python -m pip' (modo usuário)...");
    const r = spawnSync(pyCmd, ["-m", "pip", "install", "--user", "xodex-cli"], {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (r.status === 0) return true;
  }

  console.error(
    "\n[xodex-cli] Falha ao instalar automaticamente.\n" +
    "Instale manualmente e tente de novo:\n" +
    "  pipx install xodex-cli\n" +
    "  # ou (para ambientes externamente gerenciados)\n" +
    `  ${pyCmd || "python"} -m pip install --break-system-packages xodex-cli\n` +
    "  # ou (instalação tradicional)\n" +
    `  ${pyCmd || "python"} -m pip install --user xodex-cli\n`
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

  // Garante que o módulo Python exista; senão, instala
  if (!hasPythonModule(pyCmd, "xodex")) {
    const ok = tryInstall(pyCmd);
    if (!ok || !hasPythonModule(pyCmd, "xodex")) {
      process.exit(1);
    }
  }

  const proc = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
  proc.on("exit", (code) => process.exit(code));
  proc.on("error", () => process.exit(1));
}

run();
