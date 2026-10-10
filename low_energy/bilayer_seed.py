"""Feed exact sparse-support heat traces to the audited three-purity replay."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from fractions import Fraction as F
from pathlib import Path
import sys,json,argparse,time
from dimer_subspace import certify_sparse,bilayer_bonds
from local_relative_bound import optimize_bound,update_ground,trace,exp_bounds,down
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent/'two_d_theory'))
from three_purity_certificate import replay

def seed3(r22,r42,r44,beta):
 beta=F(beta)
 _,q22,t22=trace(r22,beta);_,q42,t42=trace(r42,beta);_,q44,t44=trace(r44,beta)
 c1=F(r42['ground_upper'])-2*F(r22['ground_upper'])
 c2=F(r44['ground_upper'])-2*F(r42['ground_upper'])
 A=down(exp_bounds(-beta*c1)[0]/q22**2,digits=15)
 B=down(exp_bounds(-beta*c2)[0]/q42**2,digits=15)
 C=down(1/q44**2,digits=15)
 boot=replay(A,B,C,n=2,m=2,beta=beta,rounds=32,digits=18)
 return dict(beta=str(beta),A_lower=str(A),B_lower=str(B),C_lower=str(C),
  A_lower_display=float(A),B_lower_display=float(B),C_lower_display=float(C),
  tails_upper_display=[float(t22),float(t42),float(t44)],bootstrap=boot)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--g',default='1/100');ap.add_argument('--spin',default='1/2');ap.add_argument('--betas',default='10,12,16,20,24,32');ap.add_argument('--relative',action='store_true');ap.add_argument('--max-excited',type=int,default=2);args=ap.parse_args()
 s=F(args.spin);g=F(args.g);rs=[];t0=time.monotonic()
 for nx,ny in [(2,2),(4,2),(4,4)]:
  tag=f'bilayer_s{s}_{nx}x{ny}_g{g}_k{g}_q{args.max_excited}'.replace('/','d')
  path=OUT/(tag+'_ground.json')
  bound=optimize_bound(s,g,'bilayer',nx*ny) if args.relative else None
  r=json.loads(path.read_text()) if path.exists() else certify_sparse(s,nx*ny,bilayer_bonds(nx,ny,g,g),args.max_excited,tag=tag,relative_bound=bound)
  if args.relative:r=update_ground(r,bound)
  rs.append(r)
 seeds=[]
 for b in args.betas.split(','):
  r=seed3(*rs,F(b));seeds.append(r)
  print('SEED3',b,r['A_lower_display'],r['B_lower_display'],r['C_lower_display'],r['bootstrap'],flush=True)
 out=dict(status='exact_rational_physical_heat_trace_inputs_and_three_purity_replay',spin=str(s),g=str(g),
 graph='Square bilayer, unit AF rungs, positive equal x/y AF intralayer coupling, periodic with two parallel bonds in length-2 directions',
 ground_certificates=rs,seeds=seeds,total_seconds=time.monotonic()-t0)
 path=OUT/(f'bilayer_seed_s{s}_g{g}_relative{args.relative}_q{args.max_excited}.json'.replace('/','d'));path.write_text(json.dumps(out,indent=2));print('SAVED',path)
if __name__=='__main__':main()
