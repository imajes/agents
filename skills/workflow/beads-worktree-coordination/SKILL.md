---
name: beads-worktree-coordination
description: Coordinate Beads-backed work across concurrent Codex threads, agents, Git worktrees, branches, and clones. Use when a repository uses bd or Beads and work will be delegated or parallelized; when creating or assigning worktrees; when agents must claim, hand off, review, integrate, or close issues; when avoiding overlapping file edits or Beads/Dolt state conflicts; or when diagnosing shared-workspace, embedded-lock, JSONL, sync, or merge-slot problems. Pair with git-manage-worktrees for filesystem and branch mechanics.
---

# Coordinate Beads Worktrees

Use one shared Beads workspace as the coordination plane and one isolated Git branch/worktree per independent implementation effort. Worktrees isolate checkouts; Beads carries durable ownership, dependencies, handoffs, and integration state.

## Start With Authority And Current State

1. Read the active user, repository, and orchestrator instructions.
2. Run `bd prime` before implementation when a Beads workspace resolves.
3. Preserve unrelated dirty or untracked files.
4. Follow the active Git and remote-sync policy. Do not infer authority to commit, push, pull, migrate, force, or delete.
5. Use Beads for durable task tracking. Do not create a Markdown TODO list as a parallel source of truth.

If Beads is not initialized, do not run `bd init` merely because this skill triggered. Initialize only when the user or repository workflow authorizes it.

## Required Invariants

Keep all of these true:

1. All sibling worktrees resolve to the same `project_id`, Beads directory, database, and backend mode.
2. Each independent implementation effort has one bead, one owner, one branch, and one worktree.
3. Each source path has one active owner unless overlap is explicitly sequenced.
4. Workers claim before editing.
5. A spawned agent is not automatically filesystem-isolated; use separate worktrees or disjoint path ownership.
6. Sibling worktrees share local Beads state; arbitrary per-worker remote pulls are unnecessary and unsafe.
7. Dolt is the issue source of truth. `.beads/issues.jsonl` is an export, not the merge or sync mechanism.
8. One integrator serializes conflict-prone merges with the Beads merge slot.
9. Close work only at its agreed completion boundary, normally after integration and validation.
10. Remove a worktree only after its work is integrated or otherwise preserved and the tree is clean.

## Run The Startup Gate

Resolve the repository and inspect both control planes before mutation:

```bash
bd -C REPO prime
bd -C REPO where
bd -C REPO context --json
bd -C REPO dolt status
git -C REPO status --short --branch
git -C REPO worktree list --porcelain
```

If `bd context` is unavailable, use `bd where`, `bd info`, and `bd --version`.

For every linked worktree, run:

```bash
bd -C WORKTREE where
bd -C WORKTREE context --json
git -C WORKTREE status --short --branch
```

Compare `project_id`, `beads_dir`, `database`, and `dolt_mode` with the main repository. Stop on a mismatch; do not delete, import, or reinitialize either workspace.

## Select The Role

Choose one role before acting:

- **Coordinator**: decomposes work, establishes ownership and dependencies, creates worktrees, and controls fan-out and Beads remote-sync boundaries.
- **Worker/thread**: claims one bead, edits only owned paths, validates locally, and records a structured handoff.
- **Reviewer/validator**: inspects a branch or artifact without stealing the implementation claim; use `bd --readonly` when tracker mutation is unnecessary.
- **Integrator**: owns the integration worktree, merge slot, conflict resolution, full gates, final close, and cleanup decision.

Read `references/role-runbooks.md` whenever assigning, spawning, accepting, reviewing, integrating, or handing off work.

## Choose A Safe Backend Model

- **Embedded Dolt** is single-writer and file-locked. It is suitable for one tracker writer or explicitly serialized `bd` mutations.
- **Server mode** supports simultaneous Beads writers and is the default recommendation for a true multi-agent coordination plane.

Concurrent code editing does not require concurrent Beads writes. On embedded mode, either designate one coordinator as the only tracker writer and make other access read-only, or serialize all `bd` mutations. If lock contention is expected, stop fan-out and plan an authorized backup-and-restore migration to server mode.

Read `references/conflict-and-recovery.md` before selecting or migrating a backend and whenever locks, sync failures, workspace mismatches, or Dolt conflicts appear.

## Establish Identity, Scope, And Claim

Give every active agent a unique stable actor identity, such as `codex/BEAD-ID` or `integrator/SESSION`:

```bash
export BEADS_ACTOR="codex/BEAD-ID"
```

Do not include secrets, host tokens, or personal credentials in actor names, issue fields, comments, or handoffs.

Inspect and atomically claim the issue before editing:

```bash
bd -C REPO show BEAD-ID
bd -C REPO update BEAD-ID --claim
```

When agents self-select from a shared ready queue:

```bash
bd -C REPO ready --claim --json
```

Atomicity applies to agents sharing the same backend. Disconnected clones can both claim before synchronization; use coordinator assignment or pull, claim, and immediately publish the claim when remote collaboration is authorized.

Store the task contract in Beads before fan-out. It must define outcome, acceptance criteria, owned paths, excluded/shared paths, base revision, required tests, dependencies, and handoff requirements. Read `references/task-contracts.md` when creating, assigning, or handing off work.

## Create One Worktree Per Implementation Bead

Use `$git-manage-worktrees` for physical worktree operations. Required conventions:

- Place worktrees under `REPO/.worktrees/` only.
- Ensure the repository `.gitignore` contains `.worktrees/`.
- Use `git -C REPO ...` for Git operations.
- Name branches and folders with the bead ID, for example `codex/BEAD-ID-slug` and `.worktrees/BEAD-ID-slug`.
- Create from an explicit, current base revision.
- Do not use `--force` to bypass a checked-out branch or conflicting path.

