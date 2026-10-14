Updated: 2026-10-10 14:30 EDT (America/New_York, UTC−4) / 18:30 UTC.

# Independent audit of the spin-2 finite I/P moment witness

## Decision

**Accepted for the explicitly stated interval relaxation.** Independent rational arithmetic verifies all 14 archived I/P interval inclusions at orders 2 through 8, the four proposed order-9/10 interval inclusions, positive integer multiplicities, and strictly positive I/P traces at every integer length L≥2. No producer code was executed or imported. The revised generated proof has corrected two overbroad interpretations identified during this audit.

The witness rules out an **unconditional** nontrivial-sector mass upper bound below one and a successful **numerator-one thermal certificate** based solely on this relaxation. It is not a spin-2 Hamiltonian, a local quantum transfer construction, a proof of gaplessness, or a no-go theorem for other scalar methods.

Audit entry points:

- [Independent verifier](independent_audit.py)
- [Exact results and provenance checks](audit_results.json)
- [Bounded run log](run.log)
- [Reconciled producer revision](producer_manifest_revision.json)
- [Reviewed frozen producer packet](../spin2_scalar_improvement/frozen_ip_witness/MANIFEST.json)
- [Reviewed generated proof](../spin2_scalar_improvement/frozen_ip_witness/IP_WITNESS_PROOF.md)

## 1. Exact input provenance and its limits

The physical inputs concern the periodic spin-2 isotropic Heisenberg chain,
H_L=Σ_j S_j·S_(j+1), coupling J=1 and S²=6. At L=2 both parallel bonds are
counted. I is the untwisted seam. P is a π rotation. C is a 2π/3 rotation.
The traces are Tr exp[−β(H_L(g)+aL)], with β=8 and a=5951/1250=4.7608.
No normalization from a different Hamiltonian or shift is substituted.

The lower-order rows were independently selected from the archived `trace_intervals.json`. The original file hash is `ed30cdae706c3907c08f69fe6913e81ff22c3c69e7b53733a1ef8fe0e4967690`. The original archive manifest confirms that hash. The 14 selected rows match the producer's frozen copy exactly, including endpoints, shifts, and dimensions. A portable full copy is [here](inputs/archive_trace_intervals.json).

These are the archive's complete-spectrum residual-validated rational enclosures, with the archive's stated IEEE-754, interval-inclusion and exact integer-dot-product assumptions. The L=4 β=8 rows also use the narrower prior exact-integer polynomial certificates. This audit verifies provenance and the exact use of those intervals. It does **not** independently rerun every archived many-body eigensystem. See the preserved [validation assumptions](inputs/ARCHIVE_VALIDATION.md) and [archive status](inputs/ARCHIVE_STATUS.json). Physical Hilbert dimensions are 5^L. They are not the artificial spatial-spectrum dimensions below.

The order-9/10 centers originate in the archived `exploratory_order10_results.json`, hash `0094c200f21c049090e931588b88466f684a29388ebcb575bf9cf7e2b4bfff9d`. The selected a=4.7608, β=8, maximum-order-10 row matches the frozen copied row. These are incomplete Ritz data. Completeness, omitted in-sector contributions and eigenvalue errors have not been enclosed. They are **not certified physical trace values or certified interval centers**.

The manifest of the generating package originally had hash `28f3a9a687161376f7d88134928d19ec67193d498d392ba9f5ea3680e0575aaf`. After the audit's scope corrections, only `IP_WITNESS_PROOF.md` and the manifest changed. The accepted manifest hash is `df696b5db74babc762f53743196ff7f76b766b1f7a292f5f808fb6e52adfe3be`. All numerical inputs, atoms, generating verifier and generated results stayed unchanged. This transition is explicit in [producer_manifest_revision.json](producer_manifest_revision.json). The [first audit record](audit_initial_results.json) is retained. The independent verifier pins the revised hash and fails if the frozen packet changes.

## 2. The precise mathematical relaxation

There are two finite real eigenvalue lists J and N, with repeated eigenvalues represented by positive integer counts. N is repeated in each of the three nontrivial D₂ characters. Define

    M_s(k) = Σ_j c_(s,j) x_(s,j)^k,
    I_k = M_J(k) + 3 M_N(k),
    P_k = M_J(k) − M_N(k).

The retained assumptions are:

