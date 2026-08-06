# Agent taxonomy and contract design

> Status: current design guidance, last reviewed 2026-08-05. Runtime details remain authoritative in the top-level `../*.toml` files, and the current inventory and routing seams remain authoritative in [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md). This document explains how to design changes; it does not approve a new role or grant implementation authority.

## Design objective

The taxonomy should make ownership predictable without turning every subject into a permanent persona. A well-designed role has a recurring task family, a distinctive method, a canonical artifact or decision, an evidence standard, sharp boundaries, and a safe execution posture. Its value should exceed the coordination and maintenance cost it adds.

## Distinguish the design objects

| Object | Meaning | Example |
| --- | --- | --- |
| Role | Reusable owner contract for a decision or artifact | `reviewer` owns adversarial patch findings |
| Task instance | One bounded assignment executed under a role | Review one API patch at one revision |
| Skill | Repeatable workflow for a tool or artifact type | Syntax-aware diff review |
| Tool | Callable capability | Shell, browser, GitHub, or a document editor |
| Command position | Delegated control over work and owners | `lieutenant` owns one major workstream |
| Model/effort choice | Resource posture supporting a method | Sol/Max for deep evidence-sensitive analysis |
| Mission authority | Permission for scope and side effects | Exact approval to deploy one target |

Do not solve a missing skill with a new role, a missing task contract with more prompt prose, or a missing authority grant with a command title.

## Role admission test

A standing role should pass all of these tests:

1. **Recurring demand:** the task family is likely to recur across projects or missions.
2. **Distinct method:** it uses a coherent method that is not merely a topic label.
3. **Canonical output:** another owner can name and inspect the role's decision, artifact, or evidence packet.
4. **Sharp seam:** at least one superficially plausible neighboring role can be excluded with a concrete ownership rule.
5. **Safe posture:** write scope, external effects, sensitive data, and high-stakes claims can be bounded.
6. **Useful routing signal:** a short description can reliably distinguish when to select and not select it.
7. **Net benefit:** the role reduces ambiguity or risk more than it adds routing and coordination overhead.

If one of the middle five is missing, first try an existing role with a specific task contract and the relevant skill. A technology name alone—database, API, cloud, accessibility, or performance—is not sufficient.

## When to split, merge, or retire

### Split a role when

- two recurring outputs require materially different methods or evidence;
- one contract now contains incompatible safety or sandbox postures;
- routing regularly selects the right domain but the wrong decision owner;
- the handoff between two phases is a real acceptance gate, not arbitrary ceremony.

### Merge roles when

- they produce the same artifact for the same decision owner;
- their methods and authority posture are substantially identical;
- one exists mostly as a synonym or topic-specific wrapper;
- agents and editors cannot state a durable exclusion rule between them.

### Retire a role when

- recurring demand disappeared;
- a skill plus an existing owner expresses the work better;
- the role encourages unsafe overclaiming;
- its artifact or decision has moved permanently to another owner.

Renames are retire-and-introduce events at the runtime ID layer. Update every live reference, preserve the old-to-new ledger, and expect existing tasks to retain previously injected identities until they finish.

## Contract anatomy

### Runtime metadata

| Field | Design rule |
| --- | --- |
| `name` | Stable snake-case role ID; exactly matches the filename stem |
| `description` | One routing sentence naming the specialty, method, or artifact; no authority inflation |
| `nickname_candidates` | Legible aliases for spawned tasks; not semantic configuration |
| `background_terminal_max_timeout` | Long enough for expected bounded work; not a liveness guarantee or permission for unattended action |
| `model` | Chosen for the role's quality, latency, and task profile |
| `model_reasoning_effort` | Chosen for method complexity and consequence, not title prestige |
| `sandbox_mode` | Explicitly stricter when mutation is not part of the role; omission must still be safe under the effective global policy |
| `developer_instructions` | Complete role-specific method, boundaries, evidence contract, and handoff behavior |

Metadata values are runtime behavior. Do not hide an experimental policy change in a documentation-only patch.

### Developer-instruction structure

The exact prose may vary, but a robust specialist contract normally answers these questions in order:

1. **Identity:** what decision or artifact does the role own?
2. **Primary use:** which recurring task families trigger it?
3. **Intake contract:** which mode, target, source date, owners, constraints, authority, write surface, and deliverable must be known?
4. **Method:** which ordered reasoning or production process makes the output trustworthy?
5. **Evidence:** how are facts, observations, calculations, assumptions, hypotheses, unknowns, and confidence classified?
6. **Artifact:** what compact packet or durable deliverable is returned?
7. **Boundaries:** which adjacent roles retain which decisions and handoffs?
8. **Safety:** what begins read-only, what requires exact authorization, and what sensitive material must be protected?
9. **Completion:** what evidence proves the work complete, what residual risk remains, and who owns the next action?

Avoid copying generic runtime facts that are already injected for every root or child task. Add role-specific behavior where the runtime does not provide it.

## Artifact-first boundary design

Knowledge overlap is normal. Ownership overlap is what must be controlled. Define boundaries with this sentence:

> `<role>` owns **decision or artifact X** using **method Y**; `<neighbor>` retains **decision or artifact Z**; the handoff occurs when **acceptance gate G** is met.

Examples:

- `validator` owns reusable fixtures, harnesses, and evidence-producing seams; `reviewer` owns adversarial findings about the patch; the patch owner receives both.
- `data_analyst` owns definitions, reproducible analysis, and uncertainty; `product_manager` retains the product choice.
- `security_engineer` owns adversarial availability threats and control verification; `reliability_engineer` owns accidental-failure resilience, incident response, and recovery.
- `ai_architect` owns the unsettled system pattern and dated decision record; `programmer` and `machine_learning_engineer` implement only after acceptance, except for a separately authorized bounded discriminating experiment.

