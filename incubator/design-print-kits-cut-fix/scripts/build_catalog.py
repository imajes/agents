#!/usr/bin/env python3
"""Rebuild the compact catalog from complete bundled archives; no network."""
from pathlib import Path
import gzip, hashlib, json, zipfile
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets/fontawesome'
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def main():
    paths=sorted((ASSETS/'packs').glob('*.zip'))
    if not paths:raise SystemExit('No bundled packs')
    plus=next(p for p in paths if 'pro-plus-' in p.name)
    with zipfile.ZipFile(plus) as z:
        meta=json.loads(z.read(next(n for n in z.namelist() if n.endswith('/metadata/icon-families.json'))))
    aliases={a:n for n,d in meta.items() for a in d.get('aliases',{}).get('names',[])}
    icons={};packs=[];unknown=[]
    for path in paths:
        pack='pro-plus' if 'pro-plus-' in path.name else 'pro' if '-pro-' in path.name else 'free'
        with zipfile.ZipFile(path) as z:
            names=z.namelist(); prefix=next(n for n in names if n.endswith('/LICENSE.txt')).rsplit('/',1)[0]
            license_bytes=z.read(prefix+'/LICENSE.txt')
            (ASSETS/'licenses').mkdir(exist_ok=True)
            (ASSETS/'licenses'/f'{pack}-LICENSE.txt').write_bytes(license_bytes)
            fonts=[n for n in names if '/otfs/' in n and n.endswith('.otf')]
            full=[n for n in names if '/svgs-full/' in n and n.endswith('.svg')]
            for member in full:
                folder,name=member.split('/svgs-full/')[1].split('/')
                name=name[:-4];canonical=aliases.get(name,name);info=meta.get(canonical,meta.get(name,{}))
                if folder in ('solid','regular','light','thin','brands'):family,style='classic',folder
                elif folder=='duotone':family,style='duotone','solid'
                else:family,style=folder.rsplit('-',1)
                if not info or style not in info.get('svgs',{}).get(family,{}):
                    unknown.append((name,family,style));continue
                record=icons.setdefault(name,{'name':name,'canonical':canonical,'label':info.get('label',name),'terms':info.get('search',{}).get('terms',[]),'variants':{}})
                key=family+'/'+style
                record['variants'].setdefault(key,{'family':family,'style':style,'providers':{}})['providers'][pack]=member
            packs.append({'id':pack,'archive':'packs/'+path.name,'bytes':path.stat().st_size,'sha256':digest(path),'license':'licenses/'+pack+'-LICENSE.txt','full_svg_count':len(full),'otf_count':len(fonts),'fonts':fonts})
    if unknown:raise SystemExit('Unmapped metadata: '+repr(unknown[:20]))
    for record in icons.values():record['variants']=list(record['variants'].values())
    data={'schema':1,'icons':sorted(icons.values(),key=lambda d:d['name'])}
    with gzip.open(ASSETS/'index.json.gz','wt',encoding='utf8') as f:json.dump(data,f,separators=(',',':'))
    manifest={'schema':1,'version':'7.3.1','archive_bytes':sum(p['bytes'] for p in packs),'packs':packs,'indexed_names':len(icons),'indexed_variants':sum(len(v['variants']) for v in icons.values())}
    (ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='packs'},indent=2))
if __name__=='__main__':main()

