"""Exact independent spin-coordinate identities, without backend imports."""
import json
from pathlib import Path
import sympy as S


def spin(n):
    plus=S.zeros(n+1)
    minus=S.zeros(n+1)
    for p in range(n): plus[p+1,p]=p+1
    for p in range(1,n+1): minus[p-1,p]=n-p+1
    z=S.diag(*[p-S.Rational(n,2) for p in range(n+1)])
    w=S.diag(*[S.binomial(n,p) for p in range(n+1)])
    return plus,minus,z,w

checks=[]
for n in (1,2,3,4):
    p,m,z,w=spin(n)
    eye=S.eye(n+1)
    assert p*m-m*p == 2*z
    assert z*p-p*z == p
    assert z*m-m*z == -m
    assert z*z+(p*m+m*p)/2 == S.Rational(n,2)*(S.Rational(n,2)+1)*eye
    assert p.T*w == w*m
    root=S.diag(*[S.sqrt(w[k,k]) for k in range(n+1)])
    normalized=root*p*root.inv()
    for k in range(n):
        assert S.simplify(normalized[k+1,k]-S.sqrt((n-k)*(k+1))) == 0
    assert all(w[k,k]>0 for k in range(n+1))
    checks.append({'twice_spin':n,'dimension':n+1,'exact_algebra':'PASS'})

p1,m1,z1,w1=spin(2)
p2,m2,z2,w2=spin(3)
kron=S.kronecker_product
w=kron(w1,w2)
h=S.Rational(2,3)*(kron(p1,m2)+kron(m1,p2))/2 + S.Rational(5,7)*kron(z1,z2)
h+=S.Rational(1,11)*kron((p1+m1)/2,S.eye(4))
h+=S.Rational(2,13)*kron(S.eye(3),z2)
h+=S.Rational(3,17)*kron(z1*z1,S.eye(4))
a=w*h
assert a==a.T
root=S.diag(*[S.sqrt(w[k,k]) for k in range(12)])
orth=root*h*root.inv()
assert S.simplify(orth-orth.T)==S.zeros(12)
e=S.Rational(7,19)
assert S.simplify(a-e*w-root*(orth-e*S.eye(12))*root)==S.zeros(12)
x=S.Matrix([S.Integer(k-5) for k in range(12)])
rho=(x.T*a*x)[0]/(x.T*w*x)[0]
r=(h-rho*S.eye(12))*x
variance=(r.T*w*r)[0]/(x.T*w*x)[0]
assert rho.is_Rational and variance.is_Rational and variance>=0

p,m,z,wc=spin(1)
y=(p-m)/(2*S.I)
ac=wc*y
assert ac==ac.conjugate().T
assert ac!=ac.T
b=S.re(ac)
c=S.im(ac)
realified=b.row_join(-c).col_join(c.row_join(b))
assert realified==realified.T
assert realified.eigenvals()=={-S.Rational(1,2):2,S.Rational(1,2):2}
result={'status':'PASS','arithmetic':'Exact SymPy rational and symbolic square-root identities',
        'single_spin_checks':checks,'mixed_spin_dimension':12,'mixed_spin_pencil':'PASS',
        'generalized_rayleigh_rational':True,'full_residual_variance_rational':True,
        'complex_field_realification_doubled_multiplicities':'PASS'}
Path(__file__).with_name('rational_spin_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
