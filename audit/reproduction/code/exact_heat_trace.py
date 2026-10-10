"""No eigensolver: exact integer power traces and rational exponential remainder.
Spin-2, four-site Heisenberg periodic ring, inverse temperatures 1 and 2.
The unnormalized spin basis is diagonally similar to the Hermitian basis.
Every accepted enclosure is calculated with integers and Fraction.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import time
import numpy as np
from analytic_certificates import exp_bounds

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'results'
L=4
D=5**L
K=200

def exact_rows(M):
    # B = 8 L I - 2 H has spectrum in [0,20 L].
    states=[]
    digits=[]
    for i in range(D):
        a=[(i//5**j)%5 for j in range(L)]
        if sum(a)==2*L+M:
            states.append(i)
            digits.append(a)
    lookup={i:j for j,i in enumerate(states)}
    rows=[{} for _ in states]
    for c,(idx,a) in enumerate(zip(states,digits)):
        diag=8*L
        for j in range(L):
            k=(j+1)%L
            diag-=2*(a[j]-2)*(a[k]-2)
            if a[j]<4 and a[k]>0:
                r=lookup[idx+5**j-5**k]
                rows[r][c]=rows[r].get(c,0)-(4-a[j])*a[k]
            if a[j]>0 and a[k]<4:
                r=lookup[idx-5**j+5**k]
                rows[r][c]=rows[r].get(c,0)-a[j]*(4-a[k])
        rows[c][c]=rows[c].get(c,0)+diag
    return rows

def moments():
    path=OUT/'integer_heat_trace_moments.json'
    if path.exists():
        return [int(a) for a in json.loads(path.read_text())['moments']]
    total=[0]*(K+1)
    t=time.time()
    dims=[]
    for M in range(2*L+1):
        rows=exact_rows(M)
        n=len(rows)
        P=np.eye(n,dtype=object)
        mult=1 if M==0 else 2
        dims.append(n*mult)
        for k in range(K+1):
            tr=sum(P[i,i] for i in range(n))
            assert tr>=0
            total[k]+=mult*tr
            if k==K:
                break
            Q=np.zeros((n,n),dtype=object)
            for r,row in enumerate(rows):
                for c,v in row.items():
                    Q[r,:]+=v*P[c,:]
            P=Q
        print('integer block',M,n,'elapsed',time.time()-t,flush=True)
    assert sum(dims)==D and total[0]==D
    path.write_text(json.dumps(dict(L=L,K=K,dimension=D,moments=[str(a) for a in total]),indent=2))
    return total

def certificate(beta,mu):
    beta=F(beta)
    x=beta*10*L
    assert x<K+2
    # exp(-beta H) = exp(-4 beta L) exp((beta/2) B).
    coeff=F(1)
    series=F(mu[0])
    for k in range(1,K+1):
        coeff*=beta/F(2*k)
        series+=coeff*mu[k]
    rem=D*x**(K+1)/F(math.factorial(K+1))/(1-x/F(K+2))
    el,eu=exp_bounds(-4*beta*L)
    lower=el*series
    upper=eu*(series+rem)
    rel=(upper-lower)/lower
    assert rel<F(1,10**15)
    return dict(beta=str(beta),Z_lower=str(lower),Z_upper=str(upper),
                Z_lower_display=float(lower),Z_upper_display=float(upper),
                relative_interval_width_upper=str(rel),relative_width_display=float(rel),
                polynomial_degree=K,finite_dimension=D,status='exact_integer_and_rational_certificate')

def main():
    mu=moments()
    rows=[certificate(b,mu) for b in [1,2]]
    # ED comparison is strictly downstream, and does not enter the certificate.
    path=OUT/'spec_heis_s2_L4.npz'
    if path.exists():
        e=np.load(path)['energies']
        for row in rows:
            b=float(F(row['beta']))
            z=float(np.sum(np.exp(-b*e)))
            row['independent_float_ED_value']=z
            row['ED_relative_discrepancy_display']=abs(z/row['Z_lower_display']-1)
    (OUT/'exact_heat_trace_certificate.json').write_text(json.dumps(rows,indent=2))
    for r in rows:
        print({k:v for k,v in r.items() if not ('lower' in k or 'upper' in k) or 'display' in k},flush=True)

if __name__=='__main__':
    main()
