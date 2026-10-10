#!/usr/bin/env python3
"""One authorized pi-only contraction campaign with exact resumable records.

The displacement data are collected only to form the two-vector pi Gram/H.
No other momentum minimization is launched by this runner.
"""
import os,resource,subprocess,json,hashlib,time,sys
from pathlib import Path
P=Path(__file__).resolve().parent;os.chdir(P)
os.sched_setaffinity(0,{2} if 2 in os.sched_getaffinity(0) else {max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(2400,2400))
inputs={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['cells.txt','contract_current_cached.cpp','contract_current_cached']}
tokens=[f'mix:{r}' for r in range(24)]+[f'jj:{r}' for r in range(13)]
path=P/'n24_checkpoint.json'
if path.exists():
    state=json.loads(path.read_text());assert state['input_sha256']==inputs,'Inputs changed; do not reuse this checkpoint.'
else:
    state={'status':'not started','n':24,'momentum_target':'pi only','input_sha256':inputs,'tokens':tokens,'exact':{},'completed':[],'attempts':[]}
def save():
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(state,indent=2)+'\n');os.replace(temp,path)
def complete(token):
    kind,r=token.split(':');return all(f'{x}_{kind}_24_{r}' in state['exact'] for x in ['C','K'])
pending=[t for t in tokens if not complete(t)]
def publish():
    keys=[f'{kind}_{family}_24_{r}' for family,count in [('mix',24),('jj',13)] for r in range(count) for kind in ['C','K']]
    (P/'n24_exact.out').write_text(''.join(f'{k}={state["exact"][k]}\n' for k in keys))
if not pending:
    state['status']='complete';save();publish();print('All37 correlation records are already complete.');sys.exit(0)
assert all('CPU_seconds' in a for a in state['attempts']), 'Prior attempt has unknown CPU use. Preserve checkpoint and obtain a measured recovery plan before resuming.'
previous_cpu=sum(a.get('CPU_seconds',0) for a in state['attempts'])
assert previous_cpu<2400,'Campaign budget reached; further work needs a new measured plan.'
attempt={'started_UTC':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pending_tokens':pending,'CPU_before_children':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime}
state['attempts'].append(attempt);state['status']='running';save()
index=len(state['attempts']);errpath=P/f'n24_run_{index}.log'
with errpath.open('w') as log:
    remaining=max(1,int(2400-previous_cpu))
    process=subprocess.Popen(['./contract_current_cached','cells.txt','24',*pending],stdout=subprocess.PIPE,stderr=log,text=True,bufsize=1,preexec_fn=lambda:resource.setrlimit(resource.RLIMIT_CPU,(remaining,remaining)))
    assert process.stdout is not None
    for line in process.stdout:
        key,value=line.strip().split('=');value=str(int(value))
        assert key not in state['exact'] or state['exact'][key]==value
        state['exact'][key]=value
        newly=[t for t in pending if complete(t) and t not in state['completed']]
        if newly:
            state['completed'].extend(newly);save();print('Saved',','.join(newly),'completed',len(state['completed']),'of37',flush=True)
    code=process.wait()
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
attempt['CPU_seconds']=usage.ru_utime+usage.ru_stime-attempt.pop('CPU_before_children');attempt['exit_code']=code;attempt['peak_child_KiB']=usage.ru_maxrss
state['status']='complete' if code==0 and all(complete(t) for t in tokens) else 'interrupted; exact completed records preserved'
save()
if state['status']=='complete':
    publish()
print(state['status'],'CPU',attempt['CPU_seconds'],'peakKiB',attempt['peak_child_KiB'],flush=True)
sys.exit(code if code else (0 if state['status']=='complete' else 1))
