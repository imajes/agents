# Agent role manifest

This manifest is the human-readable index for the standalone roles in the parent `agents` directory. The top-level TOML files remain authoritative for runtime behavior, models, permissions, and detailed instructions. This file defines the taxonomy, routing intent, and cross-role boundaries; it is not a mission-state store, action ledger, or replacement for the canonical workstream record.

Start with the [agent system handbook](README.md) for the authority ladder and reading paths. [Architecture](ARCHITECTURE.md), [design guidance](DESIGN.md), and the [decision register](DECISIONS.md) explain this contract without overriding it; [editing](EDITING.md) and [validation](VALIDATION.md) define the change workflow.

## Naming doctrine

- Use naval rank names only for roles with delegated command authority.
- Use naval operational terms where the analogy clarifies a real function.
- Keep technical specialists named for the evidence or artifact they produce.
- A role name never grants authority beyond the user's request and the mission contract.
- `default` is the runtime-reserved omitted-role fallback and is not part of the command rank system.

## Command topology

```text
commander
├── lieutenant        one major independently managed workstream
│   └── chief         one narrow squad with close supervision
├── archivist         committed operational record and recovery
├── inspector         swarm assurance, dependency/gate health, and capacity
└── briefer           user-facing situation picture and commitments
```

The commander, lieutenant, and chief are the only standing command roles. Lieutenants and chiefs receive bounded delegated authority; they do not inherit authority to change mission scope or perform external side effects.

## Role inventory