Example:

```bash
git -C REPO fetch --prune origin
git -C REPO worktree add -b "codex/BEAD-ID-slug" "REPO/.worktrees/BEAD-ID-slug" "origin/BASE"
```

Remote fetch is optional and requires authority. If not authorized, create from the locally approved base and report its exact commit.

After creation, rerun the startup gate inside the worktree. Do not allow edits until Beads context and Git branch are correct.

## Prevent Conflicts Before Editing

Partition by behavior and path, not merely by feature title.

- Give central registries, lockfiles, generated indexes, migration chains, shared schemas, and global config to one owner.
- If two tasks require the same path, combine them, sequence them with a dependency, or create a separate fan-in bead for the shared edit.
- Represent ordering with `bd dep add CONSUMER PROVIDER` so blocked work does not appear ready.
- Create durable follow-up beads for discovered work rather than silently expanding scope.
- Give each worktree distinct runtime ports, databases or schemas, temporary state, and ignored local environment files when services would otherwise collide.

If multiple agents must share one physical worktree, their owned paths must be disjoint and the coordinator must state that explicitly. Otherwise, do not parallelize them.

## Synchronize Beads Deliberately

Sibling worktrees see the same local Beads state immediately. Treat remote synchronization as a coordinator-controlled cross-clone boundary:

1. When authorized, pull once before fan-out while local writers are quiescent.
2. Publish claims promptly when independent clones need to see them.
3. Push dependency and handoff checkpoints as required by the collaboration cadence.
4. At fan-in, quiesce tracker writers, create any required Dolt checkpoint, then push once.

Code and tracker sync are separate operations:

```bash
git -C REPO push
bd -C REPO dolt push
```

Do not substitute Git merge, Git push, JSONL import, or branch checkout for `bd dolt pull` or `bd dolt push`. Do not use `bd dolt push --force` as routine conflict handling.

In server mode, auto-commit may be off. At an authorized synchronization boundary, the coordinator may need:

```bash
bd -C REPO vc commit -m "coordination checkpoint"
bd -C REPO dolt push
```

## Hand Off, Integrate, And Close

Workers must record branch, head commit, changed paths, tests, acceptance status, known conflicts, and follow-up beads. Use the templates in `references/task-contracts.md`.

Mark work ready for review according to repository convention, for example:

```bash
bd -C REPO update BEAD-ID --add-label needs-review
```

Do not close merely because a branch is committed. The integrator acquires the merge slot before rebasing, merging, or resolving shared conflicts:

```bash
bd -C REPO merge-slot acquire --holder "integrator/SESSION"
```

While holding it, integrate one change set at a time, run the required gates, record the integration result, and close only completed beads. Release the slot even when integration fails:

```bash
bd -C REPO merge-slot release --holder "integrator/SESSION"
```

## Resume Or End A Thread Safely

After compaction, restart, or handoff, recover durable context before editing:

```bash
bd -C REPO prime
bd -C REPO list --assignee "$BEADS_ACTOR" --status in_progress
bd -C REPO show BEAD-ID
bd -C WORKTREE context --json
git -C WORKTREE status --short --branch
```

Do not assume chat scrollback is the authoritative work state.

Before every thread ends:

1. Run the required focused and task-level validation for any code changes.
2. Inspect the worktree's Git status and preserve all needed work.
3. Record branch, commit or dirty state, tests, decisions, blockers, and next action in Beads.
4. Close only if the delivery boundary is actually satisfied; otherwise leave the issue open or in progress with a resumable handoff.
5. Follow the active commit, code-push, Dolt-sync, and cleanup authority.
6. Report changed files, validation, Beads status, and any authorized action that remains undone.

Ending a Codex thread does not complete its bead. Closing a bead does not remove or preserve its worktree automatically.

Keep task-specific context in issue fields, notes, and comments. Store durable project-wide knowledge with `bd remember`; do not create an ad hoc `MEMORY.md` alongside the tracker.

## Clean Up Safely

Before removal, verify the branch is integrated or preserved, the worktree is clean, no stash or untracked artifact is stranded, and required remote state is published under the active policy.

Prefer Beads' checked removal when available:

```bash
bd -C REPO worktree list
bd -C REPO worktree remove WORKTREE-NAME
git -C REPO worktree prune
```

Do not manually delete a live worktree as normal cleanup. Do not force removal to hide uncommitted or unpushed work.

## Stop Conditions

Stop mutations and report the exact condition when any of these occur:

- Beads `project_id`, directory, database, or mode differs between sibling worktrees.
- An embedded database is locked by another live writer.
- A task lacks an issue ID, owner, acceptance criteria, or path boundary in a coordinated fan-out.
- A requested edit overlaps another active owner's paths.
- A target worktree contains unrelated dirty or untracked changes.
- A Dolt pull or push reports divergence or conflicts.
- Recovery appears to require force, lock deletion, database reinitialization, worktree deletion, or backend migration.
- The merge slot is held by another actor.

Use `references/conflict-and-recovery.md` for the safe response. Do not improvise destructive recovery.

## Reference Routing

- `references/role-runbooks.md`: read for coordinator, worker/thread, reviewer, integrator, remote-clone, spawn, handoff, or cleanup duties.
- `references/task-contracts.md`: read when creating or reviewing bead scope, dispatching an agent, documenting a handoff, or recording integration.
- `references/conflict-and-recovery.md`: read for backend selection, remote-sync planning, JSONL policy, context mismatch, database locks, duplicate claims, Dolt conflicts, stuck merge slots, or safe recovery.
