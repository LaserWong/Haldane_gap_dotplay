"""Exact cancelled first-step seeds for producer frontier records."""
import os
for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[x]='1'
import json,sys,argparse,time
from pathlib import Path
from fractions import Fraction as F
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'seed_size/code'))
from certified_core import exp_bounds,G,up
sys.path.insert(0,str(ROOT/'low_energy'))
from ground_tail import replay,down

def trace(r,b):
    a=F(r['relative_form_bound']['alpha']);B=F(r['relative_form_bound']['B']);N=r['N_dimers']
    z=1+3*exp_bounds(-b*a)[1]+5*exp_bounds(-3*b*a)[1]
    tail=up(exp_bounds(-b*(F(r['E00'])-B-F(r['ground_upper'])))[1]*(z**N-1))
    return up(exp_bounds(b*(F(r['ground_upper'])-F(r['ground_lower'])))[1]+tail),tail

def seeds(record,betas):
    rs=record['ground_certificates'];n=rs[0]['N_dimers'];shift=F(rs[1]['ground_upper'])-2*F(rs[0]['ground_upper']);rows=[]
    for beta in map(F,betas):
        q1,t1=trace(rs[0],beta);q2,t2=trace(rs[1],beta)
        S=down(exp_bounds(-beta*shift)[0]/q1**2);T=down(1/q2**2)
        J=down(exp_bounds(-2*beta*shift)[0]/q1**4)
        A=down(G(J)) if J>0 else F(-1)
        B=down(G(T*T*A)) if T>0 and A>0 else F(-1)
        boot=replay(str(A),str(B),2*n,str(2*beta)) if A>0 and B>0 else dict(status='rejected_first_correlated_step')
        rows.append(dict(beta=str(beta),S_lower=str(S),T_lower=str(T),J_direct_lower=str(J),first_S_lower=str(A),first_T_lower=str(B),tail_upper=[str(t1),str(t2)],bootstrap=boot))
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--betas',default=','.join(map(str,range(32,161,2))));args=ap.parse_args()
    path=Path(args.source).resolve();rec=json.loads(path.read_text());rows=seeds(rec,args.betas.split(','));good=[r for r in rows if r['bootstrap']['status'].startswith('accepted')]
    best=max(good,key=lambda r:F(r['bootstrap']['conditional_gap_lower_rational'])) if good else None
    out=dict(status='exact_arithmetic_producer_candidate_requires_independent_audit',source=str(path.relative_to(ROOT)),g=rec['g'],n=rec['n'],depth=rec['depth'],ground_certificates=rec['ground_certificates'],seeds=rows,best=best)
    (OUT/(path.stem+'_correlated.json')).write_text(json.dumps(out,indent=2))
    print('CORRELATED',rec['g'],rec['n'],rec['depth'],'accepted',len(good),'best',None if best is None else {'beta':best['beta'],'gap':float(F(best['bootstrap']['conditional_gap_lower_rational'])),'L0':best['bootstrap']['final_n']},flush=True)
if __name__=='__main__':main()
