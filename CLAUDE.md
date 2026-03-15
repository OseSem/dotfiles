# Dotfiles

> **Keep this file up to date.** After any significant change — new modules, renamed files, added
> configs, setup script changes, architectural decisions — update the relevant sections below.
> Stale instructions lead to wasted effort and broken assumptions. When in doubt, re-read the
> repo and correct anything that has drifted.

Cross-platform dotfiles repo. Configs are stored here and linked into their target locations via `setup.py`.

## Repo layout

- `setup.py` — the linker script. All module definitions live in the `MODULES` dict at the top.
- Each top-level directory is a module (e.g. `claude/`, `hyprland/`). Its contents get linked into a target directory on the system.
- `.gitignore` — keeps ephemeral/sensitive files out of version control. When adding a new module, update this file with anything that shouldn't be tracked.

## Current modules

| Module | Target | Platform |
|--------|--------|----------|
| `claude/` | `~/.claude` | all |
| `powershell/` | `Documents/WindowsPowerShell` | windows |
| `pwsh/` | `Documents/PowerShell` | windows |

## setup.py behavior

- **Linux**: `os.symlink()` for everything.
- **Windows**: `os.link()` (hard links) for files, `mklink /J` (junctions) for directories. No admin required.
- Idempotent — prints `OK` for existing correct links, only acts on changes.
- Backs up existing files/dirs as `.bak` before replacing.

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
