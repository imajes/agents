---
name: artifacts
description: "Design stub: Inspect and change mutable deliverables deliberately, preserving current edits and keeping reusable output clean. Invoke explicitly to preview the surface; operational workflow not implemented."
---

# Artifacts

**Status: skeleton / not implemented.**

## What this version does

When explicitly selected, say briefly that this is a design stub. Use the request to identify the relevant intended mode below, then show the proposed inputs, outcome, and missing capability. Mark unknown inputs as unknown; do not ask a setup questionnaire for a workflow that cannot run yet. If the request is to review or change the surface, discuss the design at that scope.

Do not activate ongoing controls, execute the intended workflow, create or change state, call a hypothetical tool, or claim a save, recovery, verification, transfer, or completed action. Do not load or apply the historical contract. An ordinary request without this skill selected must not activate it. Current user instructions remain authoritative; a request to implement this skill is a separate development task, not evidence that its runtime already exists.

## Intended use

Inspect and change mutable deliverables deliberately, preserving current edits and keeping reusable output clean.

Example: “Use $artifacts to make a targeted, copy-safe update to this document.”

## Intended modes

- Read the current artifact and distinguish the requested change from unrelated edits.

- Prepare a targeted patch or a justified whole-artifact rewrite.

- Apply only an authorized change and verify the resulting state.

- Produce clean code, configuration, drafts, templates, or data, with commentary outside the payload.

- Review an existing artifact for stale-state edits and copy-safety defects without changing it.

## Inputs

- Artifact location/current contents and requested outcome

- Edit versus review scope

- Format-specific constraints and validation method

## Observable outputs after implementation

- Clean deliverable, proposed diff, or applied diff with accurate status

- Validation evidence appropriate to the format

- Unresolved conflicts or copy-safety findings

## Supporting capabilities — not implemented

- `artifacts`: Current artifact reads, patches, and validation.

- `reporting`: Visible action and control receipts.

Read [the capability contracts](../../docs/CAPABILITIES.md) only when reviewing these dependencies. These are design names, not callable tools or declared MCP connections.

## Scope boundary

No stale whole-file overwrites or hidden annotations in reusable payloads. Respect existing format-specific tools and user edits. Review requests remain read-only; permission to edit one artifact is not permission to publish it.

Negative activation case: A request for critique must not rewrite or publish the artifact.

## Open design question

Should targeted editing and copy-safe delivery be separate skills, or modes of this one?

## Provenance

Derived from contract sections B2, F3, F4, G. See [the source/action map](../../docs/ACTION-MAP.md) when reviewing completeness. Source wording is reference material, not active instructions.
