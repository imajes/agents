# Agent specialist-gap audit checkpoint

> Historical completed audit. The runtime TOMLs and `agents/meta/ROLE_MANIFEST.md` are the current authorities; later dated research records supersede role-count and active-work statements here.

Last updated: 2026-08-05 17:18:48 UTC

## Completion state

Complete. James clarified that the generalist and command backbone was already settled, so this pass audited only missing specialists. Six roles with distinct recurring methods and artifacts were added, adjacent routing was made explicit, the complete 28-role inventory was validated through the real Codex loader, and every agent change remains unstaged and uncommitted.

## Authoritative repository boundary

- Repository: `/Users/james/.codex`, branch `app/beta`, prior known HEAD `3e589031e9079175f9338694a473cec0ca6839cc`.
- The pre-existing inspector/continuity patch remains unstaged: tracked changes in `agents/meta/ROLE_MANIFEST.md`, `analyst.toml`, `archivist.toml`, `briefer.toml`, `chief.toml`, `commander.toml`, `default.toml`, `lieutenant.toml`, and `watchkeeper.toml`, plus untracked `inspector.toml`.
- Unrelated user-owned changes remain in `.codex-global-state.json`, `config/config.toml`, `custom_instructions.md`, and `skills/.system/openai-docs/**`. Preserve them exactly.
- No agent diff is staged. Do not stage or commit without James's request.
- `/Users/james/.codex/AGENTS.md` is zero bytes.

## Generalist conclusion — frozen

Do not add, delete, merge, or broaden generalists. The apparent overlaps are intentional and already bounded:

- `analyst` decomposes ambiguity; `navigator` turns an accepted goal into a delivery course.
- `validator` builds validation apparatus; `reviewer` attacks code/patch correctness.
- `watchkeeper` observes one target; `inspector` audits the mission control plane.
- `writer`, `briefer`, and `signals` own a substantial artifact, official mission projection, and short dispatch respectively.
- `default` is the runtime fallback/controller; `deckhand` is the explicit bounded generic execution lane.
- Commander/lieutenant/chief overlap only by deliberate hierarchy and scope.

Existing generalist TOMLs should receive no scope expansion. Only narrowly necessary routing-boundary sentences may be added so new specialists do not collide with existing roles.

## Specialist decisions

### Add now — six roles

1. `critic` — cross-domain, non-code adversarial challenge of ideas, decisions, plans, claims, and outputs. Distinct artifact: challenge packet with steelman, material objections, countercase, tests/mitigations, and disposition. Boundary: code patches stay with `reviewer`; swarm health with `inspector`.
2. `marketer` — customer/audience, positioning, brand, GTM, growth/channel, campaign, and marketplace strategy. Distinct artifacts: positioning/message house, GTM or launch plan, campaign brief, marketplace playbook, experiment/measurement plan. Boundary: `designer` owns visual/experience expression; `writer` polished copy; `researcher` source collection.
3. `venture_analyst` — founder-side fundraising readiness or investor-side VC diligence, explicitly separated. Distinct artifacts: venture/fundability packet, investment memo content, round/return logic, diligence plan. Boundary: `marketer` owns market-facing execution; no personalized securities/legal/tax advice or transactions.
4. `product_manager` — product discovery, customer problem, outcome metrics, prioritization, roadmap/experiment decisions, and product requirement artifacts. Distinct artifact: product decision packet/brief/roadmap slice. Boundary: `navigator` owns delivery shaping and sequencing, `designer` experience, `marketer` commercial positioning.
5. `data_analyst` — quantitative analysis, metric definition, data quality, SQL/Python/statistical reasoning, uncertainty, experiment readouts, and reproducible analytical artifacts. Distinct artifact: source-backed analysis with grain/denominator/assumption ledger. Boundary: intake `analyst` is not quantitative; `researcher` sources facts; `validator` tests software.
6. `security_engineer` — threat modeling, security architecture/review, vulnerability validation, trust boundaries, secrets/auth/data/privacy controls, and remediation guidance. Distinct artifact: evidence-backed threat/review findings. Boundary: `reviewer` owns general patch correctness, `critic` non-code argument challenge, `inspector` swarm control plane. Use security skills when invoked.

### Implemented specialist set

- `/Users/james/.codex/agents/critic.toml`: Sol/Max, read-only. Steelman-first, non-performative adversarial reasoning, stable gated findings, explicit boundaries.
- `/Users/james/.codex/agents/marketer.toml`: Sol/XHigh. Modes for brand/GTM/growth/campaign/marketplace, evidence and ethical constraints, production/external-action boundaries.
- `/Users/james/.codex/agents/venture_analyst.toml`: Sol/Max, read-only. Strict founder-advisory versus investor-diligence modes, quantitative/source discipline, venture return logic, high-stakes guardrails.
- `/Users/james/.codex/agents/product_manager.toml`: Sol/XHigh. Customer-problem and outcome framing, metric trees, inspectable prioritization, falsifiable discovery, requirements, product decision packet, and local-artifact-only write boundary.
- `/Users/james/.codex/agents/data_analyst.toml`: Sol/Max. Data-quality and definition audits, reproducible SQL/Python/statistical work, experiment checks, uncertainty, sensitive-data controls, and explicit source/grain/denominator ledger.
- `/Users/james/.codex/agents/security_engineer.toml`: Sol/Max, read-only. Passive-first threat/review modes, exact authorization for active probing, stable evidence-backed findings, secret protection, remediation requirements, and no silent implementation.

