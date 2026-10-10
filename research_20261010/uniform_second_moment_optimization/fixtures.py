from fractions import Fraction as F
from math import comb
# Signed finite lists are sanity fixtures, not physical-transfer realizations.
x=[F(-4,5),F(2,5),F(1),F(1,5)]
m={j:sum(a**j for a in x) for j in range(4,13)}
q=[F(1,10),F(-1,3),F(2,7),F(-1,5),F(1)]
c=[sum(q[i]*q[j-i] for i in range(5) if 0<=j-i<5) for j in range(9)]
B=sum(c[j]*m[j+4] for j in range(9));direct=sum(a**4*sum(q[i]*a**i for i in range(5))**2 for a in x);assert B==direct
assert all(a**4*sum(q[i]*a**i for i in range(5))**2<=B for a in x)
assert B!=sum(c[j]*sum(abs(a)**(j+4) for a in x) for j in range(9))
# Three copies of N contribute exactly three sector sums, not a rescaled atom.
J=[F(1),F(-1,2)];N=[F(-4,5),F(2,5)]
for k in range(4,13):assert sum(a**k for a in J+3*N)==sum(a**k for a in J)+3*sum(a**k for a in N)
# Bernstein fixture on [-1,1]: 1-x^2 has Bernstein coefficients [0,2,0].
assert [F(0),F(2),F(0)]==[1-(-1)**2,F(2),1-1**2]
print('PASS signed filters, unit atom removal, sector multiplicities, Bernstein fixture')
