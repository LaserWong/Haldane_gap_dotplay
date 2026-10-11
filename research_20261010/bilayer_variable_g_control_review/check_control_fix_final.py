import os,sys,json,copy,time,hashlib,math,resource,fcntl,signal
from pathlib import Path
P=Path(__file__).resolve().parent;S=P/'memory_sandbox';sys.path.insert(0,str(S))
import engine as e
from session_supervisor import supervise
R=P/'control_checks_final';R.mkdir();checks=[]
def reject(fn,label):
 try:fn()
 except (AssertionError,ValueError,KeyError,TypeError):checks.append(label);return
 raise AssertionError('MUTATION_SURVIVED:'+label)
# Reconcile our own complete fresh2945 synthetic dataset with corrected source.
t=time.process_time();near=e.IncrementalJob(P/'control_fresh/data',e.read(P/'control_fresh/data/state.json')['job']);near.finish();assert near.reads['raw_outputs']==near.reads['new_adoptions']==0;checks.append('corrected_full2945_restart_zero_historical_outputs');restart=time.process_time()-t
rows=e.plan();assert len(rows)==2945 and sum(r['cap'] for r in rows)==16800
for q,N,stride in [(0,1,1),(2,496,127),(4,4495,1024),(6,169911,65536)]:
 rr=[r for r in rows if r['q']==q];assert rr[0]['begin']==0 and rr[-1]['end']==N and all(a['end']==b['begin'] for a,b in zip(rr,rr[1:]));assert math.gcd(stride,N)==1
checks.append('disjoint_complete2945_schedule_and_coprime_permutations')
# Signed values, receipt binding, and exact shape validation.
for mode in ['digest','kind','range','length','canonical','integer_type','incomplete']:
 d=R/mode;s=e.IncrementalJob(d,'SYNTHETIC-REVIEW-'+mode);a=s.reserve(0);a=s.complete_synthetic(0,a);s.adopt_one(0,a)
 f=d/'committed/0000.json';v=e.read(f)
 if mode=='digest':v['payload']['values'][23]='987654321'
 elif mode=='kind':v['payload']['kind']='PHYSICAL-FIXED-WITNESS24'
 elif mode=='range':v['payload']['range']['q']=2
 elif mode=='length':v['payload']['values'].pop()
 elif mode=='canonical':v['payload']['values'][0]='-012'
 elif mode=='integer_type':v['payload']['values'][0]=-12
 elif mode=='incomplete':a['state']='failed'
 v['sha256']=e.sha(e.raw(v['payload']))
 if mode!='digest':
  a['output_sha256']=v['sha256'];e.atomic(d/'attempts/0000.json',a);v['receipt_sha256']=e.sha(e.raw(a))
 e.atomic(f,v);reject(lambda:e.IncrementalJob(d,s.job),'restart_reject_'+mode)
# Incomplete->abandoned and no-refund retry archival crash recovery.
d=R/'retry';s=e.IncrementalJob(d,'SYNTHETIC-RETRY');a=s.reserve(0);s=e.IncrementalJob(d,s.job);a=e.read(d/'attempts/0000.json');assert a['state']=='abandoned' and s.worker_charged==s.failed_charged==3
reject(lambda:s.reserve(0),'no_implicit_retry');h=e.sha(e.raw(a));s.authorize_retry(0,h,'bounded-review-authority');e.atomic(d/'attempts/0000.json',a);z=e.IncrementalJob(d,s.job);assert z.worker_charged==z.failed_charged==3 and not(d/'attempts/0000.json').exists();z.authorize_retry(0,h,'bounded-review-authority');b=z.reserve(0);assert z.worker_charged==6 and b['forecast']==21600;checks.append('stale_abandon_archive_crash_idempotence_no_refund')
# Controller reservations remain after faults; refunds/inflation rejected.
c=e.ControlBudget(R/'budget.json');i=c.reserve(20,3);c.finish(i,.1,.01,'stopped');assert c.state['reserved']==23
reject(lambda:c.reserve(1200,3),'controller_prepaid_hard_cap')
for key,val in [('prepaid',2400),('reserved',0)]:
 bad=copy.deepcopy(c.state);bad[key]=val;f=R/('budget_bad_'+key+'.json');e.atomic(f,bad);reject(lambda:e.ControlBudget(f),'controller_mutation_'+key)
