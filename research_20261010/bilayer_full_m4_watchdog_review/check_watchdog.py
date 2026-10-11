import os,sys,signal,time,json,hashlib,ctypes,importlib.util,copy
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent;BASE=R/'bilayer_control_memory_revision';sys.path.insert(0,str(BASE))
from engine import read,sha,raw,atomic,ControlBudget
pins=read(P/'PINNED_INPUTS.json');identity=read(P/'PROPOSED_JOB_ID.json');assert sha((P/'PINNED_INPUTS.json').read_bytes())==identity['pins_sha256']=='6f34d04b6336616afaaaaa29d476a1549f82aa24d1620a2b2d4a3bcd25845fb7'
assert all(sha(Path(f).read_bytes())==h for f,h in pins.items())
assert sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins)))==identity['job_id']=='db32cbc51cf71726756f7910921ef26b684e6c3020a8e8f0a0e5eecd17d24556'
assert sha((P/'EXPECTED_M012.json').read_bytes())=='f528834efae7b875b4dfa665ab991f4bfd7db73d54507ac681c8402e1a6f19ec'
launch=(P/'source/launch_watchdog.sh').read_text();assert '--cpu=100:100 --as=67108864:134217728' in launch and '--signal=TERM --kill-after=5s 28800s' in launch and '-ge 115205' in launch
assert 115205==28800+5+86400
# No producer file import writes; helper's globals are redirected only in this process.
spec=importlib.util.spec_from_file_location('review_terminal',R/'bilayer_full_m4_watchdog_gate/outer.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
m=P/'terminal_mock';m.mkdir();mod.JOB=m;job='REVIEW_TERMINAL_METADATA_ONLY';controls=read(P/'EXPECTED_M012.json');atomic(m/'EXPECTED_M012.json',controls)
state=dict(job=job,kind='PHYSICAL-FIXED-WITNESS24',committed_count=2945);value=dict(job=job,schema='bilayer-moment24-v1',complete=True,accepted_m012=True,pencil_at_11_over_100=dict(G_numerators=[controls[k] for k in ['m0','m1','m2']]))
assert mod.terminal_valid(job) is False
atomic(m/'store/state.json',state);atomic(m/'FULL_MOMENTS.json',value);assert mod.terminal_valid(job)
mutations=[]
for field,val in [('job','FOREIGN'),('schema','old22'),('complete',False),('accepted_m012',False)]:
 bad=copy.deepcopy(value);bad[field]=val;atomic(m/'FULL_MOMENTS.json',bad)
 try:mod.terminal_valid(job)
 except AssertionError:mutations.append(field)
 else:raise AssertionError('bad terminal marker survived')
atomic(m/'FULL_MOMENTS.json',value);bad=dict(state,committed_count=2944);atomic(m/'store/state.json',bad)
try:mod.terminal_valid(job)
except AssertionError:mutations.append('coverage')
else:raise AssertionError('incomplete terminal survived')
atomic(m/'store/state.json',state);bad=copy.deepcopy(value);bad['pencil_at_11_over_100']['G_numerators'][2]='0';atomic(m/'FULL_MOMENTS.json',bad)
try:mod.terminal_valid(job)
except AssertionError:mutations.append('m012')
else:raise AssertionError('wrong terminal controls survived')
# The legacy positive-two-field budget records the watchdog's100 total explicitly.
b=ControlBudget(P/'test_control_budget.json');a=b.reserve(100,20);w=b.reserve(99,1);b.state['sessions'][w].update(role='external_watchdog',watchdog_cpu_cap=100);atomic(b.path,b.state);b=ControlBudget(b.path);assert b.state['reserved']==220 and 220+30*23==910<=1200
# One real pinned GNU timeout fault, only duration and hard CPU cap are lowered.
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
start=time.monotonic();pid=os.fork()
if not pid:
 os.execv('/usr/bin/prlimit',['/usr/bin/prlimit','--cpu=3:3','--as=67108864:134217728','--','/usr/bin/timeout','--signal=TERM','--kill-after=5s','0.5s',sys.executable,str(P/'ignore_term.py'),str(P/'fault')])
wp,status,use=os.wait4(pid,0);orphans=[]
while True:
 try:x,st,u=os.wait4(-1,0)
 except ChildProcessError:break
 orphans.append(dict(pid=x,exit=os.waitstatus_to_exitcode(st),cpu=u.ru_utime+u.ru_stime))
limits=read(P/'fault/PID_LIMITS.json');assert (P/'fault/TERM_SEEN').exists()
assert os.waitstatus_to_exitcode(status)==-9 and any(x['pid']==limits['pid'] and x['exit']==-9 for x in orphans)
assert not Path('/proc',str(pid)).exists() and not Path('/proc',str(limits['pid'])).exists()
assert limits['cpu']==[3,3] and limits['address_space']==[64*1024**2,128*1024**2] and limits['affinity']==[7]
assert b.state['reserved']==220
report=dict(status='PASS_PINNED_WATCHDOG_AND_TERMINAL_DELTA',source_manifest='16d7500fe6a439cbc80813954e43f56eb043002d08a122f2ec7a613688931afc',production_job=identity['job_id'],production_watchdog_seconds=28800,test_watchdog_seconds=.5,kill_grace_seconds=5,term_seen=True,watchdog_exit=os.waitstatus_to_exitcode(status),watchdog_wait4_cpu=use.ru_utime+use.ru_stime,orphan_wait4=orphans,wall=time.monotonic()-start,terminal_mutations_rejected=mutations,control_nominal=910,control_hard_pool=1200,virtual_soft_total_mib=384,whole_five_process_RSS_cap_mib=256,no_physical_workers=True)
atomic(P/'CHECKS.json',report);print('WATCHDOG DELTA PASS')
