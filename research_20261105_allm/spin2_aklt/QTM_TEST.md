# QTM-reality test for KHH(α) — all results NUMERICAL

Question: are the leading eigenvalues of the quantum transfer matrix (QTM) of
H = Σ h_α (spin-2, KHH family; R35 = P3 + 35/9·P4) real, or do they come in complex pairs?
(If X in eq.13 is real self-adjoint, *every* eigenvalue must be real.)

## Method
* R = SWAP·exp(−ε h), ε = β/(2N); column QTM Q of dim 5^{2N}, with Tr Q^L = Z_N(L) := Tr(T_R T_R^T)^N **exactly**
  (Trotter–Suzuki checkerboard; Z_N → Z = Tr e^{−βH} as N→∞).
* Matrix-free MPO matvec + ARPACK (scipy eigs, LM). N=2 also checked against the full dense spectrum.
  Script: `qtm/qtm.py`; raw: `qtm/qtm_results.jsonl`; table: `qtm/summary_table.txt`.
* Validation (`qtm/log_validate_b1.txt`, β=1): Tr Q^L = Z_N(L) to 1e-16 (identity check);
  Trotter error vs exact Z at L=3/4: KHH(1) 36%/17% (N=1) → 6.8%/4.6% (N=2); R35 3.0%/1.5% (N=2);
  KHH(0) 202%/7.7% (N=2, large bond spread). Ratios λ_k/λ_0 converge much faster than Z (see below).
* All ARPACK relative residuals ≤ 1e-11.

## Results (λ_k/λ_0; full data in summary_table.txt)
Leading structure, all models/β: λ_0 > 0 real (non-degenerate), then a REAL negative triplet
(−0.47…−0.85), then a REAL positive quintet, then real multiplets. **The top ≥ 12 eigenvalues are real in every run.**

Complex multiplets (conjugate pairs of SU(2) multiplets) found in the subleading spectrum:

| model | β | N=2 | N=3 | N=4 |
|---|---|---|---|---|
| KHH(1) | 2 | 0.021±0.047i (rank 12) | −0.0115±0.0557i (rank 31, ×10) | −0.0080±0.0624i (rank 25) |
| KHH(1) | 4 | −0.0417±0.0751i (rank 12, ×10) | −0.0374±0.0959i (rank 34 of k=60 / 22 of k=24, ×10) | −0.0359±0.0993i (rank 23) |
| KHH(1) | 8 | −0.0720±0.1004i (rank 19) | −0.0728±0.1337i (rank 18, ×10) | −0.1666±0.0080i (rank 17, ×10; k=30 reaches only |r|≥0.165, so the N=3 multiplet at |r|=0.152 is not resolved) — β=8 NOT Trotter-converged |
| R35 | 2 | −0.0113±0.0338i (rank 9) | −0.0103±0.0457i (rank 21, ×10) | – |
| R35 | 4 | −0.0246±0.0572i (rank 12) | −0.0177±0.0792i (rank 24, ×10) | −0.0148±0.0886i (rank 21) |
| R35 | 8 | −0.0581±0.0905i (rank 14) | −0.0561±0.1178i (rank 18, ×10) | – |
| KHH(0.9) | 4 | (dense: first complex rank 31, |r|=0.048) | 0.0828±0.0098i (rank 28) | – |
| KHH(0.9) | 1,2,8 | dense N=2 has complex at |r|≤0.033 | none in top 60 | β=2: none in top 24 |
| KHH(0.5), KHH(0) control | 1–8 | none in top 24 (dense N=2: KHH(0) max |Im|/λ0 ≤ 7e-5, |r|~2e-4 deep tail) | none in top 60 | – |

Trotter convergence (KHH(1), β=4, the cleanest series): Im = 0.0751, 0.0959, 0.0993 for N=2,3,4
(increments 0.021, 0.0034 — converging, not shrinking toward 0); a/N² fit gives Im∞ ≈ 0.10, Re∞ ≈ −0.035.
Same pattern for KHH(1) β=2 (0.047→0.056→0.062) and R35 β=4 (0.057→0.079→0.089, Im∞≈0.10). At β=8 (ε=1 at N=4) the deep spectrum is not converged. Real leading ratios move by ≲1% from N=3 to N=4
(e.g. KHH(1) β=4 second ratio −0.6281 → −0.6347).

## Verdict (NUMERICAL)
1. Leading QTM eigenvalues (top ~12: λ_0, the triplet, the quintet…) are **real** for all α∈{0,0.5,0.9,1} and R35, β∈{1,2,4,8}.
   No complex *leading* pair. Negative real eigenvalues are generic (−0.5…−0.85 triplet).
2. **But genuine complex-conjugate multiplets exist in the subleading spectrum** for α near the AKLT point
   (KHH(1), R35, and KHH(0.9) at β=4), at |λ/λ_0| ≈ 0.05–0.15, and they are **stable/strengthening under Trotter refinement**
   N=2→3→4 — not a Trotter artifact at the level testable here. They are absent (to |r|≳0.03–0.1) for α≤0.5 and Heisenberg.
3. Consequence: a model "Z_L = Tr X^L with X real self-adjoint (finite-dim)" is **numerically contradicted for KHH(1)/R35 at finite β**
   if it must reproduce the full QTM spectrum; it is consistent only for the top-12 (leading) part, i.e. up to corrections
   ~|0.1|^L in Z_L. HEURISTIC: for bootstrap at large L this is exponentially small; at small L it is not.

## Limitations
* Bootstrap-relevant β (βΔ ≳ 5, β ~ 25 for KHH(1)) is NOT reached: β ≤ 8, N ≤ 4 (ε = β/2N ≤ 1). N=4 at β=8 is at the CPU cap.
* k ≤ 60 (N=3), ≤ 30 (N=4): deeper spectrum unseen; a count of "none" means none within the computed top-k.
* Trotter error in Z is several % at N=2; convergence claims are from 3 points (N=2,3,4) — NUMERICAL, not PROVED.
* Q is the specific checkerboard QTM; its N→∞ limit is the physical QTM; finite-N spectra are not decomposition-invariant.
