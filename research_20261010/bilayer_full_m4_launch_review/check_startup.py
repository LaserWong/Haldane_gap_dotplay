import os,sys,resource,json,hashlib,time,textwrap,fcntl
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import adapted_outer as o
from engine import raw,sha,atomic,read,ControlBudget
checks=[];real=read(P/'PROPOSED_PINNED_INPUTS.json');binding=read(P/'PROPOSED_JOB_ID.json')
assert sha((P/'PROPOSED_PINNED_INPUTS.json').read_bytes())==binding['pins_sha256']=='f1943170fe4fc309e05dac8df25b19ffe739e4a5d3cd08d4014268366a3eeeaf'
assert all(sha(Path(f).read_bytes())==h for f,h in real.items())
assert sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=real)))==binding['job_id']=='8bd34794ff776ba9222058c06ade5c76ffd85515518dbc7462d8fc7e49b21a14'
assert read(P/'CONTROLS_CHECK.json')['status']=='PASS_ACCEPTED57D_FIXED_WITNESS_M012'
checks.append('final_proposed_job_and_all_source_controls_pins_exact')
launch=(P/'source/launch.sh').read_text();assert '--cpu=99:100 --as=67108864:134217728' in launch and 'taskset -c 6' in launch
assert os.sched_getaffinity(0)=={7} and resource.getrlimit(resource.RLIMIT_CPU)==(20,22) and resource.getrlimit(resource.RLIMIT_AS)==(64*1024**2,128*1024**2)
checks.append('pre_interpreter_limits_and_affinity_applied_lowered_review_profile')
# Execute the unchanged stage-token validation fragment without dispatching workers.
s=(P/'source/outer.py').read_text();fragment=s[s.index('   cap=100\n'):s.index('   statepath=')];ns=dict(read=read,sha=sha,raw=raw);exec('def stage(JOB,job):\n'+textwrap.indent(textwrap.dedent(fragment),' ')+' return cap\n',ns);stage=ns['stage']
td=P/'token_tests';td.mkdir();jobid='REVIEW-SYNTHETIC-TOKEN-ONLY'
def reject(fn):
 try:fn()
 except (AssertionError,KeyError):return
 raise AssertionError('unsafe token survived')
assert stage(td,jobid)==100
state=dict(committed_count=100,worker_charged=300);ready=dict(job_id=jobid,state=state,checkpoint_sha256=sha(raw(state)))
atomic(td/'CHECKPOINT_READY_100.json',ready);token=dict(job_id=jobid,checkpoint_sha256=ready['checkpoint_sha256'],explicit_root_approval=True,max_completed_chunks=400)
atomic(td/'CONTINUE_AFTER_100.json',token);assert stage(td,jobid)==400
for key,bad in [('max_completed_chunks',2945),('job_id','OTHER'),('checkpoint_sha256','0'*64),('explicit_root_approval',False),('extra',True)]:
 changed=dict(token);changed[key]=bad;atomic(td/'CONTINUE_AFTER_100.json',changed);reject(lambda:stage(td,jobid))
atomic(td/'CONTINUE_AFTER_100.json',token)
state=dict(committed_count=400,worker_charged=1200);ready=dict(job_id=jobid,state=state,checkpoint_sha256=sha(raw(state)));atomic(td/'CHECKPOINT_READY_400.json',ready)
atomic(td/'CONTINUE_AFTER_400.json',dict(job_id=jobid,checkpoint_sha256=ready['checkpoint_sha256'],explicit_root_approval=True,max_completed_chunks=2945));assert stage(td,jobid)==2945
assert 95+min(100,2945-95)>100 and 100+100>100 and 2945+min(100,0)==2945
checks.append('exact_stage_fragment_100_400_2945_and_five_token_rejections')
# One actual bounded startup-fault execution. Inner is a no-physics stub only.
job=P/'startup_job';job.mkdir();o.JOB=job;o.BASE=P/'startup_stub'
atomic(job/'EXPECTED_M012.json',read(P.parent/'bilayer_full_m4_production_run/EXPECTED_M012.json'))
files=o.required_pins(job)|{str((P/'adapted_outer.py').resolve()),str(Path(__file__).resolve()),str((P/'test_launch.sh').resolve()),str((P/'startup_stub/production_supervisor.py').resolve())}
pins={f:sha(Path(f).read_bytes()) for f in sorted(files)};atomic(job/'PINNED_INPUTS.json',pins)
id=sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins)))
atomic(job/'PRODUCTION_AUTHORITY.json',dict(explicit_authorization=True,hard_cap=21600,deadline_utc='2026-10-14T00:00:00Z',session_chunk_limit=100,job_id=id,outer_reservation_id=0,review_only='NO_PHYSICAL_STARTUP_FAULT_STUB'))
b=ControlBudget(job/'CONTROL_SESSIONS.json');assert b.reserve(100,20)==0
try:o.run()
except AssertionError as e:assert str(e)=='session_failed_no_automatic_retry'
else:raise AssertionError('planned startup failure did not stop outer')
res=read(job/'OUTER_RESULT_0.json');lim=read(job/'STUB_LIMITS.json');ledger=read(job/'CONTROL_SESSIONS.json')
assert res['reason']=='outer_stopped' and res['sessions']==0 and ledger['reserved']==120 and len(ledger['sessions'])==1 and ledger['sessions'][0]['state']=='stopped'
assert lim['cpu']==[3,20] and lim['address_space']==[64*1024**2,128*1024**2] and lim['affinity']==[7] and not Path('/proc',str(lim['pid'])).exists()
assert not(job/'store').exists() and not(job/'FULL_MOMENTS.json').exists()
assert any(v['role']=='supervisor' and v['cpu']==[3,20] for v in res['post_exec_limit_observations'].values())
checks.append('one_pre_reservation_startup_failure_reaped_with120_charge_retained')
lock=open(job/'OUTER_LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock.close()
reject(o.run);assert read(job/'CONTROL_SESSIONS.json')['reserved']==120 and len(list(job.glob('OUTER_STARTED_*')))==1
checks.append('outer_lock_released_and_reservation_id_cannot_be_reused')
report=dict(status='PASS_BOUNDED_NO_PHYSICS_STARTUP_FAULT',checks=checks,source_manifest='010d82f4e4ef2cb9accec45641a84dc7ddc3eda6ce3957d0f683750af5d4f28c',production_job=binding['job_id'],test_job=id,source_adaptations=['CPU6→7','outer CPU99/100 and software98 lowered to20/22 and19 for review budget','dependency path made absolute','job path overridden toreview-only sandbox','inner exec path replaced by pinned exit7 stub'],no_physical_workers=True,result=res,limits=lim)
atomic(P/'STARTUP_CHECK.json',report);print('BOUNDED STARTUP/FAULT PASS')
