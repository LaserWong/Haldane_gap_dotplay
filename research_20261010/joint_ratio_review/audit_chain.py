"""External audit of frozen joint-aware alternating spin-one chain certificates.
No chain_filter_extension or new producer mathematical module is imported.
Physical local kernel and complete small-trial checker are inherited by sealed
hash from the already independent frontier review. The first moments, trace
bounds, exponentials, scalar paths, windows and coverage are checked here.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys
sys.dont_write_bytecode=True
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from functools import lru_cache
import json,math,hashlib,shutil,time
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=ROOT/'research_20261010/chain_filter_extension';SNAP=HERE/'chain_snapshot'
OLD=ROOT/'research_20261010/chain_frontier_review'
INPUT={}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    INPUT[str(p.relative_to(ROOT))]=sha(p)
    return json.loads(p.read_text())
def save(name,x):(HERE/'results'/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def floor(x,digits=12):return Q(x.numerator*10**digits//x.denominator,10**digits)
def root(x,digits=70):
    D=10**digits;k=math.isqrt(x.numerator*D*D//x.denominator);r=Q(k,D)
    assert r*r<=x<(r+Q(1,D))**2
    return r

def freeze():
    man=PROD/'FROZEN_MANIFEST.json'
    assert sha(man)=='bc1b7bcc23f7f217c558a77790c0c45a8763ae40c1d8b20b5ca3b50d18d16370'
    files=load(man);SNAP.mkdir(exist_ok=True)
    for name,digest in files.items():
        p=PROD/name;q=SNAP/name;assert sha(p)==digest,('producer drift',name)
        if q.exists():assert sha(q)==digest
        else:q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    shutil.copy2(man,HERE/'PRODUCER_CHAIN_MANIFEST.json')
    external=load(SNAP/'EXTERNAL_INPUT_SHA256.json')
    for name,digest in external.items():assert sha(ROOT/name)==digest,('external drift',name)
    oldfiles=load(OLD/'SHA256SUMS.json')
    for name,digest in oldfiles.items():assert sha(OLD/name)==digest,('old review drift',name)
    assert sha(OLD/'independent_core.py')=='30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19'
    return dict(producer_manifest_sha256=sha(man),frozen_producer_files=len(files),
        external_files_verified=len(external),prior_independent_review_files_verified=len(oldfiles),
        physical_core_sha256=sha(OLD/'independent_core.py'))
PROVENANCE=freeze()
sys.path.insert(0,str(OLD));import independent_core as C

# Separate interval exponential: 110 terms, <=1/16, directed 384-bit rounding.
BITS=384;SCALE=1<<BITS

def down(x):return Q(x.numerator*SCALE//x.denominator,SCALE)
def up(x):return -down(-x)
@lru_cache(maxsize=4096)
def expbox(x):
    x=Q(x)
    if x<0:
        lo,hi=expbox(-x);return down(1/hi),up(1/lo)
    n=0
    while x>Q(1,16):x/=2;n+=1
    term=Q(1);v=Q(1)
    for j in range(1,111):term=term*x/j;v+=term
    nextterm=term*x/111
    low=down(v);high=up(v+nextterm/(1-x/112))
    for _ in range(n):low=down(low*low);high=up(high*high)
    return low,high

# Reconstruct full returning-support matrix elements using per-column action
# dictionaries, independently of the producer's nested first-moment assembly.
def moments(mat):
    N=mat['N'];paths=[ROOT/p for p in mat['source_paths']]
    arrays=[np.load(p,allow_pickle=False) for p in paths]
    for p in paths:INPUT[str(p.relative_to(ROOT))]=sha(p)
    basis=[tuple(map(int,s)) for s in arrays[0]['basis']]
    assert len(set(basis))==len(basis)==mat['trial_support']
    assert mat['full_dimension']==9**N and all(len(s)==N and all(0<=d<9 for d in s) for s in basis)
    assert all(sum(C.MAG[d] for d in s)==0 for s in basis)
    assert all(np.array_equal(a['basis'],arrays[0]['basis']) for a in arrays)
    coeff=[list(map(int,a['vector'])) for a in arrays]
    assert all(len(c)==len(basis) for c in coeff)
    k=len(coeff);assert k==mat['linear_combination_dimension']
    index={s:i for i,s in enumerate(basis)};weights=[math.prod(C.W[d] for d in s) for s in basis]
    denom=math.lcm(*(v.denominator for row in C.K.values() for _,_,v in row))
    kernel={pair:[(a,b,int(v*denom)) for a,b,v in row] for pair,row in C.K.items()}
    h0=[-2*N+sum(C.EX[d] for d in s) for s in basis]
    gram=[[sum(w*x*y for w,x,y in zip(weights,coeff[i],coeff[j])) for j in range(k)] for i in range(k)]
    strong=[[sum(w*e*x*y for w,e,x,y in zip(weights,h0,coeff[i],coeff[j])) for j in range(k)] for i in range(k)]
    weak=[[0]*k for _ in range(k)]
    bonds=[((j-1)%N,j) for j in range(N)]
    assert len(bonds)==N
    for j,state in enumerate(basis):
        action=Counter()
        for left,right in bonds:
            for a,b,val in kernel[state[left],state[right]]:
                dest=list(state);dest[left]=a;dest[right]=b
                ii=index.get(tuple(dest))
                if ii is not None:action[ii]+=val
        for i,v in action.items():
            for row in range(k):
                bra=weights[i]*coeff[row][i]*v
                for col in range(k):weak[row][col]+=bra*coeff[col][j]
    for calc,name in ((gram,'G'),(strong,'K0'),(weak,'K1_scaled')):
        assert calc==[list(map(int,r)) for r in mat[name]],name
        assert calc==[list(t) for t in zip(*calc)]
    assert mat['weak_denominator']==denom
    if k==2:assert gram[0][0]>0 and gram[0][0]*gram[1][1]-gram[0][1]**2>0
    else:assert gram[0][0]>0
    return dict(N=N,physical_spins=2*N,full_dimension=9**N,support=len(basis),
        first_moment_search_dimension=k,periodic_bond_multiset=bonds,
        exact_Gram_strong_and_weak_moments_verified=True,largest_residual_not_required=True)

def expectation(mat,c,g):
    k=len(c)
    bil=lambda key:sum(Q(mat[key][i][j])*c[i]*c[j] for i in range(k) for j in range(k))
    norm=bil('G');assert norm>0
    return (bil('K0')+g*bil('K1_scaled')/mat['weak_denominator'])/norm

@lru_cache(maxsize=128)
def trace_upper(small_serialized,beta):
    rec=json.loads(small_serialized)
    N=rec['N_dimers'];assert N==4
    alpha=Q(rec['relative_form_bound']['alpha']);B=Q(rec['relative_form_bound']['B'])
    rho=Q(rec['ground_upper']);elo=Q(rec['ground_lower'])
    bins=Counter({0:1})
    for _ in range(N):
        nxt=Counter()
        for e,m in bins.items():
            for f,mm in ((0,1),(1,3),(3,5)):nxt[e+f]+=m*mm
        bins=nxt
    assert sum(bins.values())==9**N and bins[0]==1
    terms=[expbox(beta*(rho-elo))[1]]
    for e,m in bins.items():
        if e:terms.append(m*expbox(-beta*(Q(-2*N)-B+alpha*e-rho))[1])
    return sum(terms)

def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)

def window(win,S,T,K,n,beta):
    assert 0<S<=1 and 0<T<=1 and S*S*T<=K<=1 and K>Q(1,2)
    assert win['cells']==[n,2*n] and Q(win['beta'])==beta
    assert [Q(win[z]) for z in ('S_lower','T_lower','joint_S2T_lower')]==[S,T,K]
    # Check the exact saved 50-decimal root witness, then independently use 70.
    savedw=Q(win['dominant_weight_lower']);savedroot=2*savedw-1
    assert savedroot*savedroot<=2*K-1<(savedroot+Q(1,10**50))**2
    savedr=Q(win['absolute_tail_ratio_upper']);savedd=Q(win['D_lower'])
    assert savedr==(1-savedw)/savedw and savedd==T/(1+savedr*savedr)
    w=(1+root(2*K-1))/2;r=(1-w)/w;d=T/(1+r*r)
    I=(1-r)*min(S*root(d),d)
    saved=Q(win['thermal_purity_lower']);gap=Q(win['gap_lower'])
    assert Q(1,2)<saved<=I and gap>0
    margin=saved-expbox(beta*gap)[1]*(1-saved);assert margin>0
    return dict(cells=[n,2*n],beta=str(beta),thermal_lower=str(saved),gap_lower=str(gap),
        independent_70digit_thermal_lower=str(floor(I,60)),exponential_margin_lower=str(margin))

def scalar(rec,row):
    beta=Q(row['beta']);small=rec['input']['small'];rho=Q(rec['input']['large']['exact_rayleigh'])
    shift=rho-2*Q(small['exact_rayleigh']);assert shift==Q(row['Rayleigh_shift'])
    sm=json.dumps(small,sort_keys=True)
    q1,q2=[Q(row[x]) for x in ('small_Q_beta_upper','small_Q_2beta_upper')]
    assert trace_upper(sm,beta)<=q1 and trace_upper(sm,2*beta)<=q2
    L=expbox(-2*beta*shift)[0];J,cc=[Q(row[x]) for x in ('J_lower','C_lower')]
    assert 0<J<=L/q1**4<=1 and 0<cc<=L/q2**2<=1
    a=floor(G(J));b=floor(G(cc*cc*a))
    assert [a,b]==list(map(Q,row['initial_time_pair'])) and a>0 and b>0
    n=8;be=2*beta;states=row['states'];wins=row['windows'];result=[];i=0
    for _ in range(row['time_steps']):
        K=a*a*b;S=floor(a*root(b));T=floor(K)
        assert states[i]==dict(order='time-space',cells=n,beta=str(be),pair=list(map(str,[a,b])),canonical_joint=str(K))
        result.append(window(wins[i],S,T,K,n,be));i+=1
        na=floor(G(K));nb=floor(G(b*b*na));assert na>0 and nb>0
        a,b=na,nb;n*=2;be*=2
    K=a*a*b;S=floor(a*root(b));T=floor(K)
    assert row['conversion']==dict(cells=n,beta=str(be),time_pair=list(map(str,[a,b])),S_lower=str(S),T_lower=str(T),joint_S2T_lower=str(K))
    assert S*S<=K and T<=K and S*S*T<=K
    conversion_base=[n,str(be)]
    for _ in range(row['canonical_steps']):
        assert states[i]==dict(order='space-time',cells=n,beta=str(be),pair=list(map(str,[S,T])),joint_S2T_lower=str(K))
        result.append(window(wins[i],S,T,K,n,be));i+=1
        S=floor(G(K));T=floor(G(T*T*S));assert 0<S<=1 and 0<T<=1
        K=S*S*T;n*=2;be*=2
    assert i==len(states)==len(wins)
    u=max(1-S,1-T);final=row['final'];d=Q(final['asymptotic_gap_lower'])
    assert final==dict(cells=n,beta=str(be),S_lower=str(S),T_lower=str(T),common_defect_upper=str(u),asymptotic_gap_lower=str(d))
    assert 0<u<=Q(1,100) and d>0
    margin=1-expbox(be*d)[1]*5*u;assert margin>0
    allgap=min([d]+[Q(w['gap_lower']) for w in result]);assert allgap==Q(row['M_ge8_gap_lower'])
    assert [w['cells'][0] for w in result]==[8*2**j for j in range(i)]
    assert n==8*2**i
    return dict(initial_beta=str(beta),time_cycles=row['time_steps'],canonical_cycles=row['canonical_steps'],
        conversion_base_cells_beta=conversion_base,windows=result,asymptotic_cells=n,asymptotic_beta=str(be),
        asymptotic_gap=str(d),asymptotic_exponential_margin_lower=str(margin),M_ge8_gap_lower=str(allgap))

def main():
    start=time.monotonic()
    matrices={n:load(SNAP/name) for n,name in [(8,'M8_two_trial_moments.json'),(6,'M6_bridge_moments.json'),(7,'M7_bridge_moments.json')]}
    momresults={n:moments(m) for n,m in matrices.items()}
    save('chain_first_moments.json',momresults)
    print('PASS independent first moments M=8,6,7',flush=True)
    rows=[]
    for path in sorted(SNAP.glob('candidate_g*.json')):
        rec=load(path);g=Q(rec['g']);inp=rec['input'];assert Q(inp['g'])==g and Q(inp['large']['g'])==g
        small=inp['small'];assert small['N_dimers']==4 and Q(small['relative_form_bound']['local_certificate']['coupling'])==g
        folder=ROOT/inp['small_folder'];C.DATA=SNAP if folder==PROD else folder
        INPUT[str((C.DATA/small['trial_artifact']).relative_to(ROOT))]=sha(C.DATA/small['trial_artifact'])
        ground=C.check_ground(small)
        rho8=expectation(matrices[8],list(map(int,inp['large']['combination_integers'])),g)
        assert rho8==Q(inp['large']['exact_rayleigh'])
        assert inp['large']['trial_support']==43294 and inp['large']['full_dimension']==9**8
        assert inp['large']['linear_combination_dimension']==2
        short=rec['short_bridge'];local=short['local'];lc=local['local_certificate']
        assert Q(lc['coupling'])==g;psd=C.local_psd(lc)
        aa,bb=Q(lc['a']),Q(lc['b']);alpha=1-2*aa
        assert 0<alpha<=1 and bb>=0 and Q(local['alpha'])==alpha and Q(local['B'])==7*bb
        assert Q(local['second_shift_lower'])==alpha-7*bb
        assert len(short['rows'])==6;shortrows=[]
        for m,sr in zip(range(2,8),short['rows']):
            rho=min(Q(-2*m),expectation(matrices[m],[1],g)) if m in (6,7) else Q(-2*m)
            cutoff=-2*m+alpha-m*bb;gap=cutoff-rho
            assert gap>0 and sr['M']==m and sr['full_dimension']==9**m
            assert [Q(sr[x]) for x in ('cutoff_lower','rayleigh_upper','gap_lower')]==[cutoff,rho,gap]
            shortrows.append(dict(cells=m,cutoff=str(cutoff),rayleigh=str(rho),gap_lower=str(gap)))
        shortgap=min(Q(sr['gap_lower']) for sr in shortrows);assert shortgap==Q(short['gap_lower'])
        allrows=[scalar(rec,row) for row in rec['rows']]
        for row,checked in zip(rec['rows'],allrows):
            assert min(shortgap,Q(checked['M_ge8_gap_lower']))==Q(row['all_M_ge2_gap_lower'])
        best=max(rec['rows'],key=lambda r:Q(r['all_M_ge2_gap_lower']));assert best==rec['best']
        bestindex=rec['rows'].index(best)
        output=dict(g=str(g),accepted_gap_lower=best['all_M_ge2_gap_lower'],accepted_gap_display=float(Q(best['all_M_ge2_gap_lower'])),
            scope='Every integer periodic cell count M>=2, unique finite-volume ground state',
            small_complete_physical_review=ground,largest_exact_rayleigh=str(rho8),short_local_LDL=psd,
            short_sizes=shortrows,minimum_short_gap=str(shortgap),audited_rows=len(allrows),
            audited_window_count=sum(len(r['windows']) for r in allrows),selected_path=allrows[bestindex],all_paths=allrows)
        save('chain_review_'+str(g).replace('/','d')+'.json',output)
        rows.append({k:v for k,v in output.items() if k in ('g','accepted_gap_lower','accepted_gap_display','scope','audited_rows','audited_window_count','minimum_short_gap')})
        print('PASS',g,best['all_M_ge2_gap_lower'],'all rows',len(allrows),flush=True)
    summary=dict(status='PASS external independent physical, joint-scalar, and all-integer bridge audit',results=rows,provenance=PROVENANCE,
        exact_exponentials='110 Taylor terms after <=1/16 range reduction, directed 384-bit rounding; no producer exponential calls',
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,seconds=time.monotonic()-start,
        AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0)))
    save('chain_summary.json',summary);save('chain_audit_input_sha256.json',INPUT)
    print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
