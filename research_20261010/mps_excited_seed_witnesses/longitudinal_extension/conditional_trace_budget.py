#!/usr/bin/env python3
"""An explicitly hypothetical scalar success and its impossible trace premise."""
from pathlib import Path
import json
from fractions import Fraction as F
from math import isqrt
P=Path(__file__).resolve().parent
source=(P.parent/'verify_scalar.py').read_text().split('rows=[]\nfor r in')[0]
ns={'__file__':str(P.parent/'verify_scalar.py')};exec(source,ns)
exp_i,up,down,G=[ns[k] for k in ['exp_i','up','down','G']];B=1<<160;Q=1<<64
data=json.loads((P.parent/'exact_witness_data.json').read_text())['rows'][-1]
d=F(data['delta']);g=F(data['trial_energy_difference'])
dhi=F(-(-d.numerator*Q//d.denominator),Q);glo=F(g.numerator*Q//g.denominator,Q);ghi=F(-(-g.numerator*Q//g.denominator),Q)
beta=F(8);eta=F(201,200)
assert dhi>=d>0 and 0<glo<=g<=ghi
num=exp_i(-2*beta*dhi)[0]
J=down(num/(eta**4*(1+2*exp_i(-beta*glo)[1])**4))
C=down(num/(eta**2*(1+2*exp_i(-2*beta*glo)[1])**2))
a=down(G(J));b=down(G(C*C*a));assert min(a,b)>0
history=[{'stage':'initial','a_lower':str(a),'b_lower':str(b)}]
for k in range(2):
    a=down(G(a*a*b));assert a>0
    b=down(G(b*b*a));assert b>0
    history.append({'stage':f'additional time-first cycle {k+1}','a_lower':str(a),'b_lower':str(b)})
sqrtlo=F(isqrt(b.numerator*B*B//b.denominator),B);assert sqrtlo*sqrtlo<=b
s=down(a*sqrtlo);t=down(a*a*b);K=t
history.append({'stage':'joint-aware canonical conversion','S_lower':str(s),'T_lower':str(t),'K_lower':str(K)})
for k in range(16):
    if min(s,t)>F(99,100):break
    s=down(G(max(s*s*t,K)));assert s>0
    t=down(G(max(t,K)**2*s));assert t>0
    K=F(0)
    history.append({'stage':f'canonical cycle {k+1}','S_lower':str(s),'T_lower':str(t)})
assert min(s,t)>F(99,100)
# The fourth orthogonal witness actually contradicts the hypothetical small-beta trace premise.
xlo=exp_i(-beta*ghi)[0];ratio_lo=down((1+3*xlo)/(1+2*xlo));assert ratio_lo>eta
out={'status':'PASS conditional replay; its trace premise is rigorously contradicted by the fourth witness','n':24,'beta':'8','hypothetical_multiplier':'201/200','conditional_premise':'If upper traces U(beta) and U(2beta) were at most 201/200 times the three-state trial trace at each temperature, the following scalar lower orbit succeeds. No such upper traces are certified; the first premise is impossible by the new fourth-state trace lower bound.','J_lower_under_hypothesis':str(J),'C_lower_under_hypothesis':str(C),'history':history,'final_common_lower_display':float(min(s,t)),'four_state_to_three_state_trace_ratio_lower_at_beta8':str(ratio_lo),'four_state_to_three_state_trace_ratio_lower_display':float(ratio_lo),'physical_conclusion':'The apparent three-state warm opportunity cannot be interpreted as allowing a 0.5% tail above that incomplete trace. A four-state necessary screen is the appropriate next baseline.'}
(P/'conditional_trace_budget.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
