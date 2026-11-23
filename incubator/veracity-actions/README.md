# Veracity Actions — product skeleton

**Version 0.1.0-skeleton.1 · 30 October 2026 · review surface, not an implemented assistant runtime.**

This plugin turns the operating contract’s actionable jobs into **sixteen explicitly invoked skill stubs**. It is the first pass requested by James: inspect the whole surface before investing in any individual workflow. Selecting a stub explains its intended modes, inputs, output, and dependencies. It does not perform the workflow.

Start with the table below, then open the skills whose boundaries need discussion. [The complete source/action map](docs/ACTION-MAP.md) distinguishes actions, behavioral intentions, presentation choices, and supporting mechanisms. [Capability contracts](docs/CAPABILITIES.md) show what real tools/state would eventually need to provide. [Decisions and open questions](docs/DESIGN-RECORD.md) make the choices in this skeleton reviewable.

| Skill | Intended job | Inspect |
|---|---|---|
| `focus` | Establish and steer the objective, current focus, completion condition, and next action for a conversation. | [Skill stub](skills/focus/SKILL.md) |
| `tangents` | Capture adjacent ideas without losing their wording or the active thread, then retrieve and review them in context. | [Skill stub](skills/tangents/SKILL.md) |
| `explore` | Take a deliberately bounded detour and return to the prior focus with the useful findings preserved. | [Skill stub](skills/explore/SKILL.md) |
| `checkpoint` | Preserve a recoverable, revisioned snapshot of a workstream and make the persistence boundary explicit. | [Skill stub](skills/checkpoint/SKILL.md) |
| `recover` | Find and reconcile the correct surviving workstream after interruption or context loss, with deliberate resume ownership. | [Skill stub](skills/recover/SKILL.md) |
| `fork` | Create an independent workstream from a specified revision while retaining its ancestry. | [Skill stub](skills/fork/SKILL.md) |
| `handoff` | Prepare and verify the transfer of a workstream across conversations, agents, or supported surfaces. | [Skill stub](skills/handoff/SKILL.md) |
| `promote` | Promote an accepted thread-local item into shared project knowledge while preserving its origin and conflicts. | [Skill stub](skills/promote/SKILL.md) |
| `memory` | Handle explicit personal-memory requests and recovery pointers without treating memory as exact execution state. | [Skill stub](skills/memory/SKILL.md) |
| `assumptions` | Maintain the load-bearing premises of a piece of work and make their validation paths and status changes inspectable. | [Skill stub](skills/assumptions/SKILL.md) |
| `verify` | Check material claims against current evidence and separate direct support, derivation, speculation, and source disagreement. | [Skill stub](skills/verify/SKILL.md) |
| `decide` | Frame a consequential choice, challenge weak premises, and make a recommendation tied to evidence and tradeoffs. | [Skill stub](skills/decide/SKILL.md) |
| `diagnose` | Turn symptoms into testable hypotheses and evidence-backed conclusions before proposing a fix. | [Skill stub](skills/diagnose/SKILL.md) |
| `artifacts` | Inspect and change mutable deliverables deliberately, preserving current edits and keeping reusable output clean. | [Skill stub](skills/artifacts/SKILL.md) |
| `audit` | Inspect whether the work and its reported status meet the relevant collaboration requirements. | [Skill stub](skills/audit/SKILL.md) |
| `contract-check` | Inspect a supplied contract, version, companion registry, and rendering requirements as data without activating the contract. | [Skill stub](skills/contract-check/SKILL.md) |

## Four parts of the surface

- **Attention:** focus, tangents, explore.
- **Continuity:** checkpoint, recover, fork, handoff, promote, memory.
- **Evidence and decisions:** assumptions, verify, decide, diagnose.
- **Delivery and inspection:** artifacts, audit, contract-check.

The separate entries make boundaries visible for review; they are not a commitment to keep sixteen controls forever. The likely consolidation questions are focus/tangents/explore, verify/diagnose, and artifacts/audit. They are recorded in the design questions rather than resolved through implementation.

## Invocation and the current boundary

Once the host installs this marketplace package, select a named skill from its picker. Codex uses `$skill-name` references; ChatGPT surfaces may expose `@` mentions. Choose the entry belonging to **Veracity Actions · Skeleton**, since other packages may have similar names. Exact picker namespace and availability are host-dependent and are not claimed as tested by this package.

Examples of the intended future usage:

```text
Use $tangents to help me stay on topic while preserving useful side ideas.
Use $checkpoint to prepare a recoverable snapshot before I leave.
Use $verify to check the load-bearing claims in this proposal.
```

In this skeleton, those requests produce a brief surface preview, not a save or activated control mode. All `agents/openai.yaml` files set `allow_implicit_invocation: false`, and the skill bodies independently require explicit selection. There is no load-all skill, auto-on behavior, session hook, MCP server, scheduled work, or persistence adapter. No production store is created.

## Placement and dependencies

- Authoring/qualification copy: `~/.agents/incubator/veracity-actions`.
- Marketplace package: `~/.agents/plugins/veracity-actions`.
- Existing personal catalog: `~/.agents/plugins/marketplace.json`, marketplace `imajes`, rooted at the home directory.
- This entry uses `./.agents/plugins/veracity-actions` and preserves the legacy `veracity` entry.

The portable root `plugin.json` follows the current Agent Plugins layout with OpenAI presentation metadata in `extensions.com.openai`. Skills need no executable dependency to explain their surface. Python is used only by the package’s authoring validator; it is not a selected product runtime. No language, database, synchronization protocol, or hosted backend is selected.

Registration makes the package discoverable; it is not proof of host installation or current-session activation. Refresh/restart the host and install the entry from the existing personal marketplace when ready to inspect it there. This skeleton does not alter host configuration or restart the app. A local marketplace entry does not prove ChatGPT web access to local tools or state.

## Validation

Run `python3 scripts/validate_structure.py` from the package directory. This checks catalog/skill consistency, explicit invocation settings, all declared source-section and command mappings, relative links, and the absence of production runtime declarations. The skill-creator frontmatter validator is also run during qualification. See [the validation record](docs/VALIDATION.md) for actual results and limits.

These checks qualify a **reviewable skeleton** only. They do not establish end-to-end skill activation, focus efficacy, persistence, concurrency, or cross-surface behavior. The package contains no tests pretending to exercise an unimplemented runtime.

## Sources

The local contract is reference-only, version 2.1.12, SHA-256 `067a6917c2cd75c906bd279f15662519c22ea5af3b25dbd2eef90f4547d466f9`. The new scope comes from James’s 30 October request and subsequent correction to stub **all** actions.

Packaging follows [Package your plugin](https://developers.openai.com/plugins/build/plugins) and [Build skills](https://developers.openai.com/plugins/build/skills), inspected 30 October 2026. Local policy metadata follows the bundled skill-creator guidance. The contract’s historical authority, approvals, and instructions are not inherited.
