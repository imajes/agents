# Scope, assumptions, decisions and questions

This document records product interpretation; Beads owns execution tracking in the Veracity repository under `veracity-6gm`. The old reboot graph is historical context and does not override this request.

## User constraints

| ID | Constraint | Source |
|---|---|---|
| U01 | Extract actionable contract behaviors into skills callable at will, including at the start of a conversation. | 30 October implementation request. |
| U02 | Build under `~/.agents` inside the existing personal marketplace. | Same request. |
| U03 | First pass is stubs and product skeleton, to review the surface before implementing any action. | Subsequent correction. |
| U04 | Cover all actions, not just tangents. | Explicit clarification. |
| U05 | Treat historical repo/contract material as reference; preserve original ideas and project context when designing persistence. | Earlier task instructions and persistence clarification. |

## Decisions for this skeleton

| ID | Decision | Rationale and limit |
|---|---|---|
| D01 | Name the package `veracity-actions`; label version and UI as a skeleton. | Existing `veracity` points at a legacy alpha. Preserve that entry and make this new surface identifiable. Naming remains reviewable. |
| D02 | Sixteen focused entries in four groups. | Makes the whole action surface visible. This is proposed granularity, not approval for sixteen implementations. |
| D03 | Explicit invocation only, with preview behavior in every stub. | The user asked to invoke controls at will; the latest scope prohibits implementing them now. No global prompt loader. |
| D04 | Document shared capabilities rather than create placeholder servers or persistence code. | Makes dependencies reviewable without fake functionality or premature runtime choices. |
| D05 | Package in the incubator first, validate, then copy the qualified skeleton into the marketplace plugin directory. | Honors the local skill-development convention. This is skeleton qualification, not promotion into user-wide working skills. |
| D06 | Use the portable root manifest and OpenAI metadata extension. | Current official packaging guidance; no MCP, hooks, apps, or install-time actions are declared. |
| D07 | Keep behavioral intentions, presentation profiles and action workflows distinguishable. | No claim that an opt-in skill guarantees general reasoning, tone, or adherence. |
| D08 | Adapt single-label message classification to segment-level handling. | Compound requests can include a correction, tangent and explicit pivot; preserve all user intent. |
| D09 | Preserve accepted/proposed and inspect/execute distinctions. | A stored next action or recommendation does not create current mutation authority. |
| D10 | Keep initiative bootstrapping and autonomous research outside this contract-action extraction. | They belong to the wider product discussion; capturing an idea does not commit to either. |
| D11 | Do not install/enable the package, restart the host, or change its configuration in this pass. | The requested result is a marketplace skeleton for assessment. Marketplace registration is distinct from host activation. |

## Working assumptions

| ID | Assumption | Consequence if changed |
|---|---|---|
| A01 | Separating these sixteen actions will make missing or overlapping responsibilities easier to spot. | Consolidate or split entries before implementation. |
| A02 | The current local v2.1.12 contract is the correct source for extraction. | Reconcile another source version using the recorded section map and digest. |
| A03 | A Markdown-first package surface is sufficient for this skeleton review. | Add a rendered view later if it materially improves assessment; use Karla for body text. |
| A04 | The existing marketplace root remains the home directory. | Re-resolve the catalog and adjust only the new entry’s source path if host discovery changes. |

## Open product questions

These are design choices for review, not blockers or a request to answer sixteen questions now. Each also appears beside the relevant stub.

| ID | Surface | Question |
|---|---|---|
| Q01 | `focus` | Should focus and tangents remain separate controls, or should selecting tangents also establish a minimal direction card? |
| Q02 | `tangents` | Which context is essential for a faithful capture, and should the inline receipt always include the durable ID? |
| Q03 | `explore` | Is an assistant-turn budget the right default, and how should nesting or an interrupted exploration work? |
| Q04 | `checkpoint` | Which state deserves capture at each material change, and which parts can remain links to existing Beads records? |
| Q05 | `recover` | Should read-only recovery and writer-acquiring resume be separate skills or clearly separated modes? |
| Q06 | `fork` | Which state should the child inherit by reference, and which state should be copied as a snapshot? |
| Q07 | `handoff` | What is the smallest safe transfer protocol that preserves a usable source until target acceptance? |
| Q08 | `promote` | Should promoting a tangent mean linking a project idea, accepting a project fact, or offering those as different destinations? |
| Q09 | `memory` | Is this best retained as a skill, or should Veracity only route explicit requests to the host’s memory tool? |
| Q10 | `assumptions` | Should assumption history live alongside workstream checkpoints or in a shared evidence register? |
| Q11 | `verify` | Should verification produce a separate evidence review, inline annotations, or a user-selected combination? |
| Q12 | `decide` | Should accepted decision capture be a mode here or a separate action later? |
| Q13 | `diagnose` | Is this distinct enough from verify to earn a separate invocation, given its causal-test workflow? |
| Q14 | `artifacts` | Should targeted editing and copy-safe delivery be separate skills, or modes of this one? |
| Q15 | `audit` | Which review checks provide useful signal without recreating a large mandatory response wrapper? |
| Q16 | `contract-check` | Should this diagnostic ship with the user-facing bundle or remain an authoring-only skill? |

## Remaining uncertainty

The structure can be checked locally; real picker visibility, model activation behavior, ongoing conversation adherence, and cross-surface availability require host/user trials. No persistence, concurrency, data migration, offline worker, or time-management efficacy is claimed by this skeleton.
