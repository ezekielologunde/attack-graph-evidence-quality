"""Integrated, exact structural-exposure development model. No network actions."""
import hashlib
import json
import math
from pathlib import Path
import shared_paths as graph_model


def posterior(prior, n, reports, grouped=True, age=True):
    if len(prior) != 2**n or any(not math.isfinite(p) or p < 0 for p in prior) or abs(sum(prior)-1)>1e-9:
        raise ValueError('Invalid prior')
    groups = {}
    for i, r in enumerate(reports):
        if r['gate'] not in range(n) or r['value'] not in (0, 1):
            raise ValueError('Invalid observation')
        if any(not math.isfinite(r[k]) or not 0 <= r[k] <= 1 for k in ('accuracy', 'flip')):
            raise ValueError('Invalid observation parameters')
        key = (r['gate'], r['source']) if grouped else i
        groups.setdefault(key, []).append(r)
    used, conflicts = [], 0
    for rows in groups.values():
        signatures = {(r['value'], r['accuracy'], r['flip']) for r in rows}
        if len(signatures) > 1:
            # Explicit conservative policy: discard all conflicting rows in this group.
            conflicts += 1
        else:
            used.append(rows[0])
    mass = []
    for state, p in zip(graph_model.states(n), prior):
        for r in used:
            q, f = r['accuracy'], r['flip'] if age else 0
            effective = q*(1-f)+(1-q)*f
            p *= effective if state[r['gate']] == r['value'] else 1-effective
        mass.append(p)
    total = sum(mass)
    if total <= 0:
        raise ValueError('Evidence has zero likelihood')
    return [p/total for p in mass], conflicts


def public_reports(reports):
    return [{k:r[k] for k in ('gate','value','source','accuracy','flip')} for r in reports]


def evaluate(graph, prior, reports, budget=1.5, cost=.25, query_accuracy=.9):
    evaluator_reports = [dict(gate=r['gate'], value=r['value'], source=r['true_source'],
                              accuracy=r['accuracy'], flip=r['true_flip']) for r in reports]
    truth, conflicts = posterior(prior, graph['n'], evaluator_reports)
    if conflicts:
        raise ValueError('True event records disagree')
    visible = public_reports(reports)
    rows = []
    for name, grouped, age, factorized in (
        ('naive', False, False, False),
        ('deduplicated', True, False, False),
        ('lineage_age', True, True, False),
        ('factorized_lineage_age', True, True, True),
    ):
        belief, dropped = posterior(prior, graph['n'], visible, grouped, age)
        if factorized:
            belief = graph_model.independent_marginals(belief, graph['n'])
        for query in (False, True):
            decision = graph_model.plan(graph, belief, budget, cost, query_accuracy, query)
            loss, spent = graph_model.score(graph, truth, decision, cost, query_accuracy)
            rows.append(dict(policy=name+('_voi' if query else '_immediate'),
                             expected_loss=loss, expected_spend=spent,
                             conflicting_groups_dropped=dropped, decision=decision))
    # Privileged correct observation model: a diagnostic, not an operational policy.
    for query in (False, True):
        decision = graph_model.plan(graph, truth, budget, cost, query_accuracy, query)
        loss, spent = graph_model.score(graph, truth, decision, cost, query_accuracy)
        rows.append(dict(policy='privileged'+('_voi' if query else '_immediate'),
                         expected_loss=loss, expected_spend=spent, decision=decision))
    oracle = sum(p*min(graph_model.reachable_loss(graph,s,a) for a in graph_model.patch_choices(graph['n'],budget))
                 for s,p in zip(graph_model.states(graph['n']),truth))
    for row in rows:
        row['oracle_regret'] = row['expected_loss']-oracle
        assert row['oracle_regret'] >= -1e-9 and row['expected_spend'] <= budget+1e-9
    return dict(oracle_loss=oracle, truth_weights=truth, policies=rows)


def observation_cases():
    base = dict(gate=2, value=1, source='a', true_source='a', accuracy=.8, flip=0., true_flip=0.)
    negative = dict(base, value=0, source='b', true_source='b')
    return {
        'single': [base],
        'copies_correct': [base.copy() for _ in range(4)],
        'copies_split': [dict(base, source=f'split{i}') for i in range(4)],
        'independent_conflict': [base, negative],
        'false_merge_conflict': [base, dict(negative, source='a')],
        'stale_correct': [dict(base, flip=.4, true_flip=.4)],
        'stale_underestimated': [dict(base, true_flip=.4)],
        'split_and_stale': [dict(base, source=f'split{i}', true_flip=.4) for i in range(4)],
    }


def main():
    root = Path(__file__).resolve().parents[1]
    fixture = root/'data/shared-paths-v0.2.json'
    spec = json.loads(fixture.read_text())
    cases = []
    for graph in spec['graphs']:
        for prior in spec['priors']:
            for name, reports in observation_cases().items():
                for cost in spec['verification_costs']:
                    cases.append(dict(graph=graph['name'], prior=prior['name'], evidence=name,
                                      query_cost=cost, **evaluate(graph,prior['weights'],reports,cost=cost)))
    dest = root/'analysis/integrated-v0.3'
    dest.mkdir(exist_ok=True)
    result = dest/'results.json'
    result.write_text(json.dumps(dict(held_out=False, type='exact synthetic development calculations', cases=cases),indent=2)+'\n',encoding='utf-8')
    files = [Path(__file__),root/'src/shared_paths.py',fixture,root/'tests/test_evidence_graph.py',result]
    manifest = {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'{len(cases)} integrated development cases')


if __name__ == '__main__':
    main()
