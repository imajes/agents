#!/usr/bin/env python3
"""Impose two half-size portrait faces onto landscape Letter/A4 without scaling."""
from pathlib import Path
import argparse,io,json
from pypdf import PdfReader,PdfWriter,PageObject,Transformation
from printkit import Kit,Theme,LETTER,A4,A5
def impose(source,target,paper='letter',marks=True,theme=None,mark_width=1):
    size=LETTER if paper=='letter' else A4
    width,height=size[1],size[0];card=(width/2,height)
    if Path(source).resolve()==Path(target).resolve():raise ValueError('Source and print output must be different paths')
    reader=PdfReader(source);writer=PdfWriter();kit=Kit(theme=theme)
    if mark_width<=0:raise ValueError('Mark width must be positive')
    if not reader.pages:raise ValueError('No source faces')
    first=(float(reader.pages[0].mediabox.width),float(reader.pages[0].mediabox.height))
    allowed=[card]+([A5] if paper=='a4' else [])
    if not any(all(abs(a-b)<.05 for a,b in zip(first,shape)) for shape in allowed):raise ValueError(f'Expected half-{paper} {card}'+(f' or ISO A5 {A5}' if paper=='a4' else '')+f', got {first}; refusing to scale')
    card=first;gap=width-2*card[0]
    for page in reader.pages:
        actual=(float(page.mediabox.width),float(page.mediabox.height))
        if any(abs(a-b)>.05 for a,b in zip(actual,card)):raise ValueError('All faces must have the same dimensions')
        if page.get('/Rotate',0)%360:raise ValueError('Normalize page rotation before imposition')
    for i in range(0,len(reader.pages),2):
        page=PageObject.create_blank_page(width=width,height=height)
        page.merge_transformed_page(reader.pages[i],Transformation())
        if i+1<len(reader.pages):page.merge_transformed_page(reader.pages[i+1],Transformation().translate(width-card[0],0))
        if marks and gap>.05:
            buff=io.BytesIO()
            from reportlab.pdfgen.canvas import Canvas
            from reportlab.lib.colors import HexColor
            from cut_guides import gutter_ticks,draw_guides
            c=Canvas(buff,pagesize=(width,height),initialFontName='PK-Regular')
            # Both tips lie in the center waste. First cut leaves the same
            # two bars with the opposite tips available for the second cut.
            draw_guides(c,gutter_ticks(card[0],width-card[0],height),HexColor(kit.theme.accent),mark_width)
            c.save()
            buff.seek(0);page.merge_page(PdfReader(buff).pages[0])
        writer.add_page(page)
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('wb') as f:writer.write(f)
    kit.finish(target)
    return {'source_faces':len(reader.pages),'print_sheets':len(writer.pages),'blank_half':bool(len(reader.pages)%2),'paper':paper,'scale':1,'sheet_points':[width,height],'card_points':list(card),'center_trim_strip_points':gap,'cut_method':'two gutter-edge cuts; align blade to inner tips, retain gutter until second cut' if gap>.05 and marks else 'measure one card width inward from an intact outer sheet edge for each cut; no printed marks','cut_positions_points':[card[0],width-card[0]] if gap>.05 else [width/2]}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('target');p.add_argument('--paper',choices=['letter','a4'],default='letter');p.add_argument('--mark-color');p.add_argument('--mark-width',type=float,default=1);a=p.parse_args()
    try:print(json.dumps(impose(a.source,a.target,a.paper,theme=Theme(accent=a.mark_color) if a.mark_color else None,mark_width=a.mark_width),indent=2))
    except ValueError as e:raise SystemExit(str(e))
