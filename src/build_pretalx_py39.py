"""Bounded isolated dependency preparation, separate from behavioral collection."""
import datetime, hashlib, json, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = Path(r'C:\Users\WT8\Documents\ChatGPT\Research\public-evidence-snapshots\v0.5')
IMAGE = 'python@sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b'
OUT = ROOT / 'analysis/public-evidence-v0.5-pretalx-py39'
OUT.mkdir(exist_ok=False)
rows = []
for package, versions in [('pretalx', ['2.3.1', '2.3.2'])]:
    for version in versions:
        name = package + '-' + version
        dest = BASE / 'py39-environments' / name
        dest.mkdir(parents=True, exist_ok=False)
        container = 'prepare-' + name.replace('.', '-')
        command = ['docker', 'run', '--rm', '--name', container, '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges', '--cpus', '2', '--memory', '3g', '--pids-limit', '128', '--tmpfs', '/tmp:rw,exec,size=2147483648', '--env', 'HOME=/tmp', '--env', 'PIP_NO_CACHE_DIR=1', '--mount', f'type=bind,source={dest},target=/wheels', IMAGE, 'python', '-m', 'pip', 'wheel', '--prefer-binary', '--wheel-dir', '/wheels', package + '==' + version]
        start = time.monotonic()
        try:
            p = subprocess.run(command, capture_output=True, encoding='utf-8', errors='replace', timeout=300)
            stdout, stderr, code = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired as e:
            subprocess.run(['docker', 'rm', '-f', container], capture_output=True)
            stdout = (e.stdout or b'').decode('utf-8', 'replace')
            stderr = (e.stderr or b'').decode('utf-8', 'replace')
            code = 124
        (OUT / (name + '.stdout.txt')).write_text(stdout, encoding='utf-8')
        (OUT / (name + '.stderr.txt')).write_text(stderr, encoding='utf-8')
        rows.append(dict(package=package, version=version, command=command, exit_code=code, elapsed_seconds=time.monotonic()-start, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), wheels={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.glob('*.whl')}))
        (OUT / 'resolution.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
        print(name, code, len(rows[-1]['wheels']), flush=True)
