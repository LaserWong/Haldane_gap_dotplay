# Complete scalar residual for the 8x4 enlarged ground trial

2026-10-10 17:47 EDT / 21:47 UTC. Exact producer candidate; independent review required.

## Result

For the saved rational 43-column trial at g=1/10, H'=H+3N/4, N=32,

- exact Rayleigh display: -.25305415013664406
- COMPLETE exact variance display: .0003553876503424027
- actual Temple lower display: -.2532914854282799

The certificate is the exact fractions in physical_result.json, not these decimals. It improves the old ground lower by .00207929923472008. A separate scalar/all-size replay is required before claiming an ordinary-bilayer g=.10 gap. The variance budget from the feasibility assessment was a target only; the actual lower uses the computed variance.

## State, normalization and every sector

Use the audited coupling-independent families B, L=A42 B_pair, R=A44L, M=A64L, and Ufam=R+M. The selected 43 columns are (B,L,Ufam). The complete rational coefficient vector is copied unchanged from the feasibility calculation into ground_8x4_trial.json; its exact norm and Rayleigh are recomputed using the audited enlarged first-moment geometry.

Write psi=B b+L l+R u+M u and H'=Q+tA, t=g/2. With d=40, h=d t=2, the q4 and q6 components of T_int psi, T_int=d H', are

    q4: L(4d l+h b_pair)+R(h l+4d u)+h(D4R+CM)u,
    q6: M(h l+6d u)+h(C†R+D6M)u.

The q0 and q2 components are computed from the first 15 enlarged K rows: if z_i=(K c)_i, their norm contribution is sum_i z_i^2/G_ii, separately split into vacuum and pair rows. Completeness of the translation-invariant singlet pair-orbit family ensures this is the whole q2 image. The q8 component is h C†M u. There are no other occupation sectors after one H' action.

All sector norms use the reduced matching convention: each closed spin-one singlet loop contributes 3; the common physical dimer factor 2^N is removed throughout. Exact normalization uses the same reduced G. The total second moment is the sum of q0/q2/q4/q6/q8 T_int norms divided by d² times the exact norm of psi. No compressed-Hamiltonian square is substituted for this sum.

## Exact q8 norm without constructing a q8 state

The separate hard-core pair-commutator proof establishes

    ||C†M u||²=||CM u||²+<M u,[C,C†]M u>.

C† is exactly the raising part of A=2V, with rung hard-core transitions and spin-one singlet coefficients. The implementation uses its signed same-edge and ordered-wedge action on q6. The commutator need not be positive. Both summands are retained exactly; their sum is asserted nonnegative. See the separately sealed hardcore_pair_commutator/PROOF.md and physical fixtures, pinned below.

CM is pulled on every q4 support from all empty geometric edges, using the exact annihilation contraction (3 for an existing matched pair, 1 when reconnecting its partners). The commutator contains 3 on empty same-edge pairs, negative singlet projection on occupied same-edge pairs, positive empty-center wedges and negative occupied-center singlet annihilation/recreation wedges. Weighted periodic edge multiplicities are retained.

## Support and translation

The production sums cover every one of C(31,3)=4,495 fixed-origin q4 supports and C(31,5)=169,911 fixed-origin q6 supports. In particular, the q6 image norm is NOT restricted to supports where M is nonzero. Its contribution on family-M-zero supports is separately exported and nonzero.

Only the commutator expectation is skipped where the weighted M bra vanishes, which is algebraically exact. Its value is a q6 expectation. Translation rescaling is N/4 for the q4 sums and N/6 for q6 sums, including the commutator expectation; it is not N/8. Every final divisibility check is exact. Full and fixed-origin 4x2 fixtures coincide.

## Ground identification and Temple theorem

The old full-spectrum comparison gives lambda_2>=a1 and lambda_(2+3N)>=a. The even trial Rayleigh rho<a1, while 3N independent odd Ritz states lie below a. Thus the global ground is unique and even, and the even sector has no other level below a. Odd global excitations are not claimed to lie above a.

For this even-sector trial, rho<a and full variance v imply

    lambda_0 >= rho-v/(a-rho).

The exact inequalities and count inputs are rechecked in assemble.py; the old denominator patch and its unchanged odd bands/tails supply the independently accepted external count. The new lower is substituted only for this one ground contribution. The retained 8x4 band is still 97 states, not 43 additional physical eigenstates.

## Exact arithmetic and bounds

Small geometric coefficient vectors use int32, with every add/multiply routed through a checked int64 temporary and int32 range assertion. L entries are <=4, R conservatively <500, D4R<100,000. For N<=64, weights<=2, d<=14: M entries<=24; CM is bounded by 128 edges ×15 matchings ×3×2×24=276,480 per output entry. D6M and C†R are conservatively each <100,000. A loose bound <1,000,000 covers commutator matching entries (vacuum diagonals, same-edge contractions, and ordered wedges combined). These are far below int32 capacity; assertions additionally guard actual accumulations.

State-coefficient contraction uses checked signed 128-bit multiplication/addition. All resulting scalar matching amplitudes must pass a signed-64-bit range assertion before norm multiplication. Norm products, mixed contractions and sums then use GMP arbitrary-precision integers. The large 56-bit rounded coefficients are never squared in fixed-width arithmetic. Python exact assembly uses arbitrary integers/Fraction. The inherited Gram loop weights are <=27.

## Validation, resources, and development

An independent physical 4x2 fixture uses cb=-2c, cl=3c, cu=5c, c=(1,-2,3,-4,5), vacuum coefficient17 and d=20,h=1. This producer exactly matches its q4 norm121947335040, q6 norm191711843328 and q8 norm97459200, as well as CM norm467635200, commutator -370176000 and P/T subnorms. A simpler U-only vector also matches the separate local worker's q8 identity, in full and fixed-origin sums.

The microbenchmark passed before production. Updated checked arithmetic gave a tenfold projected bound of about34 seconds, below600 CPU seconds, with <8 MiB RSS. The full 8x4 run took3.51709 seconds and7808 KiB RSS. One CPU5, 1 GiB address-space limit,600 CPU-second limit and610-second wall timeout were imposed. No q8 configurations were enumerated and no 8x8 production run occurred.

An initial Boost include was unavailable, so GMP was used. A first fixture detected an occupied-wedge table-index ordering bug; the implementation now orders the two positions and passes the exact independent fixtures. No failed-attempt values enter the final certificate. The final source was rebuilt and rebenchmarked after adding all integer guards.
