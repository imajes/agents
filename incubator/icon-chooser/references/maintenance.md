# Maintenance and interface

Runtime has no Python package dependencies. It needs Python >=3.10 with SQLite
FTS5. PNG additionally uses `rsvg-convert` from librsvg. Index construction uses
PyYAML >=6,<7. Source ZIPs are read only by the explicit setup helper.

From the development repository, import into an empty destination:

```zsh
python3 scripts/setup_library.py --source-dir '/Users/james/Projects/Shared/Resources/Font Awesome 7.3.1' --output .local/library
python3 scripts/icons.py build-index --json
python3 scripts/icons.py doctor --deep --json
python3 -m unittest discover -s tests -v
```

If PyYAML is unavailable, the explicit maintenance command can use
`uv run --with 'PyYAML>=6,<7' scripts/icons.py build-index`. Ordinary requests never
install dependencies or rebuild data. For an upgrade, import into a new versioned
directory, rebuild, qualify, and install a fresh package; keep the working version
until qualification succeeds. The current importer is pinned to 7.3.1.

`SOURCE_MANIFEST.json` records the supplied archive identities and checksums.
`.local/library/source-manifest.json` travels with the expanded data. `inventory.json`
records reconciled counts. `catalog.sqlite` holds compact retrieval data;
`native.sqlite` holds native geometry separately for direct selected-definition
lookup. Full raw metadata is never fed into the requesting agent's context.

Search/inspect/styles use read-only SQLite connections. Export/preview/recipes
read direct files and write only to an explicit output destination. `doctor`
checks package readiness; `--deep` explicitly hashes all canonical source SVGs.
`--library` or `ICON_CHOOSER_LIBRARY` overrides the package-local expanded root for
maintenance and testing. Paths inside the catalog remain relative.

Use `--json` for schema version 1. Successful commands return a JSON object on
stdout. Errors return a JSON object on stderr and exit 2. A failed readiness
check exits 1. Search returns `results`, `unavailable_exact_matches`, evidence,
and style recommendations. Inspection returns all real variants. Export returns
absolute `path`, `manifest`, source identity/hash, output hash, colors, dimensions,
canvas, license path, and dependencies. Original SVG export retains source bytes
and dimensions; its static styling has not been resolved.

Output files are not replaced unless `--overwrite` is explicit. CSS-mode colors
accept hex, basic named colors, currentColor, or a simple CSS variable reference.
Static/PNG colors require hex or a supported basic color name. `--size` is an
integer height of 1–8192 pixels. `--secondary-opacity` is 0–1.

The installer requires an explicit destination and refuses existing targets:

```zsh
python3 scripts/install_skill.py --output /Users/james/.agents/incubator/icon-chooser
python3 /Users/james/.agents/incubator/icon-chooser/scripts/icons.py doctor --json
python3 scripts/install_skill.py --source /Users/james/.agents/incubator/icon-chooser --output /Users/james/.agents/skills/design/icon-chooser
```

Installed packages contain their own expanded source trees, indexes, runtime
helpers, licenses, authored rules, references, and scripts. They use no symlinks
or references to the development library. Installation does not alter Codex
configuration, enable a service, commit code, or synchronize Beads.
