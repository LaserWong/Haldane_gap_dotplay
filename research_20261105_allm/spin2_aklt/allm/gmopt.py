import numpy as np, sys
from scipy.optimize import minimize
def q(c,x):
    L=len(c); return 0.0 if x>L-1 else float(np.dot(c[:L-x],c[x:]))
def bound(c,n,m,eps):
    c=np.abs(c); S=c.sum(); S2=(c*c).sum(); q1=q(c,1)+q(c,m-1)
    Qmax=max([q(c,e)+q(c,m-e) for e in range(2,m-1)]+[0])
    best=-9
    for a in (1/q1, 1/max(Qmax,1e-300)):
        if a*Qmax>1+1e-12: continue
        b=a*S2-1+2*abs(1-a*q1)
        best=max(best,a*S*S*eps/(n-1)-b)
    return best
eps={7:0.1254,8:0.12522}
for n in (7,8):
  for m in range(n,2*n+1):
    L=n-1; j=np.arange(L); c0=(n-1)+(n-2)*j-j*j
    r=[bound(c0,n,m,eps[n])]
    bestc=c0
    rng=np.random.default_rng(0)
    for s in range(40):
        x0=c0*(1+0.3*rng.standard_normal(L)) if s else c0
        res=minimize(lambda c:-bound(c,n,m,eps[n]),x0,method='Nelder-Mead',options=dict(maxiter=20000,xatol=1e-10,fatol=1e-12))
        if -res.fun>max(r): bestc=np.abs(res.x)/np.abs(res.x).max()
        r.append(-res.fun)
    print(n,m,'GMweights %.5f'%r[0],'opt %.5f'%max(r),np.round(bestc,3),flush=True)
