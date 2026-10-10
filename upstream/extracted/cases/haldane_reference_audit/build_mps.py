"""Reconstruct Appendix C from the printed formulas, not repository matrices.
Writes integer matrices for an exact GMP contraction engine.
"""
from pathlib import Path
import numpy as np
ell = [1,1,1,1,3,3,3,5]
diag = [-289,-84,-9,33,-22,27,71,-11]
P = {(1,5):-11,(1,6):-35,(1,7):-28,(2,5):-23,(2,6):16,
     (2,7):-49,(3,5):-6,(3,6):-25,(3,7):-20,(4,5):-34,
     (4,6):9,(4,7):-32,(5,8):1,(6,8):2,(7,8):-16}
labels=[(a,d) for a,l in enumerate(ell) for d in range(-l,l+1,2)]
A={}
for s in [-1,0,1]:
    a=np.zeros((26,26),dtype=object)
    for i,(alpha,d) in enumerate(labels):
        l=ell[alpha];r=(d+l)//2
        for j,(beta,e) in enumerate(labels):
            k=ell[beta]
            if e!=d+2*s or abs(k-l)>2 or (k==l and alpha!=beta):continue
            if k==l+2:
                p=P[(alpha+1,beta+1)]
                f={-1:2*(l+1-r)*(l+2-r),0:2*(r+1)*(l-r+1),1:(r+1)*(r+2)}[s]
            elif k==l:
                p=diag[alpha]; f={-1:2*(l-r+1),0:d,1:-(r+1)}[s]
            else:
                p=-P[(beta+1,alpha+1)]; f={-1:2,0:-2,1:1}[s]
            a[i,j]=int(p*f)
    A[s]=a
T=sum((np.kron(a,a) for a in A.values()),np.zeros((676,676),dtype=object))
B={(s,t):A[s]@A[t] for s in A for t in A}
O=np.zeros((676,676),dtype=object)
for (s,t),b in B.items():
    if s*t:O+=s*t*np.kron(b,b)
for s in [-1,0]:
    for t in [0,1]:
        O+=np.kron(B[s,t],B[s+1,t-1])+np.kron(B[s+1,t-1],B[s,t])
diffs=np.array([d-e for _,d in labels for _,e in labels])
assert all(T[diffs[:,None]!=diffs[None,:]]==0)
assert all(O[diffs[:,None]!=diffs[None,:]]==0)
blocks={delta:np.flatnonzero(diffs==delta) for delta in sorted(set(diffs))}
assert [len(i) for i in blocks.values()]==[1,8,32,80,136,162,136,80,32,8,1]
out=Path(__file__).parent
with (out/'mps_blocks.txt').open('w') as f:
    f.write(f'{len(blocks)}\n')
    for delta,ids in blocks.items():
        f.write(f'{delta} {len(ids)}\n')
        for M in (T,O):
            for row in M[np.ix_(ids,ids)]:f.write(' '.join(map(str,row))+'\n')
print('Reconstructed all matrices and verified difference-block decomposition.')
