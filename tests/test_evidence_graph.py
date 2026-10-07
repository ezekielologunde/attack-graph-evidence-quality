import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import evidence_graph as m


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.prior=[.125]*8
        self.cases=m.observation_cases()
        self.graph=json.loads((ROOT/'data/shared-paths-v0.2.json').read_text())['graphs'][2]

    def test_duplicate_invariance(self):
        single=m.posterior(self.prior,3,self.cases['single'])[0]
        self.assertEqual(single,m.posterior(self.prior,3,self.cases['copies_correct'])[0])
        self.assertNotEqual(single,m.posterior(self.prior,3,self.cases['copies_split'])[0])

    def test_age_likelihood_hand_calculation(self):
        b,_=m.posterior(self.prior,3,self.cases['stale_correct'])
        self.assertAlmostEqual(sum(b[i] for i in (1,3,5,7)),.56)

    def test_conflict_is_order_invariant(self):
        reports=self.cases['false_merge_conflict']
        self.assertEqual(m.posterior(self.prior,3,reports),(self.prior,1))
        self.assertEqual(m.posterior(self.prior,3,list(reversed(reports))),(self.prior,1))

    def test_true_fields_do_not_enter_policy(self):
        reports=copy.deepcopy(self.cases['copies_split'])
        before=m.public_reports(reports)
        for row in reports:
            row['true_source']='changed';row['true_flip']=.49
        self.assertEqual(before,m.public_reports(reports))
        self.assertTrue(all('true_source' not in r and 'true_flip' not in r for r in before))

    def test_true_group_disagreement_rejected(self):
        reports=copy.deepcopy(self.cases['false_merge_conflict'])
        reports[1]['true_source']='a'
        with self.assertRaises(ValueError):m.evaluate(self.graph,self.prior,reports)

    def test_privileged_voi_no_worse_for_all_development_cases(self):
        for reports in self.cases.values():
            for cost in (.25,.75):
                rows={r['policy']:r for r in m.evaluate(self.graph,self.prior,reports,cost=cost)['policies']}
                self.assertLessEqual(rows['privileged_voi']['expected_loss'],rows['privileged_immediate']['expected_loss']+1e-9)

    def test_bayes_enumeration_against_two_event_calculation(self):
        reports=[self.cases['single'][0],dict(self.cases['single'][0],source='independent',value=0,accuracy=.6)]
        b,_=m.posterior(self.prior,3,reports)
        self.assertAlmostEqual(sum(b[i] for i in (1,3,5,7)),(.8*.4)/(.8*.4+.2*.6))

    def test_no_observations_preserves_joint_prior(self):
        prior=[.5,0,0,0,0,0,0,.5]
        self.assertEqual(m.posterior(prior,3,[]),(prior,0))