| Role | Function | Key boundary |
| --- | --- | --- |
| `default` | General mixed analysis and execution fallback | Becomes commander-of-record behaviorally only after explicit multi-agent authorization. |
| `commander` | Mission-wide planning, delegation, supervision, reconciliation, and synthesis | User remains the source of mission authority. |
| `lieutenant` | Independent command of one major workstream and nested team | Escalates cross-workstream, scope, and authority decisions. |
| `chief` | Close supervision of a narrow lane and small squad | Keeps ownership local and reports through its lead. |
| `archivist` | Canonical workstream state, action/call/decision log, report reconciliation, revision acknowledgements, and recovery snapshots | Records and reconciles; does not invent mission decisions or user narrative. |
| `inspector` | Point-in-time swarm snapshots, topology/dependency/gate audits, capacity diagnosis, and bounded corrective intervention | Assures the control plane; does not become a second commander or root-record writer. |
| `briefer` | SITREPs, decision briefs, cadence updates, and the record of what the user was told, asked, or promised | Presents committed state; does not mutate operational truth while drafting. |
| `navigator` | Problem framing, scope, constraints, acceptance criteria, dependencies, and execution course | Shapes the route; does not command it or implement most code. |
| `logistics` | Reminders, scheduling, costs, bills, bookings, and real-world administrative follow-through | Role selection does not authorize purchases, payments, messages, or bookings. |
| `machinist` | Dependencies, toolchains, builds, CI, environments, caches, ports, services, and shared runtime machinery | Maintains machinery around the code; does not own product implementation. |
| `reliability_engineer` | SLOs, production observability, incidents, capacity, resilience, recovery, and operational readiness | Owns deployed-service health; production mutations require exact authority, and development machinery remains with `machinist`. |
| `integrator` | Git branches, worktrees, commits, integration, and repository permission preflight | Preserves unrelated work and owns only explicitly assigned Git operations. |
| `signals` | Short, high-signal operational alerts and authorized external dispatch | Transmits alerts; it is not SIGINT and does not own briefing narrative. |
| `watchkeeper` | Long-running observation, real bounded waits, deadline checks, and state-change reporting | Observes and reports; does not reinterpret or broaden the watched task. |
| `analyst` | Intake, decomposition, dependency mapping, risk analysis, and role routing | Shapes ambiguous work into bounded lanes without silently choosing material scope. |
| `critic` | Independent adversarial challenge of ideas, decisions, plans, claims, and non-code outputs | Steelmans and stress-tests; it neither reviews code nor makes the final decision. |
| `scout` | Fast read-only code archaeology, control-flow tracing, and repository reconnaissance | Returns bounded evidence for another role to act on. |
| `researcher` | Primary-source investigation of documentation, external systems, standards, and current behavior | Handles broader source work; routes repo-local reconnaissance to `scout`. |
| `product_manager` | Customer problems, product outcomes, prioritization, discovery, roadmaps, experiments, and requirements | Owns product judgment; `navigator` owns accepted-delivery shaping and `designer` owns experience expression. |
| `customer_success` | Post-sale outcomes, onboarding, adoption, account health, escalations, renewal readiness, and voice-of-customer evidence | Owns customer success plans; customer contact, CRM changes, and commercial commitments require exact authority. |
| `data_analyst` | Metrics, data quality, reproducible quantitative analysis, statistical uncertainty, and experiment readouts | Produces decision evidence; does not silently make the product, commercial, or venture decision. |
| `machine_learning_engineer` | Dataset and feature lineage, model training and fine-tuning, evaluation, inference packaging, drift, and retirement | Owns the learned-component lifecycle inside an accepted contract or decision-owner-approved bounded architecture experiment; application integration and AI-system shape stay separate. |
| `marketer` | Audience, positioning, brand, go-to-market, growth, campaign, and marketplace strategy | Owns commercial strategy; production, publishing, outreach, and spend require separate ownership and authority. |
| `venture_analyst` | Fundability, venture markets, business models, traction, unit economics, fundraising, and investment diligence | Keeps founder advice separate from investor diligence and does not provide legal, tax, accounting, or transactional advice. |
| `security_engineer` | Threat models, security architecture/review, vulnerability validation, controls, and remediation evidence | Defaults to read-only and requires exact authorization for active probing; remediation implementation stays with `programmer`. |
| `ai_architect` | AI-versus-non-AI choice, foundation/hosted model and provider, system pattern, knowledge/retrieval shape, orchestration, evaluation, controls, cost, and integration architecture | Produces a dated decision record or bounded discriminating experiment contract; it neither implements nor treats a fashionable model or retrieval substrate as the default. |
| `designer` | Interaction, layout, copy, UX flow, visual direction, and design specifications | Returns a design deliverable and recommended implementation handoff. |
| `programmer` | Product-code implementation, debugging, refactoring, and owned tests | Owns a concrete code surface and validates it before handoff. |
| `validator` | Reusable test harnesses, fixtures, seams, helpers, coverage strategy, and validation evidence | Builds the evidence-producing apparatus; does not replace adversarial review. |
| `reviewer` | Adversarial patch review, regression hunting, missing-test detection, and risk assessment | Reports findings and recommends fixes; does not silently implement them. |
| `writer` | Substantial polished summaries, reports, and other written artifacts | Writes an assigned artifact; routine SITREPs remain with `briefer`. |
| `deckhand` | Generic bounded execution and support when no specialist is justified | Finishes one concrete assignment and does not self-expand its scope. |

## Specialist decision routing

