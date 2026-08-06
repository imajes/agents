# Agent documentation bootstrap decision record

> Historical completed phase. The [agent system handbook](../README.md), [live role manifest](../ROLE_MANIFEST.md), and top-level runtime TOMLs now define present behavior and navigation. This record preserves the scope, information architecture, and validation evidence for the documentation bootstrap.

Last updated: 2026-08-05 20:13:18 UTC

## Completion state

Complete. A durable bootstrap layer now explains why the agent roles exist, how runtime and human-readable authorities fit together, which cross-cutting decisions are current, how role boundaries are designed, and how a future editor can change and validate the system without replaying the originating thread.

The completed work is documentation and integration only. It does not initialize the future routing skill, change the accepted 32-role runtime inventory, stage files, create a commit, initialize Beads, or authorize any external action.

## Repository boundary

- Repository: `/Users/james/.codex`, branch `app/beta`, HEAD `3e589031e9079175f9338694a473cec0ca6839cc` during this phase.
- The existing 32-role specialist/continuity patch and `agents/meta` subtree remain unstaged and uncommitted.
- Unrelated user-owned changes in `.codex-global-state.json`, `config/config.toml`, `custom_instructions.md`, and `skills/.system/openai-docs/**` were preserved.
- Root `AGENTS.md` was zero bytes.
- No external setup or mutation was in scope.

## Final document set

| Document | Canonical responsibility |
| --- | --- |
| [`README.md`](../README.md) | Five-minute bootstrap, reading paths, authority ladder, current snapshot, directory map, and research lifecycle |
| [`PHILOSOPHY.md`](../PHILOSOPHY.md) | Purpose, principles, non-goals, tradeoffs, and quality test |
| [`ARCHITECTURE.md`](../ARCHITECTURE.md) | Components, discovery, prompt assembly, authority flow, command topology, task flow, swarm shapes, continuity, and change propagation |
| [`DESIGN.md`](../DESIGN.md) | Role admission, contract anatomy, artifact-first boundaries, overlap tests, model/sandbox/timeout rationale, and swarm design |
| [`DECISIONS.md`](../DECISIONS.md) | Stable current decision IDs, rationale, consequences, and evidence pointers |
| [`EDITING.md`](../EDITING.md) | Repository-safe workflow for local edits, additions, splits, merges, retirement, rename, research, review, and handoff |
| [`VALIDATION.md`](../VALIDATION.md) | Layered executable invariants, expected results, and failure interpretation |
| [`ROLE_TEMPLATE.md`](../ROLE_TEMPLATE.md) | Markdown-safe candidate worksheet, runtime skeleton, authoring prompts, forward tests, and materialization checklists |

The [role manifest](../ROLE_MANIFEST.md) remains the only current role-by-role human inventory. The synthesis documents link to it rather than duplicating 32 role descriptions.

## Information architecture decisions

1. Top-level `agents/*.toml` files remain runtime-authoritative.
2. `agents/meta/ROLE_MANIFEST.md` remains the canonical human taxonomy, routing contract, command topology, and continuity protocol.
3. The new handbook documents explain stable current design but do not override the runtime or manifest.
4. `research/` remains dated evidence. Historical counts, paths, provisional alternatives, and active-work statements do not silently become current policy.
5. `routing/` remains the design surface for a recommendation-only future skill and does not execute or grant delegation authority.
6. `agents/meta` remains Markdown-only because Codex recursively discovers TOML files beneath `agents/`.
7. One document owns each recurring editor question. Other documents link to that owner rather than copying full sections.
8. Every current synthesis file states its status, freshness date, and authority boundary.

## Design content preserved

The handbook captures the accepted system-level rationale without flattening historical evidence:

- roles are artifact- and decision-owner contracts rather than personality collections;
- mission authority is explicit, bounded, and non-transitive;
- the smallest capable primary owner is preferred;
- naval ranks remain exclusive to `commander`, `lieutenant`, and `chief`;
- the generalist backbone remains stable and specialists must pass a recurring-method/artifact/boundary test;
- runtime-injected root/child and mode guidance is not duplicated indiscriminately in role prompts;
- shared archivist/briefer continuity and independent inspection are conditional rather than mandatory;
- Beads continuity uses durable state plus live control only when an authorized workspace/root already exists;
- the future router recommends but never silently spawns or authorizes;
- the AI architecture evidence loop requires architect proposal, decision-owner acceptance, separately bounded execution, and return of evidence before full implementation.

These choices have stable `AGT-001` through `AGT-013` identifiers in the [decision register](../DECISIONS.md).

## Navigation repairs

- The manifest now links to the handbook, architecture, design, decisions, editing, and validation surfaces.
- The router specification and fixtures now point to current authorities and explicitly restate their non-executable posture.
- The completed specialist-expansion record now carries a historical-status notice and points to current authorities.
- The earlier configuration audit and specialist-gap records already carry historical notices.
- The root repository README points to top-level `agents/*.toml` and `agents/meta/` rather than the obsolete nested agent-config layout.

## Validation evidence

Validation completed against the live working tree:

1. `taplo check agents/*.toml` passed for all 32 runtime TOMLs.
2. All 32 runtime IDs are unique and match their filename; all 32 descriptions are unique; required fields are present and nonblank; timeout and nickname constraints pass.
3. The live model split is 27 Sol and 5 Terra roles. Effort counts are 1 low, 1 medium, 4 high, 13 XHigh, 10 Max, and 3 Ultra.
4. The Ultra set is exactly `chief`, `commander`, and `lieutenant`.
5. The read-only set is exactly `ai_architect`, `analyst`, `critic`, `researcher`, `reviewer`, `scout`, `security_engineer`, `venture_analyst`, and `watchkeeper`.
6. The dynamic runtime inventory and 32-row manifest inventory match exactly.
7. `agents/meta` contains only Markdown, contains no nested TOML, and its current authority files are not ignored.
8. All three embedded JSON protocol examples in the manifest parse.
9. All 15 Markdown files under `agents/meta` passed relative file and heading-anchor resolution, duplicate-heading, balanced-fence, table-width, final-newline, and trailing-whitespace checks.
10. Live runtime TOMLs contain none of the retired backticked role IDs. Current synthesis contains no stale `config/agents` or former live manifest path.
11. `git diff --check -- agents README.md` passed, including the tracked portion; explicit scans covered untracked Markdown.
12. Ordinary and `--strict-config` Codex Doctor both reported `Configuration [ok] config loaded` with no agent-config startup warning.
13. Doctor's overall exit remained nonzero only because the noninteractive environment reports `TERM=dumb` as a failure and the pre-existing rollout/state scan discrepancy as a warning.
14. No agent, handbook, or root README change is staged.

## Final handoff

The documentation bootstrap is complete and there is no remaining implementation work in this phase. The next distinct optional phase is still the executable recommendation-only routing skill, after James accepts or revises its installation root and forward fixtures. That phase must use the canonical skill-creator workflow and is not implied by this record.
