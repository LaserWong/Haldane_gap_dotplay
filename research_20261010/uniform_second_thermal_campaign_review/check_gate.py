#!/usr/bin/env python3
from pathlib import Path
from math import isqrt
from copy import deepcopy
import json,hashlib,os,resource
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
P=Path(__file__).resolve().parent;A=P.with_name('uniform_second_thermal_campaign_gate');R=P.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
assert sha((A/'MANIFEST_SHA256.json').read_bytes())=='4a282841f56100a6ea99d20d9ce63a79309afe0d1ecdec12f39dee4f94013b68'
m=json.loads((A/'MANIFEST_SHA256.json').read_text());assert all(sha((A/f).read_bytes())==h for f,h in m.items())
for f,h in json.loads((A/'INPUT_SHA256.json').read_text()).items():assert sha((R/f).read_bytes())==h
fixtures=json.loads((P.with_name('uniform_second_thermal_kernel_review')/'fixture_results.json').read_text())
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def seal(o):return {'payload':o,'sha256':sha(canonical(o))}
rows=[dict(code=r['code'],multiplicity=r['multiplicity'],norm_squared=int(r['norm_squared'])) for r in fixtures['records'] if (r['n'],r['twist'],r['weight'])==(5,'P',0)]
ident={'n':5,'twist':'P','M':0,'count':len(rows),'start':0,'pins':{f:sha((A/f).read_bytes()) for f in ['kernel.cpp','kernel','coefficients.txt','campaign.py']}}
base={'identity':ident,'records':rows,'weighted_norm':sum(r['multiplicity']*r['norm_squared'] for r in rows),'resources':{}}
def validate(o):
 assert set(o)=={'payload','sha256'} and o['sha256']==sha(canonical(o['payload']))
 p=o['payload'];assert set(p)=={'identity','records','weighted_norm','resources'} and p['identity']==ident
 rs=p['records'];assert len(rs)==ident['count'] and [(r['code'],r['multiplicity']) for r in rs]==[(r['code'],r['multiplicity']) for r in rows]
 d=isqrt(3**ident['n'])+1;cap=(2**55+281*(d+1)+1)**2
 for r in rs:assert set(r)=={'code','multiplicity','norm_squared'} and type(r['norm_squared']) is int and 0<=r['norm_squared']<=cap
 assert p['weighted_norm']==sum(r['multiplicity']*r['norm_squared'] for r in rs)
 return p
validate(seal(base));validate(seal(base));tests=[]
def reject(name,change):
 o=deepcopy(base);change(o)
 try:validate(seal(o))
 except (AssertionError,KeyError,TypeError,ValueError):tests.append(name);return
 raise AssertionError(name)
reject('stale kernel',lambda x:x['identity']['pins'].update(kernel='0'*64))
reject('wrong seam',lambda x:x['identity'].update(twist='I'))
reject('wrong M',lambda x:x['identity'].update(M=1))
reject('wrong start',lambda x:x['identity'].update(start=1))
reject('wrong count',lambda x:x['identity'].update(count=1))
reject('missing record',lambda x:x['records'].pop())
reject('duplicate record',lambda x:x['records'].append(x['records'][0]))
reject('wrong ordering',lambda x:x['records'].reverse())
reject('wrong multiplicity',lambda x:x['records'][0].update(multiplicity=999))
reject('negative norm',lambda x:x['records'][0].update(norm_squared=-1))
reject('float norm',lambda x:x['records'][0].update(norm_squared=1.0))
reject('bool norm',lambda x:x['records'][0].update(norm_squared=True))
reject('overflow norm',lambda x:x['records'][0].update(norm_squared=2**128))
reject('wrong aggregate',lambda x:x.update(weighted_norm=0))
# The runner source concretely places accounting start after metadata rebuilding.
s=(A/'campaign.py').read_text();assert s.index("for sector in case['sectors']")<s.index('startusage=resource.getrusage');assert 'deadline' not in s and 'cpu_budget-used' in s
out={'checkpoint_identity_logic':'ACCEPTED inspected source plus independent contract tests','campaign_launch':'BLOCKED pending aggregate CPU/deadline/two-worker supervisor','faults_rejected':tests,'producer_manifest':'4a282841f56100a6ea99d20d9ce63a79309afe0d1ecdec12f39dee4f94013b68','imported_code_execution':False,'new_kernel_invocations':0,'blockers':['per-invocation CPU budget resets','metadata setup outside local accounting','failed/retried attempts have no durable aggregate debit','no global stop deadline','no global two-worker enforcement']}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
