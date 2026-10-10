#!/usr/bin/env python3
"""Exact all-beta exclusions for the fixed one-D26-Rayleigh scalar recipes."""
import os,resource,time,json,hashlib
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
P=Path(__file__).resolve().parent;ROOT=P.parents[1];t0=time.time();B=1<<160
INPUTS={
 'audit/mps/build_mps.py':'693ded40630e851fda40986460b841bcfe3e48cf5ace665997f923ec7737ffdb',
 'audit/mps/mps_blocks.txt':'26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa',
}
for path,digest in INPUTS.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest

def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def exp_i(x):
 x=F(x)
 if x<0:
  l,u=exp_i(-x);return down(1/u),up(1/l)
 k=0
 while x>F(1,16):x/=2;k+=1
 t=s=F(1)
 for j in range(1,41):t=t*x/j;s+=t
 nxt=t*x/41;l=down(s);u=up(s+nxt/(1-x/42))
 for _ in range(k):l=down(l*l);u=up(u*u)
 return l,u

def sqrt_up(x):
 z=isqrt(x.numerator*B*B//x.denominator);v=F(z+1,B);assert v*v>x;return v

def G(x):
 assert 0<x<=1
 return 1-(1-x)**2/(2*x*x)

def can_fail(a,b):
 # Joint-aware conversion at the current base. Old K is dropped after one cycle.
 s=up(a*sqrt_up(b));t=up(a*a*b);K=t
 hist=[{'stage':'converted','S_upper':str(s),'T_upper':str(t),'K_upper':str(K)}]
 for k in range(30):
  assert min(s,t)<F(99,100)
  z=max(s*s*t,K);s=up(G(z))
  if s<=0:return hist+[{'failure':'canonical spatial','round':k+1,'argument_upper':str(z),'output_upper':str(s)}]
  z=max(t,K)**2*s;t=up(G(z));K=F(0)
  if t<=0:return hist+[{'failure':'canonical thermal','round':k+1,'argument_upper':str(z),'output_upper':str(t)}]
  hist.append({'round':k+1,'S_upper':str(s),'T_upper':str(t),'K_upper':'0'})
 raise AssertionError('No finite failure witness')

raw=dict(x.split('=') for x in (P/'mps_lengths.out').read_text().splitlines());trials=json.loads((P/'exact_trial_data.json').read_text());rows=[]
# Repeated shorter contractions must equal the frozen assessment byte-for-byte values.
old=dict(x.split('=') for x in (ROOT/'research_20261010/nonperturbative_mps_assessment/mps_small.out').read_text().splitlines())
for k,v in old.items():assert raw[k]==v
for row in trials['rows']:
 n=row['n'];R=2*n*F(int(raw[f'U{2*n}']),int(raw[f'V{2*n}']));A=[F(s['Rayleigh']) for s in row['states']];alpha=A[0];delta=R-2*alpha
 assert R<0 and delta>0
 out={'n':n,'full_hilbert_dimension_small':3**n,'full_hilbert_dimension_numerator':3**(2*n),'MPS_D':26,'numerator_retained_states':1,'large_Rayleigh':str(R),'large_Rayleigh_display':float(R),'delta':str(delta),'delta_display':float(delta),'denominator_orthogonal_trials':len(A)}
 if n in (6,8):
  cut,jcap=(F(3,4),F(29,50)) if n==6 else (F(31,40),F(71,100))
  hot=exp_i(-2*cut*R)[1]/3**(4*n);cold=exp_i(-2*cut*delta)[1]
  assert hot<jcap and cold<jcap
  early=exp_i(-R)[1]/3**(4*n);late=exp_i(-delta)[1]
  assert early<F(2,5) and G(F(2,5))<0 and late<F(4,5)
  a=up(G(jcap));b=up(G(F(4,5)**2*a));conversions=[];time_history=[]
  for delay in range(10):
   if a<=0 or b<=0:break
   assert min(a,b)<F(99,100)
   conversions.append({'time_first_delay':delay,'a_upper':str(a),'b_upper':str(b),'joint_aware_canonical':can_fail(a,b)})
   z=a*a*b;a=up(G(z))
   if a<=0:
    time_history.append({'failure':'first time-first direction','additional_cycle':delay+1,'argument_upper':str(z),'output_upper':str(a)});break
   z=b*b*a;b=up(G(z))
   if b<=0:
    time_history.append({'failure':'second time-first direction','additional_cycle':delay+1,'argument_upper':str(z),'output_upper':str(b)});break
   time_history.append({'additional_cycle':delay+1,'a_upper':str(a),'b_upper':str(b)})
  assert time_history and 'failure' in time_history[-1]
  out.update({'J_global_cap':str(jcap),'global_split':str(cut),'global_hot_J_upper':str(hot),'global_cold_J_upper':str(cold),'early_beta_end':'1/2','early_J_upper':str(early),'late_C_upper':str(late),'late_C_cap':'4/5','all_legal_delayed_conversions':conversions,'time_first_replay':time_history,'verdict':'all beta excluded for immediate joint-aware canonical conversion or any fixed time-first delay then that conversion'})
 else:
  assert len(A)==4
  gaps=[x-alpha for x in A[1:]];assert min(gaps)>0
  hot=exp_i(-R)[1]/3**(4*n);cold=exp_i(-20*delta)[1]
  cap=F(3,25) if n==10 else F(19,100)
  boxes=[]
  for i in range(2,40):
   lo=F(i,4);hi=F(i+1,4)
   den=1+sum(exp_i(-hi*g)[0] for g in gaps)
   ub=up(exp_i(-2*lo*delta)[1]/den**4)
   assert ub<cap
   boxes.append({'beta_lower':str(lo),'beta_upper':str(hi),'J_upper':str(ub),'J_upper_display':float(ub)})
  assert hot<cap and cold<cap and G(cap)<0
  # Two-state refinement is optional; test it with the same exact covering.
  two=[]
  for i in range(2,40):
   lo=F(i,4);hi=F(i+1,4);den=1+exp_i(-hi*gaps[0])[0]
   ub=up(exp_i(-2*lo*delta)[1]/den**4);assert ub<F(3,10)
   two.append(ub)
  assert hot<F(3,10) and cold<F(3,10)
  # Additional exact denominator lower estimates, including the complement.
  sample=[];D=3**n;r=len(A);mu_complement=-sum(A)/F(D-r)
  assert mu_complement>0
  for beta in map(F,(1,2,4,6,8,10)):
   lo=sum(exp_i(-beta*x)[0] for x in A)+(D-r)*exp_i(-beta*mu_complement)[0]
   sample.append({'beta':str(beta),'trace_lower_with_complement':str(lo),'trace_lower_display':float(lo),'ordinary_Jensen_lower':str(D)})
  out.update({'J_global_cap':str(cap),'first_G_at_cap':str(G(cap)),'hot_beta_end':'1/2','hot_J_upper':str(hot),'cold_beta_start':'10','cold_J_upper':str(cold),'warm_boxes':boxes,'largest_warm_box_bound_display':max(b['J_upper_display'] for b in boxes),'two_state_J_global_cap':'3/10','two_state_max_warm_display':float(max(two)),'two_state_warm_J_uppers':[str(x) for x in two],'Jensen_complement_mean':str(mu_complement),'trace_lower_samples':sample,'verdict':'all beta excluded at first G; applies before any later joint-aware conversion or continuation'})
 rows.append(out)
files=[ROOT/path for path in INPUTS]+[P/'mps_lengths.cpp',P/'mps_lengths.out',P/'verify_trials.py',P/'exact_trial_data.json',P/'verify_scalar.py']+sorted(P.glob('trial*.json.gz'))+[ROOT/'research_20261010/nonperturbative_mps_assessment/trial_n6.json',ROOT/'research_20261010/nonperturbative_mps_assessment/trial_n8.json',ROOT/'research_20261010/nonperturbative_mps_assessment/mps_small.out',ROOT/'research_20261010/joint_ratio_review/GENERAL_LEMMA.md',ROOT/'research_20261010/joint_ratio_review/LEMMA_ACCEPTANCE.json']
result={'status':'PASS exact all-beta recipe-specific exclusion','independent_review':'pending','scope':'uniform periodic spin1 unit Heisenberg; even denominator n=6,8,10,12; fixed archived D26 one-Rayleigh numerator at 2n; any valid denominator upper trace bounds; G-based time-first initialization. n6/8 check every fixed time-first delay then joint-aware conversion. n10/12 fail initial G itself. No claim about physical gap or arbitrary seeds, multiple numerator states, different MPS or purification inequalities.','rows':rows,'seconds':time.time()-t0,'cpu_seconds':time.process_time(),'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'source_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'uniform_seed_size_diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
for r in rows:print(r['n'],r['verdict'],'J cap',r['J_global_cap'])
print('resources',{k:result[k] for k in ('seconds','cpu_seconds','peak_kb')})
