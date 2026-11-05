"""Rigorous (floating-point verified, Higham Thm 10.3 + Weyl) certificate that, on one symmetry block V_b of the Sz=0 sector
of the OPEN n-site chain H_n = sum_{i<n} (P3+P4)_{i,i+1}, H_n has at most k_b eigenvalues <= t.
Usage: python3 cert_block.py n r f t_num t_den c   (r,f in {+1,-1}: characters of reflection R and spin-flip F)
Logic (see CERT_T0.md):
 P (dim N x d_b, entries 0/+-1, orthogonal columns spanning V_b), Lam = P^T P = diag(|orbit|).
 A* = P^T H P - t Lam  is congruent (via Lam^{1/2}) to (H - t)|V_b, so #neg / #nonpos eigenvalues agree (Sylvester).
 U = sum_j w_j w_j^T (k_b float vectors, exactly PSD, rank <= k_b).  If A* + U > 0 then (Weyl/interlacing) A* has at most k_b
 eigenvalues <= 0, i.e. H|V_b has at most k_b eigenvalues <= t.
 Certificate of A* + U > 0: computed float matrix At with rigorous ||At - (A*+U)||_2 <= E, float Cholesky of fl(At - cI) succeeds,
 lambda_min(At) >= c - delta_shift - gamma_{d+1}||R||_F^2 - eta_term;  then lambda_min(A*+U) >= that - E > 0."""
import os, sys, json, time, numpy as np, scipy.sparse as sp
from fractions import Fraction as Fr
from scipy.linalg import lapack
t0 = time.time()
n, r, f = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
t = Fr(int(sys.argv[4]), int(sys.argv[5])); c = float(sys.argv[6])
u = 2.0**-53; eta = 2.0**-1074
gam = lambda k: k*u/(1-k*u)
B = json.load(open('bond_exact.json')); hh = np.array(B['hhat'])
# --- exact symmetry check of the bond: swap and flip (string-exact on sympy expressions, via sympy)
import sympy as sy
hx = [[sy.sympify(s) for s in row] for row in B['h_exact']]
sw = lambda p: (p % 5)*5 + p//5; fl_ = lambda p: (4 - p//5)*5 + (4 - p % 5)
assert all(sy.simplify(hx[p][q] - hx[sw(p)][sw(q)]) == 0 and sy.simplify(hx[p][q] - hx[fl_(p)][fl_(q)]) == 0
           for p in range(25) for q in range(25)), "bond not swap/flip invariant"
# --- Sz=0 basis
digs = np.array(np.meshgrid(*[np.arange(5)]*n, indexing='ij')).reshape(n, -1).T  # lexicographic
digs = digs[(digs - 2).sum(1) == 0]; N = len(digs)
pw = 5**np.arange(n-1, -1, -1); idx = digs @ pw
assert np.all(np.diff(idx) > 0)
def lookup(dg): return np.searchsorted(idx, dg @ pw)
gR = lookup(digs[:, ::-1]); gF = lookup(4 - digs); gRF = gR[gF]
assert np.all(idx[gR] == digs[:, ::-1] @ pw) and np.all(idx[gF] == (4-digs) @ pw)
chi = {'e': 1, 'R': r, 'F': f, 'RF': r*f}
# orbits
rep = np.minimum.reduce([np.arange(N), gR, gF, gRF])
cols = {}; ok_cols = []
for x in range(N):
    if rep[x] != x: continue
    orb = {}
    bad = False
    for g, img in (('e', x), ('R', gR[x]), ('F', gF[x]), ('RF', gRF[x])):
        if img in orb and orb[img] != chi[g]: bad = True
        orb[img] = chi[g]
    if not bad: ok_cols.append(orb)
db = len(ok_cols)
rows = np.concatenate([list(o.keys()) for o in ok_cols]); cidx = np.concatenate([[j]*len(o) for j, o in enumerate(ok_cols)])
vals = np.concatenate([list(o.values()) for o in ok_cols]).astype(float)
P = sp.csr_matrix((vals, (rows, cidx)), shape=(N, db))
Lam = np.array([len(o) for o in ok_cols], dtype=float)
assert np.all(np.isin(Lam, [1, 2, 4]))
# --- Hamiltonian (float, entries = single rounded bond entries on off-diagonals, sums of <= n-1 on diagonal)
R_, C_, V_ = [], [], []
nz = [(p, q, hh[p, q]) for p in range(25) for q in range(25) if hh[p, q] != 0.0]
for i in range(n-1):
    pair = digs[:, i]*5 + digs[:, i+1]
    for p, q, v in nz:
        ok = np.nonzero(pair == q)[0]
        if len(ok) == 0: continue
        nd = digs[ok].copy(); nd[:, i] = p//5; nd[:, i+1] = p % 5
        R_.append(lookup(nd)); C_.append(ok); V_.append(np.full(len(ok), v))
