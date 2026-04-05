"""
Dotfiles setup script.

Links config files from this repo into their target locations.
- Linux: symlinks everywhere
- Windows: junctions (dirs) + hard links (files) — no admin required

Run: python setup.py
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DOTFILES_DIR = Path(__file__).resolve().parent
IS_WINDOWS = sys.platform == "win32"
ENV_FILE = DOTFILES_DIR / ".env"

_TEMPLATE_RE = re.compile(r"\$\{(\w+)\}")


def load_env() -> dict[str, str]:
    """Load key=value pairs from .env file."""
    env: dict[str, str] = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip()
    return env


# --- Output ---

try:
    from rich.console import Console

    _console = Console()

    def log(status: str, msg: str, extra: str = "") -> None:
        styles = {
            "OK": "[bold green]  OK[/]",
            "HARDLINK": "[bold cyan]  HARDLINK[/]",
            "SYMLINK": "[bold cyan]  SYMLINK[/]",
            "JUNCTION": "[bold cyan]  JUNCTION[/]",
            "BACKUP": "[bold yellow]  BACKUP[/]",
            "COPY": "[bold magenta]  COPY[/]",
            "TEMPLATE": "[bold magenta]  TEMPLATE[/]",
            "SKIP": "[dim]  SKIP[/]",
            "ERROR": "[bold red]  ERROR[/]",
            "HEADER": "[bold]",
        }
        prefix = styles.get(status, f"  {status}")
        if status == "MODULE":
            _console.print(f"\n[bold dodger_blue2]\\[{msg}][/] {extra}")
        elif status == "HEADER":
            _console.print(f"{prefix}{msg}[/]")
        else:
            _console.print(f"{prefix}  {msg}")

except ImportError:

    def log(status: str, msg: str, extra: str = "") -> None:
        if status == "MODULE":
            print(f"\n[{msg}] {extra}")
        elif status == "HEADER":
            print(msg)
        else:
            print(f"  {status}  {msg}")


def _windows_documents() -> Path:
    """Get the Windows Documents folder (handles OneDrive redirection)."""
    if not IS_WINDOWS:
        return Path.home() / "Documents"
    import ctypes.wintypes

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 0x0005, None, 0, buf)
    return Path(buf.value)


# Each module: source dir in repo → target on system.
# "platform" can be "all", "linux", or "windows".
# All files/dirs inside the source get linked into the target.
MODULES = {
    "claude": {
        "target": Path.home() / ".claude",
        "platform": "all",
    },
    "powershell": {
        "target": _windows_documents() / "WindowsPowerShell" if IS_WINDOWS else None,
        "platform": "windows",
    },
    "pwsh": {
        "target": _windows_documents() / "PowerShell" if IS_WINDOWS else None,
        "platform": "windows",
    },
    "git": {
        "target": Path.home(),
        "platform": "all",
    },
    "windows-terminal": {
        "target": (
            Path.home()
            / "AppData"
            / "Local"
            / "Packages"
            / "Microsoft.WindowsTerminal_8wekyb3d8bbwe"
            / "LocalState"
            if IS_WINDOWS
            else None
        ),
        "platform": "windows",
    },
    "nvim": {
        "target": (
            Path.home() / "AppData" / "Local" / "nvim"
            if IS_WINDOWS
            else Path.home() / ".config" / "nvim"
        ),
        "platform": "all",
    },
    "sharex": {
        "target": Path("D:/ShareX") if IS_WINDOWS else None,
        "platform": "windows",
    },
    "oh-my-posh": {
        "target": (
            Path.home() / "AppData" / "Local" / "Programs" / "oh-my-posh"
            if IS_WINDOWS
            else Path.home() / ".config" / "oh-my-posh"
        ),
        "platform": "all",
    },
    "fastfetch": {
        "target": Path.home() / ".config" / "fastfetch",
        "platform": "all",
        "platform_subdirs": True,
    },
    "glazewm": {
        "target": Path.home() / ".glzr" / "glazewm",
        "platform": "windows",
    },
    "glazewm-extra": {
        "target": Path.home() / ".config",
        "platform": "windows",
    },
    "yasb": {
        "target": Path.home() / ".config" / "yasb",
        "platform": "windows",
        "template": True,
    },
}


def current_platform() -> str:
    return "windows" if IS_WINDOWS else "linux"


def should_run(platform: str) -> bool:
    return platform == "all" or platform == current_platform()


# --- Windows helpers ---


def is_junction(path: Path) -> bool:
    if not IS_WINDOWS:
        return False
    try:
        import ctypes

        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        return attrs != -1 and bool(attrs & 0x400)
    except Exception:
        return False


def is_hardlink_to(src: Path, dst: Path) -> bool:
    try:
        return dst.stat().st_ino == src.stat().st_ino and dst.stat().st_ino != 0
    except OSError:
        return False


# --- Linking ---


def backup_existing(dst: Path) -> None:
    backup = dst.with_suffix(dst.suffix + ".bak")
    log("BACKUP", f"{dst} -> {backup}")
    if dst.is_dir():
        if backup.exists():
            shutil.rmtree(str(backup))
        shutil.move(str(dst), str(backup))
    else:
        if backup.exists():
            backup.unlink()
        dst.rename(backup)


def render_template(src: Path, dst: Path, env: dict[str, str]) -> None:
    """Copy src to dst, replacing ${VAR} placeholders with values from env."""
    content = src.read_text(encoding="utf-8")
    rendered = _TEMPLATE_RE.sub(lambda m: env.get(m.group(1), m.group(0)), content)
    if dst.exists():
        if dst.read_text(encoding="utf-8") == rendered:
            log("OK", str(dst))
            return
        backup_existing(dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(rendered, encoding="utf-8")
    log("TEMPLATE", f"{dst} -> {src}")


def link_dir(src: Path, dst: Path) -> None:
    if is_junction(dst) or dst.is_symlink():
        try:
            if dst.resolve() == src.resolve():
                log("OK", str(dst))
                return
        except OSError:
            pass
        if IS_WINDOWS:
            subprocess.run(["cmd", "/c", "rmdir", str(dst)], check=True)
        else:
            dst.unlink()

    if dst.exists():
        backup_existing(dst)

    dst.parent.mkdir(parents=True, exist_ok=True)

    if IS_WINDOWS:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(dst), str(src)],
            check=True,
            capture_output=True,
        )
        log("JUNCTION", f"{dst} -> {src}")
    else:
        os.symlink(src, dst)
        log("SYMLINK", f"{dst} -> {src}")


def link_file(src: Path, dst: Path) -> None:
    if dst.is_symlink():
        if dst.resolve() == src.resolve():
            log("OK", str(dst))
            return
        dst.unlink()
    elif dst.exists():
        if IS_WINDOWS and is_hardlink_to(src, dst):
            log("OK", str(dst))
            return
        backup_existing(dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)

    if IS_WINDOWS:
        try:
            os.link(src, dst)
            log("HARDLINK", f"{dst} -> {src}")
        except OSError:
            shutil.copy2(src, dst)
            log("COPY", f"{dst} -> {src}")
    else:
        os.symlink(src, dst)
        log("SYMLINK", f"{dst} -> {src}")


def link(src: Path, dst: Path) -> None:
    if src.is_dir():
        link_dir(src, dst)
    else:
        link_file(src, dst)


def setup_module(
    name: str,
    target: Path,
    src_dir: Path,
    platform_subdirs: bool = False,
    template: bool = False,
    env: dict[str, str] | None = None,
) -> None:
    log("MODULE", name, f"{src_dir} -> {target}")

    if not src_dir.exists():
        log("SKIP", "source dir not found")
        return

    target.mkdir(parents=True, exist_ok=True)

    platform_dir_names = {"windows", "linux"}

    for item in sorted(src_dir.iterdir()):
        if platform_subdirs and item.is_dir() and item.name in platform_dir_names:
            continue
        if template and item.is_file() and env is not None:
            render_template(item, target / item.name, env)
        else:
            link(item, target / item.name)

    if platform_subdirs:
        plat_dir = src_dir / current_platform()
        if plat_dir.is_dir():
            for item in sorted(plat_dir.iterdir()):
                if template and item.is_file() and env is not None:
                    render_template(item, target / item.name, env)
                else:
                    link(item, target / item.name)


def main() -> None:
    log("HEADER", f"Dotfiles: {DOTFILES_DIR}")
    log("HEADER", f"Platform: {current_platform()}")

    env = load_env()

    for name, cfg in MODULES.items():
        if not should_run(cfg["platform"]):
            log("MODULE", name, f"SKIP (platform: {cfg['platform']})")
            continue

        src_dir = DOTFILES_DIR / name
        setup_module(
            name,
            cfg["target"],
            src_dir,
            platform_subdirs=cfg.get("platform_subdirs", False),
            template=cfg.get("template", False),
            env=env,
        )

    log("HEADER", "\nDone.")


if __name__ == "__main__":
    main()
