---
name: shellcheck-lint-commands
description: Use when authoring or modifying non-trivial shell scripts/snippets and
  CI shell blocks; lint with `shellcheck` before execution. Pair with `shell-guard-commands`
  for runtime-safe command composition.
metadata:
  short-description: Shell lint workflow with severity-based triage
---

# ShellCheck Commands

Lint non-trivial shell scripts/snippets before execution.

## Quick start

```bash
shellcheck -s bash script.sh
shellcheck -s sh ./ci/script.sh
```

## Trigger cues

Use this skill when:
- editing shell scripts or CI shell blocks
- composing multi-step shell snippets
- quoting, expansions, loops, or traps are involved

## Routing boundary

- Use `shellcheck-lint-commands` for lint/diagnostics of shell code.
- Use `shell-guard-commands` for cross-cutting runtime command safety rules.

## Workflow

1. Pick target shell (`bash`, `sh`, `zsh` compatibility expectations).
2. Run shellcheck on the script/snippet.
3. Fix correctness and safety findings first.
4. Re-run shellcheck and then execute.

## Triage priorities

1. Exit code masking and unsafe error handling.
2. Word splitting and quoting bugs.
3. Subshell/pipe behaviors that alter state unexpectedly.
4. Style/readability warnings after correctness is resolved.

## Read references only when needed

- Warning prioritization and remediation examples: `references/warning-priorities.md`
- CI-oriented shell hardening patterns: `references/warning-priorities.md#ci-patterns`
