import json,subprocess,hashlib,shutil,time,datetime
from pathlib import Path
ROOT=Path.cwd();BASE=Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5');OUT=ROOT/'analysis/public-evidence-v0.5-behavior-compatible';OUT.mkdir(exist_ok=False)
for f,h in json.load(open('protocol/public-evidence-v0.5.1-seal.json')).items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
cert=BASE/'environments/certifi-pair';cert.mkdir(exist_ok=True)
for p in (BASE/'packages').glob('certifi*.whl'):shutil.copy2(p,cert/p.name)
res=json.load(open('protocol/scrapy-compatible-lock.json'))['environments']; artifacts=json.load(open('protocol/public-evidence-v0.5-artifacts.json'));runs=[]
for case,version in [('scrapy','2.11.1'),('scrapy','2.11.2')]:
 folder=BASE/'environments-compatible'/f'{case}-{version}'
 if case=='scrapy':
  spec=next(r for r in res if r['package']==case and r['version']==version);image=spec['image'];hashes=spec['wheels']
 else:image='python@sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b';hashes={r['filename']:r['sha256'] for r in artifacts if r['package']=='certifi'}
 for n,h in hashes.items():assert hashlib.sha256((folder/n).read_bytes()).hexdigest()==h
 for repeat in range(1,4):
  name=f'research-{case}-{version.replace(".","-")}-{repeat}'
  command='python -B /probe.py certifi' if case=='certifi' else 'python -m venv /tmp/env && /tmp/env/bin/pip install --no-index --find-links /wheels scrapy=='+version+' >&2 && /tmp/env/bin/pip check >&2 && /tmp/env/bin/pip freeze >&2 && /tmp/env/bin/python -B /probe.py scrapy'
  cmd=['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--cpus','1','--memory','512m','--pids-limit','64','--user','65534:65534','--tmpfs','/tmp:rw,exec,size=268435456','--mount',f'type=bind,source={folder},target=/wheels,readonly','--mount',f'type=bind,source={ROOT / "src/public_behavior_probe.py"},target=/probe.py,readonly',image,'sh','-c',command]
  start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
  try:r=subprocess.run(cmd,capture_output=True,encoding='utf-8',timeout=30 if case=='certifi' else 120);code=r.returncode;stdout=r.stdout;stderr=r.stderr
  except subprocess.TimeoutExpired as e:
   subprocess.run(['docker','rm','-f',name],capture_output=True);code=124;stdout=str(e.stdout);stderr=str(e.stderr)
  prefix=f'{case}-{version}-{repeat}';(OUT/(prefix+'.stdout.txt')).write_text(stdout,encoding='utf-8');(OUT/(prefix+'.stderr.txt')).write_text(stderr,encoding='utf-8')
  row=dict(case=case,version=version,repeat=repeat,exit_code=code,utc=utc,elapsed_seconds=time.monotonic()-start,image=image,wheel_hashes=hashes,command=cmd)
  if code==0:row['observed']=json.loads(stdout)
  runs.append(row);(OUT/'runs.json').write_text(json.dumps(runs,indent=2)+'\n',encoding='utf-8');print(prefix,code,stdout[:180],flush=True)
