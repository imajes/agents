#!/usr/bin/env python3
"""Prime Git and Beads at the beginning of a durable agent workstream.

The hook accepts the Claude/Codex SessionStart JSON object on stdin and emits a
SessionStart hook response on stdout. It deliberately fails open: bootstrap
problems become model-visible context, never a blocked conversation.

The explicit ``install --approved`` command is the second half of the approval
flow for established repositories. It refuses a dirty repository, asks Beads
to initialize the project, and verifies/amends the resulting single commit.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import dataclasses
import enum
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Iterator, Mapping, Sequence, TextIO

try:
    import fcntl
except ImportError:  # pragma: no cover - the installed hook targets macOS/POSIX.
    fcntl = None  # type: ignore[assignment]

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ is documented.
    tomllib = None  # type: ignore[assignment]


VERSION = "1.0.0"
HOOK_EVENT_NAME = "SessionStart"
DEFAULT_COMMAND_TIMEOUT_SECONDS = 90
MAX_DIAGNOSTIC_CHARS = 2_000
COMMIT_MESSAGE = """chore(beads): initialize workstream tracking

- Workstream:
  - add the Beads database and repository metadata
  - install agent guidance and lifecycle integrations
- Bootstrap:
  - make Beads available to new conversations in this workspace
"""


class BootstrapError(RuntimeError):
    """An expected bootstrap failure with a safe, user-facing explanation."""


class BeadsKind(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    BROKEN = "broken"
    CLI_MISSING = "cli_missing"


@dataclasses.dataclass(frozen=True)
class CommandResult:
    args: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


@dataclasses.dataclass(frozen=True)
class GitState:
    root: Path
    created: bool
    has_head: bool


@dataclasses.dataclass(frozen=True)
class BeadsState:
    kind: BeadsKind
    resolved_path: Path | None = None
    diagnostic: str = ""


@dataclasses.dataclass(frozen=True)
class InstallResult:
    root: Path
    commit: str
    automatic: bool


class CommandRunner:
    """Run argument-vector commands without invoking a shell."""

    def run(
        self,
        args: Sequence[str | os.PathLike[str]],
        *,
        cwd: Path | None = None,
        input_text: str | None = None,
        timeout: int = DEFAULT_COMMAND_TIMEOUT_SECONDS,
    ) -> CommandResult:
        normalized = tuple(os.fspath(arg) for arg in args)
        try:
            completed = subprocess.run(
                normalized,
                cwd=os.fspath(cwd) if cwd is not None else None,
                input=input_text,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=timeout,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise BootstrapError(
                f"could not run {normalized[0]!r}: {exc}"
            ) from exc
        return CommandResult(
            args=normalized,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )


def _diagnostic(text: str) -> str:
    clean = text.strip()
    if len(clean) <= MAX_DIAGNOSTIC_CHARS:
        return clean
    return clean[:MAX_DIAGNOSTIC_CHARS] + "\n[diagnostic truncated]"


def _require_success(result: CommandResult, purpose: str) -> CommandResult:
    if result.returncode == 0:
        return result
    detail = _diagnostic(result.stderr or result.stdout)
    suffix = f": {detail}" if detail else ""
    raise BootstrapError(f"{purpose} failed (exit {result.returncode}){suffix}")


def _resolve_executable(env_name: str, candidates: Sequence[str]) -> str | None:
    override = os.environ.get(env_name)
    if override:
        if os.path.sep in override:
            candidate = Path(override).expanduser()
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return os.fspath(candidate.resolve())
            return None
        return shutil.which(override)
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def _git(runner: CommandRunner, git: str, root: Path, *args: str) -> CommandResult:
    return runner.run((git, "-C", root, *args))


def _find_git_root(runner: CommandRunner, git: str, cwd: Path) -> Path | None:
    result = _git(runner, git, cwd, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    if not value:
        return None
    return Path(value).expanduser().resolve()


def _git_has_head(runner: CommandRunner, git: str, root: Path) -> bool:
    result = _git(runner, git, root, "rev-parse", "--verify", "HEAD^{commit}")
    return result.returncode == 0


def _git_head(runner: CommandRunner, git: str, root: Path) -> str | None:
    result = _git(runner, git, root, "rev-parse", "--verify", "HEAD^{commit}")
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def _git_status(runner: CommandRunner, git: str, root: Path) -> str:
    result = _require_success(
        _git(
            runner,
            git,
            root,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ),
        "reading Git status",
    )
    return result.stdout.rstrip()


def _git_index_is_clean(runner: CommandRunner, git: str, root: Path) -> bool:
    result = _git(
        runner,
        git,
        root,
        "diff",
        "--cached",
        "--quiet",
        "--ignore-submodules",
        "--",
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise BootstrapError(
        "checking the Git index failed"
        + (f": {_diagnostic(result.stderr)}" if result.stderr.strip() else "")
    )


def ensure_git(runner: CommandRunner, git: str, cwd: Path) -> GitState:
    root = _find_git_root(runner, git, cwd)
    created = False
    if root is None:
        _require_success(
            _git(runner, git, cwd, "init"),
            f"initializing Git in {cwd}",
        )
        created = True
        root = _find_git_root(runner, git, cwd)
        if root is None:
            raise BootstrapError(
                f"Git initialized in {cwd}, but its worktree root could not be resolved"
            )
    return GitState(root=root, created=created, has_head=_git_has_head(runner, git, root))


def _transient_roots() -> tuple[Path, ...]:
    candidates = {
        Path(tempfile.gettempdir()).resolve(),
        Path("/tmp").resolve(),
        Path("/private/tmp").resolve(),
        Path("/var/tmp").resolve(),
    }
    return tuple(sorted(candidates, key=lambda path: len(path.parts)))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_durable_workspace(path: Path, *, allow_transient: bool = False) -> Path:
    try:
        resolved = path.expanduser().resolve(strict=True)
    except OSError as exc:
        raise BootstrapError(f"workspace path cannot be resolved: {exc}") from exc
    if not resolved.is_dir():
        raise BootstrapError(f"workspace path is not a directory: {resolved}")
    if resolved == Path(resolved.anchor):
        raise BootstrapError("the filesystem root is not a workstream")
    if resolved == Path.home().resolve():
        raise BootstrapError("the home directory itself is not a workstream")
    if ".git" in resolved.parts:
        raise BootstrapError("Git metadata directories are not workstreams")
    if not allow_transient:
        for transient_root in _transient_roots():
            if resolved == transient_root or _is_within(resolved, transient_root):
                raise BootstrapError(
                    f"transient workspace is intentionally skipped: {resolved}"
                )
    return resolved


def inspect_beads(
    runner: CommandRunner,
    bd: str | None,
    root: Path,
) -> BeadsState:
    if bd is None:
        return BeadsState(
            BeadsKind.CLI_MISSING,
            diagnostic="neither the bd nor beads executable is available on PATH",
        )
    result = runner.run((bd, "where", "--json"), cwd=root)
    if result.returncode == 0:
        try:
            payload = json.loads(result.stdout)
            resolved = Path(payload["path"]).expanduser().resolve()
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, OSError) as exc:
            return BeadsState(
                BeadsKind.BROKEN,
                diagnostic=f"bd where returned unusable JSON: {exc}",
            )
        return BeadsState(BeadsKind.PRESENT, resolved_path=resolved)
    diagnostic = _diagnostic(result.stderr or result.stdout)
    if (root / ".beads").exists() or (root / ".beads").is_symlink():
        return BeadsState(BeadsKind.BROKEN, diagnostic=diagnostic)
    return BeadsState(BeadsKind.ABSENT, diagnostic=diagnostic)


def _parse_prime_output(output: str) -> str:
    try:
        payload = json.loads(output)
        specific = payload.get("hookSpecificOutput", {})
        context = specific.get("additionalContext")
    except (AttributeError, json.JSONDecodeError):
        context = None
    if isinstance(context, str) and context.strip():
        return context.strip()
    stripped = output.strip()
    if stripped and not stripped.startswith(("{", "[")):
        return stripped
    raise BootstrapError("bd prime returned neither hook context nor plain text")


def prime_beads(runner: CommandRunner, bd: str, root: Path) -> str:
    result = _require_success(
        runner.run((bd, "prime", "--hook-json"), cwd=root),
        "priming Beads",
    )
    return _parse_prime_output(result.stdout)


def _commit_parents(
    runner: CommandRunner,
    git: str,
    root: Path,
    commit: str,
) -> tuple[str, ...]:
    result = _require_success(
        _git(runner, git, root, "rev-list", "--parents", "-n", "1", commit),
        "verifying the Beads commit",
    )
    parts = result.stdout.strip().split()
    if not parts or parts[0] != commit:
        raise BootstrapError("Git returned an unexpected commit-parent record")
    return tuple(parts[1:])


def _verify_single_commit(
    runner: CommandRunner,
    git: str,
    root: Path,
    before: str | None,
    after: str,
) -> None:
    parents = _commit_parents(runner, git, root, after)
    if before is None:
        if parents:
            raise BootstrapError(
                "Beads initialization did not produce a single root commit"
            )
    elif parents != (before,):
        raise BootstrapError(
            "Beads initialization did not produce one direct-child commit"
        )


def _commit_contains_beads(
    runner: CommandRunner,
    git: str,
    root: Path,
    commit: str,
) -> bool:
    result = _require_success(
        _git(
            runner,
            git,
            root,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "--root",
            commit,
        ),
        "inspecting the Beads commit",
    )
    return any(
        path == ".beads" or path.startswith(".beads/")
        for path in result.stdout.splitlines()
    )


def _create_fallback_commit(
    runner: CommandRunner,
    git: str,
    root: Path,
) -> str:
    _require_success(_git(runner, git, root, "add", "-A"), "staging Beads files")
    _require_success(
        runner.run(
            (git, "-C", root, "commit", "-F", "-"),
            input_text=COMMIT_MESSAGE,
        ),
        "creating the Beads commit",
    )
    head = _git_head(runner, git, root)
    if head is None:
        raise BootstrapError("Git did not create the requested Beads commit")
    return head


def _amend_commit_message(
    runner: CommandRunner,
    git: str,
    root: Path,
) -> str:
    if not _git_index_is_clean(runner, git, root):
        raise BootstrapError(
            "Beads left staged changes after its initialization commit; refusing to amend"
        )
    _require_success(
        runner.run(
            (git, "-C", root, "commit", "--amend", "-F", "-"),
            input_text=COMMIT_MESSAGE,
        ),
        "normalizing the Beads commit message",
    )
    head = _git_head(runner, git, root)
    if head is None:
        raise BootstrapError("Git lost HEAD while amending the Beads commit")
    return head


def initialize_beads(
    runner: CommandRunner,
    *,
    bd: str,
    git: str,
    root: Path,
    automatic: bool,
) -> InstallResult:
    state = inspect_beads(runner, bd, root)
    if state.kind is BeadsKind.PRESENT:
        head = _git_head(runner, git, root)
        return InstallResult(root=root, commit=head or "", automatic=automatic)
    if state.kind is BeadsKind.BROKEN:
        raise BootstrapError(
            "a .beads marker exists, but Beads cannot resolve it; reinitialization is unsafe"
            + (f": {state.diagnostic}" if state.diagnostic else "")
        )

    before_status = _git_status(runner, git, root)
    before_head = _git_head(runner, git, root)
    if not automatic and before_status:
        raise BootstrapError(
            "the established Git worktree is not clean; commit, stash, or remove its "
            "changes before approving Beads initialization:\n"
            + _diagnostic(before_status)
        )
    if not _git_index_is_clean(runner, git, root):
        raise BootstrapError(
            "the Git index contains staged changes; bd init would absorb them into its commit"
        )

    init_result = runner.run(
        (bd, "init", "--quiet", "--role", "maintainer"),
        cwd=root,
        timeout=120,
    )
    _require_success(init_result, "initializing Beads")

    resolved = inspect_beads(runner, bd, root)
    if resolved.kind is not BeadsKind.PRESENT:
        raise BootstrapError(
            "bd init returned success, but the initialized Beads workspace cannot be resolved"
        )

    after_head = _git_head(runner, git, root)
    if after_head == before_head or after_head is None:
        if automatic:
            raise BootstrapError(
                "bd init did not create its expected commit; the automatic path will not "
                "stage pre-existing files"
            )
        after_head = _create_fallback_commit(runner, git, root)

    _verify_single_commit(runner, git, root, before_head, after_head)
    if not _commit_contains_beads(runner, git, root, after_head):
        raise BootstrapError("the initialization commit does not contain .beads metadata")

    final_head = _amend_commit_message(runner, git, root)
    _verify_single_commit(runner, git, root, before_head, final_head)
    if not _commit_contains_beads(runner, git, root, final_head):
        raise BootstrapError("the amended initialization commit lost .beads metadata")

    if not automatic:
        after_status = _git_status(runner, git, root)
        if after_status:
            raise BootstrapError(
                "Beads committed successfully, but the established worktree is no longer clean:\n"
                + _diagnostic(after_status)
            )

    return InstallResult(root=root, commit=final_head, automatic=automatic)


def _canonical_hook_hash(group: Mapping[str, Any], handler: Mapping[str, Any]) -> str:
    normalized_handler: dict[str, Any] = {
        "type": "command",
        "command": handler["command"],
        "timeout": max(1, int(handler.get("timeout", 600))),
        "async": bool(handler.get("async", False)),
    }
    if handler.get("statusMessage") is not None:
        normalized_handler["statusMessage"] = handler["statusMessage"]
    context_limit = handler.get("additionalContextLimit")
    if context_limit is not None and int(context_limit) != 2_500:
        normalized_handler["additionalContextLimit"] = int(context_limit)
    identity: dict[str, Any] = {
        "event_name": "session_start",
        "hooks": [normalized_handler],
    }
    if group.get("matcher") is not None:
        identity["matcher"] = group["matcher"]
    serialized = json.dumps(
        identity,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(serialized).hexdigest()


_BEADS_SESSION_COMMAND = re.compile(
    r"(?:^|[;&|]\s*|\s)(?:bd|beads)\s+codex-hook\s+SessionStart(?:\s|$)"
)


def _read_codex_hook_state() -> Mapping[str, Any]:
    if tomllib is None:
        return {}
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    for config_path in (
        codex_home / "config.toml",
        codex_home / "config" / "config.toml",
    ):
        try:
            with config_path.open("rb") as handle:
                payload = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError):
            continue
        state = payload.get("hooks", {}).get("state", {})
        if isinstance(state, Mapping):
            return state
    return {}


def project_has_trusted_beads_session_hook(root: Path) -> bool:
    """Return true when Codex will run a project-local Beads SessionStart hook.

    This prevents duplicate full ``bd prime`` context. The trust hash is
    recomputed with Codex's canonical algorithm; merely having a hook file or a
    stale trust record is not enough.
    """

    hook_path = root / ".codex" / "hooks.json"
    try:
        payload = json.loads(hook_path.read_text(encoding="utf-8"))
        groups = payload.get("hooks", {}).get("SessionStart", [])
    except (OSError, AttributeError, json.JSONDecodeError):
        return False
    if not isinstance(groups, list):
        return False
    state = _read_codex_hook_state()
    canonical_hook_path = hook_path.resolve()
    for group_index, group in enumerate(groups):
        if not isinstance(group, Mapping):
            continue
        handlers = group.get("hooks", [])
        if not isinstance(handlers, list):
            continue
        for handler_index, handler in enumerate(handlers):
            if not isinstance(handler, Mapping) or handler.get("type") != "command":
                continue
            command = handler.get("command")
            if not isinstance(command, str) or not _BEADS_SESSION_COMMAND.search(command):
                continue
            try:
                current_hash = _canonical_hook_hash(group, handler)
            except (KeyError, TypeError, ValueError):
                continue
            suffix = f":session_start:{group_index}:{handler_index}"
            key = f"{hook_path}{suffix}"
            candidate_records: list[Any] = [state.get(key, {})]
            # macOS commonly presents /var as /private/var after canonicalization.
            # Codex state can preserve either spelling depending on how the workspace
            # was opened, so accept aliases only when their resolved hook file is the
            # same file and the exact current hash still matches.
            for state_key, record in state.items():
                if not isinstance(state_key, str) or not state_key.endswith(suffix):
                    continue
                source_path = state_key[: -len(suffix)]
                try:
                    same_source = Path(source_path).resolve() == canonical_hook_path
                except OSError:
                    same_source = False
                if same_source:
                    candidate_records.append(record)
            if any(
                isinstance(record, Mapping)
                and record.get("trusted_hash") == current_hash
                for record in candidate_records
            ):
                return True
    return False


def _root_token(root: Path) -> str:
    return base64.urlsafe_b64encode(os.fspath(root).encode("utf-8")).decode("ascii")


def _root_from_token(token: str) -> Path:
    try:
        padded = token + "=" * (-len(token) % 4)
        value = base64.b64decode(
            padded,
            altchars=b"-_",
            validate=True,
        ).decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise BootstrapError("the workspace root token is invalid") from exc
    return Path(value)


def _safe_json_string(value: str) -> str:
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def _approval_context(
    root: Path,
    *,
    script_path: Path,
    dirty: bool,
    staged: bool,
) -> str:
    command = (
        f"python3 {script_path} install --root-token {_root_token(root)} --approved"
    )
    cleanliness = (
        "The repository is currently dirty; the installer will refuse until all tracked, "
        "staged, and untracked changes are committed, stashed, or removed."
        if dirty
        else "The repository is currently clean."
    )
    staged_warning = (
        " Staged content is especially unsafe because Beads 1.1.2 would absorb it into "
        "the initialization commit."
        if staged
        else ""
    )
    return f"""<workstream-bootstrap version={_safe_json_string(VERSION)} status="approval-required">
