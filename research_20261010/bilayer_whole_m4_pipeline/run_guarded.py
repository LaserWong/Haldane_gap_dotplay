import os,sys,time,json,resource,signal,math,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
name,cap,mode,kind,*extra=sys.argv[1:];cap=int(cap)
ledger_path=p/'BUDGET_LEDGER.json';ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'authorized_cpu_seconds':300,'charged_cpu_seconds':0,'attempts':[]}
assert ledger['charged_cpu_seconds']+cap<=270, 'Aggregate soft admission stop at 270 CPU seconds'
out=p/'runs'/name;out.mkdir(parents=True,exist_ok=False)
def save():
 tmp=ledger_path.with_suffix('.tmp');tmp.write_text(json.dumps(ledger,indent=2)+'\n');os.replace(tmp,ledger_path)
entry={'name':name,'reserved_cpu_seconds':cap,'charged_cpu_seconds':cap,'state':'reserved_before_launch','mode':mode,'kind':kind,'args':extra,'source_sha256':hashlib.sha256((p/'whole.cpp').read_bytes()).hexdigest(),'executable_sha256':hashlib.sha256((p/'whole').read_bytes()).hexdigest()};ledger['charged_cpu_seconds']+=cap;ledger['attempts'].append(entry);save()
args=[str(p/'whole'),mode,kind,str(out),str(p),str(p.parent/'bilayer_brauer_rule_compiler/run'),str(cap),*extra]
start=time.monotonic();pid=os.fork()
if pid==0:
 try:
  os.setsid();os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));log=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(log,1);os.dup2(log,2);os.close(log);os.execv(args[0],args)
 except BaseException:
  os._exit(127)
entry['pid']=pid;entry['state']='running';save();ticks=os.sysconf('SC_CLK_TCK');kill_reason=None;lastcpu=0
while True:
 waited,status,usage=os.wait4(pid,os.WNOHANG)
 if waited:break
 try:
  text=Path(f'/proc/{pid}/stat').read_text();parts=text[text.rfind(')')+2:].split();lastcpu=(int(parts[11])+int(parts[12]))/ticks
  children=Path(f'/proc/{pid}/task/{pid}/children').read_text().strip()
  if children:kill_reason='unexpected_descendant_process'
 except FileNotFoundError:pass
 if lastcpu>=cap-1:kill_reason='external_cpu_guard'
 if time.monotonic()-start>max(30,cap*2+10):kill_reason='external_wall_guard'
 if kill_reason:
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  waited,status,usage=os.wait4(pid,0);break
 time.sleep(.05)
actual=usage.ru_utime+usage.ru_stime;entry.update(state='complete' if os.waitstatus_to_exitcode(status)==0 else 'failed_or_stopped',exit_status=os.waitstatus_to_exitcode(status),wait4_user_seconds=usage.ru_utime,wait4_system_seconds=usage.ru_stime,wait4_cpu_seconds=actual,wall_seconds=time.monotonic()-start,peak_rss_kib=usage.ru_maxrss,last_external_cpu_seconds=lastcpu,stop_reason=kill_reason)
extra_charge=max(0,math.ceil(actual)-cap);entry['charged_cpu_seconds']+=extra_charge;ledger['charged_cpu_seconds']+=extra_charge;save();(out/'wait4_resources.json').write_text(json.dumps(entry,indent=2)+'\n');print(json.dumps(entry,indent=2));assert ledger['charged_cpu_seconds']<=300
raise SystemExit(0 if entry['state']=='complete' else 2)
