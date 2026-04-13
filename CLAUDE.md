# Dotfiles

> **Keep this file up to date.** After any significant change — new modules, renamed files, added
> configs, setup script changes, architectural decisions — update the relevant sections below.
> Stale instructions lead to wasted effort and broken assumptions. When in doubt, re-read the
> repo and correct anything that has drifted.

Cross-platform dotfiles repo. Configs are stored here and linked into their target locations via `setup.py`.

## Repo layout

- `setup.py` — the linker script. All module definitions live in the `MODULES` dict at the top.
- Each top-level directory is a module (e.g. `claude/`, `git/`). Its contents get linked into a target directory on the system.
- `.gitignore` — keeps ephemeral/sensitive files out of version control. When adding a new module, update this file with anything that shouldn't be tracked.

## Current modules

| Module | Target | Platform |
|--------|--------|----------|
| `claude/` | `~/.claude` | all |
| `git/` | `~` | all |
| `powershell/` | `Documents/WindowsPowerShell` | windows |
| `pwsh/` | `Documents/PowerShell` | windows |
| `windows-terminal/` | `AppData/.../WindowsTerminal/LocalState` | windows |
| `nvim/` | `AppData/Local/nvim` (win) / `~/.config/nvim` (linux) | all |
| `sharex/` | `Documents/ShareX` | windows |
| `oh-my-posh/` | `AppData/.../Programs/oh-my-posh` (win) / `~/.config/oh-my-posh` (linux) | all |
| `fastfetch/` | `~/.config/fastfetch` | all |
| `glazewm/` | `~/.glzr/glazewm` | windows |
| `glazewm-extra/` | `~/.config` | windows |
| `yasb/` | `~/.config/yasb` | windows |

## setup.py behavior

- **Linux**: `os.symlink()` for everything.
- **Windows**: `os.link()` (hard links) for files, `mklink /J` (junctions) for directories. No admin required.
- Idempotent — prints `OK` for existing correct links, only acts on changes.
- Backs up existing files/dirs as `.bak` before replacing.
- Modules with `platform_subdirs: True` link root-level files on all platforms, plus files from the matching `windows/` or `linux/` subdirectory (e.g. `fastfetch/`).
- Tracks all managed links in `.setup-manifest.json` (git-ignored, machine-specific).
- Warns about top-level directories not registered as modules.
- Template modules (e.g. `yasb`) replace `${VAR}` placeholders with values from `.env`. See `.env.example` for available variables. Warns on undefined variables.
- Exits with non-zero status if any errors occur.

### CLI flags

| Flag | Description |
|------|-------------|
| `--dry-run` / `-n` | Preview changes without making them |
| `--module NAME` / `-m NAME` | Only process specific module(s) (repeatable) |
| `--status` / `-s` | Check link health without making changes |
| `--clean` / `-c` | Remove managed links (restores backups if available) |

Examples:
```
python setup.py                        # link all modules
python setup.py --dry-run              # preview what would change
python setup.py --status               # health check
python setup.py -m nvim -m git         # only re-link nvim and git
python setup.py --clean                # remove all managed links
python setup.py --clean -m nvim        # remove only nvim links
```

## Adding a module

1. Create the directory in the repo root.
2. Add config files to it.
3. Add an entry to `MODULES` in `setup.py` with `target` and `platform`.
4. Add ignore rules to `.gitignore` if the target directory contains files that shouldn't be tracked.
5. Update this file's "Current modules" table.

## Conventions

- **Never commit sensitive files.** If unsure whether a file contains credentials, tokens, or secrets, ask before staging it. Always list any potentially sensitive files at the end of a commit summary so nothing slips through unnoticed.
- Module directories mirror the structure of their target — files go where they'd be inside the target dir.
- Platform values: `"all"`, `"linux"`, `"windows"`.
- **Never push to remote without explicit permission.** Commit freely, but always ask before running `git push` unless the user specifically requested it.
- **Always run `python setup.py` when you're done making changes.** This ensures links are up to date after any file or module changes.
- **Edit configs in this repo, not at their target locations.** When the user says "add to my config", "update my config", "change my settings", etc., always make the change in the corresponding module directory in this repo — never edit the file at its installed/linked location. The links created by `setup.py` ensure the changes propagate automatically.