1. The 14 fixed archived rational boxes constrain I_k and P_k for k=2,…,8.
2. Four explicitly prospective boxes constrain I_9,P_9,I_10,P_10.
3. The spectrum is real, with positive integer multiplicities. No dimension bound, first moment or zeroth moment is specified by the input data.
4. I_k and P_k are positive for every integer k≥2.

The spectrum has 17 rational groups in each list. Interpreting the decimal node strings as exact rationals gives

- dim J = 1,752,765,679,903,846,037
- dim N = 1,752,713,560,036,067,552, for one nontrivial list
- full singlet/triplet realization dimension = 7,010,906,360,012,048,693

These dimensions are artificial transfer-space dimensions. They are neither physical 5^L dimensions, trial-space sizes nor MPS bond dimensions. They are legal because the relaxation has no transfer-rank bound.

Every legitimate even-base Hankel positivity condition and atom-removal condition is automatically satisfied by these actual atoms. Specifically, for even b≥0, Σ_j c_j x_j^b v(x_j)v(x_j)^T is positive semidefinite. Removing one actual copy of an atom preserves positivity. Signed odd moments may appear as off-diagonal entries of these matrices. No assertion is made that an arbitrary odd-base Hankel matrix is positive semidefinite.

## 3. Exact inclusion checks and tolerances

All 14 lower-order inclusions are strict rational comparisons. No numerical acceptance tolerance, midpoint replacement or enlarged input interval is used. The tightest input widths are 10^−16 at L=4, for both I and P. Their distances from the witness to the nearer endpoint are approximately 5×10^−17, verified exactly. The exact per-row margins are in `audit_results.json`.

For k=9,10 the center is reconstructed from the saved J/N decimal values using
I=J+3N and P=J−N. The exact discrepancies are nonzero but exceptionally small:

| Order | Twist | Absolute discrepancy from reconstructed center | Proposed radius |
|---|---|---:|---:|
| 9 | I | ≈5.5481949261×10^−65 | 6×10^−6 |
| 9 | P | ≈1.1014373788×10^−64 | 6×10^−6 |
| 10 | I | ≈4.7942501136×10^−65 | 5×10^−5 |
| 10 | P | ≈5.1774899249×10^−68 | 5×10^−5 |

Thus a common radius 1.102×10^−64 already suffices around these particular reconstructed centers, though exact equality with zero radius has not been proved. The reconstructed I9 center differs from the separately stored Z9 decimal by −3.9475×10^−16. The I10 difference is +10^−15. These harmless rounding differences must still be distinguished from physical trace errors.

The proposed 6×10^−6 and 5×10^−5 radii exceed the earlier heat-kernel error budgets ≈5.7707121×10^−6 and ≈4.4357032×10^−5 conditional on Z≤100. That comparison does **not** enclose the Ritz omissions and does **not** turn the proposed boxes into physical certificates. The kernel's error theorem was independently audited elsewhere. This review does not repeat that audit.

For any future replacement intervals the exact necessary test for reusing this particular witness is that every interval contains its corresponding moment. It is insufficient that a true trace, or a future narrow interval, merely lies inside one of these broad proposed boxes. A narrower box may exclude the witness. Higher precision alone at the same reconstructed centers would need an extreme reduction to exclude it, but newly completed traces could move the centers and must be evaluated afresh.

## 4. All-length positivity proof

The leading atoms are α=103/100 in J and γ=51/50 in N, each with multiplicity one. Every other atom satisfies |x|<r=3/4. Let C_J and C_N be the exact tenth moments of the remaining atoms. The independent sums give

    C_J ≈ 3.0113253354557052,
    C_N ≈ 2.8136004811851687.

For every integer k≥10,

    |R_J(k)| ≤ C_J r^(k−10),
    |R_N(k)| ≤ C_N r^(k−10).

The independent verifier checks I_k>0 and P_k>0 exactly for 2≤k≤31. At k=32, the two lower bounds are strictly positive:

    α^32 + 3γ^32 − (C_J+3C_N)r^22 > 8.2082761513,
    α^32 − γ^32 − (C_J+C_N)r^22 > 0.6801516217.

The geometric remainders decrease. The leading I expression increases, and the leading P difference increases because

    (α^(k+1)−γ^(k+1)) − (α^k−γ^k)
      = α^k(α−1) − γ^k(γ−1) > 0.

