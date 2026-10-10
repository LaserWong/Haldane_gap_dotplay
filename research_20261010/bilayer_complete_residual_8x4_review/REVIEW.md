# Independent review of one complete 8×4 bilayer residual

Status: PASS for the complete 8×4 residual, sector Temple lower, g=1/10 all-integer certificate, and fixed-vector coupling polynomials. Reviewed 2026-10-10 17:53 America/New_York (EDT) / 21:53 UTC.

## Scope and conventions

Ordinary spin-1/2 square bilayer, periodic multiedges, rung coupling 1 and straight intralayer coupling g=1/10. The shifted Hamiltonian is H′=Q+(g/2)A. The 8×4 geometry has 32 rungs, 64 spins, full Hilbert dimension 2^64. Its enlarged singlet search rank is 43, with one saved rational vector. These numbers are distinct from the 97 retained denominator levels (one ground plus 96 odd triplet levels).

Only this review directory is modified. The extracted project has no Git metadata. No producer, project-root or GitHub file is changed.

## Independent local and small-space tests

The fresh audit_local.py builds the physical local bilayer operator from spin-half raising/lowering and Sz matrices, transforms into the singlet/triplet rung basis, and works with exact integer physical amplitudes. It imports no producer or previous-review code. On every basis vector of two-, three-, and four-rung test graphs it checks the full local commutator, including a signed weighted graph.

For an edge e={i,j}, [P_e,P_e†]=3h_i h_j−|Ω_e><Ω_e|. For an ordered wedge, [P_ij,P_ik†] is the positive empty-center hop minus the occupied-center singlet reconnection. Identical-edge terms carry w_e²; ordered wedges carry w_e w_f with no additional factor two. Parallel periodic edges must first be aggregated. Neither the negative same-edge term nor the negative occupied-center term may be omitted.

All cross entries of the q8 Gram agree with ||CM||²+<M,[C,C†]M> on 2×2, 3×2 and 4×2. The 3×2 saturated fixture has zero q8 output by cancellation. The 4×2 combination c=(1,−2,3,−4,5) gives 3,898,368 = 18,705,408 − 14,807,040. This is a complete physical Hilbert-space fixture, not an assumption of canonical boson commutation.

A separate nontrivial enlarged vector uses vacuum coefficient 17, B coefficients −2c, L coefficients 3c, and U=R+M coefficients 5c. For T_int=20H′ its exact q0/q2/q4/q6/q8 image norms are respectively 2304, 413857608, 121947335040, 191711843328, 97459200. Every nonvacuum sector independently satisfies its fixed-origin rescaling identity N/q. In physical-state coordinates T=C†R+D6M has nonzero components where this coherent M vector vanishes; those must not be dropped.

The independent C++ audit extends only the accepted independent third-moment review's geometry engine. It does not import/include the producer source. The local K expectation is evaluated as a sum of bilinear local forms, rather than constructing the producer's K image. It separately constructs CM, P, and T, and checks the above nontrivial q4/q6/q8 numbers in full and fixed-origin modes. Production q6 enumeration visits every C(31,5)=169,911 fixed-origin support, irrespective of M activity.

## Full image and normalization

For ψ=Bc_B+Lc_L+(R+M)c_U and T_int=dH′=dQ+hA,

- q0 and q2: obtain their complete amplitudes from the B rows of Kc, where K is the exact enlarged first-Hamiltonian matrix and B is the complete translation-invariant singlet q≤2 basis. Its Gram is diagonal, so the norm is the sum of (Kc)_i²/G_ii.
- q4: L(4d c_L+h c_B,pair)+R(h c_L+4d c_U)+h(D4R+CM)c_U.
- q6: M(h c_L+6d c_U)+h(C†R+D6M)c_U.
- q8: norm h²[||CMc_U||²+<Mc_U,Kcomm Mc_U>]. No production q8 support is enumerated.

Each coherent sum is formed before squaring, preserving all interference. Sum the orthogonal sector norms, divide by d²||ψ||², then subtract the exact Rayleigh quotient squared. For commutator expectations the bra is q6, so N/6 is the rescaling factor; the q4 norm CM uses N/4, even though their sum equals a q8 norm.

## Ground identification needed for Temple

The inherited ordered global comparison gives λ₂≥a1 and λ98≥a. A singlet even trial mean below a1 establishes an even-sector eigenvalue below a1 and hence identifies it as the unique global ground. There are 96 independent odd trial levels with all Ritz uppers below a. Together with the even ground, these exhaust the 97 possible levels below a. Thus the even-singlet sector contains exactly one level below a. Temple with cutoff a applies there, not across the global spectrum. The reference-bin multiplicities are oscillator overcounts C(3N+q−1,q), not physical triplet-number multiplicities.

Any resulting denominator update must retain the odd-band endpoints and complete counted spectral tails. A small complete residual alone does not certify a heat-trace startup or all-size gap. A subsequent scalar certificate must separately verify the trace bounds, recurrence, every finite window, and all short-size bridges.

