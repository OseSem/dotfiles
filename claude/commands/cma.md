---
name: commit-and-push
description: Stage all changes, write a conventional commit message, and push to the current branch. User-invocable only — run via /cma when the user explicitly asks for it.
disable-model-invocation: true
---

# Commit and Push

Stage all changes, generate a meaningful conventional commit message, and push to the remote.

## Steps

1. **Check status** — run `git status` to see what's changed
2. **Stage all** — run `git add -A`
3. **Generate commit message** — based on the diff, write a conventional commit message:
   - Format: `type(scope): short description`
   - Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `style`, `test`, `ci`
   - Keep the subject line under 72 characters
   - Add a body if the changes are non-trivial
4. **Commit** — run `git commit -m "<message>"`
5. **Push** — run `git push`

## Generating the commit message

Run `git diff --staged` after staging to understand what changed. Summarize what changed and why if inferable.

If the user already provided a message or description, use that instead.

## Edge cases

- **Nothing to commit** — inform the user, stop
- **Push rejected** — report the error and suggest `git pull --rebase`, but do NOT run it automatically
- **Detached HEAD** — warn before pushing
- **Force push needed** — stop and ask the user, never force push automatically