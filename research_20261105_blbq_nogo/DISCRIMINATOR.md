# Discriminator test: KHH(α) ξ vs QTM reality (2026-11-05, America/Chicago)
All numbers NUMERICAL (float64, uncertified) unless marked.

## Verdict: **NO**
No α has ξ≲6 together with a real QTM spectrum (top 60). For α∈{0.6,0.7,0.8} the QTM top-60 is real but ξ≈12–17+
(> 6, still growing with χ). ξ≲6 only for α≳0.92; there (α=0.95 new; α=0.9, 1 from spin2_aklt/QTM_TEST.md) complex multiplets
are present in the top 60. The spin-1 pipeline (eq.13, real self-adjoint X) is not reusable as-is in the BLBQ window. Per instructions,
no weaker bootstrap was invented; no Z / ED L=9–10 work was started.

## (a) ξ(α): iDMRG (TeNPy 1.x, 2-site cell, no symmetry, bond h SVD-split into A_k⊗B_k), script idmrg_xi.py, logs xi_*.log
Validation: α=1 gives ξ=1.44270 = 1/ln2 (exact VBS), E=0.
| α | ξ (χ=32) | ξ (χ=64) | note |
|---|---|---|---|
| 0.6 | 13.09 | 17.46 | not χ-converged; lower bound |
| 0.7 | 11.77 | 14.99 | lower bound |
| 0.8 | 9.11 | 11.77 | lower bound |
| 0.9 | 6.15 | 7.05 | lower bound |
| 0.95 | 3.89 | 4.32 | near converged |
| 1 | 1.4427 | — | exact |
HEURISTIC: ξ≈6 crossing at α≈0.92–0.93. χ=128 runs were stopped at the 15-min cap (ξ only grows with χ, so the verdict holds).

## (b) QTM (spin2_aklt/qtm/qtm.py, ARPACK k=60, residuals ≤1.3e-9), logs qtm/N2.log, qtm/N3.log, qtm/a095.log
| α | N=2 β=2 | N=2 β=4 | N=3 β=2 | N=3 β=4 |
|---|---|---|---|---|
| 0.6 | real | real | real | real |
| 0.7 | real | real | real | real |
| 0.8 | real | real | complex pair at rank 58–59, abs r=0.029, Im 0.004 (at edge of k=60; marginal) | real |
| 0.95 | complex, rank 34, abs r=0.042, Im ±0.036 | rank 24, abs r=0.068, Im ±0.028 | rank 47, abs r=0.039, Im ±0.035 | rank 50, abs r=0.070, Im ±0.059 |
| 0.9 (prior) | dense full: complex at abs r ≤0.033 | — | β=4: 0.083±0.010i rank 28 | |
| 1 (prior) | complex rank 12, abs r≈0.05 | complex abs r≈0.09 | | rank 34, abs r≈0.10 |
The dense N=2 full spectra for α=0.6–0.8 still contain complex eigenvalues deep in the tail (max Im/λ0 = 0.0015–0.0087), below the top 60.
So "real top 60" ≠ "eq.13 holds"; eq.13 is not established at any α in (0,1] (sufficient construction fails, PROVED, spin2_aklt/SCOPING §3).

## Implication
The pivot needs either (i) a new bootstrap lemma with a rigorously bounded complex QTM tail (research debt D1, unproved), or
(ii) a different certified route near α≈0.9–1 (GM/Knabe local gap extended from CERT_*, HEURISTIC).
