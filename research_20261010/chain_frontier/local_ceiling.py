"""Exact affine test-vector ceiling for all local comparison parameters.
A floating optimizer only proposes two dyadic local test vectors; their rational
Rayleigh lines bound lambda_min from ABOVE at every a.
"""
import os
for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[x]='1'
import sys,json,argparse,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize_scalar
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'low_energy'))
from dimer_subspace import dimer_local
sys.path.insert(0,str(ROOT/'seed_size/code'))
from certified_core import exp_bounds,up

def ceiling(g,N):
    labels,weights,kernels=dimer_local(F(1));W=[x*y for x in weights for y in weights];h=[x[2]+y[2] for x in labels for y in labels]
    K=kernels[1,0];V=np.zeros((81,81));sq=np.sqrt(W)
    for c,row in enumerate(K):
        for r,t,v in row:V[9*r+t,c]=float(g*v)*sq[9*r+t]/sq[c]
    def solve(a):return eigh(V+a*np.diag(list(map(float,h))),subset_by_index=[0,0],check_finite=False)
    opt=minimize_scalar(lambda a:-(1-2*a+N*solve(a)[0][0]),bounds=(0.,.499999),method='bounded',options={'xatol':1e-13})
    rows=[]
    for a in [opt.x-.001,opt.x+.001]:
        _,vec=solve(a);u=[round(float(x/y)*2**44) for x,y in zip(vec[:,0],sq)]
        norm=sum(w*x*x for w,x in zip(W,u))
        eh=F(sum(w*x*x*e for w,x,e in zip(W,u,h)),norm)
        ev=sum((g*v*W[9*r+t]*u[9*r+t]*u[c] for c,row in enumerate(K) for r,t,v in row),F(0))/norm
        rows.append(dict(a_proposal=a,vector=list(map(int,u)),norm=str(norm),h_expectation=str(eh),gV_expectation=str(ev),intercept=str(1+N*ev),slope=str(N*eh-2)))
    p,m=rows;cp,cm=F(p['intercept']),F(m['intercept']);sp,sm=F(p['slope']),F(m['slope']);assert sp>0>sm
    across=(cm-cp)/(sp-sm);bound=cp+sp*across
    return dict(g=str(g),N=N,local_dimension=81,lines=rows,intersection_a=str(across),cutoff_shift_upper=str(bound),cutoff_shift_upper_display=float(bound),proof='For each exact dyadic vector u, lambda_min(gV+a h)<=<gV>+a<h>. The target 1-2a+N lambda_min is at most the minimum of two opposite-slope affine lines, whose global maximum is their intersection.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--g',default='7/40');ap.add_argument('--N',type=int,default=8);ap.add_argument('--record');args=ap.parse_args()
    out=ceiling(F(args.g),args.N)
    if args.record:
        rec=json.loads(Path(args.record).read_text());r1,r2=rec['ground_certificates'];assert r2['N_dimers']==args.N
        delta=F(r2['E00'])+F(out['cutoff_shift_upper'])-F(r2['ground_lower']);kappa=F(r2['ground_lower'])-2*F(r1['ground_upper']);B=F(128)
        qfloor=1+3*args.N*exp_bounds(-B*delta)[0]
        thermal_upper=up(1/qfloor**2);Jupper=exp_bounds(-2*B*kappa)[1]
        out['all_beta_obstruction']=dict(status='exact_candidate_requires_independent_audit',beta_split=str(B),delta_upper=str(delta),delta_upper_display=float(delta),curvature_lower=str(kappa),curvature_lower_display=float(kappa),thermal_upper_for_beta_below_split=str(thermal_upper),thermal_upper_display=float(thermal_upper),J_upper_for_beta_above_split=str(Jupper),J_upper_display=float(Jupper),passed=bool(delta>=0 and kappa>0 and thermal_upper<=F(1,2) and Jupper<=F(1,2)),scope='Every beta>0, every local a with a valid positive-alpha comparison, and arbitrarily sharp ground refinement within the stored ground intervals. Excludes standard and cancelled-first-step ground-only numerator plus independent dimer-bin tail recipes for this seed geometry; not physical gaplessness.')
    path=OUT/f'local_ceiling_g{str(F(args.g)).replace("/","d")}_N{args.N}.json';path.write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='lines'},indent=2))
if __name__=='__main__':main()
