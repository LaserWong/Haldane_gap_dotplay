#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,resource,os,re
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
P=Path(__file__).resolve().parent;R=P.parent;ROOT=R.parent;H={}
def rd(p):
 b=p.read_bytes();H[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(rd(p))
def ints(p):return {k:int(v) for k,v in (l.split('=') for l in rd(p).decode().splitlines())}
old=R/'uniform_anchor96_100_review';assert hashlib.sha256(rd(old/'MANIFEST_SHA256.json')).hexdigest()=='99317ea99db7892f33852e6a0b12b9aa4d3825527852ff605d7d86f22d3f22d7'
for f,h in js(old/'MANIFEST_SHA256.json').items():assert hashlib.sha256(rd(old/f)).hexdigest()==h
assert rd(P/'contract_sequential')==rd(old/'contract_sequential') and rd(P/'contract_sequential.cpp')==rd(old/'contract_sequential.cpp')
assert rd(P/'rebuild_d26.py')==rd(old/'rebuild_d26.py').replace(b'(120,120)',b'(60,60)')
assert rd(P/'limited_run.py')==rd(old/'limited_run.py').replace(b'(120,120)',b'(60,60)')
assert rd(P/'d26_blocks.txt')==rd(ROOT/'audit/mps/mps_blocks.txt');assert hashlib.sha256((P/'d26_blocks.txt').read_bytes()).hexdigest()=='26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa'
a=ints(P/'benchmark48.out');b=ints(R/'mps_excited_seed_witnesses/ground_lengths.out');assert set(a)=={'H0_48','N0_48'} and all(a[k]==b[k] for k in a)
ours=ints(P/'anchors.out');prod=ints(R/'uniform_smaller_second_initialization/anchors.out');prod.update(ints(R/'uniform_smaller_second_initialization/anchor60.out'));assert ours==prod
rebuilt=js(P/'independent_d26.json');assert rebuilt['D']==26 and rebuilt['status']=='PASS';prior=js(R/'nonperturbative_mps_review/d26_rebuild_results.json')
assert [(x['n'],x['norm'],x['total_H_numerator']) for x in rebuilt['direct_amplitude_checks']]==[(x['L'],x['norm'],x['total_H_numerator']) for x in prior['direct_amplitude_checks']]
rows=[]
for n in (60,64,68):
 h,v=ours[f'H0_{n}'],ours[f'N0_{n}'];assert v>0;energy=F(h,v)+n*F(700741,500000);assert energy<0
 rows.append({'length':n,'norm':str(v),'total_H_numerator':str(h),'shifted_total_Rayleigh':str(energy),'display':float(energy),'trial_bond_dimension':26,'trial_span_dimension':1,'physical_Hilbert_dimension':f'3^{n}'})
resources={}
for f in ('benchmark48.log','anchors.log'):
 txt=rd(P/f).decode();m=re.search(r'cpu_seconds=(\S+) peak_kib=(\d+)',txt);assert m;resources[f]={'CPU_seconds':float(m[1]),'RSS_KiB':int(m[2])}
resources['rebuild_CPU_seconds']=rebuilt['cpu_seconds'];resources['total_scientific_CPU_seconds']=sum(resources[x]['CPU_seconds'] for x in ('benchmark48.log','anchors.log'))+rebuilt['cpu_seconds'];assert resources['total_scientific_CPU_seconds']<60
out={'status':'ACCEPTED independently rebuilt physical D26 anchors60/64/68','rows':rows,'resources':resources,'producer_manifest':(P/'PRODUCER_MANIFEST_SHA256.txt').read_text().strip(),'no_gap_from_anchor_alone':True}
(P/'anchor_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'ANCHOR_INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(out['status']);print(resources)