# Namespace split and canonical normalized output admission.
s=e.IncrementalJob(R/'physical_namespace','PHYSICAL-REVIEW','bilayer-moment24-v1','PHYSICAL-FIXED-WITNESS24');a=s.reserve(0);reject(lambda:s.complete_synthetic(0,a),'synthetic_cannot_enter_physical')
d=R/'noncanonical';s=e.IncrementalJob(d,'SYNTHETIC-NONCANONICAL');a=s.reserve(0);a=s.complete_synthetic(0,a);f=d/'outputs/0000.json';f.write_text(json.dumps(e.read(f),indent=2));a['output_sha256']=e.sha(f.read_bytes());e.atomic(d/'attempts/0000.json',a);reject(lambda:e.IncrementalJob(d,s.job),'noncanonical_normalized_bytes')
# Independent accepted vacuum aggregate and receipt-chain/restart validation.
import physical_session as phys
phys.ROOT=P.parent/'bilayer_control_memory_revision';phys.KERNEL=P.parent/'bilayer_variable_g_control_gate'
job=P/'vacuum_fixture';rawdir=next((job/'raw_outputs').iterdir());receipt=e.read(rawdir/'receipt.json');identity=e.read(job/'PINNED_INPUTS.json');row=dict(q=0,begin=0,end=1,N=1,cap=3)
values=phys.verify_output(rawdir,receipt,row,identity)
from analytic_vacuum_hopping import vacuum24
analytic=vacuum24(P.parent/'bilayer_whole_m4_pipeline');e.atomic(R/'VACUUM_DIAGNOSTIC.json',dict(expected=analytic,actual=values));assert values==analytic;checks.append('all24_fixed_witness_vacuum_accumulators_match_independent_local_edge_pair_contractions');e.atomic(R/'ANALYTIC_VACUUM24.json',analytic)
state=e.read(job/'store/state.json');vstore=e.IncrementalJob(job/'store',state['job'],phys.SCHEMA,phys.KIND);assert len(vstore.committed)==1 and len(vstore.pending)==2944 and vstore.reads['raw_outputs']==0
reject(lambda:vstore.finish(),'partial_vacuum_coverage_cannot_finalize')
assert not phys.required_pins(job)<=set();checks.append('mandatory_physical_pin_set_nonempty')
# New-format finalizer, tested only as a clearly labelled dense-fixture mock.
# Scale the accepted4x2 fixture by16, then exactly invert origin weights8,16/3.
from types import SimpleNamespace
ref=next(json.loads(x) for x in (P/'physical24/reference.jsonl').read_text().splitlines() if json.loads(x)['nx']==4 and json.loads(x)['type']=='generic')
sec=e.read(phys.KERNEL/'runs/generic4/sectors24.json');mult={0:16,2:16,4:2,6:3}
committed={i:dict(range={'q':int(q)},values=[str(mult[int(q)]*int(x)) for x in a]) for i,(q,a) in enumerate(sec.items())}
fake=SimpleNamespace(job='REVIEW_DENSE_FIXTURE_MOCK_NOT_PHYSICAL8X4',committed=committed,finish=lambda:None)
mj=R/'finalizer_fixture_mock';mj.mkdir();controls=dict(schema='accepted-fixed-witness-m012-v1',T_Q=200,T_A=11,witness_sha256=identity[str((phys.ROOT.parent/'bilayer_whole_m4_pipeline/witness57.txt').resolve())],geometry_sha256=identity[str((phys.ROOT.parent/'bilayer_whole_m4_pipeline/geometry_8x4.txt').resolve())],**{k:str(16*int(v)) for k,v in zip(['m0','m1','m2'],ref['moments'][:3])})
e.atomic(mj/'EXPECTED_M012.json',controls);phys.finalize_physical(fake,mj,identity);full=e.read(mj/'FULL_MOMENTS.json');assert full['m3']==str(16*int(ref['moments'][3])) and full['m4']==str(16*int(ref['moments'][4]));checks.append('new_format_finalizer_dense_fixture_mock_all24_sector_weights')
controls['m2']=str(int(controls['m2'])+1);bad=R/'finalizer_wrong_controls';bad.mkdir();e.atomic(bad/'EXPECTED_M012.json',controls);reject(lambda:phys.finalize_physical(fake,bad,identity),'wrong_complete_m012_controls_rejected');assert not(bad/'FULL_MOMENTS.json').exists()
# Whole-cost admission: every pending worker including zero-M targets is charged.
control=e.read(job/'CONTROL_SESSIONS.json');retry=3600-vstore.failed_charged;forecast=1200+vstore.worker_charged+vstore.pending_reserved+retry
slots=(1200-control['reserved'])//23+1;wall=2*(vstore.pending_reserved+retry)+10*(len(vstore.pending)+math.ceil(retry/3))+1200+60*slots+86400
assert forecast==21600 and vstore.pending_reserved==16797 and slots==52 and wall>170000
checks.append('nonzero_complete_remaining_CPU_and_wall_forecasts')

