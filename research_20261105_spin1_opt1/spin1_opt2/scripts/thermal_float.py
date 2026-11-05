#!/usr/bin/env python3
"""Float thermal Z_L^{I,P} = Tr exp(-beta (H+aL)) for spin-1 rings. NUMERICAL only."""
from __future__ import annotations
import os, sys, json, time, math
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
import scipy.sparse as sp
from pathlib import Path

sys.path.insert(0, '/workspace/haldane_chat_bundle/runs/thermal_arb')
import blocks as B

CACHE = Path('/workspace/haldane_chat_bundle/runs/spin1_opt2/cache')
CACHE.mkdir(parents=True, exist_ok=True)
BETA0 = 49/4
A = 700741/500000

def dense_block_eigh_contrib(L, tw, beta, a):
    """Sum mult*exp(-beta*(eig+aL)) over Sz>=0 Bloch blocks (Sz<0 by spin-flip)."""
    H = B.full_H(L, tw)
    T, s = B.twisted_translation(L, tw)
    F = B.flip(L)
    chk, Szv = B.checks(L, tw, H, T, s, F)
    assert chk['H_symmetric'] and chk['H conserves Sz']
    total = 0.0
    # Sz from 0..L; for Sz>0 multiply by 2 (spin flip), Sz=0 once
    for sz in range(0, L+1):
        sd = B.sector_data(L, H, T, s, Szv, sz)
        for q, mult_q in B.q_values(L, tw, sz):
            # build block
            per, sigma = sd['per'], sd['sigma']
            ok = ((q * per) % L == 0) & ((((q * per) // L) % 2) == ((1 - sigma) // 2))
            sel = np.nonzero(ok)[0]
            m = len(sel)
            if m == 0:
                continue
            pos = -np.ones(len(per), int); pos[sel] = np.arange(m)
            real = q in (0, L)
            Hf = np.zeros((m, m), float if real else complex)
            for (a_i, b_i), cv in sd['coef'].items():
                if pos[a_i] < 0 or pos[b_i] < 0: continue
                # sum_t cv[t] * exp(i pi q t / L) * sqrt(per_a*per_b)/L
                phase = 0j if not real else 0.0
                for t in range(L):
                    if cv[t] == 0: continue
                    ang = math.pi * q * t / L
                    phase += cv[t] * (math.cos(ang) + (0 if real else 1j*math.sin(ang)))
                scale = math.sqrt(per[a_i] * per[b_i]) / L
                Hf[pos[a_i], pos[b_i]] += scale * phase
            # Hermitian cleanup
            if real:
                Hf = 0.5 * (Hf + Hf.T)
                ev = np.linalg.eigvalsh(Hf)
            else:
                Hf = 0.5 * (Hf + Hf.conj().T)
                ev = np.linalg.eigvalsh(Hf)  # Hermitian -> real eigs; use eigh on complex
            # For complex Hermitian use np.linalg.eigh
            if not real:
                ev = np.linalg.eigh(Hf, UPLO='L')[0]
            spin_mult = 1 if sz == 0 else 2
            w = spin_mult * mult_q * np.exp(-beta * (ev + a * L)).real
            total += float(w.sum())
    return total

def hutchinson_Z(L, tw, beta, a, n_probe=32, n_lanczos=64, seed=0):
    """Stochastic Tr exp(-beta(H+aL)) via Lanczos on random ±1 probes. NUMERICAL."""
    H = B.full_H(L, tw).astype(np.float64)
    N = H.shape[0]
    shift = a * L
    rng = np.random.default_rng(seed)
    acc = 0.0
    for p in range(n_probe):
        v = rng.choice([-1.0, 1.0], size=N)
        v /= np.linalg.norm(v)
        # Lanczos for v^T f(H) v with f(x)=exp(-beta(x+shift))
        # Build tridiagonal
        alpha = np.zeros(n_lanczos)
        beta_l = np.zeros(n_lanczos)
        V = np.zeros((N, n_lanczos))
        V[:, 0] = v
        w = H @ V[:, 0]
        alpha[0] = V[:, 0] @ w
        w = w - alpha[0] * V[:, 0]
        for j in range(1, n_lanczos):
            beta_l[j] = np.linalg.norm(w)
            if beta_l[j] < 1e-14:
                n_lanczos = j
                break
            V[:, j] = w / beta_l[j]
            w = H @ V[:, j]
            alpha[j] = V[:, j] @ w
            w = w - alpha[j] * V[:, j] - beta_l[j] * V[:, j - 1]
            # full reorthogonalization (small n_lanczos)
            for k in range(j + 1):
                w -= (V[:, k] @ w) * V[:, k]
        m = n_lanczos
        T = np.diag(alpha[:m]) + np.diag(beta_l[1:m], 1) + np.diag(beta_l[1:m], -1)
        evals, evecs = np.linalg.eigh(T)
        # v = V[:,0] = e0 in Lanczos basis; v^T f(H) v ≈ e0^T U f(D) U^T e0
        f = np.exp(-beta * (evals + shift))
        e0 = evecs[0, :]  # components of first basis vector
        acc += float(np.sum(e0 * e0 * f))
    # Hutchinson with normalized ±1: E[v^T A v] = Tr(A)/N * || not quite
    # With v random ±1/sqrt(N), E[v^T A v] = Tr(A)/N, so Tr ≈ N * mean
    # We normalized to unit length: ±1/sqrt(N), yes Tr ≈ N * mean(v^T f v)
    return N * acc / n_probe

def Z_exact_small(L, tw, beta, a):
    """Full dense ED in Sz sectors (no momentum) for L<=8."""
    H = B.full_H(L, tw)
    Szv = (1 - B.digits(L)).sum(1)
    total = 0.0
    for sz in range(-L, L+1):
        idx = np.nonzero(Szv == sz)[0]
        if len(idx) == 0: continue
        Hs = H[idx][:, idx].toarray().astype(float)
        ev = np.linalg.eigvalsh(Hs)
        total += float(np.exp(-beta * (ev + a * L)).sum())
    return total

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--Lmin', type=int, default=4)
    ap.add_argument('--Lmax', type=int, default=12)
    ap.add_argument('--tw', default='IP')
    ap.add_argument('--mode', default='auto')  # auto|dense|hutch
    args = ap.parse_args()
    results = {}
    t0 = time.time()
    for L in range(args.Lmin, args.Lmax + 1):
        for tw in args.tw:
            key = f'L{L}_{tw}'
            t1 = time.time()
            if args.mode == 'hutch' or (args.mode == 'auto' and L >= 14):
                z = hutchinson_Z(L, tw, BETA0, A, n_probe=48, n_lanczos=80, seed=L*10+ord(tw))
                method = 'hutchinson'
            elif L <= 8:
                z = Z_exact_small(L, tw, BETA0, A)
                method = 'dense_sz'
            else:
                z = dense_block_eigh_contrib(L, tw, BETA0, A)
                method = 'bloch'
            results[key] = {'Z': z, 'method': method, 'seconds': time.time() - t1}
            print(key, method, z, f'{results[key]["seconds"]:.2f}s', flush=True)
            json.dump(results, open(CACHE / 'thermal_partial.json', 'w'), indent=2)
    results['_meta'] = {'beta': BETA0, 'a': A, 'total_seconds': time.time() - t0,
                        'label': 'NUMERICAL float thermal'}
    json.dump(results, open(CACHE / f'thermal_L{args.Lmin}_{args.Lmax}.json', 'w'), indent=2)
    print('done', time.time() - t0)
