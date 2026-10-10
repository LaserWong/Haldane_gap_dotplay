"""Small M4 complete physical-basis floating check; never certificate evidence."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[key]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import math,json,itertools,time,resource
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.linalg import eigvalsh
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
HERE=Path(__file__).resolve().parent;PROD=HERE/'snapshot' if (HERE/'snapshot').exists() else HERE.parent/'chain_small_low_band'
def main():
 start=time.monotonic();g=F(1,5);sectors=defaultdict(list)
 for s in itertools.product([-1,0,1],repeat=8):sectors[sum(s)].append(s)
 edges=[(2*i,2*i+1,F(1)) for i in range(4)]+[((2*i-1)%8,2*i,g) for i in range(4)]
 vals=[];blocks=[]
 for m,basis in sorted(sectors.items()):
  index={s:i for i,s in enumerate(basis)};H=np.zeros((len(basis),len(basis)))
  for col,s in enumerate(basis):
   H[col,col]=8+sum(float(c)*s[i]*s[j] for i,j,c in edges)
   for i,j,c in edges:
    for sign in [-1,1]:
     if -1<=s[i]+sign<=1 and -1<=s[j]-sign<=1:
      t=list(s);t[i]+=sign;t[j]-=sign;H[index[tuple(t)],col]+=float(c)
  assert np.array_equal(H,H.T)
  v=eigvalsh(H);vals.extend(v.tolist());blocks.append(dict(magnetization=m,dimension=len(basis),min_shift=float(v[0])))
 vals=np.sort(vals);assert len(vals)==6561
 p=json.loads((PROD/'patch_g1d5.json').read_text());s=p['small'];band=s['low_band']
 lower=[float(F(s['ground_lower'])+8)]+[float(F(x['eigenvalue_lower'])) for x in band['triplet_modes'] for _ in range(x['multiplicity'])]+[float(F(band['alpha'])*e-F(band['B'])) for e,n in band['complete_reference_bins'] if e>=2 for _ in range(n)]
 assert len(lower)==6561 and lower==sorted(lower)
 diff=vals-np.array(lower);assert min(diff)>-1e-8
 trace=[]
 for beta in [2,5,10,20,40,80]:
  shift=float(F(s['exact_rayleigh'])+8);actual=float(np.sum(np.exp(-beta*(vals-shift))));upper=float(np.sum(np.exp(-beta*(np.array(lower)-shift))))
  assert actual<=upper+1e-7;trace.append(dict(beta=beta,actual_normalized_trace=actual,counted_bound=upper))
 result=dict(status='FLOATING_DIAGNOSTIC_ONLY',physical_basis='8 spin-one Sz product states; independent bond assembly',g=str(g),M=4,full_dimension=6561,blocks=blocks,lowest_24_shift=vals[:24].tolist(),lower_first_24=lower[:24],minimum_ordered_margin=float(min(diff)),all_6561_ordered_comparisons_pass=True,trace=trace,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/'physical_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','lowest_24_shift','minimum_ordered_margin','trace','seconds','peak_rss_kib']},indent=2))
if __name__=='__main__':main()
