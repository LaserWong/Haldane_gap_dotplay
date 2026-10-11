#!/usr/bin/env python3
"""Positive-cell finite-seed robustness; standalone exact scalar certificate."""
import hashlib, json, os, resource, sys, time
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
resource.setrlimit(resource.RLIMIT_AS, (256*1024**2, 256*1024**2))
sys.set_int_max_str_digits(100000)
START=time.process_time(); WALL=time.monotonic()
P=Path(__file__).resolve().parent; ROOT=P.parents[1]; B=10**120
inputs={}
def read(rel):
    p=ROOT/rel; data=p.read_bytes(); inputs[rel]=hashlib.sha256(data).hexdigest(); return data
pins={
 'uniform_smaller_second_initialization':'fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84',
 'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f',
 'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf',
 'uniform_second_thermal_full_review':'792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94',
 'uniform_alternating_robustness_proposal':'836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd',
 'uniform_alternating_robustness_review':'7c819d4758ee43bedba3298a15735d981f7b42ffeeabff40be8dd6a9e4e8bdf0',
 'uniform_alternating_positive_cell_review':'abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872',
}
for name,h in pins.items():
    rel=f'research_20261010/{name}/MANIFEST_SHA256.json'; raw=read(rel); assert hashlib.sha256(raw).hexdigest()==h
    # Verify every source-manifest member whenever the manifest uses the simple filename/hash map.
    m=json.loads(raw)
    if all(isinstance(v,str) and len(v)==64 for v in m.values()):
        for member,expected in m.items():
            data=read(f'research_20261010/{name}/{member}'); assert hashlib.sha256(data).hexdigest()==expected
source=json.loads(read('research_20261010/uniform_smaller_second_initialization/certificate.json'))
seeds={x['n']:x for x in source['rows']}
for n in [30,32,34]:
    row=seeds[n];assert row['status']=='PASS_PRODUCER' and row['anchor_length']==2*n and F(row['beta'])==F(49,4) and F(row['shifted_Rayleigh'])<0
for rel in ['audit/AUDIT_REPORT.md','research_20261010/chain_audit/CHAIN_CERTIFICATE_PROOF.md','research_20261010/integer_window_refinement_review/PROOF.md','research_20261010/uniform_cooled_seed_optimization/PROOF.md','research_20261010/uniform_smaller_second_initialization/PROOF.md','research_20261010/uniform_gap_0248_all_sizes_review/PROOF.md','research_20261010/uniform_second_thermal_full_review/PROOF.md','audit/mps/mps_blocks.txt']:
    read(rel)
