---
name: recover
description: "Design stub: Find and reconcile the correct surviving workstream after interruption or context loss, with deliberate resume ownership. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Recover

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Find and reconcile the correct surviving workstream after interruption or context loss, with deliberate resume ownership.

Example: “Use $recover to find where this workstream stopped and show the next action.”

## Intended modes

- Discover candidate workstreams using known IDs, exposed thread bindings, and project indexes.

- Load the best matching record and reconcile revision, provenance, writer, and location.

- Show recovered direction and unresolved gaps without initializing replacement state.

- For an explicit RESUME WORKSTREAM request, acquire or transfer ownership before later writes.

- Resolve ambiguity with one narrow choice; use conversation or memory only as labeled weaker evidence.

## Inputs

- Known workstream/thread/project pointers

- Current user request: inspect, recover, or resume

- Surviving records and ownership information

## Observable outputs after implementation

- Recovered identity, direction, revision, and next action

- Source and uncertainty of recovered state

- An ownership result only when a real transfer occurred

## Supporting capabilities — not implemented

- `workstreams`: Revisioned workstream state and discovery.

- `ownership`: Writer ownership and transfer.

- `export`: Portable checkpoint and handoff.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Showing a saved next action does not authorize executing it. Do not invent platform IDs, merge unrelated threads, silently reset revision numbers, or claim automatic compaction recovery. Intended duration: one recovery/resume request.

Negative activation case: A user asking what happened last time must not trigger a new task, ownership transfer, or implementation.

## Open design question

Should read-only recovery and writer-acquiring resume be separate skills or clearly separated modes?

## Provenance

Derived from contract sections 0.3, A4, D1, D6, E1, E5, E6, E7, E8. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
