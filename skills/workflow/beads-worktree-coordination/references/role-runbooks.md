# Role Runbooks

Use the runbook matching the role. One person or agent may hold several roles in a small workflow, but keep the transitions explicit.

## Coordinator

### Before fan-out

1. Read the active repository instructions and run `bd prime`.
2. Inspect Git status, active worktrees, Beads context, backend mode, and configured Dolt remote.
3. Resolve the exact base branch and commit.
4. Pull remote code and Beads state only when authorized and while local writers are quiescent.
5. Create or inspect the parent bead and its child tasks.
6. Ensure each task has acceptance criteria, owned paths, excluded paths, dependencies, required tests, and handoff requirements.
7. Convert path overlap into sequencing or an integration bead.
8. Assign a unique actor identity, bead ID, branch, and worktree path to every worker.
9. Create worktrees from the same approved base unless a dependency requires a later base.
10. Verify `bd context --json` in every worktree before dispatch.

### Dispatch payload

Pass each worker all of the following:

- absolute repository and worktree paths;
- bead ID and actor identity;
- branch and base commit;
- owned and excluded paths;
- outcome and acceptance criteria;
- required tests;
- known sibling tasks and shared hotspots;
- commit, push, sync, and close authority;
- required handoff format.

Never assume a spawned agent has a separate checkout. In shared-filesystem agent systems, the parent must either give the worker an isolated worktree or enforce disjoint file ownership.

### During fan-out

- Monitor `bd list --status=in_progress --json` and dependency state.
- Do not edit worker-owned paths from the coordinator worktree.
- Route scope changes through Beads comments, notes, updates, or new issues.
- Keep remote Dolt pulls out of worker loops. Schedule synchronization boundaries.
- Stop and resequence when workers discover overlap.

### Before fan-in

1. Ensure every worker has left a complete handoff.
2. Confirm branches and commits exist and tests were actually run.
3. Confirm the integration worktree is clean.
4. Ensure the project merge slot exists; if it is absent, create it once only when authorized.
5. Hand control to one integrator.
6. Quiesce other merge and tracker-sync activity during the integration checkpoint.

## Worker Or Thread

### Startup

1. Confirm the supplied absolute worktree path and run all commands there.
2. Set the supplied `BEADS_ACTOR`.
3. Run `bd prime`, `bd where`, `bd context --json`, and `git status --short --branch`.
4. Verify the expected bead, project ID, branch, base, owned paths, and acceptance criteria.
5. Inspect and claim the bead. If it is held by another actor, stop.
6. Do not create a second `.beads` directory or redirect `BEADS_DIR` without coordinator authorization.

### Execution

- Edit only owned paths.
- Treat excluded and sibling-owned paths as read-only context.
- Ask the coordinator to transfer ownership or add a dependency before crossing a boundary.
- Create a discovered-from follow-up bead for new durable work instead of expanding the current task silently.
- Keep code, tests, and generated changes scoped to the same contract.
- Run the narrowest meaningful validation, then the required task-level gates.
- Do not pull Beads remotely just to see sibling updates; a shared local workspace already contains them.
- Do not commit, push, close, or sync unless the dispatch contract grants that authority.

### Handoff

Record:

- branch and head commit, or state clearly that changes are uncommitted;
- exact changed paths;
- tests and results;
- acceptance-criteria status;
- known conflicts or integration ordering;
- follow-up bead IDs;
- remaining dirty or untracked files.

Mark ready for review according to project convention. Do not close an implementation bead whose delivery boundary includes merge or integration validation.

### Resume after restart or compaction

1. Run `bd prime`.
2. Find the actor's in-progress issue and inspect it before editing.
3. Reconfirm Beads context, branch, Git status, owned paths, and the last durable handoff.
4. Compare the worktree head and dirty state with the recorded handoff.
5. Resume only when they agree; otherwise stop and reconcile the discrepancy.

If ending while incomplete, leave a resumable handoff and keep the bead open or in progress. Never close work simply to make the session checklist look complete.

## Reviewer Or Validator

1. Do not claim or reassign the implementation bead unless review ownership is explicitly transferred.
2. Prefer `bd --readonly` for tracker inspection.
3. Review the task contract, diff, changed paths, test evidence, and acceptance criteria.
4. Check for scope expansion, sibling-path edits, generated-file drift, and hidden runtime coupling.
5. Record actionable findings in the designated review bead or handoff channel.
6. Do not repair the worker's branch unless the user or coordinator requested implementation.
7. If the review itself changes code, it becomes a separately owned implementation effort with its own bead and worktree.

## Integrator

### Acquire and verify

1. Work from the designated clean integration worktree.
2. Confirm all candidate branches and handoff commits.
3. Inspect `bd merge-slot check`; if no slot exists, ask the coordinator to create it rather than inventing another lock.
4. Acquire the slot with a unique holder identity.
5. If acquisition fails, do not merge concurrently and do not steal the slot.

### Integrate

1. Integrate one branch at a time in dependency order.
2. Resolve conflicts centrally or return a clearly bounded correction to the original owner.
3. Keep shared-file and generated-output decisions in the integration lane.
4. Run focused gates after each risky integration and full required gates at fan-in.
5. Record the resulting integration commit and gate results in Beads.

### Complete or reject

- On success, close only the beads whose acceptance criteria and delivery boundary are satisfied.
- On failure, leave the issue open or in progress, document the exact blocker, and remove any premature review-ready marker.
- Release the merge slot on every exit path.
- Publish tracker and code state only under the active authority policy.

### Cleanup decision

Approve worktree removal only after confirming:

- the change is integrated or its branch is preserved remotely;
- no uncommitted, untracked, or stashed work is needed;
- the final Beads state is durable;
- no dependent task still needs the worktree environment.

## Remote Clone Participant

Worktrees within one clone share a local Beads workspace; separate clones do not. For cross-clone coordination:

1. Pull before selecting work when authorized.
2. Claim atomically in the local database.
3. Push the claim immediately when authorized so other clones can observe it.
4. Treat remote rejection or divergence as a synchronization conflict, not permission to force.
5. Pull and reconcile through one designated resolver.

Because two offline clones can both claim the same issue, coordinator assignment is safer than self-selection during disconnected operation.

## Single-Worktree Exception

Parallel agents may share one worktree only when all of the following hold:

- owned paths are explicitly disjoint;
- no worker will run a formatter, generator, dependency update, or repository-wide rewrite that touches sibling paths;
- tests and build output will not overwrite shared mutable state;
- one agent owns any shared files;
- the coordinator can stop the group immediately if overlap appears.

Otherwise, create linked worktrees or run the tasks sequentially.
