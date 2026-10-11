#!/usr/bin/env python3
from pathlib import Path
from math import ceil,isqrt
import hashlib,json,os,resource
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
P=Path(__file__).resolve().parent;RUN=P/'snapshot/campaign'
def sha(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def obj(p):
 x=json.loads(p.read_text());assert set(x)=={'payload','sha256'} and x['sha256']==sha(can(x['payload']));return x['payload']
for f,h in json.loads((P/'SNAPSHOT_SHA256.json').read_text()).items():assert sha((RUN/f).read_bytes())==h
ledger=obj(RUN/'ledger.json');assert ledger['terminal_state']=='BUDGET_RESERVATION_EXHAUSTED' and ledger['limit']==21600 and ledger['deadline']==1791698400
assert len(ledger['attempts'])==len({a['id'] for a in ledger['attempts']})==61
complete=overhead=unknown=0;failed=[]
for a in ledger['attempts']:
 assert a['status'] not in ('ACTIVE','RESERVED')
 if a['kind']=='supervisor':assert a['status']=='OVERHEAD' and a['charge']==a['reservation']==122;overhead+=a['charge'];continue
 d=a['details'];n=d['n'];act=d['action'];children=4*(n+1) if act=='prepare' else 2*(n+1)+(32 if act=='run' else 0);assert a['reservation']==122*(children+2)
 if a['status']=='COMPLETE':
  r=obj(RUN/(a['id']+'.completion.json'));assert r==a['result'] and r['attempt_id']==a['id'] and r['identity']==a['identity'] and r['verified_wait4'] and r['runner_reaped'] and r['wait_status']==0
  assert r['child_cpu']<=a['terminal_wait4_cpu']<=a['reservation'];assert a['charge']==min(a['reservation'],ceil(a['terminal_wait4_cpu'])+2);complete+=a['charge']
 else:
  assert a['status']=='UNKNOWN_CHARGED' and a['wait_status']==9 and d['n']==12 and act=='run' and a['charge']==a['reservation']==7320
  log=(RUN/(a['id']+'.completion.log')).read_text();assert "AssertionError: (-9, '')" in log
  unknown+=a['charge'];failed.append(d['twist'])
assert sorted(failed)==['I','P'];total=complete+overhead+unknown;assert total==16207 and ledger['limit']-total==5393 and 5393<7320
partials=[];partial_count=0
for t,want in [('I',16),('P',12)]:
 folder=RUN/'cases'/f'L12_{t}';assert not (folder/'certificate.json').exists();case=obj(folder/'case.json');mat=json.loads((P/'matrix_L12.json').read_text())['payload'];orbit=json.loads((P/'orbits_L12.json').read_text())['payload'] if (P/'orbits_L12.json').exists() else None
 assert case['pins']==obj(RUN/'cases/L4_I/case.json')['pins']
 assert case['parameters']=={'n':12,'twist':t,'beta':'49/4','shift':'700741/500000','cutoff':280,'Q':2**55,'mode':'full_nonnegative_M','batch_size':16}
 assert orbit is not None and [sec['M'] for sec in case['sectors']]==list(range(13))
 expected={}
 for sec in case['sectors']:
  m=sec['M'];assert mat[m]['M']==m and sec['matrix_sha256']==mat[m][t+'_matrix_sha256']
  if orbit:assert sec['representatives']==orbit[str(m)]['representatives']
  rr=sec['representatives'];assert sha(can(rr))==sec['orbit_sha256']
  for start in range(0,len(rr),16):
   count=min(16,len(rr)-start);name=f'M{m:02d}_start{start:06d}_count{count:04d}.json';expected[name]=(sec,start,count)
 files=sorted(folder.glob('M*.json'));assert len(files)==want;cpu=[];seen=set();mass=0
 for f in files:
  sec,start,count=expected[f.name];p=obj(f);ident={'case_sha256':sha(can(case)),'parameters':case['parameters'],'pins':case['pins'],'M':sec['M'],'start':start,'count':count,'matrix_sha256':sec['matrix_sha256'],'orbit_sha256':sec['orbit_sha256']};assert p['identity']==ident
  rows=p['records'];assert len(rows)==count and [(r['code'],r['multiplicity']) for r in rows]==[tuple(v) for v in sec['representatives'][start:start+count]]
  E=281*(isqrt(3**12)+2)+1
  for r in rows:assert type(r['norm_squared']) is int and 0<=r['norm_squared']<=(2**55+E)**2 and r['code'] not in seen;seen.add(r['code']);mass+=r['multiplicity']
  assert p['weighted_norm']==sum(r['multiplicity']*r['norm_squared'] for r in rows);cpu.append(p['resources']['cpu_seconds'])
 assert [f.name for f in files]==[f'M00_start{16*j:06d}_count0016.json' for j in range(want)]
 cap_upper=int(120-sum(cpu))-1;assert cap_upper in (2,4) and min(cpu[-4:])>cap_upper
 partials.append({'seam':t,'valid_batches':want,'saved_columns':len(seen),'weighted_multiplicity':mass,'expected_full_batches':len(expected),'sum_completed_child_CPU_seconds':sum(cpu),'next_child_CPU_cap_upper_bound':cap_upper,'recent_batch_CPU_seconds':cpu[-4:],'no_full_trace_certificate':True});partial_count+=want
certs=list((RUN/'cases').glob('*/certificate.json'));assert len(certs)==16
complete_batches=sum(obj(p)['complete_batches'] for p in certs);assert complete_batches==962 and complete_batches+partial_count==990
out={'status':'ACCEPTED partial physical reproduction only','full_cases':16,'full_lengths':[4,5,6,7,8,9,10,11],'seams':['I','P'],'missing_full_cases':['L12_I','L12_P'],'valid_saved_batches':990,'valid_completed_case_batches':962,'valid_partial_L12_batches':partials,'ledger_terminal_state':ledger['terminal_state'],'charged_CPU_seconds':total,'completed_attempt_charges':complete,'supervisor_overhead_charge':overhead,'unknown_failed_attempt_charges':unknown,'remaining_CPU_ledger_capacity':5393,'failed_reservations_retained':True,'no_active_attempts':True,'cause':'Observed childSIGKILL(-9); deterministic next allowance at most2/4CPU seconds vs recent6.8–9.9second batches strongly supports invocation-budget boundary as cause. No per-kill kernel diagnosis was recorded.','prior_fixture_gap':'Scheduling fixtures tested failed-attempt accounting and cleanup, but not a successful batch sequence approaching the runner allowance boundary.','restart_or_refund_authorized':False,'all18_thermal_premises_discharged':False}
(P/'partial_outcome_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
