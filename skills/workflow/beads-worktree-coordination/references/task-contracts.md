# Task And Handoff Contracts

Use these templates inside Beads fields, comments, or agent dispatch messages. Replace every placeholder and omit sections that genuinely do not apply. Do not store secrets.

## Implementation Bead Contract

```text
Outcome:
  <observable result>

Acceptance criteria:
  - <criterion with a verifiable completion signal>
  - <required test or behavior>

Owned paths:
  - <path or tightly bounded module>

Excluded or read-only paths:
  - <sibling-owned or out-of-scope path>

Shared hotspots:
  - <lockfile, registry, schema, migration chain, generated index, or none>

Base:
  Branch: <branch>
  Commit: <full commit ID>

Dependencies:
  - <blocking bead IDs or none>

Required validation:
  - <focused test>
  - <task-level lint/build/test>

Handoff requirements:
  - branch and head commit
  - changed paths
  - tests and results
  - known conflicts
  - follow-up bead IDs

Authority:
  Commit: <allowed or not allowed>
  Code push: <allowed or not allowed>
  Dolt pull/push: <allowed or coordinator-only>
  Close bead: <worker or integrator>
```

Prefer `--description`, `--design`, `--acceptance`, and `--notes` flags over `bd edit`.

## Agent Dispatch Contract

```text
Role: worker
Actor: <unique BEADS_ACTOR>
Bead: <issue ID>
Repository: <absolute repository path>
Worktree: <absolute worktree path>
Branch: <branch>
Base commit: <full commit ID>

Outcome:
  <observable result>

You own:
  - <paths>

Do not edit:
  - <paths>

Acceptance and validation:
  - <criteria and commands>

Coordination:
  - Claim before editing.
  - Stop if Beads context differs from the supplied project.
  - Stop and report before crossing path ownership.
  - Create durable follow-up work in Beads.
  - Do not pull tracker state remotely from a sibling worktree.

Authority:
  <explicit commit, push, sync, close, and cleanup authority>

Return:
  <required handoff contract>
```

The dispatch message must state that other agents may be editing the shared repository and that the worker must preserve their changes.

## Worker Handoff Comment

```text
Ready for integration

Branch: <branch>
Head: <full commit ID or uncommitted>
Base used: <full commit ID>

Changed paths:
  - <path>

Validation:
  - <command>: <pass, fail, or not run with reason>

Acceptance:
  - <criterion>: <satisfied or not satisfied>

Known conflicts or ordering:
  - <details or none>

Follow-up beads:
  - <IDs or none>

Worktree state:
  <clean, or exact dirty/untracked files>
```

## Integration Result Comment

```text
Integration result: <merged, rejected, or blocked>
Source branch/head: <branch and commit>
Integration commit: <commit or none>
Merge-slot holder: <actor>

Conflict resolution:
  <decisions or none>

Validation:
  - <command>: <result>

Delivery boundary:
  <why the bead can close, or why it remains open>

Cleanup:
  <worktree retained or approved for removal>
```

## Discovered Work

Create a follow-up bead with enough context to survive handoff:

```bash
bd -C REPO create --title="Short outcome" --description="Why this exists, evidence, scope, and expected result" --type=task --priority=2
```

Link it to the originating work using the repository's supported graph convention. If it blocks the current task:

```bash
bd -C REPO dep add CURRENT-ID NEW-BLOCKER-ID
```

If it is non-blocking, use an appropriate informational relationship or record the new ID in the current issue notes. Never hide significant discovered work only in chat scrollback.

## Partitioning Test

Before declaring two tasks parallel-safe, answer all of these:

1. Are their owned paths disjoint?
2. Do they avoid the same generated files and dependency lockfiles?
3. Do they avoid the same migrations, schemas, registries, and public interfaces?
4. Can their tests run without sharing mutable ports, databases, or state directories?
5. Can either task finish without consuming the other's unmerged branch?
6. Is the intended merge order irrelevant, or represented by dependencies?

If any answer is no, sequence the tasks or create a dedicated integration bead.
