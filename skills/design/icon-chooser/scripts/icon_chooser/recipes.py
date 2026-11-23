"""Generate executable recipes using only selected native icon definitions."""

import html
import json
from pathlib import Path

from .common import connect, read_json, write_json
from .rendering import NEUTRAL, PAGE_CSS, choose, color, svg_text

TOPICS = (
    "all",
    "sizing",
    "alignment",
    "duotone",
    "rotation",
    "lists",
    "stacking",
    "motion",
    "transforms",
    "masking",
    "layers",
    "accessibility",
)


def native_definition(catalog, variant):
    db = connect(catalog.library, "native.sqlite")
    try:
        row = db.execute(
            "SELECT prefix,definition FROM definitions WHERE directory=? AND name=?",
            (variant["directory"], variant["name"]),
        ).fetchone()
        if not row:
            raise ValueError(f"No native definition for {variant['directory']}/{variant['name']}")
        return {"prefix": row["prefix"], "iconName": variant["name"], "icon": json.loads(row["definition"])}
    finally:
        db.close()


def generate(
    catalog,
    name,
    output,
    family=None,
    weight=None,
    primary=None,
    secondary=None,
    topic="all",
    overwrite=False,
):
    selected = choose(catalog, name, family, weight)
    primary = color(primary or NEUTRAL, dynamic=True)
    secondary = color(secondary or primary, dynamic=True)
    definition = native_definition(catalog, selected)
    mask = native_definition(catalog, choose(catalog, "circle", "classic", "solid"))
    tag = f'<i class="{selected["prefix"]} fa-{selected["name"]}" aria-hidden="true"></i>'

    def icon(classes="", attributes=""):
        return f'<i class="{selected["prefix"]} fa-{selected["name"]} {classes}" aria-hidden="true" {attributes}></i>'

    sections = {
        "sizing": "<p>"
        + " ".join(icon(c) for c in ["fa-xs", "fa-lg", "fa-2x", "fa-4x"])
        + "</p><p>"
        + icon("fa-width-auto")
        + " Natural width · "
        + icon()
        + " fixed canvas</p>",
        "alignment": '<button type="button">'
        + icon()
        + " Labelled action</button><p>"
        + icon("fa-border fa-pull-left fa-2x")
        + "A bordered icon beside a text paragraph.</p>",
        "duotone": '<p class="palette">' + icon("fa-3x") + " " + icon("fa-3x fa-swap-opacity") + "</p>",
        "rotation": "<p>" + icon("fa-2x fa-rotate-90") + " " + icon("fa-2x fa-flip-horizontal") + "</p>",
        "lists": '<ul class="fa-ul"><li><span class="fa-li">'
        + tag
        + "</span>First item</li>"
        + '<li><span class="fa-li">'
        + tag
        + "</span>Second item</li></ul>",
        "stacking": '<span class="fa-stack fa-2x"><i class="fas fa-circle fa-stack-2x" aria-hidden="true"></i>'
        + icon("fa-stack-1x", 'style="--fa-primary-color:white;--fa-secondary-color:white"')
        + "</span>",
        "motion": '<label><input id="reduced-motion-preview" type="checkbox"> Preview reduced motion</label>'
        + '<p class="motion">'
        + " ".join(
            icon("fa-2x " + c)
            for c in [
                "fa-beat",
                "fa-fade",
                "fa-beat-fade",
                "fa-bounce",
                "fa-flip",
                "fa-shake",
                "fa-spin",
                "fa-spin-pulse",
            ]
        )
        + "</p>",
        "transforms": '<span id="transform-demo"></span>',
        "masking": '<span id="mask-demo"></span>',
        "layers": '<span class="fa-layers fa-3x">'
        + tag
        + '<span class="fa-layers-counter" aria-hidden="true">3</span></span>'
        + '<span class="fa-layers fa-3x"><i class="fas fa-circle" aria-hidden="true"></i>'
        + '<span class="fa-layers-text" data-fa-transform="shrink-10" style="color:white">A</span></span>'
        + '<span class="sr-only">Three notifications; category A.</span>',
        "accessibility": '<button type="button" aria-label="Open details">'
        + tag
        + "</button>"
        + "<p>"
        + svg_text(catalog.library, selected, title="Meaningful example", size=32)
        + "</p>",
    }
    topics = list(sections) if topic == "all" else [topic]
    body = "".join(
        f'<section><h2>{html.escape(t.title())}</h2><div class="example">{sections[t]}</div>'
        f"<details><summary>HTML</summary><pre><code>{html.escape(sections[t])}</code></pre></details></section>"
        for t in topics
    )
    css = (
        PAGE_CSS
        + f"""
body{{--fa-primary-color:{primary};--fa-secondary-color:{secondary};--fa-secondary-opacity:.4}}
section{{background:white;color:#243247;border:1px solid #c3cddd;border-radius:14px;padding:20px;margin:18px 0}}
.example{{min-height:64px;display:flow-root}}.example p{{line-height:2}}button{{font:inherit;padding:10px 16px}}
.palette{{--fa-primary-color:{primary};--fa-secondary-color:{secondary}}}
.motion{{--fa-animation-duration:2s;display:flex;gap:24px;flex-wrap:wrap}}
pre{{overflow:auto;white-space:pre-wrap}}.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}
.reduced-motion-preview *{{animation:none!important;transition:none!important}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important}}}}
"""
    )
    js = (
        '"use strict";\nconst selected='
        + json.dumps(definition)
        + ";\nconst mask="
        + json.dumps(mask)
        + """;
FontAwesome.library.add(selected, mask);
const transform = FontAwesome.parse.transform("shrink-6 rotate-20 right-1");
const transformed = document.getElementById("transform-demo");
if (transformed) transformed.innerHTML = FontAwesome.icon(selected, {transform, classes:["fa-3x"]}).html.join("");
const masked = document.getElementById("mask-demo");
if (masked) masked.innerHTML = FontAwesome.icon(selected, {
  transform:FontAwesome.parse.transform("shrink-6"), mask, maskId:"icon-chooser-mask", classes:["fa-3x"]
}).html.join("");
FontAwesome.dom.i2svg();
const motionPreview = document.getElementById("reduced-motion-preview");
if (motionPreview) motionPreview.addEventListener("change", () => {
  document.body.classList.toggle("reduced-motion-preview", motionPreview.checked);
});
"""
    )
    page = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Icon integration recipes</title><link rel="stylesheet" href="svg-with-js.min.css">'
        '<link rel="stylesheet" href="recipes.css"><script defer src="fontawesome.min.js"></script>'
        '<script defer src="icons.js"></script><h1>Icon integration recipes</h1>'
        f"<p>{html.escape(selected['name'])} · {html.escape(selected['family'])} · {selected['weight']}</p>"
        "<p>Local Font Awesome SVG + JS runtime. Motion respects reduced-motion settings.</p>"
        + body
        + "</html>"
    )
    output = Path(output).expanduser().resolve()
    contents = {
        "index.html": page,
        "recipes.css": css,
        "icons.js": js,
        "fontawesome.min.js": (catalog.library / "web/js/fontawesome.min.js").read_text(),
        "svg-with-js.min.css": (catalog.library / "web/css/svg-with-js.min.css").read_text(),
        "FONT_AWESOME_LICENSE.txt": (catalog.library / "desktop/LICENSE.txt").read_text(),
    }
    if not overwrite:
        existing = [str(output / n) for n in (*contents, "manifest.json") if (output / n).exists()]
        if existing:
            raise ValueError("Recipe files exist: " + ", ".join(existing))
    output.mkdir(parents=True, exist_ok=True)
    for filename, text in contents.items():
        (output / filename).write_text(text)
    result = {
        "schema_version": 1,
        "path": str(output / "index.html"),
        "topics": topics,
        "icon": selected["name"],
        "family": selected["family"],
        "weight": selected["weight"],
        "files": [str(output / n) for n in contents],
        "source": read_json(catalog.library / "source-manifest.json"),
        "dependencies": ["Bundled Font Awesome SVG + JS core and SVG CSS; no network required."],
        "note": "Single-layer icons use one color. Two-layer controls apply only to actual multi-layer variants.",
    }
    write_json(output / "manifest.json", result)
    return result
