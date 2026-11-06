# Rigorous enclosure of ALL eigenvalues of an exact Hermitian block B (m x m), given exact ball entries.
# THEOREM (Weyl + Ostrowski).  Let ||B - cI||_2 <= Hn, Vt any m x m matrix, Lt real sorted ascending, and
#   eta >= ||Vt^* Vt - I||_2, eta < 1;   r >= ||B Vt - Vt Lt||_2.
# Then ||B - Vt Lt Vt^*||_2 <= Hn*eta + r*sqrt(1+eta) =: delta   [B' = B - cI, Lt' = Lt - c:
#   B' - Vt Lt' Vt^* = B'(I - Vt Vt^*) + (B Vt - Vt Lt) Vt^*;  ||I - Vt Vt^*|| = ||I - Vt^* Vt||, ||Vt|| <= sqrt(1+eta)]
# Ostrowski: lambda_i(Vt Lt' Vt^*) = theta_i Lt'_i with theta_i in [1-eta, 1+eta] (same sorted index).
# Weyl: |lambda_i(B') - lambda_i(Vt Lt' Vt^*)| <= delta.  Hence the i-th smallest eigenvalue of B lies in
#   [Lt_i - e_i, Lt_i + e_i],  e_i = eta*|Lt_i - c| + delta,   exactly m enclosures with multiplicity.
# Here c = -L/2, Hn = 3L/2: every bond term (twisted or not) has spectrum {-2,-1,1}, so spec H^g in [-2L, L],
# and B = Phi^* H^g Phi with Phi an isometry onto an invariant subspace.
# Exact entries: B = Hs + dH, Hs the computable matrix (dyadic ints / floats), ||dH||_2 <= max_i sum_j |dH_ij|
# (|dH| is a symmetric nonnegative matrix), bounded in arb from the exact ball entries.
#
# MODE 'exact' (m <= MEXACT): Vt = Vint/2^SV, Lt = Lint/2^SH, Hs = Hint/2^SH; Vt^*Vt - I and Hs Vt - Vt Lt are
#   computed EXACTLY with FLINT fmpz_mat; Frobenius norms (>= 2-norms) from exact integer sums of squares.
# MODE 'float' (m > MEXACT): Vt = V (float64 as returned), Lt = lam (float64), Hs = Hf (float64).  Products are
#   computed by IEEE-754 binary64 BLAS (round-to-nearest) and bounded by the standard model, valid for ANY
#   summation order and with/without FMA (Higham, Accuracy & Stability, Thm 3.5/eq. 3.4 + underflow term):
#     |fl(x^T y) - x^T y| <= gamma_n |x|^T |y| + n*2^-1074,  gamma_n = n u/(1-n u), u = 2^-53.
#   Gram: W = [Re V; Im V] (2m x m), Re(V^*V) = W^T W, Im(V^*V) = W^T W2, W2 = [Im V; -Re V].
#     ||fl(G) - G||_F <= sqrt(2)*(gamma_n ||W||_F^2 + m^2 n 2^-1074)  (||(|W|^T|W2|)||_F <= ||W||_F^2).
#   Residual entry (Re/Im) is one sum of n_r = nnz(Re row)+nnz(Im row)+1 products, evaluated in some tree:
#     ||fl(R)-R||_F <= gamma_nr (rho_re + rho_im + Lmax) ||W||_F + tiny, rho = max abs row sum (>= || |Hs| ||_2).
#   Sums of squares of n_s nonnegative float terms: exact <= fl/(1-gamma_ns) + n_s 2^-1074.
import numpy as np, scipy.sparse as sp, math, flint
from flint import arb, acb, fmpz_mat
flint.ctx.prec = 128
SV, SH = 60, 56
MEXACT = 3000
MHP = 40          # MODE 'hp' (m <= MHP): trial V, Lt from mpmath (60 digits) instead of LAPACK; exact fmpz checks
SVH, SHH = 180, 180
U = arb(2)**-53; TINY = arb(2)**-1074
def gam(n): return n*U/(1 - n*U)
def upf(x):   # python float >= every point of arb x (labelled: conversion + 2 ulps outward)
    return math.nextafter(math.nextafter(float(x.upper()), math.inf), math.inf)
def _fz(A): return fmpz_mat(A.shape[0], A.shape[1], A.ravel().tolist())
def _sq(M):   # exact sum of squares of an fmpz_mat
    return sum(int(x)*int(x) for x in M.entries())
