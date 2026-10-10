# Independent review of combined ground endpoint certificates

Updated 2026-10-10 15:15 America/New_York (EDT, UTC−4) / 19:15 UTC.

## Verdict and precise scope

**PASS.** All 42 frozen patch recombinations, all 42 selected order records, all 30 successful full-band scalar certificates, and all 11 largest-ground-only numerator certificates pass an independent exact replay. Every successful certificate includes its complete finite-size bridge. The model is the ordinary spin-1/2 periodic square bilayer: unit antiferromagnetic rung exchange, equal positive straight intralayer exchange g in both layers and directions, and no crossed exchange. Positive-direction bonds are counted with their multiplicity, including the two parallel bonds when a period is two.

The strongest selected combined certificates certify a unique finite-volume ground state and the following gap lower bounds for **every integer square side L≥2**, separately at the listed coupling points:

| g | Initial β | Full odd-trial numerator | Largest ground-only numerator | Asymptotic onset |
|---|---:|---:|---:|---:|
| 0.03 | 267/20 | 0.341601445704 | 0.341601363665 | 8 |
| 0.04 | 49/4 | 0.272402896810 | 0.272402625840 | 8 |
| 0.05 | 57/5 | 0.203655275044 | 0.203654642229 | 8 |
| 0.06 | 52/5 | 0.164746706191 | 0.164744743967 | 16 |
| 0.07 | 203/20 | 0.093479385120 | 0.093477650352 | 16 |
| 0.08 | 197/20 | 0.023243965748 | 0.023241913957 | 64 |

These use the time–x–y order followed by valid transport to the canonical x–y–time staircase. The exact fractions, other successful orders, and all intermediate windows are in `results/accepted_certificates.json` and `results/ground_only_certificates.json`. The displayed gaps have exact decimal denominators; they are certified lower bounds, not physical gap estimates.

This review does not establish a coupling interval, arbitrary aspect ratios, infinite-volume ground-state uniqueness, optimality, or an all-temperature obstruction. The g=0.10 scan and the unsuccessful g=0.08 orders remain bounded-search failures. The package is an exact-arithmetic certificate plus accepted analytic theorems, not a formal proof-assistant proof.

## 1. Immutable provenance and independence

The audited producer is `low_band/combined_ground_bounds/FROZEN_MANIFEST_1906.json`, SHA-256:

452848690e6303fb768b1d48e90b3635a52e46c8f4c8c620f8906d956f0aa2bd.

Its files were checked before copying and again at completion; no frozen producer file was changed. The review snapshot preserves every producer output and every consumed physical endpoint, physical matrix, geometry and short-size input. `INPUT_SHA256.json` identifies all 302 snapshot files. The active tree is an extracted shared workspace without Git metadata; no newly verified commit or remote publication is asserted.

All files in eight preceding independent-review manifests were checked, not merely their status strings:

- `large_seed_review`
- `alternative_order_review`
- `bosonic_tail_review`
- `quadratic_boson_review`
- `tail_comparison_review`
- `bilayer_frontier_review`
- `variational_filter_review`
- `ground_moment_review`

The exact seals and their entire entry maps are retained in `PRIOR_REVIEW_SHA256.json`. Each combined ground base matches the accepted ground-moment snapshot by hash; each filter endpoint matches the accepted variational-filter snapshot; each filter-only base matches its accepted tail-comparison or frontier snapshot. All current physical source digests and producer code dependencies also match their frozen declarations.

The ground-moment review seal is e981ee1b4157ce0822c464f06883638ea16e3677ca58e4f1991152595ee5d14c. Its endpoint-only producer manifest is 916b0e4a978fd7129d02f267d529e2494e26d04cdb329d50cfbf459eee1771bd. The accepted filter producer manifest is 6b520dfee4a083c1f9d98561b859ce8a56790a83ad9f1091107d333e3ff11f3e.

The new executable scalar audit imports no producer module and no previous review module. `independent_math.py` was written for this review. In particular, it evaluates the **direct H′ physical trace**, rather than using the producer's Rayleigh-normalized trace and exponential prefactors. All exponentials use independent 512-bit directed arithmetic, 100 range-reduced Taylor terms, a geometric remainder, directed squaring, and reciprocal interval reversal. All decisions about certificate validity are exact rational inequalities. The floating scan is a separate diagnostic.

The existing physical endpoint theorems and transfer/interpolation theorems are explicitly reused through accepted sealed inputs. This review does not pretend to rebuild the entire 128-spin physical Hamiltonian or repeat the preceding geometry enumeration.

## 2. Why the two endpoint improvements can be combined

Set H′=H+3N/4. The accepted full-ground moment pencil certifies l₀≤λ₀(H′), with its essential external count: the even invariant sector has exactly one eigenvalue below the full-band cutoff. The accepted variational filter certifies a normalized even singlet φ and an upper endpoint u₀ for its expectation. Thus

l₀≤λ₀(H′)≤⟨φ,H′φ⟩≤u₀.

