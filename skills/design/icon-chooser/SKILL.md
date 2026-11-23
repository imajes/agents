---
name: icon-chooser
description: Choose, compare, export, and integrate meaningful Font Awesome Pro Plus icons in websites, reports, documents, slides, diagrams, and other artifacts. Use for icon selection, finding a visual metaphor, browsing icon families, obtaining SVG/PNG files, or applying icon styling and motion. Ordinary artifact work without an icon-selection or integration need does not require this skill.
---

# Icon Chooser

Use the expanded local Font Awesome Pro Plus 7.3.1 collection to find an icon that
expresses the request. The helper retrieves candidates; judge their meaning and
visual fit against the actual artifact. Return useful files when assets are
requested, rather than only an icon name or a link to the vendor site.

## Start with the artifact

Read the request and available artifact context: concept, audience, palette,
surface, size, format, and existing icon treatment. Infer routine choices from
that context. Ask only when an ambiguity materially changes the meaning or output.

Set `ICON_SKILL` to the directory containing this SKILL.md. An installed copy is
normally `/Users/james/.agents/skills/design/icon-chooser`. Commands can run from
the requesting project's directory:

```zsh
ICON_SKILL='/Users/james/.agents/skills/design/icon-chooser'
python3 "$ICON_SKILL/scripts/icons.py" search 'constructive feedback' --json
python3 "$ICON_SKILL/scripts/icons.py" inspect comments --json
python3 "$ICON_SKILL/scripts/icons.py" styles --json
```

Search returns canonical candidates with exact/related/broader evidence, available
styles, and suggested variants. Prefer the most specific truthful representation.
For an unavailable subject, consider a related object/activity and a broader
symbol; explain the substitution in one sentence. Reformulate weak results with
the concrete action, object, or category. Do not invent an icon or style.

## Style choices

Honor explicit family, weight, and color requests. Otherwise lead with a suitable
smaller expressive family, with **Duotone Light** alongside as the house option.
Semantic fit takes priority over novelty. The helper's expressive-family ordering
is a discovery aid; choose the family whose shape suits the artifact.

Use complementary colors already present in the artifact palette. Do not invent
a new palette or rotate hues mechanically. Primary/secondary colors and opacity
should preserve legibility on the actual background. Single-layer icons support
one visible color; avoid promising duotone controls for them.

For a group, compare coverage and choose a coherent family/weight; identify any
exceptions. To inspect all variants of the same icon or show a visual comparison:

```zsh
python3 "$ICON_SKILL/scripts/icons.py" styles house --json
python3 "$ICON_SKILL/scripts/icons.py" preview house user heart --output '/absolute/artifact/icons/comparison.html'
python3 "$ICON_SKILL/scripts/icons.py" preview house --all-variants --primary '#244869' --secondary '#bf7439' --output '/absolute/artifact/icons/house-styles.html'
```

Use [family guidance](references/styles.md) when comparing visual directions.
Avoid showing dozens of variants unless the requester asks for a full comparison.

## Deliver assets

Use an explicit output directory in the requesting artifact. Choose a family and
weight deliberately after inspecting availability. Default export selection uses
the same fresh-first recommendations as search, so pass constraints to obtain the
house style or any other specific variant.

```zsh
python3 "$ICON_SKILL/scripts/icons.py" export comments --family duotone --weight light --mode css --output '/absolute/artifact/icons' --json
python3 "$ICON_SKILL/scripts/icons.py" export comments --family duotone --weight light --mode static --primary '#244869' --secondary '#bf7439' --secondary-opacity 1 --size 96 --output '/absolute/artifact/icons' --json
python3 "$ICON_SKILL/scripts/icons.py" export comments --family duotone --weight light --format png --primary '#244869' --secondary '#bf7439' --size 256 --output '/absolute/artifact/icons' --json
```

Use CSS-ready SVG inline when the host should control color. Use fixed-color SVG
or PNG for image embedding; CSS from a surrounding HTML page does not reach an
SVG loaded through `<img>`. Static/PNG exports default to a full canvas. CSS-ready
SVG defaults to a cropped canvas. Override with `--canvas full|cropped`.

`--mode original` copies source SVG bytes unchanged. It retains the original
currentColor styling and source dimensions. `--title` gives a styled SVG an
accessible name; without a title it is decorative. Label icon-only controls on
the control itself. Native brand artwork represents the named company, product,
or service; use an appropriate generic icon for unrelated concepts.

Return the selected icon identity, a brief reason, actual output paths, and the
relevant integration snippet. Link or display the delivered files in the calling
chat. Keep the manifest and supplied license with the artifact's assets.

If the artifact is being built in a different execution environment, transfer the
selected files with an available file-copy tool and return the destination paths.
Confirm that the receiving environment can read them before embedding the icons.

## Integrate and refine

For standalone SVG, use [presentation recipes](references/presentation.md).
For Font Awesome's native capabilities, generate a runnable local example:

```zsh
python3 "$ICON_SKILL/scripts/icons.py" recipes comments --family duotone --weight light --topic all --primary '#244869' --secondary '#bf7439' --output '/absolute/artifact/icon-recipes' --json
```

The result includes local CSS/JS, only selected icon definitions, a working HTML
page, and provenance. Read [native runtime guidance](references/native-runtime.md)
for transforms, masks, layers, and motion. Adapt the relevant snippet to the
target artifact. Reuse a compatible existing runtime when one is already present.
JavaScript is unnecessary for ordinary standalone SVG rendering.

## Local data and maintenance

Runtime needs Python 3.10+ and the packaged SQLite catalog. PNG needs
`rsvg-convert`. Search, inspection, preview, export, and recipes use the installed
expanded files; never unzip or scan the collection during icon requests.

```zsh
python3 "$ICON_SKILL/scripts/icons.py" doctor --json
```

Missing data or dependencies produce actionable errors. Source import,
index rebuilding, and installation are explicit maintenance operations described
in [maintenance](references/maintenance.md); they are not part of ordinary requests.