| Decision or artifact | Primary specialist | Boundary and common handoff |
| --- | --- | --- |
| Stress-test a non-code proposal, plan, claim, or decision | `critic` | Challenges the strongest version and returns findings to the decision owner; code patches remain with `reviewer`, and live swarm structure remains with `inspector`. |
| Decide which customer problem or product outcome to pursue | `product_manager` | Produces the product decision and requirements; `navigator` shapes delivery, `designer` shapes the experience, and `data_analyst` supplies quantitative evidence. |
| Turn post-sale outcomes into onboarding, adoption, health, escalation, renewal-readiness, or voice-of-customer plans | `customer_success` | Owns named-account or segment success actions; `product_manager` retains product decisions, `marketer` retains market strategy, `navigator` sequences accepted cross-team delivery, and external customer or CRM actions require exact authority. |
| Define, reconcile, or interpret metrics and structured data | `data_analyst` | Owns definitions, method, uncertainty, and reproducibility; the relevant product, commercial, or venture owner retains the decision. |
| Develop and lifecycle-manage a learned component from governed data | `machine_learning_engineer` | Owns algorithm/model candidates, training, evaluation, inference artifacts, drift, and retirement within an accepted contract or bounded architecture experiment; paid compute, registry writes, and deployment need exact authority, while service operations remain with `reliability_engineer`. |
| Decide audience, positioning, message architecture, channel, launch, growth, or marketplace strategy | `marketer` | Supplies commercial strategy and production briefs; `designer` owns expression, `writer` owns substantial polished copy, and external action needs exact authority. |
| Assess venture fundability, fundraising readiness, or an investor case | `venture_analyst` | Declares founder-advisory or investor-diligence mode; `marketer` owns market-facing execution and qualified professionals own legal, tax, accounting, and regulated advice. |
| Model threats or assess vulnerabilities and security controls | `security_engineer` | Supplies security findings and verification requirements; `programmer` implements remediation, `reviewer` reviews ordinary patch correctness, and active testing needs exact authorization. |
| Define SLOs or assess incidents, production observability, capacity, resilience, recovery, or readiness | `reliability_engineer` | Owns deployed-service reliability evidence and operational artifacts; `machinist` owns build/dev machinery, `programmer` owns code remediation, and production mutations require exact authority. |
| Decide whether and how to use AI, including system pattern, current model/provider, knowledge/retrieval shape, tools, agents, evaluation, and guardrails | `ai_architect` | Produces a dated architecture decision record; `machine_learning_engineer` owns learned-component execution, `programmer` implements, and current vendor evidence comes from `researcher` when substantial. |

## Shared state and reporting loop

For a multi-workstream, long-running, unattended, or context-risky mission, establish one stable shared `archivist` and one stable shared `briefer`. Add one stable shared `inspector` when the mission is wide, horizontally elastic, gate-heavy, degraded, or otherwise needs independent control-plane assurance; do not impose it on a small healthy mission merely to complete the topology.

1. Managers produce evidence-bearing reports at activation, ownership changes, material decisions, blockers, handoffs, completion, before long waits or context rollover, and after recovery. A manager publishes for a leaf that cannot write the configured record, preserving source attribution.
2. The reporter appends the durable report before sending a small live pointer to the archivist.
3. The archivist validates identity, record ownership, writer epoch, and base semantic revision; commits the authorized state change; and returns a revisioned acknowledgement or explicit rejection state.
4. Managers recover operational context from the named root record, its children and report cursors, plus the archivist's revisioned snapshot.
5. The inspector compares committed topology/work state with the live loaded hierarchy, publishes coherent or explicitly skewed snapshots, and routes findings or authorized interventions through command and the archivist.
6. The briefer reads committed state and assurance findings, labels their exact source revisions and freshness, and produces the user-facing situation picture.
7. The briefer returns each communication event through the same report/acknowledgement path so user asks, decisions, promises, delivery evidence, and the next briefing boundary remain recoverable.
8. Managers use `send_message` while a shared staff task is running, `followup_task` when it is idle, and `list_agents` to recover canonical paths. These are wakeup and control mechanisms, not durable payload storage.

### Beads continuity protocol v1

Use this protocol only when the mission already has an authorized Beads workspace and named root record. Role selection alone does not authorize `bd init`, repository hooks, remotes, or other setup changes. If Beads is unavailable, the commander names one durable fallback, locator, durability scope, and writer rather than silently inventing another store.

The tested baseline is Beads 1.1.2 with Dolt. Embedded mode serialized eight simultaneous comment writers successfully at ordinary staff-report volume. A separate two-writer probe confirmed that concurrent full metadata replacements are last-writer-wins: semantic revisions and epochs can detect cooperative stale work but are not compare-and-swap or a hard process fence. Protocol v1 therefore uses record-level ownership and exactly one root-envelope writer. Server mode may improve throughput or deployment topology, but it does not remove that ownership rule.

