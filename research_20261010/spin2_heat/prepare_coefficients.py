#!/usr/bin/env python3
"""Reconstruct normalized Chebyshev and Taylor coefficients with exact arithmetic."""
import json, math, hashlib
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
Q=2**56

def main():
    output={}
    for name,mu,J in [('chebyshev',128,320),('horner',256,640)]:
        fac=math.factorial(J)
        w=[mu**j*(fac//math.factorial(j)) for j in range(J+1)]
        S=sum(w)
        tau=F(mu**(J+1),math.factorial(J+1))/(1-F(mu,J+2))/F(S,fac)
        if name=='chebyshev':
            b=[(1 if k==0 else 2)*sum(w[j]*w[j+k] for j in range(J+1-k)) for k in range(J+1)]
            den=S*S; assert sum(b)==den
            tail=den
            for K,v in enumerate(b):
                tail-=v
                if 4*Q*tail<den: break
            analytic=4*tau+F(tail,den)
        else:
            b=w;den=S;K=J;tail=0;analytic=2*tau
        c=[Q*x//den for x in b[:K+1]]
        km=max(i for i,x in enumerate(c) if x)
        floor_error=sum(F(x,den)-F(y,Q) for x,y in zip(b[:K+1],c))
        assert analytic<F(1,Q)
        assert sum(c)<=Q
        path=ROOT/f'coefficients_{name}_Q56.txt'
        path.write_text(''.join(str(x)+'\n' for x in c))
        output[name]={'mu':256,'poisson_lambda':mu,'cutoff':J,'Q':str(Q),'K':K,'kmax':km,'nonzero':sum(bool(x) for x in c),'sum':str(sum(c)), 'polynomial_analytic_error':str(analytic),'coefficient_floor_error':str(floor_error),'total_uniform_error':str(analytic+floor_error),'total_uniform_error_times_Q_display':float(Q*(analytic+floor_error)),'weighted_recurrence_error':str(sum(F(x*k*(k+1),2*Q) for k,x in enumerate(c))),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    original=ROOT.parents[1]/'heat_trace/spin2/coefficients_mu256_Q56.txt'
    # ROOT.parents[1] is research root; baseline lies one level higher.
    original=ROOT.parents[1]/'heat_trace/spin2/coefficients_mu256_Q56.txt' if original.exists() else ROOT.parents[2]/'heat_trace/spin2/coefficients_mu256_Q56.txt'
    output['baseline_chebyshev_coefficients_match']=(ROOT/'coefficients_chebyshev_Q56.txt').read_bytes()==original.read_bytes()
    assert output['baseline_chebyshev_coefficients_match']
    (ROOT/'results/coefficient_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:{p:v for p,v in r.items() if p not in ('polynomial_analytic_error','coefficient_floor_error','total_uniform_error')} if isinstance(r,dict) else r for k,r in output.items()},indent=2))
if __name__=='__main__':main()
