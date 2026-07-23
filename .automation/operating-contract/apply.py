#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TARGET = Path("operating-contract/v2/OPERATING_CONTRACT.md")
PATCH_DIR = Path(sys.argv[1]).resolve()
STEPS = [
    ("2.1.4", "feat: add resilient claim-tail rendering"),
    ("2.1.5", "feat: consolidate navigation instrumentation"),
    ("2.1.6", "feat: add rolling contract read receipt"),
    ("2.1.7", "fix: classify pre-send failures by severity"),
]


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def current_version() -> str:
    match = re.search(
        r"^\*\*Version:\*\* (\d+\.\d+\.\d+)\s*$",
        TARGET.read_text(),
        re.MULTILINE,
    )
    if not match:
        raise RuntimeError(f"Could not find contract version in {TARGET}")
    return match.group(1)


def validate(version: str) -> None:
    text = TARGET.read_text()
    if current_version() != version:
        raise RuntimeError(f"Expected version {version}, found {current_version()}")
    if text.count("```") % 2:
        raise RuntimeError("Unbalanced fenced code blocks")
    if not text.endswith("\n"):
        raise RuntimeError("Contract must end with a newline")


def main() -> None:
    version = current_version()
    known = ["2.1.3", *[item[0] for item in STEPS]]
    if version not in known:
        raise RuntimeError(f"Unexpected starting version: {version}")
    if version == STEPS[-1][0]:
        print(f"Contract already at {version}; nothing to do")
        return

    start_index = known.index(version)
    for target_version, message in STEPS[start_index:]:
        patch = PATCH_DIR / f"{target_version}.diff"
        run("git", "apply", "--check", str(patch))
        run("git", "apply", str(patch))
        validate(target_version)
        run("git", "add", str(TARGET))
        run("git", "commit", "-m", message)
        print(f"Committed operating contract {target_version}")

    final = TARGET.read_text()
    required = [
        "〔🟢≡ ~99% ← current source〕",
        "〔🟠∴ ~90% ← evidence + derivation〕",
        "〔🔴? ~50% ← hypothesis〕",
        "### A1.1 — Rolling read receipt",
        "When a pre-send check fails, classify the failure before reporting it:",
    ]
    missing = [item for item in required if item not in final]
    if missing:
        raise RuntimeError(f"Final contract is missing required markers: {missing}")


if __name__ == "__main__":
    main()
