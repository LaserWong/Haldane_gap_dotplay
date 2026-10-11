#!/usr/bin/env python3
"""Finite-seed alternating-chain robustness. No physical matrices are formed."""
import hashlib, json, os, resource, sys, time
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
resource.setrlimit(resource.RLIMIT_AS, (256*1024**2, 256*1024**2))
sys.set_int_max_str_digits(100000)
START=time.process_time(); WALL=time.monotonic()
P=Path(__file__).resolve().parent; ROOT=P.parents[1]; B=10**60
inputs={}
def read(rel):
    p=ROOT/rel; data=p.read_bytes(); inputs[rel]=hashlib.sha256(data).hexdigest(); return data
pins={
 'uniform_smaller_second_initialization':'fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84',
 'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f',
 'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf',
 'uniform_second_thermal_full_review':'792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94',
}
for name,h in pins.items(): assert hashlib.sha256(read(f'research_20261010/{name}/MANIFEST_SHA256.json')).hexdigest()==h
source=json.loads(read('research_20261010/uniform_smaller_second_initialization/certificate.json'))
seed=next(x for x in source['rows'] if x['n']==32)
assert seed['status']=='PASS_PRODUCER' and seed['anchor_length']==64 and F(seed['beta'])==F(49,4)
S0=F(seed['S']); T0=F(seed['T']); R64=F(seed['shifted_Rayleigh']); assert R64<0
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
def check(radius,gap):
    beta0=F(49,4); physical_base=32; cell_base=16
    A=F(9,8)*(beta0*radius*physical_base)**2
    s=down(S0*expi(-2*A)[0]); t=down(T0*expi(-8*A)[0]); initial_s=s;initial_t=t
    beta=beta0;n=cell_base;states=[];terminal=None
    for j in range(18):
        K=down(s*s*t)
        if K<=F(1,2): break
        w=(1+root(2*K-1)[0])/2; rho=(1-w)/w; d=down(t/(1+rho*rho))
        C=down((1-rho)*min(s*root(d)[0],d))
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
    short_lower=(F(31,1250)-3*30*radius)/(1+radius)
    passed=terminal is not None and short_lower>=gap
    return {'status':'EXACT_PRODUCER_PASS_INDEPENDENT_REVIEW_REQUIRED' if passed else 'FAILED_SUFFICIENT_TEST_NOT_NO_GO','eta_radius':str(radius),'g_lower':str((1-radius)/(1+radius)),'g_upper':str((1+radius)/(1-radius)),'physical_gap_target':str(gap),'shift_per_physical_site':'c * 700741/500000','A_at_physical32':str(A),'initial_cell_base':16,'initial_normalized_beta':'49/4','S_lower':str(initial_s),'T_lower':str(initial_t),'states':states,'terminal':terminal,'finite_bridge':{'cell_min':2,'cell_max':15,'physical_min':4,'physical_max':30,'uniform_gap_premise':'31/1250','worst_gap_lower':str(short_lower),'margin':str(short_lower-gap)},'all_integer_cells_at_least':2 if passed else None,'unique_ground_state':passed}
rows=[check(F(1,20000),F(3,200)),check(F(1,12500),F(1,200))]
result={'claim_status':'Producer proof; new analytic comparison and scalar composition require independent review','model':'H_M(g)=sum_j(h_(2j-1,2j)+g*h_(2j,2j+1)), spin1, strong exchange1, periodic M>=2','uniform_seed_physical_length':32,'uniform_seed_cell_length':16,'uniform_S_lower':str(S0),'uniform_T64_lower':str(T0),'own_physical64_shifted_MPS_Rayleigh':str(R64),'rows':rows,'dependencies':pins,'resources':{'hard_cpu_seconds':30,'hard_address_space_mib':256,'process_cpu_seconds':time.process_time()-START,'monotonic_wall_seconds':time.monotonic()-WALL,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'prior_float_proposal_cpu_seconds':0.000543495,'no_physical_contractions':True,'no_eigensolver':True,'no_campaign':True}}
(P/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
for r in rows:
    print(r['status'],'eta=',r['eta_radius'],'g=',r['g_lower'],r['g_upper'],'gap=',r['physical_gap_target'],'rounds=',len(r['states']),'short=',float(F(r['finite_bridge']['worst_gap_lower'])))
print(json.dumps(result['resources'],sort_keys=True))
