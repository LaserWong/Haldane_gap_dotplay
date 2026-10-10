"""Legitimate staircase-order optimization; every order rebuilds its heat ratios.

Output bounds are converted to x,y,time order by proved adjacent-swap bounds
before the audited all-integer square interpolation is applied.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from fractions import Fraction as Q
from pathlib import Path
from itertools import permutations
from math import exp,log
import json
from scipy.optimize import minimize_scalar
from certified_core import G,down,exp_bounds,log_lower
from correlated_seeds import trace
from optimize_baselines import threshold
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parents[1]/'results'

def canonicalize(p,order):
    p=list(map(Q,p));o=list(order)
    for target,axis in enumerate('xyt'):
        k=o.index(axis)
        while k>target:
            a,b=p[k-1:k+1];p[k-1:k+1]=[down(a*b),down(a*a*b)]
            o[k-1],o[k]=o[k],o[k-1];k-=1
    return p

def ordered_replay(p,order,n,beta,max_rounds=64):
    p=list(map(Q,p));beta=Q(beta);updates=[]
    for j in range(max_rounds+1):
        cp=canonicalize(p,order);u=max(1-z for z in cp)
        if u<=Q(1,500):
            return {'accepted':True,'rounds_after_input':j,'order':order,'n':n,'m':n,'beta':str(beta),
                    'ordered_purities':list(map(str,p)),'canonical_purities':list(map(str,cp)),
                    'u_canonical':str(u),'gap_lower':str(down(log_lower(1/(32*u))/beta)) if u else None,
                    'updates':updates}
        if j==max_rounds:break
        for _ in range(3):
            x=p[0]**4*p[1]**2*p[2]
            if x<=0:return {'accepted':False}
            new=down(G(x))
            if new<=0:return {'accepted':False}
            p=p[1:]+[new]
        n*=2;beta*=2;updates.append(list(map(str,p)))
    return {'accepted':False,'reason':'Iteration budget, not an exclusion'}

def nodes(order,beta):
    state=[2,2,Q(beta)];out=[tuple(state)]
    for axis in order:
        k='xyt'.index(axis);state[k]*=2;out.append(tuple(state))
    return out

def record_for(records,node):
    x,y,_=node
    return records[0] if x*y==4 else records[1] if x*y==8 else records[2]

def ordered_bilayer(records,beta,order='xyt',correlated=True,qfunc=trace):
    beta=Q(beta);vs=nodes(order,beta);Us=[];qs=[]
    for v in vs:
        rec=record_for(records,v);Us.append(Q(rec['ground_upper']));qs.append(qfunc(rec,v[2]))
    def ratio(coeff):
        exponent=-sum((Q(k)*v[2]*U for k,v,U in zip(coeff,vs,Us)),Q(0))
        lo=exp_bounds(exponent)[0]
        for k,q in zip(coeff,qs):
            if k<0:lo/=q**(-k)
        return down(lo)
    p=[ratio([-2,1,0,0]),ratio([0,-2,1,0]),ratio([0,0,-2,1])]
    if not correlated:return ordered_replay(p,order,2,beta)
    J1=ratio([-8,0,0,1]);J2=ratio([0,-8,0,2])
    A=down(G(J1))
    if A<=0:return {'accepted':False}
    B=down(G(J2*A))
    if B<=0:return {'accepted':False}
    C=down(G(p[2]**4*A*A*B))
    if C<=0:return {'accepted':False}
    out=ordered_replay([A,B,C],order,4,2*beta)
    out.update(beta_initial=str(beta),initial_ordered_purities=list(map(str,p)),
               correlated_J1=str(J1),correlated_J2=str(J2),correlated_first_step=list(map(str,[A,B,C])))
    return out

def main():
    allrows=[]
    for g in ['1d100','1d50']:
        paths=[ROOT/'low_energy'/f'bilayer_s1d2_{nx}x{ny}_g{g}_k{g}_q2_ground.json' for nx,ny in [(2,2),(4,2),(4,4)]]
        records=[json.loads(p.read_text()) for p in paths]
        for order in ['xyt','xty','txy']:
            rows=[ordered_bilayer(records,Q(k,2),order) for k in range(12,81)]
            ok=[r for r in rows if r['accepted']]
            best=max(ok,key=lambda r:Q(r['gap_lower'])) if ok else None
            allrows.append({'model_id':'square_af_bilayer_spin_half_unit_rung','g':g.replace('d','/'),'order':order,'best_grid_gap':best})
            print('ORDER',g,order,'beta',best['beta_initial'] if best else None,'gap',float(Q(best['gap_lower'])) if best else None,'L0',best['n'] if best else None,flush=True)
    (OUT/'axis_order_results.json').write_text(json.dumps({'rows':allrows,'source_schema':'Ground records from low_energy; isotropic x/y symmetry required for shared 4x2 record'},indent=2))
if __name__=='__main__':main()
