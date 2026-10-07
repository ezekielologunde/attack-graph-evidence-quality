"""Run frozen, offline Langroid probe in fresh restricted containers."""
import datetime, hashlib, json, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5\locked-environments')
IMAGE = 'python@sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b'
lock = json.loads((ROOT/'protocol/pretalx-lock.json').read_text())
for path, digest in lock['code'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
out = ROOT/'analysis/public-evidence-v0.5-pretalx'
out.mkdir(exist_ok=False)
rows = []
for version in ('2.3.1', '2.3.2'):
    folder = BASE/('pretalx-'+version)
    assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.whl')} == lock['wheels'][version]
    for repeat in (1,2,3):
        name = 'pretalx-'+version+'-'+str(repeat)
        cmd = ['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--cpus','1','--memory','2g','--pids-limit','128','--user','65534:65534','--tmpfs','/tmp:rw,exec,size=2147483648','--env','HOME=/tmp','--env','PIP_NO_CACHE_DIR=1','--mount',f'type=bind,source={folder},target=/wheels,readonly','--mount',f'type=bind,source={ROOT / "src/probe_pretalx.py"},target=/probe.py,readonly',IMAGE,'sh','-c',f'python -m venv /tmp/env && /tmp/env/bin/pip install --no-index --find-links /wheels pretalx=={version} >&2 && /tmp/env/bin/pip check >&2 && /tmp/env/bin/pip freeze >&2 && /tmp/env/bin/python -B /probe.py']
        start=time.monotonic()
        try:
            p=subprocess.run(cmd,capture_output=True,encoding='utf-8',errors='replace',timeout=180)
            stdout,stderr,code=p.stdout,p.stderr,p.returncode
        except subprocess.TimeoutExpired as e:
            subprocess.run(['docker','rm','-f',name],capture_output=True)
            stdout=(e.stdout or b'').decode('utf-8','replace');stderr=(e.stderr or b'').decode('utf-8','replace');code=124
        (out/(name+'.stdout.txt')).write_text(stdout,encoding='utf-8')
        (out/(name+'.stderr.txt')).write_text(stderr,encoding='utf-8')
        row=dict(version=version,repeat=repeat,exit_code=code,command=cmd,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start)
        if code == 0:
            try: row['observed']=json.loads(stdout)
            except ValueError: row['parse_error']=True
        rows.append(row)
        (out/'runs.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
        print(name,code,flush=True)