| Mission concept | Beads representation | Mutable owner |
| --- | --- | --- |
| Mission/workstream | One root epic labeled `codex-workstream` | Control owner for replacement; bound archivist for normal root-envelope writes |
| Compact recovery snapshot | Root metadata key `codex_workstream` | Bound archivist only |
| Lane or action | Native child issue with assignee, status, parent, priority, and dependencies | Assigned record owner |
| Decision or blocker detail | Native decision/action record plus dependency edges and evidence comments | Assigned record owner or archivist, as declared |
| Report | `codex.report/v1` JSON comment on the affected record | Authorized reporter; append-only |
| Acknowledgement | `codex.ack/v1` JSON comment on the same record | Bound archivist; append-only |
| Live wakeup or correction | MultiAgent message containing only a locator/pointer | Current manager/staff task |
| Portable recovery document | Generated Markdown export | Generated view; never a co-authority |

The root issue's assignee and `codex_workstream.persistence_writer.task_path` must identify the same active archivist. A compact root envelope has this shape:

```json
{
  "codex_workstream": {
    "schema": "codex.workstream/v1",
    "semantic_revision": 12,
    "control_owner": "/root",
    "persistence_writer": {
      "task_path": "/root/archivist",
      "epoch": 3
    },
    "recovery_owner": "/root/archivist",
    "objective": "...",
    "focus": "...",
    "definition_of_done": ["..."],
    "authority_constraints": ["..."],
    "decision_refs": ["bd-decision-id"],
    "blocker_refs": ["bd-blocker-id"],
    "lanes": {
      "bd-lane-id": {
        "owner": "/root/lieutenant",
        "state": "running",
        "summary": "...",
        "next_action": "...",
        "evidence": ["..."]
      }
    },
    "report_cursors": {
      "bd-lane-id": {
        "report_id": "/root/lieutenant:stable-id",
        "source_comment_id": "comment-id",
        "committed_revision": 12
      }
    },
    "next_action": "...",
    "briefing": {
      "last_source_revision": 10,
      "last_event_revision": 11,
      "last_briefed_at": "2026-08-05T08:00:00Z",
      "open_user_asks": [],
      "commitments": [],
      "next_boundary": null
    },
    "inspection": {
      "last_source_revision": 10,
      "last_event_revision": 12,
      "last_inspected_at": "2026-08-05T08:00:30Z",
      "inspector": "/root/inspector",
      "health": "degraded",
      "coherence": "coherent",
      "open_finding_refs": ["bd-finding-id"],
      "undersupplied_lanes": ["bd-lane-id"],
      "pending_interventions": []
    },
    "updated_at": "2026-08-05T08:01:00Z"
  }
}
```

Keep the `inspection` object even when no inspector is configured: use null revisions, timestamp, and path; `unknown` health/coherence; and empty finding, undersupplied-lane, and intervention arrays. That makes “not inspected” explicit without turning the inspector into mandatory mission overhead.

Keep this envelope bounded. Detailed decision history, report prose, completed blockers, and exhaustive evidence remain in native issues/comments and Dolt history. Mutable lane metadata should not duplicate native issue status or accumulate stale next actions; the root lane entry is the committed mission-level projection, while the child issue and its comments retain the detailed record.

Every durable intake is a JSON comment matching this logical envelope:

```json
{
  "schema": "codex.report/v1",
  "report_id": "/root/lieutenant:stable-id",
  "workstream_id": "bd-root-id",
  "record_id": "bd-lane-id",
  "reporter": "/root/lieutenant",
  "target_writer_epoch": 3,
  "base_revision": 12,
  "event": "progress",
  "status": "running",
  "summary": "...",
  "evidence": ["file, test, source, artifact, or bead reference"],
  "dependencies_or_needs": [],
  "next_action": "...",
  "user_visible": {
    "risk_changed": false,
    "timing_changed": false,
    "decision_request": null
  },
  "observed_at": "2026-08-05T08:02:00Z"
}
```

