# Agent system decision register

> Status: current accepted decisions, last reviewed 2026-08-05. This register summarizes cross-cutting design choices. Top-level `../*.toml` files remain runtime-authoritative, [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md) remains the canonical human inventory and routing contract, and James's active request remains the source of mission authority.

## How to use this register

Stable decision IDs let current documents and future changes refer to one choice without replaying the originating thread. The register is compact by design:

- Amend a decision in place when its meaning is refined but its identity remains.
- Mark a decision superseded and link its replacement when the accepted rule changes.
- Add a dated research record when substantial evidence, experiments, or rejected alternatives matter.
- Do not append routine edit history here; Git and dated research carry that evidence.
- Do not treat a status of “accepted” as task authority or permission for side effects.

## Current index

| ID | Decision | Status |
| --- | --- | --- |
| [AGT-001](#agt-001--runtime-roles-stay-top-level-and-authoritative) | Runtime roles stay top-level and authoritative | Accepted |
| [AGT-002](#agt-002--human-documentation-has-layered-authority) | Human documentation has layered authority | Accepted |
| [AGT-003](#agt-003--roles-are-artifact-first-and-minimal) | Roles are artifact-first and minimal | Accepted |
| [AGT-004](#agt-004--naval-ranks-are-reserved-for-command) | Naval ranks are reserved for command | Accepted |
| [AGT-005](#agt-005--role-selection-never-grants-mission-authority) | Role selection never grants mission authority | Accepted |
| [AGT-006](#agt-006--the-generalist-backbone-is-stable) | The generalist backbone is stable | Accepted |
| [AGT-007](#agt-007--model-effort-and-sandbox-posture-follow-the-method) | Model, effort, and sandbox posture follow the method | Accepted |
| [AGT-008](#agt-008--role-prompts-do-not-duplicate-runtime-boilerplate) | Role prompts do not duplicate runtime boilerplate | Accepted |
| [AGT-009](#agt-009--continuity-uses-durable-state-plus-live-control) | Continuity uses durable state plus live control | Accepted, conditional |
| [AGT-010](#agt-010--shared-staff-and-inspection-are-conditional) | Shared staff and inspection are conditional | Accepted |
| [AGT-011](#agt-011--the-future-router-is-recommendation-only) | The future router is recommendation-only | Accepted |
| [AGT-012](#agt-012--ai-architecture-may-use-a-bounded-evidence-loop) | AI architecture may use a bounded evidence loop | Accepted |
| [AGT-013](#agt-013--dated-research-is-evidence-not-live-policy) | Dated research is evidence, not live policy | Accepted |

## AGT-001 — Runtime roles stay top-level and authoritative

**Decision.** Every loadable standalone role lives in one top-level `agents/<role_id>.toml` file. That file is authoritative for runtime identity, routing description, nickname candidates, timeout, model/effort, sandbox override, and developer instructions.

**Rationale.** Codex recursively discovers TOMLs beneath `agents/`. Keeping runtime definitions flat makes discovery inspectable and prevents documentation metadata from becoming accidental roles.

**Consequences.**

- `agents/meta/` remains Markdown-only.
- A candidate contract stays inside [`ROLE_TEMPLATE.md`](ROLE_TEMPLATE.md) until intentionally materialized at the top level.
- Runtime facts in human documentation must be reconciled against the TOMLs.

**Evidence.** [Agent configuration audit](research/2026-08-05-agent-config-audit.md) and [specialist expansion record](research/2026-08-05-specialist-expansion-plan.md).

## AGT-002 — Human documentation has layered authority

**Decision.** [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md) is the canonical human inventory, command topology, routing contract, and continuity protocol. The handbook explains current design. `research/` preserves dated evidence. `routing/` contains non-runtime future-router design.

**Rationale.** One document cannot be a concise routing index, a design essay, a history log, and a runtime config without becoming ambiguous and stale.

**Consequences.**

- Each current fact has one preferred owner and other documents link to it.
- A runtime/manifest mismatch is repaired in the same change rather than rationalized through a lower-authority document.
- Historical role counts and provisional conclusions never silently become current policy.

**Evidence.** [Documentation bootstrap decision record](research/2026-08-05-documentation-bootstrap-plan.md).

## AGT-003 — Roles are artifact-first and minimal

**Decision.** Select the smallest capable primary owner for the requested decision or artifact. A standing specialist must have recurring demand, a distinctive method, a canonical output, a sharp boundary, and a safe authority posture.

**Rationale.** Topic-based personas create overlap and coordination cost. Artifact ownership makes routing, verification, and handoff inspectable.

**Consequences.**

- Supporting roles are added only for distinct necessary artifacts, gates, or evidence packages.
- A technology-specific task defaults to an existing role plus an applicable skill unless the admission test proves a durable gap.
- One primary owner remains accountable even when several agents contribute.

**Evidence.** [Specialist-gap audit](research/2026-08-05-specialist-gap-audit.md) and [design guide](DESIGN.md).

## AGT-004 — Naval ranks are reserved for command

**Decision.** `commander`, `lieutenant`, and `chief` are the only standing command ranks. All technical, domain, staff, and execution roles use functional names.

**Rationale.** Rank names should communicate real delegated control, not prestige or technical seniority.

**Consequences.**

- `commander` owns the mission, `lieutenant` one major workstream, and `chief` one narrow closely supervised squad.
- `default` may behave as commander-of-record only after explicit multi-agent authorization; its runtime ID does not become a rank.
- `archivist`, `inspector`, and `briefer` remain staff functions with no parallel command path.

**Evidence.** [Role manifest command topology](ROLE_MANIFEST.md#command-topology) and [agent configuration audit](research/2026-08-05-agent-config-audit.md).

## AGT-005 — Role selection never grants mission authority

**Decision.** A role, command position, routing recommendation, model choice, or sandbox posture never expands the authority in James's request and the effective mission contract.

**Rationale.** Capability and permission are different. Conflating them is especially dangerous around external communication, money, production systems, active testing, credentials, destructive actions, and sensitive data.

**Consequences.**

- Consequential side effects have exact target, action, owner, rollback or stop boundary, and verification gates.
- Delegated authority is bounded and non-transitive.
- Advisory outputs remain proposals until the named decision owner accepts them.

**Evidence.** Every current specialist contract and the [role manifest naming doctrine](ROLE_MANIFEST.md#naming-doctrine).

## AGT-006 — The generalist backbone is stable

**Decision.** Do not add, delete, merge, or broadly expand generalist and command roles merely to resolve a domain gap. Add a specialist only after the role admission test proves a recurring distinct method and artifact.

**Rationale.** The current apparent overlaps among intake, navigation, validation, review, observation, briefing, writing, generic execution, and command are intentional and bounded by different outputs.

**Consequences.**

- New specialist work may add narrow reciprocal boundary sentences to adjacent generalists, but does not absorb their scope.
- Deferrals can be superseded by a direct request and a completed specialist design review, as happened for reliability, ML engineering, customer success, and AI architecture.
- Future editors must distinguish a recurring domain from a one-off assignment or skill need.

**Evidence.** [Specialist-gap audit](research/2026-08-05-specialist-gap-audit.md) and [specialist expansion record](research/2026-08-05-specialist-expansion-plan.md).

## AGT-007 — Model, effort, and sandbox posture follow the method

**Decision.** Model family, reasoning effort, timeout, and sandbox posture are chosen from the role's method, consequence, latency profile, and write responsibility—not its title or perceived seniority. The live TOMLs are the exact matrix.

**Rationale.** Command work needs sustained cross-lane reasoning; deep specialists need evidence-sensitive analysis; cadence-oriented roles benefit from lower latency; independent advisory roles often benefit from read-only separation.

**Consequences.**

- Ultra remains reserved for `commander`, `lieutenant`, and `chief` under the current quality-first matrix.
- A new role does not inherit Max, Ultra, or workspace write by analogy alone.
- Any matrix change requires method-based rationale, catalog compatibility, and real loader validation.

**Evidence.** [Agent configuration audit](research/2026-08-05-agent-config-audit.md) and [design guide](DESIGN.md#model-effort-and-latency-design).

## AGT-008 — Role prompts do not duplicate runtime boilerplate

**Decision.** Role prompts specify role-specific method, artifacts, evidence, boundaries, safety, and missing orchestration guarantees. They rely on runtime-injected root/child guidance and active multi-agent mode for generic platform behavior.

**Rationale.** Duplicated platform boilerplate drifts and can contradict a later effective mode. Prompt claims also cannot create runtime features such as identity mutation, durable mail, or timers.

**Consequences.**

- Shared-filesystem and canonical-task-path facts are not repeated without a role-specific reason.
- Reporting deadlines are owned supervision actions, not promises that prompt text will wake a task.
- Prompt reviews test the effective assembled behavior, not the TOML fragment in isolation.

**Evidence.** [Agent configuration audit](research/2026-08-05-agent-config-audit.md), especially the post-challenge runtime evidence.

## AGT-009 — Continuity uses durable state plus live control

**Decision.** When an authorized Beads workspace and named mission root already exist, protocol v1 uses Beads/Dolt for durable semantic state and evidence-bearing payloads, and multi-agent messaging for wakeup and control. Rollouts plus the spawn graph remain exhaustive audit evidence. Valkey is not part of protocol v1.

**Rationale.** Mail is low-latency but not a durable payload ledger. Exhaustive transcripts are durable evidence but not a compact accepted mission state. One committed root envelope plus append-only reports and acknowledgements provides recoverability without exposing agents to several competing stores.

**Consequences.**

- Durable append precedes live pointer notification.
- One bound archivist normally writes the root envelope and advances semantic revisions.
- Writer epochs and revisions detect cooperative stale work but do not provide hostile-writer compare-and-swap.
- Beads initialization, hooks, remotes, or fallback-store creation require separate authority.

**Evidence.** [Role manifest continuity protocol](ROLE_MANIFEST.md#beads-continuity-protocol-v1) and [agent configuration audit](research/2026-08-05-agent-config-audit.md).

## AGT-010 — Shared staff and inspection are conditional

**Decision.** Add one stable shared `archivist` and `briefer` for multi-workstream, long-running, unattended, or context-risky missions. Add `inspector` only when mission width, elasticity, gate density, degradation, or assurance needs justify independent control-plane review.

**Rationale.** Durable reconciliation and sourced briefing solve real continuity problems, but permanent command overhead harms small healthy tasks. Inspection must stay independent without becoming a second commander or root writer.

**Consequences.**

- Small single-owner tasks do not create staff merely to complete a topology.
- A `watchkeeper` handles one bounded wait; it does not substitute for mission assurance.
- Staff tasks are stable during the mission but replaceable from committed state.

**Evidence.** [Role manifest shared-state loop](ROLE_MANIFEST.md#shared-state-and-reporting-loop) and the live `archivist`, `briefer`, and `inspector` TOMLs.

## AGT-011 — The future router is recommendation-only

**Decision.** The proposed task router returns `single`, `parallel-swarm`, `staged-swarm`, or `clarify-first` recommendations and explicit gates. It never silently spawns, widens scope, or grants side-effect authority.

**Rationale.** Routing quality improves when task intake and exclusions are explicit, but automatic execution would conflate advice, delegation authorization, and permission.

**Consequences.**

- The future skill reads the live manifest and top-level TOMLs instead of maintaining a copied role catalog.
- It remains uninstalled until its root and fixtures are accepted and the canonical skill-creator workflow is used.
- Current provider/model choice routes to dated architect and researcher evidence rather than frozen heuristics.

**Evidence.** [Router specification](routing/ROUTER_SPEC.md) and [router fixtures](routing/ROUTER_FIXTURES.md).

## AGT-012 — AI architecture may use a bounded evidence loop

**Decision.** When current evidence cannot distinguish viable AI architectures, `ai_architect` may propose a bounded discriminating experiment. Execution begins only after decision-owner acceptance and separate exact execution authority; evidence returns to the architect before full implementation.

**Rationale.** An advisory architect should not implement silently, but an architecture process must be able to generate missing evidence without forcing an implementer to choose the architecture by accident.

**Consequences.**

- `programmer` or `machine_learning_engineer` executes only the accepted experiment scope.
- The contract names candidates, data, write surface, evaluation rule, budget, and stop conditions.
- Full implementation waits for the dated architecture decision.

**Evidence.** [Specialist expansion record](research/2026-08-05-specialist-expansion-plan.md), live specialist TOMLs, and [router fixtures](routing/ROUTER_FIXTURES.md#graph-backed-assistant-decision).

## AGT-013 — Dated research is evidence, not live policy

**Decision.** Preserve completed audits and design checkpoints as dated evidence with explicit historical status. Current documents and runtime contracts carry accepted present state.

**Rationale.** Historical records contain valuable reasoning, but they also preserve old counts, provisional alternatives, retired names, and superseded recommendations.

**Consequences.**

- Do not rewrite history merely to make old files read as current.
- Add or strengthen a historical-status notice when a record can be misread.
- Promote an accepted rule into the manifest, handbook, or decision register rather than relying on the latest timestamp alone.

**Evidence.** The [research directory](research/) and [documentation bootstrap record](research/2026-08-05-documentation-bootstrap-plan.md).
