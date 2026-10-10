"""Independent scalar composition replay using the sealed earlier verifier.
The new physical 13-state theorem is additionally externally reviewed.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,time,resource,importlib.util,hashlib
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from functools import lru_cache
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=HERE.parent/'chain_filter_extension'
spec=importlib.util.spec_from_file_location('sealed_verifier',OLD/'verify_extension.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V);C=V.C
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))

def trace(s,beta):
 z=s['low_band'];rho=Q(s['exact_rayleigh']);lo=Q(s['ground_lower']);alpha=Q(z['alpha']);B=Q(z['B'])
 answer=C.exp_bounds(beta*(rho-lo))[1]
 for row in z['triplet_modes']:answer+=row['multiplicity']*C.exp_bounds(beta*(rho+8-Q(row['eigenvalue_lower'])))[1]
 for e,m in z['complete_reference_bins']:
  if e>=2:answer+=m*C.exp_bounds(beta*(rho+8-alpha*e+B))[1]
 return answer,None
V.C.trace_bound=trace

def patch_check(rec):
 g=Q(rec['g']);s=rec['input']['small'];p=s['low_band'];C.DATA=ROOT/rec['input']['small_folder'];small=C.check_ground(s)
 lc=p['local_comparison'];assert Q(lc['a'])==g/2 and Q(lc['b'])==g+Q(1,10**12);psd=C.local_psd(lc)
 alpha=1-g;B=4*Q(lc['b']);a=2*alpha-B
 assert [alpha,B,a]==list(map(Q,[p['alpha'],p['B'],p['omitted_cutoff']])) and p['codimension']==13
 bins=Counter({0:1})
 for _ in range(4):
  nxt=Counter()
  for e,m in bins.items():
   for f,d in [(0,1),(1,3),(3,5)]:nxt[e+f]+=m*d
  bins=nxt
 assert sorted(map(list,bins.items()))==p['complete_reference_bins'] and sum(bins.values())==6561 and sum(m for e,m in bins.items() if e>=2)==6548==p['remaining_count']
 data=[(p['ground_Schur'],Q(0),Q(16,3)*g*g)]+[(row,d,v) for row,d,v in zip(p['triplet_modes'],[1-4*g/3,Q(1),1+4*g/3],[6*g*g,Q(32,9)*g*g,Q(14,3)*g*g])]
 assert [row['multiplicity'] for row in p['triplet_modes']]==[3,6,3]
 roots=[]
 for row,d,var in data:
  lo=Q(row['eigenvalue_lower']);root=Q(row['root_upper'])
  assert [d,var,a]==list(map(Q,[row['theta'],row['full_residual_squared'],row['complement_cutoff']]))
  rad=(d-a)**2+4*var
  assert root**2>=rad and (root-Q(1,10**30))**2<rad
  assert lo<=Q(d+a-root,2) and lo<a and (d-lo)*(a-lo)>=var
  roots.append(lo)
 assert roots==sorted(roots) and roots[0]<Q(s['ground_lower'])+8<roots[1]
 largest=V.load(OLD/'M8_two_trial_moments.json');rho8=V.energy(largest,list(map(int,rec['input']['large']['combination_integers'])),g)
 assert rho8==Q(rec['input']['large']['exact_rayleigh'])
 return dict(small_physical=small,local_PSD=psd,exact_channel_formulas=True,Schur_lower_roots_verified=True,full_6561_reference_count=True,largest_two_dimensional_Rayleigh_verified=True,largest_support_reconstructed=False)

def main():
 start=time.monotonic();manifest=V.load(OLD/'FROZEN_MANIFEST.json');assert hashlib.sha256((OLD/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='bc1b7bcc23f7f217c558a77790c0c45a8763ae40c1d8b20b5ca3b50d18d16370'
 for name,digest in manifest.items():assert hashlib.sha256((OLD/name).read_bytes()).hexdigest()==digest
 out=[]
 for path in sorted(HERE.glob('candidate_g*.json')):
  rec=V.load(path);g=Q(rec['g']);physical=patch_check(rec);rows=[]
  for row in rec['rows']:
   checked=V.verify_row(rec,row);bridge=row['all_size_bridge'];beta=Q(row['beta']);J=Q(row['J_lower']);S=C.floor(V.sqrtlo(J))
   wg=V.verify_window(bridge['initial_M4_M8_window'],S,J,J,4,beta)
   short=[]
   for M,saved in zip([2,3],bridge['M2_M3']):
    bound=1-(M+1)*g-Q(M,10**12);assert bound==Q(saved['gap_lower'])>0 and saved['M']==M and saved['full_dimension']==9**M
    assert Q(saved['rayleigh_upper'])==-2*M and Q(saved['second_eigenvalue_lower'])==-2*M+bound
    short.append(bound)
   total=min(Q(checked['M_ge8_gap_lower']),wg,*short)
   assert total==Q(bridge['all_M_ge2_gap_lower'])==Q(row['all_M_ge2_gap_lower'])
   rows.append(dict(**checked,initial_integer_M4_M8_window_verified=True,short_M2_M3_verified=True,all_M_ge2_gap_lower=str(total)))
  best=max(rec['rows'],key=lambda x:Q(x['all_M_ge2_gap_lower']));assert best==rec['best']
  out.append(dict(g=str(g),physical=physical,rows=rows,all_M_ge2_gap_lower=best['all_M_ge2_gap_lower']));print('PASS',g,best['all_M_ge2_gap_lower'],flush=True)
 result=dict(status='PASS independent local composition replay; external block/count review still required',results=out,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
