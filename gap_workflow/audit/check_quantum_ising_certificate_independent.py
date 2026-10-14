"""Independent review diagnostics; MP/ED comparisons are not proofs."""
import json, hashlib, copy, math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import mpmath as mp
from gapflow.quantum_ising import log_partition
from gapflow.quantum_ising_interval import RationalIntervals, Interval, canonical_seed_interval, shifted_partition
from gapflow.bootstrap import bootstrap_certificate, log_lower
mp.mp.dps=200
R=RationalIntervals(50)
counts={}
def count(k): counts[k]=counts.get(k,0)+1
def mf(x): return mp.mpf(x.numerator)/x.denominator
def contains(box,x):
    assert mf(box.lo)<=x<=mf(box.hi),(box,x)
    count('mp200_enclosures_diagnostic')
def hyper(L,b,J,h):
    J,h,b=map(mp.mpf,map(str,(J,abs(h),b)))
    P=[]
    for s in (mp.mpf('.5'),mp.mpf(0)):
        e=[2*mp.sqrt((J-h)**2+4*J*h*mp.sin(mp.pi*(m+s)/L)**2) for m in range(L)]
        P.append((mp.fprod(2*mp.cosh(b*x/2) for x in e),mp.fprod(2*mp.sinh(b*x/2) for x in e)))
    sign=1 if h>=J else -1
    return (P[0][0]+P[0][1]+P[1][0]-sign*P[1][1])/2
# Endpoint polynomial invariants require no floating arithmetic.
for x in (F(0),F(1,19),F(2),F(10**40+17,31)):
    a=R.sqrt(R.point(x)); assert a.lo*a.lo<=x<=a.hi*a.hi
    assert a.hi-a.lo<=F(1,R.scale); count('exact_sqrt_checks')
# Independently summed exact Taylor lower and geometric tail upper, no grid rounding.
for x in (F(0),F(1,100),F(1,3),F(1,2)):
    term=F(1); s=term
    for k in range(1,100): term*=x/k; s+=term
    nxt=term*x/100; upper=s+nxt/(1-x/101)
    box=R.exp(R.point(x)); assert box.lo<=s<=upper<=box.hi
    count('exact_exp_reference_containment')
for p in range(9):
    for m in range(2*(1<<p)):
        a=R.cos_dyadic(m,p)
        if 2*m%(2*(1<<p))==(1<<p): assert a==Interval(F(0),F(0))
        elif m in (0,1<<p): assert a.lo==a.hi
        else: contains(a,mp.cos(mp.pi*m/(1<<p)))
for x in (-4096,-200,-1,F(-1,3),0,F(1,3),1,100,4096): contains(R.exp(R.point(x)),mp.exp(mf(F(x))))
seed=canonical_seed_interval(16,8,1,'3/2')
c=F(seed['shift_per_site']); zs=[]
for (L,b),rec in zip(((16,8),(32,8),(32,16)),seed['shifted_partition_intervals']):
    z=hyper(L,b,1,1.5); zs.append(z)
    contains(Interval(F(rec['lower']),F(rec['upper'])),z*mp.exp(-b*mf(c)*L))
for rec,v in zip(seed['purity_intervals'],(zs[1]/zs[0]**2,zs[2]/zs[1]**2)):
    contains(Interval(F(rec['lower']),F(rec['upper'])),v)
