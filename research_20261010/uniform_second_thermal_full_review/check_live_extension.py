#!/usr/bin/env python3
"""Read-only validation of extension and completed partial checkpoints."""
from pathlib import Path
from math import isqrt,ceil
import hashlib,json,os,resource
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
P=Path(__file__).resolve().parent;RUN=__import__('snapshot_reader').campaign(P);OLD=P.with_name('uniform_second_thermal_partial_review')
def sha(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def load(p):
 x=json.loads(p.read_text());assert x['sha256']==sha(can(x['payload']));return x['payload']
old=load(OLD/'snapshot/campaign/ledger.json');ledger=load(RUN/'ledger.json');assert ledger['limit']==43200 and ledger['deadline']==1791698400 and ledger['attempts'][:61]==old['attempts'] and ledger['bindings']==old['bindings'] and len(ledger['extensions'])==1
e=ledger['extensions'][0];assert (e['old_limit'],e['additional_budget'],e['new_limit'],e['retained_charge'],e['original_attempt_count'])==(21600,21600,43200,16207,61);assert e['authorization_id']=='root-20261011-cap-extension-21600-to-43200' and e['original_terminal_sha256']=='9a6b8fe6944c06544247c07b04344e2258784cbfc722f902b3cc2b979d57f288'
assert sha((RUN/'history'/('original_terminal_'+e['original_terminal_sha256']+'.json')).read_bytes())==e['original_terminal_sha256']
assert ledger['active_extension_bindings']==e['new_bindings']
for f,h in e['new_bindings'].items():assert sha(Path(f).read_bytes())==h
for f,h in json.loads((OLD/'SNAPSHOT_SHA256.json').read_text()).items():
 if f!='ledger.json':assert sha((RUN/f).read_bytes())==h
# Distinguish new failed attempts from the two retained historical failures.
new_failed=[]
for a in ledger['attempts'][61:]:
 if a['kind']=='supervisor':assert a['charge']==a['reservation']==122;continue
 d=a['details'];meta=4*(d['n']+1) if d['action']=='prepare' else 2*(d['n']+1);nc=8 if d['action']=='run' else 0;assert d['max_new_batches']==8 and a['reservation']==meta*7+(nc+2)*37
 if a['status']=='COMPLETE':
  assert a['charge']==min(a['reservation'],ceil(a['terminal_wait4_cpu'])+2);assert load(RUN/(a['id']+'.completion.json'))==a['result']
 elif a['status'] not in ('ACTIVE','RESERVED'):new_failed.append(a['id'])
assert sum(a['charge'] for a in ledger['attempts'])<=43200
summary=[]
for t in ('I','P'):
 folder=RUN/'cases'/f'L12_{t}';case=load(folder/'case.json');expected=[];meta={};orbit=load(P/'orbits_L12.json');mat=load(P/'matrix_L12.json')
 assert case['pins']==load(RUN/'cases/L4_I/case.json')['pins']
 for sec in case['sectors']:
  m=sec['M'];assert sec['representatives']==orbit[str(m)]['representatives'] and sec['dimension']==orbit[str(m)]['dimension'] and sec['matrix_sha256']==mat[m][t+'_matrix_sha256']
  for start in range(0,len(sec['representatives']),16):
   cnt=min(16,len(sec['representatives'])-start);name=f'M{m:02d}_start{start:06d}_count{cnt:04d}.json';expected.append(name);meta[name]=(sec,start,cnt)
 files=sorted(folder.glob('M*.json'));assert [f.name for f in files]==expected[:len(files)]
 columns=0;codes=set()
 for f in files:
  sec,start,cnt=meta[f.name];p=load(f);ident={'case_sha256':sha(can(case)),'parameters':case['parameters'],'pins':case['pins'],'M':sec['M'],'start':start,'count':cnt,'matrix_sha256':sec['matrix_sha256'],'orbit_sha256':sec['orbit_sha256']};assert p['identity']==ident
  rows=p['records'];assert len(rows)==cnt and [(r['code'],r['multiplicity']) for r in rows]==[tuple(x) for x in sec['representatives'][start:start+cnt]]
  E=281*(isqrt(3**12)+2)+1
  for r in rows:assert type(r['norm_squared']) is int and 0<=r['norm_squared']<=(2**55+E)**2 and r['code'] not in codes;codes.add(r['code'])
  assert p['weighted_norm']==sum(r['multiplicity']*r['norm_squared'] for r in rows);columns+=cnt
 summary.append({'seam':t,'valid_batches':len(files),'expected_batches':len(expected),'columns':columns,'full_certificate_exists':(folder/'certificate.json').exists()})
out={'status':'PASS read-only checkpoint/extension audit' if not new_failed else 'NEW FAILED ATTEMPT requires root review','ledger_state':ledger['terminal_state'],'historical_charge_retained':16207,'total_current_charges':sum(a['charge'] for a in ledger['attempts']),'new_failed_attempts':new_failed,'all_old_snapshot_files_unchanged_except_authorized_ledger_extension':True,'L12':summary}
(P/'live_extension_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
