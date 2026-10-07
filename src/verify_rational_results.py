"""Independent exact-arithmetic scoring of frozen decisions, not planner tuning."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
states=list(product((0,1),repeat=4))

def loss(graph,state,patch):
    adjacency={}
    for u,v,g in graph['edges']:
        if g not in patch and state[g]: adjacency.setdefault(u,[]).append(v)
    visited=set(); stack=[graph['entry']]
    while stack:
        node=stack.pop()
        if node in visited: continue
        visited.add(node); stack.extend(adjacency.get(node,[]))
    return sum(w for t,w in graph['targets'].items() if t in visited)

def truth(case):
    weights=[F(1,16) if case['prior']=='independent_half' else F(1,32)+(F(1,4) if s in ((0,0,0,0),(1,1,1,1)) else 0) for s in states]
    stale=case['evidence'] in ('stale_correct','stale_underestimated','split_and_stale')
    accuracy=F(4,5)*(1-F(2,5))+F(1,5)*F(2,5) if stale else F(4,5)
    for i,s in enumerate(states):
        weights[i]*=accuracy if s[2] else 1-accuracy
        if case['evidence'] in ('independent_conflict','false_merge_conflict'):
            weights[i]*=F(1,5) if s[2] else F(4,5)
    total=sum(weights)
    return [p/total for p in weights]

def main():
    spec=json.loads((ROOT/'protocol/validation-v0.4.json').read_text())
    graphs={g['name']:g for g in spec['graphs']}
    rows=[json.loads(x) for x in (ROOT/'analysis/validation-v0.4/cases.jsonl').read_text().splitlines()]
    results=[]; max_error=0
    for case in rows:
        graph=graphs[case['graph']]; weights=truth(case)
        assert all(abs(float(p)-q)<1e-12 for p,q in zip(weights,case['truth_weights']))
        choices=[()] + [(i,) for i in range(4)]
        oracle=sum(p*min(loss(graph,s,a) for a in choices) for s,p in zip(states,weights))
        assert abs(float(oracle)-case['oracle_loss'])<1e-9
        for row in case['policies']:
            decision=row['decision']; value=F(0); spent=F(0)
            for s,p in zip(states,weights):
                if 'query' not in decision:
                    a=decision['patches'];value+=p*loss(graph,s,a);spent+=p*len(a)
                else:
                    for answer in (0,1):
                        q=F(9,10) if answer==s[decision['query']] else F(1,10)
                        a=decision['patches_after'][str(answer)]
                        branch_cost=F(str(case['query_cost']))+len(a)
                        assert branch_cost<=F(3,2)
                        value+=p*q*loss(graph,s,a);spent+=p*q*branch_cost
            error=abs(float(value)-row['expected_loss']);max_error=max(error,max_error)
            assert error<1e-9 and abs(float(spent)-row['expected_spend'])<1e-9
            results.append(dict(graph=case['graph'],prior=case['prior'],evidence=case['evidence'],query_cost=case['query_cost'],policy=row['policy'],loss_fraction=str(value),spend_fraction=str(spent)))
    out=ROOT/'analysis/rational-audit';out.mkdir(exist_ok=True)
    (out/'results.json').write_text(json.dumps(dict(scope='Post hoc independent exact scoring of saved decisions; not new cases or independent external replication',cases=len(rows),policy_rows=len(results),maximum_absolute_loss_error=max_error,results=results),indent=2)+'\n',encoding='utf-8')
    print(len(rows),'cases;',len(results),'policy rows; maximum float difference',max_error)

if __name__=='__main__': main()
