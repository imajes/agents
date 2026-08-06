# Specialist expansion decision record

> Historical completed phase. The 32-role result and boundary decisions remain evidence, while the [current role manifest](../ROLE_MANIFEST.md), [handbook](../README.md), and live TOMLs define present layout and behavior.

Last updated: 2026-08-05 17:58 UTC

## Completion state

Complete. Four explicitly requested standing specialists—production reliability/SRE, machine-learning engineering, customer success, and AI architecture—have been added without broadening the settled generalist or command backbone. The runtime taxonomy now contains 32 top-level role TOMLs, the human-readable taxonomy and research live under `agents/meta`, and the future routing skill has a design contract and forward-test fixtures but has not been initialized.

All changes remain unstaged and uncommitted for James's review.

## Repository boundary

- Repository: `/Users/james/.codex`, branch `app/beta`, HEAD `3e589031e9079175f9338694a473cec0ca6839cc` at completion.
- Preserve the earlier continuity/inspector work and the six previously added specialists: `critic`, `marketer`, `venture_analyst`, `product_manager`, `data_analyst`, and `security_engineer`.
- Unrelated user-owned changes remain in `.codex-global-state.json`, `config/config.toml`, `custom_instructions.md`, and `skills/.system/openai-docs/**`; this phase did not modify them.
- Do not stage or commit without James's request.
- Root `AGENTS.md` is zero bytes.

## Implemented specialists

| Role | Model / effort | Sandbox posture | Canonical artifact and hard boundary |
| --- | --- | --- | --- |
| `reliability_engineer` | Sol / Max | Assigned local reliability artifacts; deployed systems read-only until exact action authority | Reliability packet plus SLO, runbook, readiness/capacity plan, resilience evidence, or blameless incident review. Owns deployed-service outcomes; `machinist` retains build/dev/CI machinery and SLA commitment remains with the named business/product/legal/contract owner. |
| `machine_learning_engineer` | Sol / Max | Assigned local ML artifacts; source data, registries, compute services, and production read-only until exact authority | Model-lifecycle packet, experiment ledger, lineage, model card, reproducible pipeline, and readiness evidence. Owns algorithm/model candidates and learned-component lifecycle; `ai_architect` retains the larger AI-system decision and `reliability_engineer` retains serving operations. |
| `customer_success` | Sol / XHigh | Assigned local success artifacts; customer, CRM, ticketing, account, contract, and communication systems read-only until exact authority | Customer-success packet, success plan, health review, escalation brief, QBR content, renewal-readiness assessment, or voice-of-customer synthesis. Owns post-sale outcomes and customer context; `marketer` retains market strategy, `product_manager` product choices, and `navigator` cross-team delivery sequencing. |
| `ai_architect` | Sol / Max | `read-only` | Dated AI architecture decision record or bounded architecture-experiment contract. Owns AI-versus-non-AI, foundation/hosted model and provider, system/retrieval/tool pattern, evaluation gates, and integration boundaries; it proposes but does not implement or grant execution authority. |

## Deliberate routing seams

- Reliability versus machinery: `reliability_engineer` owns SLOs, production observability, incident reasoning, capacity, resilience, and recovery; `machinist` owns dependencies, toolchains, builds, CI, development environments, caches, ports, and local/shared runtime support.
- ML versus architecture: `ai_architect` owns whether and how the larger system uses AI, including foundation/hosted model and provider and knowledge/retrieval shape. `machine_learning_engineer` owns deterministic-versus-learned component baselines, algorithm and trained-model candidates, data, training, evaluation, inference artifacts, drift, retraining, and retirement inside an accepted learned-component contract.
- Architecture evidence loop: when existing evidence cannot discriminate viable architectures, `ai_architect` may propose a bounded experiment. Execution begins only after the named architecture decision owner accepts the contract and separately authorizes the exact data, candidates, write surface, budget, evaluation rule, and stop conditions. `programmer` or `machine_learning_engineer` executes only that bounded experiment; evidence returns to `ai_architect` for the final recommendation.
- Customer success versus product and marketing: `customer_success` owns post-sale realized outcomes, named-account health, adoption, escalations, renewal readiness, and field evidence. `marketer` owns acquisition and segment-level commercial strategy; `product_manager` owns cross-customer product decisions; `navigator` sequences an accepted cross-team remedy.
- Availability: `security_engineer` owns adversarial threats and security-control verification; `reliability_engineer` owns accidental-failure resilience, operational response, and recovery.
- Evidence: `researcher` gathers dated primary-source evidence and `data_analyst` produces reproducible quantitative evidence without taking the relevant specialist's decision.