def _dH_norm(m, ent, Hs_of):
    """max_i sum_j |B_ij - Hs_ij| upper bound (arb). Hs_of(i,j)-> exact arb/acb of the computable matrix entry."""
    rows = [arb(0)]*m
    keys = set(ent) | set(Hs_of('keys'))
    for (i, j) in keys:
        z = acb(ent.get((i, j), acb(0))) - Hs_of((i, j))
        rows[i] = rows[i] + abs(z)
    return max((arb(x.upper()) for x in rows), key=lambda a: float(a.upper()), default=arb(0)) if m else arb(0)
def certify(Hf, ent, L, mode=None, eig=None):
    m = Hf.shape[0]; cplx = np.iscomplexobj(Hf)
    mode = mode or ('hp' if m <= MHP else 'exact' if m <= MEXACT else 'float')
    c = arb(-L)/2; Hn = arb(3*L)/2
    if mode == 'hp':
        import mpmath as mp
        mp.mp.dps = 60
        A = mp.matrix(m, m)
        for (i, j), v in ent.items():
            A[i, j] = mp.mpc(mp.mpf(v.real.mid().str(70, radius=False)), mp.mpf(v.imag.mid().str(70, radius=False))) if cplx else mp.mpf(v.real.mid().str(70, radius=False))
        ev, Q = (mp.eigh(A) if cplx else mp.eigsy(A))
        order = sorted(range(m), key=lambda i: ev[i])
        sc = mp.mpf(2)**SVH; sl = mp.mpf(2)**SHH
        Lint = [int(mp.nint(ev[i]*sl)) for i in order]
        Vr = [[int(mp.nint(mp.re(Q[a, i])*sc)) for i in order] for a in range(m)]
        Vi = [[int(mp.nint(mp.im(Q[a, i])*sc)) for i in order] for a in range(m)] if cplx else None
        shh = arb(2)**SHH
        Hr = [[0]*m for _ in range(m)]; Hi = [[0]*m for _ in range(m)]
        for (i, j), v in ent.items():
            Hr[i][j] = int((v.real.mid()*shh).floor().unique_fmpz())
            if cplx: Hi[i][j] = int((v.imag.mid()*shh).floor().unique_fmpz())
        assert all(Lint[i] <= Lint[i+1] for i in range(m-1))
        sh = arb(2)**-SHH
        def Hs_of(k):
            if k == 'keys': return set(ent)
            i, j = k; return acb(arb(Hr[i][j])*sh, arb(Hi[i][j])*sh)
        dHn = _dH_norm(m, ent, Hs_of)
        F = lambda X: fmpz_mat(X)
        FVr = F(Vr); FHr = F(Hr); Ld = fmpz_mat(m, m, [Lint[i] if i == j else 0 for i in range(m) for j in range(m)])
        G = FVr.transpose()*FVr
        if cplx:
            FVi = F(Vi); FHi = F(Hi); G = G + FVi.transpose()*FVi
            Gim = FVr.transpose()*FVi; Gim = Gim - Gim.transpose()
        G = G - fmpz_mat(m, m, [(1 << (2*SVH)) if i == j else 0 for i in range(m) for j in range(m)])
        g2 = _sq(G) + (_sq(Gim) if cplx else 0)
        if cplx:
            Rre = FHr*FVr - FHi*FVi - FVr*Ld; Rim = FHr*FVi + FHi*FVr - FVi*Ld; r2 = _sq(Rre) + _sq(Rim)
        else:
            R = FHr*FVr - FVr*Ld; r2 = _sq(R)
        eta = arb(arb(g2).sqrt().upper())*arb(2)**(-2*SVH)
        rR = arb(arb(r2).sqrt().upper())*arb(2)**(-(SVH+SHH))
        lt = [arb(x)*sh for x in Lint]; ltrep = [str(x) for x in Lint]; scale = SHH
    elif mode == 'exact':
        lam, V = np.linalg.eigh(Hf)
        Lint = np.rint(lam*2.0**SH).astype(np.int64); assert (np.diff(Lint) >= 0).all()
        Hr = np.rint(Hf.real*2.0**SH).astype(np.int64); Hi = np.rint(Hf.imag*2.0**SH).astype(np.int64) if cplx else None
        assert np.abs(Hf).max() < 2**6
        sh = arb(2)**-SH
        nzr = set(zip(*np.nonzero(Hr))) | (set(zip(*np.nonzero(Hi))) if cplx else set())
        def Hs_of(k):
            if k == 'keys': return nzr
            i, j = k; return acb(arb(int(Hr[i, j]))*sh, arb(int(Hi[i, j]))*sh if cplx else 0)
        dHn = _dH_norm(m, ent, Hs_of)
        Vr = np.rint(V.real*2.0**SV).astype(np.int64); Vi = np.rint(V.imag*2.0**SV).astype(np.int64) if cplx else None
        del V
        FVr = _fz(Vr); FHr = _fz(Hr); Ld = fmpz_mat(m, m, [int(Lint[i]) if i == j else 0 for i in range(m) for j in range(m)])
        G = FVr.transpose()*FVr
        if cplx:
            FVi = _fz(Vi); FHi = _fz(Hi)
            G = G + FVi.transpose()*FVi
            Gim = FVr.transpose()*FVi; Gim = Gim - Gim.transpose()
        G = G - fmpz_mat(m, m, [(1 << (2*SV)) if i == j else 0 for i in range(m) for j in range(m)])
        g2 = _sq(G) + (_sq(Gim) if cplx else 0); del G
        if cplx:
            Rre = FHr*FVr - FHi*FVi - FVr*Ld; Rim = FHr*FVi + FHi*FVr - FVi*Ld
            r2 = _sq(Rre) + _sq(Rim); del Rre, Rim
        else:
            R = FHr*FVr - FVr*Ld; r2 = _sq(R); del R
        eta = arb(arb(g2).sqrt().upper())*arb(2)**(-2*SV)
        rR = arb(arb(r2).sqrt().upper())*arb(2)**(-(SV+SH))
        lt = [arb(int(x))*sh for x in Lint]; ltrep = [str(int(x)) for x in Lint]; scale = SH
    else:
        lam, V = eig if eig is not None else np.linalg.eigh(Hf)   # any trial pair; rigor does not depend on it
        assert np.isfinite(V).all() and V.shape == (m, m) and (np.diff(lam) >= 0).all()
        W = np.vstack([V.real, V.imag]) if cplx else np.ascontiguousarray(V.real); del V
        n = W.shape[0]
        def ss(A):   # rigorous upper bound on exact sum of squares of float array
            N = A.size; s = float(np.sum(A*A)); return arb(s)/(1 - gam(N + 1)) + N*TINY
        WF2 = ss(W)
        Gt = W.T@W; d = np.diag(Gt).copy(); assert (d > 0.5).all() and (d < 2).all()   # Sterbenz: d-1 exact
        Gt[np.diag_indices(m)] = d - 1.0
        gA = ss(Gt); del Gt
        if cplx:
            W2 = np.vstack([W[m:], -W[:m]]); Gi = W.T@W2; del W2; gA = gA + ss(Gi); del Gi
        Ge = (gam(n)*WF2 + m*m*n*TINY)*(arb(2).sqrt() if cplx else 1)
        eta = arb(gA.sqrt().upper()) + Ge
        Hs_ = sp.csr_matrix(Hf)
        def Hs_of(k):
            if k == 'keys': return set(zip(*Hs_.nonzero()))
            i, j = k; z = complex(Hs_[i, j]); return acb(arb(z.real), arb(z.imag))
        dHn = _dH_norm(m, ent, Hs_of)
        Hr_ = sp.csr_matrix(Hf.real); Hi_ = sp.csr_matrix(Hf.imag) if cplx else None
        rowabs = lambda A: max((sum((arb(abs(float(v))) for v in A.data[A.indptr[i]:A.indptr[i+1]]), arb(0)) for i in range(m)), key=lambda a: float(a.upper()))
        rho = rowabs(Hr_) + (rowabs(Hi_) if cplx else 0)
        nr = int(np.diff(Hr_.indptr).max()) + (int(np.diff(Hi_.indptr).max()) if cplx else 0) + 1
        Lmax = arb(float(np.abs(lam).max()))
        Vr, Vi = (W[:m], W[m:]) if cplx else (W, None)
        if cplx:
            Rre = Hr_@Vr - Hi_@Vi - Vr*lam[None, :]; Rim = Hr_@Vi + Hi_@Vr - Vi*lam[None, :]
            rA = ss(Rre) + ss(Rim); del Rre, Rim
        else:
            R = Hr_@Vr - Vr*lam[None, :]; rA = ss(R); del R
        Re_ = gam(nr)*(rho + Lmax)*arb(WF2.sqrt().upper())*(arb(2).sqrt() if cplx else 1) + m*nr*TINY*2
        rR = arb(rA.sqrt().upper()) + Re_
        lt = [arb(float(x)) for x in lam]; ltrep = [float(x).hex() for x in lam]; scale = None
    assert eta < arb(1)/2, 'eta too large'
    r = rR + dHn*(1 + eta).sqrt()
    delta = Hn*eta + r*(1 + eta).sqrt()
    errs = [upf(eta*abs(x - c) + delta) for x in lt]
    return dict(mode=mode, m=m, lt=ltrep, SH=scale, err_up=errs, eta_up=upf(eta), delta_up=upf(delta),
                dH_up=upf(dHn), r_up=upf(rR))