H = sp.csr_matrix((np.concatenate(V_), (np.concatenate(R_), np.concatenate(C_))), shape=(N, N))
rs_h = np.abs(hh).sum(1).max()*(1+1e-12)               # rigorous upper bound on max row abs-sum of |h|
Habs_inf = (n-1)*rs_h*(1+gam(n))                         # bound on ||Habs||_inf (and on ||H||, ||Hhat|| up to (1+gam7))
# --- block matrix
tf = float(t)
Ab = (P.T @ H @ P).toarray()
Ab[np.diag_indices(db)] -= tf*Lam                         # tf*Lam exact (power-of-2 scaling); one rounding per diag entry
# kernel-vector update from EXACT VBS vectors projected onto V_b (any float vectors would do for the logic)
K = json.load(open(f'kernel_vectors_n{n}.json'))
import math
wsite = np.array([math.sqrt(math.factorial(k)*math.factorial(4-k)) for k in range(5)])
Vk = np.zeros((N, len(K)))
for j, (nm, lst) in enumerate(K.items()):
    ks = np.array([e[0] for e in lst]); cs = np.array([float(e[1]) for e in lst])
    Vk[lookup(ks), j] = cs*np.prod(wsite[ks], axis=1)
# project onto V_b: P Lam^{-1} P^T v
Y = (P.T @ Vk)/Lam[:, None]; Vb = P @ Y
Q, s_, _ = np.linalg.svd(Vb, full_matrices=False); kb = int((s_ > 1e-8*max(s_.max(), 1e-300)).sum()) if s_.max() > 0 else 0
Q = Q[:, :kb]
res_kernel = float(np.linalg.norm(H @ Q)) if kb else 0.0
W = (P.T @ Q) if kb else np.zeros((db, 0))
for j in range(kb): Ab += np.outer(W[:, j], W[:, j])
wnorm2 = float((W**2).sum())*(1+1e-10)
# --- rigorous build-error bound E (2-norm), see CERT_T0.md section 3
P2 = 4.0                                                  # ||P||_2^2 = max |orbit|
E_H = gam(n)*Habs_inf*P2                                  # bond rounding (u) + diagonal summation (gam_{n-2}) -> gam_n, times ||P||^2
E_PHP = gam(16)*(1+gam(n))*Habs_inf*P2                    # sparse triple product: <= 16 summands per entry, any order
E_t = (abs(tf - float(0) ) * 0 + abs(Fr(tf) - t))*P2 + u*(P2*Habs_inf*(1+1e-6) + float(t)*P2)   # t rounding + diag subtraction
rowsum_abs = np.abs(Ab).sum(1).max()*(1+1e-10)
E_U = gam(kb+1)*(rowsum_abs + wnorm2) if kb else 0.0     # rounding of the dense rank-k additions
E = (E_H + E_PHP + float(E_t) + E_U)*(1+1e-6)
# --- shifted Cholesky (in place, upper triangle)
Ab[np.diag_indices(db)] -= c
diagmax = np.abs(np.diag(Ab)).max()
delta_shift = u*(diagmax + c)*(1+1e-10)
dg = np.diag(Ab).copy(); assert np.all(dg > 0)
trace_up = float(dg.sum())*(1+gam(db))*(1+1e-12)
g1 = gam(db+1)
rump = g1/(1-g1)*trace_up + db*3*(2*db + float(dg.max()))*eta    # ||Delta(A)||_2 <= ||Delta||_F-free bound: alpha<=g1 => ||alpha d d^T||<=g1*||d||^2
mem = Ab.T                                                # F-contiguous view of the (symmetric) C array
Rm, info = lapack.dpotrf(mem, lower=0, clean=0, overwrite_a=1)
out = dict(n=n, r=r, f=f, t=str(t), c=c, N=N, db=db, kb=kb, kernel_residual_float=res_kernel,
           E_build=E, info=int(info))
if info == 0:
    fro2 = 0.0; minabs = np.inf
    for i0 in range(0, db, 1000):
        blk = np.triu(Rm[i0:i0+1000, :], k=i0) if False else None
    # Rm is the F-ordered factor; its upper triangle holds R. Accumulate row-wise on the transposed C view.
    RC = Rm.T                                             # C-contiguous; RC[j, i] = R[i, j]; R upper => RC lower
    for j0 in range(0, db, 512):
        blk = RC[j0:j0+512, :]
        msk = np.tril(np.ones(blk.shape, bool), k=j0)
        bb = np.where(msk, blk, 0.0)
        fro2 += float((bb*bb).sum())
        nzv = np.abs(bb[bb != 0]); minabs = min(minabs, nzv.min() if nzv.size else np.inf)
    assert np.isfinite(fro2)
    fro2 *= (1 + 1e-6)
    chol_err = gam(db+1)*fro2
    eta_term = 4*(db+1)*(2*(db+2) + diagmax)*eta*10      # underflow allowance (Demmel/Rump model), absurdly generous
    lam_At = c - delta_shift - chol_err - eta_term
    lam_true = lam_At - E
    lam_At_rump = c - delta_shift - rump
    out.update(rump_bound=rump, lam_min_AstarU_lower_rump=lam_At_rump - E, CERTIFIED_rump=bool(lam_At_rump - E > 0))
    out.update(R_fro2=fro2, chol_err=chol_err, delta_shift=delta_shift, min_nonzero_absR=float(minabs),
               lam_min_At_lower=lam_At, lam_min_AstarU_lower=lam_true, CERTIFIED=bool(lam_true > 0))
else:
    out.update(CERTIFIED=False)
out['sec'] = time.time() - t0
print(json.dumps(out), flush=True)
json.dump(out, open(f'cert_n{n}_r{r:+d}_f{f:+d}_t{sys.argv[4]}_{sys.argv[5]}.json', 'w'), indent=1)
