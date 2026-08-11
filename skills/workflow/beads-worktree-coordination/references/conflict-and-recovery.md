# Conflict And Recovery Guide

Stop other writers before diagnosing tracker state. Preserve every potentially authoritative database until reconciliation is verified.

## Source-Of-Truth Map

| Artifact | Purpose | Coordination rule |
|---|---|---|
| Local Dolt database | Canonical local issue state and history | All sibling worktrees use one database. |
| Dolt remote | Cross-clone issue synchronization | Pull and push at coordinator-controlled boundaries. |
| `.beads/config.yaml` and metadata | Tracked workspace configuration and identity | Keep small configuration changes intentional and reviewable. |
| `.beads/issues.jsonl` | Optional export for viewers, interchange, or backup assistance | Never treat as canonical sync or conflict resolution. |
| Git branches | Code history | Independent from Dolt issue history. |
| Git worktrees | Isolated checkout, index, and `HEAD` | One implementation effort per branch/worktree. |

Normal Git pull, merge, checkout, or push does not replace Dolt synchronization. Routine JSONL import does not replace `bd dolt pull` and cannot reconstruct full history or reliably infer deletions.

## Backend Decision

| Situation | Preferred model |
|---|---|
| One person, several worktrees, serialized tracker updates | Embedded Dolt |
| Several agents read while one coordinator writes tracker state | Embedded Dolt plus `bd --readonly` workers |
| Several agents claim, comment, update, or close concurrently | Dolt server mode |
| Several independent clones collaborate | Either backend per clone, plus disciplined Dolt remote synchronization |

Embedded mode is single-writer and file-locked. Do not interpret successful concurrent code editing as proof that concurrent Beads mutations are safe.

## Safe Backend Migration Boundary

Treat migration of an existing workspace as a separate authorized operation:

1. Quiesce every Beads writer.
2. Record `bd --version`, `bd where`, `bd context --json`, issue count, project ID, backend mode, and remotes.
3. Create a full Dolt backup using the installed version's `bd backup` workflow.
4. Verify the backup before changing backend configuration.
5. Restore into the target server-mode workspace according to version-specific CLI help.
6. Verify identity, counts, dependencies, recent issue history, and remote configuration.
7. Archive the former store until the new authoritative store has been checkpointed and synchronized.

Do not use JSONL as the only migration backup. Do not run `bd init --server` blindly over a live embedded store. Do not allow two stores with the same project identity to remain active.

## Workspace Mismatch

Symptoms:

- different `project_id`, Beads directory, database, or mode between sibling worktrees;
- an unexpected local `.beads` directory in a linked worktree;
- an inherited `BEADS_DIR` points outside the intended project;
- agents see different issue counts or claims.

Response:

1. Stop all Beads writes.
2. Capture `bd where` and `bd context --json` from every affected worktree.
3. Inspect `BEADS_DIR` without changing it.
4. Back up every candidate workspace.
5. Designate the authoritative workspace only after comparing project IDs and unique issue history.
6. Reconfigure or archive the duplicate through a reviewed, non-destructive process.

Do not delete the extra workspace merely because its path looks wrong.

## Embedded Lock Contention

Symptoms include `database is locked`, timeouts, or another `bd` process holding the embedded store.

Response:

1. Stop launching new `bd` mutations.
2. Determine whether another live process is legitimately using the store.
3. Wait or serialize commands through the coordinator.
4. Use read-only workers when possible.
5. If contention is routine, plan a server-mode migration.

Never remove a lock while a live owner may exist. Lock deletion is recovery, not concurrency control.

## Duplicate Claims Across Clones

Atomic claim protects one shared backend. Two disconnected local databases can both accept a claim.

Prevention:

- assign remotely coordinated work before disconnection;
- pull before selection when authorized;
- push claims immediately when authorized;
- use one coordinator or shared server for high-contention queues.

Resolution:

1. Stop both implementations from expanding scope.
2. Compare progress, branches, and path ownership.
3. Select one owner or repartition into disjoint beads.
4. Record the decision and dependencies in Beads.
5. Preserve useful work from the non-owner through a new bounded task or handoff.

## Dolt Pull Or Push Conflict

1. Stop other tracker writers.
2. Back up the local Dolt workspace.
3. Capture the exact command, version, branch, remote, and error.
4. Designate one resolver.
5. Follow the installed CLI's merge or doctor guidance; feature availability differs by backend and version.
6. Verify issue counts, claims, dependencies, recent changes, and version-control status.
7. Push the reconciled state only after verification and authorization.

Do not retry with `--force` merely to make the command pass. A force push can overwrite remote tracker history.

## JSONL Churn Or Git Conflicts

If `.beads/issues.jsonl` changes across feature branches:

- Prefer disabling automatic export when no integration consumes it.
- Otherwise designate the main or integration worktree as the sole exporter and committer.
- Exclude generated Beads exports from feature commits unless repository policy explicitly requires them.
- Regenerate once after Dolt state is reconciled.

Do not choose one feature branch's JSONL as the winning database state.

## Overlapping Code Ownership

When two workers need the same path:

1. Stop edits to the overlap.
2. Record the collision in both beads.
3. Choose one of: transfer ownership, add a blocking dependency, combine tasks, or create a fan-in bead.
4. Update dispatch contracts and worktree instructions.
5. Resume only after one active owner remains.

For lockfiles, generated indexes, migration chains, schemas, and central registries, default to one integration owner.

## Merge Slot Held Or Stuck

1. Run `bd merge-slot check` and identify the holder.
2. Contact or inspect the holder's active integration work and Beads state.
3. Do not acquire by force or start a parallel merge.
4. Release only when the holder confirms completion or a coordinator verifies that the holder is gone and no integration is active.
5. Document any administrative release in the relevant issue.

## Dirty Or Stale Worktree

Before cleanup, inspect:

```bash
git -C WORKTREE status --short --branch
git -C REPO worktree list --porcelain
```

If needed work remains, preserve it on a branch or through an authorized commit and push. Prefer `bd worktree remove` because it checks uncommitted changes, unpushed commits, and stashes. Use `git worktree prune` only for stale administrative records after the actual worktree is gone.

Do not use recursive filesystem deletion as the normal worktree-removal procedure.

## Recovery Completion Gate

Do not resume concurrent work until all are true:

- one authoritative Beads workspace is identified;
- context matches in every sibling worktree;
- no unexpected writer or lock remains;
- claims and dependencies reflect the agreed ownership;
- the integration and sync actor is explicit;
- backups remain available;
- Git and Dolt status are understood;
- the recovery decision is recorded durably.
