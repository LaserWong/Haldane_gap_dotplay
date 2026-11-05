#!/usr/bin/env python3
"""Ideal packing from Prony-fitted transfer atoms (float). NUMERICAL/HEURISTIC."""
import json, math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from pilot_core import (load_repo_moments, load_long, load_R68, chain_max_gamma,
                        seed_from_moments, BETA0, CACHE, TARGET, CUR_GAMMA, pack)

def prony_atoms(moments, n_atoms=4):
    """Prony/Hankel SVD: moments m_k = sum w_i λ_i^k for k=0..N-1 indexing our list as k=4+i."""
    # We have m4..m_{4+n-1}. Shift: use ratio for powers of lambda.
    # Standard: Hankel H_{ij} = m_{i+j}, pencil H1 v = λ H0 v
    m = np.asarray(moments, float)
    n = len(m)
    r = min(n_atoms, n // 2)
    H0 = np.array([[m[i+j] for j in range(r)] for i in range(n-r)])
    H1 = np.array([[m[i+j+1] for j in range(r)] for i in range(n-r)])
    # TLS via SVD of H0
    U, S, Vt = np.linalg.svd(H0, full_matrices=False)
    # rank truncate
    rank = max(1, int(np.sum(S > S[0] * 1e-8)))
    rank = min(rank, r)
    U, S, Vt = U[:, :rank], S[:rank], Vt[:rank]
    H0i = (Vt.T * (1 / S)) @ U.T
    A = H0i @ H1
    # eigenvalues of companion-like A restricted
    # better: generalized eig of (H1, H0) on column space
    try:
        evals = np.linalg.eigvals(Vt[:rank] @ A.T)  # messy
    except Exception:
        evals = np.array([])
    # Standard pencil on square Hankel
    r = min(n_atoms, (n - 1) // 2)
    H0 = np.array([[m[i+j] for j in range(r)] for i in range(r)])
    H1 = np.array([[m[i+j+1] for j in range(r)] for i in range(r)])
    try:
        evals = np.linalg.eigvals(np.linalg.solve(H0, H1))
    except np.linalg.LinAlgError:
        evals = np.linalg.eigvals(np.linalg.pinv(H0) @ H1)
    # Keep real-ish atoms inside (-1.2, 1.2)
    atoms = []
    for lam in evals:
        if abs(lam.imag) < 1e-4 and abs(lam.real) < 1.2:
            atoms.append(lam.real)
    atoms = sorted(atoms, key=lambda x: -abs(x))
    # Solve for weights from first r moments: Vandermonde
    if not atoms:
        return [], []
    r = len(atoms)
    V = np.array([[a ** k for a in atoms] for k in range(r)])
    # moments indexed as power 4,5,... so m[k] = sum w λ^{4+k}
    # Let w'_i = w_i λ_i^4, then m[k] = sum w' λ^k
    try:
        wp = np.linalg.solve(V, m[:r])
    except np.linalg.LinAlgError:
        wp = np.linalg.lstsq(V, m[:r], rcond=None)[0]
    weights = []
    for i, a in enumerate(atoms):
        if abs(a) < 1e-14:
            w = wp[i]
        else:
            w = wp[i] / (a ** 4)
        weights.append(w)
    return list(zip(atoms, weights))

def exact_power_sum(atoms_weights, power):
    return sum(max(w, 0) * (lam ** power) for lam, w in atoms_weights if lam > 0) + \
           sum(max(w, 0) * (abs(lam) ** power) * (1 if power % 2 == 0 else -1)
               for lam, w in atoms_weights if lam <= 0)
    # Actually for packing we only need positive-atom contribution upper bounds.
    
def ideal_sector_bound(atoms_weights, n, positive_only=True):
    """Exact sum |λ|^n * w using fitted atoms (optimistic if weights positive)."""
    s = 0.0
    for lam, w in atoms_weights:
        if w < 0:
            continue  # drop negative weights (noise)
        if positive_only and lam <= 0:
            # odd/even: for upper bound on Z use |lam|^n * w
            s += w * (abs(lam) ** n)
        else:
            s += w * (lam ** n)
    return s

if __name__ == '__main__':
    M, caps, _ = load_repo_moments()
    longB = load_long()
    R = load_R68()
    mids = {s: [0.5*(lo+hi) for lo,hi in rows] for s,rows in M.items()}
    out = {}
    for sector in ['J','N']:
        atoms = prony_atoms(mids[sector], n_atoms=4)
        out[sector] = {'atoms': [{'lam': float(a), 'w': float(w)} for a,w in atoms]}
        print(sector, 'atoms', atoms)
        # residual of fit
        for k, mk in enumerate(mids[sector]):
            pred = sum(w * (lam ** (4+k)) for lam,w in atoms)
            print(f'  m{4+k} mid={mk:.8f} pred={pred:.8f} err={pred-mk:.2e}')

    # Ideal seed: replace sector packing by exact power sums from positive atoms
    # Top J atom ~ ell, residual = sum of other |contrib| at n
    J_atoms = [(a['lam'], a['w']) for a in out['J']['atoms']]
    N_atoms = [(a['lam'], a['w']) for a in out['N']['atoms']]
    # Sort J by lam descending
    J_atoms = sorted(J_atoms, key=lambda x: -x[0])
    if not J_atoms or J_atoms[0][0] <= 0:
        print('no positive top'); raise SystemExit(1)
    ell, w0 = J_atoms[0]
    # Normalize: physical top weight should be ~1 for PF; force ell from forcing instead
    # Optimistic: use ell from Z68 forcing with rem mass = mj - ell^12 from repo mj
    mj = mids['J'][-1]; mn = mids['N'][-1]
    Z1 = math.exp(-BETA0 * R)
    # residual atoms after removing top
    others = J_atoms[1:]
    def J_n(n):
        # w0 * ell^n + sum others
        return w0 * (ell ** n) + sum(max(w,0) * (lam ** n) for lam,w in others if lam>0) \
               + sum(max(w,0) * (abs(lam)**n) for lam,w in others if lam<=0)
    def N_n(n):
        return sum(max(w,0) * (abs(lam)**n) for lam,w in N_atoms)

    # For seed formulas use exact: S = [1 + (J_n - ell^n)/ell^n + 3 N_n / ell^n ]^-2
    # with ell = top, but top weight may not be 1. Use ell_eff with weight folded: dominant = w0*ell^n
    n = 34
    # Forcing-style: find largest L such that pack-equivalent: use top lambda as ell
    # Require w0*ell^{68} + residual_J(68) + 3 N(68) < Z1? Actually Z = J+3N, J includes top.
    # True Z_68 lower is Z1. Upper on non-dominant: Z_68 - w0*ell^68 <= Z_68_upper - ...
    # Optimistic seed: S = (dominant / Z_n)^2 approximately = 1 / (1 + tail/dominant)^2
    dom_n = w0 * (ell ** n)
    tail = (J_n(n) - dom_n) + 3 * N_n(n)
    S = (1 + tail / dom_n) ** -2 if dom_n > 0 else 0
    Q = J_n(68) + 3 * N_n(68)
    Z2 = math.exp(-2 * BETA0 * R)
    T = Z2 / Q ** 2
    print('prony ell,w0', ell, w0, 'S', S, 'T', T, 'K', S*S*T)
    g, C0 = chain_max_gamma(max(min(S,0.999999),1e-6), max(min(T,0.999999),1e-6), W=20)
    print('prony-ideal gamma', g, 'C0', C0)

    # Even more ideal: use true spectral radius = 1 (normalized) and residual from
    # mj_mid - 1^12, with V_true from N+ Prony max |lam|
    U_true = max(abs(a) for a,_ in J_atoms)
    V_true = max(abs(a) for a,_ in N_atoms) if N_atoms else 0.87
    sd = seed_from_moments(mj, mn, U_true, V_true, 12, 34, BETA0, R, longB, full=True)
    print('seed with Prony caps', sd)
    if sd:
        g2,C2 = chain_max_gamma(sd['S'], sd['T'], W=20)
        print('Prony-cap gamma', g2, C2)

    # Absolute oracle: suppose residual J mass at L=12 is known and ALL concentrated at the
    # SECOND eigenvalue from Prony (tightest packing for large n)
    if len(J_atoms) >= 2:
        lam2 = J_atoms[1][0]
        rem = mj - 1.0  # assume ell=1 exactly after shift
        # Actually mj = sum w λ^12, top contributes ~1
        rem = max(mj - 1.0, 0)
        # best case for large-n tail: rem mass at lam2 (not at U)
        # S = [1 + (rem*(lam2/1)^{n} /1^n  wait rem is at power 12: rem_12 = mj-ell^12
        # mass at lam2: alpha with alpha*lam2^12 = rem => alpha = rem/lam2^12, contrib alpha*lam2^n = rem * lam2^{n-12}
        for n_try in [24,28,32,34,36,40,48]:
            rem12 = mj - 1.0
            if rem12 <= 0: rem12 = mj - 0.999999**12
            tail = rem12 * (abs(lam2) ** (n_try - 12)) + 3 * (mn * (V_true ** (n_try - 12)))
            # N: mn = sum w μ^12 <= B * V^12 => sum w μ^n <= mn * (V^{n-12}) if all at V — use Prony N_n
            tail = rem12 * (abs(lam2) ** (n_try - 12)) + 3 * N_n(n_try)
            S = (1 + tail) ** -2
            Q = 1.0 + rem12 * (abs(lam2) ** (68 - 12)) + 3 * N_n(68)
            T = math.exp(-2*BETA0*R) / Q**2
            g3,C3 = chain_max_gamma(min(S,1-1e-15), min(max(T,1e-15),1-1e-15), n=n_try, W=20)
            print(f'oracle n={n_try} lam2={lam2:.5f} S={S:.5f} T={T:.5f} gamma={g3:.6f} C0={C3:.5f}')

    json.dump({'prony': out, 'label': 'HEURISTIC ideal spectrum'}, open(CACHE/'prony_ideal.json','w'), indent=2)
