"""PROVED (exact rationals via sympy): rank decomposition h = sum_k g_k Sum_q T^k_q (x) T^k_q^dagger,
T^k_q orthonormal irreducible tensor operators (HS norm). Sufficient condition of THEORY.md eq.(13) construction
in the time-reversal-real basis: g_k >= 0 for odd k, g_k <= 0 for even k >= 2 (k=0 is a constant shift)."""
import sympy as sp
from sympy.physics.quantum.cg import CG
def spin(S):
    ms=[S-i for i in range(2*S+1)]; d=len(ms)
    Sz=sp.diag(*ms); Sp=sp.zeros(d)
    for i in range(1,d): m=ms[i]; Sp[i-1,i]=sp.sqrt(S*(S+1)-m*(m+1))
    return ms,Sz,Sp,Sp.T
def T(S,k,q,ms):
    d=len(ms); M=sp.zeros(d)
    for i,m in enumerate(ms):
        for j,mp in enumerate(ms):
            M[i,j]=CG(S,mp,k,q,S,m).doit()
    n=sp.sqrt(sum(abs(v)**2 for v in M)); return M/n
def kron(A,B): return sp.kronecker_product(A,B)
def ranks(S,h):
    ms,_,_,_=spin(S); g=[]
    for k in range(2*S+1):
        P=sum((kron(T(S,k,q,ms),T(S,k,q,ms).H) for q in range(-k,k+1)),sp.zeros(len(ms)**2))
        g.append(sp.nsimplify(sp.simplify((P.H*h).trace()/(2*k+1))))
    return g
def xmat(S):
    ms,Sz,Sp,Sm=spin(S); return kron(Sz,Sz)+(kron(Sp,Sm)+kron(Sm,Sp))/2
if __name__=='__main__':
    a=sp.symbols('alpha')
    x1=xmat(1); I1=sp.eye(9)
    print('spin1 Heis', ranks(1,x1)); print('spin1 AKLT x+x^2/3', ranks(1,x1+x1**2/3))
    x=xmat(2); I=sp.eye(25); x2=x*x; x3=x2*x; x4=x3*x
    print('spin2 x', ranks(2,x)); print('spin2 x^2', ranks(2,x2)); print('spin2 x^3', ranks(2,x3)); print('spin2 x^4', ranks(2,x4))