These inequalities prove positivity for every k≥32, completing all integer lengths k≥2 without extrapolating a finite numerical scan.

A real SO(3) representation realizes J as singlets and N as triplets. Its rotation trace at angle θ is M_J(k)+(1+2cos θ)M_N(k). This is affine in a coefficient lying in [−1,3], so positivity of the two endpoint traces P_k and I_k implies positivity at every rotation angle. Group covariance alone therefore does not eliminate this witness.

## 5. What is excluded

The same shift conversion is applied to every atom:

    a₁=4.76121, ρ=exp[−8(a₁−4.7608)]=exp(−41/12500).

Independent odd/even Taylor bounds certify

    ρα > 1.0266271345,
    ργ > 1.0166598807.

Every rescaled physical-input box would need the corresponding factor ρ^k. The original a=4.7608 boxes are not reused unchanged at a₁.

For every even L≥2 the remaining spectral powers are nonnegative. Hence

    I_L(a₁) ≥ (ρα)^L+3(ργ)^L > 4,
    total nontrivial-sector mass ≥ 3(ργ)^L > 3.

Any unconditional upper bound valid for the entire stated relaxation must allow these values. Consequently:

- It cannot bound the total nontrivial-sector mass below one.
- If a thermal-purity certificate uses only the numerator lower bound one and an upper bound U_L on I_L(a₁), its lower-bound expression 1/U_L² is less than 1/16 at every even L≥2. It cannot reach the proposed 7/8 startup threshold.

This is a limitation on that proof expression. It is **not an upper bound on the physical chain's thermal purity**. There is no physical 2β numerator in the constructed relaxation, and the actual numerator can be larger than one.

The independently checked selected-length values are:

| L | Abstract spatial purity S(L/2,8) | Lower bound on I_L(a₁) | Ceiling on 1/U_L² |
|---|---|---:|---:|
| 128 | (0.273805237, 0.273805238) | 53.761701 | 0.000345982393 |
| 256 | (0.360188494, 0.360188495) | 1041.06022 | 9.226740283×10^−7 |
| 512 | (0.656301666, 0.656301667) | 711303.935911 | 1.976467041×10^−12 |
| 1024 | (0.960713368, 0.960713369) | 486076088872.512754 | 4.232446573×10^−24 |

The L=128 ratio was recomputed directly from the rational order-64 and order-128 sums. The larger lengths use rigorous leading-atom/remainder bounds. All acceptance comparisons and outward decimal endpoints are exact.

## 6. What remains open or outside this certificate

1. **Conditional J-cutoff atom exclusion.** If an argument assumes all J atoms have modulus at most ℓ<1.03 at a=4.7608, the witness is inadmissible under that additional assumption. It cannot refute a joint optimization over that smaller feasible set. This was corrected in the producer's revised proof.
2. **Existing C moments.** C is a 2π/3 rotation, with triplet character zero. This realization predicts C8=M_J(8)≈8.6054184342, whereas the archived interval is approximately [0.6267925313,0.6267926901]. That single existing datum excludes this realization. No C-aware exact integer witness is accepted by this audit. Exploratory weighted/PSD results have a different scope.
3. **Temperature consistency and locality.** No common local Hamiltonian family producing the β and 2β heat traces is constructed. Local quantum-transfer structure, physical heat-semigroup consistency, further moments, or stronger numerator estimates may remove the witness or enable another certificate.
4. **MPS diagnostics.** Exploratory twisted-MPS computations are not premises of this result and have not been certified here. The use of a₁ identifies the same stated shift as the archived MPS energy claim. This audit proves the scalar rescaling and does not re-audit that MPS claim.
5. **The physical gap.** No conclusion about a uniform spin-2 gap, gaplessness, phase boundary or optimal initialization follows from this witness.

## Reproduction and resource use

From the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python research_20261010/spin2_moment_review/independent_audit.py

Only the Python standard library is used. The verifier fixes CPU affinity to one available CPU, address space to 1 GiB and CPU time to 120 seconds. The accepted run took approximately 0.22 seconds and 11 MiB maximum RSS. BLAS is not called. Reproduction writes only this review's `audit_results.json`.

The shared source tree is a filesystem snapshot, not an accessible Git checkout: Git status/commit queries failed and the mounted `.git` directory contains no repository metadata. No original source files were edited, no external publication was performed, and no large physical calculation was started. Project-level status and publication are handled separately.
