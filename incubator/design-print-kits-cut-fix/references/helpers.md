# Helpers

Use Python with reportlab, pypdf and Pillow, plus Poppler for QA. Paths resolve from the skill, while outputs may live anywhere writable.

## Discover and export

```bash
python scripts/icon_catalog.py search conversation --family duotone --style regular
python scripts/icon_catalog.py get head-side-speak --family duotone --style regular --out ./assets/speaker.svg
python scripts/icon_catalog.py get puzzle --family duotone --style solid --out ./assets/puzzle.svg
python scripts/icon_catalog.py fonts --pack pro-plus
python scripts/icon_catalog.py font "EXACT FILENAME FROM fonts" --pack pro-plus --out ./assets/font.otf
python scripts/icon_catalog.py verify-packs
```

Search returns exact family/style and provider packs. --pack free|pro|pro-plus constrains provenance. Export copies original bytes, license and provenance. Missing names/variants or ambiguous fonts fail; no alternative is fetched.

## Layout primitives

Import the skill's scripts directory into your editable builder:

```python
import sys
sys.path.insert(0, str(skill_root / "scripts"))
from printkit import Theme, Kit, LETTER, HALF_LETTER, A4, A5, HALF_A4
kit = Kit(theme=Theme())
c = kit.canvas(output_path, size=HALF_LETTER)
kit.title(c, "Studio setup", "Before doors open",
          icon=("duotone", "regular", "clipboard-check"))
kit.panel(c, 27, 250, 342, 260)
kit.paragraph(c, "Keep this task readable.", 43, 487, 310, min_y=266)
kit.icon(c, "puzzle", "duotone", "solid", 43, 440, 24)
kit.checkbox(c, "Set out blank labels", 43, 412, 294)
c.showPage()
c.save()
kit.finish(output_path)
```

Coordinates are points from the lower-left. Paragraphs take a top coordinate and return their bottom. Bounds failures raise, never shrink text. title uses actual page width. word_field wraps complete examples and rejects oversized items or too many rows. Choose a readable layout/font size rather than splitting meaningful phrases.

Kit exposes text, paragraph, panel, icon, checkbox, word_field, title and cut_marks; inspect signatures for options. Theme is a dataclass with adjustable colors and typography. Icons accept primary/secondary overrides. The renderer supports normalized M/L/C/Q/Z paths in bundled full SVGs (quadratics are converted to cubics) and rejects unexpected geometry.

## Imposition and review

```bash
python scripts/impose.py logical-cards.pdf print-sheets.pdf --paper letter
python scripts/render_qa.py print-sheets.pdf --out previews --dpi 150
```

Use --paper a4 with exact ISO A5 or HALF_A4 logical faces. A5 is 148 mm wide; HALF_A4 is 148.5 mm. Exact A5 pairs get a 1 mm center trim strip with two horizontal waste-only bars; align their tips for the first cut, retain the strip, then align the opposite tips for the second. Full half-sheet pairs have no printed marks: use one measured center cut from the intact sheet edges. An odd count leaves a reported blank half. No input is modified or scaled. Print preferences specify no scaling and simplex; the returned cut_method and cut_positions_points describe the cutting route.

To match a chosen palette, pass theme=theme and mark_width=.75 to impose(), or use CLI --mark-color '#285D55' --mark-width .75. The default is a 1 pt accent-color mark.

QA writes each page PNG, a contact sheet and JSON sizes/fonts/render status. Its success confirms mechanical checks only. Inspect every unique face and final sheet before recording visual approval in the delivery evidence.

## Adaptable example

The [book-swap builder](../examples/book-swap/build_book_swap.py) and its separate [content](../examples/book-swap/content.json) demonstrate a setup checklist, a blank volunteer roster and a facilitator sheet. It uses exact A5 faces imposed onto A4, a green theme and only Free icon exports. This is a working example, not a required layout.

```bash
python examples/book-swap/build_book_swap.py --skill-root /path/to/design-print-kits --out ./book-swap
```

Pass --content for different content, --accent and --secondary for colors. Adapt the composition when the content or physical use changes. Render and inspect the resulting pages before delivery.

Kit.cut_marks uses paired waste-side tips, inset along each selected edge, and returns their geometry. Align to the tips, not the far ends. It needs real surrounding waste and is intended for an isolated rectangle; a grid or shared edge needs an explicit staged cut plan. See physical-layout.md. scripts/cut_guides.py provides edge_ticks, draw_guides and gutter_ticks.
