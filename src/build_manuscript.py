"""Compile the standalone paper using a pre-acquired, verified portable compiler."""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IMAGE='python@sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--build-dir',type=Path,required=True)
    args=parser.parse_args();base=args.build_dir.resolve()
    assert (base/'tectonic').is_file() and (base/'compiler-receipt.json').is_file()
    (base/'output').mkdir(exist_ok=True)
    # The cache was populated separately from the official Tectonic bundle.
    # This final build is offline and does not install a local TeX distribution.
    command=['docker','run','--rm','--name','attack-graph-paper-final','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--cpus','2','--memory','2g','--pids-limit','64','--tmpfs','/tmp:rw,exec,size=536870912','--env','HOME=/tmp','--env','XDG_CACHE_HOME=/build/cache','--mount',f'type=bind,source={base},target=/build','--mount',f'type=bind,source={ROOT / "paper"},target=/input,readonly',IMAGE,'sh','-c','cp /build/tectonic /tmp/tectonic && chmod +x /tmp/tectonic && /tmp/tectonic --keep-logs --outdir /build/output /input/main.tex']
    source_hash=hashlib.sha256((ROOT/'paper/main.tex').read_bytes()).hexdigest()
    try:
        p=subprocess.run(command,capture_output=True,encoding='utf-8',errors='replace',timeout=180)
    except subprocess.TimeoutExpired:
        subprocess.run(['docker','rm','-f','attack-graph-paper-final'],capture_output=True)
        raise
    out=ROOT/'paper/build';out.mkdir(exist_ok=True)
    (out/'stdout.txt').write_text(p.stdout,encoding='utf-8')
    (out/'stderr.txt').write_text(p.stderr,encoding='utf-8')
    receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=command,exit_code=p.returncode,source_sha256=source_hash,compiler=json.loads((base/'compiler-receipt.json').read_text()),compiler_binary_sha256=hashlib.sha256((base/'tectonic').read_bytes()).hexdigest(),native_compiler_status='Unavailable: Unable to find standard directories for platform',network='none')
    if p.returncode==0:
        assert source_hash==hashlib.sha256((ROOT/'paper/main.tex').read_bytes()).hexdigest()
        pdf=(base/'output/main.pdf').read_bytes()
        (ROOT/'paper/main.pdf').write_bytes(pdf)
        receipt['pdf_sha256']=hashlib.sha256(pdf).hexdigest()
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2));raise SystemExit(p.returncode)

if __name__=='__main__':main()
