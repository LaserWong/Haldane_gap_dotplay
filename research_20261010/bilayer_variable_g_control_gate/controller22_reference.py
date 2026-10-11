import os,sys,time,json,hashlib,resource,signal,math,fcntl,ctypes,re,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent

def digest(b):return hashlib.sha256(b).hexdigest()
def atomic(path,obj):
 path=Path(path);raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode();fd,tmp=tempfile.mkstemp(prefix=path.name+'.tmp.',dir=path.parent)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path);fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
 return digest(raw)
def read(path):return json.loads(Path(path).read_text())
def identities():
 files=[P/'whole',P/'whole.cpp',P/'controller.py']+[P.parent/'bilayer_whole_m4_pipeline'/x for x in ['geometry_8x4.txt','witness57.txt']]+[P.parent/'bilayer_brauer_rule_compiler/run'/f'diagrams_{x}.bin' for x in ['N','F','L']]
 return {str(x):digest(x.read_bytes()) for x in files}
def scan():
 out={}
 for d in Path('/proc').iterdir():
  if not d.name.isdigit():continue
  try:s=(d/'stat').read_text()
  except FileNotFoundError:continue
  z=s[s.rfind(')')+2:].split();assert len(z)>21
  out[int(d.name)]={'ppid':int(z[1]),'pgrp':int(z[2]),'session':int(z[3]),'cpu':(int(z[11])+int(z[12])+int(z[13])+int(z[14]))/os.sysconf('SC_CLK_TCK'),'rss':int(z[21])*os.sysconf('SC_PAGE_SIZE'),'threads':int(z[17]),'start':z[19]}
 return out

def verify_inputs():
 assert identities()==read(P/'PINNED_INPUTS.json'),'pinned_input_mismatch'

def validate_budget(ledger):
 assert ledger['hard_cap']==120 and ledger['soft_stop']==90 and ledger['controller_reserved']==10
 assert ledger['charged']==10+sum(x['charged'] for x in ledger['attempts'])
 assert 0<=ledger['charged']<=120
 assert len({x['name'] for x in ledger['attempts']})==len(ledger['attempts'])
 assert all(isinstance(x['charged'],int) and x['charged']>=x['reserved']>0 for x in ledger['attempts'])

