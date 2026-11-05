"""T1 pipeline: purification/TEBD Y ~ exp(-tau (H+cL)) for periodic spin-1 Heisenberg, global SVD truncation to bond chi
(the open_claims/ising_mps.py pattern: site-grouped (s_k a_k) open MPS, local dim 9), and the squaring ladder.
Rigour of eta: Etilde = float64 midpoints of the arb ladder (exact_arb.py) with an entrywise bound err_k, so
 eta = ||Y - E||_F <= fl||Y - Etilde||_F (1+1e-7) + err_k * 3^L        [IEEE standard model; Higham, N <= 4.3e7]
(the (1+1e-7) absorbs gamma_N rounding of the sum of squares; same labelled assumption as thermal_arb float mode)."""
import os, sys, json, time, numpy as np
from common import *
from flint import arb
GAMMA = 1e-7
def flipidx(L, st): return (3**L - 1) - st
_cache = {}
def exact(L, k):
    key = (L, k)
    if key in _cache: return _cache[key]
    n = 3**L; E = np.zeros((n, n)); err = 0.0; Z = arb(0)
    for M in range(0, L + 1):
        z = np.load(f'{D}/cache/E_L{L}_M{M}.npz')
        st, mid, e = z['st'], z['mids'][k], float(z['errs'][k]); err = max(err, e)
        Zm = arb(str(z['Zs'][k]))
        E[np.ix_(st, st)] = mid; Z += Zm
        if M > 0:
            f = flipidx(L, st); E[np.ix_(f, f)] = mid; Z += Zm
    errF = err * n * (1 + 1e-12)  # sqrt(n^2) entries
    _cache.clear(); _cache[key] = (E, errF, Z)
    return E, errF, Z
def fro(A): return float(np.sqrt(np.einsum('ij,ij->', A, A, optimize=True)))
def eta_true(Y, L, k):
    E, errF, Z = exact(L, k)
    return fro(Y - E) * (1 + GAMMA) + errF, Z
def Zbounds(Y, eta):
    nY = fro(Y); lo = max(0.0, nY * (1 - GAMMA) - eta)**2 * (1 - 1e-12); hi = (nY * (1 + GAMMA) + eta)**2 * (1 + 1e-12)
    return lo, hi, nY
def truncate(Y, L, chi):
    """Y: (3^L,3^L) operator. Returns (Ytrunc, eps) with eps = fl||Ytrunc - Y||_F (measured)."""
    n = 3**L
    T = Y.reshape([3] * (2 * L)).transpose([x for k in range(L) for x in (k, L + k)]).reshape([9] * L)
    rest = T.reshape(1, -1); r = 1; cores = []
    for k in range(L - 1):
        rest = rest.reshape(r * 9, -1); rows, cols = rest.shape
        if min(rows, cols) <= chi:          # exact at this cut
            if rows <= cols: cores.append(np.eye(rows).reshape(r, 9, rows)); r = rows
            else: Q, R = np.linalg.qr(rest); cores.append(Q.reshape(r, 9, cols)); rest = R; r = cols
            continue
        if rows <= cols:
            G = rest @ rest.T; w, U = np.linalg.eigh(G); U = U[:, ::-1][:, :chi]
        else:
            Q, R = np.linalg.qr(rest); Ur, S, Vt = np.linalg.svd(R); U = Q @ Ur[:, :chi]
        cores.append(U.reshape(r, 9, chi)); rest = U.T @ rest; r = chi
    out = rest.reshape(r, 9)
    for c in cores[::-1]: out = np.tensordot(c, out.reshape(c.shape[2], -1), axes=([2], [0])).reshape(c.shape[0], -1)
    out = out.reshape([9] * L).reshape([3] * (2 * L))
    out = out.transpose([2 * k for k in range(L)] + [2 * k + 1 for k in range(L)]).reshape(n, n)
    return out, fro(out - Y) * (1 + GAMMA)
def gates(L, dt):
    w, V = np.linalg.eigh(hbond)
    G = lambda t: ((V * np.exp(-t * (w + float(C_SHIFT)))) @ V.T).reshape(3, 3, 3, 3)
    b = bonds(L); half = G(dt / 2); full = G(dt)
    return [(i, j, half) for (i, j) in b[:-1]] + [b[-1] + (full,)] + [(i, j, half) for (i, j) in b[:-1][::-1]]
def apply(Y, i, j, G):
    Y = np.tensordot(G, Y, axes=([2, 3], [i, j])); return np.moveaxis(Y, [0, 1], [i, j])
def tebd(L, tau, chi, steps, snaps=(), Y0=None, every=1):
    n = 3**L; dt = tau / steps; seq = gates(L, dt)
    Y = (np.eye(n) if Y0 is None else Y0).reshape([3] * (2 * L)); eps = []; out = {}
    for s in range(1, steps + 1):
        for (i, j, G) in seq: Y = apply(Y, i, j, G)
        if chi is not None and s % every == 0:
            Ym, e = truncate(Y.reshape(n, n), L, chi); Y = Ym.reshape([3] * (2 * L)); eps.append((s * dt, e))
        if s in snaps: out[s] = Y.reshape(n, n).copy()
    return Y.reshape(n, n), eps, out
