# Agent system handbook

> Status: current synthesis, last reviewed 2026-08-05. The top-level `../*.toml` files are runtime-authoritative, and [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md) is the canonical human taxonomy and routing contract. This handbook explains those authorities; it does not override them or grant mission authority.

This directory is the start-here surface for understanding and changing the standalone Codex agent system. It separates current design from runtime configuration, dated research, and the proposed—but not yet executable—task router.

## Five-minute bootstrap

1. Read the [role manifest](ROLE_MANIFEST.md) for the current inventory, command topology, routing seams, and continuity protocol.
2. Open the relevant top-level role file in `../<role_id>.toml` before relying on any summary. That file controls the role's runtime metadata and developer instructions.
3. Read [`ARCHITECTURE.md`](ARCHITECTURE.md) to understand discovery, prompt assembly, task flow, command structure, and continuity surfaces.
4. Read [`DESIGN.md`](DESIGN.md) before changing a role boundary, model/effort choice, sandbox posture, or swarm shape.
5. Follow [`EDITING.md`](EDITING.md) and [`VALIDATION.md`](VALIDATION.md) for a repository-safe change and an evidence-bearing handoff.

Do not replay the dated research unless the current documents point to a disputed decision or you need the evidence behind it.

## Choose the shortest reading path

| Need | Read |
| --- | --- |
| Pick a role or distinguish two adjacent roles | [Role manifest](ROLE_MANIFEST.md), especially **Role inventory**, **Specialist decision routing**, and **Important role boundaries** |
| Understand why the role system exists | [Philosophy](PHILOSOPHY.md) |
| Understand how runtime, documentation, swarms, and continuity fit together | [Architecture](ARCHITECTURE.md) |
| Add, split, merge, rename, or reshape a role | [Design](DESIGN.md), then [Editing](EDITING.md) |
| See which system-wide choices are currently settled | [Decision register](DECISIONS.md) |
| Validate a proposed patch | [Validation contract](VALIDATION.md) |
| Draft a new role contract | [Role template](ROLE_TEMPLATE.md) |
| Investigate how a decision was reached | [Research records](research/) |
| Work on the future recommendation-only router | [Router specification](routing/ROUTER_SPEC.md) and [fixtures](routing/ROUTER_FIXTURES.md) |

## Authority map

Different sources answer different questions. “Authoritative” is not one undifferentiated rank.

| Question | Authority | If another document disagrees |
| --- | --- | --- |
| What may this task or agent do now? | James's active request, the effective mission contract, runtime policy, and explicit side-effect authorization | Stop or gate the action; a role name or document never expands authority |
| What role configuration is loaded? | The matching top-level `../*.toml` file plus runtime-injected platform instructions | Repair the human documentation after confirming the live behavior |
| What roles exist and where should work route? | [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md), reconciled against the live TOMLs | Treat the TOMLs as runtime truth and fix the manifest in the same patch |
| Why is the system shaped this way? | [`PHILOSOPHY.md`](PHILOSOPHY.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`DESIGN.md`](DESIGN.md), and [`DECISIONS.md`](DECISIONS.md) | Prefer the narrower current authority and record a deliberate design change |
| What happened historically? | Dated files in [`research/`](research/) | Historical counts, paths, and provisional conclusions remain historical |
| How might future automated routing behave? | [`routing/`](routing/) | Nothing there executes, spawns, or grants authority |

When current runtime and human documentation diverge, do not quietly choose whichever is convenient. Confirm the live contract, correct both current surfaces, and preserve the reason in the decision register when the change is architectural.

## Current snapshot

- There are 32 runtime role TOMLs at the top level of `agents/`.
- `commander`, `lieutenant`, and `chief` are the only standing command ranks.
- `default` is the runtime-reserved omitted-role fallback, not a fourth rank.
- Specialists are distinguished by a recurring method, a canonical artifact or decision, a sharp ownership seam, and a safe authority posture.
- Shared `archivist` and `briefer` staff are conditional on a multi-workstream, long-running, unattended, or context-risky mission. `inspector` is added only when independent control-plane assurance is justified.
- The Beads continuity protocol applies only when an authorized workspace and named root record already exist. It is not implicit setup work.
- The task-router documents describe a recommendation-only future skill. No executable router skill has been installed.

The inventory and model/sandbox details can change. Reconcile this snapshot with the [manifest](ROLE_MANIFEST.md) and live TOMLs before editing.

## Directory map

```text
agents/
├── *.toml                         runtime-authoritative role definitions
└── meta/
    ├── README.md                  start-here map and authority ladder
    ├── ROLE_MANIFEST.md           canonical human inventory and routing contract
    ├── PHILOSOPHY.md              purpose, principles, and non-goals
    ├── ARCHITECTURE.md            components, flows, topology, and continuity
    ├── DESIGN.md                  taxonomy and role-contract design rules
    ├── DECISIONS.md               compact current decision register
    ├── EDITING.md                 change workflow and synchronization guide
    ├── VALIDATION.md              executable invariants and failure interpretation
    ├── ROLE_TEMPLATE.md           Markdown-safe role drafting skeleton
    ├── research/                  dated evidence and completed design records
    └── routing/                   non-runtime router contract and fixtures
```

Keep `agents/meta/` Markdown-only. Codex recursively discovers TOML files under `agents/`; a documentation or template TOML placed here can be mistaken for a loadable role.

## Document ownership

Each current document owns one recurring editor question:

- [`PHILOSOPHY.md`](PHILOSOPHY.md): why the system exists and which values resolve tradeoffs.
- [`ARCHITECTURE.md`](ARCHITECTURE.md): which components exist and how information and authority move through them.
- [`DESIGN.md`](DESIGN.md): how to decide whether a role should exist and how its contract should be shaped.
- [`DECISIONS.md`](DECISIONS.md): which cross-cutting choices are currently accepted and where their evidence lives.
- [`EDITING.md`](EDITING.md): how to make and hand off a change without damaging adjacent work.
- [`VALIDATION.md`](VALIDATION.md): which invariants must pass and what a failure means.
- [`ROLE_TEMPLATE.md`](ROLE_TEMPLATE.md): how to draft a candidate without creating an accidental runtime file.

Link to the canonical owner instead of copying its full content. The manifest remains the only current role-by-role inventory.

## Research and freshness

The durable research set currently includes:

- [Agent configuration audit](research/2026-08-05-agent-config-audit.md)
- [Specialist-gap audit](research/2026-08-05-specialist-gap-audit.md)
- [Specialist expansion decision record](research/2026-08-05-specialist-expansion-plan.md)
- [Documentation bootstrap decision record](research/2026-08-05-documentation-bootstrap-plan.md)

Research files are evidence, not live policy. Preserve their original observations and historical status notices. Update the current handbook and decision register when the accepted design changes; add a dated research record when the evidence or alternatives are substantial enough to aid a future editor.

## Safe editing rule

Start by inspecting the working tree and naming the exact files in scope. Preserve unrelated user-owned edits, keep changes unstaged unless James asks otherwise, and finish with the [validation contract](VALIDATION.md). A documentation cleanup must not silently broaden a role, change a model, alter sandbox posture, initialize external state, or turn a proposed router into executable authority.
