---
name: git-manage-worktrees
description: Standardize Git worktree operations for parallel coding tasks. Use when
  creating, managing, or cleaning up worktrees, especially in multi-agent workflows.
  Enforce repo-local `.worktrees/` usage (not `/tmp`), ensure `.worktrees/` is listed
  in repository `.gitignore` when that directory exists, and run all Git commands
  as `git -C REPO_PATH ...`.
---

# Git Worktree Guardrails

## Overview
Use this skill to run parallel work safely with Git worktrees while keeping traceability and avoiding sandbox/path issues.

## Required Rules
1. Create worktrees under `<repo>/.worktrees/` only.
2. Do not create worktrees in `/tmp` or `/private/tmp`.
3. Use `git -C <repo>` command style for all Git operations.
4. When `<repo>/.worktrees/` exists, ensure `.gitignore` contains `.worktrees/`.
5. Keep one work effort per worktree branch.

## Quick Start
```bash
# 1) Ensure local worktree root
mkdir -p <repo>/.worktrees

# 2) Ensure ignore rule exists once the folder exists
if [ -d <repo>/.worktrees ] && ! rg -n '^\\.worktrees/$' <repo>/.gitignore >/dev/null; then
  printf '\n.worktrees/\n' >> <repo>/.gitignore
fi

# 3) Create worktree from base branch
git -C <repo> worktree add -b <branch-name> <repo>/.worktrees/<worktree-name> <base-branch>

# 4) List active worktrees
git -C <repo> worktree list
```

## Workflow
1. Determine repo root and base branch (`main` unless specified).
2. Create `<repo>/.worktrees/` if missing.
3. Add `.worktrees/` to `.gitignore` if missing and folder exists.
4. Create one branch and one worktree per independent effort.
5. Execute edits/tests inside each worktree path.
6. Integrate changes back into the main worktree in clear, grouped steps.
7. Remove temporary worktrees when integration is complete.

## Naming Conventions
- Branch: `<topic>-<scope>` (short and explicit).
- Worktree folder: same as branch or task id.
- Example:
  - Branch: `fix-nav-a11y`
  - Worktree: `<repo>/.worktrees/fix-nav-a11y`

## Cleanup
```bash
# Remove a finished worktree
git -C <repo> worktree remove <repo>/.worktrees/<worktree-name>

# Optional: prune stale metadata
git -C <repo> worktree prune
```

## Guardrails
- Do not delete a worktree until required changes are integrated.
- Do not run destructive Git commands by default.
- If branch/worktree creation fails, diagnose ref/path conflicts before retrying.
- If `.gitignore` is missing, create it before appending `.worktrees/`.
