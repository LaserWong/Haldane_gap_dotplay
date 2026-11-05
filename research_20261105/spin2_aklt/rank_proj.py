import sympy as sp, json
from rank_signs import ranks, xmat
x=xmat(2); I=sp.eye(25); P=[I,x,x*x,x**3,x**4]
c=json.load(open('poly.json'))
print(list(c.keys())[:10])
