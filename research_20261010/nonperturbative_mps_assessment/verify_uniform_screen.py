#!/usr/bin/env python3
"""Exact all-temperature recipe-specific exclusions, no eigensolver or spectrum."""
import os,resource,time,json,itertools,hashlib
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
def exp_interval(x):
 x=F(x)
 if x<0:
  l,u=exp_interval(-x);return 1/u,1/l
 assert x<100
 t=F(1);s=t
 for k in range(1,201):t=t*x/k;s+=t
 nxt=t*x/201
 return s,s+nxt/(1-x/202)
def sqrt_upper(x):
 assert x>=0
 M=10**30;k=isqrt(x.numerator*M*M//x.denominator)
 return F(k+1,M)
def up(x):
 M=10**20;return F(-((-x.numerator*M)//x.denominator),M)
def G(x):
 assert 0<x<=1
 return 1-(1-x)**2/(2*x*x)
def optimistic_replay(j):
 a=G(j);b=G(a) # optimistically allow C=1
 S=up(a*sqrt_upper(b));T=up(a*a*b)
 steps=[{'stage':'initial','S_upper':str(S),'T_upper':str(T)}]
 for k in range(30):
  assert max(1-S,1-T)>F(1,100)
  z=S*S*T
  S=up(G(z))
  if S<=0:return steps+[{'failure':'spatial','round':k+1,'argument_upper':str(z),'output_upper':str(S)}]
  z=T*T*S;T=up(G(z))
  if T<=0:return steps+[{'failure':'thermal','round':k+1,'argument_upper':str(z),'output_upper':str(T)}]
  steps.append({'round':k+1,'S_upper':str(S),'T_upper':str(T)})
 raise AssertionError('No failure')
for name,expected in {
 'audit/mps/build_mps.py':'693ded40630e851fda40986460b841bcfe3e48cf5ace665997f923ec7737ffdb',
 'audit/mps/mps_blocks.txt':'26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa',
}.items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
 assert json.loads((ROOT/'MANIFEST_SHA256.json').read_text())[name]==expected
t0=time.time();raw=dict(x.split('=') for x in (P/'mps_small.out').read_text().splitlines());rows=[]
for n,beta,jmax in ((6,F(3,4),F(58,100)),(8,F(31,40),F(71,100))):
 data=json.loads((P/f'trial_n{n}.json').read_text());c=data['coefficients']
 states=[v for v in itertools.product((-1,0,1),repeat=n) if sum(v)==0];idx={v:i for i,v in enumerate(states)}
 assert len(c)==len(states)
 norm=sum(v*v for v in c);energy=0
 for j,s in enumerate(states):
  for a in range(n):
   b=(a+1)%n;energy+=c[j]*c[j]*s[a]*s[b]
   for direction in (-1,1):
    if -1<=s[a]+direction<=1 and -1<=s[b]-direction<=1:
     v=list(s);v[a]+=direction;v[b]-=direction
     energy+=c[j]*c[idx[tuple(v)]]
 small_rho=F(energy,norm)
 U=int(raw[f'U{2*n}']);V=int(raw[f'V{2*n}']);assert V>0
 big_rho=2*n*F(U,V);delta=big_rho-2*small_rho
 assert big_rho<0 and small_rho<0 and delta>0
 # For beta<=cutoff: trace Jensen with Tr H=0. For beta>=cutoff: trial lower trace.
 low_beta_upper=exp_interval(-2*beta*big_rho)[1]/3**(4*n)
 high_beta_upper=exp_interval(-2*beta*delta)[1]
 assert max(low_beta_upper,high_beta_upper)<jmax
 steps=optimistic_replay(jmax)
 assert 'failure' in steps[-1]
 # A stronger screen also permits continued time-first cycles before conversion.
 # Below beta=1/2 the Jensen bound already makes the very first G nonpositive.
 j_early=exp_interval(-big_rho)[1]/3**(4*n)
 assert j_early<F(2,5) and G(F(2,5))<0
 # Above beta=1/2, C <= exp(-delta) < 4/5.
 c_late=exp_interval(-delta)[1];assert c_late<F(4,5)
 aa=G(jmax);bb=G(F(4,5)**2*aa)
 time_steps=[{'stage':'initial time-first','a_upper':str(aa),'b_upper':str(bb)}]
 for k in range(10):
  if bb<=0:
   time_steps.append({'failure':'initial second G','round':0});break
  zz=aa*aa*bb;aa=up(G(zz))
  if aa<=0:
   time_steps.append({'failure':'first direction','round':k+1,'argument_upper':str(zz),'output_upper':str(aa)});break
  zz=bb*bb*aa;bb=up(G(zz))
  if bb<=0:
   time_steps.append({'failure':'second direction','round':k+1,'argument_upper':str(zz),'output_upper':str(bb)});break
  time_steps.append({'round':k+1,'a_upper':str(aa),'b_upper':str(bb)})
 assert 'failure' in time_steps[-1]
 cert=json.loads((ROOT/f'heat_trace/results/A_L{n}_I_full/certificate.json').read_text())
 hi=cert['interval']['upper'];trup=F(int(hi['numerator']),int(hi['denominator']))
 shift=F(700741,500000);bs=F(21,2)
 ln,un=exp_interval(-2*bs*(big_rho+2*n*shift))
 # Original smaller beta bound; at 2 beta use ordinary cooling Z(2 beta)<=Z(beta)^2.
 jlo=ln/trup**4;clo=jlo
 rows.append({'n':n,'hilbert_small':3**n,'hilbert_large':3**(2*n),'MPS_bond_dimension':26,'numerator_trial_rank':1,'small_trial_support':len(c),'small_exact_Rayleigh':str(small_rho),'small_Rayleigh_display':float(small_rho),'large_exact_Rayleigh':str(big_rho),'large_energy_per_site_display':float(big_rho/(2*n)),'delta_display':float(delta),'beta_split':str(beta),'J_global_upper':str(jmax),'beta_below_split_bound_display':float(low_beta_upper),'beta_above_split_bound_display':float(high_beta_upper),'optimistic_scalar_replay':steps,'early_beta_J_upper_display':float(j_early),'late_beta_C_upper_display':float(c_late),'optimistic_continued_time_first':time_steps,'archived_beta':str(bs),'archived_cooling_J_lower_display':float(jlo),'archived_cooling_C_lower_display':float(clo)})
files=[P/'mps_small.cpp',P/'mps_small.out',P/'trial_n6.json',P/'trial_n8.json',ROOT/'audit/mps/mps_blocks.txt',ROOT/'audit/mps/build_mps.py',ROOT/'audit/APPENDIX_A_BRIDGE.md',ROOT/'research_20261010/chain_temperature_first/PROOF.md']
result={'status':'PASS exact recipe-specific all-beta exclusion','scope':'n=6 and n=8 uniform periodic spin1, fixed archived D26 MPS at 2n; one Rayleigh numerator, any valid smaller trace upper bounds; immediate canonical conversion or continued fixed time-first G recursion. Not a no-go for other seeds, trial collections, adaptive orderings or inequalities.','rows':rows,'seconds':time.time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'uniform_screen.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['rows','sha256']},indent=2))
for r in rows:print(r['n'],r['J_global_upper'],r['optimistic_scalar_replay'][-1]['failure'],r['optimistic_scalar_replay'][-1]['round'],r['archived_cooling_J_lower_display'])
