---
name: sd-find-replace
description: Use for literal text substitutions where syntax/AST context is unnecessary
  and `sed` escaping is brittle. Do not use for syntax-aware rewrites; use `ast-grep-refactor`
  or `comby-structural-rewrite` instead.
metadata:
  short-description: Text substitution workflow with safe rollout gates
---

# sd Find Replace

Use `sd` for clear, low-ceremony string replacement when structural tooling is unnecessary.

## Quick start

```bash
sd 'before' 'after' file.txt
```

## Trigger cues

Use this skill when:
- replacement is pure text and structure-independent
- sed escaping is becoming difficult to reason about
- quick, reviewable substitutions are needed

Prefer `ast-grep` or `comby` when syntax or structure context matters.

## Routing boundary

- Use `sd-find-replace` for lexical substitutions only.
- Escalate to `ast-grep-refactor`/`comby-structural-rewrite` when meaning depends on syntax.

## Workflow

1. Select smallest file scope first.
2. Preview candidate files before replacement.
3. Apply replacement in one conceptual batch.
4. Review diff and run relevant checks.
5. Expand scope only when initial batch is clean.

## Guardrails

- Keep replacements explicit and literal where possible.
- Avoid broad wildcard runs without a reviewed dry run.

## Read references only when needed

- Multi-file rollout patterns and verification flow: `references/safe-rollout.md`
- Edge cases (regex-like tokens, escaping strategy): `references/safe-rollout.md#edge-cases`
