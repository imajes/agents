---
name: design-print-kits
description: Design and refine readable printable cards, checklists, rosters, facilitator notes, and portable reference packs. Use when typography, spacing, semantic icons, cutting, or physical page layout matter; adapt the design to the task rather than applying a fixed template.
---

# Design Print Kits

Design for the person using the physical artifact. The helpers supply primitives and assets, not a mandatory composition.

## Decide what belongs on each face

Infer the reader, use distance, paper and finished sizes, writing needs and production method from context. Ask only about consequential missing constraints. Separate public prompts from private answers when hosting; repeat a small identity icon and number on companion faces. Keep checklists practical, preserve actual assignments, and leave unknown contacts, times or attendance blank.

Keep production instructions, provenance and editing history beside the output unless they help its reader act. Keep facts, examples, names and assignments separate from layout. Verify logic or counts when they determine how an activity works.

## Compose deliberately

Karla Light titles, Regular body, Medium emphasis and true Italic asides are adjustable defaults. Respect a supplied font or tone. Start handheld body text around 12–14 pt; do not solve overflow by making it tiny. Prefer useful labels, weight changes and measured spacing over decoration.

Measure text at its final width. Reserve icon gutters independently from text padding. Give the evidence/details block the same care as the opening block: generous inside padding, space between subsections and diagram labels, and a clear bottom inset. Keep a short pacing reminder on one smaller italic line when possible.

Choose icons by meaning, exact family and exact style; apply semantic roles consistently. Distinguish identifying icons from section icons. For duotone art, use two explicit colors; do not accidentally multiply a pale secondary color by the original opacity. Read [assets and licensing](references/assets.md) when selecting or exporting assets.

Cool blue/sage accents, white space, faint tinted fields, thin borders and small solid offset panels are useful starting points, not a fixed brand. Avoid gradients and heavy fills when ink matters. Color reinforces labels; it cannot replace them.

Examples may wrap as word fields when row pairing has no meaning. Keep complete phrases or person/item examples together, label categories and preserve every example. Use a real table when alignment expresses a relationship. Prioritize handwriting room and usable checkboxes in rosters.

## Produce for real paper

Read [physical layout](references/physical-layout.md) for cutting, lamination and imposition. Prefer simple single-sided output unless requested otherwise. Do not assume a fold, grommet diameter or hole location. Keep vital content clear of trim, seal and hardware areas. Validate the actual sequence of cuts: each retained piece must keep the next cut's references. Corner-only marks can disappear on the first adjacent trim. Use separate waste-side tip pairs inset along each edge, or measured cuts where no waste exists; no guide ink belongs inside the finished faces.

Save editable source, logical card PDFs when useful, and a clearly named print-ready PDF. State finished dimensions and exact sheet counts. Already-imposed sheets print at actual size, one PDF page per sheet. Do not print without an explicit request.

## Portable helpers

Resolve the skill root from its loaded location. Do not use original-project or machine-specific asset paths. Complete supplied Font Awesome archives and Karla fonts are bundled; search the compact index and extract only chosen assets into the current workspace.

- `scripts/icon_catalog.py search QUERY --family FAMILY --style STYLE`: discover exact names and variants.
- `scripts/icon_catalog.py get NAME --family FAMILY --style STYLE --out PATH`: export exact SVG bytes and license/provenance sidecars; missing variants fail.
- `scripts/icon_catalog.py fonts --pack pro-plus`: list complete desktop fonts; `font` exports an exact filename.
- `scripts/printkit.py`: measured text, fonts, vector icons, light panels, word fields and cut marks.
- `scripts/impose.py`: two-up Letter or A4 without scaling.
- `scripts/render_qa.py`: render every page and report size and font embedding; never claim visual approval.

Read [helper usage](references/helpers.md) for APIs. Use the installed PDF/document skill when available for its format-specific tool contract. Python dependencies: ReportLab, pypdf, Pillow. Rendering needs Poppler's pdftoppm and pdffonts. Prefer the provided workspace runtime; don't hardcode its path in generated sources.

## Review and deliver

Render every final page and inspect every unique face and imposed sheet at readable scale. Check clipping, optical spacing, icons, handwriting room, cut placement and actual-size legibility. Text extraction cannot replace visual review. Reused pages may be validated by matching renders, but inspect all unique pages and final impositions.

Check font embedding, page dimensions/counts, no-scaling imposition and changed facts/examples. Fix observed failures and rerender affected pages. On a real permission, dependency or storage denial, identify the action and target and stop; do not switch routes to bypass it.

Report changes, dimensions/counts, source, preview and actual QA. Distinguish built, validated and installed when maintaining this skill. A local installation does not imply cross-device sync.

The bundled Pro/Pro Plus source packs are private licensed assets. Keep them and extracted proprietary sources out of public repositories and shared template distributions. Do not upload or publish the asset-bearing skill merely to deliver a PDF.

