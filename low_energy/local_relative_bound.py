"""Exact finite-local-matrix relative form bounds for coupled dimers.
Certification is fraction-free exact inertia; floating eigvalsh only proposes b.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from fractions import Fraction as F
from functools import reduce
import math,json,sys,time,argparse
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
from dimer_subspace import dimer_local
from ground_tail import OUT, exp_bounds, down, replay
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'original/Haldane_extensions/code'))
from inertia_trace import inertia

def local_bound(s,g,a,kind='bilayer',digits=12):
 labels,weights,kernels=dimer_local(F(s));n=len(labels);D=n*n
 G=[weights[i]*weights[j] for i in range(n) for j in range(n)]
 H=np.zeros((D,D),dtype=object)
 for p in range(n):
  for q in range(n):
   c=p*n+q
   H[c,c]+=a*(labels[p][2]+labels[q][2])
   for aa,bb in ([(0,0),(1,1)] if kind=='bilayer' else [(1,0)]):
    for r,t,v in kernels[aa,bb][c]:H[r*n+t,c]+=g*v
 weighted=np.empty((D,D),dtype=float)
 for i in range(D):
  for j in range(D):weighted[i,j]=float(H[i,j])*math.sqrt(G[i]/G[j])
 emin=eigvalsh(weighted,subset_by_index=[0,0],check_finite=False)[0]
 b=F(math.ceil(max(0,-emin)*10**digits)+1,10**digits)
 for i in range(D):H[i,i]+=b
 scale=reduce(math.lcm,[F(x).denominator for x in H.flat],1)
 A=np.array([[int(H[i,j]*scale)*G[i] for j in range(D)] for i in range(D)],dtype=object)
 assert np.array_equal(A,A.T)
 neg,zero=inertia(A)
 assert neg==0 and zero==0
 return dict(spin=str(s),coupling=str(g),a=str(a),b=str(b),local_dimension=D,
 exact_inertia=[neg,zero,D-neg-zero],kind=kind,
 inequality='g*v + a*(h_i+h_j) + b*I is strictly positive definite',
 arithmetic='Rational orthogonal dimer basis; exact integer congruence and fraction-free inertia')

def optimize_bound(s,g,model,N,W=1,grid=100):
 # Optimize second spectral-bin threshold alpha-B. Proposal loop uses
 # small local float eigenvalues; only winning candidates certified exactly.
 labels,weights,kernels=dimer_local(F(s));n=len(labels);D=n*n
 G=np.array([weights[i]*weights[j] for i in range(n) for j in range(n)])
 diag=np.array([float(labels[i][2]+labels[j][2]) for i in range(n) for j in range(n)])
 kind='bilayer' if model=='bilayer' else 'single'
 v=np.zeros((D,D))
 for c in range(D):
  for aa,bb in ([(0,0),(1,1)] if kind=='bilayer' else [(1,0)]):
   for p,q,x in kernels[aa,bb][c]: v[p*n+q,c]+=float(g*x)*math.sqrt(G[p*n+q]/G[c])
 degree=4 if model=='bilayer' else 2
 edges=2*N if model=='bilayer' else N
 proposals=[]
 for ai in range(1,grid):
  a=F(ai,grid*degree)
  mine=eigvalsh(v+float(a)*np.diag(diag),subset_by_index=[0,0],check_finite=False)[0]
  b=max(0,-mine);cut=1-degree*float(a)-edges*b
  proposals.append((cut,a))
 _,a=max(proposals)
 r=local_bound(s,g,a,kind)
 alpha=1-degree*a;B=edges*F(r['b'])
 return dict(alpha=str(alpha),B=str(B),second_shift_lower=str(alpha-B),local_certificate=r,
 full_inequality='H >= E00*I + alpha*(H0-E00*I) - B*I',
 ordered_bins='lambda_j(H) >= E00 + alpha*(lambda_j(H0)-E00) - B, by min-max')

def update_ground(rec,bound):
 rec=rec.copy();rec['relative_form_bound']=bound
 a=F(rec['E00'])+F(bound['second_shift_lower']);rho=F(rec['exact_rayleigh']);r2=F(rec['exact_residual_squared'])
 assert rho<a
 elo=rho-r2/(a-rho)
 rec['second_eigenvalue_lower']=str(a);rec['ground_lower']=str(elo)
 rec['ground_lower_display']=float(elo);rec['ground_width_display']=float(rho-elo)
 return rec

def trace(rec,beta):
 beta=F(beta);s=F(rec['s']);N=rec.get('N_dimers',rec.get('M',1)*rec.get('W',1))
 elo=F(rec['ground_lower']);ehi=F(rec['ground_upper']);E00=F(rec['E00'])
 if 'relative_form_bound' in rec:
  b=rec['relative_form_bound'];alpha=F(b['alpha']);B=F(b['B'])
 else:alpha=F(1);B=-F(rec['Vmin'])
 assert 0<alpha<=1 and B>=0, 'Ordered-bin bound requires positive alpha and nonnegative B'
 z=F(1)
 for j in range(1,int(2*s)+1):z+=(2*j+1)*exp_bounds(-beta*alpha*F(j*(j+1),2))[1]
 tail=exp_bounds(-beta*(E00-B-ehi))[1]*(z**N-1)
 upper=exp_bounds(beta*(ehi-elo))[1]+tail
 return F(1),upper,tail

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--spin',default='1/2');ap.add_argument('--g',default='1/50');ap.add_argument('--dimers',type=int,default=16);ap.add_argument('--model',default='bilayer');args=ap.parse_args()
 r=optimize_bound(F(args.spin),F(args.g),args.model,args.dimers)
 path=OUT/(f'relative_{args.model}_s{args.spin}_g{args.g}_N{args.dimers}.json'.replace('/','d'))
 path.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
if __name__=='__main__':main()
