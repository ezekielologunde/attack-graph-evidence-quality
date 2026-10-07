"""Offline focal-CVE comparison. Does not treat alias records as independent findings."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/scanner-comparison-v0.1'
def main():
 rows=[]
 for version in ('2.30.0','2.31.0'):
  osv=json.loads((OUT/f'osv-{version}.json').read_text())
  packages=[p for r in osv['results'] for p in r['packages']]
  assert len(packages)==1 and packages[0]['package']['version']==version
  hits=[v for v in packages[0]['vulnerabilities'] if 'CVE-2023-32681' in v.get('aliases',[])]
  tri=json.loads((OUT/f'trivy-{version}.json').read_text())
  findings=[v for r in tri['Results'] for v in r.get('Vulnerabilities',[]) if v['VulnerabilityID']=='CVE-2023-32681']
  for v in findings:assert v['PkgName']=='requests' and v['InstalledVersion']==version
  rows.append(dict(version=version,osv_focal_present=bool(hits),trivy_focal_present=bool(findings),
                   osv_records=[dict(id=v['id'],sources=[a.get('database_specific',{}).get('source') for a in v['affected']]) for v in hits],
                   trivy_sources=[v.get('DataSource') for v in findings]))
 assert [(r['osv_focal_present'],r['trivy_focal_present']) for r in rows]==[(True,True),(False,False)]
 (OUT/'comparison.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(rows,indent=2))
 files=[p for p in OUT.iterdir() if p.is_file() and p.name!='manifest.json']
 files+=list((ROOT/'data/scanner-inputs-v0.1').glob('*/requirements.txt'))
 files+=[Path(__file__),ROOT/'src/run_scanner_comparison.py']
 (OUT/'manifest.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
