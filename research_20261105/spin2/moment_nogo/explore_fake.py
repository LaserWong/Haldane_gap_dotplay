# Float/mp exploration only: propose fake bulk clusters (positions, integer weights). Not a proof.
import numpy as np, mpmath as mp, sys, json
from scipy.optimize import nnls
from fractions import Fraction as F
from data import Z, P
mp.mp.dps = 50
def mid(iv): return (iv[0]+iv[1])/2
def targets(M):
    J = {k: (mid(Z[k])+3*mid(P[k]))/4 for k in range(4, M+1)}
    N = {k: (mid(Z[k])-mid(P[k]))/4 for k in range(4, M+1)}
    return J, N
def solve_bulk(r, ks, c=0.95, ngrid=801, seed_scale=1.0):
    ys = np.linspace(-c, c, ngrid); ys = ys[np.abs(ys) > 1e-3]
    A = np.array([[y**k for y in ys] for k in ks]); b = np.array([float(r[k]) for k in ks])
    sc = 1/np.abs(b).clip(1e-6); w, res = nnls(A*sc[:, None], b*sc, maxiter=10000)
    act = [(ys[i], w[i]) for i in range(len(ys)) if w[i] > 1e-9]
    return act, res
def newton(r, ks, nodes, weights):
    # unknown positions for len(ks) of the nodes (the ones with largest |y|^max(ks)*w contributions? use all if counts match)
    n = len(nodes); p = len(ks)
    assert n >= p
    free = list(range(n))[:p] if n == p else sorted(range(n), key=lambda i: -weights[i]*abs(nodes[i])**ks[-1])[:p]
    fixed = [i for i in range(n) if i not in free]
    def F_(*x):
        pos = list(map(mp.mpf, nodes))
        for j, i in enumerate(free): pos[i] = x[j]
        return [sum(weights[i]*pos[i]**k for i in range(n)) - mp.mpf(str(r[k])) if not isinstance(r[k], F) else sum(weights[i]*pos[i]**k for i in range(n)) - mp.mpf(r[k].numerator)/r[k].denominator for k in ks]
    x0 = [mp.mpf(nodes[i]) for i in free]
    sol = mp.findroot(F_, x0, tol=mp.mpf(10)**-40, maxsteps=200)
    sol = [sol] if p == 1 else list(sol)
    pos = list(map(mp.mpf, nodes))
    for j, i in enumerate(free): pos[i] = sol[j]
    return pos
