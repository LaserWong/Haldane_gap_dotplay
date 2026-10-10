# Independent ordinary-bilayer frontier review

Updated 2026-10-10 14:51 America/New_York (EDT) / 18:51 UTC.

## Verdict and exact scope

For the ordinary spin-1/2 square bilayer with unit vertical rung exchange, equal straight intralayer exchange g=7/100 in both layers and both lattice directions, and no crossed exchanges,

Δ_L ≥ 24790852531 / 10^12 = 0.024790852531

for every integer periodic square side L≥2. The finite-volume ground state is unique. This is an independently replayed exact-arithmetic sufficient certificate, with inherited analytic transfer/interpolation theorems; it is not formal proof-assistant verification or an estimate of the actual gap.

The independent x–time–y certificate gives 9272103501 / 10^12 = 0.009272103501 on the same all-integer scope. The stronger result uses time–x–y, then explicitly transports to the standard x–y–time staircase.

At g=.08 and .10, all six new physical patches pass complete-band certification. No successful scalar proposal is found on the independently repeated grid β=5,…,30 in steps .05, for any of the three inequivalent placements of the time direction. Selected failed sufficient-bound witnesses also replay exactly. These are bounded diagnostics: they prove neither an all-β exclusion nor physical gaplessness, and do not exclude other geometries, trial families, order changes, or inequalities. The canonical x–y–time route at g=.07 also has no successful proposal on that grid.

## Provenance and independence

The immutable producer manifest is `snapshot/low_band/frontier_g007_g010/FROZEN_MANIFEST_1845.json`, SHA-256:

55b0ddf8e317c6953d0487a26880b075231d7fcc37c5a91a475a83b5a71dcb47

Its 70 listed files, plus the manifest, are copied here and verified. `INPUT_SHA256.json` records the snapshot bytes. The working tree is an extracted shared snapshot without Git metadata; this review does not infer a commit or publication.

`PRIOR_REVIEW_SHA256.json` seals the complete manifests and files of `large_seed_review`, `alternative_order_review`, `tail_comparison_review`, and `quadratic_boson_review`. Every prerequisite file was checked. The three producer geometry hashes equal the previously independently rebuilt geometry's frozen source hashes. No geometry contraction is rerun and no prior reviewed directory is modified.

The physical reconstruction is a specialization of the earlier independent physical auditor, not the producer. Its four-spin kernel is reconstructed from physical spin matrices. Its geometry and graph helper are taken from the sealed independent review. The arithmetic helper is an unchanged copy of the separate independent integer/rational implementation. The frontier auditor adapts earlier independent scalar code to the new couplings and adds explicit floor-clipping, short-size, and selected-failure checks. No producer Python module is imported or executed by this review.

## New coupling-dependent physical replay

All nine combinations of g=.07,.08,.10 and patches 4×4,8×4,8×8 pass:

1. Rebuild every ground M0,…,M4 moment and G/K/J matrix from the independently certified coupling-independent F/S/V/W geometry. These include complete H² contributions in four- and six-triplet sectors.
2. Use exact Schur elimination to identify the trial columns. Independently evaluate the stored integer coefficient vector, exact norm, shifted Rayleigh quotient, and full residual square. The stored coefficient vector is only a proposal; no floating eigensolver result is trusted for acceptance.
3. Reconstruct the translated generator W from the bare triplet and the physical kernel, then its complete HW image. Compare every nonzero coefficient with the frozen columns; no leakage is removed.
4. Check every one-site basis digit under every displacement, the exact highest-weight condition, every displacement Gram/H/H² moment, and all Fourier symbols in Q(√2). Check positive Gram symbols, nonnegative residual squares, and all directed rational energy/residual bounds.

The ground trial dimensions are 11,29,29. The full physical dimensions are 2^32,2^64,2^128. The retained complete bands contain 49,97,193 states, respectively: one ground state and N spin-one momentum states with multiplicity three. The single translated-generator supports are 85,181,373, and complete H-image supports are 3,185;15,466;67,755. These quantities are distinct. No maximum-patch full-spectrum diagonalization or MPS bond dimension is used.

The old affine relative-form local positivity certificates also replay; their own ground Temple test can fail without affecting the stronger count-based certificate used here.

## Full-space reference counting and Temple endpoints

Let N be the rung count, H′=H+3N/4, α=1−2g, and δ=√(1−4g). The independently accepted quadratic-boson theorem gives ordered bounds for the full physical spectrum via a stable 3N-mode reference oscillator. With weighted periodic edges w_e,

v=(3g²/4)Σ_e w_e², E_b=−v/(α+δ).

Its q-th reference energy is E_b+qδ with multiplicity binom(3N+q−1,q). This reference multiplicity is not the physical triplet-shell multiplicity binom(N,q)3^q. They are never substituted for one another or pointwise merged.

The audit reconstructs every weighted edge, degree, v, α, squared frequency bound, directed rational root interval, bin endpoint, multiplicity, first ordered index, and cumulative count. Through q=N the reference count is binom(4N,N)≥4^N, so the finite positive sum safely overcounts all physical eigenvalues. The first three endpoints give a0≤λ1, a1≤λ2, and a2≤λ_(2+3N).

