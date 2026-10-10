"""Independent, limited rational-arithmetic audit of Haldane supporting constants.
This does NOT verify the physical thermal inputs, trial-state contractions,
or the analytic induction connecting them to the Heisenberg spectral gap.
Formulas: openai/math, periodic Haldane manuscript, verification/computations/
scalars/check-bootstrap-scalars.py and check-moment-initializations.py.
"""
from fractions import Fraction as Q
from math import comb

def require(test, msg):
    if not test:
        raise ArithmeticError(msg)

def update(u):
    require(0 <= u < 1, 'update domain')
    return u*u / (2*(1-u)**2)

def round_up(x):
    y = x*10**7
    return Q(-(-y.numerator//y.denominator), 10**7)

def concentrate(total, cap, exponent):
    k = total // cap
    return k*cap**exponent + (total-k*cap)**exponent

# Rebuild the initial scalar data from the published finite-input centers.
data = [(124885379,65757),(2925,2960742),(12870614,286599),
        (54069,1920414),(4639283,510140),(195455,1514846),
        (2654823,675419),(377629,1314544),(1900547,787405)]
err = Q(30,10**6)
moments = [[Q(0)]*4+[Q(z+k*p,4*10**6) for z,p in data] for k in (3,-1)]
caps = [Q(100139,100000),Q(872,1000)]
for r, coeff in enumerate(([7,17,-280,-185,1000],[12,0,-394,0,1000])):
    poly = [0]*13
    for i,a in enumerate(coeff):
        for j,b in enumerate(coeff):
            poly[i+j+4] += a*b
    bound = sum(a*m+abs(a)*err for a,m in zip(poly,moments[r]))
    for sign in (-1,1):
        shift = [sum(comb(i,j)*a*sign**i*caps[r]**(i-j)
                     for i,a in enumerate(poly) if i>=j) for j in range(13)]
        require(shift[0]>bound and all(t>=0 for t in shift[1:]), 'filter inequality')
upper = [m[12]+err for m in moments]
lo = Q(999,1000)
def non(n):
    return 3*concentrate(upper[1],caps[1]**12,n//12)
def tail(n):
    return non(n)+(upper[0]-lo**12)**(n//12)
require(concentrate(upper[0],lo**12,6)+non(72)<1,'dominant existence scalar')
require(lo**12<upper[0]<2*lo**12,'residual and uniqueness scalars')
p = 1-(1+tail(36)/lo**36)**(-2)
q = 1-(caps[0]**72+tail(72))**(-2)
print('Source 1 initial bounds:',float(p),float(q))
expected = [(Q(151249,2500000),Q(433453,2500000)),
            (Q(343303,5000000),Q(1632381,10000000)),
            (Q(44601,625000),Q(361773,2500000)),
            (Q(632939,10000000),Q(1055161,10000000)),
            (Q(375793,10000000),Q(445941,10000000)),
            (Q(84513,10000000),Q(27493,5000000))]
for i,wanted in enumerate(expected,1):
    p=round_up(update(1-(1-p)**2*(1-q)))
    q=round_up(update(1-(1-q)**2*(1-p)))
    require((p,q)==wanted,'six-round record')
    print('Round',i,':',float(p),float(q))
require(max(p,q)<Q(1,100),'final threshold')
for u,C in [(Q(1,100),Q(5)),(Q(1,8),Q(79,10))]:
    G=sum((1-u)**(-j) for j in (1,2,3))**2/2
    require(G<C and C*u<1 and C*(1-3*u)>3,'envelope constants')
    print('Envelope:', 'u0=',str(u),'G=',float(G),'C=',float(C),'Cu0=',float(C*u))
# Source 2 final scalar purity estimates, conditional on its input bounds.
D,Ti,T0,Rq=Q(145,100),Q(1225,1000),Q(1264,1000),Q(684,10000)
t=Q(998,1000)
R=max(x*x+y*y/2+(D-t-x-y)**2/3 for x,y in
      [(Q(0),Q(0)),(Ti-t,Q(0)),(Ti-t,T0-Ti),(Q(0),T0-t)])
S=(1+R/t**2)**(-2)
T=(1+Rq)**(-2)
require(S>Q(7,8) and T>Q(7,8),'source 2 purity thresholds')
print('Source 2 final scalar purity lower bounds:',float(S),float(T))
print('PASS: only the limited scalar checks described above; not a full proof verification.')
