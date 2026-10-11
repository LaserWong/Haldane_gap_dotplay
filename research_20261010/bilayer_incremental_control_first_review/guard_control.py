import os,sys,json,time,math,signal,resource,ctypes
from pathlib import Path
p=Path(__file__).resolve().parent
name,cap,mem,*command=sys.argv[1:];cap=int(cap);mem=int(mem)
parent_cap=2;os.sched_setaffinity(0,{7})
ledger_path=p/'BUDGET_LEDGER.json'
ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'authorized_cpu_seconds':90,'charged_cpu_seconds':0,'cpu':7,'attempts':[]}
assert ledger['charged_cpu_seconds']+cap+parent_cap<=90
out=p/name;out.mkdir(exist_ok=False)
entry={'name':name,'cap_cpu_seconds':cap,'address_space_mib':mem,'charged_cpu_seconds':cap+parent_cap,'parent_reserved_cpu_seconds':parent_cap,'command':command,'state':'reserved'}
ledger['charged_cpu_seconds']+=cap+parent_cap;ledger['attempts'].append(entry)
def save():
 tmp=ledger_path.with_suffix('.tmp');tmp.write_text(json.dumps(ledger,indent=2)+'\n');os.replace(tmp,ledger_path)
save();assert ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)==0, 'subreaper required for orphan wait4';begin=time.monotonic();guard_owner=os.getpid();pid=os.fork()
if not pid:
 owner=guard_owner;assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
 if os.getppid()!=owner:os.kill(os.getpid(),signal.SIGKILL)
 os.setsid();os.sched_setaffinity(0,{7});resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));resource.setrlimit(resource.RLIMIT_AS,(mem*1024**2,mem*1024**2));f=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(f,1);os.dup2(f,2);os.close(f);os.execvp(command[0],command)
resource.setrlimit(resource.RLIMIT_CPU,(parent_cap,parent_cap))
entry['pid']=pid;entry['state']='running';save();ticks=os.sysconf('SC_CLK_TCK');why=None;max_tree_cpu=0;max_tree_rss=0;max_members=0;missing_since=None;seen={pid}
# Compiler children are allowed but aggregate all live descendant CPU; the process group is killed together.
def tree(root):
 rows={}
 for path in Path('/proc').iterdir():
  if not path.name.isdecimal():continue
  try:
   raw=(path/'stat').read_text();cols=raw[raw.rfind(')')+2:].split()
   rows[int(path.name)]=(int(cols[1]),int(cols[2]),(int(cols[11])+int(cols[12])+int(cols[13])+int(cols[14]))/ticks,int(cols[21])*os.sysconf('SC_PAGE_SIZE'))
  except FileNotFoundError:pass
 members={root}|{x for x,v in rows.items() if v[1]==root or v[0]==os.getpid()}
 while True:
  new=members|{x for x,v in rows.items() if v[0] in members}
  if new==members:break
  members=new
 return [(x,rows[x][2],rows[x][3]) for x in members if x in rows]
while True:
 got,status,use=os.wait4(pid,os.WNOHANG)
 if got:break
 try:
  rows=tree(pid)
 except BaseException as ex:
  rows=[];why='observer_failure_'+type(ex).__name__
 seen.update(x for x,_,_ in rows);max_members=max(max_members,len(rows));max_tree_rss=max(max_tree_rss,sum(r for _,_,r in rows));total=sum(v for _,v,_ in rows);max_tree_cpu=max(max_tree_cpu,total)
 if not rows:
  if missing_since is None:missing_since=time.monotonic()
  if time.monotonic()-missing_since>0.5:why='observer_missing_live_process'
 else:missing_since=None
 if total>=cap-1:why='aggregate_process_tree_CPU_guard'
 if sum(r for _,_,r in rows)>mem*1024**2:why='aggregate_process_tree_RSS_guard'
 # The controlled review driver deliberately spawns test descendants; aggregate guards still apply.
 if time.monotonic()-begin>max(30,2*cap+10):why='external_wall_guard'
 if why:
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  for child in seen:
   try:os.kill(child,signal.SIGKILL)
   except ProcessLookupError:pass
  got,status,use=os.wait4(pid,0);break
 time.sleep(.04)
orphans=[]
while True:
 try:
  child,childstatus,childuse=os.wait4(-1,os.WNOHANG)
 except ChildProcessError:break
 if not child:
  if time.monotonic()-begin>max(30,2*cap+10)+3:raise RuntimeError('orphan cleanup timeout')
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  for child in seen | {x for x,_,_ in tree(pid)}:
   try:os.kill(child,signal.SIGKILL)
   except ProcessLookupError:pass
  time.sleep(.02);continue
 orphans.append({'pid':child,'user':childuse.ru_utime,'system':childuse.ru_stime,'exit_status':os.waitstatus_to_exitcode(childstatus),'peak_rss_kib':childuse.ru_maxrss})
parent_use=resource.getrusage(resource.RUSAGE_SELF);parent_actual=parent_use.ru_utime+parent_use.ru_stime
assert parent_actual<=parent_cap
entry['parent_actual_cpu_seconds']=parent_actual
actual=use.ru_utime+use.ru_stime+sum(x['user']+x['system'] for x in orphans)
entry.update(state='completed' if os.waitstatus_to_exitcode(status)==0 else 'failed_or_stopped',exit_status=os.waitstatus_to_exitcode(status),wait4_user_seconds=use.ru_utime,wait4_system_seconds=use.ru_stime,wait4_cpu_seconds=actual,max_live_tree_cpu_seconds=max_tree_cpu,max_observed_processes=max_members,orphan_wait4=orphans,live_group_after_cleanup=tree(pid),wall_seconds=time.monotonic()-begin,peak_rss_kib=max([use.ru_maxrss]+[x['peak_rss_kib'] for x in orphans]),max_observed_tree_rss_bytes=max_tree_rss,stop_reason=why)
extra=max(0,math.ceil(actual)-cap);entry['charged_cpu_seconds']+=extra;ledger['charged_cpu_seconds']+=extra;save();(out/'resources.json').write_text(json.dumps(entry,indent=2)+'\n');print(json.dumps(entry,indent=2));assert ledger['charged_cpu_seconds']<=90
raise SystemExit(entry['exit_status']!=0)
