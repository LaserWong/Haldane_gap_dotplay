# Independent staggered-second-moment review

2026-10-11 04:17 UTC / 2026-10-11 00:17 America/New_York (EDT).

## Accepted results and limits

The exact staggered B² formula, complete D26 local insertions, small periodic physical fixtures, physical length-32/64 contractions, κ32 ≤ 17/125 and κ64 ≤ 157/1000 are independently accepted. The mathematical, physical and resource checks below are separate. This supplies finite-volume observable bounds; it does not itself enlarge an all-size alternating-chain interval.

The model is the untwisted periodic spin-one chain with h_j = S_j · S_(j+1), unit bilinear exchange, H_L = Σ_j h_j and B_L = Σ_j (−1)^j h_j. The opposite choice of staggered origin replaces B by −B and leaves B² unchanged. Physical Hilbert dimension is 3^L, MPS bond dimension is D = 26, retained trial span dimension is 1, and the complete norm-transfer dimension is 676. No physical spectral truncation or thermal-transfer rank assumption is introduced.

Producer fixture manifest: 0cad4bf9a9bd907cd9be78a6eceaf20ec041b45c3d398fd664c38bd49ee88696.
Producer length-64 manifest: 26d1977cf2324cd693c306aecd3b621989364e773413192253670c0951ca3570.
All existing files and seals remain unchanged. The separately authorized length-32 extension is documented in Section 6.

## 1. Overlap-safe formula

Let T be the one-site double transfer, O = E_h the two-site insertion, U = E_(h²), V = E_(h01 h12 + h12 h01), and N_L = Tr(T^L). The periodic one-site tensor trial is exactly translation invariant by cyclicity of the virtual trace. For even L ≥ 4, fixing the first bond in the double sum for B² gives

    ⟨B_L²⟩ = L/N_L [Tr(U T^(L−2)) − Tr(V T^(L−3))
      + Σ_(r=2)^(L−2) (−1)^r Tr(O T^(r−2) O T^(L−r−2))].

The same-bond term occurs once. The two adjacent positions have negative sign and give the two ordered products in V after a cyclic translation. Every remaining displacement is disjoint, including displacement L−2. At L = 4 the sole disjoint displacement is 2. This counting includes the closing bond and requires no reflection assumption. Multiplication by L and division by the same-length norm each occur exactly once.

For K = [[T,O],[0,−T]], write K^n = [[P_n,R_n],[0,(−1)^n P_n]], with P_n = T^n. Direct block multiplication gives

    R_(a+b) = P_a R_b + (−1)^b R_a P_b.

Its expanded off-diagonal block is Σ_(j=0)^(n−1) T^j O (−T)^(n−1−j). At n = L−3, n is odd and the coefficient is (−1)^j; setting j = r−2 gives precisely the disjoint sum. Even intermediate powers must retain their signs.

The reviewer uses sequential literal doubled-matrix checks at powers 0 through 12 and both signs. For the length-64 production check it uses an independently coded left-to-right recurrence:

    P_(2a) = P_a²,
    R_(2a) = P_a R_a + (−1)^a R_a P_a,
    R_(2a+1) = P_(2a) O − R_(2a) T.

The producer instead accumulates powers right-to-left. No producer helper is imported by the reviewer.

## 2. Complete local and physical reconstruction

independent.cpp rebuilds all three integer tensors from the representation labels and coefficients. Its local Heisenberg matrix is assembled by spin-raising/lowering action on physical basis columns. It then constructs h² and the two ordered overlapping products by ordinary matrix multiplication, checks real symmetry and the exact spin-one polynomial (h+2I)(h+I)(h−I) = 0, and checks total physical magnetization conservation.

The tensor charge rule and local magnetization conservation imply preservation of virtual charge difference. All eleven sectors, of sizes 1, 8, 32, 80, 136, 162, 136, 80, 32, 8, 1, are retained. Every entry of T, O, U and V is independently reconstructed and compared exactly with b2_blocks.txt; T and O are additionally compared with the original pinned mps_blocks.txt. No saved U/V numbers are used to construct the new local insertions.

