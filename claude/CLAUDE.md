# Global Claude Code Instructions

## Package Managers
- **Python**: Always use `uv`. Never use `pip`, `poetry`, or `virtualenv`.
  - New project: `uv init <name>`
  - Add dependencies: `uv add <package>`
  - Dev dependencies: `uv add --dev <package>`
  - Run scripts: `uv run <script>`
  - Sync environment: `uv sync`
  - Never create or edit `requirements.txt` manually
- **JavaScript/TypeScript**: Always use `pnpm`. Never use `npm` or `yarn`.
  - Install: `pnpm install`
  - Add: `pnpm add <package>`
  - Run: `pnpm run <script>`

## New Python Projects
- Always initialize new Python projects with `uv init <name>`
- Never manually create `pyproject.toml`, `setup.py`, or `requirements.txt` from scratch
- After `uv init`, use `uv add` to add dependencies — never write them manually into `pyproject.toml`
- After `uv init .`, always run `uv add --dev ruff` and add a suitable ruff config to `pyproject.toml` based on the project type and Python version being used
- For scripts/tools (no package needed): `uv init --script` or just `uv run` with inline dependencies

## Code Formatting
- **Python**: After writing or editing `.py` files, always run `ruff format <file>` and `ruff check --fix <file>`.
- For other languages, follow the project's existing formatter if configured.

## Git & Commits
- When creating GitHub repos (`gh repo create`), always make them private (`--private`) unless explicitly told otherwise.
- Always use conventional commits: `type(scope): description`
- Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `style`, `test`, `ci`, `perf`
- Keep subject line under 72 characters
- Add a body when the change is non-trivial
- Never force push without explicit user confirmation
- Never add Co-Authored-By lines to commits
- Don't add self-attribution (e.g. "Generated with Claude Code", "Built by Claude") to commits, PRs, issues, or any other platform content

## Environment
  - Running on Windows with Git Bash (`C:\Program Files\Git\bin\bash.exe`)
  - Use Windows-compatible paths and commands
  - Prefer Python scripts over shell scripts for cross-platform hooks

## General Preferences
- Prefer explicit over implicit — don't hide important steps
- When unsure between two approaches, briefly state the tradeoff and ask
- Don't add unnecessary comments to code that is already self-explanatory
- Prefer returning early over deeply nested conditionals
- When creating a `CLAUDE.md` or `AGENTS.md`, include a blockquote near the top like:
  > **Keep this file up to date.** After any significant change — ... — update the relevant sections
  > below. Stale instructions lead to wasted effort and broken assumptions. When in doubt, re-read
  > the codebase and correct anything that has drifted.
  Fill in the examples (after the dash) with things relevant to the specific project (e.g. new API routes, renamed files, schema migrations, added modules)