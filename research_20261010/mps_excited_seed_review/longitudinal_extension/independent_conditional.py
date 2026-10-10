#!/usr/bin/env python3
"""Audit hypothetical trace budget without interpreting its premise as true."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
P=Path(__file__).resolve().parent
ns={'__file__':str(P/'independent_scalar.py')}
exec((P/'independent_scalar.py').read_text().split("p=values('independent_contractions.out')")[0],ns)
exp=ns['exp_interval'];floor=ns['floor'];D=ns['D']
r=json.loads((P/'inputs/exact_witness_data.json').read_text())['rows'][-1]
d,g=F(r['delta']),F(r['trial_energy_difference']);beta=F(8);eta=F(201,200)
num=exp(-2*beta*d)[0]
j=floor(num/(eta**4*(1+2*exp(-beta*g)[1])**4));c=floor(num/(eta**2*(1+2*exp(-2*beta*g)[1])**2))
def G(x):
 assert 0<x<=1
 return floor((x*x+2*x-1)/(2*x*x))
a=G(j);b=G(c*c*a);history=[{'a':str(a),'b':str(b)}]
for _ in range(2):
 a=G(a*a*b);b=G(b*b*a);assert min(a,b)>0
 history.append({'a':str(a),'b':str(b)})
root=F(isqrt(b.numerator*D*D//b.denominator),D);assert root*root<=b
s=floor(a*root);t=floor(a*a*b);K=t
for iteration in range(100):
 if min(s,t)>F(99,100):break
 s=G(max(s*s*t,K));t=G(max(t,K)**2*s);K=F(0);assert min(s,t)>0
 history.append({'s':str(s),'t':str(t)})
assert min(s,t)>F(99,100)
x=exp(-beta*g)[0];ratio=floor((1+3*x)/(1+2*x));assert ratio>eta
out={'status':'PASS conditional success AND rigorous contradiction of its premise','beta':str(beta),'hypothetical_trace_multiplier':str(eta),'conditional_final_common_lower':str(min(s,t)),'conditional_final_common_lower_display':float(min(s,t)),'actual_four_to_three_witness_trace_ratio_lower':str(ratio),'actual_four_to_three_witness_trace_ratio_lower_display':float(ratio),'premise_is_impossible':True,'history':history,'scope':'The condition U(beta),U(2beta)<=201/200 times the three-state lower trial trace is hypothetical. The fourth orthogonal witness contradicts it already at beta8. No trace upper bound or startup certificate follows.'}
(P/'independent_conditional.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
