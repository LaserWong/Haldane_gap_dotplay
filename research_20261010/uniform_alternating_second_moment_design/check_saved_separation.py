#!/usr/bin/env python3
"""Design-only certified scalar separation checks; no new physical data."""
import json,resource,time,hashlib
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
resource.setrlimit(resource.RLIMIT_CPU,(5,5));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;B=10**70;inputs={}
def read(name):
 b=(R/name).read_bytes();inputs[name]=hashlib.sha256(b).hexdigest();return json.loads(b)
a=read('uniform_gap_0248_all_sizes/certificate.json');r32=next(x for x in a['new_rows'] if x['L']==32)
b=read('uniform_smaller_second_initialization/certificate.json');s32=next(x for x in b['rows'] if x['n']==32)
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x):
 k=isqrt(x.numerator*B*B//x.denominator);lo,hi=F(k,B),F(k+1,B);assert lo*lo<=x<=hi*hi;return lo,hi
def ex(x):
 if x<0:
  l,h=ex(-x);return down(1/h),up(1/l)
 k=0
 while x>F(1,16):x/=2;k+=1
 t=s=F(1)
 for j in range(1,101):t=t*x/j;s+=t
 nt=t*x/101;l=down(s);h=up(s+nt/(1-x/102))
 for _ in range(k):l=down(l*l);h=up(h*h)
 return l,h
rows=[]
for L,Q,mu,C,Elo,delta in [
 (32,F(r32['trace_inputs']['32']),F(r32['shifted_total_Rayleigh']),F(r32['purity_lower']),F(-63,10000),F(21,100)),
 (64,F(s32['Q']),F(s32['shifted_Rayleigh']),F(s32['T']),F(-71,10000),F(19,100))]:
 beta=F(49,4);gamma=(1+root(2*C-1)[0])/2
 thermal_margin=ex(-beta*Elo)[0]-Q;gap_margin=gamma-ex(beta*delta)[1]*(1-gamma)
 assert thermal_margin>0 and gap_margin>0
 err=mu-Elo;sep_old=F(31,1250)-err;sep=delta-err;eps=err/delta
 assert 0<eps<1 and sep_old>0 and sep>0
 cases=[]
 for q in [F(1,20),F(1,10),F(1,4)]:
  alpha=min(F(1),up((root(q)[1]+root(eps)[1])**2));kappa=up(1-gamma*(1-alpha));cases.append({'hypothetical_q_upper':str(q),'ground_effect_alpha_upper':str(alpha),'gibbs_kappa_upper':str(kappa)})
 alpha_quarter=1-F(3,4)/gamma
 qmax=down((root(alpha_quarter)[0]-root(eps)[1])**2) if root(alpha_quarter)[0]>root(eps)[1] else F(0)
 out={'L':L,'trace_upper':str(Q),'trial_shifted_mu':str(mu),'purity_lower':str(C),'ground_gibbs_weight_lower':str(gamma),'ground_shifted_energy_lower':str(Elo),'energy_lower_check_margin':str(thermal_margin),'finite_gap_lower':str(delta),'finite_gap_check_margin':str(gap_margin),'energy_excess_upper':str(err),'separation_with_uniform_gap':str(sep_old),'separation_with_finite_gap':str(sep),'energy_only_infidelity_upper':str(eps),'q_sufficient_for_kappa_at_most_one_quarter':str(qmax),'hypothetical_B2_cases':cases}
 rows.append(out)
 print('L',L,'mu',float(mu),'gamma',float(gamma),'gap',float(delta),'E0lower',float(Elo),'excess',float(err),'uniform_sep',float(sep_old),'finite_sep',float(sep),'eps_energy',float(eps),'q_for_kappa_quarter',float(qmax))
 for c in cases:print(' q',c['hypothetical_q_upper'],'kappa',float(F(c['gibbs_kappa_upper'])))
result={'status':'CERTIFIED_SCALAR_SEPARATION_AND_HYPOTHETICAL_THRESHOLDS_ONLY_NO_NEW_B2_DATA','rows':rows,'resources':{'process_cpu_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'hard_cpu_seconds':5,'hard_address_space_mib':256,'physical_contractions':False}}
(P/'separation_results.json').write_text(json.dumps(result,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(result['resources'])