The upper endpoint is a bound for one trial expectation. It is not the upper bracket of the inverse-moment pencil and is not a residual bound for φ. The independent patch audit verifies l₀≤u₀<ρ, where ρ is the exact old Rayleigh quotient, at every patch. It independently recomputes ρ and the original full variance from the consumed G/K/J matrices, with arbitrary-precision arithmetic and the saved denominator normalization.

For τ≥0, spectral Jensen gives

Tr exp(−τH′)≥⟨φ,exp(−τH′)φ⟩≥exp(−τu₀).

The existing translated triplet trials are odd in triplet-number parity and mutually orthogonal after spin and momentum resolution. The filter remains even, so it is orthogonal to that whole family. Its Jensen term may therefore replace the old even trial's term in the same trace lower sum without assigning it an inherited residual or incorrectly claiming a new excited eigenvalue endpoint.

The trace upper uses exp(−τl₀), the unchanged triplet lower endpoints, and the unchanged omitted-spectrum upper-tail sum. The lower and upper constructions are independent statements about the same physical trace. Their trial vectors need not match a common approximate eigenbasis.

For all 42 patches, the audit reconstructs the expected patch from its sealed base and accepts only the exact ground-upper substitution, corresponding width, and declared metadata changes. Every other field is equal, including all triplet blocks, their multiplicities, their old endpoints, the full tail bins, and all source hashes. The pencil variant and filter-only variant therefore differ precisely in their certified ground lower endpoint, as intended.

## 3. Spectral counts and dimensional distinctions

The largest patch has 64 rungs and 128 spins, so its physical Hilbert dimension is 4^64=2^128. The three physical dimensions are 4^16, 4^32 and 4^64. The original ground search spaces have dimensions 11, 29 and 29 and each retains one ground trial state.

The filtered state generally leaves that original search space. It belongs to span{ψ,H′ψ}, of dimension at most two. Adjoining the residual direction to the original spaces gives dimension at most 12, 30 and 30. The original trial has q≤4, its original residual has even q≤6, and φ has q≤6. No full sparse filtered vector is required, and no filtered-state residual or higher production moment is certified here. These dimensions are unrelated to an MPS bond dimension; this construction is not an MPS calculation.

The complete retained low band has 1+3N states, hence 49, 97 and 193 states on the three patches. The unchanged quadratic-boson reference has 3N oscillator modes. The audit reconstructs weighted edges, α=1−2g, v=(3g²/4)Σwₑ², δ≤√(1−4g), and all lower bins

bq=−v/(α+δ)+qδ.

Their reference multiplicities are binom(3N+q−1,q), not the physical triplet-shell multiplicities binom(N,q)3^q. Through q=N, the reference count is binom(4N,N)≥4^N. Its positive overcount remains safe. The first omitted index is 2+3N, so the trace tail starts at q=2 only after the accepted full-band count. Every reference count and ordered index is independently checked.

“Largest ground-only” describes omission of the optional odd **numerator** trial terms in the time-first path. It still consumes the original largest G/K/J, including its full second moment, plus the reviewed geometry used to certify the filter. It is therefore not the strict largest-seed first-moment-only route. It also does not delete needed denominator upper-tail information. The new audit retains the complete trace upper even in this replay; only the lower numerator is changed.

## 4. Correlated ratios, cancellation and order transport

Let Z′N(τ)=Tr exp(−τH′N). For a staircase v₀→v₁→v₂→v₃ with v₀=(4,4,β) and v₃=(8,8,2β), the correlated quantities are

J₁=Z′(v₃)/Z′(v₀)^8,
J₂=Z′(v₃)^2/Z′(v₁)^8,
C₀=Z′(v₃)/Z′(v₂)^2.

The constant −3N/4 physical energy shift cancels exactly because every numerator and denominator has equal total Nτ. The new audit forms these ratios directly from H′ trace bounds. This independently checks cancellation of the producer's additional arbitrary Rayleigh normalizations; it never assumes those trial energies are extensive.

For txy, v₁=(4,4,2β) and v₂=(8,4,2β). Only the 64-rung patch is a numerator. Its filtered upper endpoint improves the numerator; the smaller filtered upper endpoints cancel from denominator normalizations, while their pencil lower endpoints improve the actual trace uppers. For xty, v₁=(8,4,β), v₂=(8,4,2β). For xyt, v₂=(8,8,β), so the largest patch's full trace upper is required. Ground-only deletion is accordingly replayed only for txy.

All 42 selected records satisfy 0<J₁,J₂,C₀≤1. The audit's independent, higher-precision ratio floors equal or improve their stored conservative witnesses. The same stored witnesses are then replayed exactly, so no silently substituted stronger seed is accepted.

Writing G(z)=1−(1−z)²/(2z²), the first cycle gives a=G(J₁), b=G(J₂a), c=G(C₀⁴a²b), with directed downward rounding. These are at the common post-cycle base (8,8,2β), in the selected direction order.

