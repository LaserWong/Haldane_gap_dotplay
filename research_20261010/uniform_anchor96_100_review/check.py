#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import os,resource,json,hashlib,sys
sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent;R=P.parents[1];A=P.with_name('uniform_moment_optimality_assessment');C=P.with_name('uniform_cooled_seed_review')
resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
def ints(p):return {k:int(v) for line in read(p).decode().splitlines() for k,v in [line.split('=')]}
seals={}
for folder in (A,C,P.with_name('uniform_moment_optimality_review')):
 m=js(folder/'MANIFEST_SHA256.json')
 for f,h in m.items():assert hashlib.sha256(read(folder/f)).hexdigest()==h
 seals[folder.name]=hashlib.sha256((folder/'MANIFEST_SHA256.json').read_bytes()).hexdigest()
assert seals['uniform_moment_optimality_assessment']=='c862245e77fdf20e4e85859cbca804d888c96c11efcab2c30b5cbfedca3906cd'
assert seals['uniform_moment_optimality_review']=='60bb3811a98e6335d5054ff2c87c80656da8f47e5ab7e556a7a720714748525a'
assert read(P/'contract_sequential')==read(C/'contract_sequential')
assert read(P/'contract_sequential.cpp')==read(C/'contract_sequential.cpp')
assert read(P/'d26_blocks.txt')==read(R/'audit/mps/mps_blocks.txt')
assert inputs[str((R/'audit/mps/mps_blocks.txt').relative_to(R))]=='26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa'
rebuilt=js(P/'independent_d26.json');assert rebuilt['status']=='PASS' and rebuilt['D']==26 and rebuilt['transfer_dimension']==676
prior=js(R/'research_20261010/nonperturbative_mps_review/d26_rebuild_results.json');assert [(x['n'],x['norm'],x['total_H_numerator']) for x in rebuilt['direct_amplitude_checks']]==[(x['L'],x['norm'],x['total_H_numerator']) for x in prior['direct_amplitude_checks']]
bench=ints(P/'benchmark48.out');old=ints(R/'research_20261010/mps_excited_seed_witnesses/ground_lengths.out')
assert all(bench[k]==old[k] for k in bench) and set(bench)=={'H0_48','N0_48'}
now=ints(P/'anchors.out');prod=ints(A/'anchors.out');assert now==prod and set(now)=={'H0_96','N0_96','H0_100','N0_100'}
probe=js(A/'anchor_probe.json');rows=[]
for L in (96,100):
 H,N=now[f'H0_{L}'],now[f'N0_{L}'];assert N>0
 margin_num=-(500000*H+700741*L*N);assert margin_num>0
 unshifted=F(H,N);shifted=-F(margin_num,500000*N)
 assert shifted==F(next(v['shifted_Rayleigh_exact'] for v in probe['rows'] if v['L']==L))
 rows.append({'L':L,'norm_exact':str(N),'total_H_numerator_exact':str(H),'total_unshifted_Rayleigh_exact':str(unshifted),'total_shifted_Rayleigh_exact':str(shifted),'shifted_display':float(shifted),'positive_shift_margin_integer':str(margin_num),'per_bond_unshifted_Rayleigh_exact':str(unshifted/L),'physical_dimension':f'3^{L}','trial_bond_dimension':26,'trial_span_dimension':1,'norm_transfer_dimension':676})
result={'status':'ACCEPTED fresh independent physical MPS96/100 anchors only','rows':rows,'prior_seals_unchanged':seals,'method':'Fresh entrywise local matrices and physical insertion; sealed sequential-power engine on freshly rebuilt blocks; no producer engine executed','resources':{'cpu':5,'hard_memory_MiB':100,'hard_CPU_seconds':120},'does_not_certify':'a gap, thermal upper denominator, or n48/n50 bootstrap success'}
(P/'results.json').write_text(json.dumps(result,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
print(json.dumps({'status':result['status'],'rows':[{'L':x['L'],'shifted_Rayleigh':x['shifted_display']} for x in rows],'resources':result['resources']},indent=2))
