#!/usr/bin/env python3
"""Float-only Option-2 seed pilot. NUMERICAL / HEURISTIC — not a certificate."""
from __future__ import annotations
import json, math, os, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, brentq

ROOT = Path('/workspace/haldane_chat_bundle/runs/spin1_opt2')
AUDIT = Path('/workspace/haldane_chat_bundle/audit_copy/research_20261010')
OUT = ROOT
CACHE = ROOT / 'cache'

BETA0 = 49 / 4
A_SHIFT = 700741 / 500000
CUR_GAMMA = 0.0252132
TARGET = 1.5 * CUR_GAMMA  # ~0.03782

def pack(m, h, r):
    """Karamata packing: max sum y_i^r given 0<=y_i<=h, sum y_i <= m."""
    if m <= 0 or h <= 0 or r <= 0:
        return 0.0
    if m <= h:
        return m ** r
    q = int(m // h)
    rem = m - q * h
    return q * (h ** r) + (rem ** r if rem > 0 else 0.0)

def G(x):
    return 1 - (1 - x) ** 2 / (2 * x * x)

def window_C(S, T):
    K = S * S * T
    if K <= 0.5:
        return 0.0, K
    root = math.sqrt(2 * K - 1)
    rho = (1 - root) / (1 + root)
    d = T / (1 + rho * rho)
    C = (1 - rho) * min(S * math.sqrt(d), d)
    return C, K

def chain_max_gamma(S, T, n=34, beta0=BETA0, W=20, tol=1e-10):
    """Largest gamma for which all windows + asymptotic pass (float)."""
    def ok(gap):
        s, t = S, T
        size, beta = n, beta0
        for j in range(W):
            C, K = window_C(s, t)
            if K <= 0.5 or C <= 0:
                return False
            if C - math.exp(beta * gap) * (1 - C) <= 0:
                return False
            u = max(1 - s, 1 - t)
            if u <= 0.01 and 5 * u * math.exp(beta * gap) < 1:
                return True
            s2 = G(s * s * t)
            t = G(t * t * s2)
            s = s2
            size *= 2
            beta *= 2
        return False

    lo, hi = 0.0, 0.2
    if not ok(lo):
        return 0.0, window_C(S, T)[0]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ok(mid):
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return lo, window_C(S, T)[0]

def load_repo_moments():
    C = json.load(open(AUDIT / 'uniform_second_moment_optimization/certificate.json'))
    M = {k: [(float(eval(v[0].replace('/', '/'))), float(eval(v[1].replace('/', '/'))))
             if False else (float(__import__('fractions').Fraction(v[0])),
                            float(__import__('fractions').Fraction(v[1])))
             for v in rows]
         for k, rows in C['moment_intervals'].items()}
    caps = {k: float(__import__('fractions').Fraction(C['filters'][k]['cap']))
            for k in C['filters']}
    return M, caps, C

def load_long():
    L = json.load(open(AUDIT / 'uniform_smaller_second_initialization/long_certificate.json'))
    return {k: float(__import__('fractions').Fraction(v['bound'])) for k, v in L.items() if 'bound' in v}

def load_R68():
    A = {k: int(v) for k, v in (l.split('=') for l in open(
        AUDIT / 'uniform_smaller_second_initialization_review/anchors.out'))}
    return A['H0_68'] / A['N0_68'] + 68 * A_SHIFT

def hankel_caps(moments_mid, moments_err=None, degree=5):
    """Re-optimize Christoffel square filters (explore.py style). Float."""
    result = {}
    for sector, mid in moments_mid.items():
        mid = np.asarray(mid, float)
        err = np.zeros_like(mid) if moments_err is None else np.asarray(moments_err[sector], float)
        # use first `degree` moments; need 2*degree-1 length for Hankel degree
        # explore uses k=4..12 -> 9 moments, Hankel 5x5 from mid[i+j]
        n_mom = len(mid)
        d = min(degree, (n_mom + 1) // 2)
        H = np.array([[mid[i + j] for j in range(d)] for i in range(d)])
        for sg, name in [(1, '+'), (-1, '-')]:
            target = (1.00139 if sector == 'J' else 0.872) * sg
            def objective(q, target=target, sg=sg):
                c = np.convolve(q, q)
                # pad/trim c to n_mom
                if len(c) < n_mom:
                    c = np.pad(c, (0, n_mom - len(c)))
                else:
                    c = c[:n_mom]
                return (c @ mid + np.abs(c) @ err) / (target ** 4 * np.polyval(q[::-1], target) ** 2 + 1e-30)

            try:
                init = np.linalg.solve(H, np.array([target ** i for i in range(d)]))
            except np.linalg.LinAlgError:
                init = np.ones(d)
            init = init / (np.max(np.abs(init)) + 1e-30)
            q = init
            cap = abs(target)
            for _ in range(8):
                fit = minimize(objective, q, method='BFGS', options={'maxiter': 300, 'gtol': 1e-12})
                q = fit.x
                q = q / q[-1]
                q = np.round(q, 10)

                def f(r, q=q, sg=sg):
                    c = np.convolve(q, q)
                    if len(c) < n_mom:
                        c = np.pad(c, (0, n_mom - len(c)))
                    else:
                        c = c[:n_mom]
                    return r ** 4 * np.polyval(q[::-1], sg * r) ** 2 - (c @ mid + np.abs(c) @ err)

                grid = np.linspace(0.05, 1.15, 2000)
                pairs = [(a, b) for a, b in zip(grid[:-1], grid[1:]) if f(a) < 0 < f(b) or f(a) > 0 > f(b)]
                if not pairs:
                    break
                # outermost positive root
                try:
                    cap = brentq(lambda r: f(r), pairs[-1][0], pairs[-1][1])
                except Exception:
                    break
                target = sg * cap
            result[sector + name] = {'q': q.tolist(), 'cap': float(cap)}
    return result

def seed_from_moments(mj_up, mn_up, U, V, Mdeg, n, beta0, R, long_bounds=None, full=True):
    """Float seed: forcing + packing. Returns dict or None."""
    Z1 = math.exp(-beta0 * R) if full else 1.0
    Z2 = math.exp(-2 * beta0 * R) if full else 1.0

    def sec(s, nn):
        m, h = (mj_up, U ** Mdeg) if s == 'J' else (mn_up, V ** Mdeg)
        v = pack(m, h, nn / Mdeg)
        key = f'{s}{nn}'
        if long_bounds and key in long_bounds:
            v = min(v, long_bounds[key])
        return v

    N2 = 3 * sec('N', 2 * n)
    # largest ell with pack(mj, ell^Mdeg, 2n/Mdeg)+N2 < Z1 and mj > ell^Mdeg
    lo, hi = 0.9, 1.0
    if pack(mj_up, hi ** Mdeg, 2 * n / Mdeg) + N2 >= Z1:
        # try slightly above 1? U may be >1
        hi = max(U, 1.0) * 1.0001
    ok_ell = None
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if mj_up - mid ** Mdeg <= 0:
            hi = mid
            continue
        if pack(mj_up, mid ** Mdeg, 2 * n / Mdeg) + N2 < Z1:
            lo = mid
            ok_ell = mid
        else:
            hi = mid
    if ok_ell is None:
        return None
    ell = lo
    rem = mj_up - ell ** Mdeg
    if not (0 < rem < ell ** Mdeg):
        return None
    tail = pack(rem, rem, n / Mdeg)  # single atom residual is rem^(n/Mdeg); power(rem, n/Mdeg)
    # actually improve.py: power(mj-ell**12, n/12) — the residual mass raised to n/12 as ONE blob
    # which equals rem**(n/Mdeg) since pack of one piece
    tail = rem ** (n / Mdeg) + 3 * sec('N', n)
    Q = sec('J', 2 * n) + 3 * sec('N', 2 * n)
    S = (1 + tail / ell ** n) ** -2
    T = Z2 / Q ** 2
    if S <= 0 or T <= 0 or S > 1 or T > 1:
        return None
    return dict(ell=ell, S=S, T=T, K=S * S * T, tail=tail, Q=Q, Z1=Z1, rem=rem)

def moments_from_ZP(Z, P):
    """Z,P dicts keyed by L -> J,N moment lists for L=min..max sorted."""
    Ls = sorted(Z)
    J, N = [], []
    for L in Ls:
        z, p = Z[L], P[L]
        J.append((z + 3 * p) / 4)
        N.append((z - p) / 4)
    return {'J': J, 'N': N}, Ls

if __name__ == '__main__':
    M, caps, Crow = load_repo_moments()
    longB = load_long()
    R = load_R68()
    print('R68', R)
    print('repo caps', caps)
    mj = M['J'][-1][1]  # upper of last (L=12)
    mn = M['N'][-1][1]
    # Also midpoints
    mj_mid = 0.5 * (M['J'][-1][0] + M['J'][-1][1])
    mn_mid = 0.5 * (M['N'][-1][0] + M['N'][-1][1])
    U = max(caps['J+'], caps['J-'])
    V = max(caps['N+'], caps['N-'])
    print('mj_up', mj, 'mn_up', mn, 'U', U, 'V', V)

    # Baseline FULL
    sd = seed_from_moments(mj, mn, U, V, 12, 34, BETA0, R, longB, full=True)
    print('baseline seed', sd)
    g, C0 = chain_max_gamma(sd['S'], sd['T'], W=20)
    print('baseline gamma', g, 'C0', C0, 'vs certified', CUR_GAMMA, 'target', TARGET)

    # Ideal: midpoints as exact + re-optimized caps with err=0
    mids = {s: [0.5 * (lo + hi) for lo, hi in rows] for s, rows in M.items()}
    errs0 = {s: [0.0] * len(rows) for s, rows in M.items()}
    new_caps = hankel_caps(mids, errs0)
    print('ideal caps', {k: v['cap'] for k, v in new_caps.items()})
    Ui = max(new_caps['J+']['cap'], new_caps['J-']['cap'])
    Vi = max(new_caps['N+']['cap'], new_caps['N-']['cap'])
    sd_i = seed_from_moments(mj_mid, mn_mid, Ui, Vi, 12, 34, BETA0, R, longB, full=True)
    print('ideal seed', sd_i)
    if sd_i:
        gi, Ci = chain_max_gamma(sd_i['S'], sd_i['T'], W=20)
        print('ideal gamma', gi, 'C0', Ci)

    out = {
        'label': 'NUMERICAL/HEURISTIC float pilot',
        'baseline': {'seed': sd, 'gamma': g, 'C0': C0},
        'ideal_L12': {'caps': {k: v['cap'] for k, v in new_caps.items()},
                      'seed': sd_i, 'gamma': gi if sd_i else None, 'C0': Ci if sd_i else None},
        'R68': R, 'target_1p5x': TARGET, 'certified': CUR_GAMMA,
    }
    CACHE.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(CACHE / 'phaseA.json', 'w'), indent=2)
    print('wrote', CACHE / 'phaseA.json')
