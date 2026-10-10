#!/usr/bin/env python3
"""Exact positive Chebyshev coefficients from a finite Poisson convolution."""
import json,math,time
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
Q=2**56;MU=256;LAM=MU//2;J=320
def prepare():
    t=time.monotonic();fac=math.factorial(J)
    weights=[fac]
    for j in range(1,J+1):weights.append(weights[-1]*LAM//j)
    assert weights==[LAM**j*(fac//math.factorial(j)) for j in range(J+1)]
    s=sum(weights);den=s*s
    b=[(1 if k==0 else 2)*sum(weights[j]*weights[j+k] for j in range(J+1-k)) for k in range(J+1)]
    assert sum(b)==den
    tail=den;K=None
    for k,v in enumerate(b):
        tail-=v
        if F(tail,den)<F(1,4*Q):K=k;break
    # Poisson tail probability <= unnormalized tail / finite positive sum.
    tau=F(LAM**(J+1),math.factorial(J+1))/(1-F(LAM,J+2))/F(s,fac)
    assert 4*tau<F(1,4*Q)
    coeff=[Q*x//den for x in b[:K+1]]
    assert sum(coeff)<=Q
    kmax=max(k for k,c in enumerate(coeff) if c)
    weighted_error=F(sum(c*k*(k+1)//2 for k,c in enumerate(coeff)),Q)
    bound=4*tau+F(tail,den)
    assert bound<F(1,Q)
    (ROOT/'coefficients_mu256_Q56.txt').write_text(''.join(str(c)+'\n' for c in coeff))
    result={'mu':MU,'poisson_lambda':LAM,'poisson_cutoff':J,'Q':str(Q),'K':K,'kmax':kmax,
      'polynomial_uniform_error_bound':str(bound),'uniform_error_less_than_1_over_Q':True,
      'coefficient_sum':str(sum(coeff)),'weighted_recurrence_error_factor':str(weighted_error),
      'weighted_recurrence_error_factor_display':float(weighted_error),
      'floor_accumulation_factor':K+1,'source':'Normalized finite Poisson convolution, exact integers',
      'seconds':time.monotonic()-t}
    (ROOT/'chebyshev_coefficients.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='polynomial_uniform_error_bound'}))
if __name__=='__main__':prepare()
