# Contract actions and behavioral intentions

This is a **design extraction**, not a contract loader. Every labeled requirement section in the current source has a disposition below, including the whole pre-send Module G. The command table separately accounts for every explicit command in D6. Purpose and precedence prose informs the design but does not grant instruction authority.

An **action** has a recognizable trigger, bounded scope, and inspectable result: capture an idea, save a checkpoint, reconcile a revision, check evidence, prepare a patch. A **behavioral intention** describes how collaboration should feel or reason: candor, peer-level altitude, pragmatism, constructive skepticism, concise writing. Intentions shape the workflows but are not packaged as independent always-on instructions.

A **supporting capability** supplies state or mechanics shared by several actions. A **presentation choice** controls how results appear. Neither becomes a user-facing skill merely because it appears in the contract.

| Source section | Disposition | Skill surface | Reason or adaptation |
|---|---|---|---|
| 0.1 | intention + actions | [`verify`](../skills/verify/SKILL.md), [`assumptions`](../skills/assumptions/SKILL.md), [`audit`](../skills/audit/SKILL.md) | Truthfulness is a general obligation; verification, premise tracking and claim review are explicit jobs. |
| 0.2 | intention + actions | [`focus`](../skills/focus/SKILL.md), [`decide`](../skills/decide/SKILL.md), [`diagnose`](../skills/diagnose/SKILL.md) | Pragmatism informs recommendations; direction, decisions and discriminating checks have inspectable outputs. |
| 0.3 | intention + actions | [`tangents`](../skills/tangents/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md), [`recover`](../skills/recover/SKILL.md), [`memory`](../skills/memory/SKILL.md), [`promote`](../skills/promote/SKILL.md) | Continuity becomes capture/recovery/promotion actions. Personal memory requires an explicit request in this design. |
| 0.4 | intention + actions | [`verify`](../skills/verify/SKILL.md), [`decide`](../skills/decide/SKILL.md), [`diagnose`](../skills/diagnose/SKILL.md), [`audit`](../skills/audit/SKILL.md) | Constructive skepticism is a stance; source checks, decisions and diagnostics are concrete workflows. |
| A1 | diagnostic adaptation | [`contract-check`](../skills/contract-check/SKILL.md) | Inspect source completeness and identity on request. Do not inherit remote-source authority or load-all behavior. |
| A1.1 | experimental diagnostic | [`contract-check`](../skills/contract-check/SKILL.md) | Retain receipt inspection only as an optional historical experiment; no mandatory rolling receipt. |
| A2 | presentation intention + diagnostic | [`contract-check`](../skills/contract-check/SKILL.md), [`audit`](../skills/audit/SKILL.md) | Canary appearance may be inspected; no mandatory first-line wrapper or proof of comprehension. |
| A2.1 | communication intention + actions | [`focus`](../skills/focus/SKILL.md), [`audit`](../skills/audit/SKILL.md) | Useful progress reporting and material blockers belong to active workflows. No universal major/progress output grammar. |
| A2.2 | presentation intention | No standalone skill | Stable visual semantics remain a design intention; no standalone formatting skill or forced glyph profile. |
| A2.3 | diagnostic adaptation | [`contract-check`](../skills/contract-check/SKILL.md) | Registry verification and exact-render checks are opt-in diagnostics. |
| A3 | action | [`audit`](../skills/audit/SKILL.md) | Requested pillar/exception reviews are observable reviews, not permanent self-certification. |
| A4 | actions | [`recover`](../skills/recover/SKILL.md), [`audit`](../skills/audit/SKILL.md), [`contract-check`](../skills/contract-check/SKILL.md) | Recover workstream state and diagnose integrity failures; do not activate the whole contract. |
| B1 | intention + action | [`audit`](../skills/audit/SKILL.md) | Honest action reporting is foundational; an audit can compare claims with evidence. |
| B2 | actions + presentation intention | [`verify`](../skills/verify/SKILL.md), [`assumptions`](../skills/assumptions/SKILL.md), [`artifacts`](../skills/artifacts/SKILL.md) | Classify/verify material claims and protect payloads. Exact glyphs and confidence tails are optional presentation choices. |
| B3 | action | [`assumptions`](../skills/assumptions/SKILL.md) | Track material premises, validation paths and status; risk modes do not grant new authority. |
| B4 | action | [`verify`](../skills/verify/SKILL.md) | Check current facts or state the gap and validation path. |
| C1 | behavioral intention | No standalone skill | Peer-level communication is a preference, not a tool workflow. |
| C2 | behavioral intention | No standalone skill | Answer-first writing and concise structure are output preferences. |
| C3 | intention + actions | [`decide`](../skills/decide/SKILL.md), [`assumptions`](../skills/assumptions/SKILL.md) | Ask only useful questions; make decision hinges and load-bearing assumptions explicit. |
| C4 | action + intention | [`decide`](../skills/decide/SKILL.md), [`diagnose`](../skills/diagnose/SKILL.md) | Tradeoff analysis, recommendations and root-cause work have separate outcomes. |
| C5 | behavioral intention + action | [`decide`](../skills/decide/SKILL.md), [`verify`](../skills/verify/SKILL.md) | Constructive challenge informs explicit decision and evidence reviews; no performative-pushback skill. |
| C6 | behavioral intention + action | [`decide`](../skills/decide/SKILL.md) | Consider people and consequences when material to an actual decision. |
| C7 | communication intention + action | [`focus`](../skills/focus/SKILL.md) | Report meaningful progress during active work; no promised background operation. |
| D1 | action | [`focus`](../skills/focus/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md), [`recover`](../skills/recover/SKILL.md) | Establish/recover direction and stable workstream identity. |
| D2 | view + actions | [`focus`](../skills/focus/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md) | Expose current direction/state when useful; do not mandate a canary table on every answer. |
| D3 | action | [`focus`](../skills/focus/SKILL.md), [`tangents`](../skills/tangents/SKILL.md) | Classify message segments; protect explicit user pivots, corrections and necessary dependencies. |
| D4 | action | [`tangents`](../skills/tangents/SKILL.md) | Capture before optional exploration, report the real outcome, and return to focus. |
| D5 | action | [`focus`](../skills/focus/SKILL.md) | Resolve only the necessary dependency and reconnect it to focus. |
| D6 | command surface | [`focus`](../skills/focus/SKILL.md), [`tangents`](../skills/tangents/SKILL.md), [`explore`](../skills/explore/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md), [`recover`](../skills/recover/SKILL.md), [`fork`](../skills/fork/SKILL.md), [`handoff`](../skills/handoff/SKILL.md), [`promote`](../skills/promote/SKILL.md) | Every named command has a home in the command map; natural language remains valid. |
| D7 | action + intention | [`focus`](../skills/focus/SKILL.md), [`audit`](../skills/audit/SKILL.md) | Inspect progress/stalls; analysis advancing the user’s actual request counts. No automatic implementation from a review request. |
| D8 | action + view | [`tangents`](../skills/tangents/SKILL.md) | Maintain the ledger, dispositions and deliberate review triggers. |
| D9 | view + review action | [`focus`](../skills/focus/SKILL.md), [`audit`](../skills/audit/SKILL.md) | Expose meaningful drift/pivot exceptions; no obligatory footer. |
| E1 | support + actions | [`checkpoint`](../skills/checkpoint/SKILL.md), [`recover`](../skills/recover/SKILL.md), [`fork`](../skills/fork/SKILL.md), [`promote`](../skills/promote/SKILL.md), [`memory`](../skills/memory/SKILL.md) | Keep workstream, project and personal scopes distinct; ideas have their own domain. |
| E2 | support + action | [`checkpoint`](../skills/checkpoint/SKILL.md) | Define identity, ancestry, revisions and state; no runtime schema frozen in this skeleton. |
| E3 | support + actions | [`checkpoint`](../skills/checkpoint/SKILL.md), [`handoff`](../skills/handoff/SKILL.md) | Choose available adapters and accurately distinguish persistence/reach. |
| E4 | action | [`checkpoint`](../skills/checkpoint/SKILL.md) | Persist/verify material changes or emit an honestly unsaved portable checkpoint. |
| E5 | action | [`recover`](../skills/recover/SKILL.md) | Discover/reconcile surviving state before asking the user to reconstruct it. |
| E6 | actions + support | [`recover`](../skills/recover/SKILL.md), [`fork`](../skills/fork/SKILL.md), [`handoff`](../skills/handoff/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md) | Ownership, forks and expected-revision checks require a real state mechanism. |
| E7 | actions + support | [`recover`](../skills/recover/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md), [`promote`](../skills/promote/SKILL.md) | Discover via indexes of pointers; explicitly merge accepted knowledge into project scope. |
| E8 | actions + support | [`memory`](../skills/memory/SKILL.md), [`checkpoint`](../skills/checkpoint/SKILL.md), [`handoff`](../skills/handoff/SKILL.md), [`recover`](../skills/recover/SKILL.md) | Use explicit best-effort pointers, portable handoffs and verified imports; surface access limits. |
| F1 | action + intention | [`diagnose`](../skills/diagnose/SKILL.md) | Observe, hypothesize, test, conclude; distinguish diagnosis from fixing. |
| F2 | action + intention | [`verify`](../skills/verify/SKILL.md) | Gather current primary evidence and preserve disagreement and inference boundaries. |
| F3 | action | [`artifacts`](../skills/artifacts/SKILL.md) | Inspect current state, patch deliberately, and distinguish proposed/applied edits. |
| F4 | action + output intention | [`artifacts`](../skills/artifacts/SKILL.md) | Produce/review clean reusable payloads with separate explanatory material. |
| G | review action + support constraints | [`audit`](../skills/audit/SKILL.md), [`artifacts`](../skills/artifacts/SKILL.md), [`contract-check`](../skills/contract-check/SKILL.md) | Inspect applicable claims, state, rendering and payload invariants on request. No universal pre-send enforcement hook. |

