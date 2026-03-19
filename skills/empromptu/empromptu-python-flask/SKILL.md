---
name: empromptu-python-flask
description: Python workflow for Flask codebases. Use in Empromptu-style API or web
  repos when implementing or debugging Flask services, and begin by reading and internalizing
  the applicable AGENTS.md files before changing code.
---

# Empromptu Python Flask

## Startup

1. Read every applicable `AGENTS.md` first and treat those instructions as mandatory.
2. Inspect the service's workflow entry points before editing:
   - dependency files such as `pyproject.toml` or `requirements*.txt`
   - Flask app factory or startup modules
   - test, lint, and local run commands
3. Follow the repo's established patterns for blueprints, configuration loading, extensions, and data access.

## Working Style

- Preserve request handling and configuration semantics unless the task requires deliberate behavior changes.
- Prefer small, explicit changes that match the repo's existing architecture.
- Keep shell commands and validation aligned with the repo's own scripts or `Justfile`.
- Call out hidden assumptions around env vars, service wiring, or application factory behavior.

## Validation

- Run the narrowest meaningful checks available for the touched code.
- If the repo depends on external services, note what could not be exercised locally.
