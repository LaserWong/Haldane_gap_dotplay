# Benchmark rank195 and identify the g=.25 bottleneck

Updated 2026-10-10 17:42 America/New_York (EDT) / 21:42 UTC.

## Result

No new all-size gap is certified here. The exact M4 weighted E<4 comparison has dimension 195, including every single quintet at energy 3 and a fully counted 6,366-state complement. Its exact physical construction and 42 Schur-inertia endpoint groups pass. The bounded scalar scan fails at g=.25.

A stronger, exact all-temperature obstruction explains why further denominator expansion alone will not help this route:

- Three exact spin-one trial vectors give the physical small-trace lower bound Q4(β)≥1+3exp(−βd), with d=0.6780573395118954… . Their highest-weight nullspace search is 22-dimensional inside the 44-dimensional M_z=1 part of the 195-reference space; exact ladder closure, equal norms and equal Rayleigh energies are verified.
- Exact2×2 positive pivots bound every Rayleigh quotient in the saved M8 two-vector span from below. This is a trial-span bound, not a full-space ground-energy lower bound.
- Even if the M4 denominator were exact, all β and all coefficients in that saved largest span give post-cycle P≤0.669331<17/25, or fail initialization. The required first [8,16] window then has ideal purity at most 12/25<1/2.
- This excludes only the specified one-term Rayleigh/time-first/transported-early-window rule. It does not exclude a physical gap, additional numerator information, another early bridge, another inequality or changed seeds.

An additional exact variant supplies a necessary target for a different M8 Rayleigh vector: it must have ρ8<−16.3544559234426…, improving the current value by more than 0.000426143856862. This is necessary, not sufficient, and no such new vector is constructed in this package.

Read PROOF.md for all details. The optional .275/.3 tests were not launched because the first target's denominator-invariant bottleneck calls for a different input, not a harder coupling scan. No statement about those couplings is inferred.

## Inputs and resources

The maximum physical seed remains M8: 16 spin-one sites, dimension 43,046,721. Its saved two-vector span has 43,294-configuration support and remains Rayleigh-only. No new M8 action/residual, MPS claim or physical full-spectrum diagonalization is used.

The M4 reference has 195 vectors, full action union 1,898 and residual union 1,703 in physical dimension 6,561. Exact moment construction cost 0.956 CPU seconds. The complete physical endpoint benchmark cost 85.525 CPU seconds and 106,164 KiB peak RSS. Magnetic blocks have sizes 4,22,44,55,44,22,4. All jobs use one CPU, one BLAS thread and at most 1 GiB address space; the construction benchmark enforces a 600-CPU-second limit.

Producer replay independently reconstructs exact moments, the full residual, all inertia counts, the triplet ladder and energies, the span quotient bound, and both obstruction covers using separate 384-bit exponential enclosures. It passed in 110.50 seconds at 95,928 KiB peak RSS. External independent review remains separate.

## Navigation

- expanded_moments.json / expanded_inputs.json: complete counted rank195 comparison
- triplet_witness.json: exact highest-weight and lowered trial vectors
- obstruction_g1d4.json: fixed rank195 recipe's all-β obstruction
- denominator_obstruction_g1d4.json: obstruction even with exact small denominator and arbitrary saved-span coefficients
- necessary_numerator_target_g1d4.json: quantitative necessary new-numerator target
- verification.json / target_verification.json: producer replays with independent scalar arithmetic
- PHYSICAL_FREEZE.json: initial immutable review handoff
- EXTERNAL_INPUT_SHA256.json / PRESERVED_PREDECESSOR.json: inherited inputs and unchanged rank67 freeze
- FROZEN_MANIFEST.json: final complete package seal
- REPRODUCE.sh: clean sibling reproduction without modifying the freeze

All earlier archives and root files are unchanged. No GitHub action or remote publication is implied.
