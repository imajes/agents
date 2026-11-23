---
name: focus
description: "Design stub: Establish and steer the objective, current focus, completion condition, and next action for a conversation. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Focus

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Establish and steer the objective, current focus, completion condition, and next action for a conversation.

Example: “Use $focus to keep this conversation directed at finishing the migration plan.”

## Intended modes

- Start or re-anchor a focus session; infer unambiguous direction without a setup interview.

- Show STATE: objective, focus, done, next action, active controls, and honest persistence status.

- Handle ADVANCE and necessary DEPENDENCY segments; route optional TANGENT segments to tangents.

- Apply an explicit PIVOT or NEW OBJECTIVE; preserve the previous direction and reason.

- LOCK FOCUS or UNLOCK FOCUS; report the selected session mode.

- Report meaningful progress, inspect stalls, and propose a smaller next step or a deliberate change of method.

## Inputs

- Current request and relevant conversation context

- Existing workstream identity/state when known

- User-selected focus mode and completion condition

## Observable outputs after implementation

- A visible direction card and control status

- A concrete progress delta or exact blocker

- A proposed state change with its provenance

## Supporting capabilities — not implemented

- `direction`: Conversation direction and exploration state.

- `workstreams`: Revisioned workstream state and discovery.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

A correction, blocker, or explicit instruction must not be discarded as a tangent. Classify mixed messages by segment. Focus control cannot authorize implementation, and ordinary progress notes are not separate durable facts. Intended duration: this conversation until released or replaced.

Negative activation case: An ordinary factual question without explicit skill selection must not start a focus session.

## Open design question

Should focus and tangents remain separate controls, or should selecting tangents also establish a minimal direction card?

## Provenance

Derived from contract sections 0.2, 0.3, A2.1, C7, D1, D2, D3, D5, D6, D7, D9. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
