import subprocess,json,datetime,hashlib,time
from pathlib import Path
ROOT=Path.cwd(); BASE=Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5')
DEST=ROOT/'analysis/public-evidence-v0.5-environments';DEST.mkdir(exist_ok=True)
IMAGE='python@sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce'
rows=[]
for pkg,vs in [('langroid',['0.53.14','0.53.15']),('pretalx',['2.3.1','2.3.2']),('scrapy',['2.11.1','2.11.2']),('wordops',['3.20.0','3.21.0'])]:
 for v in vs:
  name=pkg+'-'+v;folder=BASE/'environments'/name;folder.mkdir(parents=True,exist_ok=True)
  cmd=['docker','run','--rm','--cpus','2','--memory','2g','--cap-drop','ALL','--security-opt','no-new-privileges','--mount',f'type=bind,source={folder},target=/wheels',IMAGE,'python','-m','pip','download','--only-binary=:all:','--dest','/wheels',pkg+'=='+v]
  start=time.monotonic()
  try:r=subprocess.run(cmd,capture_output=True,text=True,timeout=180);stdout,stderr,code=r.stdout,r.stderr,r.returncode
  except subprocess.TimeoutExpired as e:stdout=str(e.stdout);stderr=str(e.stderr);code=124
  (DEST/(name+'.stdout.txt')).write_text(stdout,encoding='utf-8');(DEST/(name+'.stderr.txt')).write_text(stderr,encoding='utf-8')
  row={'package':pkg,'version':v,'image':IMAGE,'command':cmd,'exit_code':code,'elapsed_seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wheels':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.whl')}}
  rows.append(row);print(name,code,len(row['wheels']),flush=True)
  (DEST/'resolution.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
