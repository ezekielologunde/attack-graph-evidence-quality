import json,urllib.request,hashlib,datetime,zipfile
from pathlib import Path
pairs={'langroid':['0.53.14','0.53.15'],'pretalx':['2.3.1','2.3.2'],'scrapy':['2.11.1','2.11.2'],'wordops':['3.20.0','3.21.0'],'certifi':['2024.6.2','2024.7.4']}
cache=Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5\packages');cache.mkdir(exist_ok=True)
rows=[]
for package,versions in pairs.items():
 for version in versions:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();url=f'https://pypi.org/pypi/{package}/{version}/json'
  try:
   with urllib.request.urlopen(url,timeout=40) as r: raw=r.read()
   meta=json.loads(raw); (cache/f'{package}-{version}.json').write_bytes(raw)
   wheels=sorted([f for f in meta['urls'] if f['packagetype']=='bdist_wheel' and f['filename'].endswith('none-any.whl')],key=lambda f:f['filename'])
   if not wheels: raise ValueError('No universal wheel: source-build environment must be specified separately')
   artifact=wheels[0]; dest=cache/artifact['filename']
   if not dest.exists():
    with urllib.request.urlopen(artifact['url'],timeout=60) as r: dest.write_bytes(r.read())
   digest=hashlib.sha256(dest.read_bytes()).hexdigest();assert digest==artifact['digests']['sha256']
   with zipfile.ZipFile(dest) as z:
    metadata=z.read(next(n for n in z.namelist() if n.endswith('.dist-info/METADATA'))).decode()
    deps=[s[15:] for s in metadata.splitlines() if s.startswith('Requires-Dist: ')]
    licenses=[n for n in z.namelist() if any(x in n.upper() for x in ['LICENSE','COPYING'])]
   rows.append(dict(package=package,version=version,status='wheel_hash_verified',filename=dest.name,sha256=digest,url=artifact['url'],metadata_url=url,metadata_sha256=hashlib.sha256(raw).hexdigest(),requires_dist=deps,license_members=licenses,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
  except Exception as e:rows.append(dict(package=package,version=version,status='blocked',error=str(e),metadata_url=url,started_utc=start))
p=Path('protocol/public-evidence-v0.5-artifacts.json');p.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
for r in rows:print(r['package'],r['version'],r['status'],r.get('error',''),len(r.get('requires_dist',[])))
