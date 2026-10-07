import itertools
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import shared_paths as model


class SharedPathsTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((ROOT / 'data/shared-paths-v0.2.json').read_text())

    def test_graph_loss_against_boolean_formulas(self):
        # Independent hand-derived formulas, every state and every patch set.
        formulas = [lambda a,b,c: 10*a*b + 8*a*c,
                    lambda a,b,c: 10*int((a or b) and c),
                    lambda a,b,c: 10*int((a and b) or c) + 8*a*c]
        for graph, formula in zip(self.spec['graphs'], formulas):
            for state in model.states(3):
                for action in model.patch_choices(3, 3):
                    enabled = [value if i not in action else 0 for i,value in enumerate(state)]
                    self.assertEqual(model.reachable_loss(graph, state, action), formula(*enabled))

    def test_joint_query_updates_other_gate(self):
        belief = [.5,0,0,0,0,0,0,.5]
        _, probability, updated = list(model.query_branches(belief, 3, 0, 1))[1]
        self.assertEqual(probability, .5)
        self.assertEqual(updated[-1], 1)

    def test_factorization_preserves_marginals_not_joint(self):
        belief = [.5,0,0,0,0,0,0,.5]
        self.assertEqual(model.independent_marginals(belief, 3), [.125]*8)

    def test_common_cut_precludes_value_of_query(self):
        for graph in self.spec['graphs'][:2]:
            decision = model.plan(graph, [.125]*8, 1.5, .25, .9, True)
            self.assertNotIn('query', decision)
            self.assertEqual(model.risk(graph, [.125]*8, decision['patches']), 0)

    def test_every_case_budget_oracle_and_joint_voi(self):
        for graph, prior, cost in itertools.product(self.spec['graphs'], self.spec['priors'], [.25,.75]):
            result = model.evaluate(graph, prior['weights'], 1.5, cost, .9)
            rows = {r['policy']: r for r in result['policies']}
            self.assertLessEqual(rows['joint_voi']['expected_loss'], rows['joint_immediate']['expected_loss'] + 1e-9)
            for row in rows.values():
                decision = row['decision']
                actions = decision.get('patches_after', {0:decision.get('patches', [])})
                for action in actions.values():
                    self.assertLessEqual(len(action) + (cost if 'query' in decision else 0), 1.5)

    def test_invalid_distribution_rejected(self):
        with self.assertRaises(ValueError):
            model.evaluate(self.spec['graphs'][0], [1]*8, 1.5,.25,.9)

    def test_cycles_terminate_and_targets_count_once(self):
        graph = dict(n=1, entry='s', edges=[['s','a',0],['a','s',None],['s','a',0]], targets={'a':10})
        self.assertEqual(model.reachable_loss(graph, (1,), ()), 10)

    def test_zero_probability_query_branch(self):
        branches = list(model.query_branches([1,0,0,0,0,0,0,0], 3, 0, 1))
        self.assertEqual([b[1] for b in branches], [1,0])
