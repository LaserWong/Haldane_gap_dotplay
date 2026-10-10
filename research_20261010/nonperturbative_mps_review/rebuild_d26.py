#!/usr/bin/env python3
"""Construct physical MPS matrices and insertion independently from archived parameters."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from pathlib import Path
import itertools as it, json, hashlib, time
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];t0=time.time()
mult=[1,1,1,1,3,3,3,5]
d=[-289,-84,-9,33,-22,27,71,-11]
cross=[[-11,-35,-28],[-23,16,-49],[-6,-25,-20],[-34,9,-32]]
edge={(a,b):cross[a][b-4] for a in range(4) for b in range(4,7)}
edge.update({(4,7):1,(5,7):2,(6,7):-16})
labels=[(a,m) for a,l in enumerate(mult) for m in range(-l,l+1,2)]
A=[]
for physical in [-1,0,1]:
 M=np.zeros((26,26),dtype=object)
 for row,(a,m) in enumerate(labels):
  for col,(b,k) in enumerate(labels):
   if k-m!=2*physical:continue
   la,lb=mult[a],mult[b];r=(la+m)//2
   if a==b:
    value={-1:2*(la-r+1),0:m,1:-r-1}[physical]*d[a]
   elif (a,b) in edge:
    value={-1:2*(la+1-r)*(la+2-r),0:2*(r+1)*(la-r+1),1:(r+1)*(r+2)}[physical]*edge[a,b]
   elif (b,a) in edge:
    value={-1:2,0:-2,1:1}[physical]*(-edge[b,a])
   else:continue
   M[row,col]=value
 A.append(M)
# Physical spin-one interaction in the orthonormal z basis. Matrix entries
# follow from Sz Sz + (S+ S- + S- S+)/2.
h=np.zeros((9,9),dtype=object)
for x,y in it.product(range(3),repeat=2):
 h[3*x+y,3*x+y]=(x-1)*(y-1)
 for shift in [-1,1]:
  if 0<=x+shift<3 and 0<=y-shift<3:h[3*(x+shift)+y-shift,3*x+y]=1
assert np.array_equal(h,h.T) and sum(h[i,i] for i in range(9))==0
word=[A[x]@A[y] for x,y in it.product(range(3),repeat=2)]
pairs=list(it.product(range(26),repeat=2))
groups={}
for flat,(x,y) in enumerate(pairs):groups.setdefault(labels[x][1]-labels[y][1],[]).append(flat)
T=sum((np.kron(m,m) for m in A),np.zeros((676,676),dtype=object))
O=np.zeros((676,676),dtype=object)
for bra,ket in it.product(range(9),repeat=2):
 if h[bra,ket]:O+=h[bra,ket]*np.kron(word[bra],word[ket])
sector=[labels[x][1]-labels[y][1] for x,y in pairs]
assert all(not T[i,j] and not O[i,j] for i in range(676) for j in range(676) if sector[i]!=sector[j])
with (P/'d26_rebuilt_blocks.txt').open('w') as f:
 f.write(str(len(groups))+'\n')
 for delta,ids in sorted(groups.items()):
  f.write(f'{delta} {len(ids)}\n')
  for M in [T,O]:
   for row in M[np.ix_(ids,ids)]:f.write(' '.join(map(str,row))+'\n')
assert (P/'d26_rebuilt_blocks.txt').read_bytes()==(R/'audit/mps/mps_blocks.txt').read_bytes()
# A direct amplitude expansion at L=2,3 independently checks norm and H insertion.
checks=[]
for L in [2,3]:
 states=list(it.product(range(3),repeat=L));loc={v:i for i,v in enumerate(states)}
 vec=[]
 for v in states:
  prod=np.eye(26,dtype=object)
  for x in v:prod=prod@A[x]
  vec.append(sum(prod[i,i] for i in range(26)))
 norm=sum(x*x for x in vec);energy=0
 for j,v in enumerate(states):
  for a in range(L):
   b=(a+1)%L
   for pair in range(9):
    x,y=divmod(pair,3);z=h[pair,3*v[a]+v[b]]
    if z:
     w=list(v);w[a],w[b]=x,y
     energy+=vec[j]*z*vec[loc[tuple(w)]]
 # The whole-chain scalar is compared to a separate block contraction.
 n2=0;e2=0
 for ids in groups.values():
  tb=T[np.ix_(ids,ids)];ob=O[np.ix_(ids,ids)]
  tn=np.linalg.matrix_power(tb,L)
  tm=np.linalg.matrix_power(tb,L-2)
  n2+=sum(tn[i,i] for i in range(len(ids)))
  mo=tm@ob;e2+=L*sum(mo[i,i] for i in range(len(ids)))
 assert norm==n2 and energy==e2
 checks.append({'L':L,'norm':str(norm),'total_H_numerator':str(energy),'parallel_bonds_at_L2':L==2})
result={'status':'PASS','block_sizes':[len(v) for _,v in sorted(groups.items())],'direct_amplitude_checks':checks,'rebuilt_blocks_sha256':hashlib.sha256((P/'d26_rebuilt_blocks.txt').read_bytes()).hexdigest(),'seconds':time.time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'d26_rebuild_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
