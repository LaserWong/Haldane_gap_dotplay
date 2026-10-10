#!/usr/bin/env python3
"""All-beta exclusion audit from fresh D26 output and full-basis trial action."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,itertools as it,time,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];SRC=P.parent/'nonperturbative_mps_assessment';t0=time.time()
assert hashlib.sha256((SRC/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='95a37af759e80d9030b2f99ac7d86c26b6cd6085e5746a883514b9d66b7e4eb7'
manifest=json.loads((SRC/'MANIFEST_SHA256.json').read_text())
for file,sha in manifest.items():assert hashlib.sha256((SRC/file).read_bytes()).hexdigest()==sha,file
assert (P/'d26_fresh.out').read_bytes()==(SRC/'mps_small.out').read_bytes()
uv=dict(line.split('=') for line in (P/'d26_fresh.out').read_text().splitlines())
producer={r['n']:r for r in json.loads((SRC/'uniform_screen.json').read_text())['rows']}

def exponential(x):
 # Positive Taylor series with a geometric remainder. No float enters a decision.
 if x<0:
  lo,hi=exponential(-x);return 1/hi,1/lo
 assert 0<=x<60
 term=F(1);partial=term
 for k in range(1,121):
  term*=x/k;partial+=term
 nextterm=term*x/121
 return partial,partial+nextterm/(1-x/122)
def G(x):
 assert 0<x<=1
 return (x*x+2*x-1)/(2*x*x)
def upper(x):
 scale=10**18
 return F(-((-x.numerator*scale)//x.denominator),scale)
def root_upper(x):
 assert x>=0
 scale=10**24;floor=isqrt((x.numerator*scale*scale)//x.denominator)
 u=F(floor+1,scale);assert u*u>x
 return u
def replay(a,b,canonical=False):
 if canonical:
  a,b=upper(a*root_upper(b)),upper(a*a*b)
 records=[]
 for k in range(12):
  assert max(1-a,1-b)>F(1,100)
  records.append({'round':k,'a_upper':str(a),'b_upper':str(b)})
  x=a*a*b;a=upper(G(x))
  if a<=0:return records+[{'failed_direction':1,'round':k+1,'argument':str(x),'output':str(a)}]
  x=b*b*a;b=upper(G(x))
  if b<=0:return records+[{'failed_direction':2,'round':k+1,'argument':str(x),'output':str(b)}]
 raise AssertionError('failure not established')
rows=[]
for n,cut,jbound in [(6,F(3,4),F(29,50)),(8,F(31,40),F(71,100))]:
 trial=json.loads((SRC/f'trial_n{n}.json').read_text())
 basis=list(it.product(range(3),repeat=n));loc={v:i for i,v in enumerate(basis)}
 sz0=[v for v in basis if sum(v)==n]
 assert len(trial['coefficients'])==len(sz0)
 vec=[0]*len(basis)
 for v,c in zip(sz0,trial['coefficients']):vec[loc[v]]=c
 Hv=[0]*len(basis);trace=0
 for i,v in enumerate(basis):
  diag=sum((v[a]-1)*(v[(a+1)%n]-1) for a in range(n));trace+=diag
  Hv[i]+=diag*vec[i]
  if not vec[i]:continue
  for a in range(n):
   b=(a+1)%n
   for sign in [-1,1]:
    if 0<=v[a]+sign<=2 and 0<=v[b]-sign<=2:
     w=list(v);w[a]+=sign;w[b]-=sign;Hv[loc[tuple(w)]]+=vec[i]
 assert trace==0
 alpha=F(sum(x*y for x,y in zip(vec,Hv)),sum(x*x for x in vec))
 Rbig=2*n*F(int(uv[f'U{2*n}']),int(uv[f'V{2*n}']))
 assert str(alpha)==producer[n]['small_exact_Rayleigh']
 assert str(Rbig)==producer[n]['large_exact_Rayleigh']
 delta=Rbig-2*alpha
 assert delta>0 and Rbig<0
 left=exponential(-2*cut*Rbig)[1]/3**(4*n)
 right=exponential(-2*cut*delta)[1]
 assert max(left,right)<jbound
 first=G(jbound)
 immediate=replay(first,G(first),True)
 assert immediate[-1]['round']==(1 if n==6 else 5)
 early=exponential(-Rbig)[1]/3**(4*n)
 late=exponential(-delta)[1]
 assert early<F(2,5) and G(F(2,5))<0 and late<F(4,5)
 second=G(F(16,25)*first)
 fixed=replay(first,second)
 assert fixed[-1]['round']==(1 if n==6 else 2)
 # Check every positive full-cycle state preceding fixed-order failure. Any
 # later one-off conversion is also dominated by a failed canonical replay.
 delayed=[]
 for rec in fixed[:-1]:
  a,b=F(rec['a_upper']),F(rec['b_upper'])
  assert a<=first and b<=second
  delayed.append({'time_first_cycles':rec['round'],'canonical_replay':replay(a,b,True)})
 # Check the archived beta demonstration separately from the all-beta proof.
 cert=json.loads((R/f'heat_trace/results/A_L{n}_I_full/certificate.json').read_text())
 uppertrace=cert['interval']['upper'];U=F(int(uppertrace['numerator']),int(uppertrace['denominator']))
 lowernum=exponential(-21*(Rbig+2*n*F(700741,500000)))[0]
 lowerJ=lowernum/U**4
 assert lowerJ<F(2,5)
 rows.append({'n':n,'full_trial_action_dimension':3**n,'nonzero_trial_coefficients':sum(v!=0 for v in vec),'trace_H_exact':trace,'small_rayleigh':str(alpha),'large_rayleigh':str(Rbig),'delta':str(delta),'delta_display':float(delta),'beta_split':str(cut),'J_upper':str(jbound),'J_left_display':float(left),'J_right_display':float(right),'canonical_replay':immediate,'early_J_display':float(early),'late_C_display':float(late),'fixed_time_first':fixed,'delayed_conversion_checks':delayed,'archived_cooling_J_display':float(lowerJ)})
result={'status':'PASS','scope':'fixed D26 one-Rayleigh numerator at L12/16, denominators L6/8, specified G recursions and optional one-off delayed canonical conversion at completed cycles','frozen_files_verified':len(manifest),'rows':rows,'seconds':time.time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'uniform_independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
for r in rows:print(r['n'],r['delta_display'],r['J_upper'],r['archived_cooling_J_display'])
