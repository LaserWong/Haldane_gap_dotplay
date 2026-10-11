"""Bounded review adapter: actual frozen dispatcher, one hard-allowlisted worker."""
import sys,os,json
from pathlib import Path
P=Path(__file__).resolve().parent;S=P/'receipt_sandbox';sys.path.insert(0,str(S))
import physical_session as p
p.ROOT=P.parent/'bilayer_incremental_control_receipt_fix';p.KERNEL=P.parent/'bilayer_variable_g_control_gate'
job=Path(sys.argv[1]);auth=p.read(job/'PRODUCTION_AUTHORITY.json')
assert auth['review_scope']=='ONE_VACUUM_CHUNK_ONLY' and auth['permitted_worker_ranges']==[{'q':0,'begin':0,'end':1,'N':1,'cap':3}]
actual_worker=p.worker;calls=0

def only_vacuum(out,row,identity,lockfd):
 global calls
 assert calls==0 and row==auth['permitted_worker_ranges'][0],'review_hard_worker_allowlist'
 calls+=1
 try:return actual_worker(out,row,identity,lockfd)
 finally:p.STOP=True
p.worker=only_vacuum
p.run(job,Path(sys.argv[2]));assert calls==1
p.atomic(Path(sys.argv[2])/'REVIEW_ALLOWLIST.json',dict(scope='ONE_VACUUM_CHUNK_ONLY',worker_calls=calls,stop_set_before_commit=True))
