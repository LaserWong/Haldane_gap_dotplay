"""Rational interval obstruction for all beta and all local-comparison a.
The output excludes the specific ground-only cancelled-first-step recipe only.
"""
import os
for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[x]='1'
import sys,json,argparse,time,resource
from pathlib import Path
from fractions import Fraction as F
from local_ceiling import ceiling,OUT,ROOT
sys.path.insert(0,str(ROOT/'seed_size/code'))
from certified_core import exp_bounds,G,up

def rejected_upper(J,T):
    if J<=F(1,2):return True,'initial_cancelled_spatial_argument'
    A=up(G(J))
    if A<=0:return True,'spatial_nonpositive'
    B=up(G(T*T*A))
    if B<=0:return True,'thermal_nonpositive'
    A=min(F(1),A);B=min(F(1),B)
    for _ in range(100):
        if A*A*B<=F(1,2):return True,'invariant_scalar_failure'
        if min(A,B)>=F(999,1000):return False,'optimistic_acceptance'
        AA=up(G(A*A*B));BB=up(G(B*B*AA))
        if AA<=0 or BB<=0:return True,'subsequent_nonpositive'
        A=min(F(1),AA);B=min(F(1),BB)
    return False,'optimistic_iteration_budget'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--max-depth',type=int,default=18);args=ap.parse_args();p=Path(args.source).resolve();rec=json.loads(p.read_text());rs=rec['ground_certificates'];g=F(rec['g']);t=time.monotonic()
    cs=[ceiling(g,r['N_dimers']) for r in rs];deltas=[F(r['E00'])+F(c['cutoff_shift_upper'])-F(r['ground_lower']) for c,r in zip(cs,rs)];kappa=F(rs[1]['ground_lower'])-2*F(rs[0]['ground_upper']);assert kappa>0
    B=F(1)
    while exp_bounds(-2*B*kappa)[1]>F(1,2):B*=2
    stack=[(F(0),B,0)];leaves=[];unknown=[]
    while stack:
        l,h,d=stack.pop();qfloors=[1+3*r['N_dimers']*exp_bounds(-(h if delta>=0 else l)*delta)[0] for delta,r in zip(deltas,rs)]
        J=min(F(1),up(exp_bounds(-2*l*kappa)[1]/qfloors[0]**4));T=min(F(1),up(1/qfloors[1]**2))
        reject,reason=rejected_upper(J,T)
        if reject:leaves.append(dict(beta_interval=[str(l),str(h)],J_upper=str(J),T_upper=str(T),reason=reason))
        elif d>=args.max_depth:unknown.append([str(l),str(h)]);break
        else:m=(l+h)/2;stack.extend([(l,m,d+1),(m,h,d+1)])
    out=dict(status='producer_obstruction_requires_independent_audit',source=str(p.relative_to(ROOT)),g=str(g),n=rec['n'],depth=rec['depth'],local_ceilings=cs,delta_upper=list(map(str,deltas)),curvature_lower=str(kappa),tail_beta_from=str(B),tail_J_upper=str(exp_bounds(-2*B*kappa)[1]),excluded_intervals=leaves,unresolved_intervals=unknown,remaining_unvisited_intervals=[[str(l),str(h)] for l,h,d in stack],all_beta_all_a_excluded=not unknown,elapsed_seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Specific ground-only numerator and independent dimer-bin tail family, standard or first-step cancelled recursion. Allows all beta, all valid local a separately at each geometry, zero ground-width penalties, and every improved ground pivot inside existing exact intervals. No physical gaplessness or optimal-coupling claim.')
    (OUT/(p.stem+'_obstruction.json')).write_text(json.dumps(out,indent=2));print('OBSTRUCTION',g,'excluded',not unknown,'leaves',len(leaves),'unknown',unknown,'seconds',out['elapsed_seconds'])
if __name__=='__main__':main()
