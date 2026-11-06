# Exact-integer / arb certification of all eigenvalues of a Hermitian block.
# Theorem (H exact Hermitian m x m, ||H||<=Hn; Vt any m x m matrix, Lt real diag):
#   eta >= ||Vt*Vt - I||_2 (<1), r >= ||H Vt - Vt Lt||_2  =>  ||H - Vt Lt Vt*|| <= Hn*eta + r*sqrt(1+eta) =: delta
#   (since H - Vt Lt Vt* = H(I - Vt Vt*) + (H Vt - Vt Lt) Vt*, and ||I-VtVt*|| = ||I-Vt*Vt|| for square Vt).
#   Ostrowski: lambda_i(Vt Lt Vt*) = theta_i * Lt_i, theta_i in [1-eta,1+eta] (sorted, same index).
#   Weyl: |mu_i(H) - Lt_i| <= eta|Lt_i| + delta for all i=1..m (sorted). Exactly m enclosures.
# Vt = Vint/2^38 (dyadic), Lt = Lint/2^20 (dyadic), H = Hs/2^20 + dH (dH bounded entrywise in arb).
# Vt*Vt and Hs Vt - Vt Lt are computed EXACTLY: 19-bit limbs, float64 BLAS products whose every partial sum
# is an integer < 2^53 (hence exact), recombined in int64 modulo 2^64 (exact since true results are < 2^62).
import numpy as np, flint, scipy.sparse as sp
from flint import arb, acb
SV,SL,LB=38,30,19   # Hs scaled 2^30 (|Hs|<2^34); sparse products use 13-bit limbs: 2^34*2^13*24 < 2^53
def limbs(X):
    Xi=np.rint(X*2.0**SV).astype(np.int64); A=Xi>>LB; B=Xi-(A<<LB)   # A in [-2^19,2^19], B in [0,2^19)
    return Xi,A.astype(np.float64),B.astype(np.float64)
def i64(F):
    assert np.abs(F).max()<2.0**53; return F.astype(np.int64)
def gram_part(A1,B1,A2,B2):   # (A1 2^19+B1)^T (A2 2^19+B2) mod 2^64, exact
    with np.errstate(over='ignore'):
        return (i64(A1.T@A2)<<(2*LB))+((i64(A1.T@B2)+i64(B1.T@A2))<<LB)+i64(B1.T@B2)
def sq_sum(Mint):   # exact sum of squares as python int
    tot=0
    for row in Mint: tot+=int((row.astype(object)**2).sum())
    return tot
def certify(Hf, entries, Hn):
    """Hf: float Hermitian (real or complex) matrix. entries: dict (i,j)->exact acb/arb ball of H[i,j] for all
    structurally nonzero (i,j). Returns lam_t (list of exact dyadic as float), eta (arb), delta (arb)."""
    m=Hf.shape[0]; cplx=np.iscomplexobj(Hf)
    lam,V=np.linalg.eigh(Hf)
    Lint=np.rint(lam*2.0**SL).astype(np.int64); lt=Lint/2.0**SL
    Hs=np.rint(Hf.real*2.0**SL); Hsi=np.rint(Hf.imag*2.0**SL) if cplx else None
    # dH Frobenius^2 (arb), over union of structural nonzeros (Hs nonzero only there or on diagonal)
    nz=set(entries)|set(zip(*np.nonzero(Hs)))|(set(zip(*np.nonzero(Hsi))) if cplx else set())
    d2=arb(0); sc=arb(2)**(-SL)
    for (i,j) in nz:
        ex=entries.get((i,j),acb(0))
        ap=acb(arb(int(Hs[i,j]))*sc, arb(int(Hsi[i,j]))*sc if cplx else 0)
        z=acb(ex)-ap; d2+=z.real*z.real+z.imag*z.imag   # (x**2 on a ball straddling 0 gives nan in flint)
    dHF=arb(d2.upper()).sqrt()   # upper bound (d2 may straddle 0)
    Hr=sp.csr_matrix(Hs); Hi=sp.csr_matrix(Hsi) if cplx else None
    assert np.abs(Hs).max()<2**34 and (not cplx or np.abs(Hsi).max()<2**34)
    assert max(np.diff(Hr.indptr).max(), np.diff(Hi.indptr).max() if cplx else 0)<=24
    def Hmul(Mpart):   # exact integer Hs @ (Mint) where Mint=A 2^19+B, real part matrix csr
        pass
    def spmul(Hc,A,B):   # exact Hs @ (A 2^19 + B) mod 2^64, via 13-bit limbs
        Xi=(A.astype(np.int64)<<LB)+B.astype(np.int64); C2=Xi>>26; C1=(Xi>>13)&8191; C0=Xi&8191
        with np.errstate(over='ignore'):
            return (i64(Hc@C2.astype(float))<<26)+(i64(Hc@C1.astype(float))<<13)+i64(Hc@C0.astype(float))
    if not cplx:
        Vi_,A,B=limbs(V); del V
        with np.errstate(over='ignore'):
            G=gram_part(A,B,A,B); Rint=spmul(Hr,A,B)-Vi_*Lint[None,:]
        gF2=sq_sum(G)                      # G = Vint^T Vint - 2^76 I ; 2^76 = 0 mod 2^64
        rF2=sq_sum(Rint)
    else:
        Xr,Ar,Br=limbs(V.real); Xi,Ai,Bi=limbs(V.imag); del V
        with np.errstate(over='ignore'):
            Gre=gram_part(Ar,Br,Ar,Br)+gram_part(Ai,Bi,Ai,Bi)
            P=gram_part(Ar,Br,Ai,Bi); Gim=P-P.T; del P
            gF2=sq_sum(Gre)+sq_sum(Gim); del Gre,Gim
            Rre=spmul(Hr,Ar,Br)-spmul(Hi,Ai,Bi)-Xr*Lint[None,:]
            rF2=sq_sum(Rre); del Rre
            Rim=spmul(Hr,Ai,Bi)+spmul(Hi,Ar,Br)-Xi*Lint[None,:]
            rF2+=sq_sum(Rim); del Rim
    eta=arb((arb(gF2)*arb(2)**(-4*SV)).upper()).sqrt()          # ||G||_F, exact up to sqrt ball
    assert eta<arb(1)/2
    r=arb((arb(rF2)*arb(2)**(-2*(SV+SL))).upper()).sqrt() + dHF*(1+eta).sqrt()
    delta=Hn*eta + r*(1+eta).sqrt()
    return lt.tolist(), eta, delta
def arbs(x): return x.str(radius=True)
def upper(x): return float(arb(x.mid()+x.rad()).mid())  # informational only
