"""Exact development model for gated graph reachability. No network actions."""
import hashlib
import itertools
import json
from pathlib import Path


def states(n):
    return list(itertools.product((0, 1), repeat=n))


def reachable_loss(graph, state, patches):
    reached = {graph['entry']}
    while True:
        expanded = reached | {
            v for u, v, gate in graph['edges']
            if u in reached and (gate is None or (state[gate] and gate not in patches))
        }
        if expanded == reached:
            return sum(weight for target, weight in graph['targets'].items() if target in reached)
        reached = expanded


def patch_choices(n, budget):
    return [a for count in range(n + 1) if count <= budget + 1e-9
            for a in itertools.combinations(range(n), count)]


def risk(graph, belief, patches):
    return sum(p * reachable_loss(graph, s, patches)
               for s, p in zip(states(graph['n']), belief))


def best(graph, belief, budget):
    return min(patch_choices(graph['n'], budget),
               key=lambda a: (risk(graph, belief, a), len(a), a))


def query_branches(belief, n, gate, accuracy):
    for value in (0, 1):
        mass = [p * (accuracy if s[gate] == value else 1 - accuracy)
                for s, p in zip(states(n), belief)]
        probability = sum(mass)
        yield value, probability, [p / probability for p in mass] if probability else belief[:]


def independent_marginals(belief, n):
    marginals = [sum(p * s[i] for s, p in zip(states(n), belief)) for i in range(n)]
    result = []
    for s in states(n):
        p = 1.0
        for i, value in enumerate(s):
            p *= marginals[i] if value else 1 - marginals[i]
        result.append(p)
    return result


def plan(graph, belief, budget, cost, accuracy, allow_query):
    """Only policy-visible belief and graph enter action selection."""
    action = best(graph, belief, budget)
    options = [(risk(graph, belief, action), -1, {'patches': action})]
    if allow_query and cost <= budget:
        for gate in range(graph['n']):
            actions = {}
            expected = 0.0
            for value, probability, updated in query_branches(belief, graph['n'], gate, accuracy):
                actions[value] = best(graph, updated, budget - cost)
                expected += probability * risk(graph, updated, actions[value])
            options.append((expected, gate, {'query': gate, 'patches_after': actions}))
    return min(options, key=lambda row: (row[0], row[1]))[2]


def score(graph, truth, decision, cost, accuracy):
    if 'query' not in decision:
        return risk(graph, truth, decision['patches']), len(decision['patches'])
    expected = spent = 0.0
    for value, probability, updated in query_branches(truth, graph['n'], decision['query'], accuracy):
        action = decision['patches_after'][value]
        expected += probability * risk(graph, updated, action)
        spent += probability * (cost + len(action))
    return expected, spent


def evaluate(graph, truth, budget, cost, accuracy):
    n = graph['n']
    if len(truth) != 2 ** n or any(p < 0 for p in truth) or abs(sum(truth) - 1) > 1e-9:
        raise ValueError('Invalid joint distribution')
    if budget < 0 or cost < 0 or not 0 <= accuracy <= 1:
        raise ValueError('Invalid budget, cost or accuracy')
    oracle = sum(p * min(reachable_loss(graph, s, a) for a in patch_choices(n, budget))
                 for s, p in zip(states(n), truth))
    rows = []
    for name, belief, query in (
        ('joint_immediate', truth, False),
        ('factorized_immediate', independent_marginals(truth, n), False),
        ('joint_voi', truth, True),
        ('factorized_voi', independent_marginals(truth, n), True),
    ):
        decision = plan(graph, belief, budget, cost, accuracy, query)
        expected, spent = score(graph, truth, decision, cost, accuracy)
        if expected < oracle - 1e-9 or spent > budget + 1e-9:
            raise AssertionError('Oracle or budget invariant failed')
        rows.append(dict(policy=name, expected_loss=expected, expected_spend=spent,
                         oracle_regret=expected - oracle, decision=decision))
    return dict(oracle_loss=oracle, policies=rows)


def main():
    root = Path(__file__).resolve().parents[1]
    fixture = root / 'data/shared-paths-v0.2.json'
    specification = json.loads(fixture.read_text())
    cases = []
    for graph in specification['graphs']:
        for prior in specification['priors']:
            for cost in specification['verification_costs']:
                result = evaluate(graph, prior['weights'], specification['budget'], cost,
                                  specification['verification_accuracy'])
                cases.append(dict(graph=graph['name'], prior=prior['name'], verify_cost=cost, **result))
    output = dict(kind='exact synthetic development calculations', held_out=False, cases=cases)
    destination = root / 'analysis/shared-paths-v0.2'
    destination.mkdir(exist_ok=True)
    result_file = destination / 'results.json'
    result_file.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    inputs = [fixture, Path(__file__), root / 'tests/test_shared_paths.py', result_file]
    manifest = {str(p.relative_to(root)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in inputs}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} development cases written to {destination}')


if __name__ == '__main__':
    main()
