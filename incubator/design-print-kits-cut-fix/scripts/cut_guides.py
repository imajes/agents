"""Waste-side cut references in PDF points; draw with butt line caps.

Tips terminate exactly at a trim line. Two tips are inset along each edge,
so adjacent outer trims do not remove the next edge's references.
Shared card edges have no waste: cut them before outer trimming, or measure
from intact sheet edges instead of printing ink inside finished cards.
"""

def edge_ticks(rect, edges=('left','right','bottom','top'), inset=24, length=12):
    x0,y0,x1,y1=rect
    if min(x1-x0,y1-y0)<=2*inset or inset<=0 or length<=0:
        raise ValueError('Two separated inset references require a larger rectangle')
    result=[]
    for edge in edges:
        if edge in ('left','right'):
            tip=x0 if edge=='left' else x1
            start=tip-length if edge=='left' else tip+length
            for y in (y0+inset,y1-inset):
                result.append({'edge':edge,'line':[start,y,tip,y],'tip':[tip,y]})
        elif edge in ('bottom','top'):
            tip=y0 if edge=='bottom' else y1
            start=tip-length if edge=='bottom' else tip+length
            for x in (x0+inset,x1-inset):
                result.append({'edge':edge,'line':[x,start,x,tip],'tip':[x,tip]})
        else:
            raise ValueError('Unknown edge: '+edge)
    return result

def draw_guides(c,guides,color,stroke=1):
    if stroke<=0: raise ValueError('Stroke must be positive')
    width,height=c._pagesize
    for g in guides:
        x0,y0,x1,y1=g['line']
        if min(x0,x1)<0 or max(x0,x1)>width or min(y0,y1)<0 or max(y0,y1)>height:
            raise ValueError('Cut references need real waste space inside the sheet')
    c.saveState();c.setStrokeColor(color);c.setLineWidth(stroke);c.setLineCap(0)
    for g in guides: c.line(*g['line'])
    c.restoreState()

def gutter_ticks(left,right,height,inset=18):
    if right-left<=0 or height<=2*inset:
        raise ValueError('Gutter ticks require positive waste width and separated references')
    return [{'edge':'gutter','line':[left,y,right,y],
             'left_tip':[left,y],'right_tip':[right,y]} for y in (inset,height-inset)]
