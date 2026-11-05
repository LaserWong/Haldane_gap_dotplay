"""NUMERICAL sanity test of the operator inequality behind Lemma GM' (CERT_ALLM.md):
  X := (H°)^2 + beta H° - alpha * sum_k B_k^2  >= 0   on rings  m in [n, 2n],  alpha = 1/q(1), beta = alpha*sum c^2 - 1,
valid whenever C_m(e) = q(e)+q(m-e) <= q(1) for 2<=e<=m-2. Negative control: weights violating the hypothesis.
Models: spin-1 AKLT (h=P2), spin-2 h=P3+P4. Sz=0 sector (all operators conserve Sz)."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, sys, json
def proj_bond(S, Js):
    d = int(2*S+1); mm = np.arange(d)-S
    Sz = np.diag(mm); Sp = np.zeros((d, d))
    for i in range(d-1): Sp[i+1, i] = np.sqrt(S*(S+1)-mm[i]*(mm[i]+1))
    x = np.kron(Sz, Sz)+0.5*(np.kron(Sp, Sp.T)+np.kron(Sp.T, Sp))
    ev, U = np.linalg.eigh(x); J = np.rint((-1+np.sqrt(1+4*(2*ev+2*S*(S+1))))/2)
    P = sum(np.outer(U[:, k], U[:, k]) for k in range(len(ev)) if J[k] in Js)
    return P, d, mm
def basis(m, d, mm):
    digs = np.array(np.meshgrid(*[np.arange(d)]*m, indexing='ij')).reshape(m, -1).T
    return digs[mm[digs].sum(1) == 0]
def bond_ops(m, d, mm, h):
    digs = basis(m, d, mm); N = len(digs); pw = d**np.arange(m-1, -1, -1); idx = digs@pw
    ops = []
    for i in range(m):
        j = (i+1) % m; pair = digs[:, i]*d+digs[:, j]; R = []; C = []; V = []
        for p in range(d*d):
            for qq in range(d*d):
                if abs(h[p, qq]) < 1e-14: continue
                ok = np.nonzero(pair == qq)[0]
                if not len(ok): continue
                nd = digs[ok].copy(); nd[:, i] = p//d; nd[:, j] = p % d
                R.append(np.searchsorted(idx, nd@pw)); C.append(ok); V.append(np.full(len(ok), h[p, qq]))
        ops.append(sp.csr_matrix((np.concatenate(V), (np.concatenate(R), np.concatenate(C))), shape=(N, N)))
    return ops
def q(c, x): return sum(c[j]*c[j+x] for j in range(len(c)-x)) if x < len(c) else 0.0
def test(S, Js, n, m, c):
    h, d, mm = proj_bond(S, Js); ops = bond_ops(m, d, mm, h); H = sum(ops)
    a = 1/q(c, 1); b = a*sum(x*x for x in c)-1
    hyp = all(q(c, e)+q(c, m-e) <= q(c, 1)+1e-12 for e in range(2, m-1))
    X = H@H + b*H
    for k in range(m):
        Bk = sum(c[t]*ops[(k+t) % m] for t in range(n-1)); X = X - a*(Bk@Bk)
    X = (X+X.T)/2
    lam = np.linalg.eigvalsh(X.toarray())[0] if X.shape[0] <= 9000 else sla.eigsh(X, k=1, which='SA', tol=1e-10)[0][0]
    return dict(S=S, n=n, m=m, c=[round(x, 4) for x in c], hyp=hyp, lam_min=float(lam), dim=X.shape[0])
gmw = lambda n: [(n-1)+(n-2)*j-j*j for j in range(n-1)]
import os
CASES = os.environ.get('CASES')
res = []
for (S, Js, n, ms) in ([] if CASES=='rest' else  [(1, [2], 4, range(4, 9)), (1, [2], 5, range(5, 11)), (2, [3, 4], 4, range(4, 8)), (2, [3, 4], 5, range(5, 8))]):
    for m in ms:
        r = test(S, Js, n, m, gmw(n)); print(json.dumps(r), flush=True); res.append(r)
# negative control: weights violating hypothesis at small m
for (S, Js, n, m, c) in [(1, [2], 5, 6, [1, 0.2, 0.2, 1]), (1, [2], 5, 5, [1, 0.2, 0.2, 1]), (2, [3, 4], 5, 6, [1, 0.2, 0.2, 1])]:
    r = test(S, Js, n, m, c); r['negctl'] = True; print(json.dumps(r), flush=True); res.append(r)
json.dump(res, open('test_opineq.json', 'w'), indent=1)
