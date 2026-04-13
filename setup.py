"""
Dotfiles setup script.

Links config files from this repo into their target locations.
- Linux: symlinks everywhere
- Windows: junctions (dirs) + hard links (files) — no admin required

Usage:
    python setup.py                    # link all modules
    python setup.py --dry-run          # preview without changes
    python setup.py --status           # check link health
    python setup.py --clean            # remove managed links
    python setup.py --module nvim      # only process specific module(s)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DOTFILES_DIR = Path(__file__).resolve().parent
IS_WINDOWS = sys.platform == "win32"
ENV_FILE = DOTFILES_DIR / ".env"
MANIFEST_FILE = DOTFILES_DIR / ".setup-manifest.json"

_TEMPLATE_RE = re.compile(r"\$\{(\w+)\}")

# Top-level dirs that are not modules (skipped by unreferenced-dir check).
_IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".ruff_cache",
    ".github",
    ".vscode",
    "node_modules",
    ".venv",
}


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


# --- Manifest ---


def load_manifest() -> dict:
    """Load the link manifest from disk."""
    if MANIFEST_FILE.exists():
        try:
            return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            return {"managed": {}}
    return {"managed": {}}


def save_manifest(manifest: dict) -> None:
    """Persist the link manifest to disk."""
    MANIFEST_FILE.write_text(
        json.dumps(manifest, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


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
            "MISSING": "[bold red]  MISSING[/]",
            "WRONG": "[bold yellow]  WRONG[/]",
            "REMOVED": "[bold red]  REMOVED[/]",
            "RESTORED": "[bold green]  RESTORED[/]",
            "WARNING": "[bold yellow]  WARNING[/]",
            "DRY": "[bold yellow]  DRY[/]",
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


# --- Modules ---
# Each module: source dir in repo -> target on system.
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
        "target": _windows_documents() / "ShareX" if IS_WINDOWS else None,
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
        dst_ino = dst.stat().st_ino
        return dst_ino != 0 and dst_ino == src.stat().st_ino
    except OSError:
        return False


# --- State checks ---


def check_file_link(src: Path, dst: Path) -> str:
    """Check file link state. Returns 'ok', 'wrong_symlink', 'wrong_file', or 'missing'."""
    if dst.is_symlink():
        try:
            if dst.resolve() == src.resolve():
                return "ok"
        except OSError:
            pass
        return "wrong_symlink"
    elif dst.exists():
        if IS_WINDOWS and is_hardlink_to(src, dst):
            return "ok"
        return "wrong_file"
    return "missing"


def check_dir_link(src: Path, dst: Path) -> str:
    """Check dir link state. Returns 'ok', 'wrong_link', 'wrong_dir', or 'missing'."""
    if is_junction(dst) or dst.is_symlink():
        try:
            if dst.resolve() == src.resolve():
                return "ok"
        except OSError:
            pass
        return "wrong_link"
    elif dst.exists():
        return "wrong_dir"
    return "missing"


def check_template(src: Path, dst: Path, env: dict[str, str]) -> str:
    """Check template state. Returns 'ok', 'wrong', or 'missing'."""
    content = src.read_text(encoding="utf-8")
    rendered = _TEMPLATE_RE.sub(lambda m: env.get(m.group(1), m.group(0)), content)
    if not dst.exists():
        return "missing"
    try:
        if dst.read_text(encoding="utf-8") == rendered:
            return "ok"
    except OSError:
        pass
    return "wrong"


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


def render_template(
    src: Path, dst: Path, env: dict[str, str], *, dry_run: bool = False
) -> None:
    """Copy src to dst, replacing ${VAR} placeholders with values from env."""
    content = src.read_text(encoding="utf-8")

    # Warn about undefined template variables
    missing_vars = {m.group(1) for m in _TEMPLATE_RE.finditer(content)} - set(env)
    for var in sorted(missing_vars):
        log("WARNING", f"${{{var}}} not defined in .env (in {src.name})")

    rendered = _TEMPLATE_RE.sub(lambda m: env.get(m.group(1), m.group(0)), content)

    if dst.exists():
        if dst.read_text(encoding="utf-8") == rendered:
            log("OK", str(dst))
            return
        if dry_run:
            log("DRY", f"Would update template {dst}")
            return
        backup_existing(dst)
    else:
        if dry_run:
            log("DRY", f"Would render template {dst} <- {src}")
            return
        dst.parent.mkdir(parents=True, exist_ok=True)

    dst.write_text(rendered, encoding="utf-8")
    log("TEMPLATE", f"{dst} <- {src}")


def link_dir(src: Path, dst: Path, *, dry_run: bool = False) -> None:
    state = check_dir_link(src, dst)
    if state == "ok":
        log("OK", str(dst))
        return
    if dry_run:
        if state == "missing":
            log("DRY", f"Would link {dst} -> {src}")
        else:
            log("DRY", f"Would replace {dst} -> {src}")
        return

    if state == "wrong_link":
        if IS_WINDOWS:
            subprocess.run(["cmd", "/c", "rmdir", str(dst)], check=True)
        else:
            dst.unlink()
    elif state == "wrong_dir":
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


def link_file(src: Path, dst: Path, *, dry_run: bool = False) -> None:
    state = check_file_link(src, dst)
    if state == "ok":
        log("OK", str(dst))
        return
    if dry_run:
        if state == "missing":
            log("DRY", f"Would link {dst} -> {src}")
        else:
            log("DRY", f"Would replace {dst} -> {src}")
        return

    if state == "wrong_symlink":
        dst.unlink()
    elif state == "wrong_file":
        backup_existing(dst)

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


def link(src: Path, dst: Path, *, dry_run: bool = False) -> None:
    if src.is_dir():
        link_dir(src, dst, dry_run=dry_run)
    else:
        link_file(src, dst, dry_run=dry_run)


# --- Module operations ---


def setup_module(
    name: str,
    target: Path,
    src_dir: Path,
    *,
    platform_subdirs: bool = False,
    template: bool = False,
    env: dict[str, str] | None = None,
    dry_run: bool = False,
) -> tuple[dict[str, dict], int]:
    """Link module files. Returns (managed: {dst_str: info}, error_count)."""
    log("MODULE", name, f"{src_dir} -> {target}")

    managed: dict[str, dict] = {}
    errors = 0

    if not src_dir.exists():
        log("SKIP", "source dir not found")
        return managed, errors

    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    platform_dir_names = {"windows", "linux"}

    def process_item(item: Path, target_dir: Path) -> None:
        nonlocal errors
        dst = target_dir / item.name
        try:
            if template and item.is_file() and env is not None:
                render_template(item, dst, env, dry_run=dry_run)
            else:
                link(item, dst, dry_run=dry_run)
            managed[str(dst)] = {"src": str(item), "module": name}
        except Exception as e:
            log("ERROR", f"{dst}: {e}")
            errors += 1

    for item in sorted(src_dir.iterdir()):
        if platform_subdirs and item.is_dir() and item.name in platform_dir_names:
            continue
        process_item(item, target)

    if platform_subdirs:
        plat_dir = src_dir / current_platform()
        if plat_dir.is_dir():
            for item in sorted(plat_dir.iterdir()):
                process_item(item, target)

    return managed, errors


def status_module(
    name: str,
    target: Path,
    src_dir: Path,
    *,
    platform_subdirs: bool = False,
    template: bool = False,
    env: dict[str, str] | None = None,
) -> tuple[int, int, int]:
    """Check link health for a module. Returns (ok, missing, wrong) counts."""
    log("MODULE", name, f"-> {target}")

    ok = missing = wrong = 0

    if not src_dir.exists():
        log("SKIP", "source dir not found")
        return ok, missing, wrong

    platform_dir_names = {"windows", "linux"}

    def check_item(item: Path, target_dir: Path) -> None:
        nonlocal ok, missing, wrong
        dst = target_dir / item.name

        if template and item.is_file() and env is not None:
            state = check_template(item, dst, env)
        elif item.is_dir():
            state = check_dir_link(item, dst)
        else:
            state = check_file_link(item, dst)

        if state == "ok":
            log("OK", str(dst))
            ok += 1
        elif state == "missing":
            log("MISSING", str(dst))
            missing += 1
        else:
            log("WRONG", str(dst))
            wrong += 1

    for item in sorted(src_dir.iterdir()):
        if platform_subdirs and item.is_dir() and item.name in platform_dir_names:
            continue
        check_item(item, target)

    if platform_subdirs:
        plat_dir = src_dir / current_platform()
        if plat_dir.is_dir():
            for item in sorted(plat_dir.iterdir()):
                check_item(item, target)

    return ok, missing, wrong


def clean_links(managed: dict[str, dict], *, dry_run: bool = False) -> int:
    """Remove managed links. Returns error count."""
    if not managed:
        log("HEADER", "\nNothing to clean.")
        return 0

    log("HEADER", f"\nCleaning {len(managed)} managed link(s)...")
    errors = 0

    for dst_str in sorted(managed):
        dst = Path(dst_str)

        if not dst.exists() and not dst.is_symlink():
            log("SKIP", f"{dst} (already gone)")
            continue

        if dry_run:
            log("DRY", f"Would remove {dst}")
            continue

        try:
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            elif is_junction(dst):
                subprocess.run(["cmd", "/c", "rmdir", str(dst)], check=True)
            elif dst.is_dir():
                log("SKIP", f"{dst} (real directory, not a managed link)")
                continue
            else:
                log("SKIP", f"{dst} (unknown type)")
                continue

            log("REMOVED", str(dst))

            # Restore backup if available
            backup = dst.with_suffix(dst.suffix + ".bak")
            if backup.exists():
                if backup.is_dir():
                    shutil.move(str(backup), str(dst))
                else:
                    backup.rename(dst)
                log("RESTORED", f"{dst} (from backup)")
        except Exception as e:
            log("ERROR", f"{dst}: {e}")
            errors += 1

    return errors


def warn_unreferenced_dirs() -> None:
    """Warn about top-level directories not registered in MODULES."""
    for item in sorted(DOTFILES_DIR.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith(".") or item.name in _IGNORED_DIRS:
            continue
        if item.name not in MODULES:
            log("WARNING", f"'{item.name}/' is not registered as a module")


# --- CLI ---


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Link dotfiles from this repo into their target locations.",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="preview changes without making them",
    )
    parser.add_argument(
        "-m",
        "--module",
        action="append",
        dest="modules",
        metavar="NAME",
        help="only process specific module(s) (repeatable)",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-s",
        "--status",
        action="store_true",
        help="check link health without making changes",
    )
    mode.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="remove managed links (restores backups if available)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log("HEADER", f"Dotfiles: {DOTFILES_DIR}")
    log("HEADER", f"Platform: {current_platform()}")
    if args.dry_run:
        log("HEADER", "Mode: dry run")

    env = load_env()

    # Validate --module names
    if args.modules:
        unknown = set(args.modules) - set(MODULES)
        if unknown:
            log("ERROR", f"Unknown module(s): {', '.join(sorted(unknown))}")
            log("HEADER", f"Available: {', '.join(sorted(MODULES))}")
            sys.exit(1)

    # --- Clean mode ---
    if args.clean:
        manifest = load_manifest()
        all_managed = manifest.get("managed", {})

        if args.modules:
            target_modules = set(args.modules)
            to_clean = {
                d: i
                for d, i in all_managed.items()
                if i.get("module") in target_modules
            }
            to_keep = {
                d: i
                for d, i in all_managed.items()
                if i.get("module") not in target_modules
            }
        else:
            to_clean = all_managed
            to_keep = {}

        errors = clean_links(to_clean, dry_run=args.dry_run)
        if not args.dry_run:
            save_manifest({"managed": to_keep})
        log("HEADER", "\nDone.")
        sys.exit(1 if errors else 0)

    # --- Status mode ---
    if args.status:
        total_ok = total_missing = total_wrong = 0

        for name, cfg in MODULES.items():
            if args.modules and name not in args.modules:
                continue
            if not should_run(cfg["platform"]):
                continue
            if cfg.get("target") is None:
                continue

            ok, missing, wrong = status_module(
                name,
                cfg["target"],
                DOTFILES_DIR / name,
                platform_subdirs=cfg.get("platform_subdirs", False),
                template=cfg.get("template", False),
                env=env,
            )
            total_ok += ok
            total_missing += missing
            total_wrong += wrong

        log("HEADER", f"\n{total_ok} ok, {total_missing} missing, {total_wrong} wrong")
        sys.exit(1 if (total_missing or total_wrong) else 0)

    # --- Link mode (default) ---
    all_managed: dict[str, dict] = {}
    total_errors = 0

    for name, cfg in MODULES.items():
        if args.modules and name not in args.modules:
            continue
        if not should_run(cfg["platform"]):
            if not args.modules:
                log("MODULE", name, f"SKIP (platform: {cfg['platform']})")
            continue
        if cfg.get("target") is None:
            continue

        managed, errors = setup_module(
            name,
            cfg["target"],
            DOTFILES_DIR / name,
            platform_subdirs=cfg.get("platform_subdirs", False),
            template=cfg.get("template", False),
            env=env,
            dry_run=args.dry_run,
        )
        all_managed.update(managed)
        total_errors += errors

    warn_unreferenced_dirs()

    if not args.dry_run:
        # Merge manifest: replace entries for processed modules, keep the rest
        processed = set()
        for name, cfg in MODULES.items():
            if args.modules and name not in args.modules:
                continue
            if not should_run(cfg["platform"]):
                continue
            if cfg.get("target") is None:
                continue
            processed.add(name)

        manifest = load_manifest()
        manifest["managed"] = {
            dst: info
            for dst, info in manifest["managed"].items()
            if info.get("module") not in processed
        }
        manifest["managed"].update(all_managed)
        save_manifest(manifest)

    log("HEADER", "\nDone.")
    if total_errors:
        log("HEADER", f"{total_errors} error(s) occurred.")
        sys.exit(1)


if __name__ == "__main__":
    main()
