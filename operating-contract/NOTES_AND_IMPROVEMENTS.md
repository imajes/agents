<!-- markdownlint-disable-file MD013 -->

# Notes and Improvements for the Operating Contract

This document is a companion note to `CONTRACT.md`. It records the major design issues, decisions, and improvement directions discussed while shaping **James x AI Assistants: Operating Contract**.

It is **not** the operating contract itself. The source of truth remains:

```text
https://raw.githubusercontent.com/imajes/agents/refs/heads/main/operating-contract/CONTRACT.md
```

The purpose of this file is to preserve the reasoning behind the contract so future revisions can avoid re-litigating the same issues or accidentally weakening the contract’s intent.

---

## 1. Context and goal

The original goal was to extract a durable operating contract from scattered saved memories, formalize it into a reusable document, and store it somewhere globally accessible to future assistant sessions and peer agents.

The working design evolved into:

- a canonical Markdown contract stored in GitHub;
- saved memory as a bootstrap pointer only, not a source of truth;
- raw GitHub URL retrieval as the preferred source-loading path;
- visible canary/audit behavior to detect context loss, drift, and contract non-adherence;
- a distinction between high-level operating contract material and lower-level saved-memory ground rules.

---

## 2. Core purpose of the contract

The contract is intended to govern ordinary assistant behavior with James, not merely contract-related conversations. It exists to make assistant behavior more trustworthy, inspectable, pragmatic, continuous, and skeptically grounded.

The core pillars are:

- 🧱 **Absolute truthfulness**
- 🛠️ **Effectual pragmatism**
- 🧭 **Grounded continuity**
- 🔎 **Healthy skepticism**

The contract should act as a durable behavior spec, not a decorative style guide.

---

## 3. Major architectural decisions

| Area | Decision | Rationale |
|---|---|---|
| Canonical source | Store the contract as Markdown in GitHub. | GitHub provides version history, diffs, rollback, portability, and reviewability. |
| Bootstrap memory | Saved memory should point to the raw URL, not contain the contract body. | Memory is compact, mutable, and not suited to large exact documents. |
| Raw URL | Use the raw GitHub URL directly rather than connector-specific repo/path references. | Raw URL retrieval is more portable across assistants and avoids connector assumptions. |
| Contract loading | The contract should be loaded at conversation startup before substantive work. | Waiting until a contract-specific topic appears fails, because the contract governs all interaction behavior. |
| Hooks/canaries | Visible hooks should serve as context/adherence canaries and status surfaces. | If hooks disappear or degrade, that signals possible context loss or instruction failure. |
| Objective vs Focus | Objective is the stable higher-level destination; Focus is the current immediate step. | This prevents the assistant from redefining the mission every turn while still tracking local work. |
| Ground rules | Language, technical correctness, command/editing safety, and personal continuity belong in saved memory ground rules, not the main contract. | These are important but lower-level than the main operating contract and would dilute its purpose. |

---

## 4. Audit ledger and responses

This table summarizes the deep-audit issues raised during review and James’s responses or resulting decisions.