## Explicit command coverage

These are proposed modes inside the named skills, not a registered parser or shell commands. Natural-language instructions remain valid. `RESUME` means returning from exploration; `RESUME WORKSTREAM` means recovering a specific durable workstream and explicitly resolving writer ownership.

| Contract command | Skill |
|---|---|
| `PIVOT` | [`focus`](../skills/focus/SKILL.md) |
| `NEW OBJECTIVE` | [`focus`](../skills/focus/SKILL.md) |
| `EXPLORE 1 / EXPLORE N` | [`explore`](../skills/explore/SKILL.md) |
| `PARK` | [`tangents`](../skills/tangents/SKILL.md) |
| `RESUME (prior focus)` | [`explore`](../skills/explore/SKILL.md) |
| `LEDGER` | [`tangents`](../skills/tangents/SKILL.md) |
| `STATE` | [`focus`](../skills/focus/SKILL.md) |
| `CHECKPOINT` | [`checkpoint`](../skills/checkpoint/SKILL.md) |
| `RESUME WORKSTREAM` | [`recover`](../skills/recover/SKILL.md) |
| `FORK WORKSTREAM` | [`fork`](../skills/fork/SKILL.md) |
| `HANDOFF` | [`handoff`](../skills/handoff/SKILL.md) |
| `PROMOTE ... TO PROJECT` | [`promote`](../skills/promote/SKILL.md) |
| `LOCK FOCUS` | [`focus`](../skills/focus/SKILL.md) |
| `UNLOCK FOCUS` | [`focus`](../skills/focus/SKILL.md) |