The exact adjacent-swap identity is e c²=b a². Purities are at most one, so a valid pair (a,b) yields the swapped lower pair (a√b,a²b). The audit checks formal partition-function exponents for each ratio and swap and independently verifies every rational square-root enclosure. Therefore canonical lower triples are

- xyt: (a,b,c)
- xty: (a,b√c,b²c)
- txy: (a√b,a²b√c,a⁴b²c)

No thermal quantity is relabeled as a spatial one. The basepoints and every n,m,β scaling are checked explicitly.

## 5. Exact recurrence and complete integer-size cover

From a canonical triple, the independent replay forms its upward-rounded defects. Each sequential step computes p=(1−d₁)^4(1−d₂)^2(1−d₃) and appends an upward enclosure of (1−p)²/(2p²). Every saved update, round number, doubled side and doubled inverse temperature agrees exactly.

At acceptance, 0<u=max(dᵢ)≤1/500. This is within the originally accepted small-defect theorem; the later 1/200 extension is not needed. The theorem supplies all integer L≥n, with gap at least β*⁻¹ log[1/(32u)]. Rather than trusting any floating logarithm, the audit accepts each saved asymptotic gap γ only after the strict rational inequality exp(β*γ)·32u<1 is proven by its independent upper exponential enclosure.

Every finite window before that onset is rebuilt using the accepted signed-transfer interpolation. For one direction, p=S²T>1/2, w=(1+√(2p−1))/2, r=(1−w)/w, D=T/(1+r²), and I(S,T)=(1−r)min(S√D,D). The two-dimensional result is I(A²√(2B−1),I(B,C)). All intermediate fractions and lower square roots match. Each recorded finite gap γ is accepted only when exp(βγ)(1−C*)<C* and C*>1/2. This includes odd intermediate integer sides.

The required windows are adjacent overlapping intervals [8,16],[16,32],… up to the asymptotic onset n. The script explicitly advances an interval-coverage cursor from 8 to n, verifies every required window, and separately checks the optional endpoint window. The final uniform gap is exactly the minimum of the asymptotic gap, all required finite-window gaps, and the short-size bound.

For g≤0.06, the six L=2,…,7 occupancy/Jacobi comparisons at g=0.06 are independently rebuilt, including every parity-chain positive LDL pivot, bin index, multiplicity and monotonicized endpoint. The minimum is 36490836267/62500000000=0.583853380272. Their extension to smaller g follows from larger comparison diagonals and smaller off-diagonal norm bounds, not an assumption about physical gap monotonicity.

For 0.06<g≤0.10, the independently checked uniform quadratic comparison uses squared edge-weight sums [16,18,32,50,72,98] on sides 2,…,7, α≥4/5, δ≥the saved rational lower bound to √(3/5), and v≤147/200. Its gap is δ−v/(α+δ)>0.3078104665537. The product singlet has ground energy at most zero, so the full-space first-excited lower endpoint is a gap lower bound. Comparison monotonicity in α,δ,v supplies the uniformity.

At g=0.08 and β=197/20, the required finite-window gaps are 0.085694716373, 0.052551882633 and 0.038596267315 on [8,16], [16,32] and [32,64]. The optional [64,128] window gives 0.032953695866. Every one exceeds the asymptotic 0.023243965748, and the short sizes exceed 0.3078. Thus the all-integer claim contains no unfilled finite-size interval. The corresponding ground-only replay independently gives 0.023241913957.

## 6. Search diagnostics and attribution limits

A separate direct-trace floating implementation rechecks all 501 temperatures β=5,…,30 in steps of 1/20 for each of three orders, seven couplings and two variants: 21,042 grid samples. It checks every selected β, successful-proposal count and best score. The 12 unsuccessful selected records are also checked in exact arithmetic: they either have a nonpositive first-cycle lower bound or leave the positivity domain of the scalar recurrence. They are failures of those saved sufficient bounds, never evidence of a physically closed gap.

The seven-row comparison table is verified against each exact hashed source. Its four variants generally select their temperatures separately. The table therefore reports best retained bounded-grid results; it is not a fixed-temperature decomposition or a proof that a particular endpoint change alone causes a stated numerical difference.

## 7. Reproduction and resource limits

Run `bash research_20261010/combined_ground_review/REPRODUCE.sh` from the repository root. It verifies the immutable review and input seals, then replays all exact certificates, bounded-grid diagnostics and comparison sources. Outputs go to a fresh `/tmp` directory; the frozen review and producer inputs are not overwritten. To check the live prerequisite packages too, run `python research_20261010/combined_ground_review/verify_seals.py --live`.

The Python processes are pinned to one available CPU with a 1 GiB address-space cap, and all BLAS/OpenMP thread settings are one. No external packages, eigensolvers, physical full spectra or new physical production moments are needed. The first full exact replay used about 22 MiB peak RSS and 83 seconds under shared load. Exact numerical results are reproducible; runtime fields naturally vary.
