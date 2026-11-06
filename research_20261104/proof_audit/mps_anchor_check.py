#!/usr/bin/env python3
"""Independent exact recomputation of the D26 trial-state norms/energies with FLINT fmpz_mat.
Uses ONLY the tensor definition (ells/diag/pair, copied from rebuild_d26.py) and the definition
psi(s1..sL)=Tr(A_s1...A_sL). No block decomposition, no producer/reviewer contraction code.
N_L=<psi|psi>=Tr(T^L), H_L=<psi|H|psi>=L*Tr(T^(L-2) O) (translation invariance)."""
import itertools, re, sys, time, json
from fractions import Fraction as F
from pathlib import Path
from flint import fmpz_mat, fmpz
ells=[1,1,1,1,3,3,3,5];diag=[-289,-84,-9,33,-22,27,71,-11]
pair={(0,4):-11,(0,5):-35,(0,6):-28,(1,4):-23,(1,5):16,(1,6):-49,(2,4):-6,(2,5):-25,(2,6):-20,(3,4):-34,(3,5):9,(3,6):-32,(4,7):1,(5,7):2,(6,7):-16}
labels=[(a,m) for a,l in enumerate(ells) for m in range(-l,l+1,2)]
A={s:[[0]*26 for _ in range(26)] for s in (-1,0,1)}
for i,(a,m) in enumerate(labels):
    ell=ells[a];r=(ell+m)//2
    for j,(b,k) in enumerate(labels):
        s=(k-m)//2
        if s not in A or k-m!=2*s:continue
        if a==b:val=diag[a]*({-1:2*(ell-r+1),0:m,1:-(r+1)}[s])
        elif (a,b) in pair:val=pair[a,b]*({-1:2*(ell+1-r)*(ell+2-r),0:2*(r+1)*(ell-r+1),1:(r+1)*(r+2)}[s])
        elif (b,a) in pair:val=-pair[b,a]*({-1:2,0:-2,1:1}[s])
        else:continue
        A[s][i][j]=val
M={s:fmpz_mat(A[s]) for s in A}
# two-site S.S in the m basis: diag s*t; flips with coefficient 1 (spin-1 ladder elements sqrt2*sqrt2/2)
def h(s,t,u,v):
    if (s,t)==(u,v): return s*t
    return 1 if (s+t==u+v and abs(s-u)==1) else 0
def kron(X,Y):
    n=X.nrows();Z=fmpz_mat(n*n,n*n)
    for i in range(n):
        for k in range(n):
            x=X[i,k]
            if x==0:continue
            for j in range(n):
                for l in range(n):
                    y=Y[j,l]
                    if y!=0: Z[i*n+j,k*n+l]+=x*y
    return Z
t0=time.time()
T=fmpz_mat(676,676)
for s in M: T+=kron(M[s],M[s])
O=fmpz_mat(676,676)
for s,t,u,v in itertools.product((-1,0,1),repeat=4):
    c=h(s,t,u,v)
    if c: O+=c*kron(M[s]*M[t],M[u]*M[v])
print('built',time.time()-t0,flush=True)
def tr(X):return sum((X[i,i] for i in range(X.nrows())),fmpz(0))
def trprod(X,Y):  # Tr(XY)
    n=X.nrows();s=fmpz(0)
    XT=X.entries();YT=Y.transpose().entries()
    return sum((a*b for a,b in zip(XT,YT)),fmpz(0))
res={}
P={1:T}
cur=T
for k in range(2,34):
    cur=cur*T;P[k]=cur
    print('power',k,time.time()-t0,flush=True)
for L in range(4,34):
    res[L]=(int(L*trprod(P[L-2],O)),int(tr(P[L])))
# 48: Tr(T^48)=Tr(T^33 T^15); Tr(T^46 O)=Tr(T^33 (T^13 O))
res[48]=(int(48*trprod(P[33],P[13]*O)),int(trprod(P[33],P[15])))
X=P[33]*O
res[68]=(int(68*trprod(P[33],X)), int(trprod(P[33]*T,P[33]*T)))  # H: Tr(T^66 O)=Tr(T^33 T^33 O); N: Tr(T^34 T^34)
res[60]=(int(60*trprod(P[25],X)),int(trprod(P[27],P[33])))     # Tr(T^58 O)=Tr(T^25 T^33 O)
res[64]=(int(64*trprod(P[29],X)),int(trprod(P[31],P[33])))
print('done',time.time()-t0,flush=True)
json.dump({str(k):[str(a),str(b)] for k,(a,b) in res.items()},open('mps_anchor_values.json','w'),indent=1)
