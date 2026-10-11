"""Production-profile session entrypoint. Requires absent explicit authority/pins.
No physical launch or production initialization has occurred in this gate.
"""
import os,sys,time,json,fcntl
from pathlib import Path
from engine import read,sha,atomic
from physical_session import required_pins,DEADLINE
from session_supervisor import supervise
ROOT=Path(__file__).resolve().parent

def launch(jobdir):
 jobdir=Path(jobdir).resolve();authority=read(jobdir/'PRODUCTION_AUTHORITY.json');assert authority['explicit_authorization'] is True and authority['hard_cap']==21600 and authority['deadline_utc']=='2026-10-14T00:00:00Z'
 pins=read(jobdir/'PINNED_INPUTS.json');assert required_pins(jobdir)<=set(pins) and all(sha(Path(p).read_bytes())==v for p,v in pins.items())
 assert (jobdir/'CONTROL_SESSIONS.json').exists(),'controller_budget_requires_explicit_initialization'
 lock=open(jobdir/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 sessions=read(jobdir/'CONTROL_SESSIONS.json')['sessions'] if (jobdir/'CONTROL_SESSIONS.json').exists() else [];sid=len(sessions);out=jobdir/'sessions'/str(sid);out.mkdir(parents=True,exist_ok=False)
 limit=authority.get('session_chunk_limit',100);assert 1<=limit<=100
 # Every dispatched worker has allowance<=6, so this is a full scheduled-work
 # session wall bound, not a multiple of controller CPU. Global deadline also applies.
 wall_limit=min((2*6+10)*limit+60,DEADLINE-time.time()-30);assert wall_limit>30
 result=supervise([sys.executable,str(ROOT/'physical_session.py'),str(jobdir),str(out)],out,jobdir/'CONTROL_SESSIONS.json',20,3,max_descendants=2,lock_fd=lock.fileno(),wall_limit=wall_limit,poll_interval=.05,graceful_controller=True,controller_address_space=64*1024**2,supervisor_address_space=32*1024**2,descendant_address_space=160*1024**2)
 atomic(out/'RESOURCES.json',result);assert result['exit']==0,'Stopped session retains charges; inspect before continuation'
if __name__=='__main__':launch(sys.argv[1])
