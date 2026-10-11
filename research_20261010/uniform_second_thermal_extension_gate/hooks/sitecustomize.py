"""Supervisor-only descendant lifetime/memory guard; not installed system-wide."""
import os,signal,time,ctypes,resource,subprocess
# All runner and kernel descendants share96MiB each; watchdog64MiB, total<=256MiB.
_original_limit=resource.setrlimit
_child_cpu_cap=35
MEM=96*1024**2
def limited(which,limits):
 if which==resource.RLIMIT_AS:limits=(min(limits[0],MEM),min(limits[1],MEM))
 if which==resource.RLIMIT_CPU:limits=(min(limits[0],_child_cpu_cap),min(limits[1],_child_cpu_cap))
 return _original_limit(which,limits)
resource.setrlimit=limited
_original_popen=subprocess.Popen
_deadline=float(os.environ['HALDANE_CAMPAIGN_DEADLINE'])
_libc=ctypes.CDLL(None,use_errno=True)
def bind_lifetime(parent):
 if _libc.prctl(1,signal.SIGKILL,0,0,0)!=0:raise OSError(ctypes.get_errno(),'PR_SET_PDEATHSIG')
 if os.getppid()!=parent:os.kill(os.getpid(),signal.SIGKILL)
 signal.signal(signal.SIGALRM,signal.SIG_DFL)
 signal.setitimer(signal.ITIMER_REAL,max(.001,_deadline-time.time()))
class GuardedPopen(_original_popen):
 def __init__(self,*args,**kwargs):
  original=kwargs.get('preexec_fn');parent=os.getpid()
  command=args[0] if args else kwargs.get('args');assert isinstance(command,(list,tuple))
  mode=command[-1];assert mode in ('list','matrix','compute'),'unexpected child command'
  cap=5 if mode in ('list','matrix') else 35
  def preexec():
   global _child_cpu_cap
   _child_cpu_cap=cap
   if original:original()
   bind_lifetime(parent)
  kwargs['preexec_fn']=preexec
  super().__init__(*args,**kwargs)
subprocess.Popen=GuardedPopen
