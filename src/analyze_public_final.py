"""Verify saved raw probes and summarize the fixed six-case feasibility subset."""
import hashlib,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load_runs(directory, prefix=None):
    folder=ROOT/'analysis'/directory
    rows=json.loads((folder/'runs.json').read_text())
    for r in rows:
        if directory.endswith('pretalx'):
            name=f"pretalx-{r['version']}-{r['repeat']}"
        elif directory.endswith('langroid-final'):
            name=f"langroid-v2-{r['version']}-{r['repeat']}"
        else:
            continue
        # pretalx prints a startup banner before its JSON. Preserve the original
        # runner's parse_error and derive data from the single complete JSON line.
        raw=(folder/(name+'.stdout.txt')).read_text(encoding='utf-8')
        candidates=[]
        for line in raw.splitlines():
            try: obj=json.loads(line)
            except ValueError: continue
            if isinstance(obj,dict) and 'observations' in obj: candidates.append(obj)
        assert len(candidates)==1 and r['exit_code']==0, name
        r['verified_observed']=candidates[0]
        assert candidates[0]['version']==r['version']
    return rows

def main():
    lang=load_runs('public-evidence-v0.5-langroid-final')
    pret=load_runs('public-evidence-v0.5-pretalx')
    for rows,versions in [(lang,('0.53.14','0.53.15')),(pret,('2.3.1','2.3.2'))]:
        assert len(rows)==6
        assert {(r['version'],r['repeat']) for r in rows}=={(v,n) for v in versions for n in (1,2,3)}
    for r in lang:
        o={x['label']:x['result'] for x in r['verified_observed']['observations']}
        assert set(o)=={'benign','restricted_builtin','invalid_control'}
        assert o['benign']=='2' and o['invalid_control'].startswith('Error encountered in pandas eval:')
        assert (o['restricted_builtin']=='2') if r['version']=='0.53.14' else o['restricted_builtin'].startswith('Error encountered in pandas eval:')
    for r in pret:
        o={x['label']:x for x in r['verified_observed']['observations']}
        assert set(o)=={'benign','traversal'}
        assert o['benign']['file_exists'] and o['benign']['expected_content'] and o['benign']['error'] is None
        t=o['traversal']
        if r['version']=='2.3.1': assert t['file_exists'] and t['expected_content'] and t['error'] is None
        else: assert not t['file_exists'] and not t['expected_content'] and t['error']=='Path traversal detected, aborting.'
    old=json.loads((ROOT/'analysis/public-evidence-v0.5-behavior/runs.json').read_text())
    cert=[r for r in old if r['case']=='certifi']
    scrapy=json.loads((ROOT/'analysis/public-evidence-v0.5-behavior-compatible/runs.json').read_text())
    summary=[]
    for package,rows in [('langroid',lang),('pretalx',pret),('scrapy',scrapy),('certifi',cert)]:
        obs=[r.get('verified_observed',r.get('observed')) for r in rows]
        summary.append(dict(package=package,successful_runs=len(rows),probe_seconds_min=min(o['probe_seconds'] for o in obs),probe_seconds_median=statistics.median(o['probe_seconds'] for o in obs),probe_seconds_max=max(o['probe_seconds'] for o in obs),peak_process_rss_kib_max=max(o['peak_process_rss_kib'] for o in obs),elapsed_seconds_median=statistics.median(r['elapsed_seconds'] for r in rows)))
    failures=[]
    for directory in ['public-evidence-v0.5-behavior','public-evidence-v0.5-behavior-retry','public-evidence-v0.5-langroid','public-evidence-v0.5-langroid-cached']:
        runs=json.loads((ROOT/'analysis'/directory/'runs.json').read_text())
        failures.extend(dict(series=directory,**r) for r in runs if r['exit_code']!=0)
    assert len(failures)==24
    out=ROOT/'analysis/public-evidence-final';out.mkdir(exist_ok=True)
    result=dict(scope='Fixed first-six feasibility subset; no replacements',confirmed_narrow_cases=4,excluded_stable_release=1,unsupported_fixture=1,probe_series_setup_failures=24,pretalx_json_banner_parse_corrections=6,summary=summary,langroid=lang,pretalx=pret)
    (out/'verified-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('langroid','pretalx')},indent=2))

if __name__=='__main__': main()