`event` is normally one of `activation`, `ownership`, `progress`, `decision`, `blocker`, `handoff`, `completion`, `pre_wait`, `pre_rollover`, `recovery`, `inspection`, or `briefing`. The Beads comment author must equal `reporter`; writers use their canonical task path as the `bd --actor` value. An identical retry of an unacknowledged report reuses the original `report_id` and payload. A submission rebased after `stale` or `fenced` uses a new report ID with the current base revision and writer epoch; an event-specific `source_revision` continues to identify the historical state actually observed or presented. The live notification follows the durable append and is intentionally small:

```text
REPORT_READY <workstream-id> <record-id> <report-id>
```

The archivist returns a JSON comment with this logical shape:

```json
{
  "schema": "codex.ack/v1",
  "report_id": "/root/lieutenant:stable-id",
  "workstream_id": "bd-root-id",
  "record_id": "bd-lane-id",
  "status": "accepted",
  "base_revision": 12,
  "current_revision": 12,
  "committed_revision": 13,
  "writer": {
    "task_path": "/root/archivist",
    "epoch": 3
  },
  "applied_fields": ["lanes.bd-lane-id", "report_cursors.bd-lane-id"],
  "conflict": null,
  "required_action": null,
  "acknowledged_at": "2026-08-05T08:02:10Z"
}
```

Acknowledgement status is one of:

- `accepted`: applied once and committed at `committed_revision`.
- `duplicate`: the same report ID was already applied; root state is not mutated again.
- `stale`: the base semantic revision is no longer current; refresh and submit a new report ID.
- `fenced`: the report targets a retired writer epoch; refresh the root binding and submit a new report ID.
- `conflict`: authorized evidence or fields disagree and require reconciliation or command decision.
- `rejected`: identity, ownership, schema, evidence, or authority validation failed.

The commit sequence is deliberately recoverable:

1. Read the current root, affected record, report comments after its cursor, and existing acknowledgements. Resolve report comments for that record in durable append order; before handling a pointed report, resolve every earlier unacknowledged report and never advance the cursor past one.
2. Validate workstream/record identity, Beads comment author, record ownership, permitted fields, evidence, target writer epoch, and base revision.
3. Resolve duplicate, stale, fenced, conflict, and rejection cases without mutating root state.
4. For an accepted report, replace the complete root envelope once while preserving unrelated top-level metadata keys, advance `semantic_revision` by exactly one, and commit the report ID, source comment ID, and new revision in the affected record's cursor as part of that same metadata update.
5. Append the acknowledgement comment.

If the archivist crashes after step 4 but before step 5, its replacement sees the committed cursor and emits the missing acknowledgement without applying the report again. If a live pointer is lost, recovery scans comments after the recorded cursors for unacknowledged reports.

The control owner replaces an archivist by first interrupting or retiring the old task, then changing the root assignee and complete root envelope together, advancing the semantic revision and writer epoch, and recording the replacement decision. Reports aimed at the old epoch are fenced. This is a cooperative process fence, not hard split-brain protection. If a mission genuinely requires hostile-writer or crash-consistent compare-and-swap semantics, that requirement must be surfaced explicitly before introducing a transactional adapter.

Recovery is: consume `bd prime` when available; read the named root with `bd show <root-id> --long --json`; read children/dependencies; then read comments after each cursor. `bd prime` restores Beads workflow context but is not the mission snapshot. If the root locator was lost, `bd list --all --label codex-workstream --no-parent --json` can discover active and completed candidates, but the mission contract must disambiguate them. Always state whether durability is local-only or remote-backed.

A briefer records a delivered communication as a root `codex.report/v1` event with `event="briefing"`. It adds `source_revision` for the operational revision actually shown to the user; ordinary `base_revision` remains the expected current root revision used for concurrency validation. If the event is stale, the briefer refreshes `base_revision` and submits a new report ID without changing `source_revision`. `briefing.last_source_revision` stores what the user saw, while `briefing.last_event_revision` stores the later revision that commits the communication event. This avoids pretending that the user saw state which was only recorded after the briefing.

