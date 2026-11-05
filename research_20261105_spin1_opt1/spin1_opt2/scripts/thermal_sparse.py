#!/usr/bin/env python3
"""Sparse Lanczos approx to Z_L^g = Tr exp(-beta(H+aL)). NUMERICAL, truncation-aware."""
import os, sys, json, time, argparse
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
import numpy as np
from scipy.sparse.linalg import eigsh
sys.path.insert(0, '/workspace/haldane_chat_bundle/runs/thermal_arb')
import blocks as B
from pathlib import Path

CACHE = Path('/workspace/haldane_chat_bundle/runs/spin1_opt2/cache')
CACHE.mkdir(parents=True, exist_ok=True)
BETA0, A = 49/4, 700741/500000

def Z_sparse(L, tw, k=400, beta=BETA0, a=A):
    """Lowest-k eigenvalues of sparse H, plus crude high-energy bound."""
    t0 = time.time()
    H = B.full_H(L, tw)  # scipy sparse CSR, integer
    dim = H.shape[0]
    assert dim == 3**L
    # Shift: want evals of H; use which='SA'
    # For large dim, request k; if fails reduce k
    kk = min(k, dim - 2)
    print(f'L={L} {tw} dim={dim} requesting k={kk}', flush=True)
    evals = eigsh(H.astype(np.float64), k=kk, which='SA',
                  return_eigenvectors=False, tol=1e-10, maxiter=dim)
    evals = np.sort(evals)
    shifted = evals + a * L
    contrib = np.exp(-beta * shifted)
    Z_partial = float(contrib.sum())
    # Tail bound: remaining dim-k states each ≤ exp(-beta*(evals[-1]+aL))
    # (underestimate of energy => overestimate of contrib — upper on Z)
    e_cut = float(evals[-1] + a * L)
    Z_tail_up = (dim - kk) * math.exp(-beta * e_cut) if e_cut > 0 else float('inf')
    # Also a lower: Z_partial alone
    out = {
        'L': L, 'tw': tw, 'k': kk, 'dim': dim,
        'Z_partial': Z_partial,
        'Z_tail_up': Z_tail_up,
        'Z_up': Z_partial + Z_tail_up,
        'E_min': float(evals[0]),
        'E_cut': float(evals[-1]),
        'shifted_min': float(shifted[0]),
        'shifted_cut': e_cut,
        'n_below_1': int((shifted < 1).sum()),
        'n_below_2': int((shifted < 2).sum()),
        'seconds': time.time() - t0,
        'label': 'NUMERICAL',
    }
    print(json.dumps({k: out[k] for k in out if k != 'label'}, indent=2), flush=True)
    return out

import math
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', type=int, required=True)
    ap.add_argument('--tw', default='I')
    ap.add_argument('--k', type=int, default=400)
    args = ap.parse_args()
    # Validate on L=10 vs known
    if args.L <= 10:
        pass
    out = Z_sparse(args.L, args.tw, k=args.k)
    json.dump(out, open(CACHE / f'sparse_L{args.L}_{args.tw}.json', 'w'), indent=2)
