# Independent larger-seed finite-size bridges and eight-round scalar replay

Updated: 2026-10-10 14:03 America/New_York (EDT) / 18:03 UTC.

Status: exact scalar and finite-size audit **passed**. The larger physical seeds are subject to their separately tracked independent physical audit. The eight-round continuation uses the frozen, already independently audited physical seed.

## Model and scope

The Hamiltonian is the ordinary spin-1/2 square bilayer, with unit antiferromagnetic vertical rung coupling and equal in-layer coupling `g` in the two spatial directions. There are no crossed exchanges. The periodic Hamiltonian keeps one positive-direction term at every rung in each spatial direction, on each layer. At side length two, this retains parallel terms and does not deduplicate the graph.

Write `N=L²`, `E00=−3N/4`, and `Q_i=S_{i,0}·S_{i,1}+3/4`, the rung-triplet projector. Thus

`K=H−E00 I=Σ_i Q_i + g Σ_(i,j) V_ij`,

where `V_ij=S_{i,0}·S_{j,0}+S_{i,1}·S_{j,1}`. The sum has `2N` rung-neighbor terms, including their periodic multiplicities, and each rung has degree four. The complete Hilbert-space dimension is `4^N`.

Every gap below is a strict, finite-volume certificate lower bound and establishes a unique finite-volume ground state. No assertion of infinite-volume uniqueness or of the actual numerical gap is made. The transfer/interpolation results are those already proved and independently reviewed in `../FINITE_WINDOW_INTERPOLATION.md` and the archived two-dimensional theory.

## 1. A simple exact local certificate handles both L=2 and L=3

On two rungs, the following **strictly positive definite** operator is certified in the original four-spin computational basis:

`M = V_ij + (3/2)(Q_i+Q_j) + (1/3)I > 0`.

The verifier independently assembles each physical `S_a·S_b` using the diagonal entries `±1/4` and spin-flip entries `1/2`. The resulting 16×16 integer matrix `24M` is saved in `local_small_sizes.json`. All 16 exact rational LDL pivots are positive. No trial-space truncation, numerical eigensolver, or unverified spectrum supplies this positivity.

Multiplying by `g≥0` and summing over the `2N` rung-neighbor terms yields

`K ≥ (1−6g) Q_total − (2Ng/3) I`.

For the three couplings considered, `α=1−6g>0`. The complete spectrum of `Q_total` begins with one eigenvalue zero and then eigenvalues at least one. Full-space min–max therefore gives

`λ₂(K) ≥ 1−6g−2Ng/3`.

The product of rung singlets has exact Rayleigh quotient zero for K, because each spin expectation vanishes and every inter-rung term has zero product expectation. Consequently `λ₁(K)≤0`, and

`gap(K)=λ₂(K)−λ₁(K) ≥ 1−(6+2N/3)g`.

A positive right-hand side also forces uniqueness. For L=2,3 the minimum occurs at L=3, giving:

| g | Uniform bound on L=2,3 |
| --- | --- |
| 3/100 | 16/25 = 0.64 |
| 1/25 | 13/25 = 0.52 |
| 1/20 | 2/5 = 0.40 |

This argument does not require bipartiteness, so it directly covers the odd 3×3 torus. It avoids extending the old hardcoded `g=.03`, L=2,3 Weyl value to new parameters. The optional stronger number-sector 3×3 certificates generated elsewhere are not needed here and are not relied upon.

## 2. Recover a safe base n=4 staircase from a correlated input

For the larger seeds, the physical base patches are 4×4, 8×4, and 8×8 at inverse temperature β₀. Their canonical staircase is

`A=Z(8,4;β₀)/Z(4,4;β₀)²`,

`B=Z(8,8;β₀)/Z(8,4;β₀)²`,

`C=Z(8,8;2β₀)/Z(8,8;β₀)²`.

The true transfer/thermal purities satisfy `0<A,B,C≤1`. The exact telescoping identity is

`A⁴ B² C = Z(8,8;2β₀)/Z(4,4;β₀)⁸ = J₁,true`.

The stored `J1=j` is a certified lower bound on `J₁,true`, conditional on the physical-seed audit. Because each other factor is at most one, `J₁,true≤A`, `J₁,true≤B`, and `J₁,true≤C`. Hence the conservative rational triple `(j,j,j)` is valid at the **base side n=m=4 and temperature β₀**.

Applying the already independently proved two-direction finite-window lemma to that triple covers every integer rectangle with sides between four and eight, including the needed squares L=4,5,6,7. This is a new safe use of the correlated ratio. It does not confuse the base side four with the saved `first_purities`, whose side is eight and whose temperature is `2β₀`.

