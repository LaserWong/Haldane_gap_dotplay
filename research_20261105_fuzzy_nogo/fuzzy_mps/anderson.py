"""FLOAT: Anderson cluster lower bound e0 >= E0_open(m)/(m-1) per bond (=per site on a ring with m <= L), and exact
E0(L) of the periodic ring (float Lanczos/eigh).  Rigorous versions would need certified lowest eigenvalues (cheap at
these sizes with thermal_arb/cert.py) -- not done; these numbers enter only the a-priori bound variants."""
import json, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla
from common import *
def H_open(m):
    I = sp.identity(3, format='csr'); hb = sp.csr_matrix(hbond); H = sp.csr_matrix((3**m, 3**m))
    for i in range(m - 1):
        H = H + sp.kron(sp.kron(sp.identity(3**i), hb), sp.identity(3**(m - i - 2)), format='csr')
    return H
out = {'open': {}, 'ring': {}}
for m in range(2, 12):
    H = H_open(m); e = sla.eigsh(H, k=1, which='SA', tol=1e-12)[0][0] if m > 4 else np.linalg.eigvalsh(H.toarray())[0]
    out['open'][m] = dict(E0=float(e), bound_per_site=float(e / (m - 1))); print('open', m, e, e / (m - 1), flush=True)
for L in (3, 4, 6, 8):
    H = Hdense(L) if L <= 6 else None
    e = np.linalg.eigvalsh(H)[0] if H is not None else min(sla.eigsh(Hblock_int(L, M)[1].astype(float), k=1, which='SA')[0][0] for M in (0, 1))
    out['ring'][L] = float(e); print('ring', L, e, e / L)
json.dump(out, open(f'{D}/anderson.json', 'w'), indent=1)
