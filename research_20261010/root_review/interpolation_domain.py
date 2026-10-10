"""Exact endpoint checks for enlarged all-integer 2D interpolation domain.
The analytic monotonicity arguments are recorded in INTERPOLATION_DOMAIN.md.
No eigensolver or floating-point input is used in any pass condition.
"""
from fractions import Fraction as F
import json
from pathlib import Path
v=F(1,40);u=F(1,200)
f=lambda x:x*x/(2*(1-x)**2)
checks={
 'one_dimensional_first_contraction':((3-3*v+v*v)**2/(2*(1-v)**6),F(5)),
 'one_dimensional_thermal_contraction':((2+5*v)**2/(2*(1-2*v-5*v*v)**2),F(5)),
 'one_dimensional_interpolation_loss':(F(3,2)+5*v+2/(1-2*v),F(4)),
 'one_dimensional_gap_ratio':(4/(1-4*v),F(5)),
 'two_dimensional_contraction':(49/(2*(1-7*u)**2),F(32)),
 'two_dimensional_interpolation_argument':(5*u,v),
 'two_dimensional_gap_ratio':(20/(1-20*u),F(32)),
 'two_dimensional_invariant_basin':(32*u,F(1)),
}
for k,(a,b) in checks.items():assert a<=b,(k,a,b)
assert v-5*v*v-v**3>0
# Exact coefficient conditions that appear in the pure-spectrum interpolation.
# All are monotone or bounded by their positive endpoint values on [0,v].
assert 6-4*v+v*v>0
assert 3*v<1 and 2*v<1
out={'status':'PASS exact endpoint inequalities with analytic monotonicity proof',
 'one_dimensional_domain':str(v),'two_dimensional_domain':str(u),
 'two_dimensional_contraction_constant':32,'all_integer_interpolation_loss_constant':20,
 'checks':{k:{'lhs':str(a),'upper':str(b),'passed':a<=b} for k,(a,b) in checks.items()},
 'scope':'Conditional on exact real self-adjoint Hilbert-Schmidt transfer identities for every integer length >=2 in both directions. Same-dyadic-scale rectangles and all square sizes above seed. No arbitrary-aspect-ratio conclusion.'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
