"""Source-only production outer guard. Requires separate, absent launch authority.
OS affinity/rlimits and the no-refund120-second control reservation must exist
before this interpreter is exec'd. Never use the bare inner launcher.
"""
import os,sys,time,signal,resource,ctypes,fcntl,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;BASE=P;JOB=P.parent/'bilayer_full_m4_production_run_streaming'
sys.path.insert(0,str(BASE))
from engine import read,atomic,sha,raw,ControlBudget,file_sha256,verify_pins
from physical_session import required_pins,DEADLINE
from session_supervisor import snapshot

def terminal_valid(job):
 if not (JOB/'FULL_MOMENTS.json').exists():return False
 v=read(JOB/'FULL_MOMENTS.json');state=read(JOB/'store/state.json');controls=read(JOB/'EXPECTED_M012.json')
 assert v['job']==job and v['schema']=='bilayer-moment24-v1' and v['complete'] is True and v['accepted_m012'] is True,'terminal_marker_identity'
 assert state['job']==job and state['kind']=='PHYSICAL-FIXED-WITNESS24' and state['committed_count']==2945,'terminal_store_coverage'
 assert v['pencil_at_11_over_100']['G_numerators']==[controls[k] for k in ['m0','m1','m2']],'terminal_m012'
 return True

def run():
 assert os.sched_getaffinity(0)=={6}
 assert resource.getrlimit(resource.RLIMIT_CPU)==(99,100)
 assert resource.getrlimit(resource.RLIMIT_AS)==(64*1024**2,128*1024**2)
 lock=open(JOB/'OUTER_LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 a=read(JOB/'PRODUCTION_AUTHORITY.json');assert a['explicit_authorization'] is True and a['hard_cap']==21600 and a['deadline_utc']=='2026-10-14T00:00:00Z' and a['session_chunk_limit']==100
 pins=read(JOB/'PINNED_INPUTS.json');assert required_pins(JOB)|{str(Path(__file__).resolve())}<=set(pins)
 verify_pins(pins)
 job=sha(raw(dict(kind='PHYSICAL-FIXED-WITNESS24',schema='bilayer-moment24-v1',identity=pins)));assert a['job_id']==job
 budget=ControlBudget(JOB/'CONTROL_SESSIONS.json');rid=a['outer_reservation_id'];r=budget.state['sessions'][rid]
 predecessor=read(JOB/'PREDECESSOR.json');carry=read(JOB/'CONTROL_SESSIONS_CARRY_FORWARD.json')
 assert predecessor['job_id']=='db32cbc51cf71726756f7910921ef26b684e6c3020a8e8f0a0e5eecd17d24556' and predecessor['charged_control']==220
 assert carry['reserved']==220 and budget.state['sessions'][:2]==carry['sessions'] and rid>=2
 assert str((JOB/'PREDECESSOR.json').resolve()) in pins and str((JOB/'CONTROL_SESSIONS_CARRY_FORWARD.json').resolve()) in pins
 assert int(os.environ['BILAYER_OUTER_RESERVATION_ID'])==rid
 wid=a['watchdog_reservation_id'];assert int(os.environ['BILAYER_WATCHDOG_RESERVATION_ID'])==wid and wid!=rid
 wr=budget.state['sessions'][wid];assert wr['charged']==100 and wr['role']=='external_watchdog' and wr['watchdog_cpu_cap']==100 and wr['state']=='reserved'
 watchdog=os.getppid();assert Path('/proc/%d/exe'%watchdog).resolve()==Path('/usr/bin/timeout')
 watchdog_cmd=Path('/proc/%d/cmdline'%watchdog).read_bytes().split(b'\0')
 assert all(x in watchdog_cmd for x in [b'--signal=TERM',b'--kill-after=5s',b'28800s'])
 watchdog_lines=Path('/proc/%d/limits'%watchdog).read_text().splitlines()
 watchdog_cpu=tuple(map(int,next(x for x in watchdog_lines if x.startswith('Max cpu time')).split()[-3:-1]))
 watchdog_as=tuple(map(int,next(x for x in watchdog_lines if x.startswith('Max address space')).split()[-3:-1]))
 assert watchdog_cpu==(100,100) and watchdog_as==(64*1024**2,128*1024**2)
 assert str(Path('/usr/bin/timeout')) in pins

 assert r['charged']==120 and r['controller_cap']==100 and r['supervisor_cap']==20 and r['state']=='reserved'
 marker=JOB/('OUTER_STARTED_%d.json'%rid);assert not marker.exists(),'outer_reservation_is_single_use'
 atomic(marker,dict(job=job,pid=os.getpid(),reservation_id=rid,start=time.time(),source_sha256=file_sha256(Path(__file__))))
 libc=ctypes.CDLL(None);assert libc.prctl(36,1,0,0,0)==0
 ownpid=os.getpid();active=None;seen=set();tree_cpu=0.;peak=0;session_count=0;limit_observations={watchdog:dict(role='external_watchdog',cpu=watchdog_cpu,address_space=watchdog_as)};watchdog_cpu_peak=0.;start=time.monotonic();reason=None
 def kill_known():
  if active is not None:
   try:os.killpg(active,signal.SIGKILL)
   except ProcessLookupError:pass
  for p in seen:
   try:os.kill(p,signal.SIGKILL)
   except ProcessLookupError:pass
 def signal_stop(signum,frame):
  kill_known();raise RuntimeError('outer_signal_stop')
 signal.signal(signal.SIGXCPU,signal_stop);signal.signal(signal.SIGTERM,signal_stop);signal.signal(signal.SIGINT,signal_stop)
 try:
  while not terminal_valid(job):
   # Reconstruct a bounded chain; a token for one cap cannot authorize more.
   cap=100
   while (JOB/('CONTINUE_AFTER_%d.json'%cap)).exists():
    ready=read(JOB/('CHECKPOINT_READY_%d.json'%cap));token=read(JOB/('CONTINUE_AFTER_%d.json'%cap))
    assert ready['job_id']==job and ready['checkpoint_sha256']==sha(raw(ready['state']))
    assert ready['state']['committed_count']<=cap
    assert set(token)=={'job_id','checkpoint_sha256','explicit_root_approval','max_completed_chunks'}
    assert token['job_id']==job and token['checkpoint_sha256']==ready['checkpoint_sha256'] and token['explicit_root_approval'] is True
    nxt=token['max_completed_chunks'];assert type(nxt) is int and nxt=={100:400,400:2945}.get(cap),'unauthorized_stage_promotion'
    cap=nxt
   statepath=JOB/'store/state.json';state=read(statepath) if statepath.exists() else dict(committed_count=0)
   count=state['committed_count'];assert type(count) is int and 0<=count<=cap
   if count+min(100,2945-count)>cap:
    ready_path=JOB/('CHECKPOINT_READY_%d.json'%cap);checkpoint=sha(raw(state));ready=dict(job_id=job,checkpoint_sha256=checkpoint,state=state,authorized_cap=cap,requires_root_continuation=True)
    if ready_path.exists():assert read(ready_path)==ready
    else:atomic(ready_path,ready)
    # If an inner session stopped gracefully early, pause before a new100
    # could cross the cap. Never round permission upward.
    while not (JOB/('CONTINUE_AFTER_%d.json'%cap)).exists():
     if time.time()>=DEADLINE-86400:raise RuntimeError('review_reserve_deadline_while_waiting')
     if time.process_time()>=98:raise RuntimeError('outer_cpu_before_continue')
     time.sleep(1)
    continue
   # Fresh startup admission every session; includes fixed24h review reserve.
   ctrl=ControlBudget(JOB/'CONTROL_SESSIONS.json');assert ctrl.state['reserved']+23<=1200
   # Conservative full original plan upper bound; inner dispatcher also
   # checks the exact remaining plan before every worker. Never zero forecast.
   full_plan_wall=2*(16800+3600)+10*(2945+1200)+1200+60*53+86400
   if time.time()+full_plan_wall>=DEADLINE:raise RuntimeError('full_plan_plus_review_wall_admission')
   if time.process_time()>=98:raise RuntimeError('outer_self_cpu_admission')
   pid=os.fork()
   if pid==0:
    assert libc.prctl(1,signal.SIGKILL,0,0,0)==0
    if os.getppid()!=ownpid:os.kill(os.getpid(),signal.SIGKILL)
    os.setsid();resource.setrlimit(resource.RLIMIT_CPU,(3,20));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2))
    os.execv(sys.executable,[sys.executable,str(BASE/'production_supervisor.py'),str(JOB)])
   active=pid;seen={pid};ss=time.monotonic()
   while True:
    w,st,u=os.wait4(pid,os.WNOHANG)
    if w:tree_cpu+=u.ru_utime+u.ru_stime;active=None;break
    try:
     rows=snapshot();assert pid in rows and ownpid in rows and watchdog in rows
     members={pid}
     while True:
      more=members|{p for p,v in rows.items() if v['ppid'] in members or v['pgrp']==pid}
      if more==members:break
      members=more
     seen|=members;assert len(members)<=3,'unexpected_outer_descendant'
     for child in members:
      if child in limit_observations:continue
      try:
       cmd=Path('/proc/%d/cmdline'%child).read_bytes().replace(b'\0',b' ').decode()
       if 'production_supervisor.py' in cmd:role='supervisor';cpus={(3,20),(3,3)};spaces={(64*1024**2,128*1024**2)}
       elif 'physical_session.py' in cmd:role='controller';cpus={(20,20)};spaces={(64*1024**2,128*1024**2)}
       elif 'bilayer_variable_g_control_gate/whole ' in cmd:role='native';cpus={(3,3),(6,6)};spaces={(128*1024**2,128*1024**2)}
       else:continue # Fork-to-exec transition; source sets limits before exec.
       lines=Path('/proc/%d/limits'%child).read_text().splitlines()
       cpu=tuple(map(int,next(x for x in lines if x.startswith('Max cpu time')).split()[-3:-1]))
       space=tuple(map(int,next(x for x in lines if x.startswith('Max address space')).split()[-3:-1]))
       status=Path('/proc/%d/status'%child).read_text();aff=next(x.split(':',1)[1].strip() for x in status.splitlines() if x.startswith('Cpus_allowed_list:'))
       assert cpu in cpus and space in spaces and aff=='6','post_exec_limit_mismatch'
       limit_observations[child]=dict(role=role,cpu=cpu,address_space=space,affinity=aff)
      except FileNotFoundError:pass # Exited between snapshot and fixed-PID read.

     watchdog_cpu_peak=max(watchdog_cpu_peak,rows[watchdog]['cpu']);assert watchdog_cpu_peak<=100
     rss=rows[watchdog]['rss']+rows[ownpid]['rss']+sum(rows[p]['rss'] for p in members if p in rows);peak=max(peak,rss)
     assert rss<=256*1024**2,'whole_tree_rss'
     assert time.process_time()<98,'outer_self_cpu'
     assert watchdog_cpu_peak+tree_cpu+sum(rows[p]['cpu'] for p in members if p in rows)+time.process_time()<21600,'whole_job_observed_cpu'
     assert time.monotonic()-ss<2280 and time.time()<DEADLINE-86400,'outer_wall_and_review_deadline'
    except BaseException:
     reason='outer_accounting_or_resource_failure';kill_known();w,st,u=os.wait4(pid,0);tree_cpu+=u.ru_utime+u.ru_stime;active=None;raise
    time.sleep(.05)
   assert os.waitstatus_to_exitcode(st)==0,'session_failed_no_automatic_retry'
   seen=set();session_count+=1;atomic(JOB/'OUTER_PROGRESS.json',dict(job_id=job,sessions=session_count,wait4_tree_cpu=tree_cpu,self_cpu=time.process_time(),combined_peak_rss_bytes=peak,wall=time.monotonic()-start))
 except BaseException:
  reason=reason or 'outer_stopped';raise
 finally:
  kill_known()
  # Fixed-known IDs/group cleanup plus subreaper; no new /proc scan.
  until=time.monotonic()+3
  while True:
   try:w,st,u=os.wait4(-1,os.WNOHANG)
   except ChildProcessError:break
   if w:tree_cpu+=u.ru_utime+u.ru_stime;continue
   kill_known();assert time.monotonic()<until,'outer_orphan_cleanup_timeout';time.sleep(.01)
  budget=ControlBudget(JOB/'CONTROL_SESSIONS.json');r=budget.state['sessions'][rid];r.update(state='complete' if reason is None else 'stopped',controller_cpu=time.process_time(),supervisor_cpu=None)
  atomic(budget.path,budget.state);atomic(JOB/('OUTER_RESULT_%d.json'%rid),dict(job_id=job,reason=reason,reserved=120,self_cpu=time.process_time(),wait4_tree_cpu=tree_cpu,combined_peak_rss_bytes=peak,sessions=session_count,wall=time.monotonic()-start,post_exec_limit_observations=limit_observations,watchdog_cpu_observed_peak=watchdog_cpu_peak,watchdog_reserved=100))
if __name__=='__main__':run()
