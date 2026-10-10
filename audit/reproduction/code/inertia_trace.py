"""Exact spectral counting via fraction-free symmetric elimination, without ED.
Spin-2 L=4 Heisenberg example. The retained low energies are also derived
independently by angular-momentum addition for the four-site ring.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
import numpy as np
from exact_heat_trace import exact_rows,L,D
from analytic_certificates import exp_bounds
OUT=Path(__file__).resolve().parents[1]/'results'

def inertia(A):
    A=A.copy().astype(object)
    n=len(A)
    prev=1
    negative=0
    for k in range(n):
        if A[k,k]==0:
            options=[i for i in range(k,n) if A[i,i]!=0]
            if options:
                j=options[0]
                A[[k,j],:]=A[[j,k],:]
                A[:,[k,j]]=A[:,[j,k]]
            else:
                nz=[(i,j) for i in range(k,n) for j in range(i+1,n) if A[i,j]!=0]
                if not nz:
                    return negative,n-k
                i,j=nz[0]
                A[i,:]+=A[j,:]
                A[:,i]+=A[:,j]
                A[[k,i],:]=A[[i,k],:]
                A[:,[k,i]]=A[:,[i,k]]
        p=int(A[k,k])
        negative+=int(p*prev<0)
        if k+1<n:
            B=p*A[k+1:,k+1:]-np.outer(A[k+1:,k],A[k,k+1:])
            assert all(int(x)%prev==0 for x in B.flat)
            A[k+1:,k+1:]=B//prev
        prev=p
    return negative,0

def count(cut):
    cut=F(cut)
    count_total=0
    blocks=[]
    for M in range(2*L+1):
        rows=exact_rows(M)
        n=len(rows)
        H2=np.zeros((n,n),dtype=object)
        for r,row in enumerate(rows):
            for c,v in row.items():
                H2[r,c]=-v
            H2[r,r]+=8*L
        weights=[]
        for idx in range(D):
            a=[(idx//5**j)%5 for j in range(L)]
            if sum(a)==2*L+M:
                denom=1
                for b in a:
                    denom*=comb(4,b)
                assert 12**L%denom==0
                weights.append(12**L//denom)
        A=cut.denominator*H2
        for i in range(n):
            A[i,i]-=2*cut.numerator
            A[i,:]*=weights[i]
        assert np.array_equal(A,A.T)
        neg,zero=inertia(A)
        assert zero==0
        mult=1 if M==0 else 2
        count_total+=mult*neg
        blocks.append(dict(M=M,dimension=n,negative=neg,multiplicity=mult))
    return dict(cut=str(cut),count_below=count_total,blocks=blocks)

def main():
    rows=[count(c) for c in ['-41/2','-39/2','-37/2','-33/2','-31/2']]
    assert [r['count_below'] for r in rows]==[0,1,4,9,9]
    beta=F(8)
    # H4=(S1+S3).(S2+S4): the first levels have E=-20,-19,-17.
    qlo=F(1)
    qhi=F(1)
    for Edeg,mult in [(1,3),(3,5)]:
        lo,hi=exp_bounds(-beta*Edeg)
        qlo+=mult*lo
        qhi+=mult*hi
    tail=(D-9)*exp_bounds(-beta*F(9,2))[1]
    result=dict(status='exact_fraction_free_inertia_and_rational_tail',
                model='spin-2 Heisenberg periodic L=4',counts=rows,
                retained_levels=[[-20,1],[-19,3],[-17,5]],beta='8',cut='-31/2',
                omitted_count=D-9,relative_tail_upper=str(tail/qlo),
                relative_tail_upper_display=float(tail/qlo),
                shifted_Z_lower=str(qlo),shifted_Z_upper=str(qhi+tail),
                note='The retained levels use an analytic Casimir decomposition. Spectral completeness below the cutoff is independently certified by inertia.')
    (OUT/'inertia_tail_certificate.json').write_text(json.dumps(result,indent=2))
    print('exact inertia counts',[r['count_below'] for r in rows],
          'relative tail',float(tail/qlo),flush=True)

if __name__=='__main__':
    main()
