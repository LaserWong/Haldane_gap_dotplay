#!/usr/bin/env python3
"""Directed finite Gibbs effect bound from the corrected length-32 contraction."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,resource,time,hashlib,os
resource.setrlimit(resource.RLIMIT_CPU,(1,1))
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
os.sched_setaffinity(0,{4})
start=time.process_time();P=Path(__file__).resolve().parent;ROOT=P.parents[1]
L=32;BNORM=3*L//2;SCALE=10**120;inputs={}
def read(rel):
 b=(ROOT/rel).read_bytes();inputs[rel]=hashlib.sha256(b).hexdigest();return b
def down(x):return F(x.numerator*SCALE//x.denominator,SCALE)
def up(x):return F(-(-x.numerator*SCALE//x.denominator),SCALE)
def root(x):
 assert x>=0
 k=isqrt(x.numerator*SCALE*SCALE//x.denominator);lo,hi=F(k,SCALE),F(k+1,SCALE)
 assert lo*lo<=x<=hi*hi
 return lo,hi
def ex(x):
 if x<0:
  lo,hi=ex(-x);return down(1/hi),up(1/lo)
 n=0
 while x>F(1,16):x/=2;n+=1
 t=s=F(1)
 for j in range(1,121):t=t*x/j;s+=t
 nt=t*x/121;lo=down(s);hi=up(s+nt/(1-x/122))
 for _ in range(n):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
names={x:f'{x}_{L}' for x in ['N0','H0','B2']}
v={k:int(x) for line in (P/'pilot.out').read_text().splitlines() if '=' in line for k,x in [line.split('=',1)] if k in names.values()}
assert set(v)==set(names.values())
N,H,B2=(v[names[x]] for x in ['N0','H0','B2']);assert N>0
anchors={k:int(x) for line in read('research_20261010/uniform_gap_0248_all_sizes_review/anchors.out').decode().splitlines() if '=' in line for k,x in [line.split('=',1)]}
assert N==anchors[names['N0']] and H==anchors[names['H0']]
seed=next(x for x in json.loads(read('research_20261010/uniform_gap_0248_all_sizes/certificate.json'))['new_rows'] if x['L']==L)
for rel in ['research_20261010/uniform_gap_0248_all_sizes_review/MANIFEST_SHA256.json','research_20261010/uniform_alternating_b2_fixture/MANIFEST_SHA256.json','research_20261010/uniform_alternating_b2_fixture/fixture.cpp','research_20261010/uniform_alternating_b2_fixture/b2_blocks.txt','research_20261010/uniform_alternating_b2_64_pilot/MANIFEST_SHA256.json']:
 read(rel)
failed=ROOT/'research_20261010/uniform_alternating_b2_32_companion'
for f in sorted(failed.iterdir()):
 if f.is_file():read(str(f.relative_to(ROOT)))
q=F(B2,BNORM**2*N);assert 0<=q<=1
Q=F(seed['trace_inputs'][str(L)]);C=F(seed['purity_lower']);beta=F(49,4)
mu=F(H,N)+L*F(700741,500000);assert mu==F(seed['shifted_total_Rayleigh'])
Elo=F(-63,10000);delta=F(21,100);w=(1+root(2*C-1)[0])/2
energy_margin=ex(-beta*Elo)[0]-Q;gap_margin=w-ex(beta*delta)[1]*(1-w)
assert energy_margin>0 and gap_margin>0
eps=(mu-Elo)/delta;f=1-eps;assert 0<eps<1 and f>q
alpha=min(F(1),up((root(f*q)[1]+root((1-f)*(1-q))[1])**2))
kappa=up(1-w+w*alpha)
simple=F(17,125);assert kappa<simple
cs=[json.loads(p.read_text()) for p in sorted(P.glob('checkpoint_*.json'))]
assert len(cs)==11 and {x['block_index'] for x in cs}==set(range(11))
assert sum(int(x['norm_contribution']) for x in cs)==N
assert sum(int(x['H_contribution']) for x in cs)==H
assert sum(int(x['B2_contribution']) for x in cs)==B2
adj=sum(int(x['adjacent_symmetric']) for x in cs)
true_omission=B2+L*adj;assert true_omission!=B2
res={'status':'EXACT_PRODUCER_L32_B2_AND_FIDELITY_SCALAR_REVIEW_REQUIRED','physical_length':L,'normalized_trial_B2':str(q),'normalized_trial_B2_display':float(q),'shifted_trial_mu':str(mu),'trace_upper':str(Q),'purity_lower':str(C),'ground_shifted_energy_lower':str(Elo),'ground_energy_check_margin':str(energy_margin),'finite_gap_lower':str(delta),'finite_gap_check_margin':str(gap_margin),'energy_only_infidelity_upper':str(eps),'fidelity_lower':str(f),'ground_gibbs_weight_lower':str(w),'ground_B2_effect_upper':str(alpha),'gibbs_kappa_upper':str(kappa),'simple_gibbs_kappa_upper':str(simple),'gibbs_kappa_display':float(kappa),'all_11_checkpoint_totals_match':True,'corrected_true_adjacent_omission_mutation':{'formula':'B2+L*sum(adjacent_symmetric)','altered_B2':str(true_omission),'rejected':True},'resources':{'CPU_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'scalar_result.json').write_text(json.dumps(res,indent=2)+'\n')
(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
print(res['status'],'q32=',float(q),'alpha=',float(alpha),'kappa=',float(kappa),'simple_upper=',simple)
print(res['resources'])
