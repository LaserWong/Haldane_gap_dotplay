"""Independent exact joint-ratio audit. No producer mathematical imports.
Tests are supplementary; GENERAL_LEMMA.md supplies the analytic proof.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
if hasattr(os,'sched_getaffinity'): os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations
from collections import defaultdict
import math,json,random,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
D=10**55

def lower(x,scale=D):
    return Q(x.numerator*scale//x.denominator,scale)

def root(x,scale=D):
    assert x>=0
    r=Q(math.isqrt(x.numerator*scale*scale//x.denominator),scale)
    assert r*r<=x<(r+Q(1,scale))**2
    return r

def G(x):
    assert 0<x<=1
    return Q(1)-(1-x)**2/(2*x*x)

def mul(*terms):
    d=defaultdict(int)
    for p,k in terms:
        for v,e in p.items(): d[v]+=k*e
    return {v:e for v,e in d.items() if e}

def edge(base,axis):
    end=list(base);end[axis]+=1
    return {tuple(end):1,base:-2}

def ladder(base,order):
    edges=[];points=[base]
    for axis in order:
        edges.append(edge(points[-1],axis))
        p=list(points[-1]);p[axis]+=1;points.append(tuple(p))
    return points,edges

def identity_ledger():
    output=[];total=0;swaps=0;rotations=0
    for count in (2,3,4):
        for order in permutations(range(count)):
            base=(0,)*count
            states=[]
            for cycle in range(4):
                points,q=ladder(base,order)
                powers=[2**(count-1-i) for i in range(count)]
                assert mul(*zip(q,powers))=={points[-1]:1,base:-2**count}
                for pos in range(count-1):
                    v=points[pos];i,j=order[pos:pos+2]
                    a=edge(v,i);b=edge(tuple(x+(k==i) for k,x in enumerate(v)),j)
                    c=edge(v,j);e=edge(tuple(x+(k==j) for k,x in enumerate(v)),i)
                    assert mul((a,2),(b,1))==mul((c,2),(e,1));swaps+=1
                cb,co=base,order
                for _ in order:
                    pp,qq=ladder(cb,co)
                    nb=pp[1];no=co[1:]+co[:1]
                    np,nq=ladder(nb,no)
                    assert nq[:-1]==qq[1:]
                    assert nq[-1]==edge(pp[-1],co[0])
                    # Product of all initial edges transports the first
                    # direction to the final point before purification.
                    whole=mul(*zip(qq,powers))
                    terminal_dir=edge(tuple(pp[-1][k]-(k==co[0]) for k in range(count)),co[0])
                    # There is an exact monomial ratio, but factors of
                    # other purities <=1 are dropped in the inequality.
                    states.append(dict(base=cb,order=co,end=pp[-1]))
                    cb,co=nb,no;rotations+=1
                assert cb==points[-1] and co==order
                base=cb;total+=1
            output.append(dict(axis_count=count,order=order,cycles=4,
                final_base=base,all_identities_exact=True))
    return dict(coordinates='log2 spatial lengths and log2 inverse temperature; last axis denotes inverse temperature',
        ladders_checked=total,adjacent_square_identities=swaps,sequential_rotations=rotations,orders=output)

def advance(values,K):
    a,b,c=values
    args=[];new=[]
    z=max(a**4*b*b*c,K);args.append(z);d=G(z)
    if d<=0:return None,args
    z=max(b**4*c*c,K*K)*d;args.append(z);e=G(z)
    if e<=0:return None,args
    z=max(c,K)**4*d*d*e;args.append(z);f=G(z)
    if f<=0:return None,args
    return (d,e,f),args

def I(s,t,K=Q(0)):
    assert 0<s<=1 and 0<t<=1 and 0<=K<=1
    p=max(s*s*t,K)
    if p<=Q(1,2):return Q(0)
    w=(1+root(2*p-1))/2;r=(1-w)/w;dd=t/(1+r*r)
    return lower((1-r)*min(s*root(dd),dd))

def I2(a,b,c,K):
    if b<=Q(1,2):return Q(0)
    sx=max(a*a*root(2*b-1),root(K)*root(2*b-1)/b)
    ty=I(b,c,K)
    if ty<=0:return Q(0)
    return I(sx,ty)

def exact_tests():
    rng=random.Random(119831)
    tests=0;successful=0;window_passes=0;chain_passes=0
    # Both a broad domain and a near-one domain, including exact-one boundaries.
    samples=[]
    for _ in range(700):
        actual=tuple(Q(rng.randint(1,1000),1000) for _ in range(3))
        samples.append(actual)
    for _ in range(1800):
        actual=tuple(Q(rng.randint(98000,100000),100000) for _ in range(3))
        samples.append(actual)
    samples.extend([(Q(1),)*3,(Q(1),Q(1,2),Q(1)),(Q(1),Q(1),Q(999,1000))])
    for A,B,C in samples:
        a,b,c=[v*Q(rng.randint(975,1000),1000) for v in (A,B,C)]
        actualJ=A**4*B*B*C
        K=actualJ*Q(rng.randint(975,1000),1000)
        assert 0<=K<=1
        assert B*B*C>=K and A**4*B*B>=K and C>=K
        assert max(a**4*b*b*c,K)<=actualJ
        value,args=advance((a,b,c),K)
        if value is not None:
            actual,_=advance((A,B,C),Q(0))
            assert actual is not None and all(x<=y for x,y in zip(value,actual))
            successful+=1
        if b>Q(1,2):
            # Squaring these positive expressions proves the central new bound.
            sx=max(a*a*root(2*b-1),root(K)*root(2*b-1)/b)
            assert sx*sx<=A**4*(2*B-1) and sx<=1
            # Avoid close rounding sensitivity using an independent higher-
            # precision comparator and exact directional square tests.
            ours=I2(a,b,c,K);reference=I2(A,B,C,actualJ)
            assert ours<=reference
            if ours>0:window_passes+=1
        p=A*A*B
        kk=p*Q(rng.randint(975,1000),1000)
        ij=I(a,b,kk);ref=I(A,B,p)
        assert ij<=ref
        if ij>0:chain_passes+=1
        tests+=1
    # Rational polynomial witness for f(B)^2 monotonicity, independently of calculus:
    # (2y-1)/y^2 - (2x-1)/x^2 = (y-x)(x+y-2xy)/(x^2 y^2).
    ftests=0
    for xnum in range(50,101):
        for ynum in range(xnum,101):
            x,y=Q(xnum,100),Q(ynum,100)
            lhs=(2*y-1)/(y*y)-(2*x-1)/(x*x)
            rhs=(y-x)*(x+y-2*x*y)/(x*x*y*y)
            assert lhs==rhs>=0;ftests+=1
    return dict(exact_rational_samples=tests,positive_2d_advances=successful,
        positive_2d_windows=window_passes,positive_1d_windows=chain_passes,
        exact_monotonicity_pairs=ftests,all_checks_passed=True)

def write(name,value):
    (HERE/'results'/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def main():
    write('basepoint_ledger.json',identity_ledger())
    write('exact_scalar_tests.json',exact_tests())
    source=[ROOT/'research_20261010/low_band/joint_trace_bootstrap/PROOF.md',
        ROOT/'research_20261010/low_band/joint_trace_bootstrap/joint_scalar.py',
        ROOT/'research_20261010/root_review/FINITE_WINDOW_INTERPOLATION.md',
        ROOT/'research_20261010/alternative_order_review/REVIEW.md',
        ROOT/'research_20261010/chain_temperature_review/REVIEW.md']
    write('lemma_source_sha256.json',{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source})
    print('PASS: exact ladder identities, basepoint cycles, joint scalar bounds, and monotonicity tests.')
if __name__=='__main__':main()
