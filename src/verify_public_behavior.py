"""Verify saved offline observations without rerunning package code."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(directory):
    return json.loads((ROOT / 'analysis' / directory / 'runs.json').read_text())

def main():
    corrected = read('public-evidence-v0.5-behavior-compatible')
    assert len(corrected) == 6
    assert {(r['version'], r['repeat']) for r in corrected} == {
        (v, n) for v in ('2.11.1', '2.11.2') for n in (1, 2, 3)}
    for run in corrected:
        assert run['exit_code'] == 0
        assert run['observed']['version'] == run['version']
        obs = run['observed']['observations']
        assert len(obs) == 4
        assert {(x['kind'], x['target'].split(':')[0]) for x in obs} == {
            (k, s) for k in ('location', 'meta') for s in ('https', 'file')}
        for item in obs:
            expected = item['target'].startswith('https:') or run['version'] == '2.11.1'
            assert item['returned_request'] is expected
            assert item['result_url'] == (item['target'] if expected else 'https://example.invalid/start')
    original = read('public-evidence-v0.5-behavior')
    certifi = [r for r in original if r['case'] == 'certifi']
    assert len(certifi) == 3
    for run in certifi:
        assert run['exit_code'] == 0
        obs = run['observed']
        assert obs['empty_context_control'] and obs['common_non_target_control']
        assert [x['target_present'] for x in obs['observations']] == [True, False]
    failures = [r for r in original if r['case'] == 'scrapy'] + read('public-evidence-v0.5-behavior-retry')
    assert len(failures) == 12 and all(r['exit_code'] != 0 for r in failures)
    manifest = ROOT / 'analysis/public-evidence-v0.5-behavior/evidence-manifest.json'
    if manifest.exists():
        for name, digest in json.loads(manifest.read_text()).items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    print('Verified 6 Scrapy runs, 3 certifi runs, and 12 retained setup failures; available manifest hashes pass.')

if __name__ == '__main__':
    main()
