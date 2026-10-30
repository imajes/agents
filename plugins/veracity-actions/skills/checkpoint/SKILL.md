---
name: checkpoint
description: "Design stub: Preserve a recoverable, revisioned snapshot of a workstream and make the persistence boundary explicit. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Checkpoint

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Preserve a recoverable, revisioned snapshot of a workstream and make the persistence boundary explicit.

Example: “Use $checkpoint to prepare a recoverable snapshot before I leave.”

## Intended modes

- Create or update a namespaced workstream checkpoint after a material change.

- Select an available persistence adapter and disclose its actual reach.

- Check the expected revision and writer binding; preserve history and surface conflicts.

- Verify a successful save and update a discovery index of pointers.

- Produce a portable Markdown/structured snapshot when direct saving is unavailable.

## Inputs

- Workstream ID, writer binding, expected revision, and source location

- Objective, focus, done, next action, constraints, decisions, assumptions, and tangent references

- Available destination and desired continuation surface

## Observable outputs after implementation

- Versioned state envelope and readable checkpoint

- Actual location, revision, save/read-back result, and reach

- Explicit manual-save-pending status when applicable

## Supporting capabilities — not implemented

- `workstreams`: Revisioned workstream state and discovery.

- `export`: Portable checkpoint and handoff.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Rendering a checkpoint is not saving it. Read-back is not proof of backup, cross-device access, or recovery after every failure. Do not overwrite another thread’s state or silently change adapters. Beads retains task ownership when present; a checkpoint refers to tasks rather than becoming another tracker.

Negative activation case: A brief answer or every sentence must not trigger a checkpoint automatically.

## Open design question

Which state deserves capture at each material change, and which parts can remain links to existing Beads records?

## Provenance

Derived from contract sections 0.3, D1, D2, D6, E1, E2, E3, E4, E7, E8. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
