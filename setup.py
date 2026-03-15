"""
Dotfiles setup script.

Links config files from this repo into their target locations.
- Linux: symlinks everywhere
- Windows: junctions (dirs) + hard links (files) — no admin required

Run: python setup.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

DOTFILES_DIR = Path(__file__).resolve().parent
IS_WINDOWS = sys.platform == "win32"


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
        "target": Path.home()
        / "AppData"
        / "Local"
        / "Packages"
        / "Microsoft.WindowsTerminal_8wekyb3d8bbwe"
        / "LocalState"
        if IS_WINDOWS
        else None,
        "platform": "windows",
    },
    # "hyprland": {
    #     "target": Path.home() / ".config" / "hypr",
    #     "platform": "linux",
    # },
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
    print(f"  BACKUP  {dst} -> {backup}")
    if dst.is_dir():
        if backup.exists():
            shutil.rmtree(str(backup))
        shutil.move(str(dst), str(backup))
    else:
        if backup.exists():
            backup.unlink()
        dst.rename(backup)


def link_dir(src: Path, dst: Path) -> None:
    if is_junction(dst) or dst.is_symlink():
        try:
            if dst.resolve() == src.resolve():
                print(f"  OK  {dst}")
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
        print(f"  JUNCTION  {dst} -> {src}")
    else:
        os.symlink(src, dst)
        print(f"  SYMLINK  {dst} -> {src}")


def link_file(src: Path, dst: Path) -> None:
    if dst.is_symlink():
        if dst.resolve() == src.resolve():
            print(f"  OK  {dst}")
            return
        dst.unlink()
    elif dst.exists():
        if IS_WINDOWS and is_hardlink_to(src, dst):
            print(f"  OK  {dst}")
            return
        backup_existing(dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)

    if IS_WINDOWS:
        try:
            os.link(src, dst)
            print(f"  HARDLINK  {dst} -> {src}")
        except OSError:
            os.symlink(src, dst)
            print(f"  SYMLINK  {dst} -> {src}")
    else:
        os.symlink(src, dst)
        print(f"  SYMLINK  {dst} -> {src}")


def link(src: Path, dst: Path) -> None:
    if src.is_dir():
        link_dir(src, dst)
    else:
        link_file(src, dst)


def setup_module(name: str, target: Path, src_dir: Path) -> None:
    print(f"\n[{name}] {src_dir} -> {target}")

    if not src_dir.exists():
        print("  SKIP  source dir not found")
        return

    target.mkdir(parents=True, exist_ok=True)

    for item in sorted(src_dir.iterdir()):
        link(item, target / item.name)


def main() -> None:
    print(f"Dotfiles: {DOTFILES_DIR}")
    print(f"Platform: {current_platform()}")

    for name, cfg in MODULES.items():
        if not should_run(cfg["platform"]):
            print(f"\n[{name}] SKIP (platform: {cfg['platform']})")
            continue

        src_dir = DOTFILES_DIR / name
        setup_module(name, cfg["target"], src_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
