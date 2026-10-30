---
name: assumptions
description: "Design stub: Maintain the load-bearing premises of a piece of work and make their validation paths and status changes inspectable. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Assumptions

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Maintain the load-bearing premises of a piece of work and make their validation paths and status changes inspectable.

Example: “Use $assumptions to track the premises this recommendation depends on.”

## Intended modes

- Identify and record only material unestablished premises.

- Attach why each premise matters, evidence, uncertainty, and a validation/revisit path.

- Validate, reject, or supersede an assumption with evidence and history.

- Review dependent conclusions when a premise changes; preserve selected risk mode.

## Inputs

- Proposed conclusion, plan, or action and its premises

- Known evidence and uncertainty

- Workstream context and intended risk mode

## Observable outputs after implementation

- A compact assumption register with stable references

- Evidence-backed status transitions

- Affected conclusions or next validation action

## Supporting capabilities — not implemented

- `evidence`: Evidence, assumptions, and decisions.

- `workstreams`: Revisioned workstream state and discovery.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

An inferred claim is not automatically an assumption record. Confidence is an approximate judgment unless genuinely calibrated. Risk mode changes the exploration approach, not permission or truthfulness obligations.

Negative activation case: A derived arithmetic result with verified inputs must not automatically create an open assumption.

## Open design question

Should assumption history live alongside workstream checkpoints or in a shared evidence register?

## Provenance

Derived from contract sections 0.1, B2, B3, C3, E2, E4. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
