#!/usr/bin/env python3
"""Authorized separate 37-case replay with atomic exact records and hard budget."""
from pathlib import Path
import os,resource,hashlib,json,time,subprocess,sys,math
P=Path(__file__).resolve().parent;os.chdir(P);assert 1 in os.sched_getaffinity(0);os.sched_setaffinity(0,{1});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(60,2400))
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024**2),b''):h.update(b)
 return h.hexdigest()
inputs={name:digest(name) for name in ['inputs/fused/cells.txt','inputs/fused/INPUT_MANIFEST_SHA256.json','independent_contract.cpp','independent_contract','run_independent_n24.py']}
queries=[f'mix:{r}' for r in range(24)]+[f'jj:{r}' for r in range(13)];path=P/'independent_n24_checkpoint.json'
if path.exists():
 state=json.loads(path.read_text());assert state['input_sha256']==inputs
else:state={'n':24,'scope':'Independent pi-only two-vector Gram/H review; no other momentum optimization','input_sha256':inputs,'queries':queries,'exact':{},'completed':[],'attempts':[],'status':'not started','startup_allowance_CPU_seconds':1}
def save():
 temp=path.with_suffix('.tmp');temp.write_text(json.dumps(state,indent=2)+'\n');os.replace(temp,path)
def complete(token):
 kind,r=token.split(':');return all(f'{x}_{kind}_24_{r}' in state['exact'] for x in ['C','K'])
pending=[t for t in queries if not complete(t)]
assert all('child_CPU_seconds' in a and 'driver_CPU_seconds' in a for a in state['attempts']), 'Unknown previous CPU accounting; report before any resume.'
spent=state.get('startup_allowance_CPU_seconds',0)+sum(a['child_CPU_seconds']+a['driver_CPU_seconds'] for a in state['attempts'])
if not pending:
 state['status']='complete';save();print('Already complete.');sys.exit(0)
# Reserve ten CPU seconds for driver parsing, checkpoint writes, and cleanup.
remaining=math.floor(2400-spent-time.process_time()-10);assert remaining>0
attempt={'started_UTC':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pending_queries':pending,'child_hard_CPU_cap_seconds':remaining};state['attempts'].append(attempt);state['status']='running';save();start_driver=0;before=resource.getrusage(resource.RUSAGE_CHILDREN);beforeCPU=before.ru_utime+before.ru_stime
with (P/f'independent_n24_attempt_{len(state["attempts"])}.log').open('w') as err:
 child=subprocess.Popen(['./independent_contract','inputs/fused/cells.txt','24',*pending],stdout=subprocess.PIPE,stderr=err,text=True,bufsize=1,preexec_fn=lambda:resource.setrlimit(resource.RLIMIT_CPU,(remaining,remaining)))
 try:
  for line in child.stdout:
   key,value=line.strip().split('=');value=str(int(value));assert key not in state['exact'] or state['exact'][key]==value
   state['exact'][key]=value
   newly=[q for q in pending if complete(q) and q not in state['completed']]
   state['completed'].extend(newly);save()
   if newly:print('Saved',','.join(newly),len(state['completed']),'of37',flush=True)
  code=child.wait()
 except BaseException:
  if child.poll() is None:child.terminate()
  code=child.wait();attempt['interruption']='Driver interrupted; exact records retained.'
usage=resource.getrusage(resource.RUSAGE_CHILDREN);attempt.update({'exit_code':code,'child_CPU_seconds':usage.ru_utime+usage.ru_stime-beforeCPU,'driver_CPU_seconds':time.process_time()-start_driver,'peak_child_KiB':usage.ru_maxrss})
state['status']='complete' if code==0 and all(complete(q) for q in queries) else 'interrupted; exact partial records retained'
state['total_recorded_CPU_seconds']=state.get('startup_allowance_CPU_seconds',0)+sum(a['child_CPU_seconds']+a['driver_CPU_seconds'] for a in state['attempts']);save()
if state['status']=='complete':
 keys=[f'{x}_{family}_24_{r}' for family,count in [('mix',24),('jj',13)] for r in range(count) for x in ['C','K']]
 (P/'independent_n24.out').write_text(''.join(f'{k}={state["exact"][k]}\n' for k in keys))
print(state['status'],'totalCPU',state['total_recorded_CPU_seconds'],'peakKiB',usage.ru_maxrss,flush=True)
sys.exit(0 if state['status']=='complete' else 1)
