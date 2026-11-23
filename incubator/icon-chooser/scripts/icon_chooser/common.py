"""Paths, schema boundaries, and small shared helpers."""

import hashlib
import json
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = 1
VERSION = "7.3.1"


def library_root(value=None):
    return (
        Path(value or os.environ.get("ICON_CHOOSER_LIBRARY", ROOT / ".local/library")).expanduser().resolve()
    )


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def connect(library, name="catalog.sqlite"):
    path = library / name
    if not path.is_file():
        raise ValueError(f"Missing {path}; run setup_library.py or build-index first.")
    db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    if name == "catalog.sqlite":
        version = db.execute("pragma user_version").fetchone()[0]
        if version != SCHEMA:
            db.close()
            raise ValueError(f"Index schema {version} requires rebuild; expected {SCHEMA}.")
    return db


def asset_path(library, relative):
    path = (library / relative).resolve()
    if not path.is_relative_to(library.resolve()):
        raise ValueError("Asset path escapes the library.")
    return path
