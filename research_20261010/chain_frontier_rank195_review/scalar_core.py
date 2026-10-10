"""Counted-band full exact audit. Scalar helpers copied from sealed independent joint review.
No producer mathematical module is imported. The earlier review and all source bytes
are hash-checked. Full P/Q moments are independently reconstructed here.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys
sys.dont_write_bytecode=True
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from collections import Counter
import json,math,hashlib,shutil,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=HERE.parent/'chain_small_low_band';SNAP=HERE/'snapshot';PRIOR=HERE.parent/'joint_ratio_review'
BITS=384;SCALE=1<<BITS
INPUT={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 INPUT[str(p.relative_to(ROOT))]=sha(p);return json.loads(p.read_text())
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def floor(x,digits=12):return Q(x.numerator*10**digits//x.denominator,10**digits)

def root(x,digits=70):
    D=10**digits;k=math.isqrt(x.numerator*D*D//x.denominator);r=Q(k,D)
    assert r*r<=x<(r+Q(1,D))**2
    return r

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

def expectation(mat,c,g):
    k=len(c)
    bil=lambda key:sum(Q(mat[key][i][j])*c[i]*c[j] for i in range(k) for j in range(k))
    norm=bil('G');assert norm>0
    return (bil('K0')+g*bil('K1_scaled')/mat['weak_denominator'])/norm

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

