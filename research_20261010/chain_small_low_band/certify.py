"""Combine counted small low-band tails with the sealed joint-purity route."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,time,resource,hashlib
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=HERE.parent/'chain_filter_extension'
from produce_low_band import C,trace_exact,loadmod,save
assert hashlib.sha256((OLD/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='bc1b7bcc23f7f217c558a77790c0c45a8763ae40c1d8b20b5ca3b50d18d16370'
for p,h in json.loads((OLD/'FROZEN_MANIFEST.json').read_text()).items():assert hashlib.sha256((OLD/p).read_bytes()).hexdigest()==h
sys.path.insert(0,str(OLD));sc=loadmod('sealed_scalar',OLD/'certify_extension.py');sc.C.trace_bound=trace_exact;sc.TRACE.clear()
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
def bridge(rec,row):
 g=F(rec['g']);beta=F(row['beta']);J=F(row['J_lower']);S=C.floor(sc.sqrt_lower(J));T=J
 initial=sc.window(S,T,J,beta,4)
 lc=rec['small']['low_band']['local_comparison'];a=F(lc['a']);b=F(lc['b']);rows=[]
 for M in [2,3]:
  gap=1-2*a-M*b;assert gap>0
  rows.append(dict(M=M,physical_sites=2*M,full_dimension=9**M,trial='singlet product',rayleigh_upper=str(-2*M),second_eigenvalue_lower=str(-2*M+gap),gap_lower=str(gap)))
 target=min(F(row['M_ge8_gap_lower']),F(initial['gap_lower']),*(F(r['gap_lower']) for r in rows))
 return dict(M2_M3=rows,initial_M4_M8_window=initial,all_M_ge2_gap_lower=str(target))

def main():
 st=time.monotonic();patches=json.loads((HERE/'inputs.json').read_text());scans=json.loads((HERE/'float_scan.json').read_text());summary=[]
 for rec,scan in zip(patches,scans):
  assert rec['g']==scan['g'];best=scan['best'];rows=[]
  if best is None:continue
  beta=F(str(best['beta']));ts=best['time_steps'];cs=best['canonical_steps']
  for j in [-1,0,1]:
   for t in range(max(0,ts-1),ts+2):
    for c in range(max(0,cs-1),cs+3):
     row=sc.cycle(rec,beta+F(j,20),t,c)
     if not row.get('M_ge8_gap_lower') or F(row['M_ge8_gap_lower'])<=0:continue
     bb=bridge(rec,row)
     if F(bb['all_M_ge2_gap_lower'])>0:rows.append(dict(**row,all_size_bridge=bb,all_M_ge2_gap_lower=bb['all_M_ge2_gap_lower']))
  selected=max(rows,key=lambda x:F(x['all_M_ge2_gap_lower']))
  result=dict(status='EXACT_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g=rec['g'],input=rec,rows=rows,best=selected,method='13 bare reference vectors, exact full residual Gram, direct Schur count, complete e>=2 tail, retained joint ratios and all integer bridges')
  save('candidate_g'+rec['g'].replace('/','d')+'.json',result)
  summary.append(dict(g=rec['g'],all_M_ge2_gap_lower=selected['all_M_ge2_gap_lower'],display=float(F(selected['all_M_ge2_gap_lower'])),beta=selected['beta'],time_steps=selected['time_steps'],canonical_steps=selected['canonical_steps'],asymptotic_from=selected['final']['cells'],candidate_paths=len(rows),initial_window_gap=selected['all_size_bridge']['initial_M4_M8_window']['gap_lower']))
  print('EXACT',summary[-1],flush=True)
 save('summary.json',dict(status='CANDIDATES_PENDING_REVIEW',results=summary,seconds=time.monotonic()-st,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0))))
if __name__=='__main__':main()
