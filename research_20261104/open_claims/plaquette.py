# Claim A2: plaquette inclusion-exclusion W(g)=sum_{F subset of square edges}(-1)^{4-|F|} E0(F) = -15/32 g^4 + O(g^5)
# spin-1/2 square bilayer (rung exchange 1, in-plane exchange g on both layers), 4 rungs = 8 spins.
# Part 1 (EXACT): Rayleigh-Schroedinger coefficients of E0(F) through g^4, exact rationals (Fraction).
# Part 2 (NUMERICAL ONLY): W(g)/g^4 at g=0.0125,0.025,0.05,0.1 by 60-digit mpmath diagonalization of the Sz=0 block.
import itertools, json
from fractions import Fraction as Fr
import numpy as np
N=8  # spin index: rung r (corners in cyclic order), layer l -> 2*r+l
edges=[(0,1),(1,2),(2,3),(3,0)]
def bonds(F): return [(2*a+l,2*b+l) for (a,b) in F for l in (0,1)]
rungs=[(2*r,2*r+1) for r in range(4)]
def apply_SS(i,j,st):
    si=(st>>i)&1; sj=(st>>j)&1; out={st:(Fr(1,4) if si==sj else Fr(-1,4))}
    if si!=sj: out[st^(1<<i)^(1<<j)]=Fr(1,2)
    return out
def apply(bl,vec):
    out={}
    for st,c in vec.items():
        for (i,j) in bl:
            for t,v in apply_SS(i,j,st).items(): out[t]=out.get(t,0)+c*v
    return {k:v for k,v in out.items() if v!=0}
# orthogonal (unnormalized) rung basis T+, T0, S, T-  with norms^2 1,2,2,1 ; H0 diagonal there
rb=[{0b00:1},{0b01:1,0b10:1},{0b01:1,0b10:-1},{0b11:1}]
rnorm=[1,2,2,1]; rE=[Fr(1,4),Fr(1,4),Fr(-3,4),Fr(1,4)]
basis=list(itertools.product(range(4),repeat=4))
def tovec(lab):
    vec={0:1}
    for r,k in enumerate(lab):
        nv={}
        for st,c in vec.items():
            for loc,cc in rb[k].items():
                t=st|((loc&1)<<(2*r))|(((loc>>1)&1)<<(2*r+1)); nv[t]=nv.get(t,0)+c*cc
        vec=nv
    return vec
bvec=[tovec(l) for l in basis]; bnorm=[int(np.prod([rnorm[k] for k in l])) for l in basis]; bE=[sum(rE[k] for k in l) for l in basis]
def coords(vec):
    return {i:Fr(sum(c*vec.get(st,0) for st,c in bv.items()))/bnorm[i] for i,bv in enumerate(bvec) if any(st in vec for st in bv)}
gs=basis.index((2,2,2,2)); E0=bE[gs]; assert E0==-3
def Vmat(F):
    bl=bonds(F); return {i:{k:v for k,v in coords(apply(bl,bvec[i])).items() if v!=0} for i in range(256)}
def mul(M,x):
    out={}
    for i,c in x.items():
        for k,v in M[i].items(): out[k]=out.get(k,0)+c*v
    return {k:v for k,v in out.items() if v!=0}
def ip(x,y): return sum(c*y.get(k,0)*bnorm[k] for k,c in x.items())
def Rop(x): return {k:c/(E0-bE[k]) for k,c in x.items() if k!=gs}
def coefs(F):
    if not F: return Fr(0),Fr(0),Fr(0),Fr(0)
    M=Vmat(F); p0={gs:Fr(1)}; n0=ip(p0,p0)
    E1=ip(p0,mul(M,p0))/n0
    a=Rop(mul(M,p0)); E2=ip(p0,mul(M,a))/n0
    E3=ip(a,mul(M,a))/n0 - E1*ip(a,a)/n0
    assert E1==0
    b=Rop(mul(M,a))
    E4=ip(a,mul(M,b))/n0 - E2*ip(a,a)/n0   # standard RS 4th order with E1=0 (V,R real symmetric)
    return E1,E2,E3,E4
res={};Wc=[Fr(0)]*4
for k in range(5):
    for F in itertools.combinations(edges,k):
        c=coefs(list(F)); s=(-1)**(4-k)
        Wc=[w+s*x for w,x in zip(Wc,c)]; res[str(F)]=[str(x) for x in c]
print('EXACT coefficients of W(g): g^1',Wc[0],' g^2',Wc[1],' g^3',Wc[2],' g^4',Wc[3],'| equals -15/32:',Wc[3]==Fr(-15,32))
print('single-edge E2 =',res[str(((0,1),))][1],' E4 =',res[str(((0,1),))][3])
import mpmath as mp; mp.mp.dps=60
sz0=[s for s in range(256) if bin(s).count('1')==4]; idx={s:i for i,s in enumerate(sz0)}
def Hm(bl):
    M=mp.zeros(len(sz0))
    for s in sz0:
        for (i,j) in bl:
            for t,v in apply_SS(i,j,s).items(): M[idx[t],idx[s]]+=mp.mpf(v.numerator)/v.denominator
    return M
H0=Hm(rungs); Ve={e:Hm(bonds([e])) for e in edges}; num={}
for gstr in ['0.0125','0.025','0.05','0.1']:
    g=mp.mpf(gstr); W=mp.mpf(0)
    for k in range(5):
        for F in itertools.combinations(edges,k):
            H=H0.copy()
            for e in F: H+=g*Ve[e]
            W+=(-1)**(4-k)*min(mp.eigsy(H,eigvals_only=True))
    num[gstr]=mp.nstr(W/g**4,12); print('NUMERICAL g=',gstr,' W/g^4 =',num[gstr],flush=True)
json.dump({'exact_W_coeffs_g1_to_g4':[str(x) for x in Wc],'per_subset_E1_E2_E3_E4':res,'numerical_W_over_g4_60digit':num},open('plaquette.json','w'),indent=1)
