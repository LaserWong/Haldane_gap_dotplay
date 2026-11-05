"""Bootstrap-seed proxy for T1.  Seeds (ising_mps.py convention): s = B/A^2, t = D/B^2 with A = Z_n(beta), B = Z_2n(beta),
D = Z_2n(2 beta), beta = 49/4, n in {3,4} (2n = 6, 8).  Z(beta) = ||E_5||_F^2, Z(2beta) = ||E_6||_F^2.
Lower endpoints s_lo = B_lo/A_hi^2, t_lo = D_lo/B_hi^2.  Log-loss vs exact: lS = ln(s_ex/s_lo), lT = ln(t_ex/t_lo).
PROXY budget (FEASIBILITY.md, what the PROVED spin-1 certificate actually spent at n=34): lS <= 0.033, lT <= 0.098.
slack = min(0.033 - lS, 0.098 - lT) > 0  <=>  proxy YES."""
import json, glob, math, numpy as np
from flint import arb
BUD = (0.033, 0.098)
def load(mode, L, chi):
    try: return json.load(open(f'results/{mode}_L{L}_chi{chi}.json'))
    except FileNotFoundError: return None
def zs(res, k, v):
    r = [x for x in res['rows'] if x['k'] == k][0]; ex = float(arb(r['Z_exact']).mid())
    if v == 'true': return r['Z_lo_true'], r['Z_hi_true'], ex, r['eta_true'] / r['normY']
    if f'Z_lo_{v}' not in r: return None
    return r[f'Z_lo_{v}'], r[f'Z_hi_{v}'], ex, r[f'delta_{v}'] / r['normY']
out = {}; lines = []
for mode in ('tebd', 'ladder'):
    for n in (3, 4):
        for chi in (8, 16, 32, 64, 128, 256, 512, 1024, 0):
            Ra, Rb = load(mode, n, chi if n == 4 or chi in (8, 16, 32, 64, 128, 0) else 0), load(mode, 2 * n, chi)
            if Ra is None or Rb is None: continue
            for v in ('true', 'exact', 'anders', 'bond', 'fro'):
                a, b, dd = zs(Ra, 5, v), zs(Rb, 5, v), zs(Rb, 6, v)
                if a is None or b is None or dd is None: continue
                A_lo, A_hi, A = a[:3]; B_lo, B_hi, B = b[:3]; D_lo, D_hi, Dx = dd[:3]
                lS = math.log(B / B_lo) + 2 * math.log(A_hi / A) if B_lo > 0 else math.inf
                lT = math.log(Dx / D_lo) + 2 * math.log(B_hi / B) if D_lo > 0 else math.inf
                slack = min(BUD[0] - lS, BUD[1] - lT)
                key = f'{mode}|n{n}|chi{chi or "inf"}|{v}'
                out[key] = dict(relZhi_B=B_hi / B - 1, relZhi_D=D_hi / Dx - 1, reldelta_B=b[3], reldelta_D=dd[3],
                                lS=lS, lT=lT, slack=slack, verdict='YES' if slack > 0 else 'NO',
                                s_ex=B / A**2, t_ex=Dx / B**2)
                lines.append(f'{key:34s} Zhi/Z-1: B {B_hi/B-1:9.2e} D {Dx and D_hi/Dx-1:9.2e} | lS {lS:9.3g} lT {lT:9.3g} slack {slack:9.3g} {out[key]["verdict"]}')
print('\n'.join(lines)); json.dump(out, open('T1_proxy.json', 'w'), indent=1)
