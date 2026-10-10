#!/usr/bin/env python3
"""Rebuild all physical integer H actions. No numerical eigensolver is imported."""
import os,resource,time,json,gzip,hashlib
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
import numpy as np
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent;ROOT=P.parents[1];t0=time.time();rows=[]
def dot(a,b):return sum(int(x)*int(y) for x,y in zip(a,b))
def action(n,codes,c):
 lookup=np.full(3**n,-1,dtype=np.int32);lookup[codes]=np.arange(len(codes),dtype=np.int32)
 out=np.zeros(len(c),dtype=np.int64)
 for a in range(n):
  b=(a+1)%n;ma=(codes//3**a)%3-1;mb=(codes//3**b)%3-1
  out+=ma*mb*c
  for sign in (-1,1):
   ok=(abs(ma+sign)<=1)&(abs(mb-sign)<=1)
   target=lookup[codes[ok]+sign*(3**a-3**b)]
   assert np.all(target>=0) and len(np.unique(target))==len(target)
   out[target]+=c[ok]
 return out
def sector(n,m):
 ids=np.arange(3**n,dtype=np.int64);mag=np.zeros(len(ids),dtype=np.int8)
 for a in range(n):mag+=(ids//3**a)%3-1
 return ids[mag==m]
def report(n,m,codes,c,name,sgn=None):
 assert len(codes)==len(c) and np.max(np.abs(c))<10**10
 assert 3*n*int(np.max(np.abs(c)))<2**63
 if sgn is not None:
  lookup=np.full(3**n,-1,dtype=np.int32);lookup[codes]=np.arange(len(codes))
  rot=lookup[(codes%3)*3**(n-1)+codes//3]
  assert np.array_equal(c[rot],sgn*c)
 hc=action(n,codes,c);nn=dot(c,c);en=dot(c,hc);rho=F(en,nn)
 assert nn>0 and np.max(np.abs(hc))<10**12
 return {'name':name,'Sz':m,'momentum_sign':sgn,'sector_dimension':len(codes),'nonzero_support':int(np.count_nonzero(c)),'full_H_action_support':int(np.count_nonzero(hc)),'norm_square':str(nn),'energy_form':str(en),'Rayleigh':str(rho),'Rayleigh_display':float(rho),'coefficient_sha256':hashlib.sha256(np.asarray(c,dtype='<i8').tobytes()).hexdigest(),'H_action_sha256':hashlib.sha256(np.asarray(hc,dtype='<i8').tobytes()).hexdigest()}
for n in (6,8):
 data=json.loads((ROOT/f'research_20261010/nonperturbative_mps_assessment/trial_n{n}.json').read_text());c=np.array(data['coefficients'],dtype=np.int64);codes=sector(n,0)
 rows.append({'n':n,'states':[report(n,0,codes,c,'archived_ground_proposal')],'orthogonal_trial_count':1})
for n in (10,12):
 c0codes=sector(n,0);c1codes=sector(n,1)
 with gzip.open(P/f'trial_n{n}_sz0.json.gz','rt') as f:c0=np.array(json.load(f)['coefficients'],dtype=np.int64)
 with gzip.open(P/f'trial_n{n}_sz1.json.gz','rt') as f:c1=np.array(json.load(f)['coefficients'],dtype=np.int64)
 states=[report(n,0,c0codes,c0,'momentum_zero_Sz0',1),report(n,1,c1codes,c1,'momentum_pi_Sz1',-1)]
 minus_codes=3**n-1-c1codes[::-1];minus=c1[::-1]
 states.append(report(n,-1,minus_codes,minus,'spin_flipped_Sz_minus1',-1))
 assert states[1]['Rayleigh']==states[2]['Rayleigh']
 lookup=np.full(3**n,-1,dtype=np.int32);lookup[c0codes]=np.arange(len(c0codes));lower=np.zeros(len(c0codes),dtype=np.int64)
 for a in range(n):
  ok=(c1codes//3**a)%3>0;target=lookup[c1codes[ok]-3**a]
  assert len(np.unique(target))==len(target) and np.all(target>=0)
  lower[target]+=c1[ok]
 assert dot(c0,lower)==0
 states.append(report(n,0,c0codes,lower,'lowered_momentum_pi_Sz0',-1))
 # Different Sz sectors are disjoint. Only common-sector pair has exact zero dot.
 rows.append({'n':n,'states':states,'orthogonal_trial_count':4,'common_sector_cross_inner_product':'0','other_orthogonality':'different total Sz sectors','full_hilbert_dimension':3**n,'lowering_convention':'sum local lowering divided by sqrt(2), an irrelevant common scalar','source_vectors':2,'derived_vectors':2})
result={'status':'PASS exact physical Hamiltonian actions and mutual orthogonality','model':'periodic unit-coupling spin1 Heisenberg H=sum_j S_j dot S_(j+1), n microscopic spins; no extensive energy shift','rows':rows,'seconds':time.time()-t0,'cpu_seconds':time.process_time(),'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'exact_trial_data.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
