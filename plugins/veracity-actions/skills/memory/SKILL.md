---
name: memory
description: "Design stub: Handle explicit personal-memory requests and recovery pointers without treating memory as exact execution state. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Memory

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Handle explicit personal-memory requests and recovery pointers without treating memory as exact execution state.

Example: “Use $memory to remember this preference for future conversations.”

## Intended modes

- Distinguish stable preferences from workstream state, project facts, and transient ideas.

- Prepare an explicit remember, update, or forget operation for the appropriate native memory mechanism.

- Store a compact namespaced recovery pointer only when requested and useful.

- Show the actual persistence result and relevant limitations.

## Inputs

- User’s explicit memory request and exact intended fact

- Scope: personal, project, or workstream pointer

- Available native memory mechanism and existing matching records

## Observable outputs after implementation

- Memory change or a clearly unsaved proposal

- Where it was stored and what was confirmed

- A pointer to stronger state when relevant

## Supporting capabilities — not implemented

- `memory`: Native personal-memory adapter.

- `workstreams`: Revisioned workstream state and discovery.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Use host-native memory tools where available; no silent personal-memory promotion or fabricated durability. Do not duplicate execution state into a generic project-current memory. Forget semantics depend on the actual memory system.

Negative activation case: A passing preference, sensitive aside, or useful idea without a memory request must not be saved as personal memory.

## Open design question

Is this best retained as a skill, or should Veracity only route explicit requests to the host’s memory tool?

## Provenance

Derived from contract sections 0.3, E1, E8. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
