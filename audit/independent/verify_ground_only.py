"""Independent exact replay of ground-only certificates, without original modules or ED."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math, hashlib
import numpy as np
from verify_baseline import exp_interval, ceiling, floor, f
BASE=Path(__file__).resolve().parents[2]
OUT=BASE/'audit/independent'

def check_ground(r):
 s=F(r['s']);M=r['M'];W=r['W'];L=2*M*W;d=int(2*s+1);g=F(r['g']);k=F(r['k'])
 stem=f's{s}_M{M}_W{W}_g{g}_k{k}'.replace('/','d')
 p=BASE/'low_energy'/f'{stem}_ritz.npz'
 vec=list(map(int,np.load(p)['vector']))
 basis=[a for a in product(range(d),repeat=L) if sum(a)==s*L]
 assert len(basis)==len(vec)==r['ritz_sector_dimension']
 lookup={a:i for i,a in enumerate(basis)}
 index=lambda x,y,a:2*(W*(x%M)+y)+a
 strong=[(index(x,y,1),index(x+1,y,0),F(1)) for x in range(M) for y in range(W)]
 weak=[(index(x,y,0),index(x,y,1),g) for x in range(M) for y in range(W) if g]
 weak += [(index(x,y,a),index(x,y+1,a),k) for x in range(M) for y in range(W-1) for a in (0,1) if k]
 bonds=strong+weak
 scale=math.lcm(*[4*c.denominator for _,_,c in bonds])
 hv=[0]*len(vec)
 # Column action of the exact Hermitian Hamiltonian, using constant spin-1 and spin-1/2 ladder products.
 for c,(a,v) in enumerate(zip(basis,vec)):
  diag=sum(J*(a[i]-s)*(a[j]-s) for i,j,J in bonds)
  assert (diag*scale).denominator==1
  hv[c]+=int(diag*scale)*v
  for i,j,J in bonds:
   hopping=J*(F(1,2) if s==F(1,2) else 1)
   assert (hopping*scale).denominator==1
   for sign in (-1,1):
    if 0<=a[i]+sign<d and 0<=a[j]-sign<d:
     b=list(a);b[i]+=sign;b[j]-=sign
     hv[lookup[tuple(b)]]+=int(hopping*scale)*v
 norm=sum(x*x for x in vec)
 rho=F(sum(x*y for x,y in zip(vec,hv)),scale*norm)
 variance=F(sum(x*x for x in hv),scale*scale*norm)-rho*rho
 assert rho==F(r['exact_rayleigh']) and variance==F(r['exact_residual_squared'])
 E00=-M*W*s*(s+1)
 vmin=sum(-J*s*(s+1) if J>=0 else J*s*s for _,_,J in weak)
 lam1=E00+1+vmin
 assert E00==F(r['E00']) and vmin==F(r['Vmin']) and lam1==F(r['second_eigenvalue_lower'])
 assert lam1>E00 and rho<lam1
 lo=rho-variance/(lam1-rho)
 assert lo==F(r['ground_lower']) and rho==F(r['ground_upper'])
 # Every weak edge touches different strong dimers, establishing zero trial expectation.
 owner={site:j for j,(a,b,_) in enumerate(strong) for site in (a,b)}
 assert len(owner)==L
 assert all(owner[a]!=owner[b] for a,b,_ in weak)
 return {'M':M,'W':W,'dimension':d**L,'retained_vectors':1,'vector_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact_residual_squared_matches':True,'Temple_ground_enclosure_matches':True,'full_space_second_energy_bound':str(lam1),'product_trial_has_zero_weak_expectation':True}

def q_bounds(r,beta):
 s=F(r['s']);N=r['M']*r['W'];lo=F(r['ground_lower']);hi=F(r['ground_upper']);E=F(r['E00']);v=F(r['Vmin'])
 z=F(1)
 for j in range(1,int(2*s)+1): z+=(2*j+1)*exp_interval(-beta*F(j*(j+1),2))[1]
 tail=exp_interval(-beta*(E+v-hi))[1]*(z**N-1)
 return F(1),exp_interval(beta*(hi-lo))[1]+tail

def check(path):
 data=json.loads(path.read_text()); rec=data['ground_certificates']
 grounds=[check_ground(r) for r in rec]
 seeds=[]
 for r in data['seeds']:
  beta=F(r['beta']); _,b1=q_bounds(rec[0],beta);_,b2=q_bounds(rec[1],beta)
  shift=F(rec[1]['ground_upper'])-2*F(rec[0]['ground_upper'])
  S=floor(exp_interval(-beta*shift)[0]/b1**2);T=floor(1/b2**2)
  assert S==F(r['S_lower']) and T==F(r['T_lower'])
  recorded=r['bootstrap']
  p,q=1-S,1-T;n=rec[0]['M'];bb=beta
  for u in recorded['updates']:
   p=ceiling(f(1-(1-p)**2*(1-q)))
   assert p==F(u['p_upper'])
   q=ceiling(f(1-(1-q)**2*(1-p)))
   assert q==F(u['q_upper'])
   n*=2;bb*=2
  accepted=recorded['status']=='accepted_conditional_scalar_seed'
  if accepted:
   uu=max(p,q);gap=F(recorded['conditional_gap_lower_rational'])
   assert uu<=F(1,100) and n==recorded['final_n'] and bb==F(recorded['final_beta'])
   assert exp_interval(bb*gap)[1]<1/(5*uu)
  seeds.append({'beta':str(beta),'S_lower':str(S),'T_lower':str(T),'recorded_replay_matches':True,'accepted':accepted,'gap_lower':recorded.get('conditional_gap_lower_rational')})
 result={'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'grounds':grounds,'seeds':seeds,'status':'PASS: exact matrix action, full-spectrum Weyl completeness, Temple, tails, and scalar replay'}
 (OUT/(path.stem+'_audit.json')).write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 import sys
 for a in sys.argv[1:]:check(Path(a))
