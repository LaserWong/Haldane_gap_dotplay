import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,math,itertools,time,resource,json
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigvalsh
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))

def construct(N=4,M=1):
 basis=[x for x in itertools.product(range(9),repeat=N) if sum(C.MAG[i] for i in x)==M];ind={x:i for i,x in enumerate(basis)};weights=np.array([math.prod(C.W[i] for i in x) for x in basis]);diag=np.array([sum(C.EX[i] for i in x) for x in basis]);rr=[];cc=[];vv=[];den=math.lcm(*(v.denominator for row in C.K.values() for _,_,v in row))
 for c,state in enumerate(basis):
  for j in range(N):
   i=(j-1)%N
   for p,q,v in C.K[state[i],state[j]]:
    s=list(state);s[i]=p;s[j]=q;r=ind[tuple(s)];rr.append(r);cc.append(c);vv.append(int(v*den))
 A=sp.coo_matrix((vv,(rr,cc)),shape=(len(basis),len(basis))).tocsr();A.sum_duplicates();A.eliminate_zeros();sq=np.sqrt(weights)
 V=sp.diags(sq)@A@sp.diags(1/sq)/den
 return basis,weights,diag,A,den,V

def momentum_basis(basis,weights,k):
 ind={x:i for i,x in enumerate(basis)};seen=set();rr=[];cc=[];vv=[];col=0
 for state in basis:
  if state in seen:continue
  orbit=[];s=state
  while s not in orbit:orbit.append(s);seen.add(s);s=s[-1:]+s[:-1]
  m=len(orbit)
  if k*m%4:continue
  for j,s in enumerate(orbit):rr.append(ind[s]);cc.append(col);vv.append((1j)**(-k*j)/math.sqrt(m))
  col+=1
 return sp.coo_matrix((vv,(rr,cc)),shape=(len(basis),col)).tocsr()

def local_cut(g,e):
 w=np.array([a*b for a in C.W for b in C.W]);diag=np.array([a+b for a in C.EX for b in C.EX]);V=np.zeros((81,81))
 for (i,j),row in C.K.items():
  for a,b,v in row:V[9*a+b,9*i+j]=float(v)*math.sqrt(w[9*a+b]/w[9*i+j])
 best=(-1,None)
 for ai in range(1,1000):
  a=ai/2000;ev=eigvalsh(g*V+np.diag(a*diag),subset_by_index=[0,0])[0];b=max(0,-ev);cut=e*(1-2*a)-4*b
  if cut>best[0]:best=(cut,a,b)
 return best

def main():
 st=time.monotonic();basis,w,diag,A,den,V=construct();records=[]
 for g in [.18,.185,.19,.195,.2]:
  H=sp.diags(diag)+g*V;rows=[]
  for k in range(3):
   T=momentum_basis(basis,w,k);B=T.conj().T@H@T;val=eigsh(B,k=6,which='SA',return_eigenvectors=False,tol=1e-12);val=sorted(map(float,val))
   rows.append(dict(k=k,dimension=B.shape[0],lowest_six=val))
  result=dict(g=g,ground_shift_approx=None,spin_M1_block_dimension=len(basis),momentum=rows,global_lambda14_affine_cutoff=local_cut(g,2),global_lambda2_affine_cutoff=local_cut(g,1));records.append(result);print(result,flush=True)
 (HERE/'benchmark.json').write_text(json.dumps(dict(status='FLOATING_DIAGNOSTIC_ONLY',results=records,seconds=time.monotonic()-st,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
if __name__=='__main__':main()
