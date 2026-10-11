#!/usr/bin/env python3
"""Length64 exact variance and variance-refined Gibbs effect, producer only."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import hashlib,json,os,resource,time
resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));os.sched_setaffinity(0,{4})
start=time.process_time();P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**120;inputs={}
def read(rel):
 raw=(ROOT/rel).read_bytes();inputs[rel]=hashlib.sha256(raw).hexdigest();return raw
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x):
 assert x>=0
 k=isqrt(x.numerator*B*B//x.denominator);lo,hi=F(k,B),F(k+1,B);assert lo*lo<=x<=hi*hi;return lo,hi
def ex(x):
 if x<0:
  lo,hi=ex(-x);return down(1/hi),up(1/lo)
 count=0
 while x>F(1,16):x/=2;count+=1
 t=s=F(1)
 for j in range(1,141):t=t*x/j;s+=t
 lo=down(s);hi=up(s+(t*x/141)/(1-x/142))
 for _ in range(count):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
v={k:int(x) for line in (P/'pilot.out').read_text().splitlines() if '=' in line for k,x in [line.split('=',1)] if k in ['N0_64','H0_64','H2_64','VARIANCE_NUMERATOR','VARIANCE_DENOMINATOR']}
assert len(v)==5;N,H,H2=(v[k] for k in ['N0_64','H0_64','H2_64']);assert N>0
assert v['VARIANCE_NUMERATOR']==H2*N-H*H>=0 and v['VARIANCE_DENOMINATOR']==N*N
variance=F(H2*N-H*H,N*N)
anchors={k:int(x) for line in read('research_20261010/uniform_smaller_second_initialization_review/anchors.out').decode().splitlines() if '=' in line for k,x in [line.split('=',1)]}
assert N==anchors['N0_64'] and H==anchors['H0_64']
old=json.loads(read('research_20261010/uniform_alternating_b2_64_pilot/scalar_result.json'))
seed=next(x for x in json.loads(read('research_20261010/uniform_smaller_second_initialization/certificate.json'))['rows'] if x['n']==32)
Q=F(seed['Q']);C=F(seed['T']);mu=F(H,N)+64*F(700741,500000);assert mu==F(seed['shifted_Rayleigh'])==F(old['shifted_trial_mu'])
q=F(old['normalized_trial_B2']);beta=F(49,4);w=down(ex(-beta*mu)[0]/Q)
Elo=F(-702409,100000000);delta=F(19681,100000)
energy_margin=ex(-beta*Elo)[0]-Q;gap_margin=w-ex(beta*delta)[1]*(1-w)
assert energy_margin>0 and gap_margin>0
e=mu-Elo;eps0=e/delta;assert 0<eps0<F(1,2)
variance_threshold=delta*delta*eps0*(1-eps0)
if 4*variance<=delta*delta:
 eps_variance=up((1-root(1-4*variance/(delta*delta))[0])/2)
else:eps_variance=F(1)
eps=min(eps0,eps_variance);f=1-eps;assert f>q
alpha=min(F(1),up((root(f*q)[1]+root((1-f)*(1-q))[1])**2))
kappa=up(1-w+w*alpha);simple=F(-(-kappa.numerator*10000//kappa.denominator),10000)
cs=[json.loads((P/f'checkpoint_{j}.json').read_text()) for j in range(11)]
assert sum(int(x['norm_contribution']) for x in cs)==N
assert sum(int(x['H_contribution']) for x in cs)==H
assert sum(int(x['H2_contribution']) for x in cs)==H2
for j,x in enumerate(cs):
 y=json.loads(read(f'research_20261010/uniform_alternating_b2_64_pilot/checkpoint_{j}.json'))
 for field in ['block_index','charge','side','norm_contribution','H_contribution','same_bond','adjacent_symmetric']:assert x[field]==y[field]
 assert x['positive_convolution_sign']==1 and x['all_four_old_checkpoint_fields_match']
 assert int(x['H2_contribution'])==64*sum(int(x[k]) for k in ['same_bond','adjacent_symmetric','positive_disjoint'])
for rel in ['research_20261010/uniform_alternating_b2_fixture_review/MANIFEST_SHA256.json','research_20261010/uniform_alternating_h2_design/MANIFEST_SHA256.json']:read(rel)
result={'status':'EXACT_PRODUCER_L64_H2_VARIANCE_FIDELITY_REVIEW_REQUIRED','physical_length':64,'variance':str(variance),'variance_display':float(variance),'normalized_H2':str(F(H2,N)),'shifted_trial_mu':str(mu),'trace_upper':str(Q),'purity_lower':str(C),'ground_weight_Rayleigh_lower':str(w),'ground_shifted_energy_lower':str(Elo),'finite_gap_lower':str(delta),'energy_check_margin':str(energy_margin),'gap_check_margin':str(gap_margin),'energy_only_infidelity':str(eps0),'variance_pairwise_infidelity':str(eps_variance),'retained_infidelity_upper':str(eps),'fidelity_lower':str(f),'variance_helpful_threshold':str(variance_threshold),'variance_improves_fidelity':variance<variance_threshold,'normalized_trial_B2':str(q),'ground_B2_effect_upper':str(alpha),'Gibbs_kappa_upper':str(kappa),'Gibbs_kappa_display':float(kappa),'simple_Gibbs_kappa_upper':str(simple),'all_11_old_N_H_same_adjacent_fields_match':True,'no_physical32_H2':True,'no_new_interval':True,'resources':{'process_CPU_seconds':time.process_time()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'hard_CPU_seconds':1,'hard_memory_MiB':256,'CPU_affinity':[4]}}
(P/'scalar_result.json').write_text(json.dumps(result,indent=2)+'\n');(P/'SCALAR_INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
print('PASS variance64=',float(variance),'old_epsilon=',float(eps0),'new_epsilon=',float(eps),'kappa64=',float(kappa),'simple=',simple,'variance_useful=',variance<variance_threshold)
print(result['resources'])
