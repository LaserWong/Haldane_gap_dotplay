# Independent review: staggered spin-1 MPS witnesses

Scope: uniform periodic spin-1 Heisenberg Hamiltonian H_n = sum_(j=0)^(n-1) S_j·S_(j+1 mod n), coupling one, physical Sz basis (-1,0,+1). For n=2 both periodic bond occurrences are retained, so H_2=2 S_0·S_1. All seed and numerator lengths here are even. This review changes no producer inputs or earlier seal.

## Physical verdict

PASS: the frozen real integer D=26 tensors define a legitimate periodic vector ψ_n. The derived vectors are Φ+ = sum_j (-1)^j (S_j^+/sqrt(2)) ψ_n and Φ− = F Φ+, where F maps each physical |m> to |-m>. Their unnormalized integer norms and complete Hamiltonian expectation numerators were independently verified. These are fixed trial vectors, not certified eigenvectors or a certified spin triplet. Their Rayleigh difference is not a spectral gap.

The auxiliary label rule A_m[i,j] != 0 implies label(j)-label(i)=2m. Every closed virtual path therefore has total physical Sz zero. The raising matrix has unit entries from -1 to 0 and 0 to +1, exactly S+/sqrt(2). Its tensor is B=(-,A_-1,A_0), with the first entry the zero matrix. Thus the three vectors have Sz 0,+1,-1 and are mutually orthogonal. All relevant exact norms are strictly positive.

The physical spinflip F is a unitary permutation. It sends Sz to -Sz and interchanges S+ and S−, hence F H F=H. Norm and energy equality for Φ± follows directly; no assertion that Fψ=ψ, or that ψ is an exact SU(2) singlet, is required.

## Sources, overlap, and multiplicity

Introduce one nilpotent variable on each layer. The coefficient uv of the trace of the product of local transfers is the norm of Φ+. Only powers 0 or 1 on each layer are retained, since the desired state contains exactly one source insertion per layer. This retains same-site bra/ket insertions; discarding u² and v² loses no contribution to uv. For the Hamiltonian bond at sites 0,1 the source derivative is B_s A_t − A_s B_t. Its two-layer coefficient includes both sources outside the bond, one inside and one outside, and both on the bond, including the same-site and opposite-site cases. The independent local builder enumerates these placements separately, rather than copying this derivative formula.

All tensors are real, so the norm transfer is sum A_m⊗A_m in the usual trace-of-product convention. Its source charge shifts are 0,-2,+2,0; the producer's group-index shifts 0,-1,+1,0 agree because adjacent groups differ by two. Eleven charge blocks have total auxiliary size 676 and largest diagonal side 162. The independent contraction engine uses global 676×676 indexing and explicit bra/ket insertion counts instead of the producer's rectangular-block and bit-mask representation.

Translation sends Φ+ to -Φ+ for even n, whereas ψ is translation invariant by cyclicity of the virtual trace. Consequently its Hamiltonian bond expectation is independent of the bond. Multiplying one exact bond insertion by n is correct, including the n=2 multibond convention. The relative staggered signs on the final periodic bond also agree only because n is even.

## Independent calculations

- Rebuilt every nonzero local norm/source and bond/source matrix entry by sparse tensor outer products and explicit physical h matrix elements. All eight matrices agree exactly with the frozen source file. Their ground components also reproduce the archived audited ground block file byte for byte.
- Expanded all physical words at n=2,4,6, without imposing a magnetization sector during construction, then applied every periodic Hamiltonian bond explicitly. All norms, full-H numerators, vector supports, and H-action supports match the producer. Φ± equality and the disjoint charge sectors are explicit checks.
- A separately implemented global-index GMP contraction matches all 48 norm/energy integers for every even 2≤n≤24.
- A separate sequential sparse ground engine, without the producer's binary power-squaring algorithm, matches every supplied ordinary-ground integer through n=48. Thus the n=28,32,40,48 numerator Rayleigh inputs have also been replayed.

## Dimensions and actual costs

The physical denominator Hilbert dimension is 3^n, and the numerator dimension is 3^(2n). Exactly three orthogonal states are retained in the denominator lower trace witness and one fixed state in the numerator. No eigensolver or variational coefficient search is used. ψ has bond dimension 26; each single-source vector admits bond at most 52 using triangular tangent tensors and a fixed off-diagonal closing matrix. This is an MPS bond bound, not the dimension of its physical support, not a 52-dimensional linear trial space, and not a claim of an untwisted uniform periodic trace representation.

