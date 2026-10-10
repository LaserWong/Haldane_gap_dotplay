"""Exact all-temperature W exclusion for the uniform spin-s Heisenberg seed n=2.

H_2 has both periodic bonds. H_4=(S1+S3).(S2+S4). x=exp(-2 beta).
W=x^(2s) Q_4(x)/Q_2(x)^4. All coefficients are integer.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
from certified_core import exp_bounds

OUT=Path(__file__).resolve().parents[1]/'results'

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def polynomials(twos):
    t=twos
    q2=[0]*(t*(t+1)//2+1)
    for j in range(t+1): q2[j*(j+1)//2]+=2*j+1
    # E0(H4)=-t(t+1); all pair spins a,b are integers 0,...,t.
    q4=[0]*(t*t+t*(t+1)+1)
    for a in range(t+1):
        for b in range(t+1):
            for j in range(abs(a-b),a+b+1):
                gap=(j*(j+1)-a*(a+1)-b*(b+1))//2+t*(t+1)
                q4[gap]+=2*j+1
    assert sum(q2)==(t+1)**2 and sum(q4)==(t+1)**4
    numerator=[0]*t+q4
    denominator=mul(mul(q2,q2),mul(q2,q2))
    assert len(numerator)==len(denominator)
    return numerator,denominator

def bernstein(a):
    n=len(a)-1
    return [sum((Q(a[i]*comb(k,i),comb(n,i)) for i in range(k+1)),Q(0)) for k in range(n+1)]

def split(b):
    left=[b[0]]; right=[b[-1]]
    while len(b)>1:
        b=[(a+c)/2 for a,c in zip(b[:-1],b[1:])]
        left.append(b[0]);right.append(b[-1])
    return left,list(reversed(right))

def certify_upper(twos,upper):
    num,den=polynomials(twos)
    # upper*D-N >= 0 everywhere suffices since D>=1.
    b=bernstein([upper*d-n for n,d in zip(num,den)])
    stack=[(Q(0),Q(1),b,0)]; leaves=[]
    while stack:
        l,r,b,depth=stack.pop()
        if min(b)>=0:
            leaves.append({'x_lo':str(l),'x_hi':str(r),'minimum_Bernstein_coefficient':str(min(b))})
            continue
        if depth>=40: raise ArithmeticError('Upper bound not certified at depth 40')
        lb,rb=split(b); m=(l+r)/2
        stack.extend([(m,r,rb,depth+1),(l,m,lb,depth+1)])
    return {'spin':str(Q(twos,2)),'n_bootstrap':2,'m_direct_sites':4,
            'proof':'Exact rational Bernstein subdivision of upper*D(x)-N(x) on 0<=x<=1',
            'W_upper':str(upper),'W_upper_display':float(upper),
            'numerator_coefficients':num,'denominator_coefficients':den,
            'leaves':leaves,'all_beta_excluded_for_legacy_recursion':upper<Q(1,2),
            'no_claim_about_moment_filtered_n_greater_than_2':True}

def evaluate(a,x):
    y=Q(0)
    for c in reversed(a): y=y*x+c
    return y

def main():
    rows=[]
    # Decimal constants proposed from archived floating diagnostics; each is independently certified here.
    for t,upper,x in [(2,Q('0.012674'),Q('0.450')),(4,Q('0.002098'),Q('0.574')),(6,Q('0.000695'),Q('0.676'))]:
        row=certify_upper(t,upper)
        num,den=polynomials(t); lower=evaluate(num,x)/evaluate(den,x)
        row.update(W_max_lower=str(lower),W_max_lower_display=float(lower),witness_x=str(x))
        print('spin',Q(t,2),'certified max W interval',float(lower),float(upper),'leaves',len(row['leaves']),flush=True)
        rows.append(row)
    out={'status':'certified_exact_analytic_spectra_all_temperatures','models':rows}
    (OUT/'uniform_n2_all_beta.json').write_text(json.dumps(out,indent=2))

if __name__=='__main__': main()
