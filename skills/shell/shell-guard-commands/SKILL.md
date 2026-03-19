---
name: shell-guard-commands
description: 'Use as a cross-cutting safety layer whenever composing non-trivial shell
  command chains: preserve failures, keep stderr/exit-code visibility, and use clean
  stdin/redirection patterns.'
metadata:
  short-description: Mandatory shell safety and failure-handling guardrails
---

# Shell Hygiene Guardrails

Apply strict shell hygiene to every non-trivial command sequence.

## Mandatory rules

1. Never hide failures with `2>/dev/null || true`.
2. Preserve stderr and exit codes.
3. If tolerating failure intentionally, say so explicitly and log it.
4. Avoid useless `cat` pipelines.
5. Prefer direct redirection or stdin dash handling.

## Quick examples

```bash
if ! some_command; then
  echo "some_command failed; continuing intentionally" >&2
fi

command < file.txt
command ... - < file.txt
```

## Trigger cues

Use this skill whenever composing shell blocks that:
- chain multiple commands
- handle errors/branching
- process file/stdin streams

## Routing boundary

- Apply `shell-guard-commands` alongside any shell-heavy task.
- Combine with `shellcheck-lint-commands` when editing reusable shell scripts/snippets.

## Read references only when needed

- Rule rationale and anti-pattern examples: `references/rules-and-examples.md`
- CI-focused hardened command patterns: `references/rules-and-examples.md#ci-hardened-patterns`
