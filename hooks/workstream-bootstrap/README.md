# Durable Workstream Bootstrap Hook

This package gives every local conversation with a durable workspace a consistent Git and Beads starting point. It is intentionally a user-level `SessionStart` hook: the policy follows the workspace
directory supplied by the runtime, whether the conversation originated from a Codex coding task, a project, a work surface, or a chat with an attached durable folder.

The implementation is Python 3.11+ with no third-party dependencies. Python is a better fit than a shell script here because the hook consumes and produces structured JSON, validates paths, invokes
subprocesses without shell interpolation, and has a real unit/integration test surface.

## Policy

| Starting state                                                                                     | Hook action                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Workspace is already inside Git and Beads resolves                                                 | Prime Beads immediately. If a trusted project-local Beads `SessionStart` hook exists, defer to it so full prime context is not injected twice.                                                                             |
| Workspace has no Git repository                                                                    | Run `git init` in the runtime-provided workspace folder.                                                                                                                                                                   |
| Git is new/unborn and its index is empty                                                           | Run `bd init`, verify the single initialization commit, rewrite its message conventionally, then prime. This is the automatic brand-new-workstream path.                                                                   |
| Git is established but Beads is absent                                                             | Inject an approval request into the conversation. Nothing Beads-related changes before James approves.                                                                                                                     |
| James approves                                                                                     | The agent runs the emitted `install --root-token … --approved` command. It requires a completely clean repository, initializes Beads, verifies exactly one direct-child commit, normalizes the commit message, and primes. |
| `.beads` exists but cannot be resolved                                                             | Do not reinitialize. Inject a diagnostic and recommend `bd doctor --agent`.                                                                                                                                                |
| `bd`/`beads` is missing                                                                            | Do not install a machine-wide package silently. Ask James before changing the package-manager/network state.                                                                                                               |
| Workspace is the filesystem root, the home directory itself, Git metadata, or an OS temp directory | Treat it as non-durable and do nothing.                                                                                                                                                                                    |

“Brand new” is deliberately mechanical: Git had to be initialized by the hook, or the selected repository has no `HEAD` commit yet. An unborn repository with staged content is not safe for automatic
Beads setup because Beads 1.1.2 includes pre-staged changes in its initialization commit; it takes the approval path instead.

## Atomic Commit Guarantee

Beads 1.1.2 normally creates a commit during `bd init`. It also absorbs anything already staged, which makes a naive invocation unsafe in an established repository. The approved installer therefore:

1. Acquires a per-workspace startup lock.
2. Requires `git status --porcelain=v1 --untracked-files=all` to be empty.
3. Requires the Git index to be clean independently.
4. Records `HEAD`, runs `bd init --quiet --role maintainer`, and verifies Beads resolves.
5. Verifies that the result is exactly one root/direct-child commit containing `.beads/`.
6. Refuses to amend if Beads left anything staged.
7. Amends only the commit message to:

   ```text
   chore(beads): initialize workstream tracking
   ```

8. Verifies the parent and `.beads/` content again, then requires the established worktree to still be clean.

This prevents unrelated staged, tracked, or untracked work from becoming part of the approved Beads commit. The automatic brand-new path also requires an empty index; pre-existing untracked starter
files are left for the project’s later initial commit unless Beads itself owns one of its integration paths.

The hook fails open. A bootstrap error becomes model-visible diagnostic context rather than blocking the conversation. It never performs a destructive rollback after a third-party command has begun;
if `bd init` itself fails partway through, the diagnostic reports that state for inspection.

## Codex Registration

The canonical declaration is [`codex-hooks.json`](./codex-hooks.json). This installation links it as:

```text
~/.codex/hooks.json -> ~/.agents/hooks/workstream-bootstrap/codex-hooks.json
```

Codex loads the user hook for `startup`, `resume`, and `clear`. It does not run the generic installer after compaction. Once Beads exists, Beads’ project integration owns its compact and
prompt-refresh lifecycle; the generic hook only guarantees a prime when no trusted local `SessionStart` hook will do so.

Codex command hooks are trust-gated. The installed declaration’s exact canonical hash is stored under `hooks.state` in `~/.codex/config.toml` after the package and tests are verified. Changing the
declaration correctly makes Codex request another trust review.

The JSON envelope is also Claude-style hook compatible. Another client can point its user-level `SessionStart` hook at the same command:

```text
python3 ~/.agents/hooks/workstream-bootstrap/workstream_bootstrap.py session-start
```

That client must provide a JSON object with at least `cwd` on stdin. Client registration is kept outside this package because each runtime owns a different settings file and trust model.

## Commands

Inspect without changing a workspace:

```bash
python3 ~/.agents/hooks/workstream-bootstrap/workstream_bootstrap.py status \
  --root /absolute/path/to/workspace
```

Exercise the hook protocol directly:

```bash
printf '%s' '{"hook_event_name":"SessionStart","cwd":"/absolute/path","source":"startup"}' \
  | python3 ~/.agents/hooks/workstream-bootstrap/workstream_bootstrap.py session-start
```

The established-workstream install command is intentionally not presented as a general manual shortcut. The hook emits a URL-safe root token and the required `--approved` flag only when the
conversation needs James’s decision.

## Environment Controls

- `WORKSTREAM_BOOTSTRAP_DISABLE=1` — return a quiet, successful hook response without inspection or mutation.
- `WORKSTREAM_BOOTSTRAP_GIT=/absolute/path/to/git` — override Git executable discovery.
- `WORKSTREAM_BOOTSTRAP_BD=/absolute/path/to/bd` — override Beads executable discovery.
- `WORKSTREAM_BOOTSTRAP_ALLOW_TRANSIENT=1` — allow temp-directory workspaces. This exists for isolated tests and deliberate experiments; it should not be set in normal sessions.
- `CODEX_HOME=/path/to/codex-home` — used only to verify the trust hash of a project-local Beads hook before suppressing duplicate prime output.

## Tests

The standard suite uses real Git repositories in temporary directories and a deterministic fake Beads executable. It covers Git initialization, automatic setup and priming, established-project
approval, dirty-tree refusal, commit ancestry/message verification, existing and broken Beads states, root-token safety, and Codex project-hook trust hashing.

```bash
python3 -m unittest discover -s \
  ~/.agents/hooks/workstream-bootstrap/tests -v
```

An opt-in smoke test uses the installed real `bd` binary in an isolated temporary repository:

```bash
RUN_REAL_BEADS_INTEGRATION=1 python3 -m unittest discover -s \
  ~/.agents/hooks/workstream-bootstrap/tests -v
```

Neither test mode touches an existing project.
