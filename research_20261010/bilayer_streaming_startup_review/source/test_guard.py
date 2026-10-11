import os,sys,time,signal,resource,ctypes
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from engine import atomic
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(2,100));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,128*1024**2));assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
ledger=P/'TEST_LEDGER.json';assert not ledger.exists();r=dict(authorized=5,charged=5,child_reservation=3,external_reservation=2,state='reserved');atomic(ledger,r);pid=os.fork()
if pid==0:
 assert ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)==0
 os.setsid();os.execv(sys.executable,[sys.executable,str(P/'startup_test.py')])
start=time.monotonic();peak=0;reason=None
while True:
 w,st,u=os.wait4(pid,os.WNOHANG)
 if w:break
 try:
  s=Path('/proc/%d/stat'%pid).read_text();v=s[s.rfind(')')+2:].split();cpu=(int(v[11])+int(v[12]))/os.sysconf('SC_CLK_TCK');rss=int(v[21])*os.sysconf('SC_PAGE_SIZE');peak=max(peak,rss)
  if cpu>=2.9:reason='child_external_cpu_guard'
  if time.process_time()>=1.8:reason='external_self_cpu_guard'
  if time.monotonic()-start>30:reason='wall_guard'
 except FileNotFoundError:continue
 if reason:os.killpg(pid,signal.SIGKILL);w,st,u=os.wait4(pid,0);break
 time.sleep(.01)
r.update(state='complete' if st==0 and reason is None else 'failed',exit=os.waitstatus_to_exitcode(st),reason=reason,wait4_child_cpu=u.ru_utime+u.ru_stime,external_self_cpu=time.process_time(),child_peak_rss_bytes=peak,wall=time.monotonic()-start);atomic(ledger,r);print(r);assert r['state']=='complete','Unexpected failure; no retry authorized'
