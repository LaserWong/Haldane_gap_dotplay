"""Exact moment-pencil lower endpoints, given an external spectral count.

All arrays use exact rational entries. Floating generalized eigenvalues are only
endpoint proposals. The acceptance criterion is exact symmetric inertia.
"""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import eigvalsh
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from low_band_certificate import exact_inertia, lower_round


def certify(G, A, B, a, digits=12):
    """Return all k lower endpoints; caller must prove lambda_(k+1) >= a.

    G=W*W, A=W*H*W, B=(HW)*(HW) must include all ambient leakage. The
    moments alone cannot verify the external spectral-count hypothesis.
    """
    G, A, B = (np.asarray(x, dtype=object) for x in (G, A, B))
    a = F(a)
    k = len(G)
    assert all(x.shape == (k, k) for x in (G, A, B))
    assert exact_inertia(G) == (0, 0, k)
    K = A - a * G
    S = B - 2*a*A + a*a*G
    assert exact_inertia(K) == (k, 0, 0)
    assert exact_inertia(S) == (0, 0, k)
    mu = eigvalsh(np.array(K, float), np.array(S, float))
    result = []
    for i in range(k):
        candidate = float(a) + 1/mu[k-1-i]
        endpoint = min(lower_round(candidate, digits), a-F(1, 10**digits))
        step = F(1, 10**digits)
        while True:
            counts = exact_inertia(B-(a+endpoint)*A+a*endpoint*G)
            if counts[0] >= k-i:
                break
            endpoint -= step
            step *= 2
        result.append(dict(index_one_based=i+1, lower=str(endpoint),
                           moment_pencil_inertia=list(counts)))
    return dict(external_cutoff=str(a), external_count_required=k,
                cutoff_ritz_inertia=list(exact_inertia(K)),
                shifted_squared_moment_inertia=list(exact_inertia(S)),
                endpoints=result)
