#!/usr/bin/env python3
"""Build the book-swap print kit with a separately supplied design-print-kits skill.

Usage: python build_book_swap.py --skill-root /path/to/design-print-kits
The source is portable: no original project, runtime or staging path is embedded.
All icons explicitly use the Free pack. Sources and license sidecars stay local.
"""
from pathlib import Path
import argparse
import json
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skill-root', type=Path, required=True)
parser.add_argument('--content', type=Path, default=Path(__file__).with_name('content.json'))
parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
parser.add_argument('--accent', default='#285D55')
parser.add_argument('--secondary', default='#C8D9C5')
args = parser.parse_args()
root = args.skill_root.resolve()
sys.path.insert(0, str(root / 'scripts'))

from printkit import Kit, Theme, A4, A5
from icon_catalog import IconStore
from impose import impose
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter

out = args.out.resolve()
out.mkdir(parents=True, exist_ok=True)
data = json.loads(args.content.read_text())
theme = Theme(ink='#25372F', accent=args.accent, secondary=args.secondary,
              muted='#52655B', line='#B2C3B8', tint='#F1F5EF', offset='#E5ECDD',
              body=13.5, leading=17.5, title=26)
kit = Kit(theme=theme)
store = IconStore(root)
icons = ['book-open', 'list-check', 'people-group', 'coins', 'circle-question', 'clock']
for name in icons:
    store.export(*store.read(name, 'classic', 'solid', 'free'), out / 'assets' / f'{name}.svg')

def icon(c, name, x, y, size):
    return kit.icon(c, name, 'classic', 'solid', x, y, size, pack='free')

def line(c, x1, y1, x2, y2, width=.6, color=None):
    c.setStrokeColor(HexColor(color or theme.line))
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

def badge(c, number, x, baseline):
    kit.text(c, number, x, baseline, 10, 'Medium', theme.accent)

def card_header(c, title, subtitle, number, section_icon):
    w, h = A5
    icon(c, 'book-open', 26, h-39, 17)
    kit.text(c, data['identity'], 52, h-33, 10, 'Medium', theme.accent)
    badge(c, number, w-41, h-33)
    kit.text(c, title, 26, h-80, 26, 'Light')
    kit.text(c, subtitle, 26, h-102, 12, 'Regular', theme.muted)
    icon(c, section_icon, w-52, h-86, 24)
    line(c, 26, h-118, w-26, h-118)

def footer(c, text, width):
    kit.text(c, text, 26, 23, 9.5, 'Medium', theme.muted)
    line(c, 26, 42, width-26, 42)

cards = out / 'book-swap-a5-references.pdf'
c = kit.canvas(cards, A5, 'Book swap | A5 setup and volunteer references')
card_header(c, data['setup']['title'], data['setup']['subtitle'], '01', 'list-check')
top = 449
for group in data['setup']['groups']:
    kit.text(c, group['label'].upper(), 26, top, 10.5, 'Medium', theme.accent)
    top -= 19
    for item in group['items']:
        # Reserve a full 45-point row, including wrapping room and checkbox gutter.
        kit.checkbox(c, item, 28, top, A5[0]-56, min_y=top-37)
        top -= 45
    top -= 10
kit.panel(c, 26, 62, A5[0]-52, 73, fill=theme.tint)
kit.paragraph(c, data['setup']['reminder'], 41, 117, A5[0]-82,
              size=12, leading=15.5, weight='Italic', min_y=75)
footer(c, '01 / SETUP', A5[0])
c.showPage()

card_header(c, data['roster']['title'], data['roster']['subtitle'], '02', 'people-group')
xs = [26, 107, 212, 278, A5[0]-26]
top = 453
header_h = 34
row_h = 58
bottom = top-header_h-len(data['roster']['roles'])*row_h
c.setFillColor(HexColor(theme.tint))
c.rect(26, top-header_h, A5[0]-52, header_h, fill=1, stroke=0)
headers = ['Role', 'Name', 'Time', 'Whereabouts']
for i, label in enumerate(headers):
    kit.text(c, label, xs[i]+7, top-21, 10.5, 'Medium', theme.accent)
for x in xs:
    line(c, x, top, x, bottom)
for y in [top, top-header_h]+[top-header_h-row_h*i for i in range(1,7)]:
    line(c, 26, y, A5[0]-26, y)
for i, role in enumerate(data['roster']['roles']):
    row_top = top-header_h-row_h*i
    kit.paragraph(c, role, xs[0]+7, row_top-18, xs[1]-xs[0]-14,
                  size=12, leading=15, weight='Medium', min_y=row_top-row_h+9)
