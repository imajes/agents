#!/usr/bin/env python3
"""Manage the product skill directory links and their Git submodules."""

import argparse
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
LINKS = ROOT / "skills" / "product"


def git(repo, *args, capture=True):
    result = subprocess.run(
        ["git", "-C", repo, *args], check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout.rstrip("\n") if capture else None


def packages():
    entries = git(ROOT, "config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$")
    result = {}
    for line in entries.splitlines():
        key, value = line.split(maxsplit=1)
        path = Path(value)
        if path.parent == Path("upstream"):
            result[path.name] = key.removesuffix(".path")
    if not result:
        raise ValueError("No product submodules are configured under upstream/.")
    return result


def skill_files(source, revision="HEAD"):
    # The repositories keep canonical skills under skills/ or <collection>/skills/.
    # Read the Git tree to omit generated copies in deeper plugin and build folders.
    paths = git(source, "ls-tree", "-r", "-z", "--name-only", revision).split("\0")
    skills = []
    for name in paths:
        path = Path(name)
        if path.name == "SKILL.md" and (path.parts[0] == "skills" or path.parts[1:2] == ("skills",)):
            skills.append(path.parent)
    return sorted(skills)


def active_links(package):
    directory = LINKS / package
    if directory.is_symlink():
        raise ValueError(f"Expected an ordinary directory at {directory}")
    return sorted(p for p in directory.iterdir() if not p.name.startswith(".")) if directory.is_dir() else []


def link_target(link, source):
    if not link.is_symlink() or link.readlink().is_absolute():
        raise ValueError(f"Expected a relative directory link at {link}")
    target = link.resolve()
    if not target.is_relative_to(source) or target.name != link.name:
        raise ValueError(f"Unmanaged link at {link}: {target}")
    return target


def verify_links(package, skills):
    source = ROOT / "upstream" / package
    for link in active_links(package):
        target = link_target(link, source)
        if target.relative_to(source) not in skills or not (target / "SKILL.md").is_file():
            raise ValueError(f"Missing skill for {link}: {target}")


def clean_checkout(source):
    if git(source, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError(f"Uncommitted changes in {source}. Review them before changing revisions.")


def require_recorded_pin(source):
    pin = git(ROOT, "rev-parse", f":upstream/{source.name}")
    if git(source, "rev-parse", "HEAD") != pin:
        raise ValueError(f"{source.name} differs from the parent index. Review its pending pin first.")


def update(package, key, source):
    clean_checkout(source)
    require_recorded_pin(source)
    branch = git(ROOT, "config", "--file", ".gitmodules", "--get", f"{key}.branch")
    git(source, "fetch", "--no-recurse-submodules", "origin", f"refs/heads/{branch}", capture=False)
    candidate = git(source, "rev-parse", "--verify", "FETCH_HEAD^{commit}")
    # A provider may have moved a skill. Check the new tree before moving the checkout.
    verify_links(package, skill_files(source, candidate))
    if candidate != git(source, "rev-parse", "HEAD"):
        git(source, "checkout", "--detach", candidate, capture=False)
    print(f"{package} at {candidate[:12]}")


def change_link(action, package, source, skills, selection):
    if action == "enable":
        chosen = Path(selection)
        if chosen not in skills or not (source / chosen / "SKILL.md").is_file():
            raise ValueError(f"Unknown skill path {selection!r}. See skills-available {package}.")
        link = LINKS / package / chosen.name
        target = os.path.relpath(source / chosen, link.parent)
        if link.is_symlink() and link.readlink() == Path(target):
            return
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target, target_is_directory=True)
    else:
        if Path(selection).name != selection:
            raise ValueError("Use the enabled skill name for disable.")
        link = LINKS / package / selection
        if link not in active_links(package):
            raise ValueError(f"Skill is not enabled: {selection}")
        link_target(link, source)
        link.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for action in ("list", "check", "init", "available", "enable", "disable", "update"):
        command = commands.add_parser(action)
        if action in ("available", "enable", "disable", "update"):
            command.add_argument("package")
        if action in ("enable", "disable"):
            command.add_argument("selection")
    args = parser.parse_args()
    sources = packages()
    package = getattr(args, "package", None)
    if package is not None and package not in sources:
        parser.error(f"Unknown package {package!r}. Choose from {', '.join(sorted(sources))}.")

    if args.action == "init":
        for name in sources:
            source = ROOT / "upstream" / name
            if (source / ".git").exists():
                current = git(source, "rev-parse", "HEAD")
                if current != git(ROOT, "rev-parse", f":upstream/{name}"):
                    clean_checkout(source)
                    if not git(source, "for-each-ref", "--contains=HEAD", "--format=%(refname)"):
                        raise ValueError(f"Save the detached commit in {name} before switching pins.")
        git(ROOT, "submodule", "update", "--init", "--", *[f"upstream/{p}" for p in sources], capture=False)

    if LINKS.is_symlink():
        raise ValueError(f"Expected an ordinary directory at {LINKS}")
    if LINKS.is_dir():
        unknown = [p.name for p in LINKS.iterdir() if not p.name.startswith(".") and p.name not in sources]
        if unknown:
            raise ValueError(f"Unknown package directories in {LINKS}: {', '.join(unknown)}")
    for name in ([package] if package is not None else sorted(sources)):
        source = ROOT / "upstream" / name
        if not (source / ".git").exists():
            raise ValueError(f"{name} is not initialized. Run just skills-init.")
        skills = skill_files(source)
        if args.action == "available":
            print("\n".join(map(str, skills)))
            return
        if args.action != "disable":
            verify_links(name, skills)
        if args.action == "list":
            for link in active_links(name):
                print(f"{name}\t{link.name}\t{link.resolve().relative_to(source)}")
        elif args.action in ("check", "init"):
            print(f"{name}: {len(active_links(name))} linked, {git(source, 'rev-parse', '--short', 'HEAD')}")
        elif args.action == "update":
            update(name, sources[name], source)
        else:
            change_link(args.action, name, source, skills, args.selection)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
