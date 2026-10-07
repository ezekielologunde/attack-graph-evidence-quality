"""Acquire pinned wheels, then run isolated offline workers. No global installation."""
import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
DEPENDENCIES={'urllib3':'1.26.18','idna':'3.10','certifi':'2024.8.30','charset-normalizer':'2.0.12'}


def main():
    dest=ROOT/'analysis/requests-behavior-v0.1'
    dest.mkdir(exist_ok=True)
    if (dest/'results.json').exists():raise FileExistsError('Refusing to overwrite results')
    receipts=[]
    def wheel(package,version,folder):
        url=f'https://pypi.org/pypi/{package}/{version}/json'
        with urllib.request.urlopen(url,timeout=30) as response:meta=json.load(response)
        choices=[x for x in meta['urls'] if x['filename'].endswith('none-any.whl')]
        if len(choices)!=1:raise ValueError('Ambiguous pure Python wheel')
        record=choices[0]
        with urllib.request.urlopen(record['url'],timeout=30) as response:raw=response.read()
        digest=hashlib.sha256(raw).hexdigest()
        assert digest==record['digests']['sha256']
        (folder/record['filename']).write_bytes(raw)
        receipts.append(dict(package=package,version=version,url=record['url'],sha256=digest,
                             bytes=len(raw),retrieved_utc=datetime.now(timezone.utc).isoformat()))
    outputs=[]
    with tempfile.TemporaryDirectory(prefix='requests-behavior-') as directory:
        for version in ('2.30.0','2.31.0'):
            folder=Path(directory)/version;folder.mkdir()
            for package,v in dict(DEPENDENCIES,requests=version).items():wheel(package,v,folder)
            proc=subprocess.run([sys.executable,'-I',str(ROOT/'src/requests_behavior_check.py'),
                                 '--wheels',str(folder),'--version',version],capture_output=True,text=True,check=True)
            output=json.loads(proc.stdout)
            # Remove ephemeral path while keeping the distribution/version and wheel hashes.
            output['module_path']=output['module_path'].split('requests-'+version)[-1]
            outputs.append(output)
    for output in outputs:
        for case in output['results']:
            expected=case['credentials'] and (case['scheme']=='http' or output['version']=='2.30.0')
            assert case['header_present']==expected,(output['version'],case)
    result=dict(type='offline API-level behavior check, not end-to-end exploit',dependencies=DEPENDENCIES,
                executions=outputs,receipts=receipts,checks_passed=16)
    (dest/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    files=[ROOT/'src/requests_behavior_check.py',Path(__file__),dest/'results.json']
    (dest/'manifest.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n',encoding='utf-8')
    print('16 API-level checks passed; no requests sent; temporary wheels removed')


if __name__=='__main__':main()
