import os,resource,json,subprocess,time
from pathlib import Path
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(128*1024**2,128*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(3,30))
p=Path(__file__).resolve().parent;text=(p/'ldl_results.json').read_text();assert text.endswith('}');done=json.loads(text+']');assert len(done)==6
(p/'ldl_first_completed.json').write_text(json.dumps(done,indent=2)+'\n');names={a['name'] for a in done};tok=iter((p/'ldl_input.txt').read_text().split());n=int(next(tok));rest=[]
for _ in range(n):
 name=next(tok);size=int(next(tok));values=[next(tok) for _ in range(size*size)]
 if name not in names:rest.append((name,size,values))
assert len(rest)==3
(p/'ldl_remaining_input.txt').write_text(str(len(rest))+'\n'+'\n'.join(name+' '+str(size)+'\n'+' '.join(values) for name,size,values in rest)+'\n')
def limits():resource.setrlimit(resource.RLIMIT_CPU,(25,25));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,64*1024**2))
# Raise hard ceiling only before fork to allow the separately bounded25-second child;
# the supervisor retains its3-second terminating soft CPU allowance.
resource.setrlimit(resource.RLIMIT_CPU,(3,30))
before=resource.getrusage(resource.RUSAGE_CHILDREN);result=subprocess.run([str(p/'exact_ldl'),str(p/'ldl_remaining_input.txt'),str(p/'ldl_remaining_results.json')],preexec_fn=limits,timeout=45);after=resource.getrusage(resource.RUSAGE_CHILDREN);assert result.returncode==0
extra=json.loads((p/'ldl_remaining_results.json').read_text());assert len(extra)==3
(p/'ldl_complete_results.json').write_text(json.dumps(done+extra,indent=2)+'\n');(p/'ldl_recovery_resources.json').write_text(json.dumps(dict(first_child_hard_cpu_charge=10,first_child_wall_timeout=15,completed_jobs_preserved=6,resumed_only_missing_jobs=3,second_child_cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,second_child_hard_cap=25,no_physical_work=True),indent=2)+'\n');print([(a['name'],a['PSD'],a['rank_if_PSD']) for a in extra])
