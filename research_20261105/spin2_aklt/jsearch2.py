"""NUMERICAL: nonconvex search for real structure J=VKV^+ making h in the sufficient cone. Smooth penalty objective."""
import numpy as np, sys, time
from scipy.optimize import minimize
from scipy.linalg import expm
from jsearch import x, G, v, P
from jcheck import V as V0
iu=np.triu_indices(5)
def unpack(p):
    Hm=np.zeros((5,5),complex); Hm[iu]=p[:15]+1j*p[15:30]; Hm=Hm+Hm.conj().T
    return V0@expm(1j*Hm), p[30]
def f(p,h,ret=False):
    V,t=unpack(p); VV=np.kron(V,V); g=G(VV.conj().T@h@VV)+t*np.outer(v,v)
    gs=(g+g.T)/2; e=np.linalg.eigvalsh(gs.real)
    pen=np.sum(np.minimum(e,0)**2)+10*(np.linalg.norm(gs.imag)**2+np.linalg.norm(g-g.T)**2)
    return (pen,e.min(),np.linalg.norm(gs.imag)) if ret else pen
h={'KHH1':x+(2/9)*x@x+(1/63)*x@x@x,'R35':P['P3']+35/9*P['P4'],'P34':P['P3']+P['P4']}[sys.argv[1]]
rng=np.random.default_rng(int(sys.argv[3])); best=None; t0=time.time()
for s in range(int(sys.argv[2])):
    p0=np.concatenate([rng.normal(0,float(sys.argv[4]),30),[50.0]])
    r=minimize(f,p0,args=(h,),method='L-BFGS-B',options={'maxiter':3000})
    o=f(r.x,h,True)
    if best is None or o[0]<best[0]: best=o
    print(s,'pen %.3g lmin %.4g im %.2g'%o,'best pen %.3g'%best[0],round(time.time()-t0),flush=True)
    if time.time()-t0>500: break
