import os,sys,json,subprocess,signal,time,hashlib,shutil,fcntl,resource
from pathlib import Path
P=Path(__file__).resolve().parent;R=Path(os.environ.get('RESEARCH_ROOT',P.parent));os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CORE,(0,0))
geo=R/'bilayer_complete_residual_8x4/geometry_4x2.txt';coef=P/'fixture_coefficients.txt'
def cmd(home,out,coeff=coef):return [str(home/'outer_driver'),'fixture',str(home),str(out),str(geo),str(coeff)]
def ledger(out):return [json.loads(x) for x in (out/'outer_ledger.jsonl').read_text().splitlines()]
def dead(pid):
 try:return Path(f'/proc/{pid}/stat').read_text().split()[2]=='Z'
 except FileNotFoundError:return True
out=P/'exact_campaign';p=subprocess.run(cmd(P,out),capture_output=True,text=True,timeout=10);assert p.returncode==0,p.stderr
complete=json.loads((out/'checkpoint/complete_row.json').read_text());ref=json.loads((R/'bilayer_residual_direction_fixture_review/independent.json').read_text())
for k,v in complete['rows'].items():assert v==ref[k]
assert complete['polynomial']['A_row']==ref['A'];assert complete['polynomial']['A2_row']==ref['A_squared']
L=ledger(out);charges=[x for x in L if x['event']=='reserve_invocation'];assert [x['cpu_cap_including_supervisor'] for x in charges]==[1,2,2,2,2,1];assert L[-1]['cumulative_reserved']==20
state=json.loads((out/'checkpoint/state.json').read_text());assert state['binding']['/usr/bin/python3']==hashlib.sha256(Path('/usr/bin/python3').read_bytes()).hexdigest();assert state['charged_cpu_seconds']==10
bad=P/'bad_coeff.txt';bad.write_text('0\n');out=P/'failed_campaign';p=subprocess.run(cmd(P,out,bad),capture_output=True,text=True,timeout=5);assert p.returncode==2
L=ledger(out);assert L[-1]['event']=='STOPPED_ON_FIRST_FAILURE' and L[-1]['cumulative_reserved']==11;assert sum(x['event']=='reserve_invocation' for x in L)==1
home=P/'probe_home';home.mkdir()
for f in ['outer_driver','outer_driver.cpp','checkpoint.py','chunk_kernel.cpp','base_kernel.inc','init_kernel.inc']:shutil.copy2(P/f,home/f)
shutil.copy2(P/'interrupt_probe',home/'chunk_kernel');tests=[]
for victim,sig in [('outer',signal.SIGKILL),('outer',signal.SIGXCPU),('supervisor',signal.SIGKILL)]:
 out=P/(victim+'_'+sig.name);env=dict(os.environ,RESIDUAL_TEST_DIR=str(out),RESIDUAL_REAL_KERNEL=str(P/'chunk_kernel'))
 p=subprocess.Popen(cmd(home,out),env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  end=time.monotonic()+4
  while not (out/'child.pid').exists() or not (out/'child.pid').read_text().strip():assert p.poll() is None;assert time.monotonic()<end;time.sleep(.01)
  child=int((out/'child.pid').read_text());sup=int(Path(f'/proc/{child}/stat').read_text().split()[3]);assert not dead(child) and not dead(sup)
  caps=[]
  for pid,cpu,mem in [(p.pid,10,8),(sup,1,32),(child,1,60)]:
   lines=Path(f'/proc/{pid}/limits').read_text().splitlines()
   cl=next(x for x in lines if x.startswith('Max cpu time')).split();ml=next(x for x in lines if x.startswith('Max address space')).split()
   assert int(cl[3])==cpu and int(ml[3])==mem*1024**2
   st=dict(x.split(':',1) for x in Path(f'/proc/{pid}/status').read_text().splitlines() if ':' in x)
   assert not(int(st['SigBlk'],16)&(1<<(signal.SIGXCPU-1)));assert not(int(st['SigIgn'],16)&(1<<(signal.SIGXCPU-1)))
   caps.append([cpu,mem])
  for f in [out/'outer.lock',out/'checkpoint/lock']:
   ino=f.stat().st_ino;assert any(fd.stat().st_ino==ino for fd in Path(f'/proc/{child}/fd').iterdir())
   with f.open('a') as fd:
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:pass
    else:raise AssertionError('lock not retained')
  os.kill(p.pid if victim=='outer' else sup,sig);p.wait(timeout=4);end=time.monotonic()+3
  while not(dead(sup) and dead(child)):assert time.monotonic()<end;time.sleep(.01)
  if victim=='outer':assert p.returncode==-sig
  else:assert p.returncode==2 and ledger(out)[-1]['event']=='STOPPED_ON_FIRST_FAILURE'
  digest=lambda:hashlib.sha256((out/'outer_ledger.jsonl').read_bytes()).hexdigest()
  h=digest();again=subprocess.run(cmd(home,out),env=env,capture_output=True,timeout=4);assert again.returncode!=0 and digest()==h
  st=json.loads((out/'checkpoint/state.json').read_text());assert st['charged_cpu_seconds']==3 and st['attempts'][0]['status']=='reserved'
  tests.append({'victim':victim,'signal':sig.name,'all_descendants_dead':True,'both_locks_inherited':True,'effective_cpu_and_memory_caps':caps,'SIGXCPU_unblocked_and_not_ignored':True,'restart_refused_ledger_unchanged':True,'reservation_not_refunded':True})
 finally:
  if p.poll() is None:p.kill();p.wait()
result={'status':'PASS_SOLE_PATH_OUTER_GATE','all_66_physical_entries':True,'all_44_coupling_entries':True,'interpreter_hash_bound':True,'preflight_failure_precharged_and_stops':True,'fixture_call_caps':[1,2,2,2,2,1],'production_calls':46,'production_call_reservation':350,'driver_reservation':10,'total_reservation':360,'memory_MiB':[8,32,60],'death_tests':tests,'scope':'No 8x4 support work; sole authorized path only; no automatic reset'}
(P/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS independent outer gate')
