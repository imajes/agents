"""CLI boundary: bounded JSON results and explicit write commands."""

import argparse
import json
import shutil
import sqlite3
import subprocess
import sys

from .catalog import Catalog
from .common import ROOT, digest, library_root, read_json
from .recipes import TOPICS, generate
from .rendering import export, preview


def parser():
    p = argparse.ArgumentParser(description="Find, compare, and deliver local Font Awesome icons.")
    p.add_argument(
        "--library", help="Expanded library root; defaults to the installed package .local/library"
    )
    p.add_argument("--json", action="store_true", help="Emit schema-versioned JSON")
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("search", "inspect", "styles", "export", "preview", "recipes", "build-index", "doctor"):
        command = sub.add_parser(name)
        command.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
        command.add_argument("--library", default=argparse.SUPPRESS)
        if name == "search":
            command.add_argument("query")
            command.add_argument("--limit", type=int, default=5)
        if name in ("inspect", "export", "recipes"):
            command.add_argument("icon")
        if name == "styles":
            command.add_argument("icon", nargs="?")
        if name == "preview":
            command.add_argument("icons", nargs="+")
            command.add_argument("--all-variants", action="store_true")
            command.add_argument("--background", default="#162134")
        if name in ("search", "inspect", "export", "preview", "recipes"):
            command.add_argument("--family")
            command.add_argument("--weight")
        if name in ("export", "preview", "recipes"):
            command.add_argument("--output", required=True)
            command.add_argument("--primary")
            command.add_argument("--secondary")
            command.add_argument("--overwrite", action="store_true")
        if name == "export":
            command.add_argument("--format", choices=["svg", "png"], default="svg")
            command.add_argument("--mode", choices=["original", "css", "static"], default="css")
            command.add_argument("--canvas", choices=["cropped", "full"])
            command.add_argument("--size", type=int, default=32, help="Output height in pixels")
            command.add_argument("--secondary-opacity", type=float)
            command.add_argument("--title", help="Accessible name; omitted means decorative")
        if name == "recipes":
            command.add_argument("--topic", choices=TOPICS, default="all")
        if name == "doctor":
            command.add_argument(
                "--deep", action="store_true", help="Explicit maintenance: verify all source asset hashes"
            )
    return p


def doctor(catalog, deep=False):
    library = catalog.library
    inventory = read_json(library / "inventory.json")
    missing = []
    checks = [
        "desktop/LICENSE.txt",
        "web/LICENSE.txt",
        "web/js/fontawesome.min.js",
        "web/css/svg-with-js.min.css",
        "native.sqlite",
        "source-manifest.json",
    ]
    for name in checks:
        if not (library / name).is_file():
            missing.append(name)
    stale = inventory["concepts_sha256"] != digest(ROOT / "data/concepts.json")
    mismatches = []
    if deep:
        for row in catalog.db.execute("SELECT path,full_path,sha256 FROM variants"):
            path = library / row["path"]
            if not path.is_file() or digest(path) != row["sha256"]:
                mismatches.append(row["path"])
            if not (library / row["full_path"]).is_file():
                mismatches.append(row["full_path"])
    return {
        "ok": not missing and not mismatches and not stale,
        "library": str(library),
        "inventory": inventory,
        "missing": missing,
        "modified_assets": mismatches,
        "concept_rules_changed": stale,
        "python": sys.version.split()[0],
        "png_renderer": shutil.which("rsvg-convert"),
        "native_definitions": str(library / "native.sqlite"),
        "dependencies": {
            "runtime": "Python >=3.10 + SQLite FTS5",
            "png": "rsvg-convert",
            "build_index": "PyYAML >=6,<7",
        },
        "runtime_access": "Read-only catalog and direct expanded asset files.",
    }


def run(args):
    library = library_root(args.library)
    if args.command == "build-index":
        from .indexing import build

        return build(library)
    cat = Catalog(library)
    try:
        if args.command == "search":
            if not 1 <= args.limit <= 50:
                raise ValueError("Limit must be between 1 and 50.")
            return cat.search(args.query, args.limit, args.family, args.weight)
        if args.command == "inspect":
            return cat.inspect(args.icon, args.family, args.weight)
        if args.command == "styles":
            return {"styles": cat.styles(args.icon)}
        if args.command == "doctor":
            return doctor(cat, args.deep)
        common = dict(
            family=args.family,
            weight=args.weight,
            primary=args.primary,
            secondary=args.secondary,
            overwrite=args.overwrite,
        )
        if args.command == "export":
            return export(
                cat,
                args.icon,
                args.output,
                fmt=args.format,
                mode=args.mode,
                canvas=args.canvas,
                size=args.size,
                title=args.title,
                secondary_opacity=args.secondary_opacity,
                **common,
            )
        if args.command == "preview":
            return preview(
                cat,
                args.icons,
                args.output,
                all_variants=args.all_variants,
                background=args.background,
                **common,
            )
        if args.command == "recipes":
            return generate(cat, args.icon, args.output, topic=args.topic, **common)
    finally:
        cat.close()


def text_result(result):
    if "results" in result:
        lines = [f"Candidates for {result['query']!r}:"]
        for icon in result["results"]:
            choices = ", ".join(v["directory"] for v in icon["recommendations"])
            lines.append(
                f"  {icon['name']} [{icon['match_kind']}] — {choices}\n    {'; '.join(icon['evidence'])}"
            )
        for icon in result["unavailable_exact_matches"]:
            lines.append(
                f"  Exact icon {icon['name']} is unavailable in the requested style. Available: {', '.join(icon['available_styles'])}"
            )
        if not result["results"]:
            lines.append("  No candidates. Broaden the concept or remove a style constraint.")
        return "\n".join(lines)
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    p = parser()
    args = p.parse_args()
    try:
        result = run(args)
        if isinstance(result, dict):
            result = {"schema_version": 1, **result}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else text_result(result))
        if args.command == "doctor" and not result["ok"]:
            raise SystemExit(1)
    except (ValueError, OSError, sqlite3.Error, subprocess.CalledProcessError) as error:
        message = str(error)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            message += (
                ": " + error.stderr.decode(errors="replace")
                if isinstance(error.stderr, bytes)
                else ": " + error.stderr
            )
        if args.json:
            print(json.dumps({"schema_version": 1, "error": message}), file=sys.stderr)
        else:
            print("Error: " + message, file=sys.stderr)
        raise SystemExit(2)
