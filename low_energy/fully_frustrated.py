"""Nonperturbative fully-frustrated bilayer J plus straight-only perturbation.
Completeness/tail reference uses exact occupancy-resolved weighted-star bounds.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import math,json,sys,argparse,time
import numpy as np
from scipy.optimize import minimize_scalar
from dimer_subspace import certify_sparse
from local_relative_bound import local_bound
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent/'seed_size/code'))
from certified_core import exp_bounds,down,up,G
from correlated_seeds import replay3

def rung_edges(nx,ny):
 edges=defaultdict(int);idx=lambda x,y:(x%nx)*ny+(y%ny)
 for x in range(nx):
  for y in range(ny):
   for dx,dy in [(1,0),(0,1)]:
    i,j=sorted([idx(x,y),idx(x+dx,y+dy)]);assert i!=j;edges[i,j]+=1
 return [(i,j,w) for (i,j),w in edges.items()]

def weak_bonds(nx,ny,J,eps):
 bonds=[]
 for i,j,w in rung_edges(nx,ny):
  for aa in range(2):
   for bb in range(2):bonds.append((i,aa,j,bb,w*(J+(eps if aa==bb else 0))))
 return bonds

def occupancy_bins(nx,ny,J):
 N=nx*ny;edges=rung_edges(nx,ny);hist=defaultdict(int)
 for mask in range(1<<N):
  q=mask.bit_count();incident=[0]*N;E=0
  for i,j,w in edges:
   if mask>>i&1 and mask>>j&1:
    E+=w;incident[i]=max(incident[i],w);incident[j]=max(incident[j],w)
  C=F(2*E+sum(incident),2)
  f=q-J*C
  hist[q,f]+=3**q
 rows=[dict(q=q,energy_lower=str(f),multiplicity=m) for (q,f),m in sorted(hist.items())]
 assert sum(r['multiplicity'] for r in rows)==4**N
 assert all(F(r['energy_lower'])>0 for r in rows if r['q']>0)
 return rows

def optimize_comparison(N,eps,bins):
 qs=np.array([r['q'] for r in bins if r['q']]);es=np.array([float(F(r['energy_lower'])) for r in bins if r['q']])
 def fun(a):
  b=math.sqrt(a*a-a*float(eps)+float(eps)**2)-a+float(eps)/2
  return -(min(es-4*a*qs)-2*N*b)
 opt=minimize_scalar(fun,bounds=(0,.249),method='bounded')
 a=F(round(opt.x*10**9),10**9)
 if fun(0)<=fun(float(a)):a=F(0)
 local=local_bound(F(1,2),eps,a,'bilayer')
 b=F(local['b']);B=2*N*b
 ecut=min(F(r['energy_lower'])-4*a*r['q'] for r in bins if r['q'])
 assert ecut>0, 'Vacuum must remain unique lowest reference bin'
 return dict(status='exact_occupancy_star_plus_local_PSD_reference',J='3/10',a=str(a),b=str(b),B=str(B),
  second_shift_lower=str(ecut-B),local_certificate=local,
  bins=bins,
  proof='For each occupied rung set A, Hff >= |A|-J*(active edge weight+half sum maximal incident active weight). Each bin has exact rank3^|A|. Add local epsilon comparison -4aQ-B. Vacuum unique lowest reference bin; ordered min-max then certifies all omitted states.')

def trace(rec,beta):
 beta=F(beta);ref=rec['reference_certificate'];a=F(ref['a']);B=F(ref['B'])
 elo=F(rec['ground_lower']);ehi=F(rec['ground_upper']);E00=F(rec['E00'])
 total=F(0)
 for row in ref['bins']:
  if row['q']==0:continue
  exponent=-beta*(E00+F(row['energy_lower'])-4*a*row['q']-B-ehi)
  total=up(total+row['multiplicity']*exp_bounds(exponent)[1])
 return up(exp_bounds(beta*(ehi-elo))[1]+total),total

def seed3(rs,beta):
 beta=F(beta);U=[F(r['ground_upper']) for r in rs];qt=[trace(r,beta) for r in rs];q=[v[0] for v in qt]
 A=down(exp_bounds(-beta*(U[1]-2*U[0]))[0]/q[0]**2)
 B=down(exp_bounds(-beta*(U[2]-2*U[1]))[0]/q[1]**2)
 C=down(1/q[2]**2)
 J1=down(exp_bounds(-beta*(2*U[2]-8*U[0]))[0]/q[0]**8)
 J2=down(exp_bounds(-beta*(4*U[2]-8*U[1]))[0]/q[1]**8)
 A1=down(G(J1))
 if A1<=0:boot={'accepted':False,'failure':'first spatial update'}
 else:
  B1=down(G(J2*A1))
  if B1<=0:boot={'accepted':False,'failure':'second spatial update'}
  else:
   C1=down(G(C**4*A1**2*B1))
   boot=replay3(A1,B1,C1,4,4,2*beta) if C1>0 else {'accepted':False,'failure':'thermal update'}
 return dict(beta=str(beta),A_lower=str(A),B_lower=str(B),C_lower=str(C),J1_lower=str(J1),J2_lower=str(J2),
  purity_displays=list(map(float,[A,B,C])),tail_displays=[float(v[1]) for v in qt],bootstrap=boot)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--epsilon',default='1/200');ap.add_argument('--depth',type=int,default=0);ap.add_argument('--betas',default='16,20,24,28,32,40,48,64');args=ap.parse_args()
 J=F(3,10);eps=F(args.epsilon);rs=[];t0=time.monotonic()
 for nx,ny in [(2,2),(4,2),(4,4)]:
  bins=occupancy_bins(nx,ny,J);ref=optimize_comparison(nx*ny,eps,bins)
  tag=f'ff_{nx}x{ny}_J{J}_eps{eps}_'+(f'depth{args.depth}' if args.depth else 'q2');tag=tag.replace('/','d');path=OUT/(tag+'_ground.json')
  r=json.loads(path.read_text()) if path.exists() else certify_sparse(F(1,2),nx*ny,weak_bonds(nx,ny,J,eps),tag=tag,reference_certificate=ref,support_depth=args.depth or None)
  r['nx']=nx;r['ny']=ny;rs.append(r)
  print('FFREFERENCE',nx,ny,'gap shift',float(F(ref['second_shift_lower'])),'a',ref['a'],'bins',len(bins),flush=True)
 seeds=[]
 for beta in map(F,args.betas.split(',')):
  r=seed3(rs,beta);seeds.append(r);b=r['bootstrap']
  print('FFSEED',beta,r['purity_displays'],b.get('accepted'),b.get('gap_lower'),b.get('n'),flush=True)
 out=dict(J=str(J),epsilon=str(eps),perturbation='straight J+epsilon, crossed J; unit rungs',ground_certificates=rs,seeds=seeds,total_seconds=time.monotonic()-t0)
 (OUT/(f'ff_seed_J{J}_eps{eps}_depth{args.depth}.json'.replace('/','d'))).write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
