# A degree-five ground-endpoint certificate at g=1/10

2026-10-10 17:36 EDT / 21:36 UTC. Exact producer candidate, independent review required.

## Model and sector hypothesis

The ordinary periodic spin-1/2 bilayer has unit rung exchange and g=1/10 straight intralayer exchange. Use H'=H+3N/4, N rungs, with the inherited multiedge convention. There are N rung projectors bounded above by 1 and 4N intralayer spin-half bonds bounded above by g/4. Thus H'<=U I for U=N(1+g), including on the even singlet sector.

The old full-spectrum ordered comparison gives lambda_2>=a1 and lambda_(2+3N)>=a. The old even trial Rayleigh is below a1, and all 3N independent odd triplet Ritz directions have uppers below a. These exact inequalities are rechecked. Min-max therefore gives precisely 1+3N global levels strictly below a. The odd sector contributes at least 3N; the global ground, uniquely identified by the even Rayleigh<a1, contributes one even level. Hence the EVEN sector has exactly one level below a, and all its other levels lie in [a,U]. This is not a claim that the global odd excitations lie above a. The previously certified even ground lower L also bounds this entire sector from below.

## Sign-polynomial theorem

Let an invariant-sector Hermitian operator T have exactly one eigenvalue lambda_0<a and all spectrum <=U. For ell<a, put

    P_ell(T)=(U-T)(T-a)(T-ell).

For E<=ell or a<=E<=U, the scalar P_ell(E) is nonnegative. It can be negative only for ell<E<a. Therefore an exact negative expectation in any sector vector implies lambda_0>ell. Eigenvalues at ell, a, or U cause no problem. No residual norm or inverse square root of a matrix is required for this acceptance theorem.

Use the old W=(B,Lpair) trial family, of independent ranks 11/29/29 for 4x4/8x4/8x8. With full moments G=W*W, A=W*T W, B2=W*T^2 W, C3=W*T^3 W,

    W*P_ell(T)W = -C3+(U+a+ell)B2-[U(a+ell)+a ell]A+Ua ell G.

A rounded integer vector c and exact negative scalar are stored for each shape. Its four quadratic moments are separately stored, so the sign can be checked without a generalized eigensolver. The proposal uses the ordinary inverse pencil for weighted moments UG-A, UA-B2, UB2-C3, but numerical eigenvalues play no role in exact acceptance.

## Why only base M0 through M5 are needed

The independent base family B contains the vacuum and pair-orbit sums. Let T_int=d H', and M_j=B*T_int^j B. The old W=(B,Lpair) equals span(B,T_int B). With C=M0^{-1} M1 and h=d g/2,

    Lpair_j=(T_int B_j-B C_j)/h, for pair columns j.

This supplies an exact rectangular coordinate map R from W into (B,T_int B). For k=0,1,2,3,

    W*H'^k W = d^{-k} R* [[M_k,M_(k+1)],[M_(k+1),M_(k+2)]] R.

Thus C3 needs M5, not M6. `weighted_ground.py` builds it from the audited enlarged first-moment geometry; `replay.py` independently transforms the block-Hankel moments by the displayed formula and matches all four matrices exactly, also matching the old G/A/B2. This is a separate-formulation self-replay, not an independent worker audit.

M5 at .10 is obtained by evaluating the already audited, g-independent F/S/V/W/X/Y/Z geometry at .10. The original ground matrices and denominator patches are byte-identical to their accepted combined-review snapshots. Every original M0..M4 block is checked during construction. No q8 state, M6, or residual of the enlarged numerator state is inferred. C3 concerns the OLD trial family; H' applied to that family reaches at most q6, and its first Hamiltonian expectation uses only q<=6 bra/ket overlaps.

## Candidate lower endpoints

- 4x4: -63496684407/500000000000 = -.126993368814, improvement .0000846906642
- 8x4: -637715387/2500000000 = -.255086154800, improvement .000284629863
- 8x8: -51724680959/100000000000 = -.517246809590, improvement .0007066132366

The 8x8 endpoint is ancillary: the txy startup uses this patch only in its numerator. No retained-state count changes. Small denominators retain 49 and 97 levels, and largest numerator retains one. Full physical Hilbert dimensions remain 2^32, 2^64, and 2^128.

## Optimization limit for the tested degree-five class

Let L be the old accepted ground lower. Both (U-T) and (T-L) are nonnegative on the entire even-sector spectrum. We check exact positive definiteness, by integer Bareiss leading principal minors, of

    W*(U-T)(T-a)(T-ell_hi)W,
    W*(T-L)(T-a)(T-ell_hi)W,

at ell_hi=new candidate lower+10^-10. Both are positive definite on all three geometries. W contains every affine-in-T image of the base B, after quotienting exact dependencies. Consequently no sum of endpoint-weighted affine-square tests in this class can supply a negative witness at ell_hi. This includes choosing new coefficients, combining the two endpoint weights, and summing arbitrarily many such tests.

For ell_hi<=ell<a the matrices remain positive semidefinite: each is the convex combination, with coefficient (a-ell)/(a-ell_hi), of its ell_hi matrix and the corresponding nonnegative weighted (T-a)^2 matrix. Hence the optimized endpoint in this explicit class is bracketed to 10^-10. This is NOT a no-go theorem for every use of M0..M5, gap-aware polynomial constructions, other trial families, or future moments.

The separate numerator check proves A_enlarged-(rho-10^-10)G_enlarged positive definite, while its saved rational vector has Rayleigh rho=-.5044427289405554.... Thus the minimum within that fixed 43D numerator space is bracketed to 10^-10. A material numerator gain needs more than coefficient retuning in this same space. This compression floor is not a physical ground lower bound.

## Scalar status

Replacing only the two small ground lower endpoints by these exact candidates leaves zero successful proposals on the bounded beta=5..20, step .05, txy/joint scan with at most ten cycles. The best observed minimum defect improves from .2724016181 to .2211521921. No g=.10 scalar startup or all-size gap certificate is claimed. Finite-grid failure is not an all-temperature exclusion.
