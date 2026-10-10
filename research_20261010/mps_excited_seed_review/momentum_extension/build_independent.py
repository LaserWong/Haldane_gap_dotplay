#!/usr/bin/env python3
"""Single-site Heisenberg-channel transfers and independently expanded fixtures."""
import os,resource,time,json,itertools
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
from pathlib import Path
from collections import defaultdict
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time();I=P/'inputs'
d=json.loads((I/'local_tensors.json').read_text());A=[np.array(a,dtype=object) for a in d['A']];B=[np.zeros((26,26),dtype=object),A[0],A[1]]
q=[i[1]-j[1] for i in d['labels'] for j in d['labels']]
Id=np.eye(3,dtype=object);Z=np.diag([-1,0,1]).astype(object);Rp=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);Rm=Rp.T
ops=[Id,Z,Rp,Rm];ds=[0,0,1,-1]
def sparse(a):return [(i,j,int(a[i,j])) for i,j in itertools.product(range(26),repeat=2) if a[i,j]]
def outer(target,a,b,coeff):
 if not coeff:return
 for i,j,x in sparse(a):
  for k,l,y in sparse(b):target[(26*i+k,26*j+l)]+=coeff*x*y
transfers=[]
for bra,ket in itertools.product(range(2),repeat=2):
 for op in ops:
  x=defaultdict(int)
  for s,t in itertools.product(range(3),repeat=2):outer(x,(A,B)[bra][s],(A,B)[ket][t],int(op[s,t]))
  transfers.append({ij:v for ij,v in x.items() if v})
with (P/'single_site_sources.txt').open('w') as f:
 f.write(' '.join(map(str,q))+'\n')
 for z,M in enumerate(transfers):
  pair,op=divmod(z,4);bra,ket=divmod(pair,2);shift=ds[op]-bra+ket
  assert all(q[j]-q[i]==2*shift for i,j in M)
  f.write(f'{shift} {len(M)}\n')
  for (i,j),v in sorted(M.items()):f.write(f'{i} {j} {v}\n')
# Independently reconstruct all frozen E/O matrices, explicitly from physical h.
h=np.kron(Z,Z)+np.kron(Rp,Rm)+np.kron(Rm,Rp)
words=iter((I/'sources_plus.txt').read_text().split());assert int(next(words))==1;assert [int(next(words)) for _ in range(676)]==q
expected=[transfers[4*k] for k in range(4)]
for bra,ket in itertools.product(range(3),repeat=2):
 M=defaultdict(int)
 for s,t,x,y in itertools.product(range(3),repeat=4):
  c=int(h[3*s+t,3*x+y])
  if c:
   U=(B[s] if bra==1 else A[s])@(B[t] if bra==2 else A[t]);V=(B[x] if ket==1 else A[x])@(B[y] if ket==2 else A[y]);outer(M,U,V,c)
 expected.append({ij:v for ij,v in M.items() if v})
for M in expected:
 nz=int(next(words));got={(int(next(words)),int(next(words))):int(next(words)) for _ in range(nz)};assert got==M
assert next(words,None) is None
fixtures=[]
for n in [2,4,6]:
 psi={}
 for w in itertools.product(range(3),repeat=n):
  p=np.eye(26,dtype=object)
  for s in w:p=p@A[s]
  a=int(np.trace(p))
  if a:psi[w]=a
 vecs=[];hvecs=[]
 for site in range(n):
  v={}
  for w,a in psi.items():
   if w[site]<2:
    target=w[:site]+(w[site]+1,)+w[site+1:];v[target]=a
  hv=defaultdict(int)
  for w,a in v.items():
   for j in range(n):
    k=(j+1)%n
    for s,t in itertools.product(range(3),repeat=2):
     c=int(h[3*s+t,3*w[j]+w[k]])
     if c:
      target=list(w);target[j]=s;target[k]=t;hv[tuple(target)]+=c*a
  vecs.append(v);hvecs.append(hv)
 C=[sum(a*vecs[r].get(w,0) for w,a in vecs[0].items()) for r in range(n)]
 K=[sum(a*hvecs[r].get(w,0) for w,a in vecs[0].items()) for r in range(n)]
 fixtures.append({'n':n,'C':list(map(str,C)),'K':list(map(str,K))})
assert fixtures==json.loads((I/'source_checks_plus.json').read_text())['fixtures']
out={'status':'PASS','producer_local_matrices_verified':13,'independent_single_site_transfer_count':16,'fixtures':fixtures,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_build.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
