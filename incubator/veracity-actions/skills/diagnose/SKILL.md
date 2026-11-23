---
name: diagnose
description: "Design stub: Turn symptoms into testable hypotheses and evidence-backed conclusions before proposing a fix. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Diagnose

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Turn symptoms into testable hypotheses and evidence-backed conclusions before proposing a fix.

Example: “Use $diagnose to investigate why this workflow is failing.”

## Intended modes

- Separate observed symptoms from hypotheses and assumptions.

- Choose minimal discriminating checks and record actual outcomes.

- Revise the causal explanation when evidence disagrees.

- Propose a fix with material validation, rollback, and operational implications.

## Inputs

- Symptoms, relevant artifacts, and current environment

- Available read/execute permissions

- Failure impact and already-attempted checks

## Observable outputs after implementation

- Evidence-backed diagnosis or bounded remaining uncertainty

- A reproducible check and observed result

- A proposed remedy and validation path

## Supporting capabilities — not implemented

- `sources`: Current source and artifact access.

- `evidence`: Evidence, assumptions, and decisions.

- `artifacts`: Current artifact reads, patches, and validation.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Diagnosis is not permission to apply fixes or run destructive probes. Distinguish observations, tests actually performed, and tests only proposed. Do not turn this into a generic engineering tutorial.

Negative activation case: A request to explain an error message must not silently mutate the system.

## Open design question

Is this distinct enough from verify to earn a separate invocation, given its causal-test workflow?

## Provenance

Derived from contract sections 0.1, 0.2, 0.4, C4, F1. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
