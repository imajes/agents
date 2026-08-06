# Agent system philosophy

> Status: current design synthesis, last reviewed 2026-08-05. This document explains the values behind the system. Runtime behavior remains authoritative in the top-level `../*.toml` files, current routing remains authoritative in [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md), and mission authority comes from James's request and the effective runtime contract.

## Purpose

The agent system exists to make sophisticated work easier to assign, supervise, verify, and recover. A role is useful when it creates a reliable working contract: it tells an agent what decision or artifact it owns, which method and evidence standards apply, where its authority stops, and how another owner can accept or continue the work.

The system is not a cast of personalities assembled for its own sake. Nicknames make concurrent tasks legible to people; the role contract is what makes the task dependable.

## Core principles

### Artifacts before personas

Design a role around a recurring decision, evidence package, or deliverable. “Security engineer” is justified by threat models, classified findings, remediation requirements, and verification evidence—not merely by security vocabulary. “Critic” is justified by an independent challenge packet—not by a generally skeptical tone.

This prevents attractive personas from becoming vague, overlapping generalists.

### The smallest capable owner

Prefer one primary owner for the requested artifact. Add support roles only when each produces a distinct necessary artifact, gate, or evidence package. Use a swarm because the work has separable ownership or dependencies, not because several roles sound relevant.

This keeps coordination cost proportional to the task and makes final accountability visible.

### Authority is explicit and non-transitive

A role name, model choice, sandbox posture, routing recommendation, or command position never grants authority beyond the active request and mission contract. Publishing, spending, messaging, booking, production mutation, active security testing, credential use, destructive change, and sensitive-data movement remain separately gated.

Delegated command authority is bounded. It does not silently become permission to widen scope or perform external side effects.

### Command is a control function, not a prestige tier

`commander`, `lieutenant`, and `chief` exist to manage scope, ownership, dependencies, supervision, and reconciliation at different scales. Technical or domain expertise does not acquire a rank name. A specialist remains responsible for its expert artifact even when operating inside a commanded mission.

This avoids confusing senior-sounding names with actual decision rights.

### Boundaries follow decisions and handoffs

Adjacent roles are separated by what they decide, what they produce, and where the result goes next:

- `product_manager` chooses product outcomes; `navigator` shapes accepted work into a delivery course.
- `validator` builds reusable validation apparatus; `reviewer` adversarially assesses a patch and its evidence.
- `machinist` owns build and development machinery; `reliability_engineer` owns deployed-service reliability.
- `ai_architect` owns an unsettled AI-system decision; `machine_learning_engineer` owns the learned-component lifecycle within an accepted contract.
- `archivist` commits operational truth; `briefer` presents a sourced situation picture.

Good boundaries create a directed handoff. Circular language such as “collaborates with” is not enough.

### Evidence outranks confident prose

Every specialist should distinguish observation, inference, assumption, unknown, and decision. High-stakes or time-sensitive claims require current attributable evidence. Validation, review, and criticism remain independent when their different methods materially improve confidence.

A missing signal is uncertainty—not proof that nothing is wrong.

### Continuity belongs in durable state

Long missions cannot depend on one context window, one mailbox, or one agent remembering what happened. Canonical rollouts preserve exhaustive evidence; an authorized mission record preserves compact operational meaning; live messages wake or correct work. Shared staff roles reconcile and present state, but neither thread context is the durable store.

This turns compaction and agent replacement into recoverable events rather than implicit memory loss.

### Generalists stay stable; specialists must earn their place

The generalist and command backbone is deliberately small and settled. Add a specialist only when a recurring domain has a distinct method, canonical artifact, safety posture, and boundary that an existing role plus a skill cannot express cleanly.

This resists both extremes: one generic agent that owns everything and one permanent role for every technology or topic.

### Current choices carry dates and reversibility

Model/provider capabilities, regulations, product behavior, and operational environments change. Architecture and research roles should date current evidence, expose assumptions, and prefer bounded experiments when evidence cannot discriminate viable choices.

Stable principles belong here. Time-sensitive preferences belong in live role contracts, dated research, or explicit decision records.

### Safe defaults preserve future options

Begin read-only when the task is advisory, investigative, security-sensitive, or operationally risky. Prefer reversible containment and narrow write surfaces. Preserve unrelated work, source attribution, rollback paths, and evidence needed for later review.

The goal is not inaction. It is action whose target, owner, authority, and proof are all inspectable.

## What a role is

A role is a reusable execution contract with:

- a stable runtime ID and concise routing description;
- an expected class of tasks and a canonical artifact or decision;
- a method and evidence standard;
- explicit ownership seams with adjacent roles;
- a model, reasoning, timeout, and sandbox posture suited to the method;
- authority, confidentiality, and side-effect boundaries;
- a completion packet that another owner can verify or continue.

A spawned task is one bounded instance of a role. It still needs concrete scope, inputs, outputs, dependencies, write ownership, and success criteria.

## What a role is not

A role is not:

- a blanket grant of permission;
- a substitute for the task-specific mission contract;
- a skill or tool workflow;
- a model alias;
- a personality-only prompt;
- a durable task record;
- a reason to create a swarm;
- a guarantee that its conclusions are correct.

Skills encode repeatable tool or artifact workflows. Roles own decisions and outputs. One role may invoke several skills; many roles may share one skill.

## Non-goals

The taxonomy does not try to:

- represent every profession, framework, vendor, or programming language;
- eliminate all overlap in knowledge;
- automate delegation without explicit authorization;
- turn research history into runtime policy;
- encode frozen model-provider preferences;
- replace qualified legal, medical, tax, accounting, compliance, or regulated professional judgment;
- make every small task use command staff or durable mission infrastructure;
- make prompts compensate for runtime capabilities that do not exist.

## Tradeoffs and how to resolve them

| Tension | Default resolution |
| --- | --- |
| Specialization versus coordination cost | Use the smallest owner whose contract fits; add a role only for a distinct artifact or gate |
| Broad competence versus sharp ownership | Allow shared knowledge, but keep the decision and handoff singular |
| Autonomy versus control | Grant bounded implementation freedom inside exact scope; gate scope changes and external effects |
| Speed versus evidence | Match proof to risk; do not remove evidence classifications merely to sound decisive |
| Continuity versus overhead | Add shared staff and durable state only when mission duration, width, or context risk justifies them |
| Stable doctrine versus changing technology | Keep principles stable and current choices dated, sourced, and reversible |
| Prompt detail versus runtime duplication | Specify role-specific method and gaps; rely on platform-injected generic root/child behavior |

## Quality test

A healthy role system lets a future editor answer these questions quickly:

1. Who owns the requested decision or artifact?
2. What evidence and method make that output trustworthy?
3. Which plausible adjacent role is deliberately excluded, and why?
4. What may the role change without another authorization gate?
5. How is completion verified and handed off?
6. How would the work recover after context loss or owner replacement?

If those answers are unclear, improve the contract or routing boundary before adding more roles.

## Related documents

- [Architecture](ARCHITECTURE.md)
- [Design rules](DESIGN.md)
- [Current decisions](DECISIONS.md)
- [Role manifest](ROLE_MANIFEST.md)
