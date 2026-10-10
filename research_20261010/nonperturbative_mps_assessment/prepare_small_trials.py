#!/usr/bin/env python3
"""Floating proposal only. Exact verifier rebuilds H and Rayleigh quotients."""
import os, resource, json, itertools
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from pathlib import Path
P=Path(__file__).resolve().parent
for n in (6,8):
 states=[v for v in itertools.product((-1,0,1),repeat=n) if sum(v)==0];idx={v:i for i,v in enumerate(states)}
 rr=[];cc=[];vv=[]
 for j,s in enumerate(states):
  for a in range(n):
   b=(a+1)%n
   rr.append(j);cc.append(j);vv.append(s[a]*s[b])
   for direction in (-1,1):
    if -1<=s[a]+direction<=1 and -1<=s[b]-direction<=1:
     v=list(s);v[a]+=direction;v[b]-=direction
     rr.append(idx[tuple(v)]);cc.append(j);vv.append(1)
 H=coo_matrix((vv,(rr,cc)),shape=(len(states),len(states))).tocsr().astype(float)
 val,vec=eigsh(H,k=1,which='SA',tol=1e-12,v0=np.ones(len(states)))
 c=np.rint(1e9*vec[:,0]).astype(np.int64)
 (P/f'trial_n{n}.json').write_text(json.dumps({'n':n,'basis':'lexicographic spin z -1,0,1; total Sz=0','coefficients':c.tolist(),'proposal_only_eigenvalue':float(val[0])},indent=2)+'\n')
 print(n,len(states),val[0])
