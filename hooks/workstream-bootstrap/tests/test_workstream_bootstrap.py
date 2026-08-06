from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "workstream_bootstrap.py"
sys.path.insert(0, str(PACKAGE))

import workstream_bootstrap as bootstrap  # noqa: E402


FAKE_BD = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import subprocess
import sys

args = sys.argv[1:]
root = Path.cwd()
log_path = os.environ.get("FAKE_BD_LOG")
if log_path:
    with Path(log_path).open("a", encoding="utf-8") as log:
        log.write(json.dumps({"args": args, "cwd": str(root)}) + "\n")

if "where" in args:
    marker = root / ".beads" / "metadata.json"
    if marker.is_file():
        print(json.dumps({"path": str(root / ".beads"), "database_path": str(marker)}))
        raise SystemExit(0)
    print("Error: no beads database found", file=sys.stderr)
    raise SystemExit(1)

if "prime" in args:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "# Fake Beads Prime\n\nUse Beads for this workstream."
        }
    }))
    raise SystemExit(0)

if "init" in args:
    beads = root / ".beads"
    beads.mkdir(parents=True, exist_ok=True)
    (beads / "metadata.json").write_text('{"schema":1}\n', encoding="utf-8")
    codex = root / ".codex"
    codex.mkdir(parents=True, exist_ok=True)
    (codex / "hooks.json").write_text(json.dumps({
        "hooks": {
            "SessionStart": [{
                "matcher": "startup|resume|clear",
                "hooks": [{
                    "type": "command",
                    "command": "bd codex-hook SessionStart",
                    "statusMessage": "Loading Beads context"
                }]
            }]
        }
    }), encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(root), "add", ".beads/metadata.json", ".codex/hooks.json"],
        check=True,
    )
    subprocess.run(
        [
            "git", "-C", str(root),
            "-c", "user.name=Hook Test",
            "-c", "user.email=hook-test@example.invalid",
            "commit", "-m", "bd init: initialize beads issue tracking"
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    raise SystemExit(0)

print("unsupported fake bd command: " + repr(args), file=sys.stderr)
raise SystemExit(64)
'''


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [shutil.which("git") or "git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


class HookHarness(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="workstream-bootstrap-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.bin_dir = self.base / "bin"
        self.bin_dir.mkdir()
        self.fake_bd = self.bin_dir / "bd"
        self.fake_bd.write_text(FAKE_BD, encoding="utf-8")
        self.fake_bd.chmod(0o755)
        self.log = self.base / "bd.log"
        self.codex_home = self.base / "codex-home"
        self.codex_home.mkdir()
        self.env = os.environ.copy()
        self.env.update(
            {
                "WORKSTREAM_BOOTSTRAP_ALLOW_TRANSIENT": "1",
                "WORKSTREAM_BOOTSTRAP_BD": str(self.fake_bd),
                "WORKSTREAM_BOOTSTRAP_GIT": shutil.which("git") or "git",
                "FAKE_BD_LOG": str(self.log),
                "CODEX_HOME": str(self.codex_home),
            }
        )

    def workdir(self, name: str = "work") -> Path:
        root = self.base / name
        root.mkdir()
        return root

    def init_git(self, root: Path, *, commit: bool) -> str | None:
        git(root, "init")
        git(root, "config", "user.name", "Hook Test")
        git(root, "config", "user.email", "hook-test@example.invalid")
        if not commit:
            return None
        (root / "seed.txt").write_text("seed\n", encoding="utf-8")
        git(root, "add", "seed.txt")
        git(root, "commit", "-m", "chore: seed test repository")
        return git(root, "rev-parse", "HEAD").stdout.strip()

    def hook(self, root: Path, *, source: str = "startup") -> subprocess.CompletedProcess[str]:
        event = {
            "hook_event_name": "SessionStart",
            "cwd": str(root),
            "source": source,
            "session_id": "test-session",
            "model": "test-model",
            "permission_mode": "default",
            "transcript_path": None,
        }
        return subprocess.run(
            [sys.executable, str(SCRIPT), "session-start"],
            input=json.dumps(event),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            check=False,
        )

    def install(self, root: Path, *, approved: bool = True) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(SCRIPT), "install", "--root", str(root)]
        if approved:
            command.append("--approved")
        return subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            check=False,
        )

    @staticmethod
    def context(completed: subprocess.CompletedProcess[str]) -> str:
        payload = json.loads(completed.stdout)
        return payload.get("hookSpecificOutput", {}).get("additionalContext", "")

    def test_new_folder_initializes_git_beads_commits_and_primes(self) -> None:
        root = self.workdir()
        (root / "starter.txt").write_text("leave me untracked\n", encoding="utf-8")

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((root / ".git").exists())
        self.assertTrue((root / ".beads" / "metadata.json").exists())
        self.assertIn('status="auto-installed"', self.context(result))
        self.assertIn("# Fake Beads Prime", self.context(result))
        self.assertEqual(
            git(root, "log", "-1", "--format=%s").stdout.strip(),
            "chore(beads): initialize workstream tracking",
        )
        self.assertEqual(git(root, "rev-list", "--count", "HEAD").stdout.strip(), "1")
        self.assertEqual(git(root, "status", "--short").stdout.strip(), "?? starter.txt")

    def test_established_repository_requests_approval_without_mutating(self) -> None:
        root = self.workdir()
        before = self.init_git(root, commit=True)

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        context = self.context(result)
        self.assertIn('status="approval-required"', context)
        self.assertIn("ask James", context)
        self.assertIn("--approved", context)
        self.assertFalse((root / ".beads").exists())
        self.assertEqual(git(root, "rev-parse", "HEAD").stdout.strip(), before)

    def test_approved_clean_install_is_one_direct_child_commit(self) -> None:
        root = self.workdir()
        before = self.init_git(root, commit=True)

        result = self.install(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        after = payload["commit"]
        self.assertEqual(git(root, "rev-parse", f"{after}^").stdout.strip(), before)
        self.assertEqual(
            git(root, "rev-list", "--count", f"{before}..{after}").stdout.strip(),
            "1",
        )
        self.assertEqual(
            git(root, "log", "-1", "--format=%s", after).stdout.strip(),
            "chore(beads): initialize workstream tracking",
        )
        self.assertEqual(git(root, "status", "--short").stdout.strip(), "")
        self.assertIn("# Fake Beads Prime", payload["prime"])

    def test_approved_install_refuses_dirty_repository(self) -> None:
        root = self.workdir()
        before = self.init_git(root, commit=True)
        (root / "seed.txt").write_text("dirty\n", encoding="utf-8")

        result = self.install(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not clean", result.stderr)
        self.assertFalse((root / ".beads").exists())
        self.assertEqual(git(root, "rev-parse", "HEAD").stdout.strip(), before)

    def test_install_requires_explicit_approved_flag(self) -> None:
        root = self.workdir()
        self.init_git(root, commit=True)

        result = self.install(root, approved=False)

        self.assertEqual(result.returncode, 2)
        self.assertIn("without --approved", result.stderr)
        self.assertFalse((root / ".beads").exists())

    def test_existing_beads_workspace_is_primed(self) -> None:
        root = self.workdir()
        self.init_git(root, commit=True)
        (root / ".beads").mkdir()
        (root / ".beads" / "metadata.json").write_text("{}\n", encoding="utf-8")

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('status="primed"', self.context(result))
        self.assertIn("# Fake Beads Prime", self.context(result))

    def test_broken_beads_marker_is_not_reinitialized(self) -> None:
        root = self.workdir()
        before = self.init_git(root, commit=True)
        (root / ".beads").mkdir()

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('status="broken-beads"', self.context(result))
        self.assertIn("bd doctor --agent", self.context(result))
        self.assertEqual(git(root, "rev-parse", "HEAD").stdout.strip(), before)

    def test_unborn_repository_with_staged_content_takes_approval_path(self) -> None:
        root = self.workdir()
        self.init_git(root, commit=False)
        (root / "staged.txt").write_text("staged\n", encoding="utf-8")
        git(root, "add", "staged.txt")

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('status="approval-required"', self.context(result))
        self.assertIn("Staged content is especially unsafe", self.context(result))
        self.assertFalse((root / ".beads").exists())

    def test_compact_does_not_install_absent_beads(self) -> None:
        root = self.workdir()
        self.init_git(root, commit=True)

        result = self.hook(root, source="compact")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertNotIn("hookSpecificOutput", payload)
        self.assertFalse((root / ".beads").exists())

    def test_missing_beads_cli_still_initializes_git_then_requests_approval(self) -> None:
        root = self.workdir()
        env = self.env.copy()
        env["WORKSTREAM_BOOTSTRAP_BD"] = str(self.base / "missing-bd")
        event = {
            "hook_event_name": "SessionStart",
            "cwd": str(root),
            "source": "startup",
        }

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "session-start"],
            input=json.dumps(event),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('status="missing-beads-cli"', self.context(result))
        self.assertIn("Ask James", self.context(result))
        self.assertTrue((root / ".git").is_dir())
        self.assertFalse((root / ".beads").exists())

    def test_transient_workspace_is_quiet_without_opt_in(self) -> None:
        root = self.workdir()
        env = self.env.copy()
        env.pop("WORKSTREAM_BOOTSTRAP_ALLOW_TRANSIENT")
        event = {
            "hook_event_name": "SessionStart",
            "cwd": str(root),
            "source": "startup",
        }

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "session-start"],
            input=json.dumps(event),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertNotIn("hookSpecificOutput", payload)
        self.assertTrue(payload["suppressOutput"])
        self.assertFalse((root / ".git").exists())

    def test_status_is_read_only_for_non_git_workspace(self) -> None:
        root = self.workdir()

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "status", "--root", str(root)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["git"], "absent")
        self.assertEqual(payload["beads"], "not-inspected")
        self.assertFalse((root / ".git").exists())

    def test_invalid_hook_json_fails_open_with_valid_hook_response(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "session-start"],
            input="not json",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["continue"])
        self.assertIn('status="error"', self.context(result))

    def test_root_token_round_trip(self) -> None:
        root = self.workdir("path with spaces")
        token = bootstrap._root_token(root)
        self.assertEqual(bootstrap._root_from_token(token), root)
        decoded = base64.urlsafe_b64decode(token).decode("utf-8")
        self.assertEqual(decoded, str(root))

    def test_codex_hash_matches_known_beads_hook_hash(self) -> None:
        group = {
            "matcher": "startup|resume|clear",
            "hooks": [],
        }
        handler = {
            "type": "command",
            "command": "bd codex-hook SessionStart",
            "statusMessage": "Loading Beads context",
        }
        self.assertEqual(
            bootstrap._canonical_hook_hash(group, handler),
            "sha256:392a61a090ba7d6aab6ab0fb0f82f3df3d6a380ee81f60f00af3bd42025d51a9",
        )

    def test_trusted_project_hook_suppresses_duplicate_prime(self) -> None:
        root = self.workdir()
        self.init_git(root, commit=True)
        (root / ".beads").mkdir()
        (root / ".beads" / "metadata.json").write_text("{}\n", encoding="utf-8")
        codex = root / ".codex"
        codex.mkdir()
        group = {
            "matcher": "startup|resume|clear",
            "hooks": [
                {
                    "type": "command",
                    "command": "bd codex-hook SessionStart",
                    "statusMessage": "Loading Beads context",
                }
            ],
        }
        (codex / "hooks.json").write_text(
            json.dumps({"hooks": {"SessionStart": [group]}}),
            encoding="utf-8",
        )
        trust_hash = bootstrap._canonical_hook_hash(group, group["hooks"][0])
        key = f'{codex / "hooks.json"}:session_start:0:0'
        (self.codex_home / "config.toml").write_text(
            textwrap.dedent(
                f'''\
                [hooks.state."{key}"]
                trusted_hash = "{trust_hash}"
                '''
            ),
            encoding="utf-8",
        )

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertNotIn("hookSpecificOutput", payload)
        invocations = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertFalse(any("prime" in item["args"] for item in invocations))

    def test_stale_project_hook_trust_does_not_suppress_prime(self) -> None:
        root = self.workdir()
        self.init_git(root, commit=True)
        (root / ".beads").mkdir()
        (root / ".beads" / "metadata.json").write_text("{}\n", encoding="utf-8")
        codex = root / ".codex"
        codex.mkdir()
        group = {
            "matcher": "startup|resume|clear",
            "hooks": [
                {
                    "type": "command",
                    "command": "bd codex-hook SessionStart",
                    "statusMessage": "Loading Beads context",
                }
            ],
        }
        (codex / "hooks.json").write_text(
            json.dumps({"hooks": {"SessionStart": [group]}}),
            encoding="utf-8",
        )
        key = f'{codex / "hooks.json"}:session_start:0:0'
        (self.codex_home / "config.toml").write_text(
            f'[hooks.state."{key}"]\ntrusted_hash = "sha256:stale"\n',
            encoding="utf-8",
        )

        result = self.hook(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Fake Beads Prime", self.context(result))


@unittest.skipUnless(
    os.environ.get("RUN_REAL_BEADS_INTEGRATION") == "1" and shutil.which("bd"),
    "set RUN_REAL_BEADS_INTEGRATION=1 to exercise the installed bd binary",
)
class RealBeadsSmokeTest(unittest.TestCase):
    def test_real_bd_initializes_one_commit_and_primes(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="workstream-bootstrap-real-bd-"
        ) as temp:
            root = Path(temp)
            env = os.environ.copy()
            env.update(
                {
                    "WORKSTREAM_BOOTSTRAP_ALLOW_TRANSIENT": "1",
                    "WORKSTREAM_BOOTSTRAP_BD": shutil.which("bd") or "bd",
                    "WORKSTREAM_BOOTSTRAP_GIT": shutil.which("git") or "git",
                    "CODEX_HOME": str(root / "isolated-codex-home"),
                }
            )
            event = {
                "hook_event_name": "SessionStart",
                "cwd": str(root),
                "source": "startup",
            }

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "session-start"],
                input=json.dumps(event),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
                timeout=180,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            context = payload["hookSpecificOutput"]["additionalContext"]
            self.assertIn('status="auto-installed"', context)
            self.assertTrue((root / ".beads" / "metadata.json").is_file())
            self.assertEqual(
                git(root, "log", "-1", "--format=%s").stdout.strip(),
                "chore(beads): initialize workstream tracking",
            )
            self.assertEqual(
                git(root, "rev-list", "--count", "HEAD").stdout.strip(),
                "1",
            )

    def test_real_bd_approved_established_install_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="workstream-bootstrap-real-bd-established-"
        ) as temp:
            root = Path(temp)
            git(root, "init")
            git(root, "config", "user.name", "Hook Test")
            git(root, "config", "user.email", "hook-test@example.invalid")
            (root / "seed.txt").write_text("seed\n", encoding="utf-8")
            git(root, "add", "seed.txt")
            git(root, "commit", "-m", "chore: seed real beads test")
            before = git(root, "rev-parse", "HEAD").stdout.strip()
            env = os.environ.copy()
            env.update(
                {
                    "WORKSTREAM_BOOTSTRAP_ALLOW_TRANSIENT": "1",
                    "WORKSTREAM_BOOTSTRAP_BD": shutil.which("bd") or "bd",
                    "WORKSTREAM_BOOTSTRAP_GIT": shutil.which("git") or "git",
                    "CODEX_HOME": str(root / "isolated-codex-home"),
                }
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "install",
                    "--root",
                    str(root),
                    "--approved",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
                timeout=180,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            after = payload["commit"]
            self.assertEqual(git(root, "rev-parse", f"{after}^").stdout.strip(), before)
            self.assertEqual(
                git(root, "rev-list", "--count", f"{before}..{after}").stdout.strip(),
                "1",
            )
            self.assertEqual(
                git(root, "log", "-1", "--format=%s").stdout.strip(),
                "chore(beads): initialize workstream tracking",
            )
            self.assertEqual(git(root, "status", "--short").stdout.strip(), "")
            self.assertTrue((root / ".beads" / "metadata.json").is_file())


if __name__ == "__main__":
    unittest.main()
