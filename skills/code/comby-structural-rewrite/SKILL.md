---
name: comby-structural-rewrite
description: Use for code-shaped rewrites when regex is brittle and AST tooling is
  unavailable/impractical for the target language or format. Prefer `ast-grep-refactor`
  when AST support exists; use `sd-find-replace` for pure text substitutions.
metadata:
  short-description: Code-shaped rewrite playbook using comby
---

# Comby Structural Rewrite

Use `comby` for structured pattern rewrites when full parser tooling is not practical.

## Quick start

Start narrow and preview first, then rewrite in small batches.

## Trigger cues

Use this skill when:
- regex would be brittle
- AST tool support is missing for the target format
- you need syntax-like matching across config/code text

Prefer `ast-grep` when a high-quality AST path exists for the language.

## Routing boundary

- Use `comby-structural-rewrite` for structure-like patterns without viable AST support.
- Use `ast-grep-refactor` first for AST-capable languages.
- Use `sd-find-replace` for simple lexical replacements.

## Workflow

1. Define match template with clear placeholders.
2. Run match-only pass on narrow scope.
3. Apply rewrite on small subset.
4. Review semantics and run checks.
5. Roll out incrementally.

## Guardrails

- Keep one transformation per rewrite pass.
- Avoid wide repo rewrites without validation checkpoints.

## Read references only when needed

- Template strategy, placeholders, and sequencing: `references/rewrite-playbook.md`
- Pitfalls and rollback heuristics: `references/rewrite-playbook.md#pitfalls`