assert seed['bootstrap']['gap_lower']==str(F('0.484734263212'))
# Spin basis construction is independent of JW dispersion and parity formulas.
max_error=0; min_margin=1e100
for L in range(2,9):
    D=1<<L
    for J,h in ((1,.5),(1,1),(1,1.5),(1,2),(1,-1.5),(0,.7),(1,0),(0,0)):
        A=np.zeros((D,D))
        for s in range(D):
            A[s,s]=-J*sum((1-2*((s>>i)&1))*(1-2*((s>>((i+1)%L))&1)) for i in range(L))
            for i in range(L): A[s,s^(1<<i)]=-h
        e=np.linalg.eigvalsh(A)
        if abs(h)>J:
            margin=e[1]-e[0]-2*(abs(h)-J); min_margin=min(min_margin,margin)
            assert margin>=-1e-11; count('ed_bridge_diagnostic')
        for b in (0,.1,1,8):
            expected=-b*e[0]+np.log(np.exp(-b*(e-e[0])).sum())
            err=abs(log_partition(L,b,J,h)-expected); max_error=max(max_error,err)
            assert err<1e-10; count('ed_trace_diagnostic')
# Both purity ratios must be invariant under a common linear energy shift.
for shift in (F(0),F(7,4),F(5,2)):
    a,b,c=[shifted_partition(L,beta,1,'3/2',shift=shift) for L,beta in ((4,2),(8,2),(8,4))]
    contains(R.div(b,R.mul(a,a)),hyper(8,2,1,1.5)/hyper(4,2,1,1.5)**2)
    contains(R.div(c,R.mul(b,b)),hyper(8,4,1,1.5)/hyper(8,2,1,1.5)**2)
# Mutation of claimed values alone is not rejected by a scalar adapter: external provenance needed.
data=dict(dimension=1,lengths=[16],beta='8',edges=seed['edges'],mode='dedicated',model_to_seed_proof={'verified':True,'evidence':['declared-only']})
for mutate in ('axis','length','beta','bound'):
    d=copy.deepcopy(data)
    if mutate=='axis': d['edges'][0]['axis']='beta'
    if mutate=='length': d['edges'][1]['base_lengths']=[16]
    if mutate=='beta': d['edges'][1]['base_beta']='16'
    if mutate=='bound': d['edges'][0]['lower']='1001/1000'
    assert bootstrap_certificate(d)['status']=='INVALID_INPUT'; count('tampered_scalar_label_rejected')
d=copy.deepcopy(data); d['edges'][0]['lower']='999999/1000000'
r=bootstrap_certificate(d); assert not r['physical_proof_verified'] and not r['uniform_family_claim']
for args in ((True,8,1,'3/2'),(3,8,1,'3/2'),(128,8,1,'3/2'),(16,8.,1,'3/2'),(16,8,1.,'3/2'),(16,8,1,1.5),(16,0,1,1),(16,-1,1,1),(16,1,-1,1)):
    try: canonical_seed_interval(*args)
    except ValueError: count('malformed_rejected')
    else: raise AssertionError(args)
for thunk in (lambda:R.exp(R.point(4097)),lambda:R.cos_dyadic(1,9),lambda:RationalIntervals(101),lambda:R.div(R.point(1),Interval(F(-1),F(1)))):
    try: thunk()
    except ValueError: count('caps_or_singular_rejected')
    else: raise AssertionError('did not reject')
u=F(1,100)
assert (3-3*u+u*u)**2/(2*(1-u)**6)<5
assert (2+5*u)**2/(2*(1-(2+5*u)*u)**2)<5
assert F(3,2)+5*u+2/(1-2*u)<4
assert 4/(1-4*u)<5
assert mf(log_lower(F(1)/(5*F(seed['bootstrap']['u']))))/8 <= mp.log(1/(5*mf(F(seed['bootstrap']['u']))))/8
files=['gapflow/quantum_ising.py','gapflow/quantum_ising_interval.py','gapflow/bootstrap.py','theory/QUANTUM_ISING_SEEDS.md','theory/QUANTUM_ISING_INTERVAL.md']
out={'status':'PASS','counts':counts,'ed_max_logZ_error':max_error,'ed_min_bridge_margin':min_margin,'gap_lower':seed['bootstrap']['gap_lower'],'numerical_comparisons_are_proof':False,'source_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files},'purity_intervals':seed['purity_intervals']}
Path('audit/quantum_ising_certificate_independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
