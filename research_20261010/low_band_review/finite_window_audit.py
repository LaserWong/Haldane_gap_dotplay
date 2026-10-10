"""Independent validation of root's all-integer finite-window certificates.
Accepts square-root claims by squaring rational endpoints, and uses a distinct
Taylor exponential enclosure rather than importing root's implementation.
"""
from independent_review import *
from trace_audit import exponential_interval
RROOT=OUT.parent/'root_review'

def one_dimension(S,T,detail):
    assert 0<S<=1 and 0<T<=1
    p=S*S*T;assert p>F(1,2) and p==F(detail['p'])
    w=F(detail['dominant_weight_lower']);assert F(1,2)<w<=1
    assert (2*w-1)**2<=2*p-1
    r=F(detail['tail_ratio_upper']);assert r==(1-w)/w and 0<=r<1
    d=F(detail['d_lower']);assert d==T/(1+r*r)
    c=F(detail['purity_lower']);assert 0<c<=1
    # c <= (1-r) min(S sqrt(d),d), requiring only exact rational comparisons.
    scaled=c/(1-r)
    assert scaled<=d and (scaled/S)**2<=d
    return c


def audit_file(stem):
    path=RROOT/f'finite_window_{stem}.json';record=json.loads(path.read_text())
    source=OUT.parents[1]/record['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==record['source_sha256']
    raw=json.loads(source.read_text());raw=raw['exact_results'] if isinstance(raw,dict) else raw
    rowsource={r['beta_initial']:r for r in raw if r.get('accepted') and r.get('order')=='xyt'}
    # Physical + recurrence evidence is independently established in these results.
    fn='symmetric_correlated_fast_results.json' if stem.startswith('symmetric') else ('refined_correlated_results.json' if stem.startswith('refined') else 'correlated_results.json')
    independently_verified=json.loads((OUT/fn).read_text())
    assert independently_verified['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
    accepted={r['beta_initial']:r for r in independently_verified['records']}
    reports=[]
    for result in record['results']:
        key=result['initial_beta'];saved=rowsource[key];indep=accepted[key];boot=saved['bootstrap']
        assert result['asymptotic_start']==indep['final_n'] and F(result['asymptotic_gap'])==F(indep['gap_lower'])
        states=[list(map(F,saved['first_purities']))]+[[1-F(v) for v in step['defects']] for step in boot['updates']]
        assert len(states)==len(result['windows']);min_window=None
        for j,(state,row) in enumerate(zip(states,result['windows'])):
            A,B,C=state;assert state==list(map(F,row['purities']))
            n=4*2**j;beta=F(boot['input']['beta'])*2**j
            assert row['n']==n and row['through']==2*n and F(row['beta'])==beta
            det=row['details'];sx=F(det['spatial_lower']);assert B>F(1,2) and 0<sx<=1
            assert sx*sx<=A**4*(2*B-1)
            ty=one_dimension(B,C,det['y']);assert ty==F(det['transverse_thermal_lower'])
            thermal=one_dimension(sx,ty,det['x']);assert thermal==F(row['thermal_lower']) and thermal>F(1,2)
            gap=F(row['gap_lower']);assert gap>0
            upper_exp=exponential_interval(beta*gap)[1]
            assert upper_exp*(1-thermal)<thermal
            if n<indep['final_n']:min_window=gap if min_window is None else min(min_window,gap)
        small=min(F(1)-3*F(3,100)*L*L for L in [2,3])
        assert small==F(19,100)==F(result['local_L2_L3_gap'])
        combined=min(F(indep['gap_lower']),small,min_window)
        assert combined==F(result['all_integer_L_ge2_gap'])
        reports.append(dict(beta_initial=key,all_square_sides='every integer L >= 2',
                            exact_sqrt_endpoint_inequalities_passed=True,
                            independent_exponential_gap_checks_passed=True,
                            finite_window_count=len(states),minimum_required_finite_window_gap=str(min_window),
                            small_L2_L3_lower=str(small),all_integer_gap_lower=str(combined),gap_display=float(combined)))
        print('EXACT ALL-INTEGER BRIDGE PASS',key,float(combined),flush=True)
    return dict(source_file=path.name,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),records=reports)

report=dict(status='passed_independent_exact_all_integer_bridge',files=[])
for stem in ['correlated_full_low_band_g3d100_number','refined_correlated_number_g003','symmetric_correlated_beta909d100_FINAL']:
    report['files'].append(audit_file(stem))
(OUT/'finite_window_results.json').write_text(json.dumps(report,indent=2))
