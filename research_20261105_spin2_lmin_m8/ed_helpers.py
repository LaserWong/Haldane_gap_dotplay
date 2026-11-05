"""NONRIGOROUS float ED (Lanczos) for periodic spin-S Heisenberg chain: E0(L), lowest levels in Sz=0,1.
Estimates only (cross-check / small-L physics)."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, sys, json, time
def sector(S, L, M):
    d = int(2*S+1); m = np.arange(d) - S  # local m values
    # enumerate states with total Sz = M (as integer digits base d)
    states = np.array([0], dtype=np.int64); tot = np.array([0.0])
    for site in range(L):
        states = (states[:, None] * d + np.arange(d)[None, :]).ravel()
        tot = (tot[:, None] + m[None, :]).ravel()
        # prune: remaining sites can change tot by at most S*(L-site-1)
        rem = S * (L - site - 1); keep = np.abs(tot - M) <= rem + 1e-9
        states, tot = states[keep], tot[keep]
    return states
def ham(S, L, states, twist=False):
    d = int(2*S+1); m = np.arange(d) - S
    idx = {}; order = np.argsort(states); sorted_states = states[order]
    dim = len(states); digits = np.zeros((dim, L), dtype=np.int64); x = states.copy()
    for site in range(L-1, -1, -1): digits[:, site] = x % d; x //= d
    pw = d ** np.arange(L-1, -1, -1)
    diag = np.zeros(dim); rows=[]; cols=[]; vals=[]
    for i in range(L):
        j = (i+1) % L; a = digits[:, i]; b = digits[:, j]
        diag += m[a] * m[b]
        # S+_i S-_j /2 : a->a+1, b->b-1
        for (da, db) in ((1, -1), (-1, 1)):
            ok = (a+da >= 0) & (a+da < d) & (b+db >= 0) & (b+db < d)
            ma, mb = m[a[ok]], m[b[ok]]
            ca = np.sqrt(S*(S+1) - ma*(ma+da)); cb = np.sqrt(S*(S+1) - mb*(mb+db))
            new = states[ok] + da*pw[i] + db*pw[j]
            pos = order[np.searchsorted(sorted_states, new)]
            rows.append(np.nonzero(ok)[0]); cols.append(pos); vals.append((-1 if twist and i == L-1 else 1)*0.5*ca*cb)
    H = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(dim, dim)).tocsr()
    return H + sp.diags(diag)
