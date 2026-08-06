# Agent task router specification

Status: design input for a future skill; not executable and not a source of delegation authority. The [live role manifest](../ROLE_MANIFEST.md) and top-level runtime TOMLs remain authoritative; see the [handbook](../README.md) and [AGT-011](../DECISIONS.md#agt-011--the-future-router-is-recommendation-only) for the surrounding authority model.

Proposed skill name: `route-agent-work`.

## Purpose

Given a concrete task description and optional constraints, recommend the smallest capable primary agent or explicitly shaped agent swarm. The router recommends; it never silently spawns agents, widens scope, grants external-action authority, or treats role selection as permission.

The eventual skill should read the live top-level `agents/*.toml` definitions plus `agents/meta/ROLE_MANIFEST.md`. It should not maintain a second copied role catalog.

## Input contract

Logical schema `codex.agent-routing.input/v1`:

```json
{
  "task_description": "...",
  "constraints": [],
  "repository_context": null,
  "user_authorized_delegation": false,
  "desired_delivery": null,
  "authority_context": {
    "external_actions": [],
    "production_changes": false,
    "active_security_testing": false,
    "sensitive_data": false
  }
}
```

Only `task_description` is required. Missing material facts become assumptions, unknowns, or a `clarify-first` recommendation—not invented scope.

## Output contract

Logical schema `codex.agent-routing/v1`:

```json
{
  "schema": "codex.agent-routing/v1",
  "task_summary": "...",
  "intake": {
    "intent": "...",
    "artifacts": [],
    "domains": [],
    "code_scope": null,
    "external_freshness_needed": false,
    "side_effects": [],
    "risk_factors": [],
    "unknowns": []
  },
  "recommendation": {
    "shape": "single",
    "orchestration": {
      "role": null,
      "reason": null,
      "requires_delegation_authorization": false
    },
    "primary": [
      {
        "role": "...",
        "ownership": "...",
        "deliverable": "...",
        "reason": "...",
        "confidence": "high"
      }
    ],
    "support": [],
    "lanes": [],
    "exclusions": []
  },
  "gates": {
    "before_start": [],
    "before_side_effects": [],
    "completion": []
  },
  "alternatives": [],
  "assumptions": []
}
```

`shape` is one of `single`, `parallel-swarm`, `staged-swarm`, or `clarify-first`.

## Decision rules

1. Extract the intended outcome, primary artifact, decision owner, authority, risk, and material unknowns before selecting a role.
2. Prefer one primary artifact owner. Add support roles only when each produces a distinct necessary artifact, gate, or evidence package.
3. Use `clarify-first` or `analyst` when unresolved interpretations materially change scope, success criteria, authority, or side effects.
4. Use parallel lanes only when work is genuinely separable, ownership is disjoint, dependencies are explicit, and shared-write collisions are resolved. Otherwise use staged handoffs.
5. Recommend `commander` only for an explicitly authorized multi-workstream mission. Use `lieutenant` and `chief` only beneath a command owner; never add command roles for decorative coordination.
6. Recommend `archivist` and `briefer` for multi-workstream, long-running, unattended, or context-risky missions. Recommend `inspector` only when the mission is wide, elastic, gate-heavy, degraded, or assurance-sensitive.
7. Turn publishing, spend, messages, bookings, production changes, active security testing, credentials, and sensitive-data movement into explicit gates. Never infer authority from a role.
8. Route independent challenge and verification deliberately: `critic` for consequential non-code decisions, `reviewer` for patches, `validator` for reusable software validation, `security_engineer` for threats/controls, and `inspector` for swarm control-plane assurance.
9. Treat current model/provider choice as a current-evidence task for `ai_architect` with `researcher` support, not as a frozen router heuristic.
10. Explain at least one excluded plausible role when overlap is likely, so the boundary remains inspectable.

## New specialist triggers

- `reliability_engineer`: incidents, SLOs/SLIs, observability, capacity, resilience, operational readiness, production reliability, and recovery. Use `machinist` for toolchains, CI, local environments, and shared development machinery.
- `machine_learning_engineer`: dataset-to-trained/adapted-model lifecycle, features, training/fine-tuning, predictive evaluation, inference packaging, and ML monitoring. Use `data_analyst` for descriptive/decision analysis and `ai_architect` for system, foundation/hosted-model provider, and retrieval shape.
- `customer_success`: post-sale onboarding, adoption, value realization, account health, retention, renewal risk, success plans, and voice-of-customer synthesis. Use `marketer` for acquisition/positioning and `product_manager` for product decisions.
- `ai_architect`: build-versus-buy, current model/provider choice, direct-model versus retrieval-grounded versus structured-query versus tool/agent workflows, lexical/vector/relational/graph substrate choice, fine-tuning decision, integration boundaries, evaluation, guardrails, cost, latency, privacy, and reference architecture.

## AI architecture routing heuristics

- Prefer deterministic code or ordinary search/query when it solves the task reliably.
- Use direct model context when knowledge is bounded and fits the context/evidence contract.
- Use structured database or API queries for authoritative relational or live transactional facts.
- Use vector or hybrid retrieval when changing unstructured evidence requires semantic recall and citations.
- Use a graph only when relationship traversal, multi-hop reasoning, identity resolution, or provenance is central enough to justify graph construction and maintenance.
- Treat RAG as a system pattern whose evidence substrate may be lexical, vector, relational, graph, API, tool-based, or hybrid; do not treat RAG, vector, and graph as mutually exclusive peer choices.
- Use fine-tuning for stable behavior, format, style, or learned task adaptation—not as a substitute for fresh private knowledge.
- Use tool workflows when live state or controlled actions are required; use agentic decomposition only when distinct ownership, state, tools, or approvals outweigh coordination cost.
- Require an evaluation plan and explicit cost, latency, privacy, security, and reliability tradeoffs before commitment.
- When existing evidence cannot discriminate viable architectures, route `ai_architect` to propose a bounded experiment for decision-owner acceptance, then stage execution to `programmer` or `machine_learning_engineer` and return the evidence to `ai_architect` for the final recommendation.

## Future skill implementation

Before creating the actual skill:

1. Confirm its installation root; the default candidate is the user-selected Codex skills directory, not `agents/meta`.
2. Validate the trigger examples in `ROUTER_FIXTURES.md` with James.
3. Initialize it with the canonical `skill-creator` script rather than hand-scaffolding.
4. Keep `SKILL.md` concise and load the live manifest as a reference rather than duplicating role prose.
5. Derive stable routing metadata from each live contract: triggers, anti-triggers, required inputs, canonical artifact, sandbox/write posture, external-action class, common complements, and conflict or precedence rules.
6. Add deterministic code only if repeated routing tests show that a script improves consistency over the text decision rules.
7. Run `quick_validate.py` and forward-test with fresh subagents that receive only realistic task prompts and the candidate skill.

## Related current guidance

- [Taxonomy and contract design](../DESIGN.md)
- [Role editing workflow](../EDITING.md)
- [Validation contract](../VALIDATION.md)
- [Router fixtures](ROUTER_FIXTURES.md)
