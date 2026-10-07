"""Post hoc descriptive analysis of immutable v0.4 outputs; no model evaluation."""
import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'analysis/validation-v0.4'
DEST = ROOT / 'analysis/validation-v0.4-secondary'
TOL = 1e-9


def counts(values):
    return dict(n=len(values), lower=sum(x < -TOL for x in values),
                tie=sum(abs(x) <= TOL for x in values), higher=sum(x > TOL for x in values),
                minimum=min(values), median=statistics.median(values), maximum=max(values))


def main():
    for name, expected in json.loads((SOURCE / 'manifest.json').read_text()).items():
        assert hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == expected, name
    for name, expected in json.loads((ROOT / 'protocol/validation-v0.4-seal.json').read_text())['files'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    rows = [json.loads(line) for line in (SOURCE / 'cases.jsonl').read_text().splitlines()]
    assert len(rows) == 96 and all(r['status'] == 'ok' for r in rows)
    assert len({(r['graph'], r['prior'], r['evidence'], r['query_cost']) for r in rows}) == 96
    names = [p['policy'] for p in rows[0]['policies']]
    assert len(names) == len(set(names)) == 10
    for r in rows:
        assert {p['policy'] for p in r['policies']} == set(names)
        ps = {p['policy']: p for p in r['policies']}
        d = ps['lineage_age_voi']['expected_loss'] - ps['lineage_age_immediate']['expected_loss']
        assert abs(d - r['primary_difference']) <= TOL
        for p in ps.values():
            assert abs(p['oracle_regret'] - (p['expected_loss'] - r['oracle_loss'])) <= TOL
            assert p['oracle_regret'] >= -TOL and p['expected_spend'] <= 1.5 + TOL
    saved = json.loads((SOURCE / 'summary.json').read_text())
    for graph, summary in saved.items():
        c = counts([r['primary_difference'] for r in rows if r['graph'] == graph])
        assert (c['n'], c['lower'], c['tie'], c['higher']) == (summary['total'], summary['negative'], summary['zero'], summary['positive'])
        for key in ['minimum', 'median', 'maximum']:
            assert abs(c[key] - summary[key]) <= TOL
    aggregate = {}
    for name in names:
        ps = [next(p for p in r['policies'] if p['policy'] == name) for r in rows]
        aggregate[name] = dict(mean_loss=statistics.mean(p['expected_loss'] for p in ps),
            mean_spend=statistics.mean(p['expected_spend'] for p in ps),
            mean_oracle_regret=statistics.mean(p['oracle_regret'] for p in ps),
            query_count=sum('query' in p['decision'] for p in ps),
            conflict_case_count=sum(p.get('conflicting_groups_dropped', 0) > 0 for p in ps))
    paired = []
    for r in rows:
        ps = {p['policy']: p for p in r['policies']}
        for base in ['naive', 'deduplicated', 'lineage_age', 'factorized_lineage_age', 'privileged']:
            d = ps[base + '_voi']['expected_loss'] - ps[base + '_immediate']['expected_loss']
            paired.append(dict(**{k:r[k] for k in ['graph', 'prior', 'evidence', 'query_cost']},
                               policy_family=base, difference=d,
                               queried='query' in ps[base+'_voi']['decision']))
    groups = {key: {str(v):counts([r['primary_difference'] for r in rows if r[key] == v])
                   for v in sorted({r[key] for r in rows})}
              for key in ['graph', 'prior', 'evidence', 'query_cost']}
    result = dict(status='post hoc descriptive analysis; no new experimental cases',
                  aggregate=aggregate, primary_subgroups=groups, paired=paired,
                  harmful_verification=[r for r in paired if r['difference'] > TOL])
    DEST.mkdir(exist_ok=True)
    (DEST / 'analysis.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    table = ['| Policy | Mean loss | Mean spend | Mean oracle regret | Query cases | Conflict cases |',
             '|---|---:|---:|---:|---:|---:|']
    for name, a in aggregate.items():
        table.append(f"| {name} | {a['mean_loss']:.6f} | {a['mean_spend']:.6f} | {a['mean_oracle_regret']:.6f} | {a['query_count']} | {a['conflict_case_count']} |")
    (DEST / 'policy-table.md').write_text('\n'.join(table)+'\n', encoding='utf-8')
    files = [Path(__file__), SOURCE/'cases.jsonl', SOURCE/'manifest.json', DEST/'analysis.json', DEST/'policy-table.md']
    (DEST / 'manifest.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}, indent=2)+'\n', encoding='utf-8')
    print('Verified original manifests, 96 cases, 960 policy rows, primary summaries, regrets and budgets.')
    print('\n'.join(table))


if __name__ == '__main__':
    main()