| ID | Topic | Finding / concern | James’s response / decision | Resulting direction |
|---:|---|---|---|---|
| AC-01 | Precedence model | The contract lacked a conflict-resolution order. | Agreed, but rejected placing platform/safety as the document’s own precedence item; those are external constraints. Also questioned whether technical correctness always outranks goal/pragmatism. | Add internal contract precedence focused on 🧱 **Absolute truthfulness**, Objective/Focus, 🛠️ **Effectual pragmatism**, 🧭 **Grounded continuity**, 🔎 **Healthy skepticism**, then style. |
| AC-02 | Audit hook weight | Mandatory audit risks overhead. | Accepted the concern but emphasized that inspectability matters more than reducing chrome. Hidden assumptions are the real failure mode. | Keep audit behavior, but make it more meaningful: expose load-bearing basis, assumptions, interpretation, limits, and confidence scope. |
| AC-03 | Audit examples / D3-D4 overlap | The audit schema needed examples and D3/D4 overlap was unclear. | Examples are useful; D3/D4 should be reviewed around Objective/Focus/pivot behavior. | Audit hook now uses status lines plus a details table. Further refinement should continue around verification surfaces. |
| AC-04 | Stale Goal1 reference | `Goal1` remained after renaming to Objective/Focus. | Agreed; also signaled need for a final structural polish pass. | Fixed stale reference and renamed model to Objective/Focus. |
| AC-05 | 0.3 / D5 overlap | Grounded continuity and Tangent Ledger mechanics overlapped. | Concerned about overreach and noted the Tangent Ledger had not actually been used; biased toward preserving more information rather than less. | Retain capture bias, but clarify promotion/review mechanics. Prefer preserving context and then editing/reframing over losing it. |
| AC-06 | Assumption Ledger visibility | Visible assumptions could be noisy. | Strongly emphasized that hidden assumptions cannot be validated. Need a real inspectability mechanism, not a hidden ledger. | Surface load-bearing assumptions that materially affect recommendations, conclusions, edits, commands, or next actions. |
| AC-07 | Saved memory ground rules note | Contract note omitted some saved-memory ground rules. | Did not think technical correctness or command safety needed explicit reference in the contract. | Later pared the note down; saved memories are trusted to carry those ground rules unless proven otherwise. |
| AC-08 | Shared doc state unavailable | What if current canvas/doc state is unavailable? | Workarounds without approval are unacceptable. If the document state is unavailable, say so. | Add failure behavior: state limitation plainly; do not infer from stale text; do not whole-document rewrite or invent workarounds without approval. |
| AC-09 | Hook modes / response weight | Hook chrome may be heavy. | James is usually working, not casually chatting; hook weight is acceptable if it improves trust. Context-window cost would be worth considering if real. | Do not frame hooks as busywork. Treat them as canary/status surfaces. |
| AC-10 | Session definition | “Session” was ambiguous. | Agreed. | Define first substantive response, reset, paused workstream return, milestones, and long multi-turn work as triggers. |
| AC-11 | Long back-and-forth wording | Wording was awkward. | Fine. | Use clearer language for long multi-turn work. |
| AC-12 | Check-in cadence | Periodic cadence too vague. | Cadence suggestions sensible; include returning to paused conversations. | Add cadence triggers: first substantive response, reset, paused workstream, milestones, 5–8 substantive turns, reprint triggers. |
| AC-13 | Confidence calibration | Confidence labels needed calibration. | Agreed. | Add High/Medium/Low/Mixed/Unknown calibration and scope confidence. |
| AC-14 | Mixed confidence | Need mixed state. | Agreed. | Add `Mixed` confidence where confidence varies across key claims. |
| AC-15 | Collapsible sections | Unsupported syntax risk. | Remove; earlier line was added without answering capability. | Remove reliance on collapsible sections. |
| AC-16 | “Boilerplate wrappers” language | Weakens hook importance. | Agreed, but earlier replacement was too convoluted. | Use “visible response framing” instead. |
| AC-17 | Canary/audit lapse recovery | Missing recovery path. | Agreed; recovery should acknowledge lapse, restate status/environment knowledge, and offer fresh-session rollup. | Add canary/audit lapse recovery steps. |
| AC-18 | Irrefutable freshness | Re-review rule may be too strong. | Keep high standard. Either the snapshot is fresh or it is not; weak theater is worse than refusal. | Keep strong freshness requirement; add examples such as current canvas payload, pasted current text, checksums. |
| AC-19 | Risk mode transitions | Strict/Explore/Speculative need transition language. | Agreed; use contextual phrases rather than hard permission gates. | Add phrasing: “Strictly speaking…”, “As I explore this…”, “If I were to speculate…”. |
| AC-20 | Explore assumption limit | Three assumptions may be too tight. | Fine; needs guideline/guardrail balance. | Use ≤3 active material assumptions by default, expandable when the task benefits or James opts in. |
| AC-21 | Platform exceptions | Platform-forced hook exceptions are unclear. | Concerned about hidden exception surfaces; prefer not skipping if avoidable. | Limit hook omissions only to cases where platform/tool technically prevents textual response. |
| AC-22 | “Glazing” wording | Could be slangy. | Keep “glazing” because it captures the affect, but add explanatory phrasing. | Keep term with context: “excessive praise / performative affirmation.” |
| AC-23 | Wide Markdown | Minor nit. | Fine. | Clarify readable markdown and ~120-char width for code/docs when appropriate. |
| AC-24 | Clarifying questions first | Could slow progress. | Rejected change. | Do not weaken this without further discussion. |
| AC-25 | EQ lens tie-in | Should connect to pillars. | Agreed. | Tie EQ/human-systems lens to 🧭 **Grounded continuity** and 🔎 **Healthy skepticism**. |
| AC-26 | “2 turns” definition | Subjective / weak. | Wants tighter relation to measurable progress between user turns and original goal. | Rework D1 around progress toward Objective/Focus; if no measurable progress, reset. |
| AC-27 | Measurable progress examples | Suggested adding more progress types. | Rejected broadening that hides drift. The point is not useful activity; it is progress toward original/stated goal, especially to counter ADHD rabbit holes. | Define measurable progress as progress toward Objective/Focus, not merely useful activity. |
| AC-28 | Objective lifecycle | Unsure. | Objective should be stable and higher-level, not a turn-by-turn step. | Explicitly define Objective as stable across ordinary turns; Focus carries the current step. |
| AC-29 | Focus repair phrase | Add explicit phrase. | Agreed. | Add `🔦 Focus repaired: returning to ...`. |
| AC-30 | Timeboxed mini-answer | Needs concrete reset behavior. | Accepted but objected to safety/accuracy phrasing; wants quick reset and callback to original objective. | Define ≤1 short paragraph or ≤3 bullets and end with callback to Objective/Focus. |
| AC-35 | Technical correctness in purpose | Minor accepted item. | OK to action. | Technical correctness remains mentioned but not overemphasized. |
| AC-36 | “yolo’ing” | Informal. | OK to action. | Replace with “recklessly inventing assumptions.” |
| AC-38 | Distinct bucket | Should reference Tangent Ledger. | OK to action. | Use Tangent Ledger or another explicit holding area. |
| AC-39 | Odd spaces | Formatting cleanup. | OK to action. | Normalize spacing around check-in bullets. |
| AC-40 | Evidence vs Basis | Table heading could improve. | OK to action. | Use `Basis` in audit details table. |
| AC-41 | Rabbit hole term | Maybe define. | OK to action. | Keep as useful term; can define further later if needed. |
| AC-43 | Canonical audit example | Add example. | OK to action. | Add canonical tiny-answer and document-edit examples / improve audit structure. |
| AC-44 | Ledger lifecycle | Assumption/Tangent ledgers should share fields. | OK to action. | Add clearer fields to both ledgers. |

