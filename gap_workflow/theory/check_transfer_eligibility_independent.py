"""Exact independent tensor realignment witnesses and classical identities."""
import json
import sys
from pathlib import Path
import sympy as S
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'tests'))
from test_classical_seed import transfer_and_enumeration

x=S.Matrix([[0,1],[1,0]])/2
z=S.diag(-S.Rational(1,2),S.Rational(1,2))
c=S.Matrix([[1,S.Rational(1,2)],[S.Rational(1,2),2]])
ops=[x,z]
h=-sum((c[i,j]*S.kronecker_product(ops[i],ops[j]) for i in range(2) for j in range(2)),S.zeros(4))
r=S.Matrix(4,4,lambda i,j:-h[(i//2)*2+j//2,(i%2)*2+j%2])
vec=lambda a:S.Matrix([a[i,j] for i in range(2) for j in range(2)])
expected=sum((c[i,j]*vec(ops[i])*vec(ops[j]).T for i in range(2) for j in range(2)),S.zeros(4))
assert r==expected
l,d=c.LDLdecomposition()
assert l*d*l.T==c
assert all(d[i,i]>0 for i in range(2))
witness=[sum((l[j,i]*ops[j] for j in range(2)),S.zeros(2)) for i in range(2)]
assert -h==sum((d[i,i]*S.kronecker_product(witness[i],witness[i]) for i in range(2)),S.zeros(4))
af=S.kronecker_product(z,z)
raf=S.Matrix(4,4,lambda i,j:-af[(i//2)*2+j//2,(i%2)*2+j%2])
v=vec(z)
negative=(v.T*raf*v)[0]
assert negative<0
cases=[]
for width in (1,2):
    for length in (2,3,4,5):
        t,tr,zv=transfer_and_enumeration(width,length)
        assert tr==zv
        assert t==[list(row) for row in zip(*t)]
        cases.append({'width':width,'length':length,'exact_trace':str(tr),'status':'PASS'})
result={'status':'PASS','realignment_identity':'PASS','rational_LDL_witness':'PASS',
        'antiferromagnetic_SzSz_negative_quadratic_form':str(negative),
        'classical_transfer_cases':cases}
Path(__file__).with_name('transfer_eligibility_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
