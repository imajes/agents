# .agents

This repository is the working home for James's experiments, tools, and reusable assets for collaborating with AI agents.

It exists to collect the pieces that make agent work durable instead of ad hoc: prompts, skills, plugins, operating guidance, and the supporting notes that explain how those parts are supposed to work together. The goal is not just to save snippets. The goal is to build a practical, versioned environment for doing better work with agents over time.

## What This Repo Is For

- Capture reusable agent-facing assets instead of leaving them scattered across chats, scratch files, and local experiments.
- Keep workflow knowledge close to the code and prompts that depend on it.
- Turn one-off discoveries into durable building blocks.
- Provide a place to evolve local plugins, skill bundles, and operating rules in the open.
- Make agent collaboration more inspectable, repeatable, and easier to improve.

## How To Read This Repository

This is not a single application. It is a toolkit and workspace.

Some parts define how agents should behave. Some parts teach agents how to perform specific jobs. Some parts package those capabilities into local plugins. Some parts capture the surrounding notes, experiments, and guidance that make the system usable in practice.

The throughline is simple: if a pattern is useful enough to keep using with agents, it probably belongs here.

## Repository Map

### `skills/`

Reusable skills that teach agents how to do focused kinds of work.

These range from general tooling support to domain-specific workflows, including:

- browser automation
- code refactors and repo survey tools
- design and document-processing helpers
- git and CI workflows
- media generation and transcription
- security review and threat-modeling support
- shell safety and workflow utilities
- team and ticket workflow helpers

Most skill directories include a `SKILL.md` entrypoint plus any supporting scripts, references, assets, or agent metadata needed to make the skill practical.

### `plugins/`

Local plugins and marketplace metadata.

Right now this includes a local marketplace definition in `plugins/marketplace.json` and the `codex-deltas` plugin source under `plugins/codex-deltas/`. That plugin is a concrete example of the kind of work this repository is meant to support: packaging a real agent workflow into a reusable local plugin with skills, scripts, docs, and release surfaces.

### `operating-contract/`

Long-lived guidance for how assistants should work with James.

The contract is not decorative documentation. It is meant to capture the behavioral rules that should persist across sessions: truthfulness, pragmatism, continuity, skepticism, and the visible hooks that keep those values in play.

### `docs/`

Supporting notes about the surrounding platform and workflow.

These documents exist to record what has been learned about the current agent/plugin ecosystem, especially where the official story is incomplete, evolving, or underspecified.

### `cycles/`

A holding area for repeatable loops, experiments, or workflow cycles as they become worth formalizing.

At the moment this is mostly reserved space, but it reflects the intended shape of the repo: not just static artifacts, but reusable operating loops.

## Working Model

The repository is built around a few practical ideas:

1. Prompts are useful, but prompts alone are fragile.
2. Skills are more durable when they carry instructions, scripts, references, and examples together.
3. Plugins are how those capabilities become installable, discoverable, and easier to reuse.
4. Operating rules matter because the quality of agent work depends on behavior as much as tooling.
5. Notes and guidance are worth versioning when they explain how the system really works.

In other words, this repo is meant to be an agent workshop, not a prompt dump.

## Current Shape

Today the repository is already strongest in three areas:

- curated local skills for practical engineering and workflow tasks
- local plugin work, especially around `codex-deltas`
- explicit operating guidance for how agent collaboration should feel and function

Over time, it can grow into a broader library of prompts, repeatable cycles, and plugin-backed agent systems without losing the thread that ties them together.

## Why It Matters

Working with agents gets better when the useful parts stop living only in memory.

This repository is the place where those useful parts get promoted into durable artifacts: documented expectations, reusable instructions, local tools, and workflows that can be rerun, inspected, and improved instead of rediscovered.
