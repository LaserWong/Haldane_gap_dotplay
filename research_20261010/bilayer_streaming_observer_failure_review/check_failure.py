import os,json,hashlib,math,resource,fcntl
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent;D=ROOT/'bilayer_full_m4_production_run_streaming';S=ROOT/'bilayer_streaming_hash_revision';E=P/'evidence';E.mkdir()
assert os.sched_getaffinity(0)=={7} and resource.getrlimit(resource.RLIMIT_CPU)==(3,3)
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(32768),b''):h.update(b)
 return h.hexdigest()
manifest=D/'FAILED_OBSERVER_MANIFEST_SHA256.json';assert digest(manifest)=='552153e60e66c147e6384cca5f6b878e6a7cfac271cc35d4e0d66a0ed2e17b73';mp=read(manifest);assert len(mp)==650
for name,expected in mp.items():
 p=D/name;assert digest(p)==expected
 dest=E/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
(E/manifest.name).write_bytes(manifest.read_bytes())
pins=read(D/'PINNED_INPUTS.json');assert len(pins)==26 and all(digest(p)==h for p,h in pins.items())
job=sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins)));assert job=='845b55d815552ca70bb870f0efd6be20a94850f952e63a87dc7a0338553e8a0e'
rows=[]
for q,n,w,cap in [(0,1,1,3),(2,496,64,3),(4,4495,16,3),(6,169911,64,6)]:
 for start in range(0,n,w):rows.append(dict(q=q,N=n,begin=start,end=min(start+w,n),cap=cap))
assert len(rows)==2945 and sum(r['cap'] for r in rows)==16800
state=read(D/'store/state.json');assert state==dict(committed_count=63,job=job,kind='PHYSICAL-FIXED-WITNESS24',worker_charged=192)
assert sorted(x.name for x in (D/'store/attempts').glob('*.json'))==[f'{i:04d}.json' for i in range(64)]
assert sorted(x.name for x in (D/'store/committed').glob('*.json'))==[f'{i:04d}.json' for i in range(63)]
assert sorted(x.name for x in (D/'store/outputs').glob('*.json'))==[f'{i:04d}.json' for i in range(63)]
sector={q:[0]*24 for q in [0,2,4,6]};targets={q:[] for q in sector};wait4=0;setup=0;body=0
for i in range(64):
 a=read(D/'store/attempts'/f'{i:04d}.json');assert a['id']==i and a['job']==job and a['range']==rows[i] and a['charged']==3 and a['forecast']==21600
 if i==63:assert a['state']=='reserved';continue
 assert a['state']=='complete';e=read(D/'store/committed'/f'{i:04d}.json');v=e['payload'];out=D/'store/outputs'/f'{i:04d}.json'
 assert out.read_bytes()==raw(v) and e['sha256']==sha(raw(v))==a['output_sha256'] and e['receipt_sha256']==sha(raw(a))
 assert v['job']==job and v['schema']=='bilayer-moment24-v1' and v['kind']=='PHYSICAL-FIXED-WITNESS24' and v['id']==i and v['range']==rows[i]
 val=v['values'];assert len(val)==24 and all(type(x) is str and str(int(x))==x for x in val)
 rdir=D/'raw_outputs'/f'{i:04d}_{3*(i+1)}';receipt=read(rdir/'receipt.json');assert receipt['identity']==pins and receipt['exit']==0 and receipt['reason'] is None
 assert sha(raw(receipt))==v['worker_receipt_sha256'] and 0<=receipt['wait4_cpu']<=3;wait4+=receipt['wait4_cpu']
 required={'result.json','result.json.schema.json','result.json.accumulators.json','chunk.json','targets.jsonl'};assert required<=set(receipt['output_sha256'])
 assert all(Path(name).name==name and digest(rdir/name)==h for name,h in receipt['output_sha256'].items())
 assert read(rdir/'result.json.accumulators.json')==val and read(rdir/'result.json.schema.json')==dict(schema='bilayer-moment24-v1',fields=24)
 q=rows[i]['q'];stride={0:1,2:127,4:1024,6:65536}[q];meta=read(rdir/'chunk.json');assert all(meta[k]==rows[i][k] for k in ['q','begin','end','N']) and meta['stride']==stride;setup+=meta['setup_cpu'];body+=meta['body_cpu']
 t=[json.loads(x) for x in (rdir/'targets.jsonl').read_text().splitlines()];assert [x['id'] for x in t]==list(range(rows[i]['begin'],rows[i]['end'])) and all(x['rank']==stride*x['id']%rows[i]['N'] for x in t);targets[q]+=t
 z=list(map(int,val));result=read(rdir/'result.json');assert result['complete'] and list(result['terms'].values())==val[:15]
 assert list(map(int,result['moments']))==[z[15],z[16],z[17]+121*z[20],z[18]+193600*z[20]+1331*sum(z[:4])+z[21],z[19]+sum(z[4:10])+14641*sum(z[10:15])]
 for j,x in enumerate(z):sector[q][j]+=x
