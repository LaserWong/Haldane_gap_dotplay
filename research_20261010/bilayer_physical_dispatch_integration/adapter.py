"""Bounded test adapter, never a production launcher."""
import sys,os,time,json
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent; BASE=P.parent/'bilayer_incremental_control_receipt_fix'
sys.path.insert(0,str(BASE));import engine,physical_session as phys
from engine import atomic,read,sha
ROWS=[dict(q=q,begin=0,end=1,N=n,cap=3) for q,n in [(0,1),(2,496),(4,4495),(6,169911)]]
def partial_check(store,jobdir,identity):
 try:phys_original_finalize(store,jobdir,identity)
 except AssertionError:pass
 else:raise AssertionError('partial full-coverage finalizer unexpectedly accepted')
 assert not (jobdir/'FULL_MOMENTS.json').exists()
 assert len(store.committed)==4 and not store.pending
 sector={v['range']['q']:list(map(int,v['values'])) for v in store.committed.values()}
 assert set(sector)=={0,2,4,6}
 sys.path.insert(0,str(phys.KERNEL));import pencil24
 scaled={q:[3*x for x in v] for q,v in sector.items()}
 export=pencil24.pencil(scaled,11,100,True);got={k:[x/3 for x in v] for k,v in pencil24.validate_export(export).items()}
 w={0:F(1),2:F(1),4:F(8),6:F(16,3)};v=[sum(w[q]*sector[q][i] for q in sector) for i in range(24)]
 m0,m1,m2lo,m3lo,m4lo,n8,cross,uz,wz=v[15:]
 m2=m2lo+121*n8;m3=m3lo+193600*n8+1331*sum(v[:4])+cross;m4=m4lo+sum(v[4:10])+14641*sum(v[10:15])
 assert got=={'G':[m0,m1,m2],'K':[m1/200,m2/200,m3/200],'J':[m2/40000,m3/40000,m4/40000]}
 atomic(jobdir/'PARTIAL_ASSEMBLY.json',dict(kind='TEST-ONLY-FOUR-TARGETS-NOT-FULL-MOMENTS',coverage={q:1 for q in sector},raw_sector=sector,normalized_rational_moments=list(map(str,[m0,m1,m2,m3,m4])),full_finalizer_rejected=True,three_times_partial_pencil=export))
phys_original_finalize=phys.finalize_physical
if __name__=='__main__':
 phase=int(sys.argv[1]);job=P/'job';out=P/'sessions'/str(phase)
 assert phase in (0,1);engine.plan=lambda:ROWS
 phys.KIND='INTEGRATION-ONLY-FOUR-SINGLETONS-NOT-PRODUCTION';phys.finalize_physical=partial_check
 original_worker=phys.worker;allowed={0,2} if phase==0 else {4,6};seen=[]
 if phase==0:
  for q,count in [(6,64),(4,16)]:
   row=dict(q=q,begin=0,end=count,N=169911 if q==6 else 4495,cap=3);dest=P/'controls'/str(q)
   ident=read(job/'PINNED_INPUTS.json');rec=original_worker(dest,row,ident,int(os.environ['BILAYER_LOCK_FD']));assert rec['exit']==0
   val=phys.verify_output(dest,rec,row,ident);accepted=phys.KERNEL/'runs'/('final_sample6' if q==6 else 'final_sample4')
   assert val==read(accepted/'result.json.accumulators.json')
   atomic(dest/'MATCH.json',dict(all24_equal=True,reference=str(accepted),reference_sha256=sha((accepted/'result.json.accumulators.json').read_bytes())))
 def bounded_worker(dest,row,ident,lock):
  assert row in ROWS and row['q'] in allowed and row['q'] not in seen,'hard_singleton_allowlist'
  seen.append(row['q']);return original_worker(dest,row,ident,lock)
 phys.worker=bounded_worker
 phys.run(job,out)
 assert set(seen)==allowed
 atomic(out/'ADAPTER_RESULT.json',dict(phase=phase,dispatched=seen,source_sha256=sha(Path(__file__).read_bytes()),partial_only=True))
