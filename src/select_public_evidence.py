"""Acquire or replay the official snapshot and apply v0.5 screening. No package execution."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://storage.googleapis.com/osv-vulnerabilities/PyPI/all.zip'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--archive', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    for name, expected in json.loads((ROOT/'protocol/public-evidence-v0.5-seal.json').read_text())['files'].items():
        assert sha(ROOT/name) == expected, 'Protocol hash mismatch'
    archive = Path(args.archive).resolve()
    assert ROOT not in archive.parents, 'Archive must remain outside repository'
    dest = Path(args.output)
    assert not dest.exists(), 'Output already exists; preserve prior results'
    meta = archive.with_suffix('.acquisition.json')
    if not archive.exists():
        archive.parent.mkdir(parents=True, exist_ok=True)
        start = datetime.now(timezone.utc).isoformat()
        temporary = archive.with_suffix('.partial')
        with urllib.request.urlopen(URL, timeout=120) as response, temporary.open('xb') as out:
            headers = dict(response.headers)
            while True:
                block = response.read(1048576)
                if not block:
                    break
                out.write(block)
        temporary.rename(archive)
        meta.write_text(json.dumps(dict(url=URL, started_utc=start,
            finished_utc=datetime.now(timezone.utc).isoformat(), headers=headers,
            bytes=archive.stat().st_size, sha256=sha(archive)), indent=2)+'\n', encoding='utf-8')
    acquisition = json.loads(meta.read_text())
    assert sha(archive) == acquisition['sha256']
    ledger, eligible = [], {}
    with zipfile.ZipFile(archive) as z:
        for member in sorted(z.namelist()):
            if member.endswith('/'):
                continue
            row = dict(member=member)
            try:
                raw = z.read(member)
                obj = json.loads(raw)
                ident = obj.get('id')
                row.update(id=ident, record_sha256=hashlib.sha256(raw).hexdigest())
                if not isinstance(ident, str):
                    raise ValueError('Missing or invalid id')
                reasons = []
                if not ident.startswith('GHSA-'):
                    reasons.append('not_GHSA')
                if obj.get('withdrawn'):
                    reasons.append('withdrawn')
                if ident == 'GHSA-j8r2-6x86-q33q':
                    reasons.append('development_advisory')
                published = datetime.fromisoformat(obj['published'].replace('Z', '+00:00'))
                if published.tzinfo is None:
                    raise ValueError('Published timestamp lacks timezone')
                if not datetime(2023,1,1,tzinfo=timezone.utc) <= published < datetime(2026,1,1,tzinfo=timezone.utc):
                    reasons.append('outside_publication_window')
                candidates = []
                for affected in obj.get('affected', []):
                    package = affected.get('package', {})
                    if package.get('ecosystem') != 'PyPI':
                        continue
                    name = package.get('name')
                    if not isinstance(name, str) or not name.strip():
                        raise ValueError('Missing PyPI package name')
                    fixed = sorted({e['fixed'] for r in affected.get('ranges', []) for e in r.get('events', [])
                                    if isinstance(e.get('fixed'), str) and e['fixed']})
                    if fixed:
                        candidates.append((re.sub(r'[-_.]+', '-', name).lower(), name, fixed))
                if not candidates:
                    reasons.append('no_PyPI_package_with_fixed_event')
                row['reasons'] = reasons
                row['status'] = 'excluded' if reasons else 'eligible'
                row['eligible_pairs'] = []
                if not reasons:
                    for normalized, name, fixed in candidates:
                        key = (ident, normalized)
                        row['eligible_pairs'].append(list(key))
                        if key not in eligible:
                            eligible[key] = dict(id=ident, package=normalized, original_package_name=name,
                                aliases=obj.get('aliases', []), published=obj['published'],
                                members=[], fixed_versions=[])
                        pair = eligible[key]
                        pair['members'].append(dict(member=member, sha256=row['record_sha256']))
                        pair['fixed_versions'] = sorted(set(pair['fixed_versions']) | set(fixed))
            except Exception as error:
                row.update(status='screening_failure', error=str(error))
            ledger.append(row)
    selected = [eligible[k] for k in sorted(eligible)[:20]]
    # Connected components by shared IDs/aliases; linkage does not prove independent discovery.
    clusters = []
    for pair in selected:
        tokens = set([pair['id']] + pair['aliases'])
        matches = [c for c in clusters if c['tokens'] & tokens]
        merged = dict(tokens=tokens, pairs=[(pair['id'], pair['package'])])
        for c in matches:
            merged['tokens'] |= c['tokens']; merged['pairs'] += c['pairs']; clusters.remove(c)
        clusters.append(merged)
    for index, c in enumerate(clusters, 1):
        for pair in selected:
            if (pair['id'], pair['package']) in c['pairs']:
                pair['alias_cluster'] = index
    for index, pair in enumerate(selected, 1):
        pair.update(selection_rank=index, behavioral_feasibility_candidate=index <= 6)
    dest.mkdir(parents=True)
    (dest/'screening-ledger.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in ledger), encoding='utf-8')
    summary = dict(record_status_counts=dict(Counter(r['status'] for r in ledger)),
        exclusion_reason_counts=dict(Counter(reason for r in ledger for reason in r.get('reasons', []))),
        eligible_unique_pairs=len(eligible), selected_pairs=len(selected), selected_alias_clusters=len(clusters))
    manifest = dict(status='selection frozen before new scanner or behavior runs', acquisition=acquisition,
        selection_code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        selection_code_sha256=sha(Path(__file__)), protocol_sha256=sha(ROOT/'protocol/public-evidence-v0.5.md'),
        summary=summary, selected=selected)
    (dest/'selection.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (dest/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in dest.iterdir() if p.is_file()},indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    for pair in selected:
        print(pair['selection_rank'],pair['id'],pair['package'])


if __name__ == '__main__':
    main()
