"""Run frozen, offline Langroid probe in fresh restricted containers."""
import datetime, hashlib, json, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5\locked-environments')
IMAGE = 'python@sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce'
tokenizer=json.loads((ROOT/'protocol/langroid-tokenizer.json').read_text())
assert hashlib.sha256((BASE.parent/'tokenizer-cache'/tokenizer['cache_filename']).read_bytes()).hexdigest()==tokenizer['sha256']
lock = json.loads((ROOT/'protocol/langroid-lock.json').read_text())
for path, digest in lock['code'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
out = ROOT/'analysis/public-evidence-v0.5-langroid-cached'
out.mkdir(exist_ok=False)
rows = []
for version in ('0.53.14', '0.53.15'):
    folder = BASE/('langroid-'+version)
    assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.whl')} == lock['wheels'][version]
    for repeat in (1,2,3):
        name = 'langroid-'+version+'-'+str(repeat)
        cmd = ['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--cpus','1','--memory','2g','--pids-limit','128','--user','65534:65534','--tmpfs','/tmp:rw,exec,size=2147483648','--env','TIKTOKEN_CACHE_DIR=/tokenizer','--mount',f'type=bind,source={BASE.parent / "tokenizer-cache"},target=/tokenizer,readonly','--env','HOME=/tmp','--env','PIP_NO_CACHE_DIR=1','--mount',f'type=bind,source={folder},target=/wheels,readonly','--mount',f'type=bind,source={ROOT / "src/probe_langroid.py"},target=/probe.py,readonly',IMAGE,'sh','-c',f'python -m venv /tmp/env && /tmp/env/bin/pip install --no-index --find-links /wheels langroid=={version} >&2 && /tmp/env/bin/pip check >&2 && /tmp/env/bin/pip freeze >&2 && /tmp/env/bin/python -B /probe.py']
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