---

## 5. Important correction about “minimum viable compliance”

A proposed “minimum viable compliance” rule was rejected in spirit. The phrase sounded like the assistant was trying to reduce or avoid the work required to be inspectable.

The corrected principle is not “do as little audit as possible.” It is:

> Expose the load-bearing assumptions, basis, interpretation, drift, and status needed for James to verify the work, especially when the assistant is highly confident.

The point of the audit hook is to counter two model failure modes:

1. The assistant does not reliably know its own limitations or the reliability of its sources, assumptions, and tool outputs.
2. The assistant often states things with excessive confidence even when its premises are stale, invalid, hidden, or weak.

Therefore, confidence labels are not sufficient. The audit must make the basis and assumptions inspectable.

---

## 6. Bootstrap memory wording that James settled on

James edited the startup memory into a cleaner, self-contained form. This version is better than the earlier assistant-generated attempts because it reads like a startup instruction to a future assistant, not a note about a prior conversation.

```md
***IMPORTANT: For every new conversation with James, load the current assistant operating contract before doing substantive work.***

Immediately fetch the canonical contract directly from: https://raw.githubusercontent.com/imajes/agents/refs/heads/main/operating-contract/CONTRACT.md

Use the fetched document as the active operating contract for the conversation:

  - It governs how responses should be structured;
  - how uncertainty should be surfaced;
  - how Objective/Focus should be handled;
  - how drift/pivot behavior should work, and
  - how the assistant should collaborate with James generally.

Notes:

  - Do not rely on a cached copy, saved memory summary, prior conversation state, canvas state, repo path, or connector-backed GitHub state as a substitute for the freshly fetched raw document.
  - If cache control is available, request a fresh copy. Otherwise, append a cache-busting query string such as `?v=<current-UTC-timestamp>`.
  - Do not let the contract silently fall out of active context.
  - In long conversations, after pauses, after resets, or when behavior suggests the contract may no longer be active, re-fetch & re-anchor on the document.
  - If the document cannot be fetched at all or freshly requested, say so plainly before proceeding. Ask James whether to paste the current contract or continue with limited context.
  - Saved memory is only the bootstrap instruction that points to the contract.
  - The raw GitHub document is the source of truth.
```