The first updated purities are independently recomputed exactly as

`A₁= floor_16 G(J1)`,

`B₁= floor_16 G(J2 A₁)`,

`C₁= floor_16 G(C_stored⁴ A₁² B₁)`,

where `G(x)=1−(1−x)²/(2x²)` and `floor_16` rounds downward on the decimal grid `10^−16`. Every generated value equals the stored value. Subsequent recurrence updates are also recomputed independently, using upward rounding of defects at each elementary step.

## 3. Exact bridges for the larger seeds

| g | β₀ | L=4…8 window | L=8…16 window when required | Asymptotic onset | Combined all-L≥2 bound |
| --- | --- | --- | --- | --- | --- |
| 3/100 | 277/20 | 0.337867884900 | unnecessary | 8 | 0.281837226184 |
| 1/25 | 51/4 | 0.264039251376 | unnecessary | 8 | 0.179380190534 |
| 1/20 | 251/20 | 0.188350474715 | 0.169897925769 | 16 | 0.093620600631 |

These numbers are exact downward endpoints, not rounded floating evaluations used for acceptance. The JSON contains every fraction, its input hash, all intermediate purities, and square-root witnesses. A separate 256-bit directed exponential enclosure checks every proposed finite-window gap `d` by

`exp(βd) (1−T_lower) < T_lower`.

For asymptotic endpoints, the independent test is

`exp(βd) 32u < 1`,

at an accepted common defect `0<u≤1/500`. This directly validates the logarithmic lower bound without trusting the producer's logarithm code or its floating proposal.

The resulting integer-size cover is: L=2,3 by the local comparison; L=4…7 by the base window; L=8…15 for g=.05 by its first updated window; and every larger integer by the independently replayed asymptotic theorem.

**Qualification:** The physical trace and low-band inputs of these new large seeds remain conditional until their separate independent physical audit passes. This bridge proves the missing implication and performs its arithmetic; it does not independently reconstruct those many-rung physical inputs.

## 4. Independent eight-round continuation of the frozen g=.03 seed

The source is `low_band/scalar_refinement/symmetric_beta909d100_eight_rounds.json`. The frozen parent is `low_band/symmetric_correlated_beta909d100_FINAL.json`, with SHA-256

`19a1752cd99638a86b2f0482dec0347fdd3ae28d49f40cf672afb43202158f07`.

The verifier checks that this hash equals both the continuation's declared source hash and the earlier independent physical/scalar audit's source hash. The initial inverse temperature, x→y→temperature order, J1/J2/C values, first purities, and bootstrap input are unchanged. It does not accept a merely matching filename as evidence of inheritance.

Starting from the frozen input, every three-step round is recomputed with exact rational arithmetic. Initial defects are rounded upward to 128 bits. Round precisions are exactly 128, 128, 128, 128, 256, 512, 1024, and 2048 bits, matching all stored update fractions. The final side is 1024 and inverse temperature `116352/25`. The direct exponential test certifies

`gap ≥ 11205710127059 / 10^15 = 0.011205710127059`

for every integer L≥1024 under the already audited transfer theorem.

Exact finite-window bounds for the missing range are:

| Side interval | Gap lower bound |
| --- | --- |
| 4–8 | 0.040642307452 |
| 8–16 | 0.025170972644 |
| 16–32 | 0.018206380046 |
| 32–64 | 0.015078393431 |
| 64–128 | 0.013513267909 |
| 128–256 | 0.012630952861 |
| 256–512 | 0.012096484746 |
| 512–1024 | 0.011801433640 |

Every one exceeds the final asymptotic value. The already reviewed elementary Weyl estimate `1−3gL²≥.19` at g=.03 covers L=2,3. Therefore the eight-round endpoint is certified for **every integer L≥2**, inheriting the frozen independently audited physical inputs. This is a scalar enhancement only; it requires no new larger physical seed.

## Reproduction and resource limits

From the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
      python research_20261010/root_review/large_seed_bridges/audit_bridges.py

The verifier uses one CPU affinity, one BLAS thread, a one-GiB address-space limit, exact Python integer/Fraction arithmetic, and no numerical linear algebra package. It imports only the already reviewed finite-window implementation and independently checks its returned square-root inequalities and gap endpoints. No frozen input is modified.

The first complete run took 0.23 seconds of reported audit time and 11.2 MiB peak RSS. Results are `local_small_sizes.json`, `large_seed_bridge_results.json`, and `eight_round_scalar_results.json`; local artifact hashes are in `MANIFEST_SHA256.json`.