## Meta-document layout

```text
agents/
  *.toml
  meta/
    README.md
    ROLE_MANIFEST.md
    research/
      2026-08-05-agent-config-audit.md
      2026-08-05-specialist-gap-audit.md
      2026-08-05-specialist-expansion-plan.md
    routing/
      ROUTER_SPEC.md
      ROUTER_FIXTURES.md
```

The top-level `agents/*.toml` files remain runtime-authoritative. `agents/meta` is deliberately Markdown-only because the Codex loader recursively discovers TOMLs beneath `agents/`. `ROLE_MANIFEST.md` is the canonical human taxonomy and routing contract. The two older ignored visualization files remain unchanged thread-recovery snapshots; their durable, versionable research copies live here and carry historical-status notices.

The root `README.md` now points to `agents/*.toml` and `agents/meta/` instead of the former nonexistent nested agent-config layout.

## Future routing skill

`routing/ROUTER_SPEC.md` defines a recommendation-only `codex.agent-routing/v1` output, the `single`, `parallel-swarm`, `staged-swarm`, and `clarify-first` shapes, authority gates, role-selection rules, and the four new specialist triggers. `routing/ROUTER_FIXTURES.md` contains realistic forward cases for support RAG, production reliability, fraud modeling, customer onboarding/renewal, CI dependency work, graph-backed assistant decisions, patch review, and materially ambiguous AI requests.

The router treats RAG as a system pattern; lexical, vector, relational, graph, API, and tool surfaces are possible evidence substrates rather than mutually exclusive peer architectures. It treats current foundation model/provider choice as a dated-evidence problem and supports the architect-proposed, decision-owner-accepted bounded experiment loop when evidence is insufficient.

No executable skill was scaffolded. The next skill-specific decisions are its installation root and James's acceptance or revision of the forward fixtures. Once those are settled, initialize it with the canonical skill-creator workflow, load the live manifest rather than copying a second role catalog, validate it with `quick_validate.py`, and forward-test it with fresh realistic prompts.

## Adversarial review corrections

The independent boundary audit first confirmed that all four prior defer conditions were explicitly superseded by James's request, then reviewed the implemented runtime prompts. Its findings were corrected and re-reviewed to closure:

1. Added a decision-owner-approved bounded experiment path so AI architecture does not require evidence that no role is allowed to produce.
2. Limited `ai_architect` to system-level and foundation/hosted model/provider choice while keeping algorithm and trained-model candidates with ML engineering.
3. Added `navigator` as the owner of accepted cross-team delivery sequencing while keeping customer-side readiness and commitments with customer success.
4. Replaced the manifest's overbroad “build and operate” ML wording with lifecycle management plus exact compute/registry/deployment gates and reliability ownership of service operations.
5. Changed SLA ownership to feasibility review and retained external commitment with the named business/product/legal/contract owner.
6. Mirrored architect proposal, decision-owner acceptance, and explicit execution authorization across the architect, ML, programmer, manifest, and router-fixture contracts.

The final closure pass reported no remaining contradiction, material overlap, authority leak, or handoff loop.

## Validation evidence

- `taplo check agents/*.toml` passes for all 32 runtime role files.
- Required fields are nonblank; runtime role IDs are unique and match filenames; descriptions are unique; model, effort, timeout, newline, and nickname-character constraints pass.
- The Ultra set remains exactly `commander`, `lieutenant`, and `chief`.
- The read-only set is exactly `ai_architect`, `analyst`, `critic`, `researcher`, `reviewer`, `scout`, `security_engineer`, `venture_analyst`, and `watchkeeper`.
- The 32-row manifest inventory exactly matches the 32 top-level role TOMLs, and all three embedded JSON examples parse.
- `agents/meta` contains no TOML files and its documents are not ignored by Git.
- No retired backticked role IDs remain in runtime TOMLs; the historical research and manifest rename ledger preserve old names intentionally. No stale short-form ML role ID or stale live manifest/config-agent path remains.
- `git diff --check` and explicit untracked-file whitespace/newline checks pass.
- Ordinary and `--strict-config` Codex Doctor both report `Configuration [ok] config loaded`. Their overall nonzero status remains caused by the noninteractive `TERM=dumb` check; the pre-existing rollout/state parity issue remains only a warning.
- No agent or meta-document change is staged.

There is no remaining implementation work in this specialist-expansion phase. The next distinct phase is the executable routing skill after its two user-facing design decisions are settled.
