#!/usr/bin/env python3
"""Render every PDF page and report mechanical checks; visual review remains pending."""
from pathlib import Path
import argparse,json,re,shutil,subprocess
from pypdf import PdfReader
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def review(pdf,out,dpi=150):
    for tool in ['pdftoppm','pdffonts']:
        if not shutil.which(tool):raise RuntimeError('Required rendering tool missing: '+tool)
    pdf=Path(pdf).resolve();out=Path(out);out.mkdir(parents=True,exist_ok=True)
    reader=PdfReader(pdf);prefix=out/'page'
    subprocess.run(['pdftoppm','-r',str(dpi),'-png',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL)
    pages=sorted(out.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
    if len(pages)!=len(reader.pages):raise ValueError('Render count differs; use a fresh output directory')
    fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
    rows=fonts.splitlines()[2:];unembedded=[line for line in rows if not re.search(r'\byes\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$',line)]
    if unembedded:raise ValueError('Unembedded fonts: '+repr(unembedded))
    columns=min(3,len(pages));rows_count=(len(pages)+columns-1)//columns;cw,ch=450,635
    contact=Image.new('RGB',(cw*columns,ch*rows_count),'#E7EDEF');draw=ImageDraw.Draw(contact)
    font=ImageFont.truetype(str(ROOT/'assets/fonts/Karla-Regular.ttf'),19)
    for i,path in enumerate(pages):
        im=Image.open(path).convert('RGB');im.thumbnail((cw-24,ch-42),Image.Resampling.LANCZOS)
        x=(i%columns)*cw+(cw-im.width)//2;y=(i//columns)*ch+8
        contact.paste(im,(x,y));draw.text(((i%columns)*cw+16,(i//columns)*ch+ch-30),str(i+1),font=font,fill='#243844')
    contact.save(out/'contact-sheet.png')
    report={'pdf':str(pdf),'pages':len(reader.pages),'page_points':[[float(p.mediabox.width),float(p.mediabox.height)] for p in reader.pages],'dpi':dpi,'font_report':fonts,'all_fonts_embedded':True,'rendered_pages':[str(p.resolve()) for p in pages],'visual_review':'pending: open and inspect every unique page and imposed sheet'}
    (out/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf');p.add_argument('--out',required=True);p.add_argument('--dpi',type=int,default=150);a=p.parse_args()
    try:
        r=review(a.pdf,a.out,a.dpi);print(json.dumps({k:v for k,v in r.items() if k not in ['font_report','rendered_pages']},indent=2))
    except (ValueError,RuntimeError) as e:raise SystemExit(str(e))

