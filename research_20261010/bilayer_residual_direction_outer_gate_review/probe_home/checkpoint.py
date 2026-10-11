"""One explicitly requested bounded chunk per invocation; never starts a full pass."""
import argparse,ctypes,fcntl,hashlib,json,math,os,resource,signal,subprocess,sys,tempfile,time
from pathlib import Path
HOME=Path(__file__).resolve().parent
SCHEMA='residual-q6-sector-checkpoint-v1'
LIBC=ctypes.CDLL(None,use_errno=True)
LIBC.prctl.argtypes=[ctypes.c_int,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong]
LIBC.prctl.restype=ctypes.c_int
BIND=['checkpoint.py','chunk_kernel.cpp','base_kernel.inc','init_kernel.inc','chunk_kernel','outer_driver.cpp','outer_driver']
def limit_supervisor():
 # Two-process peak address allowance: supervisor32 + kernel68 =100MiB.
 soft,hard=resource.getrlimit(resource.RLIMIT_AS);newhard=min(hard,100*1024**2) if hard!=resource.RLIM_INFINITY else 100*1024**2
 resource.setrlimit(resource.RLIMIT_AS,(32*1024**2,newhard))
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while data:=f.read(16384):h.update(data)
 return h.hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def atomic(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');data=json.dumps(x,indent=2)+'\n'
 with tmp.open('w') as f:f.write(data);f.flush();os.fsync(f.fileno())
 os.replace(tmp,p)
 fd=os.open(p.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
def binding():return {**{s:digest(HOME/s) for s in BIND},'/usr/bin/python3':digest('/usr/bin/python3')}
def verify(state):
 assert state['schema']==SCHEMA
 assert state['binding']==binding(),'source/binary changed: start a separately authorized state'
 for key in ('geometry','coefficients'):assert digest(state[key]['path'])==state[key]['sha256'],key
 config={k:state[k] for k in ('schema','binding','geometry','coefficients','nx','ny','N','d','total','cpu_budget','memory_MiB','cpu_affinity')}
 assert hashlib.sha256(canonical(config)).hexdigest()==state['configuration_id']
 assert 0<=state['charged_cpu_seconds']<=state['cpu_budget']
 return config

def read_chunks(folder,state):
 by={'q4':[],'q6':[]}
 for a in state['attempts']:
  if a['status']!='complete':continue
  f=folder/a['output'];assert digest(f)==a['output_sha256'];c=json.loads(f.read_text())
  assert c['configuration_id']==state['configuration_id'];raw=c['raw'];phase=a['phase']
  assert raw['phase']==phase and raw['N']==state['N'] and raw['d']==state['d']
  assert raw['range_start']==a['start'] and raw['range_end']==a['end']
  assert raw['support_total']==state['total'][phase]
  assert raw['q4_processed']==(a['end']-a['start'] if phase=='q4' else 0)
  assert raw['q6_processed']==(a['end']-a['start'] if phase=='q6' else 0)
  assert raw['partial'] is True
  for k in ('G','H200','H200_squared'):assert len(raw[k])==4*state['d']+2
  by[phase].append((a['start'],a['end'],raw))
 for phase,chunks in by.items():
  chunks.sort();end=0
  for start,stop,_ in chunks:assert start==end and stop>start;end=stop
  assert end<=state['total'][phase]
 return by

def initialize(folder,geometry,coefficients,nx,ny,budget):
 assert budget>=2;assert not (folder/'state.json').exists(),'will not overwrite state'
 vals=Path(geometry).read_text().split();N,d=map(int,vals[:2]);assert N==nx*ny and N in (8,32)
 cv=Path(coefficients).read_text().split();assert len(cv)==2*d and all(abs(int(z))<=2**48 for z in cv)
 config=dict(schema=SCHEMA,binding=binding(),geometry=dict(path=str(Path(geometry).resolve()),sha256=digest(geometry)),coefficients=dict(path=str(Path(coefficients).resolve()),sha256=digest(coefficients)),nx=nx,ny=ny,N=N,d=d,total=dict(q4=math.comb(N-1,3),q6=math.comb(N-1,5)),cpu_budget=budget,memory_MiB=100,cpu_affinity=4)
 state={**config,'configuration_id':hashlib.sha256(canonical(config)).hexdigest(),'charged_cpu_seconds':1,'initialization_charge':1,'assembly_charge':0,'attempts':[]}
 atomic(folder/'state.json',state);return state

def arm_parent_death(parent_pid):
 if LIBC.prctl(1,signal.SIGKILL,0,0,0)!=0:raise OSError(ctypes.get_errno(),"PR_SET_PDEATHSIG failed")
 if os.getppid()!=parent_pid:os.kill(os.getpid(),signal.SIGKILL)

def run_chunk(folder,state,phase,count,cap,lock_fd=None):
 if lock_fd is None:
  with (folder/'lock').open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
   return run_chunk(folder,state,phase,count,cap,lock.fileno())
 verify(state);chunks=read_chunks(folder,state)[phase];start=chunks[-1][1] if chunks else 0
 assert isinstance(cap,int) and cap>=2 and count>0
 assert start<state['total'][phase],'phase already complete'
 count=min(count,state['total'][phase]-start)
 assert state['charged_cpu_seconds']+cap<=state['cpu_budget'],'budget exhausted; separate parent decision required'
 n=len(state['attempts']);attempt=dict(index=n,phase=phase,start=start,end=start+count,charged_cpu_seconds=cap,kernel_cpu_cap_seconds=cap-1,supervisor_cpu_cap_seconds=1,status='reserved',output=f'chunk_{n:04d}.json')
 # Charge the full hard cap before launch. Interrupted/failed attempts are never refunded.
 state['charged_cpu_seconds']+=cap;state['attempts'].append(attempt);atomic(folder/'state.json',state)
 inherited_fds=[lock_fd]
 if os.environ.get("RESIDUAL_OUTER_LOCK_FD"):
  outer_fd=int(os.environ["RESIDUAL_OUTER_LOCK_FD"]);actual=os.fstat(outer_fd);expected=(folder.parent/"outer.lock").stat();assert (actual.st_dev,actual.st_ino)==(expected.st_dev,expected.st_ino)
  inherited_fds.append(outer_fd)
 parent_pid=os.getpid()
 def limits():
  # Install before limits/exec; check parent identity to close the fork/prctl race.
  arm_parent_death(parent_pid)
  os.sched_setaffinity(0,{state['cpu_affinity']});resource.setrlimit(resource.RLIMIT_AS,(60*1024**2,60*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(cap-1,cap-1))
 before=resource.getrusage(resource.RUSAGE_CHILDREN);starttime=time.monotonic()
 cmd=[str(HOME/'chunk_kernel'),state['geometry']['path'],state['coefficients']['path'],str(state['nx']),str(state['ny']),phase,str(start),str(count),'raw_chunk']
 try:
  result=subprocess.run(cmd,preexec_fn=limits,pass_fds=tuple(inherited_fds),capture_output=True,text=True,timeout=2*cap+5)
  after=resource.getrusage(resource.RUSAGE_CHILDREN);attempt['observed_cpu_seconds']=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime;attempt['elapsed_seconds']=time.monotonic()-starttime
  attempt['returncode']=result.returncode;(folder/f'chunk_{n:04d}.log').write_text(result.stderr)
  assert result.returncode==0,'kernel failed'
  verify(state) # Reject inputs/source changed while the kernel was running.
  raw=json.loads(result.stdout);assert raw['range_start']==start and raw['range_end']==start+count and raw['phase']==phase
  record=dict(configuration_id=state['configuration_id'],raw=raw);output=folder/attempt['output'];assert not output.exists();atomic(output,record)
  attempt['output_sha256']=digest(output);attempt['status']='complete'
 except BaseException as e:
  attempt['status']='failed';attempt['error']=str(e);atomic(folder/'state.json',state);raise
 atomic(folder/'state.json',state);read_chunks(folder,state)
 return attempt

def assemble(folder,state):
 verify(state);by=read_chunks(folder,state);size=4*state['d']+2;normalized={};scalar={}
 for phase in ('q4','q6'):
  assert by[phase] and by[phase][-1][1]==state['total'][phase],f'{phase} incomplete'
 if state.get('complete_row_sha256'):
  assert digest(folder/'complete_row.json')==state['complete_row_sha256']
  return json.loads((folder/'complete_row.json').read_text())
 assert state['charged_cpu_seconds']+1<=state['cpu_budget'],'assembly CPU allowance exhausted'
 state['charged_cpu_seconds']+=1;state['assembly_charge']+=1;atomic(folder/'state.json',state)
 for phase,q in [('q4',4),('q6',6)]:
  chunks=by[phase];assert chunks and chunks[-1][1]==state['total'][phase],f'{phase} incomplete'
  normalized[phase]={}
  for k in ('G','H200','H200_squared'):
   raw=[sum(int(c[k][j]) for _,_,c in chunks) for j in range(size)];numerators=[v*state['N'] for v in raw];assert all(v%q==0 for v in numerators),(phase,k,'nonintegral normalization');normalized[phase][k]=[v//q for v in numerators]
  for k in ('T_norm','CT_norm','T_K_T'):
   v=sum(int(c[k]) for _,_,c in chunks)*state['N'];assert v%q==0;scalar[k]=scalar.get(k,0)+v//q
 rows={k:[normalized['q4'][k][j]+normalized['q6'][k][j] for j in range(size)] for k in ('G','H200','H200_squared')}
 qcols=[0]+[2]*state['d']+[4]*(2*state['d'])+[6]*(state['d']+1)
 G,H,J=[rows[k] for k in ('G','H200','H200_squared')]
 av=[h-1200*g for h,g in zip(H,G)];assert all(v%11==0 for v in av);A=[v//11 for v in av]
 av2=[j-1440000*g-2200*(6+q)*a for j,g,q,a in zip(J,G,qcols,A)];assert all(v%121==0 for v in av2);A2=[v//121 for v in av2]
 result=dict(status='COMPLETE_EXACT_NEW_ROW',configuration_id=state['configuration_id'],N=state['N'],d=state['d'],partial=False,sector_normalization={'q4':f"{state['N']}/4",'q6':f"{state['N']}/6"},rows={k:list(map(str,v)) for k,v in rows.items()},polynomial=dict(convention='H(g)=Q+g A/2; row coefficients G,A,A² with fixed q(T)=6',Q_row=list(map(str,[6*v for v in G])),A_row=list(map(str,A)),Q2_row=list(map(str,[36*v for v in G])),QA_AQ_row=list(map(str,[(6+q)*a for q,a in zip(qcols,A)])),A2_row=list(map(str,A2))),scalars={k:str(v) for k,v in scalar.items()})
 atomic(folder/'complete_row.json',result);state['complete_row_sha256']=digest(folder/'complete_row.json');atomic(folder/'state.json',state);return result

def main():
 assert Path(sys.executable).resolve()==Path('/usr/bin/python3').resolve(),'use pinned /usr/bin/python3'
 limit_supervisor()
 soft,hard=resource.getrlimit(resource.RLIMIT_CPU);resource.setrlimit(resource.RLIMIT_CPU,(1,hard))
 a=argparse.ArgumentParser();a.add_argument('action',choices=['init','chunk','assemble']);a.add_argument('folder',type=Path);a.add_argument('--geometry');a.add_argument('--coefficients');a.add_argument('--nx',type=int);a.add_argument('--ny',type=int);a.add_argument('--budget',type=int);a.add_argument('--phase',choices=['q4','q6']);a.add_argument('--count',type=int);a.add_argument('--cap',type=int);v=a.parse_args();v.folder.mkdir(parents=True,exist_ok=True)
 with (v.folder/'lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if v.action=='init':result=initialize(v.folder,v.geometry,v.coefficients,v.nx,v.ny,v.budget)
  else:
   state=json.loads((v.folder/'state.json').read_text());result=run_chunk(v.folder,state,v.phase,v.count,v.cap,lock.fileno()) if v.action=='chunk' else assemble(v.folder,state)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
