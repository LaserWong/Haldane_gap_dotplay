"""Independent exact-integer heat-kernel checks using ALL physical columns.
Does not use the manuscript's orbit representatives or cached column totals.
Checks A: n=6, twists I/P/C; B: n=4,5,6, twists I/P.
Finite exponential enclosures use the error estimates proved in Appendices A/B.
"""
from fractions import Fraction as F
from math import factorial, isqrt
from itertools import product
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix, bmat

a=F(700741,500000)
CENTERS_A={(6,'I'):8945303,(6,'P'):346734,(6,'C'):939987}
CENTERS_B={(4,'I'):124885379,(4,'P'):65757,(5,'I'):2925,(5,'P'):2960742,(6,'I'):12870614,(6,'P'):286599}

def polynomial_coefficients(mu,J,Q):
    fac=factorial(J)
    v=[mu**j*(fac//factorial(j)) for j in range(J+1)]
    den=sum(v)
    return [Q*x//den for x in v]

def thermal(n,twist,appendix):
    isa=appendix=='A'
    Q=2**(56 if isa else 55); J=256 if isa else 280
    coeff=polynomial_coefficients(84 if isa else 98,J,Q)
    kmax=max(j for j,x in enumerate(coeff) if x)
    den=16 if isa else 32
    groups={}
    for w in product([-1,0,1],repeat=n):groups.setdefault(sum(w),[]).append(w)
    total=0
    for words in groups.values():
        d=len(words); index={w:i for i,w in enumerate(words)}
        rr=[];cc=[];aa=[];bb=[]
        for j,w in enumerate(words):
            diag=sum(w[k-1]*w[k] for k in range(n))
            rr.append(j);cc.append(j);aa.append((16-3*n//2-diag) if isa else (32-3*n-2*diag));bb.append(0)
            for k in range(n):
                l=(k+1)%n
                for step in [-1,1]:
                    v=list(w);v[k]-=step;v[l]+=step
                    if not(-1<=v[k]<=1 and -1<=v[l]<=1):continue
                    i=index[tuple(v)]
                    # Physical seam factor is exp(i theta (column_0-row_0)).
                    power=(w[0]-v[0]) if l==0 else 0
                    if twist=='C' and power:
                        ar,bi=((0,-1) if power==1 else (1,1)) # -omega^{power}
                    else:
                        ar=(-1 if isa else -2)*(-1 if twist=='P' and power else 1);bi=0
                    rr.append(i);cc.append(j);aa.append(ar);bb.append(bi)
        A=csr_matrix((np.array(aa,dtype=np.int64),(rr,cc)),shape=(d,d))
        if twist=='C':
            B=csr_matrix((np.array(bb,dtype=np.int64),(rr,cc)),shape=(d,d))
            M=bmat([[A,-B],[B,A-B]],format='csr'); X=np.zeros((2*d,d),dtype=np.int64)
        else:
            M=A;X=np.zeros((d,d),dtype=np.int64)
        # Conservative no-overflow bound for every sparse partial sum.
        err=(257*(2*isqrt(3**n)+3)) if isa else 281*(isqrt(3**n)+2)
        compbound=(2 if twist=='C' else 1)*(Q+err)
        rowsum=int(np.max(np.asarray(abs(M).sum(axis=1))))
        assert rowsum*compbound < 2**63
        ids=np.arange(d)
        for j in range(kmax,-1,-1):
            X=(M@X)//den
            X[ids,ids]+=coeff[j]
        U=X[:d].astype(object)
        if twist=='C':
            V=X[d:].astype(object);total+=int(np.sum(U*U-U*V+V*V))
        else:total+=int(np.sum(U*U))
    b=F(21,2) if isa else F(49,4)
    x=b*n*(F(3,2)-a)
    s=sum((x**j/F(factorial(j)) for j in range(101)),F(0))
    if isa:
        # A.8: error in scaled norm <4e-7; norm upper <4.
        upper=s+2*x**101/F(factorial(101))
        val_lo=s*total/F(Q*Q);val_hi=upper*total/F(Q*Q)
        assert val_hi<16
        normerr=F(4,10**7)
        traceerr=(8+normerr)*normerr
        lo=val_lo-traceerr;hi=val_hi+traceerr
        c=F(CENTERS_A[n,twist],10**6);tol=F(1,10**5)
    else:
        dn=isqrt(3**n)+1;En=281*(dn+1)+1;err=dn*En;r=isqrt(total)
        lo=s*max(0,r-err)**2/F(Q*Q)
        hi=(s+x**100/F(factorial(100)))*(r+1+err)**2/F(Q*Q)
        c=F(CENTERS_B[n,twist],10**6);tol=F(30,10**6)
    assert c-tol<lo<=hi<c+tol,(appendix,n,twist,float(lo),float(hi))
    print(f'{appendix} n={n} twist={twist}: [{float(lo):.12f}, {float(hi):.12f}], published interval PASS',flush=True)

if __name__=='__main__':
    for n,g in CENTERS_A:thermal(n,g,'A')
    for n,g in CENTERS_B:thermal(n,g,'B')
    print('PASS: 9 independent finite thermal enclosures; NOT all 27 inputs.')
