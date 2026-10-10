"""Improve existing exact ground certificates using local relative-form tails."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,argparse
from fractions import Fraction as F
from pathlib import Path
from local_relative_bound import optimize_bound,update_ground,trace,exp_bounds,down,replay
OUT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--g',default='1/10');ap.add_argument('--spin',default='1');args=ap.parse_args()
 s,g=F(args.spin),F(args.g)
 inp=OUT/(f'certificate_s{s}_W1_g{g}_k0.json'.replace('/','d'))
 orig=json.loads(inp.read_text());rs=[]
 for r in orig['ground_certificates']:
  rs.append(update_ground(r,optimize_bound(s,g,'chain',r['M'])))
 results=[]
 for bi in range(8,41):
  b=F(bi,2);r1,r2=rs
  _,q1,t1=trace(r1,b);_,q2,t2=trace(r2,b)
  shift=F(r2['ground_upper'])-2*F(r1['ground_upper'])
  S=down(exp_bounds(-b*shift)[0]/q1**2);T=down(1/q2**2)
  boot=replay(str(S),str(T),2,str(b))
  result=dict(beta=str(b),S_lower=str(S),T_lower=str(T),S_display=float(S),T_display=float(T),bootstrap=boot)
  results.append(result)
  if boot['status'].startswith('accepted'):print('ACCEPT',b,float(S),float(T),boot.get('conditional_gap_lower_rational'),flush=True)
 out=dict(ground_certificates=rs,seeds=results)
 (OUT/(f'chain_relative_s{s}_g{g}.json'.replace('/','d'))).write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