An inspector records a snapshot as a root `codex.report/v1` event with `event="inspection"`. It also separates `source_revision`—the committed workstream revision actually inspected—from concurrency-control `base_revision`, and records independent record/live `as_of` times plus `coherence`. Its event-specific payload contains health, planned and live topology, work coverage, dependency/gate/report freshness, capacity findings, interventions, evidence, and next check. The compact root `inspection` object stores only the last source/event revisions, timestamp, inspector path, health/coherence, open finding references, undersupplied lanes, and pending interventions; detailed snapshots remain in comments or finding records.

Protocol v1 has two agent-visible internal surfaces: Beads/Dolt for durable state and payloads, and MultiAgent messaging for live control/wakeup. It does not use Valkey. Add finite-TTL plumbing only after a measured lease, ingestion, queue, or deduplication need survives Beads comments plus MultiAgent wakeups; it may never be the sole copy of a report, acknowledgement, or pending external side effect.

## Important role boundaries

- `archivist` records operational truth; `briefer` presents it; `writer` produces substantial artifacts; `signals` dispatches short alerts.
- `inspector` audits the swarm control plane and may act only through its assigned intervention level; `archivist` remains the root writer and command roles retain mission decisions.
- `watchkeeper` observes one named wait or changing target; `inspector` diagnoses mission-wide structural health; `signals` transmits. None substitutes for the briefer.
- `navigator` defines a viable execution course; command roles accept, alter, and supervise it.
- `programmer` changes product code; `machinist` maintains build/dev/CI machinery; `reliability_engineer` owns deployed-service health and recovery; `integrator` controls Git consolidation.
- `validator` constructs validation evidence; `reviewer` adversarially evaluates the change and that evidence.
- `scout` handles fast repo-local reconnaissance; `researcher` handles broader primary-source investigation; `analyst` decomposes and routes the mission.
- `critic` challenges non-code reasoning; `reviewer` challenges code changes; `inspector` challenges control-plane health; `security_engineer` assesses system security.
- `product_manager` owns product outcomes and requirements; `navigator` shapes accepted work into a delivery course; `designer` owns experience expression; `marketer` owns commercial positioning and distribution.
- `customer_success` owns post-sale realized outcomes and named-account success plans; `marketer` owns acquisition and market-facing strategy; `product_manager` owns cross-customer product choices.
- `data_analyst` owns reproducible quantitative evidence; `machine_learning_engineer` owns repeated learned inference and its lifecycle; `researcher` owns substantial source collection; the relevant domain specialist or decision owner owns the resulting choice.
- `ai_architect` owns the unsettled AI-system decision, dated architecture record, and any proposed discriminating experiment contract; after decision-owner acceptance, `machine_learning_engineer` or `programmer` may execute that bounded experiment and return evidence, while full implementation waits for the accepted architecture.
- `security_engineer` owns adversarial availability threats and controls; `reliability_engineer` owns accidental-failure resilience and operational response. AI safety boundaries in an architecture do not replace independent security review.
- `venture_analyst` owns venture and fundraising judgment, not operational finance, accounting, tax, legal advice, or marketing execution.
- `logistics` performs real-world coordination only within exact inherited authority.

## Rename ledger

| Historical role | Current role |
| --- | --- |
| `conductor` | `commander` |
| `concertmaster` | `lieutenant` |
| `principal` | `chief` |
| `publicist` | `briefer` |
| `producer` | `navigator` |
| `operator` | `logistics` |
| `quartermaster` | `machinist` |
| `steward` | `integrator` |
| `herald` | `signals` |
| `watcher` | `watchkeeper` |
| `explorer` | `scout` |
| `testsmith` | `validator` |
| `scribe` | `writer` |
| `worker` | `deckhand` |

Existing tasks may retain the role inventory injected when they started. Newly loaded tasks use the current standalone TOML names.
