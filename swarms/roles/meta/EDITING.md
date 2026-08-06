# Editing the agent system

> Status: current editor workflow, last reviewed 2026-08-05. Follow the live repository instructions and James's active request first. Top-level `../*.toml` files are runtime-authoritative; [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md) is the current human routing contract. This workflow does not authorize staging, committing, external setup, or side effects.

## Before editing

Work from the repository root at `/Users/james/.codex` and establish the boundary before making a change.

1. Read the applicable `AGENTS.md` files.
2. Inspect `git status --short --branch` and identify pre-existing tracked, untracked, staged, and ignored work.
3. Name the exact runtime and documentation files in scope.
4. Read the live role TOMLs on both sides of any proposed boundary.
5. Read the relevant manifest rows and the matching current decision.
6. Use dated research only when the rationale or rejected alternatives matter.
7. Route the editing method through the tooling skill router and load the most specific matching skill.

The working tree may already contain user-owned changes. Preserve them, do not reformat them incidentally, and do not stage or commit unless James explicitly asks.

## Classify the change

| Change class | Examples | Minimum surfaces |
| --- | --- | --- |
| Editorial | Broken link, grammar, heading, no semantic change | Owning Markdown file; validate links and diff |
| Role-local runtime | Intake wording, evidence packet, timeout, model, or sandbox for one role | Role TOML; manifest only if current routing or listed facts change |
| Boundary | One role gains or loses an artifact, decision, or handoff | Both adjacent TOMLs, manifest, fixtures when represented |
| Taxonomy | Add, split, merge, retire, or rename a role | Runtime files, all adjacent contracts, manifest, decisions, routing fixtures, validation baseline |
| Control-plane | Command topology, staff, reporting, continuity, or authority protocol | Relevant command/staff TOMLs, manifest, architecture, decisions, protocol tests |
| Historical evidence | Completed audit or experiment | Dated research record; current docs only if accepted design changes |

Do not let an “editorial” label hide a semantic change. Replacing “may recommend” with “owns,” changing a handoff, or removing an authorization qualifier is runtime design.

## Prepare a change contract

Before a nontrivial edit, write down:

- requested outcome and decision owner;
- exact files and write surface;
- current behavior and evidence;
- proposed behavior;
- primary artifact or decision owner;
- positive and negative routing examples;
- adjacent-role seams and handoff gate;
- authority, sandbox, privacy, and external-action effects;
- model/effort/timeout implications;
- validation commands and expected result;
- migration or compatibility concerns;
- whether staging or committing is authorized.

For a new role, use [`ROLE_TEMPLATE.md`](ROLE_TEMPLATE.md). For a cross-cutting decision, assign or update a stable ID in [`DECISIONS.md`](DECISIONS.md).

## Edit an existing role

1. Read the entire TOML, not only the matching sentence.
2. Identify the contract section that owns the change: intake, method, evidence, artifact, boundary, safety, or completion.
3. Inspect every named neighboring role and reciprocal seam.
4. Make the smallest coherent runtime edit.
5. Update the manifest when the human inventory, primary function, routing table, command topology, continuity protocol, or important boundary changes.
6. Update current synthesis only when the architectural or design rule changes.
7. Update dated research only to preserve substantial new evidence or a completed decision process.
8. Run targeted validation, then the full relevant contract.

Avoid opportunistic cleanup in unrelated roles. If a broader defect is real, record it as a separate scoped change.

## Add a role

### Establish need

