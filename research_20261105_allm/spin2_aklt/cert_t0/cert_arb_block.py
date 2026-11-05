"""Independent residual certificate for one Sz=0 symmetry block of open n-chain P3+P4.

Removes trust in LAPACK dpotrf's rounding model (Higham/Rump a-priori bounds).
Instead: treat the computed Cholesky factor R as an arbitrary dyadic matrix we chose;
rigorously bound ||R^T R - (Ab - c I)||_2 and ||R^{-1}||_2; conclude
  lambda_min(M) >= c + 1/||R^{-1}||_2^2 - rho - E_build - delta_shift
where M = A* + U is the exact (rational + dyadic) block matrix, Ab is its float
construction, and E_build bounds ||Ab - M||_2 as in CERT_T0.md.

Trusted base after this script: IEEE-754 round-to-nearest for the *explicit*
GEMM / triangular-solve / abs-sum reductions we invoke (with Higham gamma_n
a-priori bounds on those ops), python-flint only if used for cross-checks,
and the exact-rational kernel / bond facts from CERT_T0.md. NOT trusted:
internal OpenBLAS dpotrf algorithms.

Usage: python3 cert_arb_block.py n r f t_num t_den c
Writes cert_arb_n{n}_r{r:+d}_f{f:+d}_t{num}_{den}.json and optional R factor npz.
"""
from __future__ import annotations
import os, sys, json, time, math
import numpy as np
import scipy.sparse as sp
from fractions import Fraction as Fr
from scipy.linalg import lapack

t_wall0 = time.time()
n, r, f = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
t = Fr(int(sys.argv[4]), int(sys.argv[5]))
c = float(sys.argv[6])
save_R = os.environ.get("SAVE_R", "0") == "1"
u = 2.0 ** -53
eta = 2.0 ** -1074
gam = lambda k: (k * u) / (1.0 - k * u) if k * u < 0.5 else float("inf")


def norm2_via_1inf(Mabs: np.ndarray) -> tuple[float, float, float]:
    """Upper bound ||M||_2 <= sqrt(||M||_1 ||M||_inf) for entrywise-abs matrix Mabs."""
    # column / row sums with a mild gamma inflation for the summation rounding
    d = Mabs.shape[0]
    gsum = gam(d) if d else 0.0
    col = Mabs.sum(axis=0)
    row = Mabs.sum(axis=1)
    # fl(sum) <= sum + gam_d * sum_||  =>  true_sum <= fl_sum / (1-gam) roughly
    # safer: true_sum <= fl_sum + gam_d * fl_sum_abs = fl_sum*(1+gam) when all nonnegative
    n1 = float(col.max()) * (1.0 + gsum)
    ninf = float(row.max()) * (1.0 + gsum)
    return math.sqrt(n1 * ninf), n1, ninf


B = json.load(open("bond_exact.json"))
hh = np.array(B["hhat"], dtype=np.float64)

# --- Sz=0 basis + symmetry block (identical construction to cert_block.py) ---
digs = np.array(np.meshgrid(*[np.arange(5)] * n, indexing="ij")).reshape(n, -1).T
digs = digs[(digs - 2).sum(1) == 0]
N = len(digs)
pw = 5 ** np.arange(n - 1, -1, -1)
idx = digs @ pw
assert np.all(np.diff(idx) > 0)


def lookup(dg):
    return np.searchsorted(idx, dg @ pw)


gR = lookup(digs[:, ::-1])
gF = lookup(4 - digs)
gRF = gR[gF]
chi = {"e": 1, "R": r, "F": f, "RF": r * f}
rep = np.minimum.reduce([np.arange(N), gR, gF, gRF])
ok_cols = []
for x in range(N):
    if rep[x] != x:
        continue
    orb = {}
    bad = False
    for g, img in (("e", x), ("R", gR[x]), ("F", gF[x]), ("RF", gRF[x])):
        if img in orb and orb[img] != chi[g]:
            bad = True
        orb[img] = chi[g]
    if not bad:
        ok_cols.append(orb)
db = len(ok_cols)
rows = np.concatenate([list(o.keys()) for o in ok_cols])
cidx = np.concatenate([[j] * len(o) for j, o in enumerate(ok_cols)])
vals = np.concatenate([list(o.values()) for o in ok_cols]).astype(np.float64)
P = sp.csr_matrix((vals, (rows, cidx)), shape=(N, db))
Lam = np.array([len(o) for o in ok_cols], dtype=np.float64)
assert np.all(np.isin(Lam, [1, 2, 4]))

