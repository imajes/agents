---
name: empromptu-typescript
description: TypeScript and JavaScript workflow for React plus Remix codebases. Use
  in Empromptu-style frontend repos when implementing features, fixing bugs, or reviewing
  code in a React plus Remix application, and begin by reading the applicable AGENTS.md
  files.
---

# Empromptu TypeScript

## Startup

1. Read every applicable `AGENTS.md` before making changes and treat those rules as binding.
2. Inspect the local workflow entry points before editing:
   - `package.json`
   - `tsconfig*.json`
   - Remix or Vite config
   - existing test, lint, and build commands
3. Follow the repo's current routing, loader or action, styling, and component patterns instead of introducing a parallel architecture.

## Working Style

- Prefer explicit types over `any` and avoid weakening type boundaries to "make it work."
- Keep Remix data flow aligned with existing loader, action, and component boundaries.
- Preserve route contracts, form behavior, and server-client data shapes.
- Use the repo's existing scripts or `Justfile` targets for validation rather than ad hoc command sequences.

## Validation

- Run the narrowest relevant test, lint, or build commands defined by the repo.
- If validation cannot run, say exactly what is missing.
- Surface any AGENTS, framework, or routing assumptions explicitly.
