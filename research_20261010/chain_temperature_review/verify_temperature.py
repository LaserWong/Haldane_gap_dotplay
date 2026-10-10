"""Independent temperature-first chain certificate audit.
No producer mathematical modules. Physical kernel and certified exponentials
are inherited by pinned hash from the earlier independent chain reviewer.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import json,hashlib,math,sys,time,resource,shutil
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PRODUCER=HERE.parent/'chain_temperature_first'
OLD=HERE.parent/'chain_frontier_review'
DATA=HERE.parent/'chain_frontier'
T0=time.monotonic()
INPUT={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    INPUT[str(p.relative_to(ROOT))]=sha(p)
    return json.loads(p.read_text())
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
# The inherited complete review is immutable and verified before imports.
manifest=read(OLD/'SHA256SUMS.json')
for name,digest in manifest.items():assert sha(OLD/name)==digest,('old review drift',name)
assert manifest['independent_core.py']=='30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19'
sys.path.insert(0,str(OLD))
import independent_core as C
# The inherited core imposes 1 GiB AS, below this audit's 1.5 GiB ceiling.
assert resource.getrlimit(resource.RLIMIT_AS)[0]<=1500*1024**2
sealed_inputs=read(OLD/'INPUT_SHA256SUMS.json')
for name,digest in sealed_inputs.items():assert sha(DATA/name)==digest,('old physical input drift',name)
for rel,digest in read(OLD/'PROVENANCE.json')['prior_independent_sources'].items():assert sha(ROOT/rel)==digest
save('INHERITED_PROVENANCE.json',dict(prior_review_manifest_sha256=sha(OLD/'SHA256SUMS.json'),
    prior_review_files_verified=len(manifest),prior_physical_inputs_verified=len(sealed_inputs),
    independent_core_sha256=sha(OLD/'independent_core.py'),prior_analytic_sources=read(OLD/'PROVENANCE.json')['prior_independent_sources']))

# Minimal affine Rayleigh reconstruction. Only matrix elements returning to the
# trial support contribute to v^* H v; no claim is made about H v or residuals.
def affine_rayleigh(path,N):
    import numpy as np
    INPUT[str(path.relative_to(ROOT))]=sha(path)
    z=np.load(path,allow_pickle=False)
    basis=[tuple(map(int,s)) for s in z['basis']];vector=[int(x) for x in z['vector']]
    assert len(set(basis))==len(basis)==len(vector)
    assert all(len(s)==N and all(0<=d<9 for d in s) and sum(C.MAG[d] for d in s)==0 for s in basis)
    values=dict(zip(basis,vector));weighted={s:v*math.prod(C.W[d] for d in s) for s,v in zip(basis,vector)}
    norm=sum(weighted[s]*v for s,v in zip(basis,vector));assert norm>0
    h0=sum(weighted[s]*v*(-2*N+sum(C.EX[d] for d in s)) for s,v in zip(basis,vector))
    scale=math.lcm(*(c.denominator for row in C.K.values() for _,_,c in row))
    kernel={key:[(a,b,int(c*scale)) for a,b,c in row] for key,row in C.K.items()}
    weak=0
    edges=[((j-1)%N,j) for j in range(N)]
    # At N=2 these are the two oppositely oriented, distinct physical links.
    assert len(edges)==N and all(sum(i==v or j==v for i,j in edges)==2 for v in range(N))
    for s,v in zip(basis,vector):
        for i,j in edges:
            for a,b,c in kernel[s[i],s[j]]:
                t=list(s);t[i]=a;t[j]=b
                weak+=weighted.get(tuple(t),0)*c*v
    return dict(N=N,dimension=len(vector),full_dimension=9**N,physical_sites=2*N,
        norm=str(norm),H0_expectation=str(Q(h0,norm)),weak_unit_expectation=str(Q(weak,scale*norm)),
        source=str(path.relative_to(ROOT)),sha256=sha(path),periodic_edge_multiset=edges,
        contract='Exact Rayleigh polynomial only; no residual, isolation, or retained-band count.')

def evaluate(a,g):return Q(a['H0_expectation'])+g*Q(a['weak_unit_expectation'])

def ground_input(r,source,tag):
    assert r['s']=='1' and r['N_dimers']==4 and r['physical_sites']==8 and r['full_dimension']==9**4
    assert Q(r['relative_form_bound']['local_certificate']['coupling'])==Q(source['g'])
    if tag in ('13d80','7d40'):
        file='chain_sparse_s1_g13d80_n4_depth4_obstruction_independent_review.json' if tag=='13d80' else 'g7d40_obstruction_independent_review.json'
        prior=read(OLD/file)['ground_checks'][0]
        assert prior['N_dimers']==4 and prior['rayleigh_identical'] and prior['entire_residual_identical'] and prior['Temple_interval_identical']
        assert sha(DATA/r['trial_artifact'])==prior['source_sha256']==sealed_inputs[r['trial_artifact']]
        result=dict(mode='Previously sealed complete physical input reused by hash',prior_review=file,check=prior)
    else:
        result=dict(mode='New independent complete physical reconstruction',check=C.check_ground(r))
        INPUT[str((DATA/r['trial_artifact']).relative_to(ROOT))]=sha(DATA/r['trial_artifact'])
    # Independent full-bin count and normalization checks also apply to reused inputs.
    bins=Counter({0:1})
    for _ in range(4):
        out=Counter()
        for e,m in bins.items():
            for f,d in [(0,1),(1,3),(3,5)]:out[e+f]+=m*d
        bins=out
    assert sum(bins.values())==9**4 and bins[0]==1 and bins[1]==12
    rb=r['relative_form_bound'];lc=rb['local_certificate'];a,b=Q(lc['a']),Q(lc['b'])
    assert Q(rb['alpha'])==1-2*a>0 and Q(rb['B'])==4*b and Q(r['E00'])==-8
    cutoff=-8+1-2*a-4*b
    assert Q(r['second_eigenvalue_lower'])==cutoff>Q(r['exact_rayleigh'])
    assert Q(r['ground_upper'])==Q(r['exact_rayleigh'])
    assert Q(r['ground_lower'])==Q(r['exact_rayleigh'])-Q(r['exact_residual_squared'])/(cutoff-Q(r['exact_rayleigh']))
    result['full_reference_bins']=sorted(bins.items())
    return result

def purification(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)

def sqrt_lower(x,digits=60):
    scale=10**digits;k=math.isqrt(x.numerator*scale*scale//x.denominator)
    a=Q(k,scale);assert a*a<=x<(a+Q(1,scale))**2
    return a

def interpolate(S,T):
    assert 0<S<=1 and 0<T<=1 and S*S*T>Q(1,2)
    root=sqrt_lower(2*S*S*T-1);w=(1+root)/2;r=(1-w)/w;D=T/(1+r*r)
    rootD=sqrt_lower(D);p=(1-r)*min(S*rootD,D)
    return p,dict(P=str(S*S*T),root_lower=str(root),weight_lower=str(w),tail_ratio_upper=str(r),D_lower=str(D),sqrt_D_lower=str(rootD),purity_lower=str(p))

# This signature deliberately permits only one quantity from the largest seed.
def audit_cycle(small,rho8,row):
    beta=Q(row['beta']);assert beta>0
    q1,_=C.trace_bound(small,beta);q2,_=C.trace_bound(small,2*beta)
    assert q1<=Q(row['small_Q_beta_upper']) and q2<=Q(row['small_Q_2beta_upper'])
    shift=rho8-2*Q(small['ground_upper']);assert shift==Q(row['Rayleigh_shift'])
    L=C.exp_bounds(-2*beta*shift)[0]
    J=Q(row['J_lower']);C0=Q(row['C_lower'])
    assert 0<J<=1 and 0<C0<=1
    assert J<=L/q1**4 and C0<=L/q2**2
    a=C.floor(purification(J));b=C.floor(purification(C0*C0*a)) if a>0 else Q(-1)
    assert [a,b]==list(map(Q,row['time_first']))
    result=dict(beta=str(beta),exact_trace_and_Rayleigh_ratios_verified=True,
        independently_rebuilt_first_cycle=list(map(str,[a,b])))
    if b<=0:
        assert row['status']=='nonpositive_first_cycle'
        return dict(**result,accepted=False,status='finite tested point nonpositive')
    savedroot=Q(row['sqrt_b_lower']);assert savedroot**2<=b<(savedroot+Q(1,10**40))**2
    S=C.floor(a*savedroot);T=C.floor(a*a*b)
    assert [S,T]==[Q(row['canonical_S']),Q(row['canonical_T'])]
    assert S<=a*sqrt_lower(b) and 0<S<=1 and 0<T<=1
    rep=C.bootstrap(S,T,8,2*beta);saved=row['bootstrap']
    assert rep['status']==saved['status'] and rep['updates']==saved['updates']
    assert saved['input']==dict(S_lower=str(S),T_lower=str(T),n=8,beta=str(2*beta))
    result.update(canonical_base=dict(n=8,beta=str(2*beta)),canonical_pair=[str(S),str(T)],updates=rep['updates'])
    if not rep['status'].startswith('accepted'):
        assert row['status']=='scalar_rejected'
        return dict(**result,accepted=False,status=rep['status'])
    n=rep['n'];bb=Q(rep['beta']);u=max(Q(rep['p']),Q(rep['q']));gap=Q(saved['conditional_gap_lower_rational'])
    assert n==saved['final_n'] and str(bb)==saved['final_beta'] and u==Q(saved['final_common_u'])
    assert u<=Q(1,100) and C.exp_bounds(bb*gap)[1]*5*u<1
    states=[(S,T)]+[(1-Q(x['p_upper']),1-Q(x['q_upper'])) for x in rep['updates']]
    assert len(row['windows'])==len(rep['updates'])
    nn=8;be=2*beta;windows=[]
    for st,win in zip(states,row['windows']):
        assert win['cells']==[nn,2*nn] and Q(win['beta'])==be
        assert list(st)==[Q(win['S']),Q(win['T'])]
        p,details=interpolate(*st);sP=Q(win['thermal_lower']);d=Q(win['gap_lower'])
        assert Q(1,2)<sP<=p and d>0 and C.exp_bounds(be*d)[1]*(1-sP)<sP
        windows.append(dict(cells=[nn,2*nn],beta=str(be),gap_lower=str(d),independent=details))
        nn*=2;be*=2
    assert nn==n and be==bb
    combined=min([gap]+[Q(w['gap_lower']) for w in windows])
    assert combined==Q(row['M_ge8_gap'])
    result.update(accepted=True,status='PASS all integer M>=8',windows=windows,asymptotic_from=n,
        asymptotic_beta=str(bb),asymptotic_gap=str(gap),common_defect=str(u),M_ge8_gap=str(combined))
    return result

M7=None
M6=None
def short_bridge(g,saved):
    global M7,M6
    local=saved['local_comparison'];lc=local['local_certificate']
    assert Q(lc['coupling'])==g
    psd=C.local_psd(lc);a,b=Q(lc['a']),Q(lc['b']);alpha=1-2*a
    assert alpha>0 and b>=0 and Q(local['alpha'])==alpha and Q(local['B'])==7*b
    assert Q(local['second_shift_lower'])==alpha-7*b
    if M7 is None:M7=affine_rayleigh(DATA/'chain_s1_M7_g129d800_depth2_trial.npz',7)
    affine=saved['affine_M7_trial']
    assert all(affine[k]==M7[k] for k in affine)
    # The old optimized coupling is only a cross-check: the new coupling is
    # reevaluated from the exact affine polynomial, never copied as a rho.
    old=read(DATA/'chain_s1_M7_g129d800_depth2_ground.json')
    assert evaluate(M7,Q(129,800))==Q(old['exact_rayleigh'])
    rows=[]
    for M,row in zip(range(2,8),saved['rows']):
        assert row['M']==M
        if M==7:rho=evaluate(M7,g);assert row['trial_source']==M7['source'] and row['trial_source_sha256']==M7['sha256']
        elif M==6 and g==Q(7,40):
            source=ROOT/row['trial_source'];r=read(source);assert sha(source)==row['trial_source_sha256']
            assert r['N_dimers']==6 and Q(r['relative_form_bound']['local_certificate']['coupling'])==g
            if M6 is None:M6=affine_rayleigh(DATA/r['trial_artifact'],6)
            rho=evaluate(M6,g);assert rho==Q(r['exact_rayleigh'])<-2*M
        else:
            rho=Q(-2*M);assert row['trial_source']=='singlet product' and row['trial_source_sha256'] is None
        cutoff=-2*M+alpha-M*b;gap=cutoff-rho
        assert gap>0 and [cutoff,rho,gap]==[Q(row[k]) for k in ['cutoff_lower','trial_rayleigh','gap_lower']]
        rows.append(dict(M=M,physical_sites=2*M,full_dimension=9**M,second_eigenvalue_cutoff=str(cutoff),trial_rayleigh=str(rho),gap_lower=str(gap)))
    assert len(saved['rows'])==6
    gap=min(Q(r['gap_lower']) for r in rows);assert gap==Q(saved['gap_lower'])
    return dict(new_local_exact_LDL=psd,full_space_cutoffs_rebuilt=True,rows=rows,gap_lower=str(gap),M7_affine=M7,M6_rayleigh=M6 if g==Q(7,40) else None)

# Formal partition monomials, independent of numerical data.
def mul(*exprs):
    out=Counter()
    for e in exprs:
        for k,v in e.items():out[k]+=v
    return {k:v for k,v in out.items() if v}
def powe(e,k):return {x:y*k for x,y in e.items()}
def P(i,w):
    z=list(w);z[i]+=1
    return {tuple(z):1,w:-2}
def symbolic_ledger():
    v=(0,0);w=(1,1);dx=(1,0);dt=(0,1)
    J={w:1,v:-4};C0=P(0,dt)
    assert J==mul(powe(P(0,v),2),P(1,dx))==mul(powe(P(1,v),2),C0)
    first_a=P(1,w);first_b=P(0,(1,2))
    assert mul(powe(C0,2),first_a)==mul(powe(P(1,dt),2),P(0,(0,2)))
    swap_c=P(0,w);swap_e=P(1,(2,1))
    assert mul(powe(swap_c,2),swap_e)==mul(powe(first_a,2),first_b)
    out=dict(coordinates='(log2 spatial length relative to n=4, log2 inverse temperature relative to beta)',
        initial_base=v,post_cycle_base=w,post_cycle_physical_base='(8,2 beta)',
        first_cycle_order=['time','space'],canonical_order=['space','time'],
        original_edges=[{'axis':'time','base':w},{'axis':'space','base':(1,2)}],
        swapped_edges=[{'axis':'space','base':w},{'axis':'time','base':(2,1)}],
        identities=['J=P_x(v)^2 P_t(D_x v)=P_t(v)^2 P_x(D_t v)',
            'C^2 P_t(w)=P_t(D_t v)^2 P_x(D_t^2 v)',
            'P_x(w)^2 P_t(D_x w)=P_t(w)^2 P_x(D_t w)'],
        verified=True)
    save('PATH_LEDGER.json',out)


def main():
    symbolic_ledger()
    freeze=PRODUCER/'FROZEN_MANIFEST.json'
    if not freeze.exists():raise RuntimeError('Producer freeze not yet available')
    assert sha(freeze)=='2aed748169de52b5a2acce733abecbeb491f309229545404295b38262f0cc915'
    pinned=read(freeze)
    if 'files' in pinned:pinned=pinned['files']
    for name,digest in pinned.items():
        assert sha(PRODUCER/name)==digest,('producer freeze mismatch',name)
        destination=HERE/'snapshot'/name;destination.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(PRODUCER/name,destination)
    shutil.copyfile(freeze,HERE/'PRODUCER_FROZEN_MANIFEST.json')
    producer_inputs=read(HERE/'snapshot'/'INPUT_SHA256.json')
    for rel,digest in producer_inputs.items():
        assert sha(ROOT/rel)==digest,('producer input drift',rel)
        INPUT[rel]=digest
    outcomes=[]
    for tag in ['323d2000','13d80','7d40','1d5']:
        r=read(HERE/'snapshot'/f'candidate_g{tag}.json');g=Q(r['g'])
        assert r['source']==f'research_20261010/chain_frontier/chain_sparse_s1_g{tag}_n4_depth4.json'
        source=read(ROOT/r['source']);assert sha(ROOT/r['source'])==r['source_sha256']
        assert Q(source['g'])==g and source['n']==4
        small,big=source['ground_certificates'];assert r['small_input']==small
        assert r['large_input']=={'exact_rayleigh':big['exact_rayleigh']}
        assert big['N_dimers']==8 and big['s']=='1' and big['physical_sites']==16 and big['full_dimension']==9**8
        assert Counter(tuple(b) for b in big['weak_bonds'])==Counter(((j-1)%8,1,j,0,str(g)) for j in range(8))
        small_check=ground_input(small,source,tag)
        # Replay just the largest Rayleigh quotient even when a sealed full
        # certificate exists. This independently verifies the reduced contract.
        large=affine_rayleigh(ROOT/r['large_trial_path'],8);rho8=evaluate(large,g)
        assert rho8==Q(big['exact_rayleigh'])==Q(r['large_input']['exact_rayleigh'])
        assert large['dimension']==r['large_trial_dimension']==big['trial_subspace_dimension']
        assert large['full_dimension']==r['large_full_dimension']
        print('PHYSICAL INPUT PASS',str(g),flush=True)
        rows=[audit_cycle(small,rho8,row) for row in r['rows']]
        accepted=[x for x in rows if x['accepted']]
        bridge=short_bridge(g,r['short_bridge']) if accepted else None
        for row,saved in zip(rows,r['rows']):
            if row['accepted']:
                gap=min(Q(row['M_ge8_gap']),Q(bridge['gap_lower']))
                assert gap==Q(saved['all_M_ge2_gap']);row['all_M_ge2_gap']=str(gap)
        if accepted:
            best=max(accepted,key=lambda x:Q(x['all_M_ge2_gap']))
            assert best['beta']==r['best']['beta'] and best['all_M_ge2_gap']==r['best']['all_M_ge2_gap']
            status='PASS independent exact all-integer M>=2 certificate'
        else:
            best=None;assert r['best'] is None and r['short_bridge'] is None
            status='PASS replay of bounded failed scan only; no obstruction conclusion'
        result=dict(status=status,g=str(g),small_physical_input=small_check,largest_Rayleigh_only=large,
            largest_consumed_energy_quantities=['exact_rayleigh'],largest_residual_or_count_used=False,
            rows=rows,short_bridge=bridge,best=best)
        save('review_g'+tag+'.json',result)
        outcomes.append(dict(g=str(g),status=status,gap=None if best is None else best['all_M_ge2_gap'],
            beta=None if best is None else best['beta'],asymptotic_from=None if best is None else best['asymptotic_from'],
            smallest_short_gap=None if bridge is None else bridge['gap_lower']))
        print('CANDIDATE REVIEW',outcomes[-1],flush=True)
    save('SUMMARY.json',dict(status='PASS',results=outcomes,seconds=time.monotonic()-T0,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,CPU_affinity=sorted(os.sched_getaffinity(0)),
        BLAS_threads=1,address_space_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],
        large_ED_used=False,producer_manifest_sha256=sha(freeze),verifier_sha256=sha(Path(__file__))))
    save('INPUT_SHA256SUMS.json',INPUT)
    print(json.dumps(outcomes,indent=2),flush=True)
if __name__=='__main__':main()