The singlet trial has ρ<a1. Every triplet momentum Ritz upper bound is below a2. Exact invariant sectors and spin multiplicities therefore supply exactly 1+3N states below a2; no omitted low state remains. The full ground is unique and singlet. Every represented singlet or momentum/spin sector has precisely one level below a2 and all other levels at least a2.

For each such sector the full residual gives the rank-one Temple bound

λ≥θ−r²/(a2−θ), with θ<a2 and r²≥0.

Every exact rational ground endpoint and Q(√2) triplet endpoint is independently reconstructed, including the directed 14-decimal lower approximations. The new global-floor clipping is separately verified:

- Ground lower endpoint is max(Temple lower,a0)
- Triplet lower endpoint is max(Temple lower,a1)

The triplet step is sound because these spin-one invariant sectors are orthogonal to the unique singlet ground. This clipping genuinely affects 9 triplet endpoints on the g=.07 8×8 patch; it is not silently ignored. Across g=.08/.10 the corresponding counts are retained in `results/patch_review.json`.

## Independent heat trace, order transport, and scalar certificate

For each required β, the complete retained-band contribution bounds the trace from both sides. The upper bound adds every positive reference-tail term q=2,…,N with its correct oscillator multiplicity. The actual physical energy shift is explicitly restored in every partition-function ratio; an extensive trial-energy shift is not assumed.

The independent exponential enclosure uses directed integer Taylor arithmetic with 384 binary fractional bits, reduction to |x|≤1/16, 80 terms, a rigorous positive remainder, and directed squaring. It differs from the producer implementation. All saved initial ratio witnesses in the accepted g=.07 certificates agree exactly with the independent 16-decimal floors.

The partition-function monomial ledger verifies the basepoints and adjacent-direction cancellation identities. For first-cycle bounds (a,b,c), transport to the common canonical base (8,8,2β) is:

- x–time–y: (a,b√c,b²c)
- time–x–y: (a√b,a²b√c,a⁴b²c)

Every square root and 18-decimal downward rounding is independently checked. Only after this transport is the canonical recursion used. Every saved rational defect update, acceptance threshold u≤1/500, accepted side and temperature, and logarithmic endpoint is checked. A separate rigorous inequality exp(β_final d)·32u<1 certifies the proposed gap d.

The txy certificate starts at β=49/5, accepts at side 64 and β_final=784/5, with gap .024790852531. The xty certificate starts at β=43/4, accepts at side 128 and β_final=344, with gap .009272103501.

## All-integer bridge, including new uniform short sizes

For L=2,…,7, the independent weighted edge-square sums are 16,18,32,50,72,98. This includes the parallel positive-direction bonds at L=2; replacing squared multiplicities by simple edge counts would be invalid.

Uniformly for these six sides and 0≤g≤1/10,

α≥4/5, δ≥δ_lower≤√(3/5), v≤147/200.

The directed δ_lower is verified by exact squared inequalities. Hence λ2(H′) is at least

δ_lower−(147/200)/(4/5+δ_lower) = 0.307810466553… >0.

The comparison expression is increasing in α and δ and decreasing in v. This proves its uniformity without asserting physical-gap monotonicity. The singlet product has H′ expectation zero, so λ1(H′)≤0; the same bound therefore applies to the physical gap and proves uniqueness on these short sizes.

For txy, independent finite-window interpolation and direct exponential gap witnesses give:

- Every integer L∈[8,16]: gap ≥ .087252183109
- Every integer L∈[16,32]: gap ≥ .054169796249
- Every integer L∈[32,64]: gap ≥ .040154192241

Each exceeds .024790852531. Together with short sizes and the canonical all-integer theorem for L≥64, no integer size is omitted. The additional saved [64,128] window is verified but not needed. All xty windows through its side-128 onset are separately verified as well.

## Finite-grid diagnostics and limits

The independent floating grid contains 501 temperatures per order and coupling, or 4,509 samples. At g=.07 it reproduces zero xyt, 39 xty and 70 txy successful proposals and the selected β values. At g=.08 and .10 all six order/coupling grids have zero successful proposals. All seven saved failed selected witnesses have independently valid exact trace-ratio bounds and replay to a nonpositive first-cycle bound or a canonical recurrence leaving its positivity domain.

A failure of these sufficient lower bounds does not establish that a true physical purity or gap fails. The floating grid is diagnostic only; mathematical acceptance of g=.07 uses the independent exact certificate above. There is no continuous-coupling global gap theorem, arbitrary-aspect-ratio assertion, all-β exclusion, optimality claim, or infinite-volume uniqueness claim in this review.

## Reproduction and resource scope

Run `bash REPRODUCE.sh` from this directory. It verifies immutable inputs, repeats the physical and scalar checks sequentially, and repeats the bounded diagnostic. It writes only this review directory, does not change the producer snapshot or external state, and imposes one CPU, BLAS/OpenMP thread count one, and at most 1.5 GiB address space. The inherited physical kernel lowers its limit to 1 GiB. The observed physical peak RSS was about 99 MiB.

`MANIFEST_SHA256.json` seals the completed review. Reproduction rewrites timing-bearing logs/results, so verify the seal before reproduction and regenerate a new seal if archiving the repeated run.
