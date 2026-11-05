"""NUMERICAL (float64): full spectrum of periodic ring H_L = sum_i h(i,i+1) for L=2 (two bonds) .. 7, by Sz sector.
Saves eigenvalues with multiplicity weights (Sz>0 sectors counted twice)."""
import numpy as np, sys, time
from ed import bond, sector, ham
model=sys.argv[1]; alpha=float(sys.argv[2]); L=int(sys.argv[3])
h=bond(model,alpha); ev=[]; w=[]; t=time.time()
for M in range(0,2*L+1):
    st=sector(L,M)
    if L==2:
        H=2*ham(2,st,h)/2   # ham() with L=2 adds bond (0,1) and (1,0): two bonds -> already 2 terms
    else:
        H=ham(L,st,h)
    e=np.linalg.eigvalsh(H.toarray()); ev.append(e); w.append(np.full(len(e),1 if M==0 else 2))
ev=np.concatenate(ev); w=np.concatenate(w)
assert abs(w.sum()-5**L)<0.5
np.savez(f'spec_{model}_{alpha:g}_L{L}.npz',ev=ev,w=w)
print(L,'E0',ev.min(),'time',time.time()-t)
