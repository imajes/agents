# Agent system architecture

> Status: current architecture synthesis, last reviewed 2026-08-05. The top-level `../*.toml` files remain runtime-authoritative, [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md) remains the current human routing contract, and any mission-specific authority comes from the active request and runtime policy. Dated research is supporting evidence, not an override.

## System boundary

This architecture covers standalone role discovery, role contracts, human taxonomy documentation, task and swarm shaping, and continuity conventions under `agents/`. It does not define the entire Codex runtime, install the future routing skill, initialize Beads, or grant authority for external actions.

## Component model

```text
James's request + effective mission contract
                    │
          runtime policy and mode
                    │
            route or clarify work
                    │
        ┌───────────┴───────────┐
        │                       │
 agents/*.toml            ROLE_MANIFEST.md
 runtime contract         human routing contract
        │                       │
        └───────────┬───────────┘
                    │
          bounded task instance
                    │
      evidence → artifact → verification
                    │
          handoff or final synthesis

Current explanation: README / PHILOSOPHY / ARCHITECTURE / DESIGN
Current decisions:   DECISIONS.md
Change procedure:    EDITING.md → VALIDATION.md
Historical evidence: research/
Future router design: routing/  (non-executable)
```

| Component | Responsibility | Does not own |
| --- | --- | --- |
| James's request and mission contract | Outcome, scope, authority, constraints, and material decisions | Reusable role behavior |
| Runtime policy and multi-agent mode | Effective sandbox, approval, delegation, and platform behavior | Domain-specific role method |
| Top-level `agents/*.toml` | Runtime role identity, description, model/effort, timeout, sandbox override, and developer instructions | Mission state or a task-specific assignment |
| [Role manifest](ROLE_MANIFEST.md) | Current human inventory, routing intent, command topology, shared-state protocol, and cross-role seams | Runtime loading or external-action authority |
| Handbook documents | Philosophy, architecture, design rationale, current decisions, editing, and validation | Per-role runtime truth |
| `research/` | Dated evidence, alternatives, completed audits, and historical decisions | Current role count or policy by implication |
| `routing/` | Proposed router input/output contract and forward-test fixtures | Execution, spawning, or delegated authority |

## Discovery and prompt assembly

Codex discovers standalone role TOMLs recursively beneath `agents/`. Runtime roles therefore live only at the top level, while `agents/meta/` remains Markdown-only. A TOML template, metadata file, or fixture beneath `meta/` could be treated as another role and must not be placed there.

Each role file normally defines:

- `name`, which must match the filename stem;
- `description`, used for routing and agent selection;
- `nickname_candidates`, used only for legible spawned-task identity;
- `background_terminal_max_timeout`;
- `model` and `model_reasoning_effort`;
- optional `sandbox_mode` when the role needs a stricter posture;
- `developer_instructions`, the role-specific operating contract.

The runtime assembles the effective context from more than this file. The role's developer instructions are combined with platform-provided root or child usage guidance and the active multi-agent mode. Spawned tasks receive the selected role fragment; they do not need copies of generic shared-filesystem, task-path, or delegation-policy boilerplate inside every TOML.

This assembly has two consequences:

1. Role prompts should concentrate on domain method, required inputs, artifacts, boundaries, evidence, and missing orchestration guarantees.
2. A prompt cannot truthfully claim a runtime identity mutation, permission, wakeup mechanism, or persistence feature that the platform does not provide.

Existing tasks can retain an inventory or instruction fragment injected when they started. Newly loaded tasks use the current files. A rename therefore has a transition period and should preserve a historical ledger in the manifest.

## Authority layers

Authority flows inward from the task; it does not flow outward from the role:

1. James defines or accepts the objective, scope, and meaningful side effects.
2. Runtime policy and mode constrain what the current task may do.
3. A manager may delegate only a bounded portion of authority it actually holds.
4. A specialist owns its assigned artifact or decision, not the whole mission.
5. A recommendation, plan, review, or role selection remains advice until the named decision owner accepts it.

Publishing, messaging, spending, booking, production mutation, active probing, credential use, destructive change, and sensitive-data movement require exact authority even when a role commonly works near those actions.

## Command and execution topology

The standing command hierarchy is:

```text
commander
├── lieutenant       one major independently managed workstream
│   └── chief        one narrow squad requiring close supervision
├── archivist        committed operational record and recovery
├── inspector        optional independent control-plane assurance
└── briefer          sourced user-facing situation picture
```

Only `commander`, `lieutenant`, and `chief` are command ranks. Their distinction is scale and delegated control:

- `commander` owns mission-wide planning, delegation, reconciliation, and synthesis.
- `lieutenant` owns one major workstream and its nested team.
- `chief` owns one narrow lane and a small closely supervised squad.

`archivist`, `inspector`, and `briefer` are staff functions, not alternate command paths. The archivist cannot invent decisions, the inspector cannot become a second commander, and the briefer cannot mutate operational truth while drafting.

Specialists and bounded executors remain artifact owners beneath or beside this control plane. A manager does not absorb their expert judgment merely by supervising them.

## Task-to-artifact flow

A well-shaped task moves through these states:

1. **Intake:** identify the outcome, primary artifact, decision owner, source and freshness needs, side effects, risk, unknowns, and acceptance evidence.
2. **Routing:** choose one primary role; clarify first when ambiguity changes scope, authority, or success criteria.
3. **Contract:** assign exact ownership, inputs, write surface, dependencies, deliverable, validation, stop conditions, and escalation boundary.
4. **Execution:** the owner follows its role-specific method and classifies evidence and uncertainty.
5. **Verification:** use the relevant evidence apparatus, patch review, independent criticism, security assessment, or control-plane inspection. These are distinct methods and are added only when risk justifies them.
6. **Handoff:** return the artifact, evidence, residual risk, decisions needed, and exact next owner.
7. **Synthesis:** the mission owner reconciles accepted outputs against the original objective and authority.

