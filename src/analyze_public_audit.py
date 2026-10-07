"""Offline comparison of sealed feasibility snapshots."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIRECTORY=ROOT/'data/public-artifact-audit-v0.1'


def main():
    audit=json.loads((DIRECTORY/'audit.json').read_text())
    for receipt in audit['receipts']:
        if 'saved_as' in receipt:
            assert hashlib.sha256((DIRECTORY/receipt['saved_as']).read_bytes()).hexdigest()==receipt['sha256']
    github=json.loads((DIRECTORY/'github-advisory.json').read_text())
    osv=json.loads((DIRECTORY/'osv-advisory.json').read_text())
    normalize=lambda d:[dict(name=a['package']['name'],ecosystem=a['package']['ecosystem'],ranges=a['ranges']) for a in d['affected']]
    output=dict(same_advisory_id=github['id']==osv['id'],
                normalized_package_ranges_equal=normalize(github)==normalize(osv),
                osv_added_aliases=sorted(set(osv['aliases'])-set(github['aliases'])),
                github_package=github['affected'][0]['package'],osv_package=osv['affected'][0]['package'],
                interpretation='OSV explicitly identifies GitHub as upstream; range agreement is not independent corroboration.',
                independent_fact='Wheel METADATA confirms package name and version; no independent affectedness label was measured.')
    dest=ROOT/'analysis/public-artifact-audit-v0.1'
    dest.mkdir(exist_ok=True)
    (dest/'comparison.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
