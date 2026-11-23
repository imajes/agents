---
name: empromptu-devenv
description: Repo-grounded migration planning for the Empromptu dev environment. Use
  when analyzing the `Empromptu-ai/dev-env` repository, identifying devcontainer or
  Docker anti-patterns with file references, and designing a migration toward per-service
  devcontainers backed by a shared docker-compose stack.
---

# Empromptu Dev Env

## Goal

Produce a concrete migration plan from an "everything in one box" devcontainer setup toward:

- per-service `.devcontainer` folders in each service repo
- a shared `docker-compose.yml` in `dev-env`
- service-specific `dev` Dockerfile targets
- per-repo env files referenced by compose instead of redefined in `dev-env`

## Inventory Workflow

Inspect the current repo before proposing architecture changes. Start with:

- `devcontainer.json`
- `Dockerfile`
- any compose files
- `scripts/*`
- `go-service-manager/*` if present
- workspace files such as `empromptu.code-workspace`
- docs that describe the dev setup

Summarize which services are managed here, how they start, and where env or config currently live.

## Analysis Rules

- Ground every anti-pattern in specific files and lines when possible.
- Do not invent repo paths. Derive paths and sibling repo names only from references that actually exist.
- Call out places where `localhost`, env duplication, or single-container assumptions will break the target architecture.

## Target State

Design around:

- one compose service per app or infrastructure component
- service names as internal DNS hostnames
- each service building from its own Dockerfile with a `dev` target
- per-service `.devcontainer/devcontainer.json` files pointing back to the shared compose file

## Required Output Sections

Always produce one Markdown document with these sections:

1. `## Current State (Grounded in Repo Files)`
2. `## Identified Anti-Patterns (with References)`
3. `## Target Architecture (Per-Service Devcontainers + Compose)`
4. `## Env and Config Strategy`
5. `## Migration Runbook (Step-by-Step)`
6. `## Open Questions / Assumptions`

Include example file additions or modifications only when they follow from the repo structure you inspected.
