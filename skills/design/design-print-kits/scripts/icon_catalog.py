#!/usr/bin/env python3
"""Search and export exact bundled Font Awesome variants and desktop fonts."""
from pathlib import Path
import argparse,gzip,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
class IconStore:
    def __init__(self,root=None):
        self.assets=(Path(root) if root else ROOT)/'assets/fontawesome'
        self.manifest=json.loads((self.assets/'manifest.json').read_text())
        self.packs={p['id']:p for p in self.manifest['packs']}
        with gzip.open(self.assets/'index.json.gz','rt',encoding='utf8') as f:self.icons=json.load(f)['icons']
        self.names={i['name']:i for i in self.icons}
        self._archives={}
    def variants(self,item,family=None,style=None,pack=None):
        return [v for v in item['variants'] if (not family or v['family']==family) and (not style or v['style']==style) and (not pack or pack in v['providers'])]
    def search(self,query,family=None,style=None,pack=None,limit=12):
        terms=query.lower().split();found=[]
        for item in self.icons:
            hay=' '.join([item['name'],item['label']]+item['terms']).lower()
            variants=self.variants(item,family,style,pack)
            if variants and all(t in hay for t in terms):
                score=100 if query.lower()==item['name'] else 10*sum(t in item['name'] for t in terms)
                found.append((score,{'name':item['name'],'canonical':item['canonical'],'label':item['label'],'variants':[{'family':v['family'],'style':v['style'],'packs':list(v['providers'])} for v in variants]}))
        return [r for _,r in sorted(found,key=lambda pair:(-pair[0],pair[1]['name']))[:limit]]
    def read(self,name,family,style,pack=None):
        if name not in self.names:raise ValueError('Unknown exact icon name: '+name)
        variants=self.variants(self.names[name],family,style,pack)
        if len(variants)!=1:raise ValueError(f'No exact variant for {name} {family}/{style}, pack={pack}')
        v=variants[0];pack=pack or next(p for p in ['pro-plus','pro','free'] if p in v['providers'])
        p=self.packs[pack];member=v['providers'][pack]
        if pack not in self._archives:self._archives[pack]=zipfile.ZipFile(self.assets/p['archive'])
        raw=self._archives[pack].read(member)
        return raw,{'name':name,'family':family,'style':style,'pack':pack,'archive':p['archive'],'member':member,'sha256':hashlib.sha256(raw).hexdigest(),'license':p['license']}
    def export(self,raw,info,out):
        out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        out.with_name(out.name+'.provenance.json').write_text(json.dumps(info,indent=2)+'\n')
        out.with_name(out.name+'.LICENSE.txt').write_bytes((self.assets/info['license']).read_bytes())
        return {'output':str(out.resolve()),**info}
def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    for action in ['search','get']:
        p=sub.add_parser(action);p.add_argument('name');p.add_argument('--family',required=action=='get');p.add_argument('--style',required=action=='get');p.add_argument('--pack',choices=['free','pro','pro-plus'])
        if action=='search':p.add_argument('--limit',type=int,default=12)
        else:p.add_argument('--out',required=True)
    p=sub.add_parser('fonts');p.add_argument('--pack',required=True,choices=['free','pro','pro-plus'])
    p=sub.add_parser('font');p.add_argument('name');p.add_argument('--pack',required=True,choices=['free','pro','pro-plus']);p.add_argument('--out',required=True)
    sub.add_parser('verify-packs')
    a=parser.parse_args();store=IconStore()
    if a.action=='search':result=store.search(a.name,a.family,a.style,a.pack,a.limit)
    elif a.action=='get':result=store.export(*store.read(a.name,a.family,a.style,a.pack),a.out)
    elif a.action=='fonts':result=store.packs[a.pack]['fonts']
    elif a.action=='font':
        p=store.packs[a.pack];members=[n for n in p['fonts'] if Path(n).name==a.name]
        if len(members)!=1:raise ValueError('Use one exact filename returned by fonts')
        with zipfile.ZipFile(store.assets/p['archive']) as z:raw=z.read(members[0])
        result=store.export(raw,{'pack':a.pack,'member':members[0],'sha256':hashlib.sha256(raw).hexdigest(),'license':p['license']},a.out)
    else:
        result=[]
        for p in store.manifest['packs']:
            h=hashlib.sha256()
            with (store.assets/p['archive']).open('rb') as f:
                for block in iter(lambda:f.read(1048576),b''):h.update(block)
            if h.hexdigest()!=p['sha256']:raise ValueError('Archive checksum mismatch: '+p['id'])
            result.append({'pack':p['id'],'sha256':h.hexdigest(),'verified':True})
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,FileNotFoundError,KeyError) as e:raise SystemExit(str(e))
