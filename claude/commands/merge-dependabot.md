---
name: merge-dependabot
description: Find and merge all open Dependabot PRs in the current repo. Auto-approves, squash-merges, and skips PRs with failing CI. Use this command when the user says "merge dependabot", "merge dependabot PRs", "dependabot merge", "merge all dependency updates", "merge bot PRs", or any variation of wanting to batch-merge Dependabot pull requests.
---

# Merge Dependabot PRs

Automatically approve and squash-merge all open Dependabot PRs in the current repository. PRs with failing checks are flagged for investigation but do not block the rest.

## Steps

### 1. List all open Dependabot PRs

```bash
gh pr list --author "dependabot[bot]" --state open --json number,title,headRefName,statusCheckRollup
```

If no PRs are found, inform the user and stop.

### 2. Check CI status for each PR

For each PR, inspect the `statusCheckRollup` field to determine check status:
- **All checks passed** → eligible for merge
- **Checks still pending** → wait and re-check once (up to 30 seconds), then treat as failing if still pending
- **Any check failed** → add to the "failed" list, skip this PR

### 3. Report the plan

Before merging anything, show the user:
- How many PRs will be merged (with titles)
- How many PRs have failing/pending checks (with titles and which checks failed)

Then proceed without waiting for confirmation.

### 4. Approve and squash-merge eligible PRs

For each eligible PR, run:

```bash
gh pr review <number> --approve
gh pr merge <number> --squash
```

Do NOT use `--auto` — auto-merge is not enabled on any repo.

Process PRs one at a time. If a merge fails (e.g., merge conflict), report it and continue with the next PR.

### 5. Handle failing PRs

For PRs that had failing checks:
- List each one with the PR number, title, and which specific checks failed
- Tell the user: "These PRs have failing checks — you may want to investigate them. I've skipped them for now."
- Do NOT attempt to merge them

### 6. Pull main

After all merges are done, update the local branch:

```bash
git pull
```

### 7. Summary

At the end, print a summary:
- Successfully merged: list of PR titles
- Skipped (failing checks): list of PR titles with failure reasons
- Failed to merge (conflicts/errors): list of PR titles with error details

## Edge cases

- **No `gh` CLI available** — inform the user they need the GitHub CLI installed and authenticated
- **Not in a git repo** — inform the user and stop
- **Auth issues** — if `gh` returns auth errors, suggest `gh auth login`
- **Merge conflicts** — skip the PR, report it in the summary, continue with others
- **Rate limiting** — if GitHub rate limits are hit, wait briefly and retry once
