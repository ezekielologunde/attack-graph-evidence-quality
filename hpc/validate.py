"""Execute the sealed finite validation grid; never modify frozen model inputs."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT), *a], text=True).strip()
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('Tracked checkout is dirty')
    seal = json.loads((ROOT / 'protocol/validation-v0.4-seal.json').read_text())
    for name, expected in seal['files'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Frozen input mismatch: ' + name)
    spec = json.loads((ROOT / 'protocol/validation-v0.4.json').read_text())
    import evidence_graph as model
    observations = model.observation_cases()
    assert len(spec['graphs']) * len(spec['priors']) * len(observations) * len(spec['query_costs']) == 96
    assert spec['expected_case_count'] == 96
    assert [p['name'] for p in spec['priors']] == ['independent_half', 'shared_cause_mixture']
    assert all(g['n'] == 4 for g in spec['graphs'])
    if args.check_only:
        print('Seal verified; 96-case grid validated; no evaluations executed')
        return
    dest = Path(args.output).resolve()
    if dest == ROOT or ROOT in dest.parents:
        raise ValueError('Output must be outside checkout')
    dest.mkdir(parents=True, exist_ok=False)
    run = dict(commit=git('rev-parse', 'HEAD'), python=sys.version,
               platform=platform.platform(), job_id=os.environ.get('PBS_JOBID'),
               started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               sealed_hashes=seal['files'], kind='exact finite synthetic validation; no population inference')
    cases = []
    for graph in spec['graphs']:
        for prior in spec['priors']:
            weights = [1 / 16] * 16
            if prior['name'] == 'shared_cause_mixture':
                weights = [p * .5 for p in weights]
                weights[0] += .25
                weights[-1] += .25
            for evidence, reports in observations.items():
                for cost in spec['query_costs']:
                    row = dict(graph=graph['name'], prior=prior['name'], evidence=evidence, query_cost=cost)
                    try:
                        row.update(model.evaluate(graph, weights, reports, budget=spec['budget'],
                                                  cost=cost, query_accuracy=spec['query_accuracy']))
                        assert len(row['policies']) == 10
                        policies = {p['policy']: p for p in row['policies']}
                        row['primary_difference'] = policies['lineage_age_voi']['expected_loss'] - policies['lineage_age_immediate']['expected_loss']
                        row['status'] = 'ok'
                    except Exception:
                        row.update(status='failed', error=traceback.format_exc())
                    cases.append(row)
                    with (dest / 'cases.jsonl').open('a', encoding='utf-8') as stream:
                        stream.write(json.dumps(row) + '\n')
    failed = sum(c['status'] != 'ok' for c in cases)
    summary = {}
    for graph in spec['graphs']:
        rows = [c for c in cases if c['graph'] == graph['name']]
        differences = [c['primary_difference'] for c in rows if c['status'] == 'ok']
        summary[graph['name']] = dict(total=len(rows), failed=sum(c['status'] != 'ok' for c in rows),
            minimum=min(differences) if differences else None,
            median=statistics.median(differences) if differences else None,
            maximum=max(differences) if differences else None,
            negative=sum(d < -1e-9 for d in differences),
            zero=sum(abs(d) <= 1e-9 for d in differences), positive=sum(d > 1e-9 for d in differences))
    run.update(case_count=len(cases), failed=failed, exit_code=int(bool(failed)),
               finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    for name, data in [('run.json', run), ('summary.json', summary)]:
        (dest / name).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file()}
    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(output=str(dest), run=run, summary=summary), indent=2))
    sys.exit(run['exit_code'])


if __name__ == '__main__':
    main()
