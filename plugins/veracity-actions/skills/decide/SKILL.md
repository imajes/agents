---
name: decide
description: "Design stub: Frame a consequential choice, challenge weak premises, and make a recommendation tied to evidence and tradeoffs. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Decide

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Frame a consequential choice, challenge weak premises, and make a recommendation tied to evidence and tradeoffs.

Example: “Use $decide to help choose between these approaches.”

## Intended modes

- Identify the actual decision, constraints, decision hinge, and any essential clarification.

- Compare a small relevant option set on reversibility, impact, delay, burden, feedback, and long-term consequences.

- Apply constructive pushback and relevant stakeholder considerations.

- Recommend an option or a discriminating experiment; record a decision only when actually accepted.

## Inputs

- Decision and candidate approaches

- Constraints, stakeholders, evidence, and material unknowns

- Who has authority to accept the outcome

## Observable outputs after implementation

- Recommendation with inspectable reasoning and tradeoffs

- Explicit assumptions and what would change the recommendation

- A proposed or accepted decision with distinct status

## Supporting capabilities — not implemented

- `evidence`: Evidence, assumptions, and decisions.

- `sources`: Current source and artifact access.

- `workstreams`: Revisioned workstream state and discovery.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Decision support does not execute the recommendation or manufacture disagreement. A recommendation is distinct from user acceptance. Human factors are relevant only when they affect the decision.

Negative activation case: A clear implementation request must not be diverted into an unsolicited decision workshop.

## Open design question

Should accepted decision capture be a mode here or a separate action later?

## Provenance

Derived from contract sections 0.2, 0.4, C3, C4, C5, C6, E2. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