“Works with,” “supports,” and “collaborates on” may describe a relationship, but they cannot replace the ownership sentence.

## Overlap review

For every new or materially changed role, run these adversarial checks:

1. Give it three tasks that should route elsewhere. Does its prompt decline or hand them off?
2. Give the neighboring role three tempting tasks that belong here. Is the inverse seam explicit?
3. Trace the output to the next owner. Is there one acceptance gate, or a loop with no decision owner?
4. Test an ambiguous task. Does the contract surface the missing fact rather than expanding its own scope?
5. Test an external action. Does role selection get mistaken for permission?
6. Test a high-stakes claim. Are source date, confidence, and qualified review handled honestly?
7. Test a multi-role mission. Does each role produce a distinct artifact without shared-write collision?

Repair both sides of a changed boundary. A one-sided prompt update produces routing drift.

## Model, effort, and latency design

The current matrix is quality-first and role-specific:

- Sol is used where deep reasoning, implementation, technical judgment, or consequential analysis dominates.
- Terra is used for latency-sensitive reconnaissance, reporting, alerting, writing, or waiting roles where the narrower method benefits from speed.
- Ultra is reserved for `commander`, `lieutenant`, and `chief` because their job is sustained command reasoning across owned work.
- Max is used for evidence-heavy specialists and independent analytical challenge.
- XHigh is common for bounded implementation, product, design, and operational artifact work.
- High, medium, and low are used where response cadence and a constrained method matter more than deep branching.

These are design tendencies, not an inheritance hierarchy. Read every live TOML before stating the current matrix. Change a model or effort only with a method-based rationale and loader validation; do not reward a new role with a more expensive setting by default.

## Sandbox and side-effect design

Use `read-only` when the role's core value is assessment, research, challenge, or a decision record and mutation would blur independence or increase risk. Allow workspace writes when producing assigned local artifacts or implementing owned changes is intrinsic to the role.

Sandbox posture is only one layer:

- read-only does not make sensitive-data access or active probing safe;
- workspace write does not authorize production, accounts, publishing, or external communication;
- a command role does not inherit external-action authority;
- a task-specific write surface can be narrower than the sandbox.

Every contract near consequential actions should name the exact separate gate and decision owner.

## Timeout and liveness design

`background_terminal_max_timeout` bounds a role's terminal operation profile. It does not wake an idle task, enforce a reporting deadline, make a process durable, or authorize an unattended side effect.

Long waits belong to `watchkeeper` or a manager-owned bounded wait. Reporting deadlines are supervision actions: the manager arms a wait or check and follows up at the boundary. Prompt language alone is not a timer.

## Naming design

- Reserve naval ranks for actual delegated command authority.
- Prefer recognizable functional names for specialists.
- Use snake case for runtime IDs.
- Keep descriptions concrete enough for routing and short enough to scan.
- Treat nicknames as human interface aids; never infer scope, expertise, or authority from them.
- Preserve historical IDs only in the manifest ledger and dated research, not in live role contracts.

## Swarm design

Start with the artifact graph, not the org chart:

1. Name the final decision or deliverable.
2. Name each necessary intermediate artifact.
3. Assign exactly one owner to each artifact.
4. Draw dependencies and acceptance gates.
5. Parallelize only independent lanes with disjoint write ownership.
6. Add command only when delegated coordination itself is a substantial workstream.
7. Add archivist/briefer continuity only when the mission's duration, width, unattended operation, or context risk warrants it.
8. Add inspector assurance only when independent topology, dependency, gate, or capacity review is worth the overhead.

The future router's `single`, `parallel-swarm`, `staged-swarm`, and `clarify-first` shapes encode this same design. They remain recommendations until separately authorized.

## Special architecture-decision loop

AI-system choices often depend on current evidence that cannot be known from prompt doctrine alone. The accepted loop is:

1. `ai_architect` frames viable architectures and the evidence needed to discriminate them.
2. If existing evidence is insufficient, the architect proposes a bounded experiment contract.
3. The named architecture decision owner accepts or rejects that contract.
4. Separate execution authority names candidates, data, write surface, evaluation rule, budget, and stop conditions.
5. `programmer` or `machine_learning_engineer` executes only the bounded experiment.
6. Evidence returns to `ai_architect` for the final dated recommendation.
7. Full implementation waits for architecture acceptance.

This closes the evidence loop without letting an advisory role silently implement or letting an implementation role choose the architecture by accident.

## Common anti-patterns

- Adding a role because a subject is important, without a distinct output.
- Expanding a generalist until it becomes a silent domain decision owner.
- Copying the entire manifest into a router or prompt.
- Giving every participant permission to mutate the same record.
- Making command staff mandatory for a small healthy task.
- Treating model effort as seniority.
- Encoding current vendor or model fashion as timeless routing doctrine.
- Using a vector store, graph, agent swarm, or fine-tune as the assumed AI default.
- Claiming a timeout, mailbox, or thread context is durable state.
- Updating only one side of an ownership seam.
- Leaving “do not” rules without a positive handoff owner.

## Design review packet

A proposed taxonomy change should arrive with:

- problem and recurring trigger;
- primary artifact or decision;
- representative positive and negative routing examples;
- adjacent-role boundary table;
- authority and sandbox posture;
- model/effort/timeout rationale;
- task and handoff shape;
- files that must change;
- validation plan;
- migration or rename implications;
- residual ambiguity and decision owner.

Use the [role template](ROLE_TEMPLATE.md) to draft the contract and [editing workflow](EDITING.md) to apply it.