Only n≤6 physical supports are expanded. The review enforces one CPU affinity and 1 GiB address-space caps. Independent global source contraction: 46.1745 CPU seconds, 111,624 KiB peak RSS. Independent ordinary ground contraction through 48: 5.41173 CPU seconds, 9,872 KiB peak RSS. Producer timings (not substituted for review cost) were 16.6101 CPU seconds / 66,288 KiB for source contraction through 24 and about 7.6 CPU seconds / 19 MiB for ordinary ground powers. No exponential physical support expansion or full spectrum is hidden in these costs.

## Scalar meaning and proof

Let α0 and α1 be the exact ψ and Φ± Rayleigh values at n; let R be the exact D26 Rayleigh value at 2n. Jensen's inequality on three orthonormal spectral measures gives

Z_n(β) ≥ exp(-βα0) [1 + 2 exp(-β(α1-α0))].

The fixed recipe uses L=exp(-2βR) as a lower numerator, and any valid upper denominator certificates U0≥Z_n(β), U1≥Z_n(2β). Its inputs J=L/U0^4 and C=L/U1² satisfy

J ≤ exp(-2βδ) / [1+2 exp(-βg)]^4,
C ≤ exp(-2βδ) / [1+2 exp(-2βg)]²,

where δ=R−2α0>0 and g=α1−α0>0. These are upper obstructions to this chosen certificate recipe. They are NOT upper bounds on the physical trace ratios with the true large-system numerator.

At hot β∈[0,1/2], Tr H_n=0 implies Z_n(β)≥3^n, so J≤exp(-R)/3^(4n). At cold β≥b, J≤exp(-2bδ). Both are below 2/5 and G(2/5)=−1/8. On every intervening closed box [l,u] of width 1/4, monotonic exponential bounds give upper endpoints by evaluating exp(-2lδ) in the numerator and exp(-ug), exp(-2ug) in the denominator. Shared endpoints are included; the hot, warm, and cold ranges cover the complete half-line.

The G function is increasing on (0,1]. Independent decimal-grid outward rounding with an 80-term Taylor enclosure and exact positive geometric remainder bounds the exponential; reciprocal bounds handle negative arguments. This differs from the producer's binary grid, 40-term expansion and preliminary 64-bit parameter enclosure. The replay uses exact physical rational parameters, checks that its box bounds improve every producer endpoint, and independently verifies every claimed excluded box.

For positive initialization a=G(J), b=G(C²a), the tested recipe allows any number of whole time-first cycles, followed by the specified joint-aware canonical conversion s=a sqrt(b), t=a²b, K=a²b. Its first canonical cycle is s'=G(max(s²t,K)), t'=G(max(t,K)²s'), and K is discarded thereafter. Every successful exclusion exhibits a nonpositive upper update before the accepted common target min(s,t)≥99/100. A finite loop cap or entrance of an optimistic upper orbit into the target yields only an inconclusive result. To exclude all delays, the replay checks each preceding conversion and proves that continued time-first evolution itself fails after finitely many positive cycles. It does not extrapolate a finite failed scan to all delays.

The inherited transfer/purification identification and the accepted conversion remain premises of the fixed recipe. The result does not cover new numerator witnesses, other geometries, arbitrary adaptive switching, new inequalities, or additional independently propagated joint information.

## Scalar verdicts

Independent exact directed replay verifies all producer exclusions:

| Denominator n | Complete half-line result | Global J upper display |
|---:|---|---:|
| 14 | Fixed recipe excluded for every β≥0 | 0.3439677774040145 |
| 16 | Fixed recipe excluded for every β≥0 | 0.4443968726381364 |
| 20 | Fixed recipe excluded for every β≥0 | 0.6346374878360025 |
| 24 | Bounded screen only | 0.7802532573943833 |

For n=24 the unresolved closed-box union is exactly [13/2,45/4]; outside it the specified recipe is excluded by the saved witnesses. A surviving optimistic upper orbit is not a realizable denominator upper certificate and does not establish actual scalar startup. No physical spectral gap conclusion follows from these exclusions or the unresolved window.

Machine-readable primary review outputs are independent_physical.json, independent_scalar.json, regressions.json, and CLAIM_VERDICTS.json. Frozen producer copies and their original manifests are under inputs/. REPRODUCE.sh rebuilds the independently implemented engines and exact results; it overwrites local replay outputs and timings, so run it on a copy when retaining the immutable seal.

Final clean replay resource measurements are recorded exactly in RESOURCES.json. The descriptive first-pass timings above are retained as an additional observed benchmark.
