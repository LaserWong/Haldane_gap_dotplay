# Independent review: g = 0.10 endpoint diagnostics

2026-10-10 17:41 America/New_York (EDT, UTC−4) / 21:41 UTC.

## Verdict and scope

PASS for the three rational ground lower improvements, the restricted endpoint-weighted degree-five optimization brackets, and the fixed 43-dimensional numerator Ritz bracket. PASS for numerical reproduction of the explicitly conditional sensitivity scans. There is **no g = 0.10 startup or all-size gap certificate**, and no all-temperature impossibility theorem.

This review consumes the frozen producer manifest with SHA-256 `64aef0cf10637f509afd325ab230f8a74a97775b961657d1c5962e6c61be04bb`. All 28 covered files, all direct input pins, seven inherited seals containing 810 file entries, and equalities to accepted ground/geometry snapshots pass. Neither producer nor project-root nor GitHub files were changed. This extracted workspace has no Git metadata; no branch or commit can be inferred from it.

The model is the ordinary periodic square spin-1/2 bilayer, unit rung coupling, straight intralayer coupling g = 1/10, with the inherited periodic multiedge convention. N is the number of rungs and T = H′ = H + 3N/4. The 4×4, 8×4, and 8×8 patches have N = 16, 32, 64, and full Hilbert dimensions 2^32, 2^64, 2^128. Their old even-singlet trial ranks are 11, 29, 29; these are not full Hilbert dimensions or MPS bond dimensions. The numerator compression has dimension 43 and retains one state. Small denominator traces retain 49 and 97 levels respectively.

## Global ground identification before the sector cut

The inherited ordered comparison has λ₂ ≥ a₁ and λ_(2+3N) ≥ a. The bin labels are oscillator-reference overcounts, with multiplicity C(3N+q−1,q), not physical triplet-number multiplicities C(N,q)3^q. The replay independently checks their cumulative first indices, q = 1/2 endpoints, and total overcount. The q = 2 bin starts at 2+3N.

The even-singlet trial Rayleigh r is strictly below a₁. By min–max, there is an eigenvalue below a₁; λ₂ ≥ a₁ implies it is the unique global ground. Because the even-singlet subspace is invariant, the Rayleigh bound also gives an eigenvalue there below a₁, so this unique global ground belongs to that subspace. This proves ground identification independently of the new polynomial.

The inherited independent odd spin-triplet family has N spatial directions, multiplicity three, and its maximum Ritz upper is strictly below a. Thus at least 3N odd levels lie below a. Along with the even ground there are at least 1+3N global levels below a. The ordered bound λ_(2+3N) ≥ a allows no more. Consequently the even sector, and hence its singlet subspace, contains exactly one level below a. All other even-singlet levels are ≥ a. The replay verifies the numerical strict inequalities exactly; invariance, independent odd family, and ordered comparison are inherited from the verified source audits, not re-derived by a full Hilbert-space diagonalization here.

The cut a must therefore be applied **only in the appropriate invariant even-singlet space**, not across the global spectrum. The odd band demonstrably lies below a. This distinction is essential to the proof.

## Spectral upper bound and polynomial theorem

Each shifted rung term is a projector ≤ I. Each of the 4N intralayer spin-half bonds is bounded above by g/4. Hence T ≤ U I, U = N(1+g), in the full space and every invariant sector. The inherited ground lower L bounds the entire spectrum in the identified sector.

For ℓ < a, let pℓ(x) = (U−x)(x−a)(x−ℓ). On x ≤ ℓ and a ≤ x ≤ U it is nonnegative; it can be negative only for ℓ < x < a. A negative sector expectation therefore certifies an eigenvalue in (ℓ,a). Because the sector has exactly one eigenvalue below a and that eigenvalue is already identified as the unique global ground, λ₀ > ℓ. Thus the reported rational ℓ is a valid lower endpoint. Values exactly at ℓ, a or U give zero and do not undermine the implication.

Independent exact acceptance gives:

| Patch | New lower ℓ | Gain over old lower |
|---|---:|---:|
| 4×4 | −0.126993368814 | 0.0000846906642 |
| 8×4 | −0.255086154800 | 0.000284629863 |
| 8×8 | −0.517246809590 | 0.0007066132366 |

All stored integer coefficient vectors, four rational quadratic moments, and negative scalar witnesses match exact independent reconstruction. The 8×8 ground lower is ancillary to this txy calculation, which uses that patch only as a numerator. Patch comparisons show that only the ground lower and added witness differ; all odd endpoints and counted tails remain unchanged. Inherited descriptive metadata such as `ground_width` still describes the old patch width and is not used as the new interval width.

## Moment reconstruction and absence of M6

The independent replay imports no producer modules. It assembles the Gram and first-Hamiltonian matrices of (B,L,Ufamily) directly from accepted F/S/V/W/X/Y/Z geometry. It forms the coordinate matrices of B, T_int B, and T_int² B, where T_int = dT. Every available Gram/first-moment contraction through M4 is compared exactly with the accepted integer moments. It then computes M5 as the first Hamiltonian expectation of T_int² B, and matches the frozen M5.

A separate centered coordinate map R expresses the old W = (B,Lpair) family within (B,T_int B). The replay forms, for k = 0,…,3,

W* T^k W = d^(−k) R* [[M_k,M_(k+1)],[M_(k+1),M_(k+2)]] R.

