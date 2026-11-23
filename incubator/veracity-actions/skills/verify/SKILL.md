---
name: verify
description: "Design stub: Check material claims against current evidence and separate direct support, derivation, speculation, and source disagreement. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Verify claims

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Check material claims against current evidence and separate direct support, derivation, speculation, and source disagreement.

Example: “Use $verify to check the load-bearing claims in this proposal.”

## Intended modes

- Extract material claims, splitting claims with different evidence status.

- Check freshness and retrieve appropriate primary sources or current artifacts.

- Expose what the source actually supports, what is derived, and what remains speculative.

- Reconcile conflicting sources and give a practical validation path for unresolved claims.

- Produce a claim review or optional inline evidence annotations, keeping reusable payloads clean.

## Inputs

- Claims or artifact to review

- Relevant time/version and decision context

- Available sources, tools, and requested review depth

## Observable outputs after implementation

- Claim-to-evidence findings and citations

- Limitations, conflicts, and validation paths

- Optional annotated explanation outside clean payloads

## Supporting capabilities — not implemented

- `sources`: Current source and artifact access.

- `evidence`: Evidence, assumptions, and decisions.

- `artifacts`: Current artifact reads, patches, and validation.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

Source retrieval and interpretation are separate. A source saying something does not establish universal truth. No invented browsing, test results, or numeric calibration; a failed tool is not evidence of an absent fact.

Negative activation case: Ordinary conversation must not activate a mandatory claim-tail format without selecting this skill or a later explicit profile.

## Open design question

Should verification produce a separate evidence review, inline annotations, or a user-selected combination?

## Provenance

Derived from contract sections 0.1, 0.4, B1, B2, B4, F2. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
