# Independent full-ground moment-pencil review

Updated 2026-10-10 15:09 America/New_York (EDT) / 19:09 UTC.

## Verdict and scope

The new exact lower endpoints for all 21 ground patches are accepted by independently recomputed rational negative quadratic forms, with their external spectral-count hypotheses checked against previously sealed physical reviews. All 14 newly successful scalar certificates and all their integer-size bridges pass independent exact replay. The ordinary spin-1/2 periodic square bilayer has unit rung exchange, equal straight intralayer exchange g in both directions and layers, and no crossed exchange. Its finite-volume ground state is unique, with these strongest retained bounds for every integer square side L≥2:

| g | Gap lower bound | Status |
|---|---:|---|
| 0.03 | 0.318423498447 | New improvement |
| 0.04 | 0.236077925502 | New improvement |
| 0.05 | 0.171822115684 | Previous independently accepted result retained |
| 0.06 | 0.107275412881 | New improvement |
| 0.07 | 0.032948924929 | New improvement |

The new independent x–time–y route at g=.07 gives 0.020459331271. All new ground certificates at g=.08 and .10 pass, but no scalar certificate succeeds on the checked β grid. Those failures are only bounded-grid diagnostics, not exclusions at every β or claims of physical gaplessness.

These are discrete coupling points, not a continuous-coupling result. No assertion is made about arbitrary aspect ratios, infinite-volume uniqueness, the actual physical gap, or optimality. The acceptance combines exact arithmetic and inherited analytic theorems; it is not formal proof-assistant verification.

## Immutable provenance and independence

The producer's full `FROZEN_MANIFEST_SHA256.json` has SHA-256

57a927ffa078343b6154668effba924ed57de1c3bd504bc657eeeaba1fb53417.

It seals 68 files, preserved here alongside the manifest. The separately frozen 48-file endpoint manifest has SHA-256

916b0e4a978fd7129d02f267d529e2494e26d04cdb329d50cfbf459eee1771bd.

`INPUT_SHA256.json` seals 169 snapshot files, including all physical matrices, old patches, quadratic bins, selected baseline scalar records and short-size inputs used by the new review. The matrices, old endpoint patches and count bins are matched byte-for-byte with the accepted snapshots in `tail_comparison_review` and `bilayer_frontier_review`. The complete seals of `large_seed_review`, `alternative_order_review`, `tail_comparison_review`, `quadratic_boson_review`, and `bilayer_frontier_review` are checked before and after calculation. Their manifest hashes and individual entries are preserved in `PRIOR_REVIEW_SHA256.json`.

No producer Python module is imported or executed. The matrix/witness auditor is separate from the producer. It uses ordinary exact rational Schur complements rather than the producer's fraction-free integer inertia. Its primary acceptance also evaluates the polynomial using just three integer quadratic forms. `independent_math.py` and `independent_scalar.py` are unchanged copies of the preceding independent frontier auditor's arithmetic and scalar auditor; this explicitly reuses their established independent implementation. The new drivers apply them to the new frozen endpoint records. No previous review or producer file is changed.

The project is an extracted shared snapshot with no local Git metadata; a filesystem write is not represented as a commit or publication. The auxiliary interval export produced later is outside this review and is not used to claim an interval certificate.

## Direct polynomial theorem: the essential acceptance test

Let H be finite-dimensional Hermitian on an invariant sector. Suppose that sector has exactly k eigenvalues, counting multiplicity, strictly below a. Eigenvalues equal to a are permitted. For an arbitrary rectangular trial map W and exact full moments

G=W*W, A=W*HW, B=(HW)*(HW),

put M(l)=B−(a+l)A+alG for l<a. Then M(l)=W*(H−a)(H−l)W.

The scalar polynomial (E−a)(E−l) is negative exactly when l<E<a, and is zero at either endpoint. A compression cannot have more negative directions than the full Hermitian form. Thus negative inertia at least j implies at least j sector eigenvalues in (l,a). In particular, if the k below-cutoff eigenvalues are λ₁≤⋯≤λ_k, then λ_(k+1−j)>l.

For k=1 it suffices to produce one exact rational/integer vector c with c*M(l)c<0. Equivalently, if the unique below-cutoff level were ≤l, the full polynomial would be positive semidefinite and no such negative direction could exist. This ground acceptance requires neither G>0 nor S>0 and permits any number of trial directions. The 11/29-dimensional trial space is not mistaken for the number of physical levels below the cutoff.

