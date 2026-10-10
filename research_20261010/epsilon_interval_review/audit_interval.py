"""Independent exact continuum audit. Imports no project or producer modules.

Only writes in this directory. Reconstructs physical spin kernels, every full
sparse action and coefficient, occupation reference, endpoint LDL, correlated
heat factors, bootstrap, finite windows, baseline and exact union coverage.
One CPU thread; NumPy is used solely to load immutable integer NPZ vectors.
"""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
import json, math, hashlib, time, resource, itertools
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from functools import lru_cache
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
CAND=ROOT/'research_20261010/epsilon_interval_extension'
BASE=ROOT/'research_20261010/nonperturbative_audit'
J=F(3,10)
START=time.monotonic()
HASHES={}
def read(path):
    path=Path(path); b=path.read_bytes()
    name=str(path.relative_to(ROOT)); digest=hashlib.sha256(b).hexdigest()
    assert name not in HASHES or HASHES[name]==digest, ('input changed',name)
    HASHES[name]=digest
    return json.loads(b)
def sha(path):
    b=path.read_bytes(); s=hashlib.sha256(b).hexdigest()
    name=str(path.relative_to(ROOT))
    assert name not in HASHES or HASHES[name]==s, ('input changed',name)
    HASHES[name]=s
    return s
def strs(xs):return list(map(str,xs))
def poly(cs,x):return sum(c*x**i for i,c in enumerate(cs))
def lower(x,bits=224):
    x=F(x); return F((x.numerator<<bits)//x.denominator,1<<bits)
def upper(x,bits=224):return -lower(-x,bits)
@lru_cache(None)
def exp_interval(x):
    """224-bit outward, 64 Taylor terms after reduction to [0,1/8]."""
    x=F(x)
    if x<0:
        l,h=exp_interval(-x);return lower(1/h),upper(1/l)
    squarings=0
    while x>F(1,8):x/=2;squarings+=1
    term=F(1);s=term
    for k in range(1,65):term*=x/k;s+=term
    # Subsequent ratios are <= x/66 after the first omitted term.
    remainder=(term*x/65)/(1-x/66)
    l,h=lower(s),upper(s+remainder)
    for _ in range(squarings):l,h=lower(l*l),upper(h*h)
    return l,h

# Direct four-physical-spin exchange matrices, indexing tensor factors MSB first.
def spin_exchange(n,i,j):
    a=[[F(0) for _ in range(1<<n)] for _ in range(1<<n)]
    mi,mj=1<<(n-1-i),1<<(n-1-j)
    for c in range(1<<n):
        parallel=bool(c&mi)==bool(c&mj)
        a[c][c]=F(1 if parallel else -1,4)
        if not parallel:a[c^mi^mj][c]=F(1,2)
    return a
# Fixed artifact convention: unnormalized singlet, down/down, triplet zero, up/up.
RV=((0,-1,1,0),(1,0,0,0),(0,1,1,0),(0,0,0,1))
METRIC=tuple(sum(x*x for x in col) for col in RV)
assert METRIC==(2,1,2,1)
assert all(sum(a*b for a,b in zip(RV[i],RV[j]))==0 for i in range(4) for j in range(i))
RUNG=spin_exchange(2,0,1)
assert all(sum(RUNG[i][j]*RV[s][j] for j in range(4))==(-F(3,4) if s==0 else F(1,4))*RV[s][i] for s in range(4) for i in range(4))
COLUMNS=[tuple(RV[s][i]*RV[t][j] for i in range(4) for j in range(4)) for s in range(4) for t in range(4)]
EX={(i,j):spin_exchange(4,i,j) for i,j in [(0,1),(2,3),(0,2),(0,3),(1,2),(1,3)]}
KERNEL={}
for a,b in itertools.product(range(2),repeat=2):
    physical=EX[a,2+b]; kernel={}
    for source in range(16):
        action=[sum(physical[i][j]*COLUMNS[source][j] for j in range(16)) for i in range(16)]
        vals=[sum(COLUMNS[target][i]*action[i] for i in range(16))/ (METRIC[target//4]*METRIC[target%4]) for target in range(16)]
        assert all(sum(vals[t]*COLUMNS[t][i] for t in range(16))==action[i] for i in range(16))
        kernel[source//4,source%4]=[(t//4,t%4,v) for t,v in enumerate(vals) if v]
    KERNEL[a,b]=kernel

@lru_cache(None)
def edges(nx,ny):
    e=Counter()
    for x in range(nx):
        for y in range(ny):
            i=x*ny+y
            for j in (((x+1)%nx)*ny+y,x*ny+(y+1)%ny):e[tuple(sorted((i,j)))]+=1
    assert sum(e.values())==2*nx*ny
    assert all(sum(w for uv,w in e.items() if i in uv)==4 for i in range(nx*ny))
    return e
@lru_cache(None)
def occupancy(nx,ny):
    n=nx*ny; h=Counter()
    for mask in range(1<<n):
        q=mask.bit_count();active_weight=0;max_incident=[0]*n
        for (i,j),w in edges(nx,ny).items():
            if (mask>>i)&(mask>>j)&1:
                active_weight+=w
                max_incident[i]=max(max_incident[i],w);max_incident[j]=max(max_incident[j],w)
        f=F(20*q-6*active_weight-3*sum(max_incident),20)
        h[q,f]+=3**q
    assert sum(h.values())==4**n
    assert all(sum(m for (k,f),m in h.items() if k==q)==math.comb(n,q)*3**q for q in range(n+1))
    return h

def local_psd(a,b,e):
    assert a>=0 and b>0
    # P_i+P_j = S_0.S_1 + S_2.S_3 + 3 I / 2.
    matrix=[[e*(EX[0,2][i][j]+EX[1,3][i][j])+a*(EX[0,1][i][j]+EX[2,3][i][j])+(F(3,2)*a+b if i==j else 0) for j in range(16)] for i in range(16)]
    piv=[]
    # Exact rational Cholesky/LDL recurrence, distinct from Schur updates.
    L=[[F(i==j) for j in range(16)] for i in range(16)]
    for k in range(16):
        d=matrix[k][k]-sum(L[k][j]**2*piv[j] for j in range(k))
        assert d>0,(a,b,e,k,d)
        piv.append(d)
        for i in range(k+1,16):
            L[i][k]=(matrix[i][k]-sum(L[i][j]*L[k][j]*piv[j] for j in range(k)))/d
    return piv

def action_coefficients(basis,vector,nx,ny):
    """Accumulate H_FF psi and V psi independently on complete rung outputs."""
    n=nx*ny;E=-F(3*n,4);scale=40
    hp=defaultdict(int);vp=defaultdict(int);reached=set(basis)
    for st,amplitude in zip(basis,vector):
        per_h=defaultdict(int);per_v=defaultdict(int)
        per_h[st]+=int(scale*(E+sum(s!=0 for s in st)))
        for (i,j),weight in edges(nx,ny).items():
            local_h=defaultdict(F);local_v=defaultdict(F)
            for a,b in itertools.product(range(2),repeat=2):
                for s,t,value in KERNEL[a,b][st[i],st[j]]:
                    target=st[:i]+(s,)+st[i+1:j]+(t,)+st[j+1:]
                    local_h[target]+=J*value
                    if a==b:local_v[target]+=value
            for target in local_h.keys()|local_v.keys():
                if local_h[target] or local_v[target]:reached.add(target)
                h=scale*weight*local_h[target];v=scale*weight*local_v[target]
                assert h.denominator==v.denominator==1
                per_h[target]+=int(h);per_v[target]+=int(v)
        for target,value in per_h.items():hp[target]+=value*amplitude
        for target,value in per_v.items():vp[target]+=value*amplitude
    metric=lambda st:math.prod(METRIC[s] for s in st)
    norm=sum(metric(st)*a*a for st,a in zip(basis,vector));assert norm>0
    mean=[F(sum(metric(st)*a*z[st] for st,a in zip(basis,vector)),norm*scale) for z in (hp,vp)]
    support=set(hp)|set(vp)
    h2=F(sum(metric(st)*hp[st]**2 for st in support),norm*scale**2)
    hv=F(sum(metric(st)*hp[st]*vp[st] for st in support),norm*scale**2)
    v2=F(sum(metric(st)*vp[st]**2 for st in support),norm*scale**2)
    residual=[h2-mean[0]**2,2*(hv-mean[0]*mean[1]),v2-mean[1]**2]
    assert residual[2]>=0
    # Positive semidefiniteness of the two-operator covariance matrix.
    assert residual[0]>=0 and 4*residual[0]*residual[2]>=residual[1]**2
    return {'mean':mean,'residual':residual,'moments':[h2,2*hv,v2],'norm':norm,'union':len(reached),'nonzero_h':sum(bool(v) for v in hp.values()),'nonzero_v':sum(bool(v) for v in vp.values())}

POLY_RESULTS={}
@lru_cache(None)
def check_polynomial(key,filename):
    saved=read(CAND/filename)[key];nx,ny=saved['geometry'];n=nx*ny
    source=read(ROOT/saved['source_record']);path=ROOT/saved['trial_artifact']
    assert HASHES[saved['source_record']]==saved['source_record_sha256']
    assert sha(path)==saved['trial_artifact_sha256']
    assert path==(ROOT/saved['source_record']).parent/source['trial_artifact']
    with np.load(path,allow_pickle=False) as z:
        basis=[tuple(int(t) for t in st) for st in z['basis']];vector=[int(x) for x in z['vector']]
    assert len(basis)==len(vector)==len(set(basis))==saved['linear_trial_dimension']==source['trial_subspace_dimension']
    assert all(len(st)==n and set(st)<={0,1,2,3} and sum((0,-1,0,1)[s] for s in st)==0 for st in basis)
    assert max(sum(s!=0 for s in st) for st in basis)==2
    assert source['full_dimension']==saved['full_dimension']==4**n and saved['physical_spins']==2*n
    center=F(saved['vector_epsilon'])
    assert key==f'{center}_{nx}x{ny}'
    physical_bonds=Counter({(i,a,j,b):w*(J+(center if a==b else 0)) for (i,j),w in edges(nx,ny).items() for a,b in itertools.product(range(2),repeat=2)})
    assert physical_bonds==Counter({(i,a,j,b):F(c) for i,a,j,b,c in source['weak_bonds']})
    rebuilt=action_coefficients(basis,vector,nx,ny)
    assert rebuilt['mean']==list(map(F,saved['rayleigh_coefficients']))
    assert rebuilt['residual']==list(map(F,saved['residual_squared_coefficients']))
    assert rebuilt['norm']==int(saved['integer_metric_norm'])
    assert rebuilt['union']==saved['full_action_union_dimension']
    assert F(saved['E00'])==-F(3*n,4)
    assert poly(rebuilt['mean'],center)==F(source['exact_rayleigh'])
    assert poly(rebuilt['residual'],center)==F(source['exact_residual_squared'])
    assert occupancy(nx,ny)==Counter({(r['q'],F(r['energy_lower'])):r['multiplicity'] for r in saved['reference_bins']})
    POLY_RESULTS[key]={'geometry':[nx,ny],'center':str(center),'full_dimension':4**n,'trial_dimension':len(basis),'full_action_union':rebuilt['union'],'nonzero_HFF_action':rebuilt['nonzero_h'],'nonzero_V_action':rebuilt['nonzero_v'],'metric_norm':str(rebuilt['norm']),'Rayleigh_coefficients':strs(rebuilt['mean']),'full_second_moment_coefficients':strs(rebuilt['moments']),'full_residual_squared_coefficients':strs(rebuilt['residual']),'source_sha256':saved['source_record_sha256'],'artifact_sha256':saved['trial_artifact_sha256'],'status':'PASS exact polynomial and saved-point contractions'}
    return rebuilt

def reference_check(ref,nx,ny,lo,hi):
    hist=occupancy(nx,ny);n=nx*ny
    assert len(ref['bins'])==len(hist)
    assert hist==Counter({(r['q'],F(r['energy_lower'])):r['multiplicity'] for r in ref['bins']})
    assert F(ref['J'])==J
    a,b=F(ref['a']),F(ref['b']);B=2*n*b
    assert F(ref['B'])==B and hist[0,F(0)]==1
    cut=min(f-4*a*q for q,f in hist if q);assert cut>0
    assert cut-B==F(ref['second_shift_lower'])
    pivots=[local_psd(a,b,e) for e in (lo,hi)]
    return {'hist':hist,'a':a,'B':B,'alpha':-F(3*n,4)+cut-B,'pivots':pivots}

COMBINATIONS={'A':(-2,1,0),'B':(0,-2,1),'J1':(-8,0,2),'J2':(0,-8,4)}
def interval_inputs(record,polynomial_file):
    lo,hi=map(F,record['epsilon_interval']);assert 0<=lo<=hi
    rows=[]
    assert [r['geometry'] for r in record['ground_records']]==[[2,2],[4,2],[4,4]]
    for r in record['ground_records']:
        nx,ny=r['geometry']
        assert r['polynomial_key']==f"{F(record['vector_epsilon'])}_{nx}x{ny}"
        co=check_polynomial(r['polynomial_key'],polynomial_file)
        rho,variance=co['mean'],co['residual'];ref=reference_check(r['reference_certificate'],nx,ny,lo,hi)
        assert rho==list(map(F,r['rayleigh_coefficients']))
        re=[poly(rho,e) for e in (lo,hi)];ve=[poly(variance,e) for e in (lo,hi)]
        assert min(ve)>=0 and strs(re)==r['rayleigh_endpoint_values'] and strs(ve)==r['residual_squared_endpoint_values']
        U=max(re);v=max(ve);alpha=ref['alpha'];assert alpha>U
        delta=v/(alpha-U)
        assert U==F(r['rayleigh_max']) and v==F(r['residual_squared_max'])
        assert alpha==F(r['uniform_second_eigenvalue_lower']) and delta==F(r['uniform_Temple_correction'])
        assert F(r['E00'])==-F(3*nx*ny,4)
        for endpoint,pivots in zip(r['endpoint_local_PSD'],ref['pivots']):
            assert endpoint['exact_positive_LDL_pivots']==strs(pivots)
        assert [F(ep['epsilon']) for ep in r['endpoint_local_PSD']]==[lo,hi]
        rows.append({**ref,'rho':rho,'U':U,'delta':delta,'E':F(r['E00'])})
    maxima={}
    for label,weights in COMBINATIONS.items():
        c=[sum(w*r['rho'][k] for w,r in zip(weights,rows)) for k in range(2)]
        values=[poly(c,e) for e in (lo,hi)];maximum=max(values)
        s=record['correlated_energy_combinations'][label]
        assert s['weights']==list(weights) and s['affine_coefficients']==strs(c) and s['endpoint_values']==strs(values) and F(s['maximum'])==maximum
        maxima[label]=maximum
    return rows,maxima

def heat_inputs(rows,maxima,beta):
    q=[]
    for r in rows:
        tail=sum(mult*exp_interval(-beta*(r['E']+f-4*r['a']*occ-r['B']-r['U']))[1] for (occ,f),mult in r['hist'].items() if occ)
        q.append(exp_interval(beta*r['delta'])[1]+tail)
    values={k:exp_interval(-beta*maxima[k])[0]/q[i]**power for k,i,power in [('A',0,2),('B',1,2),('J1',0,8),('J2',1,8)]}
    values['C']=1/q[2]**2
    return values,q

def G(x):
    assert 0<x<=1
    return 1-F(1,2)*(1/x-1)**2

def replay(seed,values):
    initial={k:F(seed[k+'_lower']) for k in values}
    assert all(0<initial[k]<=values[k]<=1 for k in values)
    a=lower(G(initial['J1']),128)
    b=lower(G(initial['J2']*a),128)
    c=lower(G(initial['C']**4*a*a*b),128)
    assert min(a,b,c)>0
    states=[[initial[k] for k in ['A','B','C']],[a,b,c]]
    beta=2*F(seed['beta']);n=4;updates=[]
    while max(1-a,1-b,1-c)>F(1,500):
        for _ in range(3):
            a,b,c=b,c,lower(G(a**4*b*b*c),128)
            assert min(a,b,c)>0
        states.append([a,b,c]);updates.append(strs((a,b,c)));n*=2;beta*=2
        assert len(updates)<65
    u=max(1-a,1-b,1-c);boot=seed['bootstrap'];g=F(boot['gap_lower'])
    assert boot['accepted'] and boot['rounds']==len(updates) and n==boot['n']==boot['m']
    assert F(boot['beta'])==beta and boot['updates']==updates and F(boot['u'])==u and boot['purities']==strs((a,b,c))
    assert 0<u<=F(1,500) and exp_interval(beta*g)[1]<1/(32*u)
    return states,n,g

# An independently implemented finite-window lemma with the exact saved 40-
# decimal floor convention; no imported finite_window_2d routine is used.
DEC=10**40
def sqrt_down(x):
    assert x>=0
    root=math.isqrt((x.numerator*DEC**2)//x.denominator)
    assert root**2*x.denominator<=x.numerator*DEC**2<(root+1)**2*x.denominator
    return F(root,DEC)
def interval_purity(s,t):
    assert 0<s<=1 and 0<t<=1 and s*s*t>F(1,2)
    w=(1+sqrt_down(2*s*s*t-1))/2
    r=(1-w)/w;d=t/(1+r*r)
    result=(1-r)*min(s*sqrt_down(d),d)
    return F(result.numerator*DEC//result.denominator,DEC)
def window_purity(a,b,c):
    assert F(1,2)<b<=1 and 0<a<=1 and 0<c<=1
    spatial=a*a*sqrt_down(2*b-1)
    transverse=interval_purity(b,c)
    return interval_purity(spatial,transverse)

def audit_selected(selected):
    source=ROOT/selected['source'];records=read(source);r=records[selected['source_index']]
    assert selected['epsilon_interval']==r['epsilon_interval']
    assert selected['vector_epsilon']==r['vector_epsilon']
    pf=source.stem.replace('_certificates','_polynomials')+'.json'
    rows,maxima=interval_inputs(r,pf);s=r['seed'];beta=F(s['beta'])
    values,qs=heat_inputs(rows,maxima,beta)
    assert all(F(stored)>=computed for stored,computed in zip(s['uniform_shifted_trace_uppers'],qs))
    states,n,asym=replay(s,values);windows=[]
    assert F(selected['initial_beta'])==beta and selected['asymptotic_entry_side']==n
    assert len(s['all_integer_finite_windows'])==len(states)-1
    for j,w in enumerate(s['all_integer_finite_windows']):
        side=2**(j+1);temperature=beta*2**j;state=states[j]
        assert w['n']==side and w['through']==2*side and F(w['beta'])==temperature and w['purities']==strs(state)
        purity=window_purity(*state)
        assert purity==F(w['uniform_thermal_lower']) and purity>F(1,2)
        gap=F(w['uniform_gap_lower'])
        assert gap>0 and exp_interval(temperature*gap)[1]*(1-purity)<purity
        windows.append({'from':side,'through':2*side,'beta':str(temperature),'purity':str(purity),'gap':str(gap)})
    assert windows[0]['from']==2 and windows[-1]['through']==n
    assert all(left['through']==right['from'] for left,right in zip(windows,windows[1:]))
    gap=min([asym]+[F(w['gap']) for w in windows])
    assert gap==F(s['uniform_all_integer_L_ge2_gap'])==F(selected['uniform_gap'])
    assert all(F(w['gap'])>asym for w in windows)
    result={'epsilon_interval':r['epsilon_interval'],'vector_epsilon':r['vector_epsilon'],'initial_beta':str(beta),'asymptotic_entry':n,'uniform_gap':str(gap),'gap_decimal':format(float(gap),'.15g'),'window_count':len(windows),'finite_windows':windows,'correlated_energy_maxima':{k:str(v) for k,v in maxima.items()},'independent_shifted_trace_uppers':strs(qs),'status':'PASS full physical polynomial, uniform reference, 224-bit heat, exact recursion, every integer finite window'}
    print(json.dumps({k:result[k] for k in ('epsilon_interval','uniform_gap','asymptotic_entry','status')}),flush=True)
    return result

def audit_baseline(selected):
    path=ROOT/selected['source'];records=read(path)
    r=next(x for x in records if x['epsilon_interval']==selected['epsilon_interval'])
    lo,hi=map(F,r['epsilon_interval']);assert lo==0
    rows=[]
    for record in r['uniform_ground_records']:
        nx,ny=record['nx'],record['ny'];n=nx*ny;E=-F(3*n,4)
        ref=reference_check(record['reference_certificate'],nx,ny,lo,hi)
        co=action_coefficients([(0,)*n],[1],nx,ny)
        assert co['mean']==[E,F(0)] and co['residual']==[F(0),F(0),F(3,4)*sum(w*w for w in edges(nx,ny).values())]
        delta=poly(co['residual'],hi)/(ref['alpha']-E)
        assert F(record['ground_upper'])==E and F(record['ground_lower'])==E-delta
        rows.append({**ref,'rho':[E,F(0)],'U':E,'delta':delta,'E':E})
    raw=next(x for x in r['seeds'] if x['seed']['beta']==r['best_beta'])
    seed=raw['seed'];values,qs=heat_inputs(rows,{k:F(0) for k in COMBINATIONS},F(seed['beta']))
    states,n,asym=replay(seed,values)
    b=raw['uniform_bridge'];a=F(b['a']);bb=F(b['b']);assert 0<=a<F(1,16) and bb>0
    local_psd(a,bb,lo);local_psd(a,bb,hi)
    levels=[(q,F(1) if q==1 else q-J*(min(2*q,q*q//4)+F(q,2))) for q in range(1,9)]
    assert [[q,str(e)] for q,e in levels]==b['reference_levels']
    cutoff=min(e-4*a*q for q,e in levels)
    assert cutoff==F(b['cutoff']) and b['worst_L']==n-1
    large=cutoff-2*(n-1)**2*bb;small=[F(2,5)-12*hi,F(1)-27*hi]
    assert large==F(b['large_square_bridge']) and b['small']==[[2,str(small[0])],[3,str(small[1])]]
    bridge=min(large,*small);assert bridge==F(b['bound'])
    gap=min(asym,bridge)
    assert gap==F(raw['uniform_all_integer_L_ge2_gap'])==F(r['best_uniform_all_sizes_gap'])==F(selected['uniform_gap'])
    return {'epsilon_interval':r['epsilon_interval'],'uniform_gap':str(gap),'asymptotic_entry':n,'short_size_minimum':str(bridge),'status':'PASS fresh full-vacuum action, reference, heat, recursion and analytic short-size bridge replay'}

def main():
    summary=read(CAND/'coverage_summary.json');chosen=summary['selected_intervals']
    baseline=audit_baseline(chosen[0])
    results=[audit_selected(s) for s in chosen[1:]]
    union=[baseline]+results;end=F(0)
    for r in union:
        lo,hi=map(F,r['epsilon_interval']);assert lo==end and hi>lo;end=hi
    assert end==F(171,20000)
    common=min(F(r['uniform_gap']) for r in union)
    through_85=min(F(r['uniform_gap']) for r in union if F(r['epsilon_interval'][1])<=F(17,2000))
    assert common==F(summary['uniform_gap']) and through_85==F(summary['uniform_gap_on_0_through_17_over_2000'])
    assert common>F('0.000768515509') and through_85>F('0.001703099464')
    assert summary['coverage_union']==[['0','171/20000']] and summary['gaps_inside_union']==[]
    for name in ['BASELINE_PROOF.md','EPSILON_FRONTIER.md','INTERVAL_INDEPENDENT_REVIEW.md']:
        sha(BASE/name)
    for name in ['FINITE_WINDOW_INTERPOLATION.md','INTERPOLATION_DOMAIN.md']:
        sha(ROOT/'research_20261010/root_review'/name)
    sha(CAND/'PROOF.md');sha(CAND/'extend_interval.py')
    for name,h in HASHES.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    result={'status':'PASS independent complete continuum certificate audit','model':'unit-rung spin-1/2 square bilayer, J=3/10, straight J+epsilon, crossed J; positive-direction periodic multiplicities','parameter_interval':['0','171/20000'],'integer_square_sides':'every L>=2','unique_finite_volume_ground_state':True,'uniform_gap':str(common),'uniform_gap_decimal_strict_lower':'0.000768515509','uniform_gap_through_17_over_2000':str(through_85),'stronger_decimal_strict_lower':'0.001703099464','baseline':baseline,'intervals':results,'physical_polynomials':POLY_RESULTS,'input_hashes':HASHES,'dependencies':'Analytic weighted-star and real self-adjoint thermal-transfer/interpolation proofs; no imported producer arithmetic or project modules. Fresh physical/scalar reconstruction in this script.','resource_use':{'seconds':time.monotonic()-START,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cpu_threads':1},'unchanged_input_hashes_verified':True}
    (OUT/'audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'uniform_gap':str(common),'uniform_gap_through_17_over_2000':str(through_85),'resource_use':result['resource_use']}),flush=True)
if __name__=='__main__':main()