## Related operations without a separate skill

- Thread/project/general idea filtering, tangent disposition, revisit triggers and inline receipts belong to **tangents**.
- Progress notes, state views, dependency handling, drift review and intentional pivots belong to **focus**, with **audit** for a requested inspection.
- Expected-revision writes and a project index of state pointers support **checkpoint** and **recover**; they are not additional conversation controls.
- Writer acquisition, release and acceptance support **recover**, **fork** and **handoff**.
- Explicit source/version/registry inspection belongs to **contract-check**. Mandatory canaries and rolling receipts do not become a global bootstrap.
- Copy-safe exclusions and current-state editing belong to **artifacts**; optional claim annotation belongs to **verify**.
- Stable preference requests belong to **memory**. Durable task commitments remain in Beads where available.

## Deliberately outside this contract-action skeleton

Project bootstrapping (Chat/Work/Code folders, Git and Beads initialization), autonomous idea research, calendar management, reminders, scheduler operation and new-agent creation appeared in the broader product discussion or could support future workflows. They are **not implemented or silently added as contract-derived skills here**. Tangent records should remain usable by future research workers, but that does not authorize running one. These extension surfaces can be assessed separately after the contract actions are reviewed.

## Source identity

- File inspected: `/Users/james/.agents/operating-contract/v2/OPERATING_CONTRACT.md`.
- Version: 2.1.12; SHA-256: `067a6917c2cd75c906bd279f15662519c22ea5af3b25dbd2eef90f4547d466f9`.
- Source role: historical/reference material only.
- Current scope: user-requested skeleton for all actionable contract behaviors, 30 October 2026.
- Machine-readable companion: [catalog.json](../catalog.json). It is a design index, not executable tooling or task tracking.
