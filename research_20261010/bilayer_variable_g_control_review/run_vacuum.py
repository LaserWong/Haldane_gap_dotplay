import os,sys,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;S=P/'receipt_sandbox';sys.path.insert(0,str(S))
import physical_session as p
p.ROOT=P.parent/'bilayer_incremental_control_receipt_fix';p.KERNEL=P.parent/'bilayer_variable_g_control_gate'
import production_supervisor as ps
from engine import atomic,read,sha
job=P/'vacuum_fixture';job.mkdir()
auth=dict(explicit_authorization=True,hard_cap=21600,deadline_utc='2026-10-14T00:00:00Z',session_chunk_limit=100,review_scope='ONE_VACUUM_CHUNK_ONLY',permitted_worker_ranges=[dict(q=0,begin=0,end=1,N=1,cap=3)],no_resume=True)
atomic(job/'PRODUCTION_AUTHORITY.json',auth)
# Deliberately non-accepted controls: this bounded fixture must never finalize a full physical job.
atomic(job/'EXPECTED_M012.json',dict(schema='review-only-no-full-controls',scope='NOT_A_PHYSICAL_CERTIFICATE'))
atomic(job/'CONTROL_SESSIONS.json',dict(prepaid=1200,reserved=0,sessions=[]))
files=p.required_pins(job)|{str(f.resolve()) for f in S.glob('*.py')}|{str((P/'vacuum_entry.py').resolve()),str(Path(__file__).resolve()),str((job/'PRODUCTION_AUTHORITY.json').resolve())}
atomic(job/'PINNED_INPUTS.json',{f:sha(Path(f).read_bytes()) for f in sorted(files)})
actual_supervise=ps.supervise

def bounded_entry(command,*args,**kwargs):
 assert command[1]==str(S/'physical_session.py')
 command=list(command);command[1]=str(P/'vacuum_entry.py')
 return actual_supervise(command,*args,**kwargs)
ps.supervise=bounded_entry
ps.launch(job)
state=read(job/'store/state.json');assert state['committed_count']==1
assert len(list((job/'store/attempts').glob('*.json')))==len(list((job/'store/committed').glob('*.json')))==1
rec=read(job/'sessions/0/SESSION_SELF_CPU.json');assert rec['completed_this_session']==1 and rec['pending_chunks']==2944
assert read(job/'sessions/0/REVIEW_ALLOWLIST.json')['worker_calls']==1
assert not(job/'FULL_MOMENTS.json').exists()
atomic(job/'REVIEW_RESULT.json',dict(status='ONE_VACUUM_ACTUAL_DISPATCHER_PASS',committed_chunks=1,pending_chunks=2944,no_resume=True,no_full_controls=True,profile='CPU7;32/64/160MiB AS;256MiB combined RSS',source_overlay='bb79db2442c9f34cb9cdd877551fda639bb0328602a2b1a25884d0e19b1f6a8c'))
print('ONE VACUUM ACTUAL DISPATCHER PASS')
