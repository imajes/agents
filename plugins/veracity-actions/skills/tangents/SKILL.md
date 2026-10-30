---
name: tangents
description: "Design stub: Capture adjacent ideas without losing their wording or the active thread, then retrieve and review them in context. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Tangents

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Capture adjacent ideas without losing their wording or the active thread, then retrieve and review them in context.

Example: “Use $tangents to help me stay on topic while preserving useful side ideas.”

## Intended modes

- PARK an idea immediately, before exploring it; preserve the original wording separately from a short title.

- Show an inline capture receipt and the return point to the main task.

- Show LEDGER on request or a relevant milestone; filter by thread, project, or general ideas.

- Set or revise a concrete revisit trigger, priority, project association, or relationship.

- Close, drop, reopen, or propose promotion of a tangent with a reason and retained history.

- Recognize an idea becoming a dependency; route explicit exploration to explore and accepted project promotion to promote.

## Inputs

- Original idea text and enough surrounding context to interpret it

- Originating conversation/workstream and known project associations

- Current focus/return point, revisit trigger, and user intent

## Observable outputs after implementation

- A stable capture reference with actual write/read-back status

- A compact inline receipt and return-to-focus cue

- Contextual ledger views and disposition history

## Supporting capabilities — not implemented

- `ideas`: Faithful idea capture and contextual views.

- `direction`: Conversation direction and exploration state.

- `reporting`: Visible action and control receipts.

- `promotion`: Project knowledge promotion.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

General ideas and project-specific ideas need distinct context without separate competing copies. An idea is not a task, a memory, or permission for background research. A save failure must remain visible. Natural-language overrides remain valid. Intended duration: the opted-in conversation, with explicit release.

Negative activation case: A correction to the current deliverable must not be parked, and a fictional idea in a quotation must not be captured as the user’s own initiative.

## Open design question

Which context is essential for a faithful capture, and should the inline receipt always include the durable ID?

## Provenance

Derived from contract sections 0.3, D3, D4, D6, D8, E1, E7. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
