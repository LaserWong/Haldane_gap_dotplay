"""NUMERICAL necessary-condition test for Z_L = Tr X^L with X real self-adjoint (all L>=2):
Hamburger Hankel H_ij = Z_{i+j}, i,j>=1, must be PSD. Uses shifted energies (shift-invariant test up to scaling by e^{-beta a L}:
PSD of [Z_{i+j} e^{-beta a (i+j)}] equals PSD of [Z_{i+j}] by congruence with diag(e^{-beta a i}))."""
import numpy as np, sys, glob
from mpmath import mp, mpf, exp, matrix, eigsy
mp.dps=50
model,alpha=sys.argv[1],sys.argv[2]
Ls=sorted(int(f.split('_L')[1].split('.')[0]) for f in glob.glob(f'spec_{model}_{alpha}_L*.npz'))
spec={L:np.load(f'spec_{model}_{alpha}_L{L}.npz') for L in Ls}
print('L available',Ls)
for beta in [0.5,1,2,4,8,16,32]:
    Z={}
    for L in Ls:
        ev,w=spec[L]['ev'],spec[L]['w']; e0=ev.min()
        Z[L]=sum(mpf(int(wi))*exp(-beta*(mpf(float(e))-mpf(float(e0)))) for e,wi in zip(ev,w))*exp(-beta*mpf(float(e0)))
    Lm=max(Ls); n=(Lm)//2
    for m in range(2,n+1):
        H=matrix(m,m)
        for i in range(m):
            for j in range(m): H[i,j]=Z[i+j+2]
        # normalize by diag for conditioning
        D=[1/mp.sqrt(H[i,i]) for i in range(m)]
        for i in range(m):
            for j in range(m): H[i,j]*=D[i]*D[j]
        E=eigsy(H,eigvals_only=True)
        print(f'beta={beta} Hankel size {m} (Z_2..Z_{2*m}) min eig {mp.nstr(min(E),8)}')