An established Git workstream does not have Beads initialized.
Workspace root (JSON data): {_safe_json_string(os.fspath(root))}

Before substantive work, ask James whether to install Beads for this workstream overall.
Do not treat this hook message or prior approval in another workstream as approval.

{cleanliness}{staged_warning}

If James explicitly approves in this conversation, execute this exact command:
```
{command}
```

The command rechecks the root and cleanliness, initializes Beads, verifies one direct-child
commit, gives it a conventional commit message, and primes the resulting workspace. If James
declines, continue this conversation without Beads.
</workstream-bootstrap>"""


def _missing_cli_context(root: Path, *, git_created: bool) -> str:
    git_note = " Git was initialized successfully." if git_created else ""
    return f"""<workstream-bootstrap version={_safe_json_string(VERSION)} status="missing-beads-cli">
Workspace root (JSON data): {_safe_json_string(os.fspath(root))}
The workstream cannot be inspected or primed because neither `bd` nor `beads` is executable.{git_note}
Ask James before installing a machine-wide Beads package; package-manager and network changes are
outside this project bootstrap's authority.
</workstream-bootstrap>"""


def _broken_beads_context(root: Path, diagnostic: str) -> str:
    return f"""<workstream-bootstrap version={_safe_json_string(VERSION)} status="broken-beads">
