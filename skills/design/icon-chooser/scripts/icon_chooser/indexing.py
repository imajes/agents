"""Maintenance-only indexing; runtime modules do not import this module."""

import json
import os
import re
import sqlite3
import xml.etree.ElementTree as ET

from .common import ROOT, SCHEMA, digest, read_json, write_json


def directory(family, weight):
    if family == "classic":
        return weight
    if family == "duotone" and weight == "solid":
        return "duotone"
    return f"{family}-{weight}"


def build(library):
    try:
        import yaml
    except ImportError as error:
        raise ValueError(
            "Index building needs PyYAML: use uv run --with PyYAML scripts/icons.py build-index"
        ) from error
    metadata = library / "desktop/metadata"
    icons = read_json(metadata / "icon-families.json")
    categories = yaml.safe_load((metadata / "categories.yml").read_text())
    styles = read_json(ROOT / "data/styles.json")
    manifest = read_json(library / "source-manifest.json")
    category_map = {}
    for category, value in categories.items():
        for name in value["icons"]:
            category_map.setdefault(name, []).extend([category, value["label"]])
    temp = library / "catalog.sqlite.new"
    native_temp = library / "native.sqlite.new"
    if temp.exists() or native_temp.exists():
        raise ValueError("Interrupted build files exist; inspect .sqlite.new files before retrying.")
    db = sqlite3.connect(temp)
    db.executescript("""
        PRAGMA journal_mode=DELETE;
        CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE icons(name TEXT PRIMARY KEY, label TEXT, unicode TEXT, aliases TEXT, terms TEXT, categories TEXT);
        CREATE TABLE aliases(alias TEXT PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE variants(name TEXT, family TEXT, weight TEXT, directory TEXT, path TEXT,
            full_path TEXT, width INTEGER, height INTEGER, layers INTEGER, sha256 TEXT,
            PRIMARY KEY(name,family,weight));
        CREATE TABLE styles(directory TEXT PRIMARY KEY, family TEXT, weight TEXT, prefix TEXT, description TEXT, fresh INTEGER);
        CREATE VIRTUAL TABLE search USING fts5(name, label, aliases, terms, categories, tokenize='porter unicode61');
        CREATE INDEX variant_family ON variants(family, weight);
    """)
    native = sqlite3.connect(native_temp)
    native.execute(
        "CREATE TABLE definitions(directory TEXT, name TEXT, prefix TEXT, definition TEXT, PRIMARY KEY(directory,name))"
    )
    dirs = set()
    aliases = {}
    count = 0
    for name, value in sorted(icons.items()):
        names = value.get("aliases", {}).get("names", [])
        for alias in names:
            if alias in aliases and aliases[alias] != name:
                raise ValueError(f"Ambiguous alias: {alias}")
            aliases[alias] = name
        terms = value.get("search", {}).get("terms", [])
        cats = list(dict.fromkeys(category_map.get(name, [])))
        db.execute(
            "INSERT INTO icons VALUES(?,?,?,?,?,?)",
            (name, value["label"], value["unicode"], json.dumps(names), json.dumps(terms), json.dumps(cats)),
        )
        db.execute(
            "INSERT INTO search VALUES(?,?,?,?,?)",
            (name.replace("-", " "), value["label"], " ".join(names), " ".join(terms), " ".join(cats)),
        )
        for family, weights in value["svgs"].items():
            for weight, svg_meta in weights.items():
                style = directory(family, weight)
                dirs.add((style, family, weight))
                relative = f"desktop/svgs/{style}/{name}.svg"
                full = f"desktop/svgs-full/{style}/{name}.svg"
                path = library / relative
                root = ET.parse(path).getroot()
                if not (library / full).is_file():
                    raise ValueError(f"Missing full SVG: {full}")
                layers = len(root.findall(".//{http://www.w3.org/2000/svg}path"))
                db.execute(
                    "INSERT INTO variants VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (
                        name,
                        family,
                        weight,
                        style,
                        relative,
                        full,
                        svg_meta["width"],
                        svg_meta["height"],
                        layers,
                        digest(path),
                    ),
                )
                count += 1
    db.executemany("INSERT INTO aliases VALUES(?,?)", sorted(aliases.items()))
    for style, family, weight in sorted(dirs):
        text = (library / f"web/js/{style}.js").read_text()
        prefixes = [
            p for p in re.findall(r"defineIcons\('([^']+)', icons", text) if p != "fa" and "-" not in p
        ]
        if not prefixes:
            raise ValueError(f"No native prefix for {style}")
        prefix = prefixes[0]
        start = text.index("var icons = ") + len("var icons = ")
        definitions, _ = json.JSONDecoder().raw_decode(text, start)
        info = styles[family]
        db.execute(
            "INSERT INTO styles VALUES(?,?,?,?,?,?)",
            (style, family, weight, prefix, info["description"], info["fresh"]),
        )
        for row in db.execute("SELECT name FROM variants WHERE directory=?", (style,)).fetchall():
            name = row[0]
            if name not in definitions:
                raise ValueError(f"Missing native definition: {style}/{name}")
            native.execute(
                "INSERT INTO definitions VALUES(?,?,?,?)",
                (style, name, prefix, json.dumps(definitions[name], separators=(",", ":"))),
            )
    # Full inventory reconciliation includes alias files, not just canonical metadata rows.
    inventory = {(r[0], r[1]) for r in db.execute("SELECT directory,name FROM variants")}
    verified = 0
    for canvas in ("svgs", "svgs-full"):
        for path in (library / "desktop" / canvas).glob("*/*.svg"):
            canonical = aliases.get(path.stem, path.stem)
            if (path.parent.name, canonical) not in inventory:
                raise ValueError(f"Unmapped artwork: {path}")
            verified += 1
    expected_count = 2 * sum(1 for _ in (library / "desktop/svgs").glob("*/*.svg"))
    if verified != expected_count:
        raise ValueError("Cropped/full inventories differ")
    report = {
        "schema_version": SCHEMA,
        "version": manifest["version"],
        "icons": len(icons),
        "aliases": len(aliases),
        "variants": count,
        "styles": len(dirs),
        "reconciled_svg_files": verified,
        "unmapped_svg_files": 0,
        "concepts_sha256": digest(ROOT / "data/concepts.json"),
    }
    db.executemany("INSERT INTO meta VALUES(?,?)", [(k, json.dumps(v)) for k, v in report.items()])
    db.execute(f"PRAGMA user_version={SCHEMA}")
    db.commit()
    native.commit()
    db.close()
    native.close()
    os.replace(native_temp, library / "native.sqlite")
    os.replace(temp, library / "catalog.sqlite")
    write_json(library / "inventory.json", report)
    return report
