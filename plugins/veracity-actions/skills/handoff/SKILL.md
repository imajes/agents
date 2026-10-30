---
name: handoff
description: "Design stub: Prepare and verify the transfer of a workstream across conversations, agents, or supported surfaces. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Handoff

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Prepare and verify the transfer of a workstream across conversations, agents, or supported surfaces.

Example: “Use $handoff to prepare this work for another conversation.”

## Intended modes

- Checkpoint the source revision and prepare a portable transfer packet.

- Identify target, capability gaps, and any manual transfer step.

- Transfer writer ownership with an explicit acceptance/verification state.

- Verify the imported revision and report whether transfer is pending, accepted, or failed.

## Inputs

- Source identity, revision, and writer

- Target surface or recipient when specified

- Transfer scope and available adapters

## Observable outputs after implementation

- Portable state packet and source receipt

- Explicit transfer and ownership status

- Target verification or a concrete manual handoff step

## Supporting capabilities — not implemented

- `workstreams`: Revisioned workstream state and discovery.

- `ownership`: Writer ownership and transfer.

- `export`: Portable checkpoint and handoff.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Preparation does not mean delivery or acceptance. No implicit messaging, remote connection, or background agent. Transfer failure must not strand the only usable state. Do not claim that local files are accessible in ChatGPT web.

Negative activation case: Asking for a summary must not send it to another chat or pause another writer.

## Open design question

What is the smallest safe transfer protocol that preserves a usable source until target acceptance?

## Provenance

Derived from contract sections D6, E3, E4, E6, E8. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
