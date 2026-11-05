"""FLOAT: operator-Schmidt (purification) spectrum of the EXACT E_k = exp(-tau_k(H+cL)) across every open-chain cut of the
site-grouped (s_k a_k) MPS used by the pipeline.  For each cut and k: chi needed so that the discarded relative Frobenius
weight at that cut is <= 1e-2, 1e-3, 1e-6.  A single TT-SVD at bond chi has relative error >= max_cut tail(chi) and
<= sqrt(sum_cut tail^2): this is the best one-shot truncation any chi-MPS pipeline could achieve."""
import sys, json, numpy as np
from pipeline import exact, fro
L = int(sys.argv[1]); out = {}
for k in (0, 3, 5, 6):
    E, _, _ = exact(L, k); nE = fro(E)
    T = E.reshape([3] * (2 * L)).transpose([x for j in range(L) for x in (j, L + j)]).reshape([9] * L)
    rk = {}
    for cut in range(1, L):
        Mx = T.reshape(9**cut, -1); G = Mx @ Mx.T if Mx.shape[0] <= Mx.shape[1] else Mx.T @ Mx
        w = np.clip(np.linalg.eigvalsh(G)[::-1], 0, None); tail = np.sqrt(np.maximum(np.cumsum(w[::-1])[::-1], 0)) / nE
        need = {tol: int(np.argmax(np.append(tail, 0) <= tol)) for tol in (1e-2, 1e-3, 1e-6)}
        rk[cut] = dict(maxrank=len(w), need=need, tail_at={c: float(tail[c]) if c < len(tail) else 0.0 for c in (16, 32, 64, 128, 256)})
        print(L, k, cut, len(w), need, {c: '%.2e' % v for c, v in rk[cut]['tail_at'].items()}, flush=True)
    out[k] = rk
json.dump(out, open(f'results/spectrum_L{L}.json', 'w'), indent=1)
