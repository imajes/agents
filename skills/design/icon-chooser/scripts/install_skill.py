#!/usr/bin/env python3
"""Copy the authored skill and its expanded library to an explicit destination."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from icon_chooser.common import ROOT


def install(source, output):
    source, output = source.resolve(), output.expanduser().resolve()
    if output.exists():
        raise ValueError(f"Refusing to replace an existing skill: {output}. Qualify a new destination first.")
    if source == output or source in output.parents:
        raise ValueError("Install outside the source tree.")
    required = [
        "SKILL.md",
        "SOURCE_MANIFEST.json",
        "scripts",
        "data",
        "references",
        "agents",
        ".local/library",
    ]
    for relative in required:
        if not (source / relative).exists():
            raise ValueError(f"Incomplete source package: {relative}")
    output.mkdir(parents=True)
    (output / ".gitignore").write_text(".local/\n__pycache__/\n*.pyc\noutput/\n*.zip\n")
    for relative in required:
        src, dst = source / relative, output / relative
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.new"))
        else:
            shutil.copy2(src, dst)
    # Runtime is invoked from the copy, never from the development tree.
    subprocess.run(
        [sys.executable, str(output / "scripts/icons.py"), "doctor", "--json"], cwd=output, check=True
    )
    print(f"Installed expanded standalone skill: {output}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=ROOT)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        install(args.source, args.output)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        p.exit(2, f"Error: {error}\n")
