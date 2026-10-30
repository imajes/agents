---
name: audit
description: "Design stub: Inspect whether the work and its reported status meet the relevant collaboration requirements. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Audit collaboration

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Inspect whether the work and its reported status meet the relevant collaboration requirements.

Example: “Use $audit to check this result for unsupported claims, drift, and missing recovery information.”

## Intended modes

- Run a requested full pillar review or a focused exception review.

- Compare reported actions, evidence, focus, and persistence claims with observable results.

- Check relevant pre-send requirements for the selected skills and delivery format.

- Distinguish repairable presentation defects, operational delays, and material integrity problems.

- Recommend recovery, verification, or state repair without claiming universal adherence.

## Inputs

- Result, conversation excerpt, or workstream to inspect

- Selected requirements and actual evidence

- Desired review depth

## Observable outputs after implementation

- Concrete findings linked to evidence

- Material exceptions and repair recommendations

- Explicit untested areas and limits of the audit

## Supporting capabilities — not implemented

- `evidence`: Evidence, assumptions, and decisions.

- `workstreams`: Revisioned workstream state and discovery.

- `artifacts`: Current artifact reads, patches, and validation.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

A status table is not proof of compliant reasoning. This is a deliberate review action, not a hidden every-response hook. Diagnose missing evidence without pretending to inspect private reasoning.

Negative activation case: Missing decorative glyphs alone must not block unrelated authorized work.

## Open design question

Which review checks provide useful signal without recreating a large mandatory response wrapper?

## Provenance

Derived from contract sections 0.1, 0.2, 0.3, 0.4, A3, A4, B1, D7, D9, G. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
