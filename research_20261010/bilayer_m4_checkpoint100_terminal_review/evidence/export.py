import os,sys,resource,time,signal,fcntl,json,shutil,traceback
from pathlib import Path
BASE=Path('/workspace/shared/haldane_active/research_20261010')
PKG=Path(__file__).resolve().parent
JOB=BASE/'bilayer_full_m4_production_run_checksum'
sys.path.insert(0,str(BASE/'bilayer_stable_observer_checksum_fix'))
from engine import ControlBudget,atomic,read,raw,sha,file_sha256,plan
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_AS,(64<<20,64<<20));resource.setrlimit(resource.RLIMIT_CPU,(1,4))
t0=time.monotonic();cpu0=time.process_time()
lock=open(JOB/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert (JOB/'CONTINUE_AFTER_100.json').exists() and not (JOB/'CONTINUE_AFTER_400.json').exists()
assert (JOB/'OUTER_RESULT_5.json').exists()
outerlock=open(JOB/'OUTER_LOCK','a+');fcntl.flock(outerlock,fcntl.LOCK_EX|fcntl.LOCK_NB)
checkpoint=read(JOB/'CHECKPOINT_READY_100.json');assert checkpoint['state']==read(JOB/'store/state.json') and checkpoint['state']['committed_count']==100
budget=ControlBudget(JOB/'CONTROL_SESSIONS.json');assert budget.state['reserved']==711
idx=budget.reserve(4,1);assert idx==9
atomic(PKG/'RESERVATION.json',dict(id=idx,charged=5,control_reserved=716,scope='metadata export only; exclusive lifetime lock',checkpoint_sha256=checkpoint['checkpoint_sha256']))
pid=os.fork()
if pid==0:
 try:
  os.setsid();resource.setrlimit(resource.RLIMIT_CPU,(4,4))
  dest=PKG/'snapshot';dest.mkdir()
  for src in JOB.rglob('*'):
   if src.is_file() and src.name not in ('LOCK','OUTER_LOCK'):
    out=dest/src.relative_to(JOB);out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,out)
  commits=sorted((dest/'store/committed').glob('*.json'));attempts=sorted((dest/'store/attempts').glob('*.json'));assert len(commits)==len(attempts)==100
  sums={str(q):[0]*24 for q in (0,2,4,6)};coverage={str(q):0 for q in (0,2,4,6)};rows=plan()
  for i,(cf,af) in enumerate(zip(commits,attempts)):
   e=read(cf);v=e['payload'];a=read(af)
   assert a['state']=='complete' and a['id']==v['id']==i and v['range']==a['range']==rows[i]
   assert e['sha256']==sha(raw(v))==a['output_sha256'] and e['receipt_sha256']==sha(raw(a))
   assert len(v['values'])==24 and all(str(int(x))==x for x in v['values'])
   q=str(v['range']['q']);coverage[q]+=v['range']['end']-v['range']['begin']
   sums[q]=[x+int(y) for x,y in zip(sums[q],v['values'])]
  timings={str(q):0. for q in (0,2,4,6)}
  for d in (dest/'raw_outputs').iterdir():
   receipt=read(d/'receipt.json');i=int(d.name.split('_')[0]);v=read(commits[i])['payload'];assert file_sha256(d/'receipt.json')==v['worker_receipt_sha256']
   assert receipt['exit']==0 and receipt['reason'] is None
   for name,h in receipt['output_sha256'].items():assert file_sha256(d/name)==h
   timings[str(rows[i]['q'])]+=receipt['wait4_cpu']
  inner=read(dest/'sessions/7/RESOURCES.json');assert inner['exit']==0 and inner['reason'] is None
  atomic(PKG/'CHECKPOINT_REPORT.json',dict(job=checkpoint['job_id'],checkpoint=checkpoint,coverage=coverage,partial24_raw_by_sector={q:list(map(str,v)) for q,v in sums.items()},worker_wait4_by_sector=timings,inner_resources=inner,outer_progress=read(dest/'OUTER_PROGRESS.json'),outer_terminal=read(dest/'OUTER_RESULT_5.json'),observer_transition_records=len(list((dest/'LIMIT_EVENTS').glob('*.json'))),idle_evidence=['exclusive inherited lifetime LOCK acquired and held throughout export','all100 attempts complete','inner session exited and reaped','only previously authorized cap400 token; launcher terminal; exclusive OUTER_LOCK held'],pid_namespace_caveat='Live launch PID namespace is unavailable from separate exec; no empty process scan is claimed.',observer_caveat='Terminal cumulative verified PID map is now retained in OUTER_RESULT_5.json.',forecast=dict(standard_remaining=16500,retry_remaining=3008,control_reserved=716,remaining_inner_sessions=29,remaining_inner_reservations=667,planned_total_control_if_relaunch_authorized=1383,control_spare_before_new_launcher=217,total_reserved_now=1208,q6_sampled=0),partial_only=True))
  os._exit(0)
 except BaseException:
  (PKG/'CHILD_ERROR.txt').write_text(traceback.format_exc());os._exit(1)
resource.setrlimit(resource.RLIMIT_CPU,(1,1))
reason=None
while True:
 got,status,ru=os.wait4(pid,os.WNOHANG)
 if got:break
 if time.monotonic()-t0>20 or time.process_time()-cpu0>.75:
  reason='guard_wall_or_cpu';os.killpg(pid,signal.SIGKILL);got,status,ru=os.wait4(pid,0);break
 try:
  fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split();live=(int(fields[11])+int(fields[12]))/os.sysconf('SC_CLK_TCK')
  if live>3.8:reason='child_cpu';os.killpg(pid,signal.SIGKILL);got,status,ru=os.wait4(pid,0);break
 except FileNotFoundError:pass
 time.sleep(.025)
child=ru.ru_utime+ru.ru_stime;parent=time.process_time()-cpu0;code=os.waitstatus_to_exitcode(status)
budget.finish(idx,child,parent,'complete' if code==0 and reason is None else 'failed')
atomic(PKG/'RESOURCES.json',dict(child_cpu=child,guard_cpu_to_receipt=parent,child_exit=code,reason=reason,wall=time.monotonic()-t0,child_maxrss_kib=ru.ru_maxrss,charged=5,limits=dict(child_CPU=4,guard_CPU=1,child_AS=64<<20,guard_AS=64<<20,CPU=6),memory_bound='Export pair128MiB AS plus paused outer/watchdog128MiB AS <=256MiB; lifetime lock excludes other production roles. No cross-namespace RSS observation asserted.'))
if (PKG/'snapshot').exists():shutil.copyfile(JOB/'CONTROL_SESSIONS.json',PKG/'snapshot/CONTROL_SESSIONS.json')
assert code==0 and reason is None
assert read(JOB/'CHECKPOINT_READY_100.json')==checkpoint and read(JOB/'store/state.json')==checkpoint['state']
manifest={str(p.relative_to(PKG)):file_sha256(p) for p in sorted(PKG.rglob('*')) if p.is_file() and p.name!='MANIFEST_SHA256.json'}
atomic(PKG/'MANIFEST_SHA256.json',manifest)
print(json.dumps(dict(seal=file_sha256(PKG/'MANIFEST_SHA256.json'),files=len(manifest),checkpoint=checkpoint['checkpoint_sha256'],control=716,worker=492,charged=1208,child_cpu=child,guard_cpu=time.process_time()-cpu0)),flush=True)
