"""Portable print-design primitives. All dimensions are PDF points."""
from pathlib import Path
from dataclasses import dataclass
import re,xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as LETTER,A4,A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,DictionaryObject
from icon_catalog import IconStore
ROOT=Path(__file__).resolve().parents[1]
HALF_LETTER=(LETTER[1]/2,LETTER[0]);HALF_A4=(A4[1]/2,A4[0])
NUMBER=r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?'
@dataclass
class Theme:
    ink:str='#243844'
    accent:str='#315F79'
    secondary:str='#A8C6BD'
    muted:str='#506574'
    line:str='#BACBD2'
    tint:str='#F0F5F2'
    offset:str='#DEE8EE'
    body:float=13
    leading:float=16.5
    title:float=25
    label:float=11
class Kit:
    def __init__(self,theme=None,font_dir=None,font_files=None):
        self.theme=theme or Theme();self._icons=None
        font_dir=Path(font_dir) if font_dir else ROOT/'assets/fonts'
        files=font_files or {n:'Karla-'+n+'.ttf' for n in ['Light','Regular','Medium','Italic']}
        for style,file in files.items():pdfmetrics.registerFont(TTFont('PK-'+style,str(font_dir/file)))
        pdfmetrics.registerFontFamily('PK-Regular',normal='PK-Regular',bold='PK-Medium',italic='PK-Italic',boldItalic='PK-Italic')
    def canvas(self,path,size=LETTER,title=''):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        c=canvas.Canvas(str(path),pagesize=size,initialFontName='PK-Regular',initialFontSize=self.theme.body)
        c.setTitle(title);return c
    def text(self,c,s,x,y,size=None,weight='Regular',color=None):
        size=size or self.theme.body
        if x<0 or y<0 or x+pdfmetrics.stringWidth(s,'PK-'+weight,size)>c._pagesize[0]+.01:raise ValueError('Text exceeds page: '+s)
        c.setFillColor(HexColor(color or self.theme.ink));c.setFont('PK-'+weight,size);c.drawString(x,y,s)
    def paragraph(self,c,s,x,top,width,size=None,leading=None,weight='Regular',color=None,min_y=0):
        size=size or self.theme.body;leading=leading or (self.theme.leading if size==self.theme.body else size*1.26)
        p=Paragraph(s.replace('\n','<br/>'),ParagraphStyle('p',fontName='PK-'+weight,fontSize=size,leading=leading,textColor=HexColor(color or self.theme.ink)))
        _,height=p.wrap(width,10000)
        if top-height<min_y:raise ValueError(f'Paragraph overflows floor {min_y}: bottom={top-height:.2f}: {s[:70]}')
        if x<0 or x+width>c._pagesize[0]+.01:raise ValueError('Paragraph exceeds page width')
        p.drawOn(c,x,top-height);return top-height
    def panel(self,c,x,y,width,height,fill='#FFFFFF',offset=None,radius=5):
        if min(width,height)<=0:raise ValueError('Panel dimensions must be positive')
        c.setFillColor(HexColor(offset or self.theme.offset));c.roundRect(x+3,y-3,width,height,radius,fill=1,stroke=0)
        c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(self.theme.line));c.setLineWidth(.55);c.roundRect(x,y,width,height,radius,fill=1,stroke=1)
    def icon(self,c,name,family,style,x,y,size=28,primary=None,secondary=None,pack=None):
        if self._icons is None:self._icons=IconStore()
        raw,info=self._icons.read(name,family,style,pack)
        root=ET.fromstring(raw);vx,vy,vw,vh=map(float,root.attrib['viewBox'].split())
        paths=list(root)
        if any(p.tag.split('}')[-1]!='path' for p in paths):raise ValueError('Unsupported SVG geometry: '+name)
        scale=size/max(vw,vh)
        c.saveState();c.translate(x+(size-vw*scale)/2,y+(size+vh*scale)/2);c.scale(scale,-scale);c.translate(-vx,-vy)
        for element in paths:
            if 'transform' in element.attrib:raise ValueError('Unsupported SVG transform: '+name)
            d=element.attrib['d']
            commands=re.findall('[A-Za-z]',re.sub(NUMBER,'',d))
            if set(commands)-set('MLCQZz'):raise ValueError('Unsupported SVG commands: '+str(set(commands)))
            tokens=re.findall('[MLCQZz]|'+NUMBER,d);path=c.beginPath();i=0;op=None;current=(0,0);start=(0,0)
            while i<len(tokens):
                if tokens[i] in 'MLCQZz':
                    op=tokens[i];i+=1
                    if op in 'Zz':path.close();current=start;op=None;continue
                if op is None:raise ValueError('Path has no command')
                count={'M':2,'L':2,'C':6,'Q':4}[op];values=list(map(float,tokens[i:i+count]));i+=count
                if len(values)!=count:raise ValueError('Truncated SVG path')
                if op=='M':path.moveTo(*values);current=tuple(values);start=current;op='L'
                elif op=='L':path.lineTo(*values);current=tuple(values)
                elif op=='C':path.curveTo(*values);current=tuple(values[-2:])
                else:
                    qx,qy,ex,ey=values;cx,cy=current
                    path.curveTo(cx+2*(qx-cx)/3,cy+2*(qy-cy)/3,ex+2*(qx-ex)/3,ey+2*(qy-ey)/3,ex,ey)
                    current=(ex,ey)
            is_secondary=float(element.attrib.get('opacity','1'))<1 or 'secondary' in element.attrib.get('class','')
            color=(secondary or self.theme.secondary) if is_secondary else (primary or self.theme.accent)
            c.setFillColor(HexColor(color));c.drawPath(path,fill=1,stroke=0,fillMode=1)
        c.restoreState();return info
    def title(self,c,title,subtitle='',icon=None,number=None,margin=27):
        w,h=c._pagesize;x=margin
        if icon:
            family,style,name=icon;self.icon(c,name,family,style,margin,h-69,36);x+=45
        self.text(c,title,x,h-42,self.theme.title,'Light')
        if subtitle:self.text(c,subtitle,x,h-63,10,'Italic',self.theme.muted)
        if number is not None:self.text(c,str(number),w-margin-22,h-39,11,'Medium',self.theme.accent)
        return h-91
    def checkbox(self,c,s,x,top,width,size=None,min_y=0):
        c.setStrokeColor(HexColor(self.theme.accent));c.setLineWidth(.7);c.rect(x,top-12,10,10,fill=0,stroke=1)
        return self.paragraph(c,s,x+21,top,width-21,size=size,min_y=min_y)-14
    def word_field(self,c,items,label,x,top,width,height,size=18,leading=29,tint=None,padding=14):
        c.setFillColor(HexColor(tint or self.theme.tint));c.roundRect(x,top-height,width,height,4,fill=1,stroke=0)
        self.text(c,label.upper(),x+padding,top-20,10,'Medium',self.theme.accent)
        cursor=x+padding;baseline=top-44
        for item in items:
            advance=pdfmetrics.stringWidth(item,'PK-Light',size)
            if advance>width-2*padding:raise ValueError('Whole example exceeds field width: '+item)
            if cursor>x+padding and cursor+advance>x+width-padding:cursor=x+padding;baseline-=leading
            if baseline-size*.25<top-height+padding:raise ValueError('Word field has too many lines')
            self.text(c,item,cursor,baseline,size,'Light');cursor+=advance+20
        return top-height
    def cut_marks(self,c,x,y,width,height,length=12,stroke=1,inset=24,
                  edges=('left','right','bottom','top')):
        from cut_guides import edge_ticks,draw_guides
        guides=edge_ticks((x,y,x+width,y+height),edges,inset,length)
        draw_guides(c,guides,HexColor(self.theme.accent),stroke)
        return guides
    @staticmethod
    def finish(path):
        path=Path(path);r=PdfReader(path);w=PdfWriter();w.clone_document_from_reader(r)
        w._root_object[NameObject('/ViewerPreferences')]=DictionaryObject({NameObject('/PrintScaling'):NameObject('/None'),NameObject('/Duplex'):NameObject('/Simplex')})
        with path.open('wb') as f:w.write(f)