All six files are untracked by design. The pre-existing untracked `inspector.toml` remains separate but part of the same validated 28-role inventory. Do not stage or commit them without James's request.

### Adversarial corrections made

- `critic.toml` now routes product judgment, reproducible quantitative analysis, and security assessment to their new specialists while retaining independent challenge authority.
- `marketer.toml` no longer assigns product priorities to `navigator`; it separates `product_manager` product choices, `navigator` delivery shaping, `data_analyst` measurement, and `venture_analyst` fundability.
- `venture_analyst.toml` now separates product judgment, delivery shaping, commercial execution, and substantial reproducible metric analysis while retaining venture-specific calculations and judgment.
- The first Codex Doctor pass caught an invalid apostrophe in one security nickname candidate. The candidate was replaced; both ordinary and strict config loading now have zero startup warnings.
- No material overlap, authority leak, handoff loop, or high-stakes overclaim survived the final review.

### Defer as standing roles

Historical decision at 2026-08-05 17:18 UTC. At 17:32 UTC James explicitly requested standing reliability, machine-learning, customer-success, and AI-architecture roles. That request supersedes the SRE, ML, and customer-success deferrals below; the rationale remains preserved as the condition that triggered their later addition.

- Legal/compliance: real high-stakes domain, but a generic persona risks jurisdiction-free pseudo-advice. Use `researcher` with current authoritative jurisdiction-specific sources and human counsel; add a narrowly scoped legal/compliance role only after recurring work proves the need.
- Operational finance/accounting/tax: `venture_analyst` is deliberately not this. Use spreadsheet/data analysis plus qualified professionals; add only after recurring budgeting/accounting workflows define a safe boundary.
- Sales/customer success: currently overlaps `marketer` strategy, `logistics` authorized execution, and product work. Split later only if repeatable pipeline, enablement, onboarding, or retention lanes appear.
- SRE/cloud/reliability: `machinist` + `programmer` cover current tooling/runtime needs. Add a reliability specialist only when production observability, incidents, SLOs, or cloud architecture recur.
- ML/science, accessibility, performance, database, and API architecture: currently better expressed as a domain-specific assignment plus relevant skills to `programmer`, `researcher`, `designer`, `reviewer`, or `data_analyst`; avoid one role per technology.

## Applied routing edits

Edits were kept minimal and specialist-only:

- `reviewer.toml`: explicitly route non-code ideas/decisions/output challenges to `critic`.
- `designer.toml`: `marketer` owns commercial audience/positioning/message strategy; designer owns visual/interaction expression and UI copy.
- `writer.toml`: render accepted commercial/venture/product strategy; do not silently create it.
- `researcher.toml`: provide current source packs to marketer/venture/product/data/security roles without becoming the decision specialist.
- `inspector.toml`: distinguish control-plane assurance from `critic` and `security_engineer`.
- `validator.toml`: distinguish software validation infrastructure from quantitative analysis and security review if needed.
- `commander.toml`: optionally invoke `critic` as a bounded gate for consequential/irreversible decisions; it is not permanent command staff. Do not broaden generalist scope.
- `agents/meta/ROLE_MANIFEST.md`: add all six roles to inventory and important boundaries; update role count implicitly through table. Add a compact specialist-routing section/table if useful.

No specialist-gap edit was made to `analyst`, `navigator`, `default`, or `deckhand`. Their pre-existing inspector/continuity changes were preserved exactly.

## Validation completed

1. All six prompts received an adversarial overlap, authority, external-action, high-stakes, and handoff-loop review; the three stale cross-role boundaries above were repaired.
2. `taplo check agents/*.toml` passes for all 28 role files.
3. All required fields are nonblank; role names are unique and match filenames; descriptions are unique; every nickname candidate satisfies the runtime character constraint and every file ends with a newline.
4. The current model catalog supports all configured effort levels. The Ultra set remains exactly `commander`, `lieutenant`, and `chief`. The read-only set is exactly `analyst`, `critic`, `researcher`, `reviewer`, `scout`, `security_engineer`, `venture_analyst`, and `watchkeeper`.
5. The manifest inventory exactly matches all 28 TOMLs, and all three embedded JSON examples parse.
6. Live TOMLs contain no retired role IDs, `assign_task`, or `send_input`; every referenced new specialist exists.
7. Ordinary and `--strict-config` Codex Doctor both report `config.load: ok`, `summary: config loaded`, with no startup warnings.
8. `git diff --check -- agents`, the cached diff check, and explicit untracked-file trailing-whitespace checks pass.
9. No agent change is staged. Unrelated `.codex-global-state.json`, `config/config.toml`, `custom_instructions.md`, and `skills/.system/openai-docs/**` changes remain untouched.

## Final handoff state

The specialist-gap pass is complete. Do not reopen or refactor the settled generalists on recovery. The only optional next repository action is to review, stage, or commit the combined agent patch if James explicitly asks; otherwise leave the working tree as-is.
