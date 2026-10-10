"""Small exact-rational certificate kernel. No floating value is proof input."""
from fractions import Fraction as Q
from functools import lru_cache

BITS = 128
SCALE = 1 << BITS

def down(x):
    x=Q(x); return Q(x.numerator*SCALE//x.denominator,SCALE)

def up(x):
    x=Q(x); return Q(-((-x.numerator*SCALE)//x.denominator),SCALE)

@lru_cache(maxsize=100000)
def exp_bounds(x):
    """Taylor enclosure with range reduction, all rational/outward-rounded."""
    x=Q(x)
    if x<0:
        a,b=exp_bounds(-x); return down(1/b),up(1/a)
    k=0
    while x>Q(1,8): x/=2; k+=1
    t=Q(1); s=t
    for j in range(1,33): t=t*x/j; s+=t
    nxt=t*x/33
    a=down(s); b=up(s+nxt/(1-x/34))
    for _ in range(k): a=down(a*a); b=up(b*b)
    return a,b

def log_lower(x,terms=80):
    x=Q(x)
    if x<1: raise ValueError('log_lower expects x >= 1')
    k=0
    while x>=2: x/=2; k+=1
    def unit(y):
        z=(y-1)/(y+1)
        return 2*sum((z**(2*j+1)/Q(2*j+1) for j in range(terms)),Q(0))
    return down(k*unit(Q(2))+unit(x))

def G(x):
    x=Q(x)
    return 1-(1-x)**2/(2*x*x)

def replay(S,T,n,beta,max_rounds=40,clip=False,small=Q(1,100)):
    S,T,beta=map(Q,(S,T,beta))
    if not (0<S<=1 and 0<T<=1 and beta>0 and n>=2 and n%2==0): raise ValueError('Invalid seed')
    input_record={'S':str(S),'T':str(T),'n':n,'beta':str(beta)}
    updates=[]
    for j in range(max_rounds+1):
        u=max(1-S,1-T)
        if u<=small:
            return dict(accepted=True,input=input_record,rounds=j,L0=n,beta_final=str(beta),
                        S_final=str(S),T_final=str(T),u=str(u),
                        gap_lower=str(down(log_lower(1/(5*u))/beta)) if u else None,updates=updates)
        if S*S*T<=Q(1,2):
            return dict(accepted=False,reason='Invariant scalar failure region S^2 T <= 1/2',updates=updates)
        if j==max_rounds: break
        SS=down(G(S*S*T))
        if clip: SS=max(SS,down(S*S*T))
        if SS<=0: return dict(accepted=False,reason='Spatial lower bound nonpositive',updates=updates)
        TT=down(G(T*T*SS))
        if clip: TT=max(TT,down(T*T*SS))
        if TT<=0: return dict(accepted=False,reason='Thermal lower bound nonpositive',updates=updates)
        S,T=SS,TT; n*=2; beta*=2
        updates.append({'S':str(S),'T':str(T),'n':n,'beta':str(beta)})
    return dict(accepted=False,reason='Maximum replay rounds reached; not an exclusion',updates=updates)
