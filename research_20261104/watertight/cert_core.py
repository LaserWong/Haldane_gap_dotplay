# Watertight eigenvalue-enclosure core (independent re-implementation, with an explicit mod-2^64 wrap guard).
#
# Theorem used (H exact Hermitian m x m with ||H||_2 <= Hn; Vt arbitrary m x m; Lt real, sorted ascending):
#   eta >= ||Vt^* Vt - I||_2 with eta < 1,   r >= ||H Vt - Vt Lt||_2
#   => ||H - Vt Lt Vt^*||_2 <= Hn*eta + r*sqrt(1+eta) =: delta
#      [H - Vt Lt Vt^* = H (I - Vt Vt^*) + (H Vt - Vt Lt) Vt^*, ||I - Vt Vt^*|| = ||I - Vt^* Vt|| (square Vt),
#       ||Vt|| <= sqrt(1+eta)]
#   Ostrowski (Horn-Johnson Thm 4.5.9): lambda_i(Vt Lt Vt^*) = theta_i Lt_i, theta_i in [s_min^2, s_max^2]
#       subset [1-eta, 1+eta]; Weyl: |mu_i(H) - lambda_i(Vt Lt Vt^*)| <= delta.
#   => the i-th smallest eigenvalue mu_i(H) lies in [Lt_i - (eta|Lt_i|+delta), Lt_i + (eta|Lt_i|+delta)].
# Vt = Vint/2^SV, Lt = Lint/2^SL dyadic; H = Hs/2^SL + dH, dH bounded entrywise by arb balls.
# Exact integer products: limbs so every float64 partial sum is an integer < 2^53 (exact), recombined in int64,
# i.e. modulo 2^64.  WRAP GUARD (new): the same product is also evaluated in plain float64 (F); with the a priori
# bound |F - T| <= E_fl < 2^60 (asserted from |Vint| <= 2^39, row/col sizes), and the check |F - c| <= 2^61 for
# the wrapped residue c, we get |T - c| < 2^62 < 2^63 and T = c (mod 2^64)  =>  T = c exactly.
import numpy as np, scipy.sparse as sp, math
from flint import arb, acb
SV, SL, LB = 38, 30, 19
TWO61 = float(2**61)
def _i64(F):
    assert np.abs(F).max() < 2.0**53
    return F.astype(np.int64)
def _limbs(X):
    Xi = np.rint(X*2.0**SV).astype(np.int64)
    assert np.abs(Xi).max() <= 2**39
    A = Xi >> LB; B = Xi - (A << LB)
    return Xi, A.astype(np.float64), B.astype(np.float64)
def _gram(A1, B1, A2, B2):
    with np.errstate(over='ignore'):
        return (_i64(A1.T@A2) << (2*LB)) + ((_i64(A1.T@B2) + _i64(B1.T@A2)) << LB) + _i64(B1.T@B2)
def _spmul(Hc, Xi):
    C2 = Xi >> 26; C1 = (Xi >> 13) & 8191; C0 = Xi & 8191
    with np.errstate(over='ignore'):
        return (_i64(Hc@C2.astype(float)) << 26) + (_i64(Hc@C1.astype(float)) << 13) + _i64(Hc@C0.astype(float))
def _guard(c, F):
    # c: int64 residues (true value T = c mod 2^64); F: float64 approximation of T with |F-T| <= E_fl < 2^60
    assert np.abs(F - c.astype(np.float64)).max() <= TWO61, 'wrap guard failed'
def _sqsum(M):
    tot = 0
    for row in M: tot += int((row.astype(object)**2).sum())
    return tot
