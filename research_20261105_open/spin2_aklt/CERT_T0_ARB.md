# CERT_T0_ARB: residual / approximate-inverse recheck of ε₈ > 6261/50000

Date: 2026-11-04. Scripts and logs: `runs/spin2_aklt/cert_t0/cert_arb_block.py`, `runs/spin2_aklt/cert_t0/arb/`.

## 0. Result

**VERIFIED.** The same intermediate claim as in `CERT_T0.md`,

\[
ε_8 > 6261/50000 = 0.12522,
\]

is re-certified on all four Sz = 0 symmetry blocks by an independent method that **does not use** the Higham / Rump a-priori rounding model of LAPACK `dpotrf`. Consequently Theorem T0 of `CERT_T0.md` (gap ≥ 6283/150000 on periodic chains of length ≥ 17, and the KHH(1) corollary) stands with the updated trusted base of §4.

| block (r,f) | dim | k_b | ρ (residual 2-norm bound) | ‖R⁻¹‖₂ bound | λ_min(RᵀR) lower | λ_min(A*+U) lower | CERT |
|---|---|---|---|---|---|---|---|
| (+,+) | 9719 | 2 | 2.23e-10 | 196.17 | 2.60e-5 | **2.80e-5** | yes |
| (+,−) | 9406 | 0 | 1.68e-10 | 26.87 | 1.38e-3 | **1.39e-3** | yes |
| (−,+) | 9364 | 0 | 1.52e-10 | 16.24 | 3.79e-3 | **3.79e-3** | yes |
| (−,−) | 9676 | 1 | 2.22e-10 | 1158.06 | 7.46e-7 | **2.75e-6** | yes |

Tightest block (−,−): margin 2.75e-6 above 0. Runtime ≈ 24–34 s/block with `OPENBLAS_NUM_THREADS=4`.

## 1. Method (residual witness, not a Cholesky error model)

For each block the float matrix Ab ≈ A* + U is built exactly as in `cert_block.py` (same `E_build` bound). Set Ac = Ab − cI with c = 2e-6. Let R be the upper-triangular array returned by `dpotrf(Ac)` (discovery only). From this point R is treated as an **arbitrary dyadic matrix we chose**; no property of how `dpotrf` computed it is used.

1. **Residual.** Compute fl(RᵀR) by an explicit GEMM. With Higham’s classical model for that GEMM,
   \[
   \|RᵀR - Ac\|_2 ≤ \|fl(RᵀR)-Ac\|_2 + γ_{d_b}\,\||R|ᵀ|R|\|_2 =: ρ.
   \]
   The two 2-norms are bounded by √(‖·‖₁‖·‖_∞) with a (1+γ_d) inflation on the nonnegative row/column sums.
2. **Approximate inverse.** Let X be the dyadic array returned by `dtrtri(R)` (again only a witness). Compute F = I − RX with an explicit GEMM and the same γ-radius. If ‖F‖₂ < 1 then
   \[
   \|R^{-1}\|_2 ≤ \frac{\|X\|_2}{1-\|F\|_2},
   \]
   and ‖X‖₂, ‖F‖₂ are bounded by the 1/∞ formula as above.
3. **Weyl.** λ_min(RᵀR) ≥ 1/‖R⁻¹‖₂², and
   \[
   \|RᵀR - (M - cI)\|_2 ≤ ρ + E_{\mathrm{build}} + δ_{\mathrm{shift}},
   \]
   where M = A* + U is the exact block matrix (rational PHP − tΛ plus the dyadic WWᵀ). Hence
   \[
   λ_{\min}(M) ≥ c + \frac1{\|R^{-1}\|_2^2} - ρ - E_{\mathrm{build}} - δ_{\mathrm{shift}}.
   \]
4. **Logic unchanged from CERT_T0.** If λ_min(A*+U) > 0 with the recorded k_b, then the block has at most k_b eigenvalues ≤ t. Summing k_b = 2+0+0+1 = 3 and using the exact 3-dimensional Sz=0 kernel gives ε₈ > t.

## 2. Negative controls

| case | result |
|---|---|
| n=8, t = 1253/10000 = 0.1253 > ε₈ | block (−,−) `dpotrf` fails (`info=9676`); global certificate **rejected**. The other three blocks still certify (the first excited multiplet sits in (−,−)), which is consistent. |
| n=6, t = 135/1000 > ε₆ | blocks (+,+) and (−,−) fail discovery Cholesky; rejected. |
| n=6, t = 134/1000 < ε₆ | (+,+) and (−,−) certify (λ_min lowers 8.0e-5 and 1.36e-4). |

So the verifier is not vacuous: it refuses the known-false thresholds.

## 3. What this removes, and what remains

| item | status after this recheck |
|---|---|
| Higham Thm 10.3 applied to `dpotrf` | **removed** (was C2/C3 load-bearing for the Cholesky step) |
| Rump 2006 Thm 2.3 applied to `dpotrf` | **removed** |
| IEEE-754 for the *explicit* GEMMs / abs-sums we invoke (`RᵀR`, `|R|ᵀ|R|`, `RX`, `|R||X|`, row/column sums), classical (non-Strassen) evaluation, round-to-nearest | **still assumed** (documented; OpenBLAS blocked GEMM at these sizes) |
| `E_build` construction bound for Ab vs M (bond rounding, sparse triple product, rank-k update) | **unchanged** from CERT_T0 §3 |
| Exact kernel dim = 9, bond projector / SU(2) / GM hypotheses | **unchanged** (exact arithmetic / paper check) |

## 4. Updated trusted base (replaces CERT_T0 §5 C2 for the positivity step)

To accept ε₈ > 6261/50000 via this file it is enough to trust:

1. IEEE-754 binary64, round-to-nearest, no mid-evaluation exception, for the **explicit** dense products and reductions listed in §1 (classical summation / GEMM; Higham γ_k bounds).
2. The exact-arithmetic facts of CERT_T0 §§1–2 (projector bond, dim ker = 9, SU(2) reduction, symmetry splitting).
3. The `E_build` derivation in CERT_T0 §3 (same scripted constants; still an IEEE model for the *construction* of Ab, not for Cholesky).
4. Python / NumPy / SciPy / OpenBLAS as the vehicle that materialises the dyadic witnesses R, X and the float matrix Ac; their internal `dpotrf`/`dtrtri` algorithms are **not** part of the proof, only the output arrays are.

No a-priori LAPACK Cholesky rounding theorem is required.

## 5. Files

- `cert_t0/cert_arb_block.py` — verifier.
- `cert_t0/arb/cert_arb_n8_r±1_f±1_t6261_50000.json` — four positive certificates.
- `cert_t0/arb/cert_arb_n8_r±1_f±1_t1253_10000.json` — negative control (fails in (−,−)).
- `cert_t0/arb/cert_arb_n6_*.json` — n=6 smoke / negctl.
- `cert_t0/arb/log_arb_n8.txt` — full run log.
- No Cholesky factors were retained (each is ~750 MB); they are recomputable in < 1 min/block.

## 6. Relation to Theorem T0

Unchanged numerical claim: ε₈ > 6261/50000 ⇒ for every periodic m ≥ 17,
gap(H°_m) ≥ 6283/150000, and gap(KHH(1)_m) ≥ 6283/105000.
Only the machine-arithmetic justification of ε₈ > 6261/50000 has been strengthened.
