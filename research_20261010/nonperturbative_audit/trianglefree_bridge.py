"""Finite square bridge from simple degree-4 triangle-free occupancy graphs.
For L>=4, E(A)<=min(2q,floor(q^2/4)) by degree and Mantel; weighted-star
then bounds every q-sector. Local comparison is checked at both epsilon endpoints.
"""
import os,sys
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
from fractions import Fraction as F
from pathlib import Path
import math,json
from scipy.optimize import minimize_scalar
OUT=Path(__file__).resolve().parent;BASE=OUT.parents[1]
sys.path.insert(0,str(BASE/'low_energy'));sys.path.insert(0,str(OUT))
from fully_frustrated import local_bound
from audit_ff import local_psd
# q>=8 has f(q)>=q/4, hence q=8 suffices whenever a<1/16.
LEVELS=[(1,F(1))]+[(q,F(q)-F(3,10)*(min(2*q,q*q//4)+F(q,2))) for q in range(2,9)]

def bridge(eps,n):
    eps=F(eps)
    small=[(2,F(2,5)-12*eps)]
    if n>3:small.append((3,1-27*eps))
    if n<=4:return dict(bound=str(min(v for L,v in small)),small=small,kind='exact_FF_plus_Weyl')
    N=(n-1)**2
    def objective(x):
        b=math.sqrt(x*x-x*float(eps)+float(eps)**2)-x+float(eps)/2
        return -(min(float(e)-4*x*q for q,e in LEVELS)-2*N*b)
    opt=minimize_scalar(objective,bounds=(0,1/16),method='bounded',options={'xatol':1e-14})
    proposals={F(0),F(round(opt.x*10**12),10**12)}
    for q,e in LEVELS:
        for r,f in LEVELS:
            if q!=r:
                x=(e-f)/(4*(q-r))
                if 0<=x<F(1,16):proposals.add(x)
    a=min(proposals,key=lambda x:objective(float(x)))
    lc=local_bound(F(1,2),eps,a,'bilayer');b=F(lc['b'])
    local_psd(a,b,eps);local_psd(a,b,F(0))
    assert 0<=a<F(1,16)
    cutoff=min(e-4*a*q for q,e in LEVELS);large=cutoff-2*N*b;bound=min(large,*(v for L,v in small))
    return dict(kind='triangle_free_occupancy_plus_local_PSD',bound=str(bound),worst_L=n-1,a=str(a),b=str(b),cutoff=str(cutoff),large_square_bridge=str(large),small=[[L,str(v)] for L,v in small],local_certificate=lc,PSD_at_both_endpoints=True,reference_levels=[[q,str(e)] for q,e in LEVELS])

if __name__=='__main__':
    data=json.loads((OUT/'epsilon_scan_summary.json').read_text());rows=[]
    for rec in data:
        success=[]
        for seed in rec['exact_successes']:
            b=bridge(F(rec['epsilon']),seed['n']);value=min(F(seed['bootstrap_gap']),F(b['bound']))
            success.append(dict(beta=seed['beta'],n=seed['n'],bootstrap_gap=seed['bootstrap_gap'],bridge=b,all_sizes_gap=str(value) if value>0 else None))
        best=max((r for r in success if r['all_sizes_gap']),key=lambda r:F(r['all_sizes_gap']),default=None)
        rows.append(dict(epsilon=rec['epsilon'],checks=success,best=best))
        print(rec['epsilon'],float(F(best['all_sizes_gap'])) if best else None,flush=True)
    (OUT/'trianglefree_bridge_scan.json').write_text(json.dumps(rows,indent=2))
