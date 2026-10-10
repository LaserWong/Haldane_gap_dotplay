# Full-ladder joint trace constraints

Updated 2026-10-10 15:16 EDT / 19:16 UTC.
**New scalar lemma, pending independent review.**

## Domain

Use only the reflected even base patches covered by the existing signed-transfer
theorem: both base spatial lengths are even and subsequent base doublings keep
them even. Every ladder purity invoked below is then in (0,1]. Thermal purities
also satisfy this intrinsically. No assertion of spatial purity≤1 on arbitrary
odd base geometries is made. Finite-window interpolation retains exactly the
admissibility hypotheses of the previously reviewed even-base interpolation
theorem; the new information only sharpens its endpoint inequalities.

## Exact joint identity

Let u0→u1→u2→u3 be a ladder that doubles each of the two spatial directions and
inverse temperature exactly once, in any order. Define its *actual* purities

    p_i = Z(u_i)/Z(u_(i−1))²,   i=1,2,3.

Cancellation gives, with no estimate,

    p1⁴ p2² p3 = Z(u3)/Z(u0)^8.

All permutations have the same endpoints. Therefore canonical actual purities
A,B,C and actual txy purities a,b,c at the same base obey

    A⁴B²C = a⁴b²c.

If lower bounds a_l,b_l,c_l are known, retain K=a_l⁴b_l²c_l as a separate lower
bound for the common full product. One must not replace this with the generally
smaller product of separately transported canonical lower bounds. No equality
between partial products from different orders is asserted.

## Consequences and canonical update

Since 0<A,B,C≤1, a full-product lower bound K also implies

    B²C ≥ K,       A²B ≥ sqrt(K),       C ≥ K.

These are inequalities obtained by dropping factors≤1, not partial-product
identities. In the canonical sequential update, write

    D ≥ G(A⁴B²C),  E ≥ G(B⁴C²D),  F ≥ G(C⁴D²E),
    G(z)=1−(1−z)²/(2z²), monotone increasing on (0,1].

With lower endpoints A_l,B_l,C_l,D_l,E_l, valid improved arguments are

    D_l = G(max(A_l⁴B_l²C_l,K)),
    E_l = G(max(B_l⁴C_l²,K²) D_l),
    F_l = G(max(C_l,K)^4 D_l² E_l).

Only positive outputs are retained. At the next full doubled base, an
independently propagated txy ladder can supply another full-product lower
bound K_next. Canonical componentwise lower bounds obtained by different valid
routes may be maximized, because their labels and base points coincide. Their
full-product bound and the txy full-product bound may likewise be maximized.
This produces a coupled lower-bound propagation, without treating incompatible
lower endpoints as exact physical values.

Repeated txy cycles before canonical conversion are also valid directly: use
the already reviewed axis-order recurrence on the txy ladder, double both
spatial bases and β after each full cycle, then apply the already reviewed
adjacent-order conversion at the resulting base. Every earlier spatial window
still requires its own bridge; a later successful recurrence does not erase
those windows.

## Joint-aware one-dimensional interpolation

Suppose actual endpoint purities S,T satisfy S≥s>0, T≥t>0 and independently
S²T≥P. Let p=max(s²t,P). If p>1/2, define

    w=(1+sqrt(2p−1))/2, r=(1−w)/w, d=t/(1+r²),
    I(s,t;P)=(1−r) min(s sqrt(d),d).

The previously reviewed inverse-dominant-weight proof uses S²T only to upper
bound its tail ratio. Replacing s²t by the stronger valid p decreases r. With
s,t fixed, both factors in this expression improve when r decreases. Thus the
same proof yields I(s,t;P) as a valid lower bound. The separate parameter P is
essential: s and t remain lower endpoints and are not silently changed to
inconsistent values.

## Joint-aware two-dimensional finite window

Let canonical actual A,B,C satisfy lower endpoints A_l,B_l,C_l and full joint
lower bound K. The earlier transverse spatial estimate is

    Sx ≥ A² sqrt(2B−1),   provided B_l>1/2.

Write its right side as `(A²B) f(B)`, where
`f(B)=sqrt(2B−1)/B`. On [1/2,1], f is increasing: its square has derivative
`2(1−B)/B³ ≥0`. Since A²B≥sqrt(K), we obtain

    sx = max(A_l² sqrt(2B_l−1), sqrt(K) sqrt(2B_l−1)/B_l).

The transverse thermal lower bound can use the separate constraint B²C≥K:

    ty = I(B_l,C_l;K).

Applying the unchanged outer one-dimensional interpolation gives

    T(L,W,β) ≥ I(sx,ty;0),   n≤L,W≤2n.

All square roots and final output rounding must be outward. The exact scalar
code stores K separately in every record. Positive all-size gaps require this
finite-window bound (or another valid bridge) on every earlier doubled window,
plus the independent short-size bound.