## Accepted production result

The physical seal 7d6269e8b080301cf7f941f9c3b9fd9e3f1db339ce2587bd078ed3ded96def95 was checked and snapshotted before replay. Every independent raw contraction matches the producer exactly. The replay covers 4,495 q4 and 169,911 q6 fixed-origin supports. The family-M-zero part of the q6 T_int image norm is exactly 29130309466953366381448306212864, strictly positive.

The exact variance is

2448428261480406422854939482523166872870525432155341756199656673 / 6889457917632865412998596125412817968594334183872573551656077845000,

approximately 0.0003553876503424027. It is strictly positive and below the stated 75%-closure budget. The independently justified Temple ground lower is approximately −0.2532914854282799, with exact fraction in assembly_result.json. The q8 creation norm is exactly 814477123828667505456009253416960; it includes the q4 CM norm and q6 signed commutator expectation before the h² normalization. No production q8 state was constructed.

## Scalar and all-integer acceptance

PASS: for g=1/10, every periodic integer square side L≥2 has a unique ground state and gap at least **0.038976038275**. This is a discrete-coupling certificate.

The scalar seal is 0c7abb4cee911bb2c42990c0402b00dd7ecf62e0d607775d1f1c69c205424555. The independent replay reuses only previously accepted, hash-checked independent rational/exponential/interpolation functions. No producer module is imported. It re-evaluates the complete trace ratios from the new inputs and checks every recurrence state, rounding direction, joint-product physical base, order-transport step, and finite-size window.

The 4×4 denominator is exactly unchanged. The 8×4 denominator changes only its ground lower and explanatory metadata; all odd endpoints, multiplicities, omitted-level counts and spectral tails are identical. The largest 8×8 numerator retains exactly the previously accepted single 43D-search trial state's contribution. Its full space still has 2^128 states; no enlarged largest-seed residual is assumed or computed.

Initial β is 47/5. Coverage is exhaustive:

- L=2,…,7: inherited exact vacuum short-size bound, freshly checking periodic edge-square sums 16,18,32,50,72,98, g_max=1/10, the scalar constants and positivity.
- [8,16]: gap ≥0.052015820732 at physical β=94/5.
- [16,32]: gap ≥0.054902632007 at β=188/5.
- [32,64]: gap ≥0.055049054532 at β=376/5.
- Every integer L≥64: gap ≥0.038976038275 at terminal β=752/5 via the accepted interpolation/bootstrap lemma.

The optional [64,128] window is also verified but is not needed in the final minimum. Endpoint overlaps leave no missing integer sizes. The terminal rounded defect satisfies 0<u≤1/500, and the exact exponential witness exp(β gap)·32u<1 is independently checked. The short-size gap exceeds the final minimum.

## Fixed-vector coupling export

The separate polynomial seal 96027b2dbe17e94c922a3884122ff96c525354a359e143e38328fbd3abbbc3ed is accepted. The auditor decomposes U into distinct q4 R and q6 M families and rebuilds Q, Q², A and QA+AQ expectations independently. The bookkeeping decomposition has 57 columns; it does not claim 57 independent trial vectors or change the original 43D search.

The complete A² expectation follows exactly from the already verified full second moment at nonzero g=1/10, since H′(g)=Q+(g/2)A. Every coefficient of the affine mean, quadratic full second moment, and quadratic full variance matches. The variance quadratic is positive for every real g, independently checking the Gram/Cauchy–Schwarz consistency condition. These fixed-vector polynomials alone are not a continuous-coupling gap certificate; parameter-dependent sector cutoffs, tails, traces and all-size scalar bounds remain necessary.

## Arithmetic and reproducibility

The producer now checks every geometric V::add through an int64 intermediate with an int32 range assertion, and each scalar amplitude through checked 128-bit operations and a signed-64-bit check before GMP products. Direct geometry formulas have bounded integer inputs. The independent auditor uses separate long-long geometric coefficients and 128-bit linear combinations, then GMP arbitrary integers for every quadratic product and accumulated sum.

For the accepted fixtures/32-rung input, edge weight≤2 and degree≤4, L coefficients≤4 and M≤24. Conservative absolute bounds R<500, D4R<100,000, CM<276,480, C†R and D6M<100,000, and Kcomm M<1,000,000 bound all geometric intermediates. With at most 14 coefficients of magnitude≤2^56 and d≤40, scalar linear combinations remain far below 2^100, within signed 128-bit range. No large trial coefficient is squared in fixed-width arithmetic. Matching Gram factors are at most 27. All asserted translation divisions are exact.

Run bash REPRODUCE.sh. It checks inherited seals and snapshots, rebuilds the independent C++ auditor, replays physical and matching fixtures, performs the complete 8×4 contraction, then checks assembly, scalar coverage and coupling polynomials. CPU6, BLAS1 and a 1 GiB address-space cap are used; source assertions remain enabled. Direct source snapshots and every result used here are sealed. Prior source files are preserved.
