"""NUMERICAL search over real structures J=V K V^dagger: is there V in U(5), t in R with
G(V) = [Tr(-(h'+t)(E_ab (x) E_cd))], h'=(V(x)V)^dag h (V(x)V), real and PSD?  (sufficient-construction cone)."""
import numpy as np, json, sys
from fractions import Fraction as F
from scipy.optimize import minimize
from scipy.linalg import expm
from ed import bond
c=json.load(open('poly.json'))
def proj(J):
    from ed import xbond
def spin2x():
    S=2; ms=[2,1,0,-1,-2]; d=5
    Sz=np.diag(ms).astype(float); Sp=np.zeros((5,5))
    for i in range(1,5): m=ms[i]; Sp[i-1,i]=np.sqrt(S*(S+1)-m*(m+1))
    return np.kron(Sz,Sz)+0.5*(np.kron(Sp,Sp.T)+np.kron(Sp.T,Sp))
x=spin2x(); I=np.eye(25)
def poly(co): return sum(float(F(ci))*np.linalg.matrix_power(x,k) for k,ci in enumerate(co))
P={J:poly(c[J].strip('[]').split(',')) for J in ['P0','P1','P2','P3','P4']}
def G(h):
    m=-h.reshape(5,5,5,5)  # m[i,k,j,l] = <ik| -h |jl>
    # Tr(-h (E_ab x E_cd)) = (-h)_{(b,d),(a,c)} = m[b,d,a,c]
    return np.einsum('bdac->abcd',m).reshape(25,25)
v=np.eye(5).reshape(25)
def obj(p,h,w=10.0):
    Hm=np.zeros((5,5),complex); iu=np.triu_indices(5)
    n=len(iu[0]); re=p[:n]; im=p[n:2*n]; t=p[-1]
    Hm[iu]=re+1j*im; Hm=Hm+Hm.conj().T
    V=expm(1j*Hm); VV=np.kron(V,V)
    hp=VV.conj().T@h@VV
    g=G(hp)+t*np.outer(v,v)
    gs=(g+g.T)/2
    asym=np.linalg.norm(g-g.T); imn=np.linalg.norm(gs.imag)
    lmin=np.linalg.eigvalsh(gs.real).min()
    return -lmin + w*(imn+asym), lmin, imn, asym
def search(h,name,starts=40,seed=0):
    rng=np.random.default_rng(seed); best=None
    for s in range(starts):
        p0=np.concatenate([rng.normal(0,0.7 if s else 0,30),[10.0]])
        r=minimize(lambda p: obj(p,h)[0],p0,method='Nelder-Mead' if False else 'BFGS',options={'maxiter':4000})
        o=obj(r.x,h)
        if best is None or o[0]<best[0]: best=o
    print(name,'best: -lmin+pen=%.4g lmin=%.4g im=%.2g asym=%.2g'%best, flush=True); return best
if __name__=='__main__':
    hn=np.linalg.norm
    search(x,'Heisenberg x',starts=3)
    search(x+(2/9)*x@x+(1/63)*x@x@x,'KHH alpha=1 (x+2/9x^2+1/63x^3)',starts=int(sys.argv[1]))
    search(P['P3']+35/9*P['P4'],'P3+35/9 P4',starts=int(sys.argv[1]))
    search(P['P3']+P['P4'],'P3+P4',starts=int(sys.argv[1]))