# Planned low-threshold external guard faults; each has its own no-refund inner charge.
results={}
for mode in ['controller','memory','supervisor']:
 out=R/('fault_'+mode);out.mkdir();pid=os.fork()
 if pid==0:
  lock=open(out/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  code='while True: pass' if mode=='controller' else 'import time; a=bytearray(70*1024*1024); time.sleep(10)' if mode=='memory' else 'import time;time.sleep(10)'
  kw=dict(watch_cpu=.2) if mode=='controller' else dict(memory_bytes=80*1024**2) if mode=='memory' else dict(supervisor_watch_cpu=.2)
  r=supervise([sys.executable,'-c',code],out,out/'budget.json',2,1,lock_fd=lock.fileno(),**kw);e.atomic(out/'RESULT.json',r);os._exit(0)
 _,status,u=os.wait4(pid,0);assert os.waitstatus_to_exitcode(status)==0
 r=e.read(out/'RESULT.json');expected={'controller':'controller_session_cpu_guard','memory':'combined_supervisor_controller_worker_memory_guard','supervisor':'supervisor_prepaid_cpu_guard'}[mode];assert r['reason']==expected and r['exit']!=0 and r['inherited_lock_verified'];assert e.read(out/'budget.json')['reserved']==3;results[mode]=r;checks.append('planned_'+mode+'_fault_stopped_reaped_no_refund')
# Planned controller death with a lock-inheriting descendant. No numerical work.
out=R/'controller_death';out.mkdir();pid=os.fork()
if pid==0:
 lock=open(out/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 r=supervise([sys.executable,str(P/'metadata_descendant.py'),str(out)],out,out/'budget.json',2,1,max_descendants=2,lock_fd=lock.fileno());e.atomic(out/'RESULT.json',r);os._exit(0)
end=time.monotonic()+5
while not(out/'PIDS.json').exists():
 assert time.monotonic()<end;time.sleep(.005)
pids=e.read(out/'PIDS.json');os.kill(pids['controller'],signal.SIGKILL)
_,status,u=os.wait4(pid,0);assert os.waitstatus_to_exitcode(status)==0
r=e.read(out/'RESULT.json');assert r['exit']<0 and all(not Path('/proc',str(n)).exists() for n in pids.values())
lock=open(out/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock.close();assert e.read(out/'budget.json')['reserved']==3
results['controller_death']=r;checks.append('controller_death_descendant_cleanup_lock_recovery_no_refund')
e.atomic(R/'CHECKS.json',dict(checks=checks,corrected2945_restart_cpu=restart,reads=near.reads,faults=results,self_cpu=time.process_time()));print('CONTROL TARGETED CHECKS PASS',len(checks))
