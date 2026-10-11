# Independent symbolic and cached-matrix review

Scope: ordinary bilayer H'=Q+gV=Q+(g/2)(C+C†+D), accepted 57D even-singlet witnesses at .11/.12. This review makes no new physical support contraction, energy endpoint or all-size gap claim. The reviewed producer plan and cost erratum, complete57D matrix review, endpoint review and subsequent moment-budget package are hash-pinned in snapshot.

## Normal ordering

The checker treats C,C†,D as free noncommuting generators, with their actual adjoints, rather than assuming bosonic commutation. Set K=[C,C†], E=[D,C†], N=[C,E], L=[[C,K],C†]. Direct word expansion verifies

C D C† = C† C D + D C† C − C† D C + K D + N.

Taking an expectation in q6 vector m gives the producer's m3 identity. KD+N is Hermitian; N generally is not. Replacing KD by DK is detected as false. The two cross terms combine through real parts only after taking the adjoint correctly.

For t=g/2, χ=H'ψ and m=ψ6, χ8=tC†m. Occupation grading gives (H'χ)8=C†v+t²Em with v=8tm+tχ6+t²D6m, and (H'χ)10=t²(C†)²m. The q8 norm follows from CC†=C†C+K, CE=EC+N, and E†E=EE†+[E†,E]. Its interference term 2t² Re<v,CEm> is mandatory. The q10 identity is checked by expanding

(CC†)² + C†CK + KC†C − C†KC + K² + L = C²(C†)².

Thus the negative term −<Cm,K Cm>, the extra K², and both real cross terms are mandatory. L is Hermitian. Neutral nested commutators and lower/raising images on q≤6 permit these expectation formulas without constructing q8/q10 output states. This is an algebraic reduction; it does not validate a new physical local-action implementation. Hard-core matrix elements, motifs, channel permutations and all terms still need independent fixtures.

## Krylov pencil and sector scope

For normalized ψ, the actual two-vector trial {ψ,H'ψ} has Gram [[1,m1],[m1,m2]], first moment [[m1,m2],[m2,m3]], and complete second moment [[m2,m3],[m3,m4]]. Its rank is two when variance>0. A full57D augmentation by H'ψ additionally needs vector third-moment cross entries, unavailable from scalar m3 alone.

If verified ell0≤H'≤U, spectral calculus gives H'²(H'−ell0)(U−H')≥0, hence m4≤M4=(U+ell0)m3−ell0 U m2, even with negative ground energy. Replacing only m4 by M4 raises the second-moment matrix in Loewner order. A strictly negative upper pencil Jupper−(a+l)H+l a G therefore implies a negative true pencil. For l<a, the polynomial (E−l)(E−a) is negative only in (l,a); if the second eigenvalue of the full untruncated even-singlet sector is ≥a, its ground energy lies strictly above l and below a. This is a lower-endpoint argument, not a variational upper bound or a full-Hilbert λ2 claim. Accepted odd counting provides the sector cutoff r2, and separate r1 comparison identifies the unique global ground. A hypothetical target cannot replace the verified ell0 in the envelope. A small exact spectral example verifies this distinction.

For N rungs, each of the 4N physical spin-half intralayer bonds is ≤1/4, so V≤N and U=N(1+g). Weighted parallel bonds are counted with multiplicity.

## Exact scoped envelope barrier

Use the accepted .11 57D witness, rho=<H'>, variance v>0, verified ell0=rho−v/(a−rho), a=r2, U=35.52. In centered basis {ψ,η}, η=(H'−rho)ψ, put R=<η,H'η>/v. Then m3=rho³+2rho v+Rv. PSD of the degree-one localizing moment matrices gives R≥a+ell0−rho and R≤U−v/(U−rho).

The actual η has q≤8. Consequently R≤8+Ng=11.52, stronger than the producer's valid 14.6 occupation-row estimate. This bound uses only expectation of Q and the same rigorous interaction upper, and does not assert H' preserves q≤8.

For target l, P00=v+(rho−a)(rho−l)>0; P01=v(rho+R−a−l). P11 follows by centering the upper second moment. Its determinant is a concave quadratic in R. Exact rational checks show nonnegative determinant at both endpoints of the physical feasible interval, hence everywhere between them; together with P00>0 this proves the upper pencil PSD. Thus neither selected target can have a negative witness using this envelope, for any physically admissible m3 of this fixed ψ.

A stronger interval-localizing bound also fails. Let b0=(U+ell0)rho−ell0 U−m2>0 and b1=−m3+(U+ell0)m2−ell0 U rho. Positivity of <[1,H']*(H'−ell0)(U−H')[1,H']> yields m4≤M4−b1²/b0. Its pencil determinant is again concave, zero at the lower feasible R endpoint and strictly positive at 11.52. Both producer determinant polynomials and exact root brackets were independently checked. Large root displays for the two targets are 25.63018195/26.19099904 (generic) and 25.62347487/26.18700392 (sharper bound), all above 11.52.

This is an envelope-specific obstruction for these two targets and this fixed ψ. An exact two-atom Jacobi model with diagonal entries rho and R=4.5, squared off-diagonal v, has the same first two moments, valid spectral ordering and negative true target pencils. Thus exact m4, another ψ, other target choices and larger trial spaces remain open. The checker records exact m3,m4 and determinant for this counterexample.

## Cached rank and cost

The checker independently reconstructs the q4 and q6 Schur norms from accepted57D Gram and complete image blocks. Both are strictly positive at .11/.12. Occupation orthogonality gives rank58 for adding T=(C†R)cR+D6M cM and rank59 for adding the q4 companion P. Residual sector contributions sum exactly to the accepted complete variance. This establishes rank, not the missing <T,D6T> or full58D residual.

The generic K identity <C†u,C†v>=<Cu,Cv>+<u,Kv> applies to arbitrary q6 vectors. Existing M-specific lookup is insufficient for T. Every occupied-site-to-origin translation, sorted-site permutation and matching-channel transformation must agree exactly; use two-dimensional torus translations. M-zero supports must remain included. The q6 scalar int128 cache is 40,778,640 bytes, optional q4 cache 1,726,080; direct q8 scalar cache is 4,417,686,000 bytes. Coefficient dot products alone are below 2^83; subsequent local sums require their own bounds, and norm accumulation requires arbitrary precision.

Nested triple-edge operators need at most4 rungs; quartet operators at most5. Connected-prefix ceilings are 5376 triples and86016 quartets. For [E†,E], either edge of the second connected pair may first touch the first pair, giving the corrected uniform172032 ceiling. These count motifs before cancellation, not CPU work. Per-support scanning of all motifs is not an acceptable projected implementation. q10 fixed-origin supports number20,160,075, with945 matchings each; the normal-order route avoids that enumeration.

## Recommendation

Skip a full m3-only physical support pass for these fixed-witness targets under either tested m4 envelope. The smallest low-risk next fixture is generic q6 T lookup, all translation/matching permutations, and signed K on a small geometry, followed by a measured sampled-action cost gate before58D production. If prioritizing true2D Krylov, fixture exact m4's [C,E], [E†,E] and L with all orientations on small connected motifs; triple m3 fixtures are then a component of that full route. No physical fixture or support launch is authorized or performed by this review.