def run(name,cap,args,test=None):
 ct=time.process_time();verify_inputs()
 os.sched_setaffinity(0,{6});os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1');lock=open(P/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 ledger_path=P/'BUDGET_LEDGER.json'
 ledger=read(ledger_path) if ledger_path.exists() else {'hard_cap':120,'soft_stop':90,'charged':10,'controller_reserved':10,'attempts':[]}
 validate_budget(ledger);assert ledger['charged']+cap<=90
 out=P/'runs'/name;out.mkdir(parents=True,exist_ok=False);ident=identities()
 rec={'name':name,'reserved':cap,'charged':cap,'state':'reserved','args':args,'identity':ident,'test':test};ledger['charged']+=cap;ledger['attempts'].append(rec);atomic(ledger_path,ledger)
 # Become a subreaper so deliberately orphaned descendants can be reaped.
 libc=ctypes.CDLL(None,use_errno=True);assert libc.prctl(36,1,0,0,0)==0
 t=time.monotonic();pid=os.fork()
 if pid==0:
  os.setsid();os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap));fd=os.open(out/'run.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(fd,1);os.dup2(fd,2);os.close(fd)
  if test=='descendant':
   os.fork()
   while True:time.sleep(.05)
  if test=='cpu':
   while True:pass
  if test in ('interrupt','observer'):
   time.sleep(10);os._exit(0)
  cmd=[str(P/'whole'),*args[:2],str(out),str(P.parent/'bilayer_whole_m4_pipeline'),str(P.parent/'bilayer_brauer_rule_compiler/run'),str(cap),*args[2:]]
  os.execv(cmd[0],cmd)
 rec['pid']=pid;rec['state']='running';atomic(ledger_path,ledger);seen={pid};reason=None;peakcpu=0;reaped=[]
 while True:
  w,status,u=os.wait4(pid,os.WNOHANG)
  if w:reaped.append((w,status,u));break
  try:
   if test=='observer':raise RuntimeError('injected_observer_failure')
   stats=scan()
   # A live mandatory child lacking stat is a failed observation, never ignored.
   if pid not in stats:raise RuntimeError('mandatory_child_stat_missing')
   members={pid}|{p for p,z in stats.items() if z['pgrp']==pid or z['session']==pid}
   changed=True
   while changed:
    nxt=members|{p for p,z in stats.items() if z['ppid'] in members};changed=nxt!=members;members=nxt
   seen|=members;peakcpu=max(peakcpu,sum(stats[p]['cpu'] for p in seen if p in stats))
   if members-{pid}:reason='unexpected_descendant'
   if any(stats[p]['threads']!=1 for p in members if p in stats):reason='unexpected_threads'
   if sum(stats[p]['rss'] for p in members if p in stats)>256*1024**2:reason='aggregate_RSS_guard'
   if peakcpu>=cap-.5:reason='external_cpu_guard'
  except Exception as e:reason='accounting_failure:'+str(e)
  if time.monotonic()-t>max(10,2*cap):reason='external_wall_guard'
  if test=='interrupt' and time.monotonic()-t>.1:reason='injected_interrupt'
  if test=='numeric_interrupt' and (out/'targets.jsonl').exists() and (out/'targets.jsonl').stat().st_size>0:reason='injected_mid_chunk'
  if reason:
   try:os.killpg(pid,signal.SIGKILL)
   except ProcessLookupError:pass
   for child in seen:
    try:os.kill(child,signal.SIGKILL)
    except ProcessLookupError:pass
   w,status,u=os.wait4(pid,0);reaped.append((w,status,u));break
  time.sleep(.01)
 # Drain subreaped descendants, with a bounded deadline and no silent survivors.
 until=time.monotonic()+2
 while True:
  try:w,st,u=os.wait4(-1,os.WNOHANG)
  except ChildProcessError:break
  if w:reaped.append((w,st,u));continue
  
  try:os.killpg(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  for child,z in scan().items():
   if z['ppid']==os.getpid():
    seen.add(child)
    try:os.kill(child,signal.SIGKILL)
    except ProcessLookupError:pass
  assert time.monotonic()<until,'unreaped_descendant';time.sleep(.01)
 final=scan();assert not any(p in final for p in seen),'surviving_process'
 actual=sum(u.ru_utime+u.ru_stime for _,_,u in reaped);controller=time.process_time()-ct
 rec.update(state='complete' if os.waitstatus_to_exitcode(status)==0 else 'stopped',reason=reason,exit=os.waitstatus_to_exitcode(status),seen=sorted(seen),reaped=[w for w,_,_ in reaped],wait4_cpu=actual,wait4_user=sum(u.ru_utime for _,_,u in reaped),wait4_system=sum(u.ru_stime for _,_,u in reaped),wall=time.monotonic()-t,controller_cpu=controller,peak_rss_kib=max(u.ru_maxrss for _,_,u in reaped),external_cpu_peak=peakcpu)
 if actual>cap:ledger['charged']+=math.ceil(actual-cap);rec['charged']+=math.ceil(actual-cap)
 rec['output_sha256']={f.name:digest(f.read_bytes()) for f in out.iterdir() if f.is_file()}
 atomic(ledger_path,ledger);atomic(out/'receipt.json',rec);print(json.dumps(rec))
 if test:assert reason=={'descendant':'unexpected_descendant','cpu':'external_cpu_guard','interrupt':'injected_interrupt','numeric_interrupt':'injected_mid_chunk','observer':'accounting_failure:injected_observer_failure'}[test];return out
 assert rec['state']=='complete','Failed attempt remains charged; no automatic retry'
 return out

def validate_payload(v,job):
 assert set(v)=={'job','sector','begin','end','N','values'} and v['job']==job
 assert v['sector'] in (0,2,4,6) and 0<=v['begin']<v['end']<=v['N']
 assert len(v['values'])==22
 assert all(isinstance(x,str) and re.fullmatch(r'-?(0|[1-9][0-9]*)',x) for x in v['values'])
 return v

def commit(directory,payload,job,inject=None):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);validate_payload(payload,job)
 name=f"q{payload['sector']}_{payload['begin']}_{payload['end']}.json";dest=directory/name
 journal=directory/'PREPARED.json';prepared=read(journal) if journal.exists() else {}
 raw=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode();sha=digest(raw)
 if name in prepared:assert prepared[name]==sha,'conflicting_duplicate'
 else:prepared[name]=sha;atomic(journal,prepared)
 if dest.exists():assert digest(dest.read_bytes())==sha and read(dest)==payload;return 'identical_duplicate'
 if inject=='before_write':return 'injected'
 if inject=='partial_write':(directory/(name+'.partial')).write_text('{');return 'injected'
 atomic(dest,payload)
 if inject=='after_rename':return 'injected'
 return 'committed'

def finalize(directory,job,expected):
 intervals={q:[] for q in expected};sums={q:[0]*22 for q in expected};prepared=read(Path(directory)/'PREPARED.json')
 for path in sorted(Path(directory).glob('q*.json')):
  assert path.name in prepared and digest(path.read_bytes())==prepared[path.name],'checksum_mismatch'
  v=validate_payload(read(path),job);q=v['sector'];assert q in expected and v['N']==expected[q]
  intervals[q].append((v['begin'],v['end']))
  for i,a in enumerate(v['values']):sums[q][i]+=int(a)
 for q,N in expected.items():
  pos=0
  for a,b in sorted(intervals[q]):assert a==pos,'gap_or_overlap';pos=b
  assert pos==N,'incomplete_coverage'
 return sums
if __name__=='__main__':
 if sys.argv[1]=='test':run(sys.argv[2],int(sys.argv[3]),sys.argv[5:],sys.argv[4])
 else:run(sys.argv[1],int(sys.argv[2]),sys.argv[3:])
