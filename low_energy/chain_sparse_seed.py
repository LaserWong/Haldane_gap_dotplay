"""Longer initial cells using sparse dimer/Krylov-support ground certificates."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,argparse,time
from fractions import Fraction as F
from pathlib import Path
from dimer_subspace import certify_sparse,columnar_bonds
from local_relative_bound import optimize_bound,update_ground,trace,exp_bounds,down,replay
OUT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--spin',default='1');ap.add_argument('--g',default='1/10');ap.add_argument('--n',type=int,default=4);ap.add_argument('--depth',type=int,default=2);ap.add_argument('--betas',default='8,12,16,20,24,32,40');args=ap.parse_args()
 s,g=F(args.spin),F(args.g);rs=[]
 for M in [args.n,2*args.n]:
  bound=optimize_bound(s,g,'chain',M)
  tag=f'chain_s{s}_M{M}_g{g}_depth{args.depth}'.replace('/','d');path=OUT/(tag+'_ground.json')
  r=json.loads(path.read_text()) if path.exists() else certify_sparse(s,M,columnar_bonds(M,1,g,F(0)),tag=tag,relative_bound=bound,support_depth=args.depth)
  r['M']=M;r['W']=1;rs.append(r)
 results=[]
 for b in map(F,args.betas.split(',')):
  _,q1,t1=trace(rs[0],b);_,q2,t2=trace(rs[1],b)
  shift=F(rs[1]['ground_upper'])-2*F(rs[0]['ground_upper'])
  S=down(exp_bounds(-b*shift)[0]/q1**2);T=down(1/q2**2)
  boot=replay(str(S),str(T),args.n,str(b))
  r=dict(beta=str(b),S_lower=str(S),T_lower=str(T),S_display=float(S),T_display=float(T),tails_display=[float(t1),float(t2)],bootstrap=boot)
  results.append(r);print('CHAINSEED',b,float(S),float(T),boot['status'],boot.get('conditional_gap_lower_rational'),flush=True)
 (OUT/(f'chain_sparse_s{s}_g{g}_n{args.n}_depth{args.depth}.json'.replace('/','d'))).write_text(json.dumps(dict(ground_certificates=rs,seeds=results),indent=2))
if __name__=='__main__':main()