For L = 4 and 6, complete periodic amplitudes are computed as traces of pairs of half-chain tensor words. Full physical bond actions on all 81 or 729 basis states give Hψ, Bψ and every bond-pair group. They agree exactly with separate transfer contractions of norm, H, H², B², same-bond, adjacent and signed disjoint contributions. The D26 integers reproduce fixture.out. The producer's D2 example and a second noncommuting D2 family also pass, so the check is not confined to the special D26 tensor symmetry. Every staggered mean is exactly zero and the full physical energy variance is nonnegative.

Eight deliberately altered numerator/scalar expressions are distinguished by these fixtures: extra L, missing L, missing norm division, wrong adjacent sign, true adjacent omission, disjoint omission, closing-bond omission, and treating the L4 adjacent pair as a disjoint pair. These are exact mutation-expression checks, not claims of eight separate production reruns.

### Preserved historical label error

The producer's original bad[4] uses B² − L·adj even though its correct B² already includes −L·adj. That doubles the adjacent subtraction; it does not omit the adjacent term as the old prose says. The actual physical formula and exact physical comparisons are correct. The reviewer tests true omission as B² + L·adj. The producer subsequently records the same correction in its new length-64 package, without rewriting the old seal.

## 3. Independent physical length-64 contraction

independent64.cpp performs fresh exact GMP contractions using the reviewer's own matrix operations and left-to-right signed recurrence. For every sector it independently reproduces all six checkpoint integers: norm, total H, B², same-bond, adjacent anticommutator, and alternating disjoint contributions. It then sums and compares the full integers. The accepted independent N0_64 and total H0_64 also agree exactly.

The normalized trial effect is

    q64 = B2_64 / (9216 N0_64) = 0.007521781460785803… .

The exact rational and full integers are retained in review64.out and independent_scalar_result.json. The upper norm bound is ||B64|| ≤ 96, from cancellation of the scalar parts and ||h + I/2|| = 3/2. No H² production run was needed.

## 4. Independent fidelity and Gibbs proof

At β = 49/4 use the already accepted finite length-64 trace upper bound Q, Gibbs purity lower bound C, and shift a = 700741/500000. Their source is the previously independently reviewed n32 initialization certificate, not an unverified floating search. Set

    w = (1 + sqrt(2C−1))/2,
    E_lo = −71/10000,     δ = 19/100,
    μ = H0_64/N0_64 + 64a.

Independent rational Taylor bounds establish exp(−β E_lo) > Q and w > exp(βδ)(1−w). Since exp(−β E0′) ≤ Z ≤ Q, the first proves E0′ ≥ E_lo. Purity implies a unique largest Gibbs weight p0 ≥ w, and p1 ≤ 1−p0; the second proves the finite-volume gap exceeds δ. This is a finite64 bound, not an all-size gap of .19.

The spectral decomposition of the normalized trial gives F ≥ f = 1−(μ−E_lo)/δ. Let A = B64²/96², so 0 ≤ A ≤ I, q = ⟨ψ,Aψ⟩ and α = ⟨ground,A ground⟩. Applying Cauchy–Schwarz to A and I−A yields

    sqrt(F) ≤ sqrt(qα) + sqrt((1−q)(1−α)).

On the verified branch f > q, solving this two-outcome angle constraint gives

    α ≤ f q + (1−f)(1−q) + 2 sqrt(f q (1−f)(1−q)).

The reviewer uses this single-root expression rather than the producer's sum-of-two-roots square. Integer-square-root bracketing at 80 decimal places and exact rational arithmetic give α ≈ .07703360525. Finally,

    κ64 = Tr(ρ0 A) ≤ 1−w+wα < 157/1000,

with independent upper endpoint approximately .1569041668671222. The exact interval agrees with the producer's more finely rounded endpoint within 10^−75.

Translation makes the Gibbs spectral measure of B symmetric. The scalar inequality cosh(tx)−1 ≤ (x²/b²)(cosh(tb)−1), followed by Golden–Thompson, therefore supplies the valid finite trace loss

    1 ≤ Z_eta,64(β)/Z_0,64(β)
      ≤ 1 + (157/1000)[cosh(96 β eta)−1].

An all-size interval still requires a fresh scalar bootstrap and finite-size bridge. Neither this observable certificate nor the small fixtures perform that step.

## 5. Resource accounting and reproducibility

