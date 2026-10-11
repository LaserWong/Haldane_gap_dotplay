import os,sys,time,signal,ctypes,fcntl,json
from pathlib import Path
import controller as c
p=c.P;begin=time.monotonic();assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
pid=os.fork()
if pid==0:
 fd=os.open(p/'controller_death_child.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.dup2(fd,1);os.dup2(fd,2);os.close(fd)
 os.execv(sys.executable,[sys.executable,str(p/'controller.py'),'death_q6','3','chunk','generic','4','6','0','28'])
worker=None
while time.monotonic()-begin<5:
 if (p/'BUDGET_LEDGER.json').exists():
  matches=[x for x in c.read(p/'BUDGET_LEDGER.json')['attempts'] if x['name']=='death_q6']
  if matches and matches[0]['state']=='running':
   worker=matches[0]['pid']
   try:exe=os.readlink(f'/proc/{worker}/exe')
   except FileNotFoundError:exe=''
   if exe==str(p/'whole'):break
 time.sleep(.002)
assert worker is not None and exe==str(p/'whole'),'numeric_worker_not_observed'
# The worker inherits the same flock across exec.
lock=open(p/'LOCK','a+')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);raise RuntimeError('second controller could enter')
except BlockingIOError:pass
os.kill(pid,signal.SIGKILL);w,st,u=os.wait4(pid,0);receipts=[{'pid':w,'exit':os.waitstatus_to_exitcode(st),'cpu':u.ru_utime+u.ru_stime}]
end=time.monotonic()+3
while True:
 try:w,st,u=os.wait4(-1,os.WNOHANG)
 except ChildProcessError:break
 if w:receipts.append({'pid':w,'exit':os.waitstatus_to_exitcode(st),'cpu':u.ru_utime+u.ru_stime});continue
 assert time.monotonic()<end,'worker_outlived_parent_death_bound';time.sleep(.002)
assert worker not in c.scan();assert any(x['pid']==worker and x['exit']==-9 for x in receipts)
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock.close()
l=c.read(p/'BUDGET_LEDGER.json');rec=next(x for x in l['attempts'] if x['name']=='death_q6');assert rec['state']=='running' and rec['charged']==3
assert not (p/'runs/death_q6/receipt.json').exists()
c.atomic(p/'CONTROLLER_DEATH_TEST.json',{'controller_killed':True,'worker_exec_observed':True,'inherited_lock_prevented_entry':True,'worker_killed_by_parent_death':True,'all_reaped':receipts,'no_worker_survives':True,'stale_reservation_charged':3,'wall':time.monotonic()-begin});print('CONTROLLER DEATH PASS')
