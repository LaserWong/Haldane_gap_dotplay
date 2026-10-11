import fcntl,json,os,signal,subprocess,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent;testhome=p/'adversarial_launcher';assert not testhome.exists();testhome.mkdir()
for name in ['checkpoint.py','chunk_kernel.cpp','base_kernel.inc','init_kernel.inc']:(testhome/name).write_bytes((p/name).read_bytes())
(testhome/'chunk_kernel').write_bytes((p/'interrupt_probe').read_bytes());(testhome/'chunk_kernel').chmod(0o755)
python=sys.executable;script=str(testhome/'checkpoint.py');results=[]
def dead(pid):
 try:return Path(f'/proc/{pid}/stat').read_text().split()[2]=='Z'
 except FileNotFoundError:return True
for sig in [signal.SIGKILL,signal.SIGXCPU]:
 folder=p/f'interrupt_{sig.name}';env=dict(os.environ,RESIDUAL_TEST_DIR=str(folder),RESIDUAL_REAL_KERNEL=str(p/'chunk_kernel'))
 init=[python,script,'init',str(folder),'--geometry',str(p.parent/'bilayer_complete_residual_8x4/geometry_4x2.txt'),'--coefficients',str(p/'fixture_coefficients.txt'),'--nx','4','--ny','2','--budget','6']
 subprocess.run(init,env=env,check=True,stdout=subprocess.DEVNULL)
 cmd=[python,script,'chunk',str(folder),'--phase','q4','--count','1','--cap','2'];sup=subprocess.Popen(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 deadline=time.monotonic()+3
 while not (folder/'child.pid').exists():
  assert sup.poll() is None,'supervisor exited before child ready';assert time.monotonic()<deadline;time.sleep(.01)
 pid=int((folder/'child.pid').read_text());assert not dead(pid)
 # Demonstrate kernel actually retains the exact campaign flock descriptor.
 lock_inode=(folder/'lock').stat().st_ino
 inherited=[str(f) for f in Path(f'/proc/{pid}/fd').iterdir() if f.stat().st_ino==lock_inode]
 assert inherited,'kernel lacks inherited lock descriptor'
 conflicting=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=3)
 assert conflicting.returncode!=0 and 'BlockingIOError' in conflicting.stderr
 before=json.loads((folder/'state.json').read_text());assert before['charged_cpu_seconds']==3 and before['attempts'][0]['status']=='reserved'
 os.kill(sup.pid,sig);sup.wait(timeout=3)
 deadline=time.monotonic()+3
 while not dead(pid):assert time.monotonic()<deadline,'orphan child remains alive';time.sleep(.01)
 assert sup.returncode==-sig
 # Child death released the inherited descriptor; restart is now safe.
 with (folder/'lock').open('a') as f:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
 (folder/'allow_go').write_text('resume actual small kernel\n');res=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=5);assert res.returncode==0,res.stderr
 after=json.loads((folder/'state.json').read_text());assert after['charged_cpu_seconds']==5
 assert [a['status'] for a in after['attempts']]==['reserved','complete']
 assert after['attempts'][1]['start']==0 and after['attempts'][1]['end']==1
 record=json.loads((folder/after['attempts'][1]['output']).read_text());assert record['raw']['N']==8 and record['raw']['q4_processed']==1
 results.append(dict(signal=sig.name,supervisor_returncode=sup.returncode,child_pid=pid,child_dead_after_supervisor=True,inherited_lock_fds=len(inherited),concurrent_restart_rejected=True,lock_released_after_child_death=True,successful_real_kernel_resume=True,interrupted_attempt_remains_charged=True,charged_after_death=3,charged_after_resume=5))
import checkpoint as c
child=os.fork()
if child==0:
 c.arm_parent_death(os.getppid()+1)
 os._exit(99)
_,status=os.waitpid(child,0);assert os.WIFSIGNALED(status) and os.WTERMSIG(status)==signal.SIGKILL
results.append(dict(parent_identity_race_guard_mismatch_kills_child=True))
(p/'interruption_tests.json').write_text(json.dumps(dict(status='PASS_REAL_SUPERVISOR_DEATH_AND_RESTART',tests=results,scope='single-process delayed probe followed by actual 4x2 one-support kernel; no8x4'),indent=2)+'\n');print(json.dumps(results,indent=2))
