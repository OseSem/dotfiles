# Global Pi Instructions

> **Keep this file up to date.** After any significant change — new tools, package-manager
> preferences, workflow changes, or environment changes — update the relevant sections below.
> Stale instructions lead to wasted effort and broken assumptions. When in doubt, re-read the file
> and correct anything that has drifted.

## Package Managers

- Follow the package manager declared by the project's instructions, configuration, and lockfiles.
  Do not migrate an existing project to a different package manager unless explicitly requested.
- **New Python projects:** Use `uv`. Do not use `pip`, `poetry`, or `virtualenv`.
  - Initialize: `uv init <name>`
  - Add dependencies: `uv add <package>`
  - Add development dependencies: `uv add --dev <package>`
  - Run commands or scripts: `uv run <command>`
  - Sync the environment: `uv sync`
- **New JavaScript/TypeScript projects:** Use `pnpm`. Do not use `npm` or `yarn` unless the
  project already requires one of them.
  - Install dependencies: `pnpm install`
  - Add a dependency: `pnpm add <package>`
  - Run a script: `pnpm run <script>`

## Search and File Operations

- Use Pi's `read` tool to inspect known files instead of shelling out to `cat` or `sed`.
- Prefer Pi's dedicated `grep`, `find`, and `ls` tools when they are available.
- When searching through the shell, use `rg` (ripgrep) rather than `grep`. `rg` is always installed.
- Use Pi's `edit` tool for precise changes to existing files and `write` for new files or complete
  rewrites.

## New Python Projects

- Initialize new projects with `uv init <name>` or `uv init .`.
- For new projects, do not manually create `pyproject.toml`, `setup.py`, or `requirements.txt`.
- Add dependencies with `uv add`; do not write them directly into a new `pyproject.toml`.
- After `uv init`, run `uv add --dev ruff` and add suitable Ruff configuration to `pyproject.toml`
  based on the project type and Python version.
- For standalone scripts or tools that do not need a package, use `uv init --script` or `uv run`
  with inline dependencies.

## Code Formatting

- After writing or editing Python files, run `uv run ruff format <file>` and
  `uv run ruff check --fix <file>`.
- For other languages, use the project's existing formatter when one is configured.

## Git and Commits

- When creating a GitHub repository with `gh repo create`, make it private with `--private` unless
  explicitly told otherwise.
- Use conventional commits: `type(scope): description`.
- Allowed types: `feat`, `fix`, `chore`, `refactor`, `docs`, `style`, `test`, `ci`, and `perf`.
- Keep the subject line under 72 characters. Add a body when the change is non-trivial.
- Never force-push without explicit confirmation.
- Never add `Co-Authored-By` lines or AI self-attribution to commits, pull requests, issues, or other
  platform content.
- Never create or modify Git configuration that sets or overrides identity or signing fields,
  including `user.name`, `user.email`, `user.signingkey`, or `commit.gpgsign`. Use the user's
  existing global or system configuration.

## Running Commands and Applications

- Run ordinary commands directly with Pi's `bash` tool.
- Use `tmux` for long-running or interactive processes that require continued observation or
  interaction, such as development servers, watch processes, and terminal applications.
- When using `tmux`, use a named session and inspect its output with `tmux capture-pane` as needed.

## Environment

- The environment is macOS with zsh.
- Use Unix-style paths and macOS-compatible commands.
- Write interactive shell commands that work in zsh. If a script requires Bash-specific syntax,
  give it an explicit Bash shebang.
- Prefer portable shell code when a script must work across platforms.

## General Preferences

- Prefer explicit behavior over implicit behavior; do not hide important steps.
- When unsure between approaches, briefly explain the tradeoff and ask before choosing.
- Do not add comments to code that is already self-explanatory.
- Prefer early returns over deeply nested conditionals.
- When creating a `CLAUDE.md` or `AGENTS.md`, include a blockquote near the top like:
  > **Keep this file up to date.** After any significant change — ... — update the relevant
  > sections below. Stale instructions lead to wasted effort and broken assumptions. When in doubt,
  > re-read the codebase and correct anything that has drifted.

  Replace the ellipsis with examples relevant to the project, such as new API routes, renamed files,
  schema migrations, or added modules.
