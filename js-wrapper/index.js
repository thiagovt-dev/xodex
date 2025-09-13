#!/usr/bin/env node
const { spawn, spawnSync } = require("child_process");

function hasCommand(cmd) {
  const which = process.platform === "win32" ? "where" : "which";
  return spawnSync(which, [cmd], { stdio: "ignore", shell: process.platform === "win32" }).status === 0;
}

function getPythonCmd() {
  // ordem de preferência por plataforma
  if (process.platform === "win32") {
    if (hasCommand("py")) return "py";        // launcher oficial do Python no Windows
    if (hasCommand("python")) return "python";
  } else {
    if (hasCommand("python3")) return "python3";
    if (hasCommand("python")) return "python";
  }
  return null;
}

function tryInstallWithPipModule(pyCmd) {
  if (!pyCmd) return false;
  console.log("[xodex-cli] Instalando via 'python -m pip' (modo usuário)...");
  const res = spawnSync(pyCmd, ["-m", "pip", "install", "--user", "xodex"], { stdio: "inherit", shell: process.platform === "win32" });
  return res.status === 0;
}

function tryInstall() {
  console.log("[xodex-cli] Xodex (Python) não encontrado. Tentando instalar automaticamente...");

  if (hasCommand("pipx")) {
    console.log("[xodex-cli] Instalando via pipx...");
    const res = spawnSync("pipx", ["install", "xodex"], { stdio: "inherit", shell: process.platform === "win32" });
    if (res.status === 0) return true;
  }

  if (hasCommand("pip")) {
    console.log("[xodex-cli] Instalando via pip (modo usuário)...");
    const res = spawnSync("pip", ["install", "--user", "xodex"], { stdio: "inherit", shell: process.platform === "win32" });
    if (res.status === 0) return true;
  }

  const pyCmd = getPythonCmd();
  if (tryInstallWithPipModule(pyCmd)) return true;

  console.error(
    "\n[xodex-cli] Não foi possível instalar automaticamente.\n" +
    "Verifique se o Python está instalado e no PATH.\n\n" +
    "Instalação manual sugerida:\n" +
    "  pipx install xodex\n" +
    "  # ou\n" +
    "  " + (pyCmd || "python") + " -m pip install --user xodex\n"
  );
  return false;
}

function run() {
  const args = process.argv.slice(2);
  const bin = process.platform === "win32" ? "xodex.exe" : "xodex";

  const pyCmd = getPythonCmd();
  if (!pyCmd) {
    console.error(
      "[xodex-cli] Python não encontrado no sistema.\n" +
      "Instale o Python e tente novamente:\n" +
      "  • Windows: https://www.python.org/downloads/windows/ (marque 'Add python to PATH')\n" +
      "  • macOS:   brew install python  (ou baixe do site)\n" +
      "  • Linux:   use o gerenciador de pacotes da distro\n"
    );
    process.exit(1);
  }

  if (!hasCommand(bin)) {
    const ok = tryInstall();
    if (!ok || !hasCommand(bin)) {
      console.error(
        "\n[xodex-cli] O binário ainda não foi encontrado no PATH.\n" +
        "Se você instalou via 'pip --user', pode ser necessário adicionar o diretório de scripts ao PATH.\n" +
        "Exemplos:\n" +
        "  • Linux/macOS: ~/.local/bin\n" +
        "  • Windows: %APPDATA%\\Python\\PythonXX\\Scripts  (substitua XX pela sua versão)\n"
      );
      process.exit(1);
    }
  }

  const proc = spawn(bin, args, { stdio: "inherit", shell: true });
  proc.on("exit", (code) => process.exit(code));
  proc.on("error", () => process.exit(1));
}

run();
