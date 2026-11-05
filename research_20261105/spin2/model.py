"""NONRIGOROUS estimates: free-triplet-magnon (relativistic) model of Z_L(beta)
for the periodic spin-S Heisenberg chain, plus the repo's bootstrap recursion
(window lemma, G-recursion, tail) run on modeled seeds with an adjustable slack.
Everything here is an ESTIMATE used only for feasibility scoping."""
import numpy as np
from scipy.special import k1

PARAMS = {  # literature values (DMRG/QMC); v = Delta*xi (relativistic magnon)
  1: dict(e0=-1.401484038971, Delta=0.41048, xi=6.0153),
  2: dict(e0=-4.761248, Delta=0.08917, xi=49.49),     # Todo-Kato 2001 (Delta 0.0876(13) per Wang-Qin-Yu 1999)
}

def lnZ_shifted(S, L, beta, Delta=None, xi=None):
    """ln[Z_L(beta) e^{beta L e0}] = -beta*delta_L + thermal; 3 free relativistic magnon species
    (lattice-regularised dispersion w_q^2 = D^2 + (2v sin(q/2))^2, q = 2 pi j/L about k=pi, even L).
    delta_L = E0(L) - L e0 from the Luscher/Casimir sum for 3 massive bosons."""
    p = PARAMS[S]; D = Delta or p['Delta']; x = xi or p['xi']; v = D * x
    k = np.arange(1, 60)
    delta = -(3 * D / np.pi) * np.sum(k1(k * L / x) / k)
    j = np.arange(L) - L // 2
    w = np.sqrt(D**2 + (2 * v * np.sin(np.pi * j / L))**2)
    th = -3 * np.sum(np.log1p(-np.exp(-beta * w)))
    return -beta * delta, th, delta

def lnZ(S, L, beta, **kw):
    a, b, _ = lnZ_shifted(S, L, beta, **kw); return a + b

def seeds(S, n, beta, **kw):
    lnS = lnZ(S, 2*n, beta, **kw) - 2*lnZ(S, n, beta, **kw)
    lnT = lnZ(S, 2*n, 2*beta, **kw) - 2*lnZ(S, 2*n, beta, **kw)
    return float(np.exp(lnS)), float(np.exp(lnT))

def G(x): return 1 - (1 - x)**2 / (2 * x * x)

def window_C(s, t):
    K = s * s * t
    if K <= 0.5: return None
    w = (1 + np.sqrt(2 * K - 1)) / 2; rho = (1 - w) / w; d = t / (1 + rho * rho)
    return (1 - rho) * min(s * np.sqrt(d), d)

def bootstrap(s, t, n, beta, maxw=40):
    """Run windows; return (ok, uniform gap lower bound, list of (n,beta,S,T,C,gap))."""
    rows = []; gmin = np.inf
    for j in range(maxw):
        C = window_C(s, t)
        if C is None or C <= 0.5: return False, 0.0, rows
        g = np.log(C / max(1 - C, 1e-300)) / beta; gmin = min(gmin, g)
        rows.append((n, beta, s, t, C, g))
        u = max(1 - s, 1 - t)
        if u <= 0.01 and 5 * u * np.exp(min(2 * beta * gmin, 700)) < 1:  # tail lemma (next window at 2beta)
            return True, gmin, rows
        s = G(s * s * t); t = G(t * t * s); n *= 2; beta *= 2
    return False, gmin, rows