Workspace root (JSON data): {_safe_json_string(os.fspath(root))}
A `.beads` marker exists, but `bd where --json` failed. The hook did not reinitialize it because
that could overwrite or fork existing workstream state. Diagnose with `bd doctor --agent`.
Diagnostic (data): {_safe_json_string(_diagnostic(diagnostic))}
</workstream-bootstrap>"""


def _error_context(root: Path | None, message: str) -> str:
    root_line = (
        f"\nWorkspace root (JSON data): {_safe_json_string(os.fspath(root))}"
        if root is not None
        else ""
    )
    return f"""<workstream-bootstrap version={_safe_json_string(VERSION)} status="error">{root_line}
The automatic Git/Beads bootstrap did not complete. Continue the conversation, but report this
bootstrap problem before relying on Beads.
Diagnostic (data): {_safe_json_string(_diagnostic(message))}
</workstream-bootstrap>"""


def _hook_response(
    context: str | None = None,
    *,
    system_message: str | None = None,
    suppress_output: bool = False,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "continue": True,
        "suppressOutput": suppress_output,
    }
    if system_message:
        response["systemMessage"] = system_message
    if context:
        response["hookSpecificOutput"] = {
            "hookEventName": HOOK_EVENT_NAME,
            "additionalContext": context,
        }
    return response


def _read_session_start(stream: TextIO) -> dict[str, Any]:
    raw = stream.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"SessionStart stdin is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise BootstrapError("SessionStart stdin must be a JSON object")
    event_name = payload.get("hook_event_name", HOOK_EVENT_NAME)
    if event_name != HOOK_EVENT_NAME:
        raise BootstrapError(f"expected {HOOK_EVENT_NAME}, received {event_name!r}")
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        raise BootstrapError("SessionStart input does not contain a non-empty cwd")
    return payload


@contextlib.contextmanager
def workspace_lock(root: Path) -> Iterator[None]:
    """Serialize concurrent startup hooks for the same workspace."""

    digest = hashlib.sha256(os.fspath(root).encode("utf-8")).hexdigest()[:24]
    lock_path = Path(tempfile.gettempdir()) / f"agents-workstream-bootstrap-{digest}.lock"
    handle = lock_path.open("a+", encoding="utf-8")
    try:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def _allow_transient() -> bool:
    return os.environ.get("WORKSTREAM_BOOTSTRAP_ALLOW_TRANSIENT") == "1"


def _session_start(
    payload: Mapping[str, Any],
    *,
    runner: CommandRunner,
    script_path: Path,
) -> dict[str, Any]:
    if os.environ.get("WORKSTREAM_BOOTSTRAP_DISABLE") == "1":
        return _hook_response(suppress_output=True)
    source = payload.get("source", "startup")
    try:
        cwd = validate_durable_workspace(
            Path(str(payload["cwd"])),
            allow_transient=_allow_transient(),
        )
    except BootstrapError:
        # A missing/transient/non-workspace cwd is not a durable workstream and should
        # not create model noise on every conversation.
        return _hook_response(suppress_output=True)

    git = _resolve_executable("WORKSTREAM_BOOTSTRAP_GIT", ("git",))
    bd = _resolve_executable("WORKSTREAM_BOOTSTRAP_BD", ("bd", "beads"))
    if git is None:
        return _hook_response(
            _error_context(cwd, "Git is not executable; the workstream cannot be initialized")
        )

    try:
        with workspace_lock(cwd):
            git_state = ensure_git(runner, git, cwd)
            root = git_state.root
            beads_state = inspect_beads(runner, bd, root)

            if beads_state.kind is BeadsKind.CLI_MISSING:
                return _hook_response(
                    _missing_cli_context(root, git_created=git_state.created)
                )
            if beads_state.kind is BeadsKind.BROKEN:
                return _hook_response(
                    _broken_beads_context(root, beads_state.diagnostic)
                )
            if beads_state.kind is BeadsKind.PRESENT:
                assert bd is not None
                # Codex will execute both user and project hooks. Let a verified,
                # trusted project-local Beads hook supply the full prime context once.
                if project_has_trusted_beads_session_hook(root):
                    return _hook_response(suppress_output=True)
                prime = prime_beads(runner, bd, root)
                prefix = (
                    f"<workstream-bootstrap version={_safe_json_string(VERSION)} "
                    f"status=\"primed\" root={_safe_json_string(os.fspath(root))} />"
                )
                return _hook_response(prefix + "\n\n" + prime)

            # Compaction should refresh an existing Beads workspace, never create a
            # project. The installed project hooks cover their own compact lifecycle.
            if source == "compact":
                return _hook_response(suppress_output=True)

            brand_new = git_state.created or not git_state.has_head
            index_clean = _git_index_is_clean(runner, git, root)
            if brand_new and index_clean:
                assert bd is not None
                installed = initialize_beads(
                    runner,
                    bd=bd,
                    git=git,
                    root=root,
                    automatic=True,
                )
                prime = prime_beads(runner, bd, root)
                prefix = f"""<workstream-bootstrap version={_safe_json_string(VERSION)} status="auto-installed">
