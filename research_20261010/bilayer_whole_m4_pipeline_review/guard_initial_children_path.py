import os,sys,json,time,math,signal,resource
from pathlib import Path
p=Path(__file__).resolve().parent
name,cap,mem,*command=sys.argv[1:];cap=int(cap);mem=int(mem)
ledger_path=p/'BUDGET_LEDGER.json'
ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'authorized_cpu_seconds':90,'charged_cpu_seconds':0,'cpu':7,'attempts':[]}
assert ledger['charged_cpu_seconds']+cap<=90
out=p/name;out.mkdir(exist_ok=False)
entry={'name':name,'cap_cpu_seconds':cap,'address_space_mib':mem,'charged_cpu_seconds':cap,'command':command,'state':'reserved'}
ledger['charged_cpu_seconds']+=cap;ledger['attempts'].append(entry)
def save():
 tmp=ledger_path.with_suffix('.tmp');tmp.write_text(json.dumps(ledger,indent=2)+'\n');os.replace(tmp,ledger_path)
save();begin=time.monotonic();pid=os.fork()
if not pid:
 os.setsid();os.sched_setaffinity(0,{7});resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));resource.setrlimit(resource.RLIMIT_AS,(mem*1024**2,mem*1024**2));f=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(f,1);os.dup2(f,2);os.close(f);os.execvp(command[0],command)
entry['pid']=pid;entry['state']='running';save();ticks=os.sysconf('SC_CLK_TCK');why=None;max_tree_cpu=0
# Compiler children are allowed but aggregate all live descendant CPU; the process group is killed together.
def tree(root):
 todo=[root];found=[]
 while todo:
  x=todo.pop()
  try:
   raw=Path(f'/proc/{x}/stat').read_text();cols=raw[raw.rfind(')')+2:].split();cpu=(int(cols[11])+int(cols[12])+int(cols[13])+int(cols[14]))/ticks
   rss=int(cols[21])*os.sysconf('SC_PAGE_SIZE')
   kids=[int(v) for v in Path(f'/proc/{x}/task/{x}/children').read_text().split()]
   found.append((x,cpu,rss));todo.extend(kids)
  except FileNotFoundError:pass
 return found
while True:
 got,status,use=os.wait4(pid,os.WNOHANG)
 if got:break
 rows=tree(pid);total=sum(v for _,v,_ in rows);max_tree_cpu=max(max_tree_cpu,total)
 if total>=cap-1:why='aggregate_process_tree_CPU_guard'
 if sum(r for _,_,r in rows)>mem*1024**2:why='aggregate_process_tree_RSS_guard'
 if mem==256 and len(rows)>1:why='unexpected_runtime_descendant'
 if time.monotonic()-begin>max(30,2*cap+10):why='external_wall_guard'
 if why:
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  got,status,use=os.wait4(pid,0);break
 time.sleep(.04)
actual=use.ru_utime+use.ru_stime
entry.update(state='completed' if os.waitstatus_to_exitcode(status)==0 else 'failed_or_stopped',exit_status=os.waitstatus_to_exitcode(status),wait4_user_seconds=use.ru_utime,wait4_system_seconds=use.ru_stime,wait4_cpu_seconds=actual,max_live_tree_cpu_seconds=max_tree_cpu,wall_seconds=time.monotonic()-begin,peak_rss_kib=use.ru_maxrss,stop_reason=why)
extra=max(0,math.ceil(actual)-cap);entry['charged_cpu_seconds']+=extra;ledger['charged_cpu_seconds']+=extra;save();(out/'resources.json').write_text(json.dumps(entry,indent=2)+'\n');print(json.dumps(entry,indent=2));assert ledger['charged_cpu_seconds']<=90
raise SystemExit(entry['exit_status']!=0)
