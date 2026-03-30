# Merge Dependabot PRs

Autonomously merge all open Dependabot pull requests in the current repository that have passing CI checks. Do NOT ask for confirmation — just merge them.

## Steps

1. **List open Dependabot PRs** — run:
   ```
   gh pr list --author "app/dependabot" --state open --json number,title,statusCheckRollup,mergeable,url
   ```

2. **Immediately squash-merge every PR** where CI checks all pass and there are no merge conflicts:
   ```
   gh pr merge <number> --squash
   ```

3. **Skip** any PR with failing CI, pending checks, or merge conflicts — do not ask the user what to do with these.

4. **Print a short summary** when done: which PRs were merged, which were skipped and why.

## Rules

- Do NOT ask for confirmation before merging — just do it
- Never force-merge PRs with failing or pending checks
- Always use `--squash`
- If there are no open Dependabot PRs, say so and stop
