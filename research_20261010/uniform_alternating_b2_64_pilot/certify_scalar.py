#!/usr/bin/env python3
"""Rational scalar validation of the new64-site observable and Gibbs bound."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,resource,time,hashlib
resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time();P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**120;inputs={}
def read(rel):
 b=(ROOT/rel).read_bytes();inputs[rel]=hashlib.sha256(b).hexdigest();return b
v={}
for line in (P/'pilot.out').read_text().splitlines():
 if '=' in line:
  k,x=line.split('=',1)
  if k in ['N0_64','H0_64','B2_64']:v[k]=int(x)
assert set(v)=={'N0_64','H0_64','B2_64'} and v['N0_64']>0
anchors={k:int(x) for line in read('research_20261010/uniform_smaller_second_initialization_review/anchors.out').decode().splitlines() if '=' in line for k,x in [line.split('=',1)]}
assert v['N0_64']==anchors['N0_64'] and v['H0_64']==anchors['H0_64']
seed=next(x for x in json.loads(read('research_20261010/uniform_smaller_second_initialization/certificate.json'))['rows'] if x['n']==32)
for rel in ['research_20261010/uniform_smaller_second_initialization_review/MANIFEST_SHA256.json','research_20261010/uniform_alternating_b2_fixture/MANIFEST_SHA256.json','research_20261010/uniform_alternating_b2_fixture/fixture.cpp','research_20261010/uniform_alternating_b2_fixture/b2_blocks.txt']:read(rel)
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x):
 assert x>=0
 k=isqrt(x.numerator*B*B//x.denominator);l,h=F(k,B),F(k+1,B);assert l*l<=x<=h*h;return l,h
def ex(x):
 if x<0:
  l,h=ex(-x);return down(1/h),up(1/l)
 n=0
 while x>F(1,16):x/=2;n+=1
 t=s=F(1)
 for j in range(1,121):t=t*x/j;s+=t
 nt=t*x/121;l=down(s);h=up(s+nt/(1-x/122))
 for _ in range(n):l=down(l*l);h=up(h*h)
 return l,h
q=F(v['B2_64'],9216*v['N0_64']);assert 0<=q<=1
Q=F(seed['Q']);C=F(seed['T']);beta=F(49,4);mu=F(v['H0_64'],v['N0_64'])+64*F(700741,500000);assert mu==F(seed['shifted_Rayleigh'])
Elo=F(-71,10000);delta=F(19,100);w=(1+root(2*C-1)[0])/2;energy_margin=ex(-beta*Elo)[0]-Q;gap_margin=w-ex(beta*delta)[1]*(1-w);assert energy_margin>0 and gap_margin>0
eps=(mu-Elo)/delta;f=1-eps;assert 0<eps<1 and f>q
alpha=up((root(f*q)[1]+root((1-f)*(1-q))[1])**2);alpha=min(F(1),alpha);kappa=up(1-w+w*alpha);assert kappa<F(157,1000)
cs=[json.loads(x.read_text()) for x in sorted(P.glob('checkpoint_*.json'))];assert len(cs)==11 and {x['block_index'] for x in cs}==set(range(11))
assert sum(int(x['norm_contribution']) for x in cs)==v['N0_64'];assert sum(int(x['H_contribution']) for x in cs)==v['H0_64'];assert sum(int(x['B2_contribution']) for x in cs)==v['B2_64']
adj=sum(int(x['adjacent_symmetric']) for x in cs);true_omission=v['B2_64']+64*adj;assert true_omission!=v['B2_64']
res={'status':'EXACT_PRODUCER_L64_B2_AND_FIDELITY_SCALAR_REVIEW_REQUIRED','physical_length':64,'normalized_trial_B2':str(q),'normalized_trial_B2_display':float(q),'shifted_trial_mu':str(mu),'trace_upper':str(Q),'purity_lower':str(C),'ground_shifted_energy_lower':str(Elo),'ground_energy_check_margin':str(energy_margin),'finite_gap_lower':str(delta),'finite_gap_check_margin':str(gap_margin),'energy_only_infidelity_upper':str(eps),'fidelity_lower':str(f),'ground_gibbs_weight_lower':str(w),'ground_B2_effect_upper':str(alpha),'gibbs_kappa_upper':str(kappa),'simple_gibbs_kappa_upper':'157/1000','gibbs_kappa_display':float(kappa),'q_le_one_twentieth':q<=F(1,20),'all_11_checkpoint_totals_match':True,'corrected_true_adjacent_omission_mutation':{'formula':'B2+64*sum(adjacent_symmetric)','altered_B2':str(true_omission),'rejected':True},'resources':{'CPU_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'scalar_result.json').write_text(json.dumps(res,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(res['status'], 'q64=',float(q),'alpha=',float(alpha),'kappa=',float(kappa),'simple_upper=157/1000');print(res['resources'])