coverage={q:len(t) for q,t in targets.items()};assert coverage=={0:1,2:496,4:864,6:0}
for q,t in targets.items():assert len(set(x['rank'] for x in t))==len(t) and [x['id'] for x in t]==list(range(len(t)))
assert all(math.gcd({0:1,2:127,4:1024,6:65536}[q],n)==1 for q,n in [(0,1),(2,496),(4,4495),(6,169911)])
failed=read(D/'FAILED_OBSERVER_PRE100.json');assert failed['raw_partial_sector24']=={str(q):list(map(str,v)) for q,v in sector.items()} and failed['committed_ids']==list(range(63)) and failed['partial_only'] and failed['exact_failure_tuple_unavailable']
control=read(D/'CONTROL_SESSIONS.json');assert control['prepaid']==1200 and control['reserved']==463==sum(x['charged'] for x in control['sessions'])
assert [r['id'] for r in control['sessions']]==list(range(5)) and [r['charged'] for r in control['sessions']]==[120,100,120,100,23]
assert control['sessions'][:2]==read(D/'CONTROL_SESSIONS_CARRY_FORWARD.json')['sessions']
assert failed['worker_reservations_charged']==192 and failed['cumulative_reserved_sum']==463+192==655
outer=read(D/'OUTER_RESULT_2.json');assert outer['job_id']==job and outer['reason']=='outer_accounting_or_resource_failure' and outer['sessions']==0 and outer['reserved']==120 and outer['wait4_tree_cpu']>=wait4
assert 'post_exec_limit_mismatch' in (D/'launch.log').read_text()
assert not(D/'FULL_MOMENTS.json').exists() and not list(D.glob('CHECKPOINT_READY_*.json')) and not list(D.glob('CONTINUE_AFTER_*.json'))
assert not(D/'PROCESSES_MATCHING_JOB_AT_FAILURE.txt').read_text().strip()
matching=[];entrypaths={str(S/x) for x in ['outer.py','production_supervisor.py','physical_session.py']}
for p in Path('/proc').iterdir():
 if not p.name.isdecimal():continue
 try:args=(p/'cmdline').read_bytes().split(b'\0')
 except FileNotFoundError:continue
 ss=[x.decode(errors='replace') for x in args]
 if any(x in entrypaths for x in ss) or (str(ROOT/'bilayer_variable_g_control_gate/whole') in ss and any(x.startswith(str(D/'raw_outputs')) for x in ss)):matching.append(int(p.name))
assert not matching
for name in ['LOCK','OUTER_LOCK']:
 with (D/name).open('r') as f:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(f,fcntl.LOCK_UN)
forecast=read(D/'FAILED_FORECAST.json');assert forecast['remaining_standard_if_reusing63']==16800-189==16611 and forecast['remaining_retry_if_reusing63']==3600-3==3597
assert forecast['proposal_control_planned_total']==463+220+690==1373 and forecast['proposal_control_remaining']==1600-1373==227 and forecast['proposal_retry_after_retired_workers']==3200-192==3008
report=dict(status='PASS_PARTIAL_RECEIPT_AND_FAILURE_ACCOUNTING',job=job,producer_failure_seal=digest(manifest),source_files=650,committed_chunks=63,covered_targets=coverage,uncommitted_reserved_attempt=63,worker_charge=192,control_charge=463,total_charge=655,completed_worker_wait4_CPU=wait4,completed_worker_setup_CPU=setup,completed_worker_body_CPU=body,outer_tree_CPU=outer['wait4_tree_cpu'],outer_self_CPU=outer['self_cpu'],combined_peak_RSS=outer['combined_peak_rss_bytes'],no_matching_processes=matching,locks_available=True,all24_signed_accumulators_preserved=True,exact_failure_cause_proven=False,production_gate='FAIL_REQUIRES_OBSERVER_REPAIR',full_moments=False,normalization_note='Partial raw sector totals only; no full accepted57D m012 gate or positivity assumption.',new_partition_proposal=dict(standard=16800,control=1600,retry=3200,retired_workers=192,control_carry=463,control_forecast=1373,retry_remaining=3008))
(P/'CHECKS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