Every matrix matches the frozen G/A/B/C and the inherited G/A/B matrices. A rational Gram-projection identity additionally proves that selected W spans the entire affine-in-T base family, including all exact dependencies. Its Gram is positive definite.

The largest moment used is M5. This establishes a third moment in the **old** W family. It does not provide an enlarged-state residual, M6, q8 support, or a denominator certificate inferred from a small residual. The numerator uses only a first Hamiltonian expectation in the 43D enlarged space.

## Restricted endpoint-class bracket

At ℓ_hi = ℓ + 10^−10, an independent rational symmetric Schur-complement/LDL calculation finds strictly positive pivots for both

W*(U−T)(T−a)(T−ℓ_hi)W and W*(T−L)(T−a)(T−ℓ_hi)W.

This is independent of the producer's integer Bareiss determinant implementation. It excludes a negative expectation for any vector in W, and excludes sums of such expectations with nonnegative coefficients, using either endpoint support weight. W contains all affine-in-T images of the base B, so the result covers the specified endpoint-weighted affine-square degree-five tests and their finite sums. The usual scalar interval cubic sum-of-squares representation places nonnegative cubic scalar support weights in that class; the exclusion here is tied to that representation and this fixed base family. It is not an unrestricted classification of every possible use of M0…M5, gap-aware sign polynomials, different trial families, or future moments.

For ℓ_hi ≤ ℓ′ ≤ a, each tested pencil is the convex combination with coefficient (a−ℓ′)/(a−ℓ_hi) of its matrix at ℓ_hi and the corresponding weighted (T−a)² matrix at a. The latter is positive semidefinite on the inherited support interval. Thus the exclusion persists through a, while the exact negative witness at ℓ proves the attainable threshold lies in a bracket of width 10^−10.

Separately, for the fixed 43D numerator matrices, the saved rational vector has Rayleigh ρ ≈ −0.5044427289405554. Exact LDL proves A−(ρ−10^−10)G positive definite; G is also positive definite. The minimum Rayleigh in this particular space lies between ρ−10^−10 and ρ. This is **not a physical ground lower bound** and does not rule out improvements in another space.

## Conditional scans and bottleneck

The second independent script imports no producer code and reconstructs normalized traces, txy startup, order transport, joint recurrence, and the bounded grid. All 23 cases match successful-point counts, best β, best scores, and minimum observed defects to 10^−10; all five trace-decomposition samples match. There are 301 β values from 5 to 20 inclusive in increments of 0.05, an initial row and at most ten recurrence advances.

At β = 9.25, the 8×4 denominator is evaluated at physical β = 18.5. Its ground contribution is approximately 1.0512446515, odd contribution 0.00003103453 and tail 0.000000004368. The 4×4 denominator at physical β = 9.25 has ground excess about 0.00315680, odd contribution 0.00809050 and tail 0.000903107.

The original 8×4 interval has width about 0.00270134294627. Hypothetically closing 75% of only that interval yields 99 successful grid proposals. Closing only the entire 4×4 ground interval, improving only odd lowers, or deleting only tails yields zero. A hypothetical numerator improvement of 0.003 yields 75 proposals, but the 43D bracket shows that coefficient retuning in that space cannot realize it. These comparisons identify **8×4 denominator ground uncertainty as the principal tested bounded-scan bottleneck**, rather than proving a universal obstruction.

Replacing the two small ground lowers by the new valid rational endpoints still gives zero successful proposals. Best observed minimum defect improves from about 0.2724016181 to 0.2211521921. Setting lower bounds equal to saved trial uppers, deleting tails, or lowering a trial upper without constructing a state are only sensitivity experiments, never physical certificates. The reported asymptotic proposal scores have not been promoted to all-integer-size gap bounds. A finite-grid failure does not exclude other β, orders, more iterations, improved inputs, or different methods.

## Adversarial and implementation checks

- A diagonal spectrum containing an eigenvalue −1 and another at 1, with ℓ = 0, a = 2, U = 4, has a negative test in the excited vector while its true ground is below ℓ. This rejects use of the polynomial without the one-low-level sector condition.
- With the same parameters p(5) < 0. This rejects use without an upper spectral support bound.
- Exact endpoint sign tests include ℓ, a and U. Raising ℓ to ℓ_hi makes each saved coefficient-vector expectation positive; both full matrices are independently positive definite.
- Exact span projection rejects silently excluding unselected dependent affine-base directions.
- Full byte seals are checked before and after exact replay. Read-only source paths are preserved.
- An initial added audit assertion incorrectly assumed physical q-sector multiplicities; inspecting the explicit reference-bin label exposed that reviewer assumption. The final test checks oscillator multiplicities C(3N+q−1,q), their cumulative indices and valid overcount. No producer claim or output changed as a result.

## Reproduction and stopping point

Run `bash REPRODUCE.sh`. It verifies this review seal, creates a fresh temporary output directory, and replays both scripts sequentially. Both jobs bind to CPU 7 when available, use one numerical-library thread, cap address space at 1 GiB and CPU time at 300 seconds. Exact replay used about 27 MiB maximum RSS and seconds of CPU; no full-space contraction was launched. Result JSON records timings and exact pivots' hashes.

The requested independent review is complete. A natural future research target is stronger justified 8×4 ground-lower information or genuinely expanded numerator data. This review itself does not launch such work or modify the accepted g ≤ 0.09 certificate range.
