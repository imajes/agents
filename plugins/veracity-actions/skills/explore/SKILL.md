---
name: explore
description: "Design stub: Take a deliberately bounded detour and return to the prior focus with the useful findings preserved. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Explore

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Take a deliberately bounded detour and return to the prior focus with the useful findings preserved.

Example: “Use $explore for one turn on this alternative, then return to the migration plan.”

## Intended modes

- Begin EXPLORE N with a topic, an explicit turn budget, and a saved return point.

- Track exploration turns and allow an explicit extension or early RESUME.

- At the limit, summarize useful findings, park unresolved follow-ups, and restore the prior focus.

## Inputs

- Topic or existing tangent ID

- Budget and what counts as a turn

- Prior focus and next action

## Observable outputs after implementation

- Exploration status and remaining budget

- A concise findings summary

- Restored direction and linked follow-ups

## Supporting capabilities — not implemented

- `direction`: Conversation direction and exploration state.

- `ideas`: Faithful idea capture and contextual views.

- `workstreams`: Revisioned workstream state and discovery.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Exploration does not silently replace the objective or authorize external actions. Tool calls and progress notes should not consume extra assistant-turn budget. Future time budgets require a real clock and execution support; this stub starts no timer.

Negative activation case: Mentioning a possible alternative in passing must not begin exploration.

## Open design question

Is an assistant-turn budget the right default, and how should nesting or an interrupted exploration work?

## Provenance

Derived from contract sections D4, D6, D7, D8. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
