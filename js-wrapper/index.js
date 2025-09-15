#!/usr/bin/env node
const { spawn, spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

/* ----------------------- Utils ----------------------- */
function hasCommand(cmd) {
  const which = process.platform === "win32" ? "where" : "which";
  return spawnSync(which, [cmd], {
    stdio: "ignore",
    shell: process.platform === "win32",
  }).status === 0;
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

function findSemver(str) {
  const m = (str || "").match(/\d+\.\d+\.\d+/);
  return m ? m[0] : null;
}

function getWrapperVersion() {
  try {
    const pkgPath = path.join(__dirname, "package.json");
    const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
    return pkg.version || "unknown";
  } catch (_) {
    return "unknown";
  }
}

/** Tenta descobrir a versão da engine via Python (importlib.metadata) */
function getEngineVersionViaPython(pyCmd) {
  if (!pyCmd) return null;

  const pySnippet = `
try:
    try:
        import importlib.metadata as m
    except Exception:
        import importlib_metadata as m  # backport
    ver = None
    for name in ("xodex-cli","xodex"):
        try:
            ver = m.version(name)
            if ver: break
        except Exception:
            pass
    if not ver:
        try:
            import xodex as _x
            ver = getattr(_x, "__version__", "") or ""
        except Exception:
            ver = ""
    print(ver)
except Exception:
    print("")
`.trim();

  const r = spawnSync(pyCmd, ["-c", pySnippet], {
    encoding: "utf8",
    shell: process.platform === "win32",
  });
  if (r.status === 0) {
    const v = findSemver(r.stdout);
    if (v) return v;
  }

  for (const mod of ["xodex_cli", "xodex"]) {
    const r2 = spawnSync(
      pyCmd,
      ["-m", mod, "--version"],
      { encoding: "utf8", shell: process.platform === "win32" }
    );
    if (r2.status === 0) {
      const v = findSemver(r2.stdout || r2.stderr);
      if (v) return v;
    }
  }
  return null;
}

/** Tenta descobrir a versão via pipx (executa o CLI) */
function getEngineVersionViaPipx() {
  if (!hasCommand("pipx")) return null;

  // 1) pipx run xodex --version
  let r = spawnSync("pipx", ["run", "xodex", "--version"], {
    encoding: "utf8",
    shell: process.platform === "win32",
  });
  if (r.status === 0) {
    const v = findSemver(r.stdout || r.stderr);
    if (v) return v;
  }

  // 2) pipx run --spec xodex-cli xodex --version
  r = spawnSync("pipx", ["run", "--spec", "xodex-cli", "xodex", "--version"], {
    encoding: "utf8",
    shell: process.platform === "win32",
  });
  if (r.status === 0) {
    const v = findSemver(r.stdout || r.stderr);
    if (v) return v;
  }
  return null;
}

function canRunPipxXodex() {
  if (!hasCommand("pipx")) return false;

  // 1) tenta 'pipx run xodex --version'
  let r = spawnSync("pipx", ["run", "xodex", "--version"], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  if (r.status === 0) return true;

  // 2) tenta 'pipx run --spec xodex-cli xodex --version'
  r = spawnSync("pipx", ["run", "--spec", "xodex-cli", "xodex", "--version"], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  return r.status === 0;
}

function runViaPipx(args) {
  let probe = spawnSync("pipx", ["run", "xodex", "--version"], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  const cmd = probe.status === 0
    ? ["run", "xodex", ...args]
    : ["run", "--spec", "xodex-cli", "xodex", ...args];

  const p = spawn("pipx", cmd, { stdio: "inherit", shell: process.platform === "win32" });
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

/* ---------------- Version switches (early exit) ---------------- */
(function maybePrintVersionsAndExit() {
  const args = process.argv.slice(2);
  const askWrapper = args.includes("--wrapper-version");
  const askEngine = args.includes("--engine-version");
  const askCombined = args.includes("--version") || args.includes("-v");

  if (!askWrapper && !askEngine && !askCombined) return;

  const wrapper = getWrapperVersion();

  let engine = null;
  const pyCmd = getPythonCmd();
  engine = getEngineVersionViaPython(pyCmd) || getEngineVersionViaPipx();

  if (askWrapper && !askCombined && !askEngine) {
    console.log(wrapper);
    process.exit(0);
  }
  if (askEngine && !askCombined && !askWrapper) {
    console.log(engine || "unknown");
    process.exit(0);
  }
  if (askCombined) {
    console.log(engine ? `${wrapper} (engine ${engine})` : `${wrapper}`);
    process.exit(0);
  }
})();

/* ----------------------- Normal run ----------------------- */
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

  if (canRunPipxXodex()) return runViaPipx(args);

  if (hasPythonModule(pyCmd, "xodex")) {
    const p = spawn(pyCmd, ["-m", "xodex", ...args], { stdio: "inherit", shell: process.platform === "win32" });
    p.on("exit", (code) => process.exit(code));
    p.on("error", () => process.exit(1));
    return;
  }

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