All successful numerical runs use CPU5, 256 MiB address-space limits, post-exec default/unblocked SIGXCPU checks, parent-death SIGKILL and an external whole-session wall/CPU watchdog. Process-group cleanup and subreaper accounting check that no workload descendants remain. Each attempt has an exclusive attempt marker. No unexpected retry is hidden.

- Local reconstruction and full tiny fixtures: wait4 .887566 CPU seconds, launcher .089090945 seconds, peak 15456 KiB.
- Independent length64: wait4 8.280454 CPU seconds, launcher .366451523 seconds, peak 29640 KiB.
- Independent scalar: wait4 .052942 CPU seconds, launcher .059919371 seconds, peak 9856 KiB.

The initial compiler launch failed before g++ executed because the parent imposed 256 MiB before the compile child requested 512 MiB. That failed attempt is preserved, with .001362 child CPU seconds and 3.124385815 launcher seconds. The parent explicitly authorized one corrected compile. Its child used 5.153076 seconds plus .2463234 launcher seconds; the separate length64 compile used 3.907435 plus .162774576 seconds. Compilation peak was 157288 KiB. All compilation, including the failed launcher, remains charged to the separate 30 CPU-second compile allowance.

The numerical sum through the independent64 scalar is 9.736423839 CPU seconds; the compilation sum is 12.595356791 seconds. Conservative replay caps and actual observed charges are kept separate. Re-execution requires its own authorization and fresh output paths; the preserved one-shot launchers intentionally refuse an existing attempt.

The working copy has no .git directory, so no new local Git commit identity is asserted. Provenance is established by immutable input manifests, source/binary hashes and the new review seal. Root README/CURRENT_STATUS and producer seals are intentionally not overwritten by this worker.

## 6. Separately authorized length-32 extension

The corrected producer package uniform_alternating_b2_32_retry1 is frozen under manifest eccb1dcbcf423c3c2678bde743bce0882c81473415160bdd24d8beb4e87d9b75; its seal is SEAL_SHA256.txt. Its failed predecessor is preserved and pinned. The predecessor's mechanical 62 → 30 substitution accidentally changed sector dimension 162 to 130. Its guard stopped before that central block and no old output was accepted as a physical32 result. The corrected producer uses structured length constants and the unchanged eleven sector dimensions.

The reviewer independently compiles a length-parameterized left-to-right recurrence. At L = 32 it builds R_(L−3) = R29 and P30, with the same sector sizes and all arithmetic exact. Every norm, total H, B², same-bond, adjacent and alternating-disjoint integer matches all eleven corrected checkpoints. The summed norm and H match the independently accepted length-32 anchor.

For b32 = 48, the new trial effect is q32 = B2_32/(2304 N0_32) ≈ .01507219528810355. Using the previously reviewed finite32 trace and purity inputs, the independently implemented rational scalar check verifies E0′ ≥ −63/10000, finite-volume gap ≥ 21/100 and fidelity f ≈ .9753351376444873. It uses the same independently derived single-root effect inequality, obtaining α32 ≈ .07678875791653625 and

    κ32 < 17/125 = .136,

with independent outward endpoint approximately .13527650801543895. All full integers and exact rational bounds are in review32.out and independent_scalar32_result.json. No physical H² or new thermal calculation was performed.

The analogous finite trace bound is

    1 ≤ Z_eta,32(β)/Z_0,32(β)
      ≤ 1 + (17/125)[cosh(48 β eta)−1],       β = 49/4.

The new32 compile used 4.077913 child CPU seconds plus .198767282 launcher seconds, peak 157508 KiB. The independent32 contraction used 4.836022 plus .245937142 CPU seconds, peak 20020 KiB. Its scalar check used .054217 plus .074979762 CPU seconds, peak 9728 KiB. All exited zero with verified post-exec CPU5/AS/signal guards, no watchdog and no retry.

Through both production lengths and both scalar checks, the observed numerical review charge is 14.947579743 CPU seconds. All compilation attempts, including the preserved failed pre-exec attempt, total 16.872037073 CPU seconds. Final manifest construction is separately recorded as small housekeeping, still charged against the same review allowance. Both aggregate 30-second allowances remain unexhausted. No computation beyond the authorized review scope was launched.
