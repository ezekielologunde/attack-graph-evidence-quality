"""Read-only public-data feasibility audit. Downloads wheels into memory, never installs them."""
import argparse
import email
import hashlib
import io
import json
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ADVISORY='GHSA-j8r2-6x86-q33q'
REPO_PATH=f'advisories/github-reviewed/2023/05/{ADVISORY}/{ADVISORY}.json'


def fetch(url):
    start=time.perf_counter()
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'research-feasibility-audit'}),timeout=30) as response:
        data=response.read()
    return data,dict(url=url, retrieved_utc=datetime.now(timezone.utc).isoformat(),
                     sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                     retrieval_seconds=time.perf_counter()-start)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,help='New output directory; refuses overwrite')
    args=parser.parse_args()
    destination=Path(args.output)
    destination.mkdir(parents=True,exist_ok=False)
    receipts=[]
    def download(url, filename=None):
        raw,receipt=fetch(url);receipts.append(receipt)
        if filename:
            (destination/filename).write_bytes(raw)
            receipt['saved_as']=filename
        return raw
    # Pin upstream GitHub source before fetching the advisory and its license.
    commit=json.loads(download('https://api.github.com/repos/github/advisory-database/commits/main'))['sha']
    prefix=f'https://raw.githubusercontent.com/github/advisory-database/{commit}/'
    gh=json.loads(download(prefix+REPO_PATH,'github-advisory.json'))
    download(prefix+'LICENSE.md','UPSTREAM-LICENSE.md')
    osv=json.loads(download(f'https://api.osv.dev/v1/vulns/{ADVISORY}','osv-advisory.json'))
    source=osv['affected'][0]['database_specific']['source']
    if not source.endswith(REPO_PATH):raise ValueError('Expected upstream lineage not present')
    projection=lambda d: (d['id'], sorted(d.get('aliases',[])),
                          [(a['package'],a['ranges']) for a in d['affected']])
    same=projection(gh)==projection(osv)
    artifacts=[]
    for version in ('2.30.0','2.31.0'):
        pypi=json.loads(download(f'https://pypi.org/pypi/requests/{version}/json'))
        wheels=[f for f in pypi['urls'] if f['filename'].endswith('py3-none-any.whl')]
        if len(wheels)!=1:raise ValueError('Ambiguous wheel')
        wheel=wheels[0];raw=download(wheel['url'])
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=wheel['digests']['sha256']:raise ValueError('PyPI digest mismatch')
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries=[n for n in archive.namelist() if n.endswith('.dist-info/METADATA')]
            if len(entries)!=1:raise ValueError('Ambiguous metadata')
            metadata=email.message_from_bytes(archive.read(entries[0]))
            if metadata['Name'].lower()!='requests' or metadata['Version']!=version:
                raise ValueError('Artifact identity mismatch')
        artifacts.append(dict(name=metadata['Name'],version=metadata['Version'],filename=wheel['filename'],
                              wheel_sha256=digest,metadata_entry=entries[0],
                              metadata_sha256=hashlib.sha256(archive_metadata(raw,entries[0])).hexdigest(),
                              listed_affected_by_osv=version in osv['affected'][0].get('versions',[])))
    report=dict(kind='two-artifact feasibility audit, not scanner benchmark',github_commit=commit,
                osv_declared_upstream=source,advisory_projection_equal=same,
                artifacts=artifacts,receipts=receipts,
                limitations=['Version identity is independent of advisory lookup; affectedness labels still come from the advisory.',
                             'No scanner execution, installed-environment inspection, exploitability test or patch-benefit measurement.',
                             'One retrieval per endpoint; wall time is acquisition latency, not verification-policy cost.',
                             'No wheels redistributed or package code executed. OSV record may change on rerun.'])
    (destination/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('github_commit','osv_declared_upstream','advisory_projection_equal','artifacts')},indent=2))


def archive_metadata(raw, entry):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        return archive.read(entry)


if __name__=='__main__':main()
