#!/usr/bin/env python3
"""One sparse extremal pair per invocation, proposal only; 300 CPU second cap."""
import os,resource,time,json,gzip,sys
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from pathlib import Path
P=Path(__file__).resolve().parent
n=int(sys.argv[1]);m=int(sys.argv[2]);assert n in (10,12) and m in (0,1)
t0=time.time();codes=np.arange(3**n,dtype=np.int64);mag=np.zeros(len(codes),dtype=np.int8)
for a in range(n):mag+=(codes//3**a)%3-1
codes=codes[mag==m];d=len(codes);idx=np.full(3**n,-1,dtype=np.int32);idx[codes]=np.arange(d,dtype=np.int32)
dig=np.array([(codes//3**a)%3 for a in range(n)],dtype=np.int8)
ii=np.arange(d,dtype=np.int32);rr=[];cc=[];vv=[];diag=np.zeros(d,dtype=np.int8)
for a in range(n):
 b=(a+1)%n;diag+=(dig[a]-1)*(dig[b]-1)
 for direction in (-1,1):
  ok=(dig[a]+direction>=0)&(dig[a]+direction<=2)&(dig[b]-direction>=0)&(dig[b]-direction<=2)
  jj=ii[ok];rr.append(idx[codes[ok]+direction*(3**a-3**b)]);cc.append(jj);vv.append(np.ones(len(jj),dtype=np.int8))
rr.append(ii);cc.append(ii);vv.append(diag)
H=coo_matrix((np.concatenate(vv),(np.concatenate(rr),np.concatenate(cc))),shape=(d,d)).tocsr().astype(float)
rng=np.random.default_rng(246810+10*n+m)
e,v=eigsh(H,k=1,which='SA',tol=2e-12,v0=rng.standard_normal(d))
c=np.rint(1e8*v[:,0]).astype(np.int64)
# Exact lattice-momentum projection after rounding. T is cyclic right shift of digits.
sgn=1 if m==0 else -1
rot=idx[(codes%3)*3**(n-1)+codes//3];out=np.zeros(d,dtype=np.int64);cur=np.arange(d)
for k in range(n):out+=sgn**k*c[cur];cur=rot[cur]
assert np.any(out) and np.array_equal(out[rot],sgn*out)
data={'n':n,'Sz':m,'momentum_sign':sgn,'basis':'ascending base-3 code; digit 0,1,2 means spin z -1,0,1; site 0 least significant; retain sum Sz','coefficient_scale':'arbitrary common integer normalization','coefficients':out.tolist(),'proposal_only_energy':float(e[0]),'proposal_seconds':time.time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'solver':'one smallest sparse Ritz pair; k=1, no full spectrum','cpu_limit_seconds':300,'address_space_limit_bytes':1024**3}
with gzip.open(P/f'trial_n{n}_sz{m}.json.gz','wt') as f:json.dump(data,f,separators=(',',':'))
print(json.dumps({k:v for k,v in data.items() if k!='coefficients'},indent=2))
