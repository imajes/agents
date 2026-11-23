#!/usr/bin/env python3
"""Explicit one-time source expansion. Never imported by the request runtime."""

import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from icon_chooser import __version__
from icon_chooser.common import ROOT, VERSION, digest, write_json


def expand(archive, destination, desktop=False):
    if destination.exists():
        raise ValueError(f"Refusing to overwrite existing import: {destination}")
    destination.mkdir(parents=True)
    count = 0
    with ZipFile(archive) as source:
        for info in source.infolist():
            if info.is_dir():
                continue
            parts = Path(info.filename).parts
            relative = Path(*parts[1:])
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"Unsafe archive member: {info.filename}")
            # Desktop is expanded intact. Web supplies core, SVG CSS and native definitions.
            if not desktop and not (
                str(relative) == "LICENSE.txt"
                or re.fullmatch(r"js/[a-z0-9-]+\.js", relative.as_posix())
                or str(relative)
                in (
                    "css/svg.css",
                    "css/svg.min.css",
                    "css/svg-with-js.css",
                    "css/svg-with-js.min.css",
                    "js/fontawesome.min.js",
                )
            ):
                continue
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open(info) as src, target.open("wb") as dst:
                import shutil

                shutil.copyfileobj(src, dst)
            count += 1
    return count


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--manifest", type=Path, default=ROOT / "SOURCE_MANIFEST.json")
    args = p.parse_args()
    root = args.output.expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        p.error(f"Output must be empty: {root}")
    sources = {}
    for kind in ("desktop", "web"):
        path = args.source_dir / f"fontawesome-pro-plus-{VERSION}-{kind}.zip"
        if not path.is_file():
            p.error(f"Missing source: {path}")
        sources[kind] = {"filename": path.name, "sha256": digest(path), "bytes": path.stat().st_size}
    root.mkdir(parents=True, exist_ok=True)
    for kind in sources:
        count = expand(args.source_dir / sources[kind]["filename"], root / kind, kind == "desktop")
        sources[kind]["imported_files"] = count
        print(f"Expanded {kind}: {count} files", flush=True)
    manifest = {
        "schema_version": 1,
        "distribution": "Font Awesome Pro Plus",
        "version": VERSION,
        "importer_version": __version__,
        "sources": sources,
        "license": "https://fontawesome.com/license",
        "runtime_policy": "Expanded files only; no archive access during requests.",
    }
    write_json(root / "source-manifest.json", manifest)
    write_json(args.manifest, manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
