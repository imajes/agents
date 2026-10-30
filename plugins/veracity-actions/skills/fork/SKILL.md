---
name: fork
description: "Design stub: Create an independent workstream from a specified revision while retaining its ancestry. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Fork workstream

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Create an independent workstream from a specified revision while retaining its ancestry.

Example: “Use $fork to branch this workstream into a separate investigation.”

## Intended modes

- Read a specified parent workstream revision.

- Create a new identity, writer binding, and initial revision with parent and fork-revision references.

- Register the child without modifying the parent or promoting local state to project authority.

## Inputs

- Parent identity and revision

- Child purpose, project association, and intended writer

- Available state adapter

## Observable outputs after implementation

- Independent child workstream reference

- Retained ancestry and provenance

- Confirmed child save with unchanged parent state

## Supporting capabilities — not implemented

- `workstreams`: Revisioned workstream state and discovery.

- `ownership`: Writer ownership and transfer.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

A Veracity workstream fork is distinct from a Git branch, worktree, or app chat. Creating those containers requires a separately requested operation and host support. Do not silently copy private context into a broader scope.

Negative activation case: An alternate solution mentioned in discussion must not create a fork or a new app chat.

## Open design question

Which state should the child inherit by reference, and which state should be copied as a snapshot?

## Provenance

Derived from contract sections D6, E1, E2, E6. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