footer(c, '02 / TEAM', A5[0])
c.showPage()
c.save()
kit.finish(cards)

host = out / 'book-swap-a4-facilitator.pdf'
c = kit.canvas(host, A4, 'Book swap | Public prompt and private facilitator notes')
w, h = A4
icon(c, 'book-open', 34, h-49, 20)
kit.text(c, data['identity'], 64, h-41, 11, 'Medium', theme.accent)
badge(c, '03', w-49, h-41)
kit.text(c, 'PUBLIC / WELCOME', 34, h-80, 10.5, 'Medium', theme.accent)
kit.paragraph(c, data['public']['title'], 34, h-96, w-68,
              size=28, leading=31, weight='Light', min_y=h-161)
kit.text(c, data['public']['invitation'], 34, h-184, 14.5, 'Italic', theme.muted)
row_top = h-218
for step in data['public']['steps']:
    icon(c, step['icon'], 34, row_top-27, 25)
    kit.text(c, step['title'], 74, row_top-10, 17, 'Medium')
    kit.paragraph(c, step['text'], 74, row_top-21, w-110,
                  size=13.5, leading=17.5, min_y=row_top-42)
    row_top -= 62

# A strong labeled boundary keeps the public prompt and private notes distinct.
# It is deliberately not labeled as a fold or cut: the sheet stays whole.
line(c, 34, 417, w-34, 417, 1.1, theme.accent)
kit.panel(c, 34, 45, w-68, 347, fill=theme.tint, radius=5)
icon(c, 'book-open', 50, 360, 16)
kit.text(c, '03 / PRIVATE / FACILITATOR ONLY', 75, 365, 10.5, 'Medium', theme.accent)
kit.text(c, data['private']['title'], 50, 331, 23, 'Light')
icon(c, 'clock', w-73, 330, 22)
row_top = 310
for label, note in data['private']['steps']:
    kit.text(c, label, 50, row_top-12, 12.5, 'Medium', theme.accent)
    kit.paragraph(c, note, 121, row_top, w-178, size=13, leading=16.5,
                  min_y=row_top-24)
    row_top -= 31
line(c, 50, 147, w-50, 147)
kit.text(c, 'HELP', 50, 128, 10.5, 'Medium', theme.accent)
kit.paragraph(c, data['private']['help'], 96, 139, w-148,
              size=12, leading=15.5, min_y=99)
kit.text(c, data['private']['pacing'], 50, 71, 11.5, 'Italic', theme.muted)
c.showPage()
c.save()
kit.finish(host)

# Exact ISO A5 faces are placed at 100% using the skill's A4 helper.
# A4's long side is 297 mm; two A5 widths total 296 mm, leaving a 1 mm strip.
sheet = out / 'book-swap-a4-two-up.pdf'
imposition = impose(cards, sheet, paper='a4', theme=theme, mark_width=.75)

combined = out / 'book-swap-print-ready-a4.pdf'
writer = PdfWriter()
for path in [sheet,host]:
    for page in PdfReader(path).pages:
        writer.add_page(page)
writer.add_metadata({'/Title':'Neighborhood book swap | Print-ready A4 kit'})
with combined.open('wb') as stream:
    writer.write(stream)
kit.finish(combined)

imposition.update({'face_mm':[148,210],'sheet_mm':[297,210],
                   'cut_positions_mm_from_left':[148,149],
                   'print_ready_sheet_count':2,'duplex':'Simplex'})
(out/'imposition.json').write_text(json.dumps(imposition, indent=2)+'\n')
print(json.dumps({'pdfs':[str(p) for p in [combined,cards,sheet,host]],
                  'imposition':imposition},indent=2))

(out/'README.txt').write_text("""Book-swap print kit: two A4 sheets, single-sided at 100% / actual size.
Sheet 1 is already two-up: do not apply another multiple-pages setting.
Keep the top and bottom edges intact. The two short bars lie wholly in the
1 mm center waste strip. Cut one edge of that strip by aligning to the two
tips on that side; keep the strip attached to the other card. Align the
opposite tips for the second cut. Either left-first or right-first works.
Alternatively, measure 148 mm inward from each intact outside sheet edge.
The two finished references are exact A5 (148 x 210 mm); discard the strip.
Sheet 2 stays whole as an A4 facilitator sheet. No fold or cut is intended.
""",encoding='utf-8')
