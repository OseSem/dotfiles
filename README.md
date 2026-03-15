# dotfiles

Cross-platform dotfiles managed with symlinks. Works on both Windows and Linux.

## Structure

```
dotfiles/
  setup.py              # links configs into their target locations
  claude/               # ~/.claude — Claude Code config
    CLAUDE.md           #   global instructions
    settings.json       #   permissions, hooks, plugins
    commands/           #   custom slash commands
    hooks/              #   post-tool-use hooks
```

## Setup

```bash
git clone <repo-url> ~/dotfiles
cd ~/dotfiles
python setup.py
```

Re-run `python setup.py` anytime to sync — it's idempotent. Existing configs get backed up as `.bak` before being replaced.

## How it works

Each top-level folder is a **module** that maps to a target directory on the system. The `MODULES` dict in `setup.py` defines these mappings:

```python
MODULES = {
    "claude": {
        "target": Path.home() / ".claude",
        "platform": "all",
    },
    "hyprland": {
        "target": Path.home() / ".config" / "hypr",
        "platform": "linux",
    },
}
```

Every file and directory inside the module folder gets linked into the target:

| Platform | Files | Directories |
|----------|-------|-------------|
| Linux | symlinks | symlinks |
| Windows | hard links | junctions |

Modules with a `platform` filter are skipped on other platforms.

## Adding a new module

1. Create a folder in the repo (e.g. `kitty/`)
2. Add your config files to it
3. Add an entry to `MODULES` in `setup.py`:
   ```python
   "kitty": {
       "target": Path.home() / ".config" / "kitty",
       "platform": "linux",
   },
   ```
4. Run `python setup.py`

## Syncing across devices

```bash
# Machine A — edit configs as usual, they live in the repo
git add -A && git commit -m "update configs" && git push

# Machine B
git pull
python setup.py
```

## Windows notes

- No admin or Developer Mode required — uses hard links and junctions instead of symlinks
- Requires Python 3.6+
- Tested with Git Bash
