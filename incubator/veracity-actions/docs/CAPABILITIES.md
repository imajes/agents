# Supporting capabilities — contracts only

**None of these capabilities is implemented by this package.** The identifiers below are design vocabulary used in [catalog.json](../catalog.json), not MCP tool names, endpoints, scripts, or dependency declarations. Existing host tools may eventually satisfy some of them; others need a deliberate implementation.

| Capability | Responsibility | Minimum intended contract |
|---|---|---|
| `direction` | Conversation direction and exploration state | Objective/focus/done/next, lock mode, return point, budget, and explicit user changes. Session-scoped; no global interception. |
| `ideas` | Faithful idea capture and contextual views | Original wording plus source context; separate summaries and classifications; stable IDs; thread/project/general associations; relationships, revisit triggers and disposition history. Proposed central location: ~/.agents/ideas, not created. |
| `workstreams` | Revisioned workstream state and discovery | Stable identity, source location, writer binding, expected revision, snapshots/history, and a project index of pointers. Refer to Beads commitments rather than duplicate them. |
| `ownership` | Writer ownership and transfer | Explicit acquire, release, fork ancestry, and handoff acceptance. Check-and-write atomically; detect stale revisions and preserve a recoverable source on failure. |
| `promotion` | Project knowledge promotion | Select accepted items; inspect destination scope and revision; merge or surface conflicts; retain origin and independently revision shared state. |
| `memory` | Native personal-memory adapter | Use the host’s supported explicit remember/update/forget mechanism. Record actual results and limits; no universal memory backend is selected. |
| `evidence` | Evidence, assumptions, and decisions | Keep original source, interpretation, claim status, assumptions, accepted/proposed decisions, uncertainty, and validation history distinguishable. |
| `sources` | Current source and artifact access | Use available primary-source/browser/file tools; record source identity, time/version, completeness and failures. No tool interface is assumed universally available. |
| `artifacts` | Current artifact reads, patches, and validation | Read latest state; preserve unrelated changes; preview/apply distinct operations; keep payloads clean; invoke existing format-specific tools when available. |
| `export` | Portable checkpoint and handoff | Readable Markdown plus lossless structured state, provenance and unknown-field preservation. Rendering, local saving, delivery, and target import are separate outcomes. |
| `reporting` | Visible action and control receipts | Compact capture, state, progress and exception views derived from actual outcomes. An intended action, failed write, successful write, read-back, backup, and cross-surface reach are different claims. |
| `integrity` | Source and registry diagnostics | Byte-complete reads, hashes, schema/version checks and exact Unicode rendering when specifically requested. No response canary proves semantic adherence. |

## State domains to keep separate

| Domain | Intended content | Boundary |
|---|---|---|
| Ideas/tangents | Faithful captures, contextual relationships, annotations and dispositions | An idea can be general, project-specific, or associated with several contexts. Capture is not task creation. |
| Workstream state | Direction, next action, controls, writer, revision and recovery references | One workstream has a stable identity; several chats do not share a generic current-state file. |
| Project knowledge | Explicitly accepted shared facts, decisions, constraints and artifact pointers | Promotion is deliberate and retains provenance. |
| Personal memory | Explicit stable preferences and necessary recovery pointers | Host-native best-effort behavior is not exact state storage. |
| Execution commitments | Tasks, dependencies, owners and completion evidence | Beads remains the tracker where available; this package does not invent a second task ledger. |

The eventual idea store should preserve original wording and the context available at capture time. Summaries, classifications, research, dispositions and commitments must remain separately attributable. “Lossless” here is an intended information-preservation property, not a claim that a stub already records complete conversations. Minimum capture context and export behavior remain open design questions.

## Observable operation boundaries

Each future mutating operation should distinguish its requested action, source identity/revision, destination/scope, actual result, and verification result. Retries must not duplicate a capture or silently overwrite newer state. Reads should not initialize records. Failures should leave recoverable data and a truthful unsaved/pending/conflicted status.

These are capability requirements to evaluate later, not a frozen API, database schema, ownership algorithm, or implementation plan. In particular, no dummy success response, no-op storage method, fake MCP server or empty hook is shipped.

## Harness reach

Skills can describe workflows across Codex and ChatGPT, but file access, memory, scheduling, writer coordination and available connectors differ. A future adapter must discover its actual capabilities and report unavailable actions. This local package does not make `~/.agents` available to ChatGPT web and does not prove any tunnel or server integration.
