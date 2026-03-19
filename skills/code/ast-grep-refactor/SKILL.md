---
name: ast-grep-refactor
description: Use for syntax-aware refactors in AST-supported languages (call shape,
  argument, chained/member rewrites). Prefer this over `comby` when AST support exists,
  and over `sd` when structure matters.
metadata:
  short-description: AST-aware refactor workflow with validation gates
---

# ast-grep Refactor

Use `ast-grep` for structure-aware search and rewrites when regex is risky.

## Quick start

```bash
sg -p 'console.log($$$ARGS)' -l js
sg -p '$PROP && $PROP()' --rewrite '$PROP?.()' -l ts
```

## Trigger cues

Use this skill when refactoring:
- call signatures or argument ordering
- chained access and null-guard patterns
- repeated code forms where syntax context matters

Prefer a plain text tool (`sd`) only when the pattern is truly lexical and structure-independent.

## Routing boundary

- Use `ast-grep-refactor` when AST support exists and semantic structure matters.
- Use `comby-structural-rewrite` only if AST support is unavailable/impractical.
- Use `sd-find-replace` for plain literal text substitution.

## Workflow

1. Scope narrowly: target directory and language first.
2. Search-only pass: confirm matches are exactly intended.
3. Rewrite pass on small scope.
4. Diff + compile/tests.
5. Expand scope incrementally.

## Quality gates

- Never start with repo-wide rewrite on first pass.
- Keep rewrites one conceptual transformation at a time.
- Require post-rewrite checks before broadening blast radius.

## Read references only when needed

- Pattern design, capture strategies, and rollout sequencing: `references/refactor-playbook.md`
- Common pitfalls (over-match, under-match, language mismatch): `references/refactor-playbook.md#pitfalls`