def down(x): return F(x.numerator*B//x.denominator,B)
def up(x): return F(-(-x.numerator*B//x.denominator),B)
def expi(x):
    if x<0:
        lo,hi=expi(-x); return down(1/hi),up(1/lo)
    ct=0
    while x>F(1,16): x/=2; ct+=1
    term=s=F(1)
    for k in range(1,101): term=term*x/k; s+=term
    nxt=term*x/101
    lo=down(s); hi=up(s+nxt/(1-x/102))
    for _ in range(ct): lo=down(lo*lo); hi=up(hi*hi)
    return lo,hi
def root(x):
    assert x>=0
    from math import isqrt
    k=isqrt(x.numerator*B*B//x.denominator)
    lo=F(k,B);hi=F(k+1,B); assert lo*lo<=x<=hi*hi
    return lo,hi
def G(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)
def check(physical_base,radius,gap):
    seed=seeds[physical_base]; S0=F(seed["S"]);T0=F(seed["T"]);
    beta0=F(49,4); cell_base=physical_base//2
    A=F(9,8)*(beta0*radius*physical_base)**2
    s=down(S0*expi(-2*A)[0]); t=down(T0*expi(-8*A)[0]); initial_s=s;initial_t=t
    beta=beta0;n=cell_base;states=[];terminal=None
    for j in range(18):
        K=down(s*s*t)
        assert 0<K<=1
        C=down(min(s*root(t)[0],t))
        beta_worst=beta*(1+radius); ee=expi(beta_worst*gap)[1]
        margin=C-ee*(1-C)
        states.append({'round':j,'cell_base':n,'physical_base':2*n,'normalized_beta':str(beta),'physical_beta_upper':str(beta_worst),'S_lower':str(s),'T_lower':str(t),'K_lower':str(K),'window_cell_from':n,'window_cell_to':2*n,'window_purity_lower':str(C),'window_margin':str(margin)})
        if margin<=0: break
        defect=max(1-s,1-t); amargin=1-5*defect*ee
        if defect<=F(1,100) and amargin>0:
            terminal={'cell_from':n,'physical_from':2*n,'defect':str(defect),'margin':str(amargin)};break
        s=down(G(K))
        if s<=0:break
        t=down(G(down(t*t*s)))
        if t<=0:break
        n*=2;beta*=2
    short_lower=(F(31,1250)-3*(physical_base-2)*radius)/(1+radius)
    passed=terminal is not None and short_lower>=gap
    return {'status':'EXACT_PRODUCER_PASS_INDEPENDENT_REVIEW_REQUIRED' if passed else 'FAILED_SUFFICIENT_TEST_NOT_NO_GO','eta_radius':str(radius),'g_lower':str((1-radius)/(1+radius)),'g_upper':str((1+radius)/(1-radius)),'physical_gap_target':str(gap),'shift_per_physical_site':'c * 700741/500000','A_at_physical_seed':str(A),'initial_physical_base':physical_base,'initial_cell_base':cell_base,'uniform_S_lower':str(S0),'uniform_T_lower':str(T0),'anchor_physical_length':2*physical_base,'shifted_anchor_Rayleigh':seed['shifted_Rayleigh'],'initial_normalized_beta':'49/4','S_lower':str(initial_s),'T_lower':str(initial_t),'states':states,'terminal':terminal,'finite_bridge':{'cell_min':2,'cell_max':cell_base-1,'physical_min':4,'physical_max':physical_base-2,'uniform_gap_premise':'31/1250','worst_gap_lower':str(short_lower),'margin':str(short_lower-gap)},'all_integer_cells_at_least':2 if passed else None,'unique_ground_state':passed}
rows=[
 check(32,F(1,20000),F(1,50)),
 check(32,F(7,100000),F(3,200)),
 check(32,F(17,200000),F(1,100)),
 check(32,F(9,100000),F(1,200)),
 check(34,F(69,1000000),F(3,200)),
 check(34,F(89,1000000),F(1,200)),
 check(30,F(1,25000),F(3,200)),
 check(30,F(7,100000),F(1,200)),
]
assert all(r['status']=='EXACT_PRODUCER_PASS_INDEPENDENT_REVIEW_REQUIRED' for r in rows)
result={'claim_status':'Producer proof; positive cell factorization, window lemma and exact scalars require independent review','model':'H_M(g)=sum_j(h_(2j-1,2j)+g*h_(2j,2j+1)), spin1, designated exchange1, periodic M>=2','source_uniform_seed_physical_lengths':[30,32,34],'source_anchor_physical_lengths':[60,64,68],'linear_trial_dimension':1,'MPS_bond_dimension':26,'positive_transfer_window':'C=min(S sqrt(T),T), any integer cell base>=2','rows':rows,'dependencies':pins,'old_accepted_intervals_preserved':True,'resources':{'hard_cpu_seconds':30,'hard_address_space_mib':256,'process_cpu_seconds':time.process_time()-START,'monotonic_wall_seconds':time.monotonic()-WALL,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'prior_successful_scalar_cpu_seconds':0.05302305+0.000543495+0.033921867+0.307987337,'conservative_cpu_seconds_charged_for_all_preliminary_probes':4,'prior_failed_design_exit':'One floating-only probe stopped with ZeroDivisionError (about0.22s wall); one exact run stopped at an overstrong all-pass assertion (about0.47s wall); no result accepted from either. A later mixed-result exact replay was preserved as preliminary_certificate.json. The 60-digit grid saturated at1e-60; final exact grid is1e-120. All earlier scalar activity, including the earlier successful120-digit replay, is conservatively charged4CPU seconds.','no_physical_contractions':True,'no_eigensolver':True,'no_campaign':True}}
(P/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
for r in rows:
    print(r['status'],'physical n=',r['initial_physical_base'],'eta=',r['eta_radius'],'g=',r['g_lower'],r['g_upper'],'gap=',r['physical_gap_target'],'rounds=',len(r['states']),'short=',float(F(r['finite_bridge']['worst_gap_lower'])))
print(json.dumps(result['resources'],sort_keys=True))