# --- Hamiltonian float build ---
nz = [(p, q, hh[p, q]) for p in range(25) for q in range(25) if hh[p, q] != 0.0]
RR, CC, VV = [], [], []
for i in range(n - 1):
    pair = digs[:, i] * 5 + digs[:, i + 1]
    for p, q, v in nz:
        ok = np.nonzero(pair == q)[0]
        if len(ok) == 0:
            continue
        nd = digs[ok].copy()
        nd[:, i] = p // 5
        nd[:, i + 1] = p % 5
        RR.append(lookup(nd))
        CC.append(ok)
        VV.append(np.full(len(ok), v, dtype=np.float64))
H = sp.csr_matrix(
    (np.concatenate(VV), (np.concatenate(RR), np.concatenate(CC))), shape=(N, N)
)
rs_h = np.abs(hh).sum(1).max() * (1 + 1e-12)
Habs_inf = (n - 1) * rs_h * (1 + gam(n))
tf = float(t)
Ab = (P.T @ H @ P).toarray()
Ab[np.diag_indices(db)] -= tf * Lam

# --- kernel update (dyadic W; any vectors OK for logic) ---
K = json.load(open(f"kernel_vectors_n{n}.json"))
wsite = np.array([math.sqrt(math.factorial(k) * math.factorial(4 - k)) for k in range(5)])
Vk = np.zeros((N, len(K)), dtype=np.float64)
for j, (nm, lst) in enumerate(K.items()):
    ks = np.array([e[0] for e in lst])
    cs = np.array([float(e[1]) for e in lst], dtype=np.float64)
    Vk[lookup(ks), j] = cs * np.prod(wsite[ks], axis=1)
Y = (P.T @ Vk) / Lam[:, None]
Vb = P @ Y
Q, s_, _ = np.linalg.svd(Vb, full_matrices=False)
kb = int((s_ > 1e-8 * max(s_.max(), 1e-300)).sum()) if s_.max() > 0 else 0
Q = Q[:, :kb]
W = (P.T @ Q) if kb else np.zeros((db, 0), dtype=np.float64)
for j in range(kb):
    Ab += np.outer(W[:, j], W[:, j])
wnorm2 = float((W**2).sum()) * (1 + 1e-10)

# --- E_build (same formula as cert_block.py / CERT_T0.md) ---
P2 = 4.0
E_H = gam(n) * Habs_inf * P2
E_PHP = gam(16) * (1 + gam(n)) * Habs_inf * P2
E_t = abs(Fr(tf) - t) * P2 + u * (P2 * Habs_inf * (1 + 1e-6) + float(t) * P2)
rowsum_abs = np.abs(Ab).sum(1).max() * (1 + 1e-10)
E_U = gam(kb + 1) * (rowsum_abs + wnorm2) if kb else 0.0
E_build = (E_H + E_PHP + float(E_t) + E_U) * (1 + 1e-6)

# --- shift and Cholesky (discovery only; R kept as dyadic witness) ---
Ac = Ab.copy()
Ac[np.diag_indices(db)] -= c
delta_shift = u * (float(np.abs(np.diag(Ac)).max()) + c) * (1 + 1e-10)
# free Ab
del Ab

Awork = np.array(Ac, order="F")
Rfac, info = lapack.dpotrf(Awork, lower=0, clean=1, overwrite_a=1)
out = dict(
    n=n, r=r, f=f, t=str(t), c=c, N=N, db=db, kb=kb,
    E_build=float(E_build), delta_shift=float(delta_shift), info=int(info),
    method="residual_RTR_inv",
)
if info != 0:
    out.update(CERTIFIED=False, reason="chol_fail_discovery")
    out["sec"] = time.time() - t_wall0
    print(json.dumps(out), flush=True)
    json.dump(out, open(f"arb/cert_arb_n{n}_r{r:+d}_f{f:+d}_t{sys.argv[4]}_{sys.argv[5]}.json", "w"), indent=1)
    sys.exit(0)