Note: if future editors prefer stricter Markdown style, `re-fetch & re-anchor` may be changed to `re-fetch and re-anchor`, but the user-authored version above should be preserved unless intentionally revised.

---

## 7. Failures observed during the design process

These are not merely conversational hiccups; they are evidence for why the contract exists.

| Failure | What happened | Lesson |
|---|---|---|
| Fast shallow review | The assistant produced a large audit ledger too quickly after being asked to think exceptionally carefully. | Visible deliberation matters; silent delay is not evidence of thought. |
| Skipping the IMPORTANT paragraph | The assistant did not explicitly engage the paragraph explaining why fast answers feel disrespectful and untrustworthy. | High-effort critiques require visible processing before patching or responding. |
| Stale contract answer | After committing to GitHub, the assistant answered a contract-detail question from memory instead of fetching the canonical file. | For contract questions, fetch the canonical source; do not rely on conversational recollection. |
| Wrong persistence framing | The assistant framed the contract as something to fetch only when the topic touched contract behavior. | The contract governs all interactions and must be loaded at conversation startup. |
| Overcomplicated bootstrap prompt | The assistant wrote memory text that assumed too much context from the current conversation. | Startup memory must be self-contained and imperative. |
| Memory pollution issue | External tools made memory-writing unsafe/off-limits in that context. | Use memory only as a pointer and update it in a clean session when necessary. |

---

## 8. Remaining improvement opportunities

These items remain worth revisiting after the contract is exercised in real use.

| Area | Opportunity |
|---|---|
| Audit hook | Continue refining it around verification surfaces: basis, interpretation, assumptions, limitations, falsifiers, and confidence scope. |
| Assumption Ledger | Ensure it is visible enough to catch bad premises without becoming mechanical clutter. |
| Tangent Ledger | Actually use it during long work sessions; otherwise the rule is aspirational. |
| Objective/Focus | Watch for whether Objective remains truly stable and whether Focus changes at the right cadence. |
| Startup loading | Test whether future sessions actually fetch the raw URL before substantive work. |
| Context fatigue | Treat long-thread degradation as evidence to roll up and restart, not as a personal failing. |
| Contract length | After field use, do a compression pass that preserves behavior while reducing repeated phrasing. |
| Peer-agent portability | Try the contract with other agents and capture where they misinterpret it. |

---

## 9. Suggested workflow for future contract edits

1. Fetch the raw contract from GitHub fresh.
2. State Objective and Focus.
3. For substantial edits, create a visible mini-ledger:
   - accepted change;
   - rejected change;
   - unresolved design tension;
   - intended patch strategy.
4. Prefer targeted patches over whole-document rewrites unless the current document state is fully available.
5. Commit changes with a clear message.
6. Update this notes file only when a change has design rationale worth preserving.

---

## 10. Standing reminder

The contract is not meant to make assistant responses decorative or bureaucratic. It is meant to make them inspectable and corrigible.

If a future assistant tries to reduce the hooks, audit, Objective/Focus, or ledger mechanisms merely because they are inconvenient, it is likely misunderstanding the purpose of the contract.
