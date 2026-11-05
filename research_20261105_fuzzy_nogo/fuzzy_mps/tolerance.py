"""Squaring-amplification probe (Xiao L=256 analogue).  Question: suppose every step of the compress-then-square ladder has a
small RELATIVE loss r (delta_0 = r ||E_0||_F, eps_k = r ||E_k||_F).  How large may r be for the a-priori recursion
    delta_{k+1} = eps_{k+1} + (2 opE_k + delta_k) delta_k         [opE_k = a-priori bound on ||E_k||_op]
to keep the seed proxy (lS <= 0.033, lT <= 0.098) alive?   The amplification is Prod_k rho_k with
    rho_k = 2 opE_k ||E_k||_F / ||E_{k+1}||_F,   ln rho_k(exact) = ln2 + L tau_k [2 f(4tau_k) - f(2tau_k) - e0]   (f = shifted free energy/site).
L=6,8: exact Z from the arb ladder (FLOAT recursion on PROVED inputs).  L=256: ESTIMATE, per-site excitation free energy
borrowed from L=8 with the ground-state part replaced by e0_inf = -1.401484 (crude; only the high-T steps matter).
Variants: exact (oracle e0), anders (Anderson m<=11, FLOAT), anders_mX (hypothetical cluster bound e0 - 0.21/(m-1)), bond (e0>=-2), fro (op<=Frobenius)."""
import json, math, numpy as np
from flint import arb
from common import TAU0, C_SHIFT, K
c = float(C_SHIFT); t0 = float(TAU0); And = json.load(open('anderson.json')); E0INF = -1.401484
def lnZ(L):   # ln ||E_k||_F^2 = ln Z_shift(2 tau_k), k = 0..K
    r = json.load(open(f'results/ladder_L{L}_chi0.json'))['rows']; return np.array([math.log(float(arb(x['Z_exact']).mid())) for x in sorted(r, key=lambda x: x['k'])])
def model(L):
    if L <= 8: return lnZ(L), And['ring'][str(L)] / L
    z8, e8 = lnZ(8) / 8, And['ring']['8'] / 8; tk = t0 * 2.0**np.arange(K + 1)
    return L * (z8 + 2 * tk * (e8 - E0INF)), E0INF
def e0lb(v, L, e0):
    if v == 'exact': return e0
    if v == 'anders': return max(x['bound_per_site'] for m, x in And['open'].items() if int(m) <= min(L, 11))
    if v == 'bond': return -2.0
    if v.startswith('anders_m'): m = int(v[8:]); return e0 - 0.21 / (m - 1)
def reldelta(L, r, v):
    lz, e0 = model(L); nF = np.exp(lz / 2); tk = t0 * 2.0**np.arange(K + 1); d = r * nF[0]; out = [d / nF[0]]
    for k in range(K):
        oE = nF[k] if v == 'fro' else math.exp(min(-tk[k] * L * (e0lb(v, L, e0) + c), math.log(nF[k])))
        d = r * nF[k + 1] + (2 * oE + d) * d; out.append(d / nF[k + 1] if np.isfinite(d) else math.inf)
    return out
def loss(n, r, v):
    a, b = reldelta(n, r, v), reldelta(2 * n, r, v)
    if b[5] >= 1 or b[6] >= 1: return math.inf, math.inf
    lS = -2 * math.log(1 - b[5]) + 4 * math.log(1 + a[5]); lT = -2 * math.log(1 - b[6]) + 4 * math.log(1 + b[5]); return lS, lT
def rmax(n, v):
    lo, hi = -80.0, 0.0
    for _ in range(80):
        mid = (lo + hi) / 2; lS, lT = loss(n, 10**mid, v)
        (lo, hi) = (mid, hi) if (lS <= 0.033 and lT <= 0.098) else (lo, mid)
    return 10**lo if lo > -79.9 else 0.0
def lnamp(L, v):
    lz, e0 = model(L); tk = t0 * 2.0**np.arange(K + 1); s = 0
    for k in range(K):
        oE = lz[k] / 2 if v == 'fro' else min(-tk[k] * L * (e0lb(v, L, e0) + c), lz[k] / 2); s += math.log(2) + oE + lz[k] / 2 - lz[k + 1] / 2
    return s / math.log(10)
V = ['exact', 'anders', 'anders_m30', 'anders_m100', 'anders_m1000', 'bond', 'fro']; out = {}
for n in (3, 4, 128):
    for v in V:
        if n <= 4 and v.startswith('anders_m'): continue
        out[f'n{n}|{v}'] = dict(r_max=rmax(n, v), log10_amp_2n=lnamp(2 * n, v), log10_amp_n=lnamp(n, v))
        print(f'n={n:3d} 2n={2*n:3d} {v:13s} r_max {out[f"n{n}|{v}"]["r_max"]:9.2e}   log10 Prod rho (L=2n) {out[f"n{n}|{v}"]["log10_amp_2n"]:8.2f}')
json.dump(out, open('T1_tolerance.json', 'w'), indent=1)
