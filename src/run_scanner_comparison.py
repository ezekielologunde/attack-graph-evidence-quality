"""Scan only two synthetic manifests in read-only mounts; preserve raw output."""
import hashlib,json,subprocess,tempfile,time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IMAGES={
 'osv':'ghcr.io/google/osv-scanner@sha256:afd838850ac1a0fcc15ff4a041dc9ba11123c3f0d2666217a5f0fcf9222b55fa',
 'trivy':'aquasec/trivy@sha256:af6acf9a6b85dfe389a1941505c0ce9efef52a4719635e1a962f022a3d855daa'}

def main():
 out=ROOT/'analysis/scanner-comparison-v0.1';out.mkdir(exist_ok=False)
 inputs=ROOT/'data/scanner-inputs-v0.1';inputs.mkdir(exist_ok=True)
 receipts=[]
 with tempfile.TemporaryDirectory(prefix='scanner-cache-') as cache:
  for name,image in IMAGES.items():
   p=subprocess.run(['docker','run','--rm',image,'--version'],capture_output=True)
   (out/f'{name}-version.txt').write_bytes(p.stdout+p.stderr)
   for version in ('2.30.0','2.31.0'):
    folder=inputs/version;folder.mkdir(exist_ok=True)
    (folder/'requirements.txt').write_text(f'requests=={version}\n',encoding='utf-8')
    command=['docker','run','--rm','--mount',f'type=bind,source={folder},target=/input,readonly']
    if name=='trivy':command+=['--mount',f'type=bind,source={cache},target=/root/.cache/trivy']
    command+=[image]
    command+=['scan','source','--no-resolve','--format','json','--all-packages','--lockfile','/input/requirements.txt'] if name=='osv' else ['fs','--scanners','vuln','--format','json','--skip-version-check','/input']
    started=datetime.now(timezone.utc).isoformat();start=time.perf_counter()
    p=subprocess.run(command,capture_output=True,timeout=300)
    stem=f'{name}-{version}'
    (out/f'{stem}.json').write_bytes(p.stdout)
    (out/f'{stem}.stderr.txt').write_bytes(p.stderr)
    receipts.append(dict(scanner=name,version=version,command=command,started_utc=started,
                         seconds=time.perf_counter()-start,exit_code=p.returncode))
    (out/'runs.json').write_text(json.dumps(receipts,indent=2)+'\n',encoding='utf-8')
    print(stem,p.returncode,flush=True)
  metadata=Path(cache)/'db/metadata.json'
  if metadata.exists():(out/'trivy-db-metadata.json').write_bytes(metadata.read_bytes())
  database=Path(cache)/'db/trivy.db'
  if database.exists():(out/'trivy-db-sha256.txt').write_text(hashlib.sha256(database.read_bytes()).hexdigest()+'\n')

if __name__=='__main__':main()