The external low count is indispensable. For H=diag(−2,−1,1), a=0 and trials spanning only the −1 and +1 eigenvectors, M(−11/10) has a negative direction, although the true ground is −2<−11/10. The correct external count is k=2, and the test bounds the second level, not the ground.

## Inverse-moment interpretation and cutoff eigenvalues

For the additional optimized-pencil interpretation, define K=A−aG and S=B−2aA+a²G. Assume S>0. With X=(H−a)W and T=(H−a)†, including its zero action at the cutoff, one has

X*X=S and X*TX=K.

T has exactly k negative eigenvalues ν_j=1/(λ_(k+1−j)−a), in increasing order. Generalized Ritz values μ_j of (K,S) satisfy ν_j≤μ_j. Hence every negative μ_j gives λ_(k+1−j)≥a+1/μ_j. There are at most k negative μ values. No negative-definiteness assumption on K is appropriate when m>k.

The identity M(l)=S+(a−l)K connects exact endpoint inertia with these generalized Ritz values. The producer's lower endpoint has one negative direction, and its nearby upper bracket has none. The latter brackets this trial pencil's optimum; it is not a physical upper bound on the ground energy. The physical upper bound remains the exact saved Rayleigh quotient.

A cutoff eigenvalue is harmless for the direct theorem and for the Moore–Penrose identity. If W contains a pure cutoff eigenvector, S becomes singular and this nonsingular pencil implementation rejects it, but the direct polynomial test can still be valid. Independent small exact regression cases include m>k, cutoff spectral components, a singular-S direct test, nonzero leakage and the missing-count counterexample.

## Full physical moments, normalization and count closure

For N=nx·ny rungs the shifted Hamiltonian is H′=H+3N/4. The stored integer matrices are G, K_num and J_num with positive integer denominator d:

A=K_num/d, B=J_num/d².

All products use Python arbitrary-precision integers or rational fractions; d² and witness products are never evaluated in a fixed-width integer type. The audit checks every matrix's integer entries, shape and exact symmetry. It recomputes the prior coefficient vector's norm, shifted Rayleigh quotient and complete residual square, and compares the results exactly with the sealed physical input.

The inherited physical proof builds the whole ground trial space from q=0,2 pair singlets and their q=4 images. Every column is spin zero, zero momentum and even triplet parity. Its complete H′ image includes q=6. Thus J_num contains full H′² leakage, not the square of a compressed Hamiltonian. These full matrices were physically reconstructed in the prior independent reviews and are reused here only by their checked sealed hashes.

The quadratic-boson reference gives full-space ordered bounds a0≤λ₁(H′), a1≤λ₂(H′), and a2≤λ_(2+3N)(H′). The audit independently reconstructs weighted periodic edges, α=1−2g, v=(3g²/4)Σw_e², the directed δ≤√(1−4g), and each bin a_q=−v/(α+δ)+qδ. Its reference multiplicity is binom(3N+q−1,q), distinct from the physical triplet-shell multiplicity binom(N,q)3^q. Through q=N the reference count binom(4N,N) is at least 4^N, so positive upper-tail overcounting is valid.

The ground Rayleigh quotient satisfies ρ<a1. It identifies a unique global ground in the even sector. The separately audited N translated spin-one directions have three orthogonal spin copies, all odd triplet parity, and their largest Ritz endpoint is strictly below a=a2. The N momentum modes are independent and mutually orthogonal in the relevant Gram/Hamiltonian form. Therefore there are at least 3N odd levels below a, as well as the even ground. The full-space count allows at most 1+3N below a, so the even sector has exactly one. No unrepresented even low level can have been missed.

Every new negative witness is recomputed both as a matrix quadratic form and as

(c*J_num c)/d² − (a+l)(c*K_num c)/d + al(c*G c) < 0.

All 21 pass strictly. The redundant independent rational-Schur replay also accepts all 105 matrices: G and S are positive definite, K and M(l) each have one negative eigenvalue, and every upper-bracket matrix is positive definite. Each l improves its previous ground endpoint, lies below its physical Rayleigh upper bound, and has the exact reported width and gain. The new complete-band patch differs only in that ground lower endpoint and associated metadata. All triplet bounds, multiplicities, full-spectrum bins and physical upper bounds are unchanged.

| Patch | Physical spins | Full Hilbert dimension | Ground trial dimension | Retained full low band |
|---|---:|---:|---:|---:|
| 4×4 rungs | 32 | 2^32 | 11 | 49 |
| 8×4 rungs | 64 | 2^64 | 29 | 97 |
| 8×8 rungs | 128 | 2^128 | 29 | 193 |

