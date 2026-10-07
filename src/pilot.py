"""Exact synthetic decision pilot. No network operations or NASim execution."""
import itertools,json,math
from pathlib import Path
STATES=list(itertools.product((0,1),repeat=2))
WEIGHTS=(10,8)

def loss(state,patches):
    # Two separate entry->service->critical-target paths; patch cuts its path.
    return sum(w for i,w in enumerate(WEIGHTS) if state[i] and i not in patches)

def posterior(reports,grouped=True,age=True,true_groups=False):
    unique={}
    for j,r in enumerate(reports):
        key=(r['asset'],r['true_source'] if true_groups else r['source']) if grouped else j
        if key in unique and unique[key]!=r:
            # Duplicate contents may differ only in externally assigned source IDs.
            a=unique[key]
            if any(a[k]!=r[k] for k in ('asset','value','accuracy','flip')):raise ValueError('Conflicting rows within a source group')
        unique.setdefault(key,r)
    values=[]
    for s in STATES:
        p=.25
        for r in unique.values():
            q=r['accuracy'];flip=r['flip'] if age else 0
            effective=q*(1-flip)+(1-q)*flip
            p*=effective if s[r['asset']]==r['value'] else 1-effective
        values.append(p)
    z=sum(values)
    if z<=0:raise ValueError('Impossible evidence')
    return [p/z for p in values]

def expected(belief,patches):return sum(p*loss(s,patches) for p,s in zip(belief,STATES))
def choices(budget):return [c for n in range(3) for c in itertools.combinations(range(2),n) if n<=budget+1e-9]
def best(belief,budget):return min(choices(budget),key=lambda c:(expected(belief,c),len(c),c))
def branches(belief,asset,q):
    result=[]
    for value in (0,1):
        mass=[p*(q if s[asset]==value else 1-q) for p,s in zip(belief,STATES)];z=sum(mass)
        result.append((value,z,[p/z for p in mass] if z else list(belief)))
    return result

def evaluate_query(truth,belief,asset,cost,budget,q):
    actions={v:best(b,budget-cost) for v,_,b in branches(belief,asset,q)}
    risk=spent=0
    for v,p,b in branches(truth,asset,q):
        risk+=p*expected(b,actions[v]);spent+=p*(cost+len(actions[v]))
    return risk,spent,actions

def run_case(case):
    # Policies receive only sanitized observation records, never true_source or truth.
    reports=case['reports'];truth=posterior(reports,true_groups=True)
    public=[{k:v for k,v in r.items() if k!='true_source'} for r in reports]
    b=posterior(public);budget=case['budget'];cost=case['verify_cost'];q=case['verify_accuracy']
    oracle=sum(p*min(loss(s,c) for c in choices(budget)) for p,s in zip(truth,STATES))
    rows=[]
    def add(name,risk,spent,decision):
        rows.append({'policy':name,'expected_loss':risk,'regret':risk-oracle,'expected_spend':spent,'decision':decision})
    for name,belief in [('naive_reports',posterior(public,False,False)),('deduplicated',posterior(public,True,False)),('lineage_and_age',b)]:
        action=best(belief,budget);add(name,expected(truth,action),len(action),{'patches':list(action)})
    # Fixed impact-first baseline ignores observations but has the same budget.
    action=tuple(range(min(2,int(budget))));add('impact_first',expected(truth,action),len(action),{'patches':list(action)})
    marg=[sum(p*s[i] for p,s in zip(b,STATES)) for i in range(2)]
    entropy=lambda p: -sum(x*math.log2(x) for x in (p,1-p) if x)
    i=max(range(2),key=lambda i:entropy(marg[i]))
    if cost<=budget:
        evaluated=[evaluate_query(truth,b,i,cost,budget,q) for i in range(2)]
        rr,ss,acts=evaluated[i];add('uncertainty_query',rr,ss,{'query':i,'patches_after':acts})
        add('random_query',sum(x[0] for x in evaluated)/2,sum(x[1] for x in evaluated)/2,{'uniform_queries':[0,1]})
        # Standard myopic VOI minimizes modeled terminal loss, including lost patch capacity.
        options=[(expected(b,best(b,budget)),None)]
        options += [(evaluate_query(b,b,i,cost,budget,q)[0],i) for i in range(2)]
        _,selected=min(options,key=lambda x:(x[0],-1 if x[1] is None else x[1]))
        if selected is None:
            a=best(b,budget);add('standard_voi',expected(truth,a),len(a),{'patches':list(a)})
        else:
            rr,ss,acts=evaluated[selected];add('standard_voi',rr,ss,{'query':selected,'patches_after':acts})
    oracle_spend=sum(p*len(min(choices(budget),key=lambda c:(loss(s,c),len(c),c))) for p,s in zip(truth,STATES))
    add('full_state_oracle',oracle,oracle_spend,{'diagnostic_only':True})
    assert all(-1e-8<=x['regret'] and x['expected_spend']<=budget+1e-9 for x in rows)
    return {'case':case['name'],'budget':budget,'verify_cost':cost,'truth_weights':truth,'results':rows}

def main():
    root=Path(__file__).resolve().parents[1]
    cases=json.loads((root/'data/pilot-cases.json').read_text())
    result={'type':'exact synthetic feasibility calculation','not_live_trials':True,'cases':[run_case(c) for c in cases]}
    (root/'analysis/pilot-results.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Exact synthetic pilot results','','These are enumerated model expectations, not measured attack frequencies or independent live trials. Lower modeled loss is better. NASim fixtures are not used in these calculations.','','| Case | Naive | Dedup | Lineage + age | Standard VOI | Oracle |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for c in result['cases']:
        m={x['policy']:x for x in c['results']}
        lines.append('| '+c['case']+' | '+' | '.join(f"{m[k]['expected_loss']:.3f}" for k in ('naive_reports','deduplicated','lineage_and_age','standard_voi','full_state_oracle'))+' |')
    lines+=['','No novel algorithm is implemented: standard VOI is a baseline. Perfect patch efficacy, a two-path graph, a known observation model and only one optional verification are strong simplifications. Source-label errors are modeled explicitly; uncertainty about error parameters and larger graphs remain untested.']
    (root/'analysis/Results.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
