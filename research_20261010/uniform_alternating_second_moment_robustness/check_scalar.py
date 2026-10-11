#!/usr/bin/env python3
"""Exact four-gap robustness gate using finite uniform Gibbs B² bounds."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import ctypes,hashlib,json,os,resource,signal,sys,time
assert resource.getrlimit(resource.RLIMIT_CPU)==(28,28)
assert resource.getrlimit(resource.RLIMIT_AS)==(256*1024**2,256*1024**2)
assert os.sched_getaffinity(0)=={4}
assert signal.getsignal(signal.SIGXCPU)==signal.SIG_DFL
assert signal.SIGXCPU not in signal.pthread_sigmask(signal.SIG_BLOCK,[])
death=ctypes.c_int();assert ctypes.CDLL(None).prctl(2,ctypes.byref(death))==0 and death.value==signal.SIGKILL
start=time.process_time();P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**160;inputs={}
def read(rel):
 b=(ROOT/rel).read_bytes();inputs[rel]=hashlib.sha256(b).hexdigest();return b
pins={
 'uniform_smaller_second_initialization':'fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84',
 'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f',
 'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf',
 'uniform_alternating_robustness_proposal':'836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd',
 'uniform_alternating_robustness_review':'7c819d4758ee43bedba3298a15735d981f7b42ffeeabff40be8dd6a9e4e8bdf0',
 'uniform_alternating_positive_cell_review':'abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872',
 'uniform_alternating_positive_transfer':'ea050102bb50eea1a287e7e674de0f43aa091a4fcd17a3d8279870f5e26ab529',
 'uniform_alternating_positive_transfer_review':'e80440ac87f53460f52c14535e2eb649388cfd3fae72fdff424a14fcf521dfa9',
 'uniform_alternating_b2_fixture':'0cad4bf9a9bd907cd9be78a6eceaf20ec041b45c3d398fd664c38bd49ee88696',
 'uniform_alternating_b2_64_pilot':'26d1977cf2324cd693c306aecd3b621989364e773413192253670c0951ca3570',
 'uniform_alternating_b2_32_retry1':'eccb1dcbcf423c3c2678bde743bce0882c81473415160bdd24d8beb4e87d9b75',
}
for name,h in pins.items():
 raw=read(f'research_20261010/{name}/MANIFEST_SHA256.json');assert hashlib.sha256(raw).hexdigest()==h
 m=json.loads(raw)
 if all(isinstance(v,str) and len(v)==64 for v in m.values()):
  for member,expected in m.items():
   assert hashlib.sha256(read(f'research_20261010/{name}/{member}')).hexdigest()==expected
source=json.loads(read('research_20261010/uniform_smaller_second_initialization/certificate.json'))
seed=next(x for x in source['rows'] if x['n']==32)
assert seed['anchor_length']==64 and F(seed['beta'])==F(49,4)
kappas={32:F(17,125),64:F(157,1000)}
for L,folder in [(32,'uniform_alternating_b2_32_retry1'),(64,'uniform_alternating_b2_64_pilot')]:
 d=json.loads(read(f'research_20261010/{folder}/scalar_result.json'))
 assert d['physical_length']==L and F(d['gibbs_kappa_upper'])<=kappas[L]
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def expi(x):
 if x<0:
  lo,hi=expi(-x);return down(1/hi),up(1/lo)
 ct=0
 while x>F(1,16):x/=2;ct+=1
 term=s=F(1)
 for k in range(1,141):term=term*x/k;s+=term
 nxt=term*x/141;lo=down(s);hi=up(s+nxt/(1-x/142))
 for _ in range(ct):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
def root(x):
 assert x>=0
 k=isqrt(x.numerator*B*B//x.denominator);lo,hi=F(k,B),F(k+1,B)
 assert lo*lo<=x<=hi*hi
 return lo,hi
def cosh_upper(x):return up((expi(x)[1]+expi(-x)[1])/2)
def G(x):
 assert 0<x<=1
 return 1-(1-x)**2/(2*x*x)
def check(r,D):
 beta=F(49,4);S0=F(seed['S']);T0=F(seed['T'])
 factors={L:up(1+kappas[L]*(cosh_upper(beta*r*3*L/2)-1)) for L in [32,64]}
 s=down(S0/factors[32]**2);t=down(T0/factors[64]**2)
 s_initial=s;t_initial=t;n=16;states=[];terminal=None;failure=None
 for j in range(20):
  K=down(s*s*t)
  if not 0<K<=1:failure='illegal_K';break
  C=down(min(s*root(t)[0],t));beta_worst=beta*(1+r);ee=expi(beta_worst*D)[1]
  margin=C-ee*(1-C)
  states.append({'round':j,'cell_base':n,'physical_base':2*n,'normalized_beta':str(beta),'physical_beta_upper':str(beta_worst),'S_lower':str(s),'T_lower':str(t),'K_lower':str(K),'window_cell_from':n,'window_cell_to':2*n,'window_purity_lower':str(C),'window_margin':str(margin)})
  if margin<=0:failure='window_margin';break
  u=max(1-s,1-t);amargin=1-5*u*ee
  if u<=F(1,100) and amargin>0:
   terminal={'cell_from':n,'physical_from':2*n,'defect':str(u),'margin':str(amargin)};break
  s=down(G(K))
  if s<=0:failure='nonpositive_S';break
  t=down(G(down(t*t*s)))
  if t<=0:failure='nonpositive_T';break
  n*=2;beta*=2
 short=(F(31,1250)-90*r)/(1+r);bridge_limit=(F(31,1250)-D)/(90+D)
 ok=terminal is not None and short>=D
 return {'status':'EXACT_PRODUCER_PASS_REVIEW_REQUIRED' if ok else 'FAILED_SUFFICIENT_TEST','eta_radius':str(r),'g_lower':str((1-r)/(1+r)),'g_upper':str((1+r)/(1-r)),'physical_gap_target':str(D),'initial_cell_base':16,'initial_physical_base':32,'anchor_physical_length':64,'initial_normalized_beta':'49/4','shift_per_physical_site':'c * 700741/500000','uniform_S_lower':str(S0),'uniform_T_lower':str(T0),'shifted_anchor_Rayleigh':seed['shifted_Rayleigh'],'trace_factors_upper':{str(k):str(v) for k,v in factors.items()},'gibbs_kappa_upper':{str(k):str(v) for k,v in kappas.items()},'S_lower':str(s_initial),'T_lower':str(t_initial),'states':states,'terminal':terminal,'failure_reason':failure,'finite_bridge':{'cell_min':2,'cell_max':15,'physical_min':4,'physical_max':30,'uniform_gap_premise':'31/1250','worst_gap_lower':str(short),'margin':str(short-D),'maximal_radius_for_this_bridge':str(bridge_limit),'radius_attains_bridge_limit':r==bridge_limit},'all_integer_cells_at_least':2 if ok else None,'unique_ground_state':ok}
rows=[];tests=[]
for D in [F(1,50),F(3,200),F(1,100),F(1,200)]:
 # First planned candidate is the exact closed-endpoint Weyl limit. If its seed
 # fails, rational bisection records ordinary rejected candidates without retry.
 limit=(F(31,1250)-D)/(90+D);candidate=check(limit,D);tests.append(candidate)
 if candidate['status']=='EXACT_PRODUCER_PASS_REVIEW_REQUIRED':rows.append(candidate)
 else:
  lo=F(0);hi=limit;best=check(lo,D);assert best['status']=='EXACT_PRODUCER_PASS_REVIEW_REQUIRED'
  for _ in range(14):
   mid=(lo+hi)/2;q=check(mid,D);tests.append(q)
   if q['status']=='EXACT_PRODUCER_PASS_REVIEW_REQUIRED':lo=mid;best=q
   else:hi=mid
  rows.append(best)
assert len(rows)==4 and all(x['status']=='EXACT_PRODUCER_PASS_REVIEW_REQUIRED' for x in rows)
result={'status':'EXACT_PRODUCER_SECOND_MOMENT_ROBUSTNESS_REVIEW_REQUIRED','model':'Periodic spin1 H_M(g)=sum_j[h_(2j-1,2j)+g*h_(2j,2j+1)], unit designated exchange, physical L=2M, integer M>=2','beta_rescaling':'actual beta_j=(2^j * 49/4)/c, c=(1+g)/2','eta_definition':'(1-g)/(1+g)','rows':rows,'planned_candidate_count':len(tests),'rejected_candidate_count':sum(x['status']!='EXACT_PRODUCER_PASS_REVIEW_REQUIRED' for x in tests),'dependencies':pins,'physical_contractions':False,'linear_trial_dimension':1,'MPS_bond_dimension':26,'producer_kappa_inputs_pending_independent_review':True,'old_intervals_and_seals_preserved':True,'resources':{'process_CPU_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'postexec_controls_verified':True}}
(P/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
(P/'planned_candidates.json').write_text(json.dumps(tests,indent=2)+'\n')
(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
for r in rows:print('PASS',r['eta_radius'],r['g_lower'],r['g_upper'],'gap',r['physical_gap_target'],'rounds',len(r['states']),'bridge_limit',r['finite_bridge']['radius_attains_bridge_limit'])
print(result['resources'])
