"""Independent extension of the earlier chain auditor, without producer imports.
Inputs are rational records and integer vectors. Exact arithmetic controls all
acceptance; floating values are display-only. One CPU and 1 GiB AS limit.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k]='1'
import json, hashlib, math, time, resource, argparse
from pathlib import Path
from fractions import Fraction as Q
import independent_core as C
HERE=Path(__file__).resolve().parent
DATA=HERE.parent/'chain_frontier'
START=time.monotonic()
HASHES={}
GROUND_CACHE={}
PINNED=json.loads((HERE/'PRODUCER_FINALIZED_SHA256.json').read_text())
assert len(os.sched_getaffinity(0))==1, 'Run with taskset on exactly one permitted CPU'

def read(name):
    p=DATA/name
    b=p.read_bytes();HASHES[name]=hashlib.sha256(b).hexdigest()
    if name in PINNED:assert HASHES[name]==PINNED[name], 'Finalized producer hash mismatch: '+name
    return json.loads(b)

def check_ground(r):
    key=json.dumps(r,sort_keys=True)
    if key not in GROUND_CACHE:
        GROUND_CACHE[key]=C.check_ground(r)
        name=r['trial_artifact'];HASHES[name]=hashlib.sha256((DATA/name).read_bytes()).hexdigest()
        print('GROUND PASS',r['N_dimers'],r['relative_form_bound']['local_certificate']['coupling'],r['trial_subspace_dimension'],r['reached_support_dimension'],flush=True)
    return GROUND_CACHE[key]

def thermal_exp(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)

def correlated_seed(r1,r2,seed):
    beta=Q(seed['beta']);q1,t1=C.trace_bound(r1,beta);q2,t2=C.trace_bound(r2,beta)
    shift=Q(r2['ground_upper'])-2*Q(r1['ground_upper'])
    S=C.floor(C.exp_bounds(-beta*shift)[0]/q1**2)
    T=C.floor(1/q2**2)
    J=C.floor(C.exp_bounds(-2*beta*shift)[0]/q1**4)
    independent=[S,T,J]
    fields=['S_lower','T_lower','J_direct_lower']
    saved_endpoints=[Q(seed[k]) for k in fields]
    assert all(x>=y for x,y in zip(independent,saved_endpoints)),(beta,independent,saved_endpoints)
    # Producer 128-bit exp enclosures can be looser at large beta. Reconstruct
    # both nonlinear first-step updates from its now-verified lower endpoints.
    S,T,J=saved_endpoints
    A=C.floor(thermal_exp(J)) if J>0 else Q(-1)
    B=C.floor(thermal_exp(T*T*A)) if T>0 and A>0 else Q(-1)
    assert [A,B]==[Q(seed[k]) for k in ['first_S_lower','first_T_lower']]
    assert t1<=Q(seed['tail_upper'][0]) and t2<=Q(seed['tail_upper'][1])
    saved=seed['bootstrap']
    out=dict(beta=str(beta),all_seed_lower_endpoints_verified=True,
             first_step_updates_identical=True,
             first_three_rounded_endpoints_identical=independent==saved_endpoints,
             independent_rounded_endpoints=list(map(str,independent)),
             whole_space_tail_upper_verified=True,independent_tail_displays=[float(t1),float(t2)])
    if A<=0 or B<=0:
        assert saved['status']=='rejected_first_correlated_step'
        out.update(accepted=False,status=saved['status']);return out
    rep=C.bootstrap(A,B,2*r1['N_dimers'],2*beta)
    assert rep['status']==saved['status'] and rep['updates']==saved['updates']
    assert saved['input']=={'S_lower':str(A),'T_lower':str(B),'n':2*r1['N_dimers'],'beta':str(2*beta)}
    out.update(accepted=rep['status']=='accepted_conditional_scalar_seed',status=rep['status'],
               all_sequential_updates_identical=True)
    if out['accepted']:
        assert rep['n']==saved['final_n'] and rep['beta']==saved['final_beta']
        u=max(Q(rep['p']),Q(rep['q']));gap=Q(saved['conditional_gap_lower_rational'])
        assert Q(saved['final_common_u'])==u
        assert C.exp_bounds(Q(rep['beta'])*gap)[1]<1/(5*u)
        out.update(asymptotic_from=rep['n'],gap=str(gap),final_common_u=str(u),
                   final_beta=rep['beta'],gap_exponential_check=True)
    return out

def interpolate(S,T):
    assert 0<S<=1 and 0<T<=1
    P=S*S*T;assert P>Q(1,2)
    root=C.sqrt_lower(2*P-1,60);assert root*root<=2*P-1<(root+Q(1,10**60))**2
    w=(1+root)/2;r=(1-w)/w;D=T/(1+r*r)
    sqrtD=C.sqrt_lower(D,60);assert sqrtD*sqrtD<=D<(sqrtD+Q(1,10**60))**2
    purity=(1-r)*min(S*sqrtD,D)
    return purity,dict(inverse_purity_argument=str(P),sqrt_lower=str(root),
                      dominant_weight_lower=str(w),tail_ratio_upper=str(r),
                      D_lower=str(D),sqrt_D_lower=str(sqrtD),purity_lower=str(purity))

def audit_bridges(stem,data,seeds):
    r=read(stem+'_correlated_bridges.json')
    assert Q(r['g'])==Q(data['g']) and r['source'].endswith(stem+'_correlated.json')
    local=r['short_local_comparison'];lc=local['local_certificate'];lp=C.local_psd(lc)
    a,b=Q(lc['a']),Q(lc['b']);assert Q(lc['coupling'])==Q(data['g']) and 0<1-2*a and b>=0
    end=r.get('short_local_cells',[2,7])[1]
    localgap=1-2*a-end*b
    assert localgap==Q(local['second_shift_lower']) and Q(local['B'])==end*b and Q(local['alpha'])==1-2*a
    edgecheck=None
    if 'short_edge_ground_certificate' in r:
        edge=r['short_edge_ground_certificate'];assert edge['N_dimers']==end+1==7
        assert Q(edge['relative_form_bound']['local_certificate']['coupling'])==Q(data['g'])
        edgecheck=check_ground(edge)
        edgegap=Q(edge['second_eigenvalue_lower'])-Q(edge['ground_upper'])
        assert edgegap==Q(r['short_edge_gap_lower'])
        shortgap=min(localgap,edgegap)
    else:assert end==7;shortgap=localgap
    bybeta={s['beta']:s for s in data['seeds']};rows=[]
    for row in r['rows']:
        seed=bybeta[row['initial_beta']];boot=seed['bootstrap']
        assert boot['status']=='accepted_conditional_scalar_seed'
        states=[(Q(seed['first_S_lower']),Q(seed['first_T_lower']))]+[(1-Q(x['p_upper']),1-Q(x['q_upper'])) for x in boot['updates']]
        n=2*data['n'];beta=2*Q(seed['beta']);wins=[]
        assert len(row['windows'])==len(boot['updates'])
        for st,saved in zip(states,row['windows']):
            assert saved['cells']==[n,2*n] and Q(saved['beta'])==beta
            assert [Q(saved['S_lower']),Q(saved['T_lower'])]==list(st)
            purity,details=interpolate(*st)
            savedC=Q(saved['thermal_purity_lower'])
            assert Q(1,2)<savedC<=purity
            gap=Q(saved['gap_lower']);assert C.exp_bounds(beta*gap)[1]*(1-savedC)<savedC
            wins.append(dict(cells=[n,2*n],beta=str(beta),gap=str(gap),
                             saved_purity_lower_verified=True,independent=details))
            n*=2;beta*=2
        assert n==boot['final_n']==row['asymptotic_from'] and row['short_size_max']==7
        assert Q(row['short_gap_lower'])==shortgap
        gap=Q(boot['conditional_gap_lower_rational']);assert gap==Q(row['asymptotic_gap'])
        allgap=max(Q(0),min([gap,shortgap]+[Q(x['gap']) for x in wins]))
        assert allgap==Q(row['all_M_ge2_gap_lower'])
        rows.append(dict(beta=seed['beta'],all_M_ge2_gap=str(allgap),asymptotic_from=n,windows=wins))
    best=max(rows,key=lambda x:Q(x['all_M_ge2_gap']))
    assert Q(r['best']['all_M_ge2_gap_lower'])==Q(best['all_M_ge2_gap'])
    return dict(short_local_positivity=lp,short_local_cells=[2,end],short_local_gap=str(localgap),
                short_M7_ground_check=edgecheck,short_combined_gap=str(shortgap),rows=rows,best=best)

def audit_candidate(stem):
    data=read(stem+'_correlated.json');assert data['n']==4 and data['depth']==4
    assert all(Q(r['relative_form_bound']['local_certificate']['coupling'])==Q(data['g']) for r in data['ground_certificates'])
    grounds=[check_ground(r) for r in data['ground_certificates']]
    assert [x['N_dimers'] for x in grounds]==[4,8]
    seeds=[correlated_seed(*data['ground_certificates'],s) for s in data['seeds']]
    bridge=audit_bridges(stem,data,seeds)
    out=dict(status='PASS independent full-space all-integer M>=2 audit',g=data['g'],
             grounds=grounds,seeds=seeds,bridges=bridge)
    (HERE/(stem+'_independent_review.json')).write_text(json.dumps(out,indent=2)+'\n')
    print('ALL-SIZE PASS',data['g'],bridge['best']['all_M_ge2_gap'],flush=True)
    return dict(g=data['g'],gap=bridge['best']['all_M_ge2_gap'],status='PASS',
                audited_seeds=len(seeds),accepted_seeds=sum(x['accepted'] for x in seeds))

def ceiling(record):
    g=Q(record['g']);N=record['N'];assert record['local_dimension']==81
    out=[]
    for line in record['lines']:
        u=line['vector'];assert len(u)==81 and all(type(x) is int for x in u)
        w=[C.W[i//9]*C.W[i%9] for i in range(81)]
        norm=sum(wi*ui*ui for wi,ui in zip(w,u));assert norm>0 and norm==int(line['norm'])
        eh=Q(sum(w[i]*u[i]**2*(C.EX[i//9]+C.EX[i%9]) for i in range(81)),norm)
        ev=sum((g*v*w[9*r+s]*u[9*r+s]*u[9*c+d] for c in range(9) for d in range(9) for r,s,v in C.K[c,d]),Q(0))/norm
        intercept=1+N*ev;slope=N*eh-2
        assert [eh,ev,intercept,slope]==[Q(line[x]) for x in ['h_expectation','gV_expectation','intercept','slope']]
        out.append((intercept,slope))
    assert len(out)==2
    (c1,s1),(c2,s2)=out;assert s1>0>s2
    cross=(c2-c1)/(s1-s2);bound=c1+s1*cross
    assert cross==Q(record['intersection_a']) and bound==Q(record['cutoff_shift_upper'])
    return dict(N=N,g=str(g),all_real_a_affine_ceiling_verified=True,
                cutoff_shift_upper=str(bound),cutoff_display=float(bound),intersection_a=str(cross))

def obstruction_replay(J,T):
    """Propagate upper bounds, using 12-decimal upward rather than dyadic rounding.
    Failure region is absorbing and disjoint from the acceptance region.
    """
    assert 0<J<=1 and 0<T<=1
    steps=[]
    if J<=Q(1,2):return dict(reason='J <= 1/2 implies absorbing failure',steps=steps)
    A=min(Q(1),C.ceil(thermal_exp(J)))
    if A<=0:return dict(reason='initial spatial upper bound nonpositive',steps=steps)
    B=min(Q(1),C.ceil(thermal_exp(T*T*A)))
    if B<=0:return dict(reason='initial thermal upper bound nonpositive',steps=steps)
    for i in range(100):
        steps.append(dict(S_upper=str(A),T_upper=str(B),argument_upper=str(A*A*B)))
        if A*A*B<=Q(1,2):return dict(reason='absorbing S^2 T <= 1/2 failure region',steps=steps)
        assert min(A,B)<Q(99,100),'Optimistic enclosure admits acceptance, exclusion unproved'
        A2=min(Q(1),C.ceil(thermal_exp(A*A*B)))
        if A2<=0:return dict(reason='subsequent spatial upper bound nonpositive',steps=steps)
        B2=min(Q(1),C.ceil(thermal_exp(B*B*A2)))
        if B2<=0:return dict(reason='subsequent thermal upper bound nonpositive',steps=steps)
        A,B=A2,B2
    raise AssertionError('No terminal independent exclusion')

def audit_interval_obstruction(stem):
    r=read(stem+'_obstruction.json');source=read(stem+'.json');rs=source['ground_certificates']
    assert all(Q(x['relative_form_bound']['local_certificate']['coupling'])==Q(source['g']) for x in rs)
    grounds=[check_ground(x) for x in rs];ceilings=[ceiling(x) for x in r['local_ceilings']]
    assert [c['N'] for c in ceilings]==[x['N_dimers'] for x in rs]
    assert all(Q(c['g'])==Q(source['g'])==Q(r['g']) for c in ceilings)
    delta=[Q(x['E00'])+Q(c['cutoff_shift_upper'])-Q(x['ground_lower']) for x,c in zip(rs,ceilings)]
    kappa=Q(rs[1]['ground_lower'])-2*Q(rs[0]['ground_upper']);assert kappa>0
    assert delta==list(map(Q,r['delta_upper'])) and kappa==Q(r['curvature_lower'])
    B=Q(r['tail_beta_from']);tail=C.exp_bounds(-2*B*kappa)[1]
    assert tail<=Q(r['tail_J_upper'])<=Q(1,2)
    assert r['all_beta_all_a_excluded'] and not r['unresolved_intervals'] and not r['remaining_unvisited_intervals']
    intervals=sorted(r['excluded_intervals'],key=lambda x:Q(x['beta_interval'][0]));edge=Q(0);results=[]
    for leaf in intervals:
        l,h=map(Q,leaf['beta_interval']);assert l==edge and l<h<=B
        qfloors=[1+3*x['N_dimers']*C.exp_bounds(-(h if d>=0 else l)*d)[0] for x,d in zip(rs,delta)]
        J=min(Q(1),C.exp_bounds(-2*l*kappa)[1]/qfloors[0]**4)
        T=min(Q(1),1/qfloors[1]**2)
        assert J<=Q(leaf['J_upper']) and T<=Q(leaf['T_upper'])
        rep=obstruction_replay(Q(leaf['J_upper']),Q(leaf['T_upper']))
        results.append(dict(beta_interval=[str(l),str(h)],independent_upper_bound_check=True,**rep))
        edge=h
    assert edge==B
    out=dict(status='PASS independent all-beta/all-local-a recipe obstruction',g=r['g'],ground_checks=grounds,
             ceilings=ceilings,delta_upper=list(map(str,delta)),curvature_lower=str(kappa),
             high_beta_tail_from=str(B),tail_J_upper_verified=True,intervals=results,
             interval_union='[0,B] plus [B,infinity); beta=0 included only for enclosure')
    (HERE/(stem+'_obstruction_independent_review.json')).write_text(json.dumps(out,indent=2)+'\n')
    print('OBSTRUCTION PASS',r['g'],len(intervals),'intervals and high-beta tail',flush=True)
    return dict(g=r['g'],status='PASS',interval_count=len(intervals),tail_beta_from=str(B))

def audit_simple_obstruction():
    r=read('local_ceiling_g7d40_N8.json');source=read('chain_sparse_s1_g7d40_n4_depth4.json')
    rs=source['ground_certificates'];grounds=[check_ground(x) for x in rs];c=ceiling(r)
    assert c['N']==rs[1]['N_dimers']==8 and Q(c['g'])==Q(7,40)
    saved=r['all_beta_obstruction'];B=Q(saved['beta_split'])
    delta=Q(rs[1]['E00'])+Q(c['cutoff_shift_upper'])-Q(rs[1]['ground_lower'])
    kappa=Q(rs[1]['ground_lower'])-2*Q(rs[0]['ground_upper'])
    assert delta==Q(saved['delta_upper'])>=0 and kappa==Q(saved['curvature_lower'])>0
    qfloor=1+24*C.exp_bounds(-B*delta)[0]
    T=1/qfloor**2;J=C.exp_bounds(-2*B*kappa)[1]
    assert T<=Q(saved['thermal_upper_for_beta_below_split'])<=Q(1,2)
    assert J<=Q(saved['J_upper_for_beta_above_split'])<=Q(1,2)
    lower=obstruction_replay(Q(1),Q(saved['thermal_upper_for_beta_below_split']))
    upper=obstruction_replay(Q(saved['J_upper_for_beta_above_split']),Q(1))
    out=dict(status='PASS independent all-beta/all-local-a recipe obstruction',g='7/40',ground_checks=grounds,
             ceiling=c,beta_split=str(B),delta_upper=str(delta),curvature_lower=str(kappa),
             lower_beta_exclusion=lower,upper_beta_exclusion=upper)
    (HERE/'g7d40_obstruction_independent_review.json').write_text(json.dumps(out,indent=2)+'\n')
    print('OBSTRUCTION PASS 7/40 split',B,flush=True)
    return dict(g='7/40',status='PASS',beta_split=str(B))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--include-new',action='store_true');ap.add_argument('--include-deeper',action='store_true');ap.add_argument('--deeper-only',action='store_true');args=ap.parse_args()
    cs=['chain_sparse_s1_g4d25_n4_depth4','chain_sparse_s1_g161d1000_n4_depth4']
    if args.include_new:cs+=['chain_sparse_s1_g129d800_n4_depth4']
    candidates=[] if args.deeper_only else [audit_candidate(s) for s in cs]
    obs=[] if args.deeper_only else [audit_interval_obstruction('chain_sparse_s1_g13d80_n4_depth4'),audit_simple_obstruction()]
    if args.include_deeper or args.deeper_only:obs.append(audit_interval_obstruction('chain_sparse_s1_g323d2000_n4_depth5'))
    # Additional finalized obstruction can be checked by explicitly changing this list.
    summary=dict(status='PASS',candidates=candidates,obstructions=obs,seconds=time.monotonic()-START,
                 peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,BLAS_threads=1,address_space_limit_bytes=1024**3,CPU_affinity=sorted(os.sched_getaffinity(0)),
                 pinned_producer_hashes_verified=[name for name in PINNED if name in HASHES],
                 verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 independent_core_sha256=hashlib.sha256((HERE/'independent_core.py').read_bytes()).hexdigest())
    suffix='_deeper' if args.deeper_only else ''
    (HERE/('summary'+suffix+'.json')).write_text(json.dumps(summary,indent=2)+'\n')
    (HERE/('INPUT_SHA256SUMS'+suffix+'.json')).write_text(json.dumps(HASHES,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))