Apply the [role admission test](DESIGN.md#role-admission-test). Supply at least:

- three representative positive routing cases;
- three superficially plausible negative cases;
- the canonical artifact or decision;
- the distinctive method and evidence standard;
- the nearest existing roles and exact exclusion rules;
- the expected downstream owner;
- authority and write posture;
- model/effort/timeout rationale.

If an existing role plus a skill can own the artifact cleanly, stop there.

### Draft safely

Draft inside the fenced Markdown template in [`ROLE_TEMPLATE.md`](ROLE_TEMPLATE.md) or another temporary `.md` file outside `agents/`. Never place a candidate `.toml` under `agents/meta/`.

Run an adversarial boundary review before materializing the file:

- Does the candidate seize product, architecture, security, commercial, legal, or operational decisions it should only inform?
- Does it have a concrete completion packet?
- Can it decline negative cases?
- Are external effects independently gated?
- Is the reciprocal seam present in adjacent roles?
- Does the handoff terminate with a named owner?

### Materialize and synchronize

1. Create `agents/<role_id>.toml` with `name = "<role_id>"`.
2. Add one row to the manifest inventory.
3. Add or update specialist routing and important-boundary entries only where the role creates a durable seam.
4. Update reciprocal runtime boundaries in neighboring TOMLs.
5. Update [`DECISIONS.md`](DECISIONS.md) if the addition changes a cross-cutting policy; ordinary instances can rely on a dated decision record.
6. Add or update router fixtures for ambiguous or high-value routing cases.
7. Validate the entire discovered role set through both TOML parsing and the real Codex loader.

Do not stage the new file by default. An untracked runtime file still affects local role discovery and must be included in validation.

## Split, merge, retire, or rename

These changes are migrations, not ordinary prose edits.

### Split

- Divide the old artifact and method explicitly.
- Assign every former positive case to one new owner.
- Add acceptance gates between stages that were previously internal.
- Prevent both new roles from retaining the full old scope.
- Update downstream handoffs and fixtures.

### Merge

- Name the surviving runtime ID and canonical artifact.
- Reconcile conflicting model, sandbox, and authority postures deliberately.
- Remove routing loops and redundant reciprocal boundaries.
- Preserve any still-useful specialist method inside the surviving contract or a skill.

### Retire

- Remove live inbound references before removing the TOML.
- Route every recurring task to a surviving owner.
- Keep the historical rationale in dated research or the decision register.
- Validate that the loader and manifest no longer discover the ID.

### Rename

- Rename the file and its `name` together.
- Replace every live backticked role ID in top-level TOMLs and current docs.
- Update descriptions, routing tables, fixtures, and command diagrams.
- Add the old-to-new mapping to the manifest rename ledger.
- Preserve old IDs only in the ledger, migration explanation, and dated research.
- State that already-running tasks may retain the previously injected inventory.

## Documentation synchronization matrix

| If this changes | Update |
| --- | --- |
| Exact role behavior | Runtime TOML |
| Role list or concise function | Manifest inventory |
| Primary specialist routing | Manifest specialist-routing table |
| Cross-role ownership | Both runtime contracts and manifest important boundaries |
| Naming or command hierarchy | Manifest naming doctrine, topology, rename ledger, architecture, decisions |
| General design principle | Philosophy or design guide plus decision register |
| Runtime/discovery/state component | Architecture plus decision register |
| Editor process or invariant | Editing or validation guide |
| Future routing expectation | Router specification and fixtures |
| Evidence or rejected alternatives | Dated research record |

Do not update every document merely because a role changed. Update the one canonical owner for each changed fact and add links where a future reader would otherwise miss it.

## Research lifecycle

Use a dated research record when work includes substantial source reconstruction, experiments, adversarial review, rejected alternatives, or a phased design decision. A research record should state:

- observation or completion date;
- repository boundary and revision;
- whether it is active, completed, provisional, or superseded;
- evidence and method;
- decisions made and authority;
- changes applied;
- validation evidence;
- open questions or final handoff.

After acceptance, promote the stable rule into the current authority. Leave historical counts and superseded paths intact behind a clear status notice.

## Review the diff

Review in this order:

1. `git diff --check` for whitespace and conflict markers.
2. Standard diff for scope and unintended churn.
3. Syntax-aware or semantic diff when formatting obscures meaning.
4. Both sides of every boundary.
5. Exact authority verbs: `owns`, `may`, `proposes`, `accepts`, `authorizes`, and `implements`.
6. New and deleted role references.
7. Model, effort, timeout, and sandbox changes.
8. Staged state and unrelated files.

Classify each segment as semantic, mechanical, or uncertain. Resolve uncertain segments before validation.

## Handoff

Return a compact evidence-bearing handoff:

```text
SCOPE: <requested outcome and files changed>
RUNTIME: <roles or behavior changed; "none" for documentation-only>
BOUNDARIES: <ownership seams added, changed, or confirmed>
AUTHORITY: <side-effect and write posture; gates preserved>
DOCS: <current authorities synchronized>
VALIDATION: <commands and exact result>
WORKTREE: <unstaged/staged state and preserved unrelated changes>
OPEN: <remaining decision, risk, or "none">
```

Do not say “validated” without naming the evidence. Do not imply that an unstaged change is committed or that an uninstalled router is active.

## Editing anti-patterns

- Starting from dated research instead of the live TOMLs and manifest.
- Creating a `.toml` template beneath `agents/meta/`.
- Editing only the most obvious side of a boundary.
- Broadening a role to avoid the work of defining a handoff.
- Copying a full role catalog into another current document.
- Treating nickname changes as taxonomy changes—or taxonomy changes as nickname-only.
- Running a formatter across unrelated user-owned files.
- Assuming an untracked role is not loaded.
- Updating counts without a dynamic inventory comparison.
- Staging or committing because validation passed.
- Initializing Beads, installing a skill, or changing production/external state as an implied documentation step.

## Related documents

- [Design guide](DESIGN.md)
- [Role template](ROLE_TEMPLATE.md)
- [Validation contract](VALIDATION.md)
- [Decision register](DECISIONS.md)
