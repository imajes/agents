"""Direct-file SVG styling and static PNG rendering."""

import html
import re
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from .common import asset_path, digest, read_json, write_json

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
NEUTRAL = "#243247"
NAMES = {
    "black",
    "white",
    "transparent",
    "red",
    "green",
    "blue",
    "gold",
    "orange",
    "purple",
    "gray",
    "grey",
    "teal",
    "navy",
    "silver",
    "lime",
    "yellow",
    "pink",
    "coral",
}


def color(value, dynamic=False):
    if value in NAMES or re.fullmatch(
        r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})", value
    ):
        return value
    if dynamic and (value == "currentColor" or re.fullmatch(r"var\(--[a-zA-Z0-9_-]+\)", value)):
        return value
    raise ValueError(
        f"Invalid {'CSS' if dynamic else 'static'} color {value!r}; use a hex color or basic named color."
    )


def choose(catalog, name, family=None, weight=None):
    canonical = catalog.canonical(name)
    rows = catalog.variants(canonical, family, weight)
    if not rows:
        available = ", ".join(r["directory"] for r in catalog.variants(canonical))
        raise ValueError(f"Unavailable style for {canonical}; available: {available}")
    return catalog.recommendations(rows)[0]


def svg_text(
    library,
    variant,
    mode="css",
    canvas="cropped",
    primary=None,
    secondary=None,
    secondary_opacity=None,
    title=None,
    size=32,
):
    path = asset_path(library, variant["full_path"] if canvas == "full" else variant["path"])
    original = path.read_text()
    if mode == "original":
        return original
    if not 1 <= size <= 8192:
        raise ValueError("Size must be between 1 and 8192 pixels.")
    primary = color(primary or ("currentColor" if mode == "css" else NEUTRAL), mode == "css")
    secondary = color(secondary or primary, mode == "css")
    if secondary_opacity is not None and not 0 <= secondary_opacity <= 1:
        raise ValueError("Secondary opacity must be between 0 and 1.")
    root = ET.fromstring(original)
    _, _, width, height = [float(v) for v in root.attrib["viewBox"].split()]
    root.set("height", str(size))
    root.set("width", f"{size * width / height:g}")
    root.set("class", "ic-icon")
    if title:
        root.set("role", "img")
        root.set("aria-label", title)
        title_node = ET.Element(f"{{{NS}}}title")
        title_node.text = title
        root.insert(0, title_node)
    else:
        root.set("aria-hidden", "true")
    root.set("focusable", "false")
    for node in root.findall(f".//{{{NS}}}path"):
        opacity = float(node.attrib.get("opacity", 1))
        is_secondary = opacity < 1
        role = "secondary" if is_secondary else "primary"
        base_opacity = secondary_opacity if is_secondary and secondary_opacity is not None else opacity
        node.set("class", f"ic-{role} fa-{role}")
        fill = secondary if is_secondary else primary
        if mode == "css":
            node.set("fill", f"var(--fa-{role}-color, {fill})")
            node.set("style", f"opacity:var(--fa-{role}-opacity, {base_opacity:g})")
        else:
            node.set("fill", fill)
        node.set("opacity", f"{base_opacity:g}")
    return ET.tostring(root, encoding="unicode")


