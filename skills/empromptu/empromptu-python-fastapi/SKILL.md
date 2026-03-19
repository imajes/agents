---
name: empromptu-python-fastapi
description: Python workflow for FastAPI codebases. Use in Empromptu-style API repos
  when implementing or debugging FastAPI services, and begin by reading and internalizing
  the applicable AGENTS.md files before changing code.
---

# Empromptu Python FastAPI

## Startup

1. Read every applicable `AGENTS.md` first and keep those rules front of mind for the rest of the task.
2. Inspect the service entry points and workflow files before editing:
   - dependency files such as `pyproject.toml` or `requirements*.txt`
   - FastAPI app startup modules
   - test commands, lint commands, and local tooling
3. Follow the repo's current structure for routers, dependency injection, settings, schemas, and background tasks.

## Working Style

- Preserve request and response contracts unless the user explicitly asks for an API change.
- Prefer typed models and clear validation boundaries over loose dictionaries.
- Keep changes idiomatic for FastAPI and the repository's existing conventions.
- Use the repo's scripts, `Justfile`, or test runners instead of improvising new workflows.

## Validation

- Run the narrowest meaningful checks available for the affected paths.
- Call out skipped validation, missing services, or unclear runtime dependencies explicitly.