def certify(Hf, entries, Hn):
    m = Hf.shape[0]; cplx = np.iscomplexobj(Hf)
    assert m < 2**13
    lam, V = np.linalg.eigh(Hf)
    Lint = np.rint(lam*2.0**SL).astype(np.int64); assert (np.diff(Lint) >= 0).all() and np.abs(Lint).max() < 2**35
    Hs = np.rint(Hf.real*2.0**SL); Hsi = np.rint(Hf.imag*2.0**SL) if cplx else np.zeros_like(Hs)
    assert np.abs(Hs).max() < 2**34 and np.abs(Hsi).max() < 2**34
    nz = set(entries) | set(zip(*np.nonzero(Hs))) | set(zip(*np.nonzero(Hsi)))
    d2 = arb(0); sc = arb(2)**(-SL)
    for (i, j) in nz:
        ex = entries.get((i, j), acb(0))
        z = acb(ex) - acb(arb(int(Hs[i, j]))*sc, arb(int(Hsi[i, j]))*sc)
        d2 += z.real*z.real + z.imag*z.imag
    assert d2.is_finite()
    dHF = arb(d2.upper()).sqrt()
    Hr = sp.csr_matrix(Hs); Hi = sp.csr_matrix(Hsi)
    rownnz = int(max(np.diff(Hr.indptr).max(), np.diff(Hi.indptr).max() if Hi.nnz else 0))
    assert rownnz*2**34*2**13 < 2**53
    # a priori float error bounds: |terms| <= 2^39*2^39=2^78 (gram), m<2^13 terms -> sum magnitude <2^91,
    # float error <= m*u*2^91/(1-mu) < 2^13*2^-53*2^92 = 2^52;  residual: <=64*2^34*2^39 + 2^35*2^39 < 2^80,
    # error < 2^7*2^-53*2^81 = 2^35.  Both << 2^60.
    if not cplx:
        Xi, A, B = _limbs(V); del V
        Xf = Xi.astype(np.float64)
        G = _gram(A, B, A, B)                       # = Vint^T Vint - 2^76 I  (mod 2^64)
        GF = Xf.T@Xf; GF[np.diag_indices(m)] -= 2.0**76; _guard(G, GF); del GF
        gF2 = _sqsum(G); del G
        R = _spmul(Hr, Xi) - Xi*Lint[None, :]
        RF = Hr@Xf - Xf*Lint[None, :].astype(np.float64); _guard(R, RF); del RF
        rF2 = _sqsum(R); del R
    else:
        Xr, Ar, Br = _limbs(V.real); Xi_, Ai, Bi = _limbs(V.imag); del V
        Xrf = Xr.astype(np.float64); Xif = Xi_.astype(np.float64)
        Gre = _gram(Ar, Br, Ar, Br) + _gram(Ai, Bi, Ai, Bi)
        GF = Xrf.T@Xrf + Xif.T@Xif; GF[np.diag_indices(m)] -= 2.0**76; _guard(Gre, GF); del GF
        gF2 = _sqsum(Gre); del Gre
        P = _gram(Ar, Br, Ai, Bi); Gim = P - P.T; del P
        GF = Xrf.T@Xif; GF = GF - GF.T; _guard(Gim, GF); del GF
        gF2 += _sqsum(Gim); del Gim
        Rre = _spmul(Hr, Xr) - _spmul(Hi, Xi_) - Xr*Lint[None, :]
        RF = Hr@Xrf - Hi@Xif - Xrf*Lint[None, :].astype(np.float64); _guard(Rre, RF); del RF
        rF2 = _sqsum(Rre); del Rre
        Rim = _spmul(Hr, Xi_) + _spmul(Hi, Xr) - Xi_*Lint[None, :]
        RF = Hr@Xif + Hi@Xrf - Xif*Lint[None, :].astype(np.float64); _guard(Rim, RF); del RF
        rF2 += _sqsum(Rim); del Rim
    eta = arb((arb(gF2)*arb(2)**(-4*SV)).upper()).sqrt()     # ||Vt*Vt - I||_F >= ||.||_2
    assert eta < arb(1)/2
    r = arb((arb(rF2)*arb(2)**(-2*(SV+SL))).upper()).sqrt() + dHF*(1+eta).sqrt()
    delta = Hn*eta + r*(1+eta).sqrt()
    return [int(x) for x in Lint], eta, delta
def up_float(x):
    """float >= every point of arb ball x"""
    f = float(x.upper()); return math.nextafter(math.nextafter(f, math.inf), math.inf)