The canonical artifact remains singular even when several agents contribute evidence.

## Swarm shapes

| Shape | Use when | Key invariant |
| --- | --- | --- |
| Single owner | One role can produce and verify the artifact within acceptable risk | Do not add decorative support |
| Parallel swarm | Lanes are independent, ownership is disjoint, and shared-write collisions are resolved | Each lane has a distinct output and no hidden ordering dependency |
| Staged swarm | One role's decision or evidence determines another's work | Acceptance and handoff gates are explicit |
| Clarify first | Missing facts materially change scope, authority, success, or side effects | Do not invent the missing contract |

Command roles are justified by an explicitly authorized multi-workstream mission, not by the mere presence of multiple plausible specialists.

## Shared state and continuity

### Exhaustive evidence

Per-thread rollout JSONL plus the persisted spawn graph are the canonical runtime audit evidence. They preserve owner-attributed events and lineage, including information that may not fit in a compact mission snapshot. They are not, by themselves, a curated statement of the current objective, accepted decision, or next action.

### Compact operational truth

For a multi-workstream, long-running, unattended, or context-risky mission, use one named durable mission record and stable shared staff when the mission contract authorizes them. The current manifest defines a Beads continuity protocol when an authorized Beads workspace and root record already exist:

- one root workstream record carries the bounded semantic envelope;
- child issues carry lanes, actions, ownership, dependencies, and detailed evidence;
- reporters append revisioned reports;
- one bound archivist validates and commits root-envelope changes and appends acknowledgements;
- stale or retired-writer reports are rejected or fenced rather than silently merged;
- the briefer records what was shown, asked, or promised against explicit source and event revisions;
- the inspector records independent point-in-time health snapshots when configured.

The root record has one normal mutable writer. This is cooperative fencing, not hostile-writer compare-and-swap. A mission requiring stronger crash or split-brain guarantees must surface that requirement before introducing a transactional adapter.

### Live control

Multi-agent messages carry small wakeup, correction, or locator signals. They are not the durable payload store. A live notification follows a durable append; losing a notification must remain recoverable from the record.

The protocol therefore exposes two agent-visible internal surfaces when Beads is configured:

1. Beads/Dolt for durable state and evidence-bearing payloads.
2. Multi-agent messaging for immediate control and wakeup.

Valkey is not part of protocol v1. A finite-lived projection or queue should be introduced only after a measured need survives the simpler design, and it must never become the sole copy of a report, acknowledgement, or pending external side effect.

### Conditional staff

- Add one shared `archivist` and `briefer` when mission width, duration, unattended operation, or context risk makes durable reconciliation worthwhile.
- Add one shared `inspector` only when the mission is wide, elastic, gate-heavy, degraded, or assurance-sensitive.
- Use a `watchkeeper` for one named long wait or changing target, not as mission-wide assurance.
- If Beads is unavailable or not authorized, the mission owner names one explicit fallback, locator, durability scope, and writer. Do not silently initialize a store or create competing authorities.

## Information flow and ownership

| Information | Producer | Current owner | Consumer |
| --- | --- | --- | --- |
| Mission objective and authority | James / mission owner | Mission contract | Every assigned owner |
| Role runtime behavior | Role editor | Top-level TOML | Runtime |
| Human role routing | Taxonomy editor | Role manifest | Humans and future router |
| Specialist evidence | Assigned role | Its artifact or source ledger | Decision owner / next stage |
| Operational report | Manager or authorized reporter | Durable mission record after acknowledgement | Archivist, managers, inspector, briefer |
| Assurance snapshot | Inspector | Detailed inspection record plus compact root projection | Command owner and briefer |
| User-facing situation picture | Briefer | Communication event after acknowledgement | James and recovery path |
| Exhaustive event history | Runtime | Rollouts and spawn graph | Audit and reconstruction |

## Change propagation

| Change | Required current surfaces |
| --- | --- |
| Role metadata or operating rule | Matching top-level TOML; manifest only when human routing or a listed boundary changes |
| New, split, merged, retired, or renamed role | TOMLs, manifest inventory and boundaries, adjacent TOMLs, decision register, relevant router fixtures, validation baseline |
| Cross-role ownership seam | Both sides' runtime contracts, manifest, design/decision docs when the rule is system-wide |
| Command or continuity protocol | Command/staff TOMLs, manifest, architecture, decision register, and protocol-specific validation |
| Model, effort, timeout, or sandbox policy | Affected TOMLs; design or decision register when the selection rule changes |
| Router behavior | Router spec and fixtures; no runtime effect until an executable skill is separately approved and installed |
| Historical evidence only | New or updated dated research record; current docs only if a present decision changes |

## Architectural invariants

- Runtime role TOMLs remain top-level and parseable.
- Every runtime `name` is unique and matches its filename.
- The manifest inventory exactly matches discovered runtime roles.
- `agents/meta/` contains no TOML.
- One role owns each primary artifact or decision.
- Command, role selection, and routing do not manufacture side-effect authority.
- Shared staff are conditional, stable for the mission, and replaceable from durable state.
- Durable payload precedes live notification.
- Historical research does not silently become current policy.
- The future router reads live contracts instead of maintaining a copied role catalog.

Run the executable checks in [`VALIDATION.md`](VALIDATION.md) after any relevant change.

## Related evidence

- [Agent configuration audit](research/2026-08-05-agent-config-audit.md)
- [Specialist-gap audit](research/2026-08-05-specialist-gap-audit.md)
- [Specialist expansion decision record](research/2026-08-05-specialist-expansion-plan.md)
- [Current decision register](DECISIONS.md)
