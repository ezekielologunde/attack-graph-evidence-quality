import sys,unittest,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pilot import *
class PilotTests(unittest.TestCase):
 def test_reference_reachability(self):
  for s in STATES:
   for patches in choices(2):
    edges=[('entry','a'),('a','critical_a'),('entry','b'),('b','critical_b')]
    allowed=[e for e in edges if not (e[0]=='entry' and (not s[0 if e[1]=='a' else 1] or (0 if e[1]=='a' else 1) in patches))]
    reached={'entry'}
    for _ in range(3):reached.update(v for u,v in allowed if u in reached)
    self.assertEqual(loss(s,patches),10*('critical_a' in reached)+8*('critical_b' in reached))
 def test_budget(self):
  for budget in (0,.5,1,1.5,2):self.assertTrue(all(len(a)<=budget for a in choices(budget)))
 def test_duplicate_invariance(self):
  r={'asset':0,'value':1,'accuracy':.8,'flip':0,'source':'x'}
  self.assertEqual(posterior([r]),posterior([r]*5))
  self.assertNotEqual(posterior([r],False),posterior([r]*5,False))
 def test_total_probability(self):
  for _,_,b in branches([.25]*4,0,.9):self.assertAlmostEqual(sum(b),1)
  self.assertAlmostEqual(sum(p for _,p,_ in branches([.25]*4,0,.9)),1)
 def test_explicit_state_flip(self):
  r={'asset':0,'value':1,'accuracy':1,'flip':1,'source':'x'}
  self.assertEqual(sum(p*s[0] for p,s in zip(posterior([r]),STATES)),0)
 def test_unaffordable_second_patch(self):self.assertNotIn((0,1),choices(1.75))
 def test_no_reports(self):self.assertEqual(posterior([]),[.25]*4)

 def test_query_opportunity_cost(self):
  c={'name':'cost','reports':[],'budget':1.5,'verify_cost':.75,'verify_accuracy':.9}
  m={r['policy']:r for r in run_case(c)['results']}
  self.assertNotIn('query',m['standard_voi']['decision'])
  self.assertGreater(m['uncertainty_query']['expected_loss'],m['standard_voi']['expected_loss'])
 def test_no_latent_access_needed(self):
  self.assertEqual(best([.25]*4,1), (0,))
 def test_perfect_query_probability(self):
  for value,prob,b in branches([.25]*4,0,1):
   self.assertEqual(prob,.5)
   self.assertEqual(sum(p*s[0] for p,s in zip(b,STATES)),value)
