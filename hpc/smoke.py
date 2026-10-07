"""Portable smoke test only. Does not evaluate the prospective validation grid."""
import argparse,datetime,hashlib,json,os,platform,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
 if sys.version_info < (3,11):raise RuntimeError('Python 3.11+ required')
 git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a],text=True).strip()
 if git('status','--porcelain','--untracked-files=no'):raise RuntimeError('Tracked checkout is dirty')
 dest=Path(args.output).resolve()
 if dest==ROOT or ROOT in dest.parents:raise ValueError('Output must be outside checkout')
 seal=json.loads((ROOT/'protocol/validation-v0.4-seal.json').read_text())
 for file,expected in seal['files'].items():
  if hashlib.sha256((ROOT/file).read_bytes()).hexdigest()!=expected:raise RuntimeError('Frozen input mismatch: '+file)
 dest.mkdir(parents=True,exist_ok=False)
 result=dict(kind='portability smoke test, no new research results',commit=git('rev-parse','HEAD'),
             python=sys.version,platform=platform.platform(),job_id=os.environ.get('PBS_JOBID'),
             started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sealed_hashes=seal['files'])
 run=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests'],cwd=ROOT,capture_output=True)
 (dest/'tests.stdout.txt').write_bytes(run.stdout);(dest/'tests.stderr.txt').write_bytes(run.stderr)
 result['exit_code']=run.returncode
 (dest/'run.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 manifest={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in dest.iterdir() if f.is_file()}
 (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 print(str(dest));sys.exit(run.returncode)
if __name__=='__main__':main()
