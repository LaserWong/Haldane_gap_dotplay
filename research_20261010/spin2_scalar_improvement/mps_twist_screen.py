"""Floating diagnostic of existing exact MPS blocks with twist characters.
No new tensor, physical spectrum, or rigorous twist certificate is produced.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np,json,hashlib,time
from pathlib import Path
P=Path(__file__).resolve().parent
src=Path('/workspace/shared/haldane_optimization/upstream/extracted/cases/spin2_campaign/mps/improved124_exact_blocks.txt')
start=time.time();Ns=[128,256,512,1024];out={str(N):{tw:{'u':0.,'v':0.} for tw in ['I','P','C']}for N in Ns};blocks=[]
with src.open() as f:
 nb=int(f.readline())
 for _ in range(nb):
  J,n=map(int,f.readline().split())
  T=np.array([list(map(float,f.readline().split()))for _ in range(n)])
  O=np.array([list(map(float,f.readline().split()))for _ in range(n)])
  if J==0:scale=max(abs(np.linalg.eigvals(T)))
  T/=scale;O/=scale**2
  chars={'I':2*J+1,'P':(-1)**J,'C':[1,0,-1][J%3]}
  TT=T@T
  for N in Ns:
   A=np.linalg.matrix_power(T,N-2);u=float(np.trace(A@O));v=float(np.trace(A@TT))
   for tw,c in chars.items():out[str(N)][tw]['u']+=c*u;out[str(N)][tw]['v']+=c*v
  blocks.append({'J':J,'dimension':n})
for N,v in out.items():
 for tw,t in v.items():
  t['energy_per_site']=t['u']/t['v'];t['beta8_trace_trial_lower_candidate']=float(np.exp(-8*int(N)*(t['energy_per_site']+4.76121)))
result={'status':'FLOATING_EXPLORATORY_ONLY_NOT_A_TWIST_CERTIFICATE','blocks_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seconds':time.time()-start,'blocks':blocks,'rows':out}
(P/'mps_twist_screen.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
