import os,sys,subprocess,signal,time,json,fcntl,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;R=Path(os.environ.get('RESEARCH_ROOT',P.parent));root=P/'interrupt_audit';root.mkdir()
for f in ['checkpoint.py','chunk_kernel.cpp','base_kernel.inc','init_kernel.inc']:shutil.copy2(P/f,root/f)
shutil.copy2(P/'interrupt_probe',root/'chunk_kernel')
def gone(pid):
 try:return Path('/proc/%d/stat'%pid).read_text().split()[2]=='Z'
 except FileNotFoundError:return True
results=[]
for sig in (signal.SIGKILL,signal.SIGXCPU,signal.SIGTERM):
 folder=root/sig.name;env=dict(os.environ,RESIDUAL_TEST_DIR=str(folder),RESIDUAL_REAL_KERNEL=str(P/'chunk_kernel'))
 base=[sys.executable,str(root/'checkpoint.py')]
 subprocess.run(base+['init',str(folder),'--geometry',str(R/'bilayer_complete_residual_8x4/geometry_4x2.txt'),'--coefficients',str(P/'fixture_coefficients.txt'),'--nx','4','--ny','2','--budget','6'],env=env,check=True,stdout=subprocess.DEVNULL)
 cmd=base+['chunk',str(folder),'--phase','q4','--count','1','--cap','2'];proc=subprocess.Popen(cmd,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  end=time.monotonic()+3
  while not (folder/'child.pid').exists():
   assert proc.poll() is None;assert time.monotonic()<end;time.sleep(.01)
  pid=int((folder/'child.pid').read_text());assert not gone(pid)
  inode=(folder/'lock').stat().st_ino;assert any(f.stat().st_ino==inode for f in Path(f'/proc/{pid}/fd').iterdir())
  fd=os.open(folder/'lock',os.O_WRONLY)
  try:
   try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:pass
   else:raise AssertionError('missing live-child lock')
  finally:os.close(fd)
  proc.send_signal(sig);proc.wait(timeout=3);end=time.monotonic()+3
  while not gone(pid):assert time.monotonic()<end;time.sleep(.01)
  assert proc.returncode==-sig
  st=json.loads((folder/'state.json').read_text());assert st['charged_cpu_seconds']==3 and st['attempts'][0]['status']=='reserved'
  fd=os.open(folder/'lock',os.O_WRONLY);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);os.close(fd)
  (folder/'allow_go').write_text('continue\n');subprocess.run(cmd,env=env,check=True,stdout=subprocess.DEVNULL,timeout=5)
  st=json.loads((folder/'state.json').read_text());assert st['charged_cpu_seconds']==5 and [a['status'] for a in st['attempts']]==['reserved','complete']
  assert st['attempts'][1]['start']==0
  results.append({'signal':sig.name,'child_dead':True,'inherited_lock_verified':True,'reservation_preserved':True,'real_small_kernel_resumed':True})
 finally:
  if proc.poll() is None:proc.kill();proc.wait()
import checkpoint as c
pid=os.fork()
if pid==0:c.arm_parent_death(os.getppid()+1);os._exit(97)
_,status=os.waitpid(pid,0);assert os.WIFSIGNALED(status) and os.WTERMSIG(status)==signal.SIGKILL
(P/'interrupt_result.json').write_text(json.dumps({'status':'PASS_INDEPENDENT_SUPERVISOR_DEATH_LOCK_AND_RESTART','tests':results,'parent_identity_race_guard':True},indent=2)+'\n');print('PASS interruption checks')
