#!/usr/bin/env python3
"""Single-attempt, CPU5, whole-session watchdog and wait4 resource accounting."""
import ctypes, hashlib, json, os, resource, signal, sys, time
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
mode=sys.argv[1]; assert mode=='audit'
cpu=4
mem=(512 if mode=='compile64' else 256)*1024**2
wall=90
assert 5 in os.sched_getaffinity(0)
attempt=P/(mode+'.attempt'); fd=os.open(attempt,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.write(fd,b'Single authorized attempt; no automatic retry.\n');os.close(fd)
os.sched_setaffinity(0,{5})
resource.setrlimit(resource.RLIMIT_AS,(mem,mem))
libc=ctypes.CDLL(None,use_errno=True); assert libc.prctl(36,1,0,0,0)==0
if mode=='audit':
    fixture=ROOT/'research_20261010/uniform_alternating_b2_fixture'
    assert hashlib.sha256((fixture/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='0cad4bf9a9bd907cd9be78a6eceaf20ec041b45c3d398fd664c38bd49ee88696'
    for name,pin in json.loads((fixture/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((fixture/name).read_bytes()).hexdigest()==pin,name
    for name,pin in json.loads((fixture/'INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,name
    pilot=ROOT/'research_20261010/uniform_alternating_b2_64_pilot'
    assert hashlib.sha256((pilot/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='26d1977cf2324cd693c306aecd3b621989364e773413192253670c0951ca3570'
    for name,pin in json.loads((pilot/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((pilot/name).read_bytes()).hexdigest()==pin,name
    for name,pin in json.loads((pilot/'INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,name
    cmd=[sys.executable,str(P/'audit.py')]
else:cmd=['g++','-O2','-std=c++17',str(P/'independent64.cpp'),'-lgmpxx','-lgmp','-o',str(P/'independent64')]
out=os.open(P/(mode+'.out'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);err=os.open(P/(mode+'.log'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
assert time.process_time()<0.5, 'Launcher startup reserve exhausted; stop without numerical launch'
start=time.monotonic();parent=os.getpid();pid=os.fork()
if pid==0:
    try:
        os.setsid();os.dup2(out,1);os.dup2(err,2);os.close(out);os.close(err)
        resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu));resource.setrlimit(resource.RLIMIT_AS,(mem,mem))
        signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU})
        assert libc.prctl(1,signal.SIGKILL,0,0,0)==0 and os.getppid()==parent
        os.execvpe(cmd[0],cmd,dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'))
    except BaseException as e:os.write(2,(repr(e)+'\n').encode());os._exit(125)
os.close(out);os.close(err);parent_cap=1; resource.setrlimit(resource.RLIMIT_CPU,(parent_cap,parent_cap))
clk=os.sysconf('SC_CLK_TCK');seen={};reason=None;reaped=[];main_status=None
def members():
    result=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():continue
        try:
            raw=(p/'stat').read_text();fields=raw[raw.rfind(')')+2:].split()
            if int(fields[3])!=pid:continue # session, including compiler descendants
            result.append((int(p.name),sum(int(fields[i]) for i in (11,12,13,14))/clk))
        except (FileNotFoundError,ProcessLookupError):pass
    return result
def kill_tree():
    for p,_ in members():
        try:os.kill(p,signal.SIGKILL)
        except ProcessLookupError:pass
    try:os.killpg(pid,signal.SIGKILL)
    except ProcessLookupError:pass
try:
    while True:
        alive=members()
        for p,_ in alive:
            try:
                exe=os.readlink(f'/proc/{p}/exe')
                if (p,exe) in seen:continue
                if str(P/'audit.py').encode() not in Path(f'/proc/{p}/cmdline').read_bytes():continue
                status=Path(f'/proc/{p}/status').read_text();limits=Path(f'/proc/{p}/limits').read_text();fields=dict(line.split(':',1) for line in status.splitlines() if ':' in line)
                assert fields['Cpus_allowed_list'].strip()=='5'
                assert not (int(fields['SigBlk'].strip(),16)&(1<<(signal.SIGXCPU-1)))
                assert not (int(fields['SigIgn'].strip(),16)&(1<<(signal.SIGXCPU-1)))
                assert not (int(fields['SigCgt'].strip(),16)&(1<<(signal.SIGXCPU-1)))
                lim={line[:25].strip():line[25:].split() for line in limits.splitlines()[1:]}
                assert lim['Max cpu time'][:2]==[str(cpu)]*2 and lim['Max address space'][:2]==[str(mem)]*2
                seen[p,exe]={'pid':p,'executable':exe,'cpu_limits':[cpu,cpu],'AS_limits':[mem,mem],'affinity':[5],'SIGXCPU':'default_unblocked'}
            except (FileNotFoundError,ProcessLookupError):pass
        if sum(t for _,t in alive)>=cpu-0.15:reason='aggregate_CPU_watchdog';kill_tree()
        if time.monotonic()-start>=wall:reason='whole_tree_wall_watchdog';kill_tree()
        while True:
            try:got,status,usage=os.wait4(-1,os.WNOHANG)
            except ChildProcessError:got=0;break
            if not got:break
            if got==pid:main_status=status
            reaped.append({'pid':got,'exit_code':os.waitstatus_to_exitcode(status),'user_cpu':usage.ru_utime,'system_cpu':usage.ru_stime,'peak_rss_kib':usage.ru_maxrss})
        if main_status is not None:
            if members():reason=reason or 'unexpected_remaining_descendant';kill_tree()
            else:break
        time.sleep(.02)
except BaseException as e:
    reason='guard_failure: '+repr(e);kill_tree()
finally:
    kill_tree()
    while True:
        try:
            got,status,usage=os.wait4(-1,0)
            if got==pid:main_status=status
            reaped.append({'pid':got,'exit_code':os.waitstatus_to_exitcode(status),'user_cpu':usage.ru_utime,'system_cpu':usage.ru_stime,'peak_rss_kib':usage.ru_maxrss})
        except ChildProcessError:break
result={'mode':mode,'exit_code':None if main_status is None else os.waitstatus_to_exitcode(main_status),'watchdog_reason':reason,'wall_seconds':time.monotonic()-start,'wait4_total_cpu_seconds':sum(x['user_cpu']+x['system_cpu'] for x in reaped),'wait4_peak_rss_kib':max((x['peak_rss_kib'] for x in reaped),default=0),'launcher_CPU_seconds':time.process_time(),'launcher_hard_CPU_seconds':parent_cap,'child_hard_CPU_seconds':cpu,'aggregate_hard_ceiling_seconds':cpu+parent_cap,'AS_mib':mem//1024**2,'postexec_observations':list(seen.values()),'wait4_records':reaped,'whole_tree_empty':not members(),'automatic_retry':False}
(P/(mode+'_resources.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(0 if result['exit_code']==0 and reason is None and seen else 1)