Workspace root (JSON data): {_safe_json_string(os.fspath(root))}
Git initialized by hook: {str(git_state.created).lower()}
Beads commit: {installed.commit}
</workstream-bootstrap>"""
                return _hook_response(prefix + "\n\n" + prime)

            status = _git_status(runner, git, root)
            return _hook_response(
                _approval_context(
                    root,
                    script_path=script_path,
                    dirty=bool(status),
                    staged=not index_clean,
                )
            )
    except BootstrapError as exc:
        return _hook_response(_error_context(locals().get("root", cwd), str(exc)))


def command_session_start(args: argparse.Namespace) -> int:
    del args
    try:
        payload = _read_session_start(sys.stdin)
    except BootstrapError as exc:
        response = _hook_response(_error_context(None, str(exc)))
    else:
        response = _session_start(
            payload,
            runner=CommandRunner(),
            script_path=Path(__file__).resolve(),
        )
    json.dump(response, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


def _requested_root(args: argparse.Namespace) -> Path:
    if args.root_token:
        return _root_from_token(args.root_token)
    if args.root:
        return Path(args.root)
    raise BootstrapError("provide --root or --root-token")


def command_install(args: argparse.Namespace) -> int:
    if not args.approved:
        print(
            "refusing to initialize an established workstream without --approved",
            file=sys.stderr,
        )
        return 2
    runner = CommandRunner()
    try:
        requested = validate_durable_workspace(
            _requested_root(args),
            allow_transient=_allow_transient(),
        )
        git = _resolve_executable("WORKSTREAM_BOOTSTRAP_GIT", ("git",))
        bd = _resolve_executable("WORKSTREAM_BOOTSTRAP_BD", ("bd", "beads"))
        if git is None:
            raise BootstrapError("Git is not executable")
        if bd is None:
            raise BootstrapError("neither bd nor beads is executable")
        root = _find_git_root(runner, git, requested)
        if root is None:
            raise BootstrapError(
                "the approved installer requires an existing Git repository; "
                "the SessionStart hook initializes new folders automatically"
            )
        with workspace_lock(root):
            result = initialize_beads(
                runner,
                bd=bd,
                git=git,
                root=root,
                automatic=False,
            )
            prime = prime_beads(runner, bd, root)
    except BootstrapError as exc:
        print(f"workstream-bootstrap: {exc}", file=sys.stderr)
        return 3
    json.dump(
        {
            "status": "installed",
            "root": os.fspath(result.root),
            "commit": result.commit,
            "prime": prime,
        },
        sys.stdout,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    sys.stdout.write("\n")
    return 0


def command_status(args: argparse.Namespace) -> int:
    runner = CommandRunner()
    try:
        requested = validate_durable_workspace(
            Path(args.root),
            allow_transient=_allow_transient(),
        )
        git = _resolve_executable("WORKSTREAM_BOOTSTRAP_GIT", ("git",))
        bd = _resolve_executable("WORKSTREAM_BOOTSTRAP_BD", ("bd", "beads"))
        if git is None:
            raise BootstrapError("Git is not executable")
        root = _find_git_root(runner, git, requested)
        if root is None:
            payload: dict[str, Any] = {
                "workspace": os.fspath(requested),
                "git": "absent",
                "beads": "not-inspected",
            }
        else:
            beads = inspect_beads(runner, bd, root)
            payload = {
                "workspace": os.fspath(requested),
                "root": os.fspath(root),
                "git": "established" if _git_has_head(runner, git, root) else "unborn",
                "clean": not bool(_git_status(runner, git, root)),
                "beads": beads.kind.value,
                "beads_path": (
                    os.fspath(beads.resolved_path) if beads.resolved_path else None
                ),
                "trusted_project_prime_hook": project_has_trusted_beads_session_hook(
                    root
                ),
            }
    except BootstrapError as exc:
        print(f"workstream-bootstrap: {exc}", file=sys.stderr)
        return 3
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap Git and Beads for durable conversation workstreams."
    )
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command")

    session = subparsers.add_parser(
        "session-start",
        help="consume SessionStart JSON from stdin and emit hook JSON",
    )
    session.set_defaults(func=command_session_start)

    install = subparsers.add_parser(
        "install",
        help="initialize Beads after explicit user approval",
    )
    root_group = install.add_mutually_exclusive_group()
    root_group.add_argument("--root", help="workspace directory")
    root_group.add_argument(
        "--root-token",
        help="URL-safe base64 workspace directory emitted by the hook",
    )
    install.add_argument(
        "--approved",
        action="store_true",
        help="assert explicit approval was given in the current conversation",
    )
    install.set_defaults(func=command_install)

    status = subparsers.add_parser("status", help="inspect a workspace without changing it")
    status.add_argument("--root", required=True, help="workspace directory")
    status.set_defaults(func=command_status)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        # Hook managers commonly configure only the executable path. Defaulting to
        # SessionStart keeps the entrypoint portable while the Codex registration is
        # explicit for readability.
        args = parser.parse_args(["session-start"])
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
