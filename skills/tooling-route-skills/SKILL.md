---
name: tooling-route-skills
description: Use when selecting among local tooling skills is ambiguous or when a
  non-trivial coding task begins. Route to the most specific skill(s) using the decision
  matrix; explicitly resolve overlaps (ast-grep vs comby vs sd, shellcheck vs shell-hygiene,
  rm-safety vs general shell safety, yq vs text tools), and default to safer tool
  usage when destructive operations are in scope.
metadata:
  short-description: Decision matrix for routing tooling skills
---

# Tooling Skill Router

Route tasks to the most specific curated tooling skill(s) with consistent precedence rules.

## Quick start

1. Identify the primary operation: `rewrite`, `review`, `yaml edit`, `benchmark`, `watch loop`, `state handoff`, `shell safety`, `destructive deletion`, `repo survey`, `worktree orchestration`.
2. Pick one primary skill from the matrix.
3. Add secondary cross-cutting skills when needed.

## Decision matrix

- Structural code refactor in AST-supported language: use `$ast-grep-refactor`.
- Structural/code-shaped rewrite without viable AST support: use `$comby-structural-rewrite`.
- Plain text substitution: use `$sd-find-replace`.
- YAML query/edit: use `$yq-yaml-edit`.
- Noisy diff/semantic review: use `$difftastic-review`.
- Shell script/snippet linting: use `$shellcheck-lint-commands`.
- Shell chain safety/command hygiene: use `$shell-guard-commands`.
- Destructive deletion with `rm`, `find ... -delete`, recursive cleanup, or wildcard removal: use `$rm-guard-deletions`.
- Repository composition survey/planning: use `$scc-codebase-survey`.
- Performance measurement claims: use `$hyperfine-benchmark`.
- Continuous rerun loops on file changes: use `$watchexec-rerun-on-changes`.
- Ephemeral shared coordination state: use `$valkey-manage-ephemeral-state`.
- Multi-agent or parallel branch setup with Git worktrees: use `$git-manage-worktrees`.
- Commit creation (`commit this`, `make a commit`): use `$git-commit-conventionally`.

## Precedence rules for overlaps

1. Rewrite family precedence:
   - `ast-grep-refactor` > `comby-structural-rewrite` > `sd-find-replace`
   - Rationale: AST semantics first, then structural templates, then lexical replacement.
2. Shell family pairing:
   - Use `shellcheck-lint-commands` for linting script/snippet code.
   - Use `shell-guard-commands` for runtime chain safety.
   - Use `rm-guard-deletions` whenever the shell task deletes files or directories.
   - In shell-heavy cleanup work, often apply both `shell-guard-commands` and `rm-guard-deletions`.
3. Config edit rule:
   - YAML files default to `yq-yaml-edit`, not text substitution.
4. Destructive command rule:
   - If a command may remove files or directories, route through `rm-guard-deletions` by default before composing the delete step.
   - If a delete command uses `-f` or `--force`, treat escalation as mandatory.
5. Worktree orchestration rule:
   - For parallel implementation using git worktrees, run `git-manage-worktrees` first.
6. Commit rule:
   - Any explicit commit request defaults to `git-commit-conventionally`.

## Composition patterns

- Refactor + safety: `$ast-grep-refactor` + `$difftastic-review`.
- Shell script change: `$shellcheck-lint-commands` + `$shell-guard-commands`.
- Shell cleanup or artifact deletion: `$rm-guard-deletions` + `$shell-guard-commands`.
- Performance optimization task: `$hyperfine-benchmark` + domain-specific edit skill.
- Large unfamiliar repo task: `$scc-codebase-survey` first, then route to task-specific skill.
- Multi-agent coding with isolated branches: `$git-manage-worktrees` first, then task-specific edit/review skills.
- Finalizing work for version control: `$git-commit-conventionally` (after implementation/testing skills).

## Routing boundary

- This skill chooses skills; it does not replace them.
- After routing, load and execute the selected skill workflow.

## Read references only when needed

- Ambiguous cases and tie-break examples: `references/routing-cases.md`
- Anti-patterns and misrouting recovery: `references/routing-cases.md#misrouting-recovery`
