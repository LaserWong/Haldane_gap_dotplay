"""Independent exact audit of alternating spin-one sparse-support certificates.

No imports from low_energy, audit, or the archived scalar programs. Floating
point is used only for human-readable displays; proof tests are rational.
Run with PYTHONDONTWRITEBYTECODE=1 and single-thread BLAS.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
DATA = BASE / 'research_20261010' / 'chain_frontier'
START = time.monotonic()
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))

# Physical order |m_left,m_right>, m=-1,0,+1. Columns, with their
# unnormalised Clebsch-Gordan coefficients explicitly specified.
V = [
    [0,0,1,0,-1,0,1,0,0],
    [0,-1,0,1,0,0,0,0,0],
    [0,0,-1,0,0,0,1,0,0],
    [0,0,0,0,0,-1,0,1,0],
    [1,0,0,0,0,0,0,0,0],
    [0,1,0,1,0,0,0,0,0],
    [0,0,1,0,2,0,1,0,0],
    [0,0,0,0,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,1],
]
W = [sum(x*x for x in v) for v in V]
EX = [0,1,1,1,3,3,3,3,3]
MAG = [0,-1,0,1,-2,-1,0,1,2]
assert W == [3,2,2,2,1,2,6,2,1]
assert all(sum(x*y for x,y in zip(V[i],V[j])) == (W[i] if i==j else 0)
           for i in range(9) for j in range(9))


def physical_dimer_action(v):
    out = [0]*9
    for c,a in enumerate(v):
        i,j=divmod(c,3)
        out[c] += (i-1)*(j-1)*a
        if i<2 and j>0: out[c+2] += a
        if i>0 and j<2: out[c-2] += a
    return out


assert all(physical_dimer_action(v)==[(e-2)*x for x in v]
           for v,e in zip(V,EX))


def spin_operator(site, name):
    physical = [[0]*9 for _ in range(9)]
    for c in range(9):
        d=list(divmod(c,3)); v=d[site]
        if name=='z': physical[c][c]=v-1
        elif name=='+' and v<2:
            d[site]+=1;physical[3*d[0]+d[1]][c]=1
        elif name=='-' and v>0:
            d[site]-=1;physical[3*d[0]+d[1]][c]=1
    return [[Q(sum(V[r][i]*physical[i][j]*V[c][j]
                   for i in range(9) for j in range(9)),W[r])
             for c in range(9)] for r in range(9)]


OPS={(site,name):spin_operator(site,name) for site in (0,1) for name in ('z','+','-')}
K={}
for c in range(9):
    for d in range(9):
        row=[]
        for r in range(9):
            for s in range(9):
                a=(OPS[1,'z'][r][c]*OPS[0,'z'][s][d]
                   + OPS[1,'+'][r][c]*OPS[0,'-'][s][d]
                   + OPS[1,'-'][r][c]*OPS[0,'+'][s][d])
                if a: row.append((r,s,a))
        K[c,d]=row
# Ladder factors: for spin one, S+ = sqrt(2)*the unit raising matrix,
# so the usual 1/2 in S+ S- + S- S+ cancels exactly.


def floor(x,digits=12):
    return Q(x.numerator*10**digits//x.denominator,10**digits)


def ceil(x,digits=12):
    return -floor(-x,digits)


def exp_positive(x):
    """Positive Taylor sum with exact geometric tail, after range reduction."""
    assert x>=0
    power=0
    while x>Q(1,8):
        x/=2;power+=1
    term=Q(1);lo=Q(1)
    for k in range(1,81):
        term=term*x/k;lo+=term
    hi=lo+term*x/81/(1-x/82)
    for _ in range(power):
        lo=floor(lo*lo,80);hi=ceil(hi*hi,80)
    return lo,hi


def exp_at(x):
    if x<0:
        lo,hi=exp_positive(-x)
        return 1/hi,1/lo
    return exp_positive(x)


def exp_bounds(x):
    # This outward compression is independent of the producer's algorithm.
    return exp_at(floor(Q(x),50))[0],exp_at(ceil(Q(x),50))[1]


def positive_ldl(matrix):
    """Unpivoted exact LDL; strictly positive pivots prove positive definite."""
    A=[[Q(x) for x in row] for row in matrix]
    assert all(A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A)))
    pivots=[]
    for k in range(len(A)):
        p=A[k][k];assert p>0,(k,p)
        pivots.append(p)
        for i in range(k+1,len(A)):
            for j in range(i,len(A)):
                A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[j][k]/p
    return pivots


LOCAL_CACHE={}
def local_psd(lc):
    a,b,g=map(Q,(lc['a'],lc['b'],lc['coupling']))
    key=(a,b,g)
    if key in LOCAL_CACHE:return LOCAL_CACHE[key]
    t=time.monotonic()
    assert lc['spin']=='1' and lc['kind']=='single' and lc['local_dimension']==81
    # Reconstruct the congruent weighted physical matrix, not producer inertia.
    A=[[Q(0)]*81 for _ in range(81)]
    for c in range(9):
        for d in range(9):
            j=9*c+d
            A[j][j]=(a*(EX[c]+EX[d])+b)*W[c]*W[d]
            for r,s,v in K[c,d]:A[9*r+s][j]+=g*v*W[r]*W[s]
    assert all(A[i][j]==A[j][i] for i in range(81) for j in range(81))
    blocks=[]
    for magnetization in range(-4,5):
        ids=[i for i in range(81) if MAG[i//9]+MAG[i%9]==magnetization]
        assert all(A[i][j]==0 for i in ids for j in range(81) if j not in ids)
        pivots=positive_ldl([[A[i][j] for j in ids] for i in ids])
        blocks.append(dict(magnetization=magnetization,dimension=len(ids),
                           pivots=[str(p) for p in pivots]))
    report=dict(a=str(a),b=str(b),g=str(g),method='independent exact rational LDL in physical magnetization blocks',
                blocks=blocks,positive_pivots=81,seconds=time.monotonic()-t)
    LOCAL_CACHE[key]=report
    return report


def check_ground(rec):
    t=time.monotonic();N=rec['N_dimers']
    assert rec['s']=='1' and rec['full_dimension']==9**N and rec['physical_sites']==2*N
    path=DATA/rec['trial_artifact'];z=np.load(path,allow_pickle=False)
    basis=[tuple(map(int,row)) for row in z['basis']]
    vec=list(map(int,z['vector']))
    assert len(set(basis))==len(basis)==len(vec)==rec['trial_subspace_dimension']
    assert all(len(st)==N and all(0<=x<9 for x in st) and sum(MAG[x] for x in st)==0 for st in basis)
    assert max(sum(x!=0 for x in st) for st in basis)==rec['trial_max_excited_dimers']
    rb=rec['relative_form_bound'];lc=rb['local_certificate'];g=Q(lc['coupling'])
    edges=[(i,aa,j,bb,Q(v)) for i,aa,j,bb,v in rec['weak_bonds']]
    expected=[((i-1)%N,1,i,0,g) for i in range(N)]
    assert Counter(edges)==Counter(expected) and N>=2
    scale=math.lcm(*( (g*v).denominator for row in K.values() for _,_,v in row))
    integer_kernel={key:[(i,j,int(scale*g*v)) for i,j,v in row] for key,row in K.items()}
    E00=-2*N;seen=set(basis);action=defaultdict(int);nnz=0
    for st,v in zip(basis,vec):
        col=defaultdict(int);col[st]=scale*(E00+sum(EX[x] for x in st))
        for i,_,j,_,_ in expected:
            for r,s,c in integer_kernel[st[i],st[j]]:
                state=list(st);state[i]=r;state[j]=s;col[tuple(state)]+=c
        for state,c in col.items():
            if c:
                seen.add(state);action[state]+=c*v;nnz+=1
    metric=lambda st:math.prod(W[x] for x in st)
    norm=sum(metric(st)*v*v for st,v in zip(basis,vec))
    rho=Q(sum(metric(st)*v*action[st] for st,v in zip(basis,vec)),scale*norm)
    second=Q(sum(metric(st)*v*v for st,v in action.items()),scale*scale*norm)
    r2=second-rho*rho
    assert rho==Q(rec['exact_rayleigh']) and r2==Q(rec['exact_residual_squared']) and r2>=0
    assert len(seen)==rec['reached_support_dimension'] and nnz==rec['sparse_nnz']
    local=local_psd(lc)
    a,b=Q(lc['a']),Q(lc['b']);alpha=1-2*a;B=N*b
    assert 0<alpha<=1 and B>=0
    assert alpha==Q(rb['alpha']) and B==Q(rb['B']) and alpha-B==Q(rb['second_shift_lower'])
    cutoff=E00+alpha-B
    assert cutoff==Q(rec['second_eigenvalue_lower']) and rho<cutoff
    lo=rho-r2/(cutoff-rho)
    assert lo==Q(rec['ground_lower']) and rho==Q(rec['ground_upper'])
    assert Q(rec['E00'])==E00 and Q(rec['Vmin'])==-2*N*g and Q(rec['Vmax'])==N*g
    # Full-space isolated dimer bins, with every magnetic degeneracy counted.
    bins=Counter({0:1})
    for _ in range(N):
        nxt=Counter()
        for energy,mult in bins.items():
            for e,d in [(0,1),(1,3),(3,5)]:nxt[energy+e]+=mult*d
        bins=nxt
    assert sum(bins.values())==9**N and bins[0]==1 and bins[1]==3*N
    return dict(N_dimers=N,physical_sites=2*N,full_dimension=9**N,retained_states=1,
                trial_dimension=len(basis),full_Hv_support=len(seen),matrix_nnz=nnz,
                independent_integer_scale=scale,rayleigh_identical=True,entire_residual_identical=True,
                Temple_interval_identical=True,full_space_cutoff=str(cutoff),
                reference_bins=[(e,m) for e,m in sorted(bins.items())],
                local_positivity=local,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def trace_bound(rec,beta):
    rb=rec['relative_form_bound'];alpha=Q(rb['alpha']);B=Q(rb['B'])
    lo,hi=Q(rec['ground_lower']),Q(rec['ground_upper']);N=rec['N_dimers']
    z=1+3*exp_bounds(-beta*alpha)[1]+5*exp_bounds(-3*beta*alpha)[1]
    tail=exp_bounds(-beta*(Q(rec['E00'])-B-hi))[1]*(z**N-1)
    return exp_bounds(beta*(hi-lo))[1]+tail,tail


def f(x):
    assert 0<=x<1
    return x*x/(2*(1-x)**2)


def bootstrap(S,T,n,beta):
    p,q=ceil(1-S),ceil(1-T);rows=[]
    for round_index in range(65):
        if max(p,q)<=Q(1,100):
            return dict(status='accepted_conditional_scalar_seed',updates=rows,n=n,beta=str(beta),p=str(p),q=str(q))
        pn=ceil(f(1-(1-p)**2*(1-q)))
        if pn>=1:return dict(status='unusable_spatial_bound',updates=rows,attempted_p_upper=str(pn))
        qn=ceil(f(1-(1-q)**2*(1-pn)))
        rows.append(dict(round=round_index+1,p_upper=str(pn),q_upper=str(qn)))
        if qn>=1:return dict(status='unusable_thermal_bound',updates=rows)
        p,q=pn,qn;n*=2;beta*=2
    raise AssertionError('Unexpectedly long scalar replay')


def check_seeds(data):
    r1,r2=data['ground_certificates'];n=r1['N_dimers'];results=[]
    for seed in data['seeds']:
        beta=Q(seed['beta']);Q1,tail1=trace_bound(r1,beta);Q2,tail2=trace_bound(r2,beta)
        shift=Q(r2['ground_upper'])-2*Q(r1['ground_upper'])
        S=floor(exp_bounds(-beta*shift)[0]/Q1**2);T=floor(1/Q2**2)
        assert S==Q(seed['S_lower']) and T==Q(seed['T_lower'])
        replay=bootstrap(S,T,n,beta);saved=seed['bootstrap']
        assert replay['status']==saved['status'] and replay['updates']==saved['updates']
        accepted=replay['status']=='accepted_conditional_scalar_seed'
        out=dict(beta=str(beta),S=str(S),T=str(T),tail_displays=[float(tail1),float(tail2)],
                 independent_seed_endpoints_identical=True,independent_sequential_updates_identical=True,
                 accepted=accepted)
        if accepted:
            assert replay['n']==saved['final_n'] and replay['beta']==saved['final_beta']
            u=max(Q(replay['p']),Q(replay['q']));gap=Q(saved['conditional_gap_lower_rational'])
            assert exp_bounds(Q(replay['beta'])*gap)[1]<1/(5*u)
            out.update(uniform_gap_lower=str(gap),all_integer_cell_counts_at_least=replay['n'],
                       final_beta=replay['beta'],final_common_u=str(u),gap_verified_by_independent_exponential=True)
        results.append(out)
    return results


def sqrt_lower(x,digits=30):
    scale=10**digits
    return Q(math.isqrt(x.numerator*scale*scale//x.denominator),scale)


def bridge(data, target):
    """Use one local form through M=7; signed-transfer windows beyond that."""
    r=data['ground_certificates'][1];lc=r['relative_form_bound']['local_certificate']
    a,b=Q(lc['a']),Q(lc['b'])
    local_gap=1-2*a-7*b
    assert local_gap>target
    result=dict(short_cells=[2,7],short_gap=str(local_gap),short_gap_display=float(local_gap),
                local_a=str(a),local_b=str(b),product_singlet_energy_upper='-2*M',windows=[])
    # Choose a strongest accepted temperature; recurse backwards only through
    # recorded, independently audited updates. Direct interpolation needs no
    # small-defect asymptotic acceptance assumption.
    accepted=[s for s in data['seeds'] if 'conditional_gap_lower_rational' in s['bootstrap']]
    best=max(accepted,key=lambda s:Q(s['bootstrap']['conditional_gap_lower_rational']))
    final_n=best['bootstrap']['final_n'];n=data['ground_certificates'][0]['N_dimers']
    beta=Q(best['beta']);rows=best['bootstrap']['updates']
    covered=8
    for index,row in enumerate(rows):
        n*=2;beta*=2
        if n>=final_n:break
        p,q=Q(row['p_upper']),Q(row['q_upper'])
        A=(1-p)**2*(1-q)
        assert A>Q(1,2)
        w=(1+sqrt_lower(2*A-1))/2
        rtail=(1-w)/w
        pnext=Q(rows[index+1]['p_upper'])
        # For t=L/(2n) in [1/2,1], replacing positive factors x^t
        # or x^(2-2t) by x is conservative.
        purity=(1-p)*(1-q)*(1-pnext)*(1-rtail)
        assert purity>Q(1,2) and exp_bounds(beta*target)[1]<purity/(1-purity)
        # Float logarithm proposes a display-friendly rational; the following
        # exact exponential inequality, not the proposal, certifies it.
        bridge_gap=Q(math.floor(math.log(float(purity/(1-purity)))/float(beta)*10**12)-1,10**12)
        assert exp_bounds(beta*bridge_gap)[1]<purity/(1-purity)
        assert n==covered;covered=2*n
        result['windows'].append(dict(cells=[n,2*n],beta=str(beta),p=str(p),q=str(q),
             Y_power_purity_lower=str(A),dominant_weight_lower=str(w),absolute_tail_ratio_upper=str(rtail),
             next_spatial_defect_upper=str(pnext),thermal_purity_lower=str(purity),
             thermal_purity_lower_display=float(purity),target_gap_passes=True,
             window_gap_lower=str(bridge_gap),window_gap_lower_display=float(bridge_gap)))
    assert covered==final_n
    result.update(bootstrap_from=final_n,uniform_gap_lower=str(target),all_integer_cells_at_least=2,
                  best_seed_beta=best['beta'])
    return result


def audit(stem):
    t=time.monotonic();path=DATA/(stem+'.json');data=json.loads(path.read_text())
    grounds=[]
    for rec in data['ground_certificates']:
        item=check_ground(rec);grounds.append(item)
        print('GROUND PASS',stem,item['N_dimers'],item['trial_dimension'],item['full_Hv_support'],round(item['seconds'],3),flush=True)
    seeds=check_seeds(data)
    target=max(Q(s['uniform_gap_lower']) for s in seeds if s['accepted'])
    bridges=bridge(data,target)
    report=dict(status='PASS: independently reconstructed exact sparse residuals, local strict positivity, whole-space completeness, Temple, all tails, scalar replay, and all-size bridge',
                source=str(path.relative_to(BASE)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                Hamiltonian='Periodic spin-one alternating chain, unit strong bonds, weak AF Heisenberg g, M two-spin cells',
                g=data['ground_certificates'][0]['relative_form_bound']['local_certificate']['coupling'],
                ground_checks=grounds,seed_checks=seeds,all_size_bridge=bridges,
                elapsed_seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                arithmetic='Python integers and fractions; independently implemented outward exponentials and exact LDL; no eigensolver',
                transfer_scope='Homogeneous exchange- and cell-time-reversal-invariant Heisenberg v; audited signed self-adjoint history transfer works for every integer M>=2; the old analytic-seed width restriction is not a transfer restriction.')
    out=HERE/(stem+'_independent_audit.json');out.write_text(json.dumps(report,indent=2)+'\n')
    print('AUDIT PASS',stem,'all M>=2 gap',str(target),'seconds',round(report['elapsed_seconds'],3),'peak MiB',report['peak_rss_kib']/1024,flush=True)
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stems',nargs='*');args=ap.parse_args()
    stems=args.stems or ['chain_sparse_s1_g1d8_n4_depth3','chain_sparse_s1_g1d10_n4_depth2',
                         'chain_sparse_s1_g3d20_n4_depth3','chain_sparse_s1_g3d20_n4_depth4']
    summaries=[]
    for stem in stems:
        r=audit(stem);summaries.append(dict(source=stem,g=r['g'],gap=r['all_size_bridge']['uniform_gap_lower'],
                                        all_integer_cells_at_least=2,elapsed_seconds=r['elapsed_seconds']))
    (HERE/'summary.json').write_text(json.dumps(dict(results=summaries,total_seconds=time.monotonic()-START,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,BLAS_threads=1,
        address_space_limit_bytes=1024**3),indent=2)+'\n')
