import json,urllib.request,zipfile,hashlib,datetime,concurrent.futures,re
from pathlib import Path
root=Path.cwd(); outside=Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5\source-audit');outside.mkdir(exist_ok=False)
sel=json.loads((root/'analysis/public-evidence-v0.5-selection/selection.json').read_text()); archive=outside.parent/'pypi-all.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest()==sel['acquisition']['sha256']
def fetch(url,path):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'research-provenance-audit'}),timeout=40) as r: data=r.read();headers=dict(r.headers)
  path.write_bytes(data)
  return {'url':url,'retrieved_utc':start,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'headers':headers,'status':'ok'},data
 except Exception as e:return {'url':url,'retrieved_utc':start,'status':'failed','error':str(e)},None
meta,b=fetch('https://api.github.com/repos/github/advisory-database/commits/main',outside/'revision.json');assert b,meta
rev=json.loads(b)['sha']; license_meta,lic=fetch(f'https://raw.githubusercontent.com/github/advisory-database/{rev}/LICENSE.md',outside/'LICENSE.md')
z=zipfile.ZipFile(archive); inputs=[(p,json.loads(z.read(p['members'][0]['member']))) for p in sel['selected']]
def process(item):
 p,o=item; a=[a for a in o['affected'] if a['package']['ecosystem']=='PyPI' and re.sub('[-_.]+','-',a['package']['name']).lower()==p['package']]
 sources=sorted({a.get('database_specific',{}).get('source','') for a in a if a.get('database_specific',{}).get('source')})
 row={'rank':p['selection_rank'],'id':p['id'],'package':p['package'],'aliases':p['aliases'],'sources':sources,'source_revision':rev,'retrievals':[],'relationship':'unresolved','range_comparison':'unknown','summary':o.get('summary'),'references':o.get('references',[])}
 for i,url in enumerate(sources):
  prefix='https://github.com/github/advisory-database/blob/main/'
  if not url.startswith(prefix):continue
  raw=f'https://raw.githubusercontent.com/github/advisory-database/{rev}/'+url[len(prefix):]
  m,data=fetch(raw,outside/(p['id']+f'-{i}.json'));row['retrievals'].append(m)
  if data:
   g=json.loads(data);row['relationship']='explicit source attribution to GitHub advisory database; retrieved same advisory ID' if g.get('id')==p['id'] else 'source identity mismatch'
   def ranges(obj):return sorted([x.get('ranges',[]) for x in obj.get('affected',[]) if x.get('package',{}).get('ecosystem')=='PyPI' and re.sub('[-_.]+','-',x['package']['name']).lower()==p['package']],key=lambda x:json.dumps(x,sort_keys=True))
   row['range_comparison']='matching structured ranges' if ranges(o)==ranges(g) else 'different structured ranges; semantic review required'
   row['source_modified']=g.get('modified');row['snapshot_modified']=o.get('modified');row['temporal_mismatch']=g.get('modified')!=o.get('modified')
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(process,inputs))
out=root/'analysis/public-evidence-v0.5-provenance';out.mkdir(exist_ok=False)
result={'revision_acquisition':meta,'source_revision':rev,'license_acquisition':license_meta,'scope':'Documentary source audit, not independent affectedness validation','rows':rows}
(out/'audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('license',license_meta['status'],'revision',rev)
for r in rows: print(r['rank'],r['package'],r['relationship'],r['range_comparison'],r.get('temporal_mismatch'))
