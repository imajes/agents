---
name: empromptu-shell-just
description: Shell, systems, Justfile, release, and devops workflow guidance for repos
  that use Just as a primary command surface. Use when working on shell scripts, automation,
  release tasks, or Just recipes in Empromptu-style repos.
---

# Empromptu Shell Just

## Startup

1. Read every applicable `AGENTS.md`.
2. Read the root `Justfile` before composing commands or changing automation.
3. Run `just --list` or the repo's help target if available so you understand the intended entry points.

## Working Style

- Treat `just` recipes as the primary interface to local workflows when the repo provides them.
- Prefer updating the canonical recipe or helper script instead of documenting ad hoc command sequences that drift from the repo.
- When a recipe wraps a shell script, inspect both sides before changing behavior.
- Keep failure modes visible and avoid commands that hide errors or silently skip work.

## Validation

- Re-run the relevant `just` target after changes when it is safe to do so.
- Lint non-trivial shell edits and preserve readable, repeatable command composition.
- Call out any recipe dependencies on missing tools, credentials, or external systems.