Only one ground state is retained in each patch. Trial dimension, retained state count, Hilbert dimension and sparse support size are different notions. No additional physical vector family, H-applied state family, higher moment or maximum-patch full-spectrum diagonalization is used.

## Exact scalar replay and order transport

Every successful record is replayed from the new endpoints using independent 384-bit directed integer exponential enclosures, all retained-band terms and every positive q≥2 reference-tail term. The full physical energy shift is restored in all partition-function ratios. Saved 16-decimal lower witnesses J1,J2,C0 must be no larger than the independently computed rigorous lower bounds.

For the three first-cycle lower purities (a,b,c), the exact partition-function monomial ledger checks the coordinate basepoints and the adjacent-swap identity e·c²=b·a². Transport to the common canonical base (8,8,2β) is

- x–y–time: (a,b,c)
- x–time–y: (a,b√c,b²c)
- time–x–y: (a√b,a²b√c,a⁴b²c)

Directed square-root witnesses and every 18-decimal downward rounding are checked. The canonical recurrence is applied only after this transport. Every saved defect update, onset side, inverse temperature, acceptance condition u≤1/500 and lower logarithmic endpoint is independently checked. A separate exact exponential inequality exp(β_final d)·32u<1 accepts the reported asymptotic gap d.

All 14 successful selected records, eight additional previous-β replays and seven selected failed sufficient-bound records pass. The 14 saved previous-β canonical triples are componentwise dominated by the new triples, and their exact difference vectors are independently reconstructed. All earlier certificates remain valid. An early-stop rule need not choose the strongest logarithmic endpoint, even when its input is improved: the newly selected g=.05 txy endpoint is 0.171026464125, so the stronger previously accepted 0.171822115684 is retained. There is no claim of regression in the physical bound or of optimized global β selection.

## Every integer size is covered

The short-size g≤.06 comparison is independently replayed for L=2,…,7, including odd-side occupancy bounds and length-two parallel bonds. Its minimum is 0.583853380272. For g≤.10, the independently replayed quadratic comparison uses weighted edge-square sums [16,18,32,50,72,98], α≥4/5, δ≥δ_lower≤√(3/5), and v≤147/200. It yields the uniform short-size lower bound

δ_lower−(147/200)/(4/5+δ_lower)=0.307810466553…>0.

Uniformity follows from monotonicity of this comparison expression in α, δ and v, not from assumed physical-gap monotonicity in g. The singlet product has H′ expectation zero, so this positive lower bound on λ₂(H′) also bounds the gap and proves short-size uniqueness.

All finite-window interpolations are recomputed, including dominant-weight square-root inequalities, both signed-transfer one-dimensional steps and a direct exponential gap witness. For the strongest g=.07 txy certificate:

- β_initial=49/5; canonical onset L=64 at β_final=784/5
- Every integer L∈[8,16] has gap ≥0.094399615657
- Every integer L∈[16,32] has gap ≥0.062065895117
- Every integer L∈[32,64] has gap ≥0.048024776703
- Every integer L≥64 has gap ≥0.032948924929

The six short sizes close the remaining L<8 range. The extra [64,128] window is verified but is not needed. All other successful orders have their own independently checked windows, so no integer size is omitted.

## Bounded diagnostic and reproducibility

The independent scan repeats 501 β values from 5 through 30 in steps .05 for three orders and seven couplings: 10,521 samples. It checks each saved successful-proposal count and score. Selection may additionally use an explicitly replayed previous β. At g=.08 and .10 all six order/coupling grids have zero accepted proposals. This supplies no all-β exclusion and says nothing about physical gaplessness or other geometries, trial spaces, intermediate order changes, or inequalities.

Run `bash REPRODUCE.sh`. The fast direct-witness acceptance is separately available as `python audit_direct.py`; the redundant exact Schur inertia checks take longer. Every substantive numerical process pins itself to one CPU, sets BLAS/OpenMP threads to one and imposes a 1.5 GiB address-space limit. The full rational-Schur pass took about 313 seconds; maximum observed resident memory across the main auditors was under 20 MiB. Reproduction writes only this review directory. It neither changes producer inputs nor makes any external write.

`MANIFEST_SHA256.json` seals the finished review. Verify it before reproduction: timing-bearing logs/results may change on a repeated run. `REVIEW_STATUS.json` records the final accepted claims; the `results` directory contains exact endpoints, counts, negative witnesses, inertias, scalar and window replays, previous-certificate dominance and bounded-grid diagnostics.