def export(
    catalog,
    name,
    output,
    family=None,
    weight=None,
    fmt="svg",
    mode="css",
    canvas=None,
    primary=None,
    secondary=None,
    secondary_opacity=None,
    size=32,
    title=None,
    overwrite=False,
):
    variant = choose(catalog, name, family, weight)
    if fmt == "png":
        if mode == "original":
            raise ValueError("PNG requires static colors; choose static or css mode with concrete colors.")
        mode = "static"
    if mode == "original" and (primary or secondary or secondary_opacity is not None or title):
        raise ValueError(
            "Original mode preserves source bytes; use css or static mode to apply colors or a title."
        )
    canvas = canvas or ("full" if fmt == "png" or mode == "static" else "cropped")
    if not 1 <= size <= 8192:
        raise ValueError("Size must be between 1 and 8192 pixels.")
    text = svg_text(
        catalog.library, variant, mode, canvas, primary, secondary, secondary_opacity, title, size
    )
    output = Path(output).expanduser().resolve()
    stem = f"{variant['name']}--{variant['directory']}--{canvas}--{mode}"
    target = output / f"{stem}.{fmt}"
    manifest_path = output / f"{stem}.{fmt}.json"
    if not overwrite and (target.exists() or manifest_path.exists()):
        raise ValueError(f"Output exists: {target}; use --overwrite to replace it.")
    payload = text.encode()
    if fmt == "png":
        renderer = shutil.which("rsvg-convert")
        if not renderer:
            raise ValueError("PNG export needs rsvg-convert (librsvg). SVG export is available.")
        payload = subprocess.run(
            [renderer, "--format=png", "--height", str(size)], input=payload, capture_output=True, check=True
        ).stdout
    license_path = output / "FONT_AWESOME_LICENSE.txt"
    license_text = (catalog.library / "desktop/LICENSE.txt").read_bytes()
    if license_path.exists() and license_path.read_bytes() != license_text:
        raise ValueError(f"Conflicting license file: {license_path}")
    output.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    # Include the supplied license alongside selected artwork without changing it.
    license_path.write_bytes(license_text)
    root = ET.fromstring(text)
    vb = [float(v) for v in root.attrib["viewBox"].split()]
    source_manifest = read_json(catalog.library / "source-manifest.json")
    result = {
        "schema_version": 1,
        "icon": variant["name"],
        "family": variant["family"],
        "weight": variant["weight"],
        "format": fmt,
        "mode": mode,
        "canvas": canvas,
        "path": str(target),
        "manifest": str(manifest_path),
        "width": root.attrib.get("width") if mode == "original" else round(size * vb[2] / vb[3], 3),
        "height": root.attrib.get("height") if mode == "original" else size,
        "view_box": vb,
        "colors": {
            "primary": primary or ("currentColor" if mode == "css" else NEUTRAL),
            "secondary": secondary or primary or ("currentColor" if mode == "css" else NEUTRAL),
            "secondary_opacity": secondary_opacity if secondary_opacity is not None else "source",
        },
        "source": {
            "distribution": source_manifest["distribution"],
            "version": source_manifest["version"],
            "asset": variant["full_path"] if canvas == "full" else variant["path"],
            "sha256": digest(
                asset_path(catalog.library, variant["full_path"] if canvas == "full" else variant["path"])
            ),
        },
        "output_sha256": digest(target),
        "license": str(license_path),
        "dependencies": ["Inline SVG: CSS variables may be set by the host."] if mode == "css" else [],
    }
    if fmt == "png":
        result["width"], result["height"] = struct.unpack(">II", payload[16:24])
    if mode == "original":
        result["colors"] = {
            "primary": "source currentColor",
            "secondary": "source",
            "secondary_opacity": "source",
        }
    write_json(manifest_path, result)
    return result


PAGE_CSS = """
:root{color-scheme:light dark;font-family:Karla,system-ui,sans-serif;background:#edf1f5;color:#243247}
body{max-width:1160px;margin:auto;padding:32px}h1,h2{font-family:system-ui,sans-serif}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:16px}
.card{border:1px solid #c3cddd;border-radius:14px;overflow:hidden;background:white;color:#243247}
.sample{display:flex;align-items:center;justify-content:center;gap:28px;padding:24px;min-height:88px}
.dark{background:#162134;color:#edf1f5}.label{padding:12px 16px;font-size:14px;line-height:1.5}
.ic-icon{display:inline-block;vertical-align:-.125em;flex:none}code{font-size:12px}
"""


def preview(
    catalog,
    names,
    output,
    all_variants=False,
    family=None,
    weight=None,
    primary=None,
    secondary=None,
    background="#162134",
    overwrite=False,
):
    background = color(background)
    cards = []
    for name in names:
        canonical = catalog.canonical(name)
        variants = catalog.variants(canonical, family, weight)
        if not variants:
            raise ValueError(f"No matching styles for {canonical}")
        if not all_variants:
            variants = catalog.recommendations(variants)
        for variant in variants:
            light = "".join(
                svg_text(catalog.library, variant, "static", "full", primary or NEUTRAL, secondary, size=s)
                for s in (20, 48)
            )
            dark = "".join(
                svg_text(catalog.library, variant, "static", "full", primary or "#edf1f5", secondary, size=s)
                for s in (20, 48)
            )
            label = html.escape(f"{canonical} / {variant['family']} / {variant['weight']}")
            cards.append(
                f'<article class="card"><div class="sample">{light}</div>'
                f'<div class="sample dark" style="background:{background}">{dark}</div>'
                f'<div class="label">{label}</div></article>'
            )
    path = Path(output).expanduser().resolve()
    if path.exists() and not overwrite:
        raise ValueError(f"Output exists: {path}")
    document = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Icon comparison</title><style>{PAGE_CSS}</style>"
        "<h1>Icon comparison</h1><p>20 px and 48 px · light and dark surfaces</p>"
        f'<main class="grid">{"".join(cards)}</main></html>'
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document)
    return {"path": str(path), "cards": len(cards), "schema_version": 1}