R = np.triu(np.array(Rfac, order="C"))  # dyadic witness; discard Rfac
del Rfac, Awork
diagR_min = float(np.min(np.abs(np.diag(R))))
out["diagR_min"] = diagR_min
if diagR_min <= 0.0:
    out.update(CERTIFIED=False, reason="zero_pivot_in_R")
    out["sec"] = time.time() - t_wall0
    print(json.dumps(out), flush=True)
    json.dump(out, open(f"arb/cert_arb_n{n}_r{r:+d}_f{f:+d}_t{sys.argv[4]}_{sys.argv[5]}.json", "w"), indent=1)
    sys.exit(0)

if save_R:
    np.savez_compressed(f"arb/R_n{n}_r{r:+d}_f{f:+d}.npz", R=R)

# --- residual rho >= ||R^T R - Ac||_2 ---
# Compute fl(R.T @ R); bound GEMM rounding by gamma_db * |R|^T |R|
t1 = time.time()
Bmat = R.T @ R
sec_RTR = time.time() - t1
E = Bmat - Ac
del Bmat, Ac
E2, E1, Einf = norm2_via_1inf(np.abs(E))
del E
t1 = time.time()
# radius matrix absolute product
Rabs = np.abs(R)
APabs = Rabs.T @ Rabs
sec_AP = time.time() - t1
g = gam(db)
# true ||R.T@R - Ac|| <= ||fl(RTR)-Ac|| + ||fl(RTR)-RTR||
# ||fl(RTR)-RTR||_2 <= gamma_db * |||R|^T |R||| _2
rad2, _, _ = norm2_via_1inf(g * APabs)
del APabs
rho = E2 + rad2
out.update(rho=float(rho), E2_fl=float(E2), rad2_gemm=float(rad2), sec_RTR=sec_RTR, sec_AP=sec_AP)

# --- approximate inverse X ~= R^{-1} as dyadic witness (via dtrtri) ---
t1 = time.time()
Xwork = np.array(R, order="F")
_, info2 = lapack.dtrtri(Xwork, lower=0, unitdiag=0, overwrite_c=1)
sec_trtri = time.time() - t1
out["info_trtri"] = int(info2)
if info2 != 0:
    out.update(CERTIFIED=False, reason="trtri_fail")
    out["sec"] = time.time() - t_wall0
    print(json.dumps(out), flush=True)
    json.dump(out, open(f"arb/cert_arb_n{n}_r{r:+d}_f{f:+d}_t{sys.argv[4]}_{sys.argv[5]}.json", "w"), indent=1)
    sys.exit(0)
X = np.triu(np.array(Xwork, order="C"))
del Xwork

# F = I - R X  (X is our chosen dyadic approx inverse; not assumed exact)
t1 = time.time()
RX = R @ X
sec_RX = time.time() - t1
F = -RX
F[np.diag_indices(db)] += 1.0
del RX
F2_fl, _, _ = norm2_via_1inf(np.abs(F))
del F
# GEMM radius for R@X
RXrad = Rabs @ np.abs(X)
del Rabs
Frad2, _, _ = norm2_via_1inf(g * RXrad)
del RXrad
F2 = F2_fl + Frad2
X2, _, _ = norm2_via_1inf(np.abs(X))
del X

out.update(
    F2=float(F2), F2_fl=float(F2_fl), Frad2_gemm=float(Frad2),
    X2_bound=float(X2), sec_trtri=sec_trtri, sec_RX=sec_RX,
)

if not (F2 < 1.0):
    out.update(CERTIFIED=False, reason="inv_residual_ge_1", lam_min_M_lower=None)
else:
    Rinv2 = X2 / (1.0 - F2)
    lmin_RTR = 1.0 / (Rinv2 * Rinv2)
    # ||RTR - (M - c I)|| <= rho + E_build + delta_shift
    # lambda_min(M - c I) >= lmin_RTR - rho - E_build - delta_shift
    # lambda_min(M) >= c + that
    lam = c + lmin_RTR - rho - float(E_build) - float(delta_shift)
    out.update(
        Rinv2_bound=float(Rinv2),
        lmin_RTR_lower=float(lmin_RTR),
        lam_min_AstarU_lower=float(lam),
        CERTIFIED=bool(lam > 0.0),
    )

out["sec"] = time.time() - t_wall0
print(json.dumps(out), flush=True)
json.dump(
    out,
    open(f"arb/cert_arb_n{n}_r{r:+d}_f{f:+d}_t{sys.argv[4]}_{sys.argv[5]}.json", "w"),
    indent=1,
)
