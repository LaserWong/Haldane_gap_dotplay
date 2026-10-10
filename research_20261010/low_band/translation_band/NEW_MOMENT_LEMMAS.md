# Stronger moment lemmas for subsequent variants

2026-10-10 13:59 America/New_York / 17:59 UTC.

These self-contained derivations are proposed for independent review. They have not been used in the frozen numerical candidates in `refined/`.

## Direct complement bound by inertia at the counted cutoff

Let Q have k orthonormal columns and let

    H = [[T,R*],[R,C]]

in its trial/complement decomposition. Assume λ_{k+1}(H)≥a and T<aI. By the variational principle, λ_k(H)≤λ_max(T)<a, so H−aI has exactly k strictly negative eigenvalues.

Schur elimination of the negative definite block T−aI gives

    inertia_−(H−aI)
      = k + inertia_−[C−aI+R(aI−T)^{-1}R*].

The second term is therefore zero. Its matrix is positive semidefinite, including when H has eigenvalues exactly at a. Thus

    C ≥ aI−R(aI−T)^{-1}R*
      ≥ [a−||R(aI−T)^{-1/2}||²]I.

This proof needs no global lower bound L₀ and no principal-angle estimate. The coarse form is a−η²/(a−r_max) when R*R≤η²I and T≤r_max I. For mutually orthogonal rank-one invariant symmetry sectors, the sharper correction is max_k r²(k)/(a−θ(k)).

## Direct low-band bounds from a generalized inverse trial

Let W be a full-rank trial matrix with exact moments

    G=W*W,  A=W*HW,  B=(HW)*(HW),

including the physical metric when a nonorthonormal ambient basis is used. Suppose λ_{k+1}(H)≥a and K=A−aG is negative definite. Define

    X=(H−aI)W,
    S=X*X=B−2aA+a²G.

X has full column rank. Otherwise Xc=0 would imply c*Kc=0, contradicting negative definiteness. Hence S is positive definite.

Let M=(H−aI)^† be the self-adjoint Moore-Penrose inverse. It has exactly k negative eigenvalues, ordered as

    ν_j=1/(λ_{k+1−j}(H)−a),  j=1,…,k.

Eigenvalues at a map to zero and do not affect this negative ordering. Since (H−aI)M(H−aI)=H−aI,

    X*MX=A−aG=K.

The Ritz values μ₁≤…≤μ_k of M on ran(X) are the generalized eigenvalues of the pencil (K,S). All are negative. The min-max principle gives ν_j≤μ_j<0. Taking reciprocals reverses the inequality on the negative half-line, so

    λ_i(H) ≥ a+1/μ_{k+1−i}.

This is an exact multilevel lower bound from the full moments and the external spectral count. No residual norm or complement lower bound is needed.

For a rational proposed endpoint l<a, the inequality μ_{k+1−i}≤1/(l−a) is sufficient for λ_i(H)≥l. A strict sufficient test is that K−S/(l−a) has at least k+1−i negative eigenvalues. Multiplication by the positive factor a−l gives the particularly simple moment test

    inertia_−[B−(a+l)A+alG] ≥ k+1−i.

A nonstrict endpoint can be obtained by a limit. In code, use strictly accepted inward endpoints to avoid that issue.

When k=1, the resulting lower bound is exactly the Temple endpoint ρ−r²/(a−ρ). For translation-resolved rank-one sectors, this can be applied independently once global counting has established that each sector contains exactly one eigenvalue below a.
