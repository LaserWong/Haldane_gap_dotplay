"""Alternative correlated cycles transported into a canonical x,y,time staircase.

Every changed basepoint is accounted for by the exact adjacent-swap identity.
Only the canonical replay is used to emit a gap candidate.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'translation_band'))
import large_refined_pipeline as P
import correlated_low_band as C
import low_band_certificate as L


def sqrt_lower(x,digits=40):
    x=F(x);assert x>=0;d=10**digits
    n=math.isqrt(x.numerator*d*d//x.denominator);lo=F(n,d)
    assert lo*lo<=x<(lo+F(1,d))**2
    return lo


def transport(a,b,c,order,sqrt):
    if order=='xyt':return [a,b,c]
    if order=='xty':return [a,b*sqrt(c),b*b*c]
    if order=='txy':return [a*sqrt(b),a*a*b*sqrt(c),a**4*b*b*c]
    raise ValueError(order)


def score(recs,beta,order):
    abc=C.float_initial(recs,beta,order)
    if abc is None:return 1.
    abc=transport(*abc,order,math.sqrt)
    for j in range(16):
        u=max(1-x for x in abc)
        if u<=.002:return -math.log(1/(32*u))/(2**(j+1)*beta) if u>0 else -1.
        for _ in range(3):
            val=C.G(abc[0]**4*abc[1]**2*abc[2])
            if val<=0:return 1.+u
            abc=abc[1:]+[val]
    return max(1-x for x in abc)


def exact(recs,beta,order):
    beta=F(beta);q=lambda i,b:P.fast_trace(recs[i],b)
    e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    q0=q(0,beta);q3=q(2,2*beta)
    i1,b1=(0,2*beta) if order[0]=='t' else (1,beta)
    i2,b2=(2,beta) if order[-1]=='t' else (1,2*beta)
    q1=q(i1,b1);q2=q(i2,b2)
    j1=L.down(P.exp_interval(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,digits=16)
    j2=L.down(P.exp_interval(-4*beta*e[2]+8*b1*e[i1])[0]*q3[0]**2/q1[1]**8,digits=16)
    c0=L.down(P.exp_interval(-2*beta*e[2]+2*b2*e[i2])[0]*q3[0]/q2[1]**2,digits=16)
    assert all(0<x<=1 for x in (j1,j2,c0))
    a=L.down(C.G(j1),digits=16);assert 0<a<=1
    b=L.down(C.G(j2*a),digits=16);assert 0<b<=1
    c=L.down(C.G(c0**4*a*a*b),digits=16);assert 0<c<=1
    abc=[L.down(x,digits=18) for x in transport(a,b,c,order,sqrt_lower)]
    assert all(0<x<=1 for x in abc)
    boot=L.replay(*abc,n=8,m=8,beta=2*beta,rounds=64,digits=18)
    return dict(status='permuted_then_canonical_candidate_pending_independent_review',g='3/50',order=order,
        beta_initial=str(beta),J1=str(j1),J2=str(j2),third_original_staircase_ratio=str(c0),
        permuted_first_purities=list(map(str,[a,b,c])),canonical_first_purities=list(map(str,abc)),
        canonical_base=dict(n=8,m=8,beta=str(2*beta)),bootstrap=boot,
        accepted=boot['status']=='accepted_analytic_scalar_certificate')


def main():
    paths=[HERE/f'temple_{x}x{y}_g3d50.json' for x,y in [(4,4),(8,4),(8,8)]]
    recs=[json.loads(p.read_text()) for p in paths];records=[]
    for order in ('xty','txy'):
        grid=sorted((score(recs,b/20,order),F(b,20)) for b in range(100,601))
        if grid[0][0]>=0:
            records.append(dict(order=order,status='no_successful_float_proposal'));continue
        value,beta=grid[0];row=exact(recs,beta,order)
        row.update(float_proposal_score=value,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        records.append(row);(HERE/f'transported_{order}_g006.json').write_text(json.dumps(row,indent=2))
        print(order,beta,row['bootstrap'],flush=True)
    (HERE/'transported_orders_summary.json').write_text(json.dumps(records,indent=2))


if __name__=='__main__':main()
