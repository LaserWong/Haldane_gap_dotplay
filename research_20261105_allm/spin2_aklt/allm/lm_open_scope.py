"""NUMERICAL scoping: Lemm-Mozgunov (arXiv:1801.08915) eq. (4.16) open-chain bound, Pi_1=Pi_m=0:
gamma_m >= alpha*c0*mu*sum(c) - beta, alpha=1/sum c_j c_{j+1}, beta=alpha(sum c^2 - sum c_j c_{j+1}),
mu = min_{n'<=n} eps_{n'} (open), valid for 3<=n<=m/2 (as stated), c symmetric, nondecreasing to midpoint."""
import numpy as np
from scipy.optimize import minimize
n=8; mu=0.12522   # float value of certified eps_8 (min over n'<=8 assumed = eps_8; eps_5..7 larger numerically)
def val(c):
    c=np.abs(c); c=np.concatenate([c, c[::-1][(n-1)%2:]]) if False else c
    return c
def full(h):
    h=np.abs(h); k=(n-1+1)//2
    c=np.concatenate([h, h[:(n-1)//2][::-1]]) if (n-1)%2 else np.concatenate([h,h[::-1]])
    return np.maximum.accumulate(c[:k]).tolist()+[None]*0 and c
def bound(h):
    h=np.abs(h); half=np.maximum.accumulate(h)
    c=np.concatenate([half, half[:-1][::-1]]) if (n-1)%2 else np.concatenate([half,half[::-1]])
    q1=np.dot(c[:-1],c[1:]); a=1/q1; b=a*(np.dot(c,c)-q1)
    return a*c[0]*mu*c.sum()-b, c
best=None
for s in range(200):
    h0=np.random.rand((n)//2)+0.1
    r=minimize(lambda h:-bound(h)[0],h0,method='Nelder-Mead',options=dict(maxiter=20000,xatol=1e-12,fatol=1e-14))
    if best is None or -r.fun>best[0]: best=(-r.fun,bound(r.x)[1])
print("LM open-chain bound (n=8, mu=eps_8):",best[0]); print("c/max:",best[1]/best[1].max())
