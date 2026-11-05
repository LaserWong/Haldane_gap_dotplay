# T1: is bare MPS compression a non-circular route to A2 (rigorous Z upper)? Spin-1 PBC Heisenberg, L = 6, 8

**Verdict: NO.** (Small-L numbers are PROVED or FLOAT as labelled; the scale extrapolation is an ESTIMATE.)

## Setup
- **Operator.** Y ≈ E(τ) = exp(−τ(H + cL)), with c = 700741/500000. Then Z(2τ) = ‖E(τ)‖_F², and from η ≥ ‖Y − E‖_F we get **Z ∈ [(‖Y‖_F − η)², (‖Y‖_F + η)²]**.
- **Ladder.** τ_k = (49/256)·2^k for k = 0..6. k = 5 gives Z(β) and k = 6 gives Z(2β), with β = 49/4. All Z values are *shifted*, i.e. multiplied by e^(−βcL).
- **Exact reference (PROVED).** A per-Sz-block arb ladder (exact_arb.py, prec 192) cross-checks thermal_arb: Z_6(12.25) = 12.8706140506 and Z_8(12.25) = 4.6392834465.
- **η_true (PROVED, modulo the IEEE standard model as in thermal_arb float mode).** The Frobenius distance of the pipeline output to the arb ladder. It is a certified η, but it **needs the exact operator**, so it is circular at scale. It is the A3a-type reference.
- **Pipelines** (open_claims/ising_mps.py pattern):
  - Strang TEBD chunk U = (step τ0/64)^64.
  - `tebd`: 64 chunks, truncate after each.
  - `ladder`: Y0 = trunc(U), then six squarings, each followed by truncation. This is the Xiao analogue.
  - MPS layout: site-grouped (s a), local dim 9, open-chain TT-SVD on the ring.
- **A-priori η (no exact operator).**
  - ladder: δ_(k+1) = ε_(k+1) + rnd + (2·opE_k + δ_k)·δ_k
  - tebd: δ_j = ε_j + ν·δ_(j−1) + η_U·opE
  - opE_k is an upper bound on ‖E_k‖_op from an energy lower bound. Variants:
    - `exact`: oracle E0, FLOAT, circular at scale
    - `anders`: Anderson open-cluster bound with m ≤ min(L, 11), FLOAT
    - `bond`: e0 ≥ −2
    - `fro`: op ≤ Frobenius, no energy input
- **PROXY (stated plainly).** At n = 3, 4 the window lemma cannot run on any seeds, exact ones included: model.bootstrap on the exact s, t returns not-ok (FLOAT). So the criterion is the log-loss of the seeds s = B/A², t = D/B² against the log-slack the PROVED spin-1 certificate actually spent (FEASIBILITY.md):
  - Seeds: A = Z_n(β), B = Z_2n(β), D = Z_2n(2β), with n = 3 for L = 6 and n = 4 for L = 8.
  - Losses: lS = ln(B/B_lo) + 2·ln(A_hi/A) ≤ 0.033 and lT = ln(D/D_lo) + 2·ln(B_hi/B) ≤ 0.098.
  - slack = min(0.033 − lS, 0.098 − lT). slack > 0 means YES.
  - The A-side (L = 3, 4) uses the same χ. At L = 4, χ ≥ 81 is exact.

## Main table (η from `results/*.json`; Z_lo/Z_hi use η_true; slack per variant)
| mode | L | chi | eta0/|E0| | Z_lo(β) | Z_hi(β) | Z_ex(β) | Z_lo(2β) | Z_hi(2β) | Z_ex(2β) | slack true | slack exact-E0 | slack Anderson | slack bond | slack fro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ladder | 6 | 8 | 0.0842 | 0 | 12.9 | 12.9 | 0 | 166 | 166 | -inf | -inf | -inf | -inf | -inf |
| tebd | 6 | 8 | 0.0842 | 0 | 13.3 | 12.9 | 0 | 167 | 166 | -inf | -inf | -inf | -inf | n/a |
| ladder | 6 | 16 | 0.0277 | 0 | 13.8 | 12.9 | 0 | 169 | 166 | -inf | -inf | -inf | -inf | -inf |
| tebd | 6 | 16 | 0.0277 | 0 | 13.9 | 12.9 | 0 | 168 | 166 | -inf | -inf | -inf | -inf | n/a |
| ladder | 6 | 32 | 0.00669 | 0 | 14.1 | 12.9 | 0 | 171 | 166 | -inf | -inf | -inf | -inf | -inf |
| tebd | 6 | 32 | 0.00669 | 0.749 | 15.4 | 12.9 | 0 | 199 | 166 | -inf | -inf | -inf | -inf | n/a |
| ladder | 6 | 64 | 0.000485 | 5.95 | 13.9 | 12.9 | 33.1 | 173 | 166 | -1.66 | -inf | -inf | -inf | -inf |
| tebd | 6 | 64 | 0.000485 | 6.74 | 16.8 | 12.9 | 80 | 218 | 166 | -1.16 | -inf | -inf | -inf | n/a |
| ladder | 6 | 128 | 5.42e-05 | 11.2 | 13.6 | 12.9 | 133 | 172 | 166 | -0.221 | -7.66 | -inf | -inf | -inf |
| tebd | 6 | 128 | 5.42e-05 | 10.5 | 14.5 | 12.9 | 123 | 198 | 166 | -0.443 | -5.11 | -inf | -inf | n/a |
| ladder | 6 | inf | 1.01e-06 | 12.9 | 12.9 | 12.9 | 166 | 166 | 166 | 0.033 | 0.0324 | 0.0317 | 0.0267 | 0.0119 |
| tebd | 6 | inf | 1.01e-06 | 12.9 | 12.9 | 12.9 | 166 | 166 | 166 | 0.033 | 0.0324 | -0.841 | -inf | n/a |
| ladder | 8 | 16 | 0.0342 | 0 | 4.91 | 4.64 | 0 | 21.6 | 21.4 | -inf | -inf | -inf | -inf | -inf |
| ladder | 8 | 32 | 0.00863 | 0 | 5.08 | 4.64 | 0 | 22 | 21.4 | -inf | -inf | -inf | -inf | -inf |
| ladder | 8 | 64 | 0.000695 | 0.728 | 5.19 | 4.64 | 0.00453 | 22.7 | 21.4 | -8.59 | -inf | -inf | -inf | -inf |
| ladder | 8 | 128 | 8.77e-05 | 2.96 | 5.09 | 4.64 | 9.64 | 22.7 | 21.4 | -0.885 | -inf | -inf | -inf | -inf |
| ladder | 8 | 256 | 6.47e-06 | 4.2 | 4.92 | 4.64 | 18.8 | 22.5 | 21.4 | -0.146 | -2.35 | -3.57 | -inf | -inf |
| ladder | 8 | 512 | 1.18e-06 | 4.55 | 4.71 | 4.64 | 21 | 21.8 | 21.4 | 0.0135 | -0.344 | -0.447 | -0.842 | -1.61 |
| ladder | 8 | 1024 | 1.12e-06 | 4.62 | 4.66 | 4.64 | 21.3 | 21.5 | 21.4 | 0.0286 | 0.00909 | -0.00867 | -0.141 | -0.739 |
| ladder | 8 | inf | 1.12e-06 | 4.64 | 4.64 | 4.64 | 21.4 | 21.4 | 21.4 | 0.0329 | 0.0316 | 0.031 | -0.0173 | -0.596 |

(chi = inf means no truncation, so only Trotter error remains, ≈1.1e-6 relative. The Z_hi/Z_exact ratio alone is misleading: Y → 0 gives η → ‖E‖ and Z_hi → Z exactly. Only the two-sided loss is meaningful.)

## Findings
1. **The bond dimension a certified-close purification needs is close to full at these sizes** (`spectrum.py`; FLOAT on PROVED-close exact E). Here is the minimal χ at the middle cut for a one-shot relative Frobenius tail ≤ 1e-2 / 1e-3:

   | | high T (k = 0) | β (k = 5) | 2β (k = 6) |
   |---|---|---|---|
   | L = 6 | 24 / 59 | 271 / 526 (max 729) | 271 / 527 (max 729) |
   | L = 8 | 24 / 59 | 455 / 1336 (max 6561) | 456 / 1337 (max 6561) |

   At low T, E ≈ e^(−τE0)|ψ0⟩⟨ψ0| + magnons. On a ring each open cut is two cuts, so χ_Y ≈ χ_ψ² with χ_ψ ≈ χ_OBC². Truncation is then applied after every step, and the errors compound.
2. **Even with the oracle η_true (circular), modest χ fails** (PROVED numbers, PROXY verdict):
   - L = 6: NO for every χ ≤ 128. At χ = 128 the slack is −0.22 (ladder) and −0.44 (TEBD).
   - L = 8: NO for χ ≤ 256 (χ = 256 gives −0.146). It turns YES only at χ = 512 (+0.0135) and χ = 1024 (+0.029), i.e. 8–16% of the full middle-cut rank at L = 8.
   - The relative error at 2β is 0.94% for χ = 512 and 0.22% for χ = 1024, against first-step errors of only 1e-6. Truncation error grows by about 10³–10⁴ through the ladder.
3. **The non-circular a-priori η is far worse** (FLOAT):
   - L = 8, χ = 512: exact-E0 −0.34, Anderson −0.45, bond −0.84, fro −1.61, all NO.
   - L = 8, χ = 1024: only the oracle-E0 variant passes (+0.009). Anderson gives −0.009, so NO.
   - No truncation, L = 8: exact +0.032 and Anderson +0.031 (YES); bond −0.017 and fro −0.60 (NO). For L = 8, a scheme with no compression at all only works because the energy input is near-exact.
4. **Squaring-amplification probe (Xiao L = 256 analogue)** (`tolerance.py`, `T1_tolerance.json`). The model gives every step a relative loss r, run through the a-priori recursion using exact norms. It reports the largest r that keeps the proxy alive and the amplification Π_k ρ_k, where ρ_k = 2·opE_k·‖E_k‖_F / ‖E_(k+1)‖_F:

   | 2n | exact-E0 r_max | log10 Πρ | Anderson | bond | fro |
   |---|---|---|---|---|---|
   | 6 (FLOAT) | 2.6e-5 | 2.65 | 9.0e-6 | 3.1e-6 | 1.2e-6 |
   | 8 (FLOAT) | 1.9e-5 | 2.95 | 1.4e-5 | 8.9e-7 | 1.7e-7 |
   | 256 (ESTIMATE) | **1.4e-40** | **38.3** | 2.5e-47 (m = 11); 1e-40 even at m = 1000 | 0 (Πρ ~ 1e85) | 0 (Πρ ~ 1e109) |

   At L = 8 the a-priori (oracle) δ at 2β is 36× the true error for χ = ∞: 9.9e-4 vs 2.7e-5 relative.
   At L = 256 the per-step log10 ρ are 15.0, 13.0, 6.4, 2.8, 0.8, 0.3, so the **high-T squarings dominate**.
   A Xiao-type first-step loss of 1e-12 misses the bound by about 28 decades **even with the exact ground-state energy** (ESTIMATE).

## Mechanism
The a-priori error recursion has to bound ‖YΔ + ΔE‖_F by ‖Y‖_op·‖Δ‖_F. Relative to the next rung, the step costs ρ_k = 2‖E_k‖_op·‖E_k‖_F / ‖E_k²‖_F. At high temperature this ratio is exponential in L: ln ρ_k ≈ ln 2 + Lτ_k[2f(4τ_k) − f(2τ_k) − e0]. The op norm sits at the bottom of the spectrum, while the Frobenius mass sits in the broad bulk. A relative error of r therefore has to be assumed fully aligned with the top eigenvector and gets inflated by e^(Θ(L)) at every high-T rung. At L = 256 that is a factor of about 1e38 with the exact E0, worse with any non-circular energy bound (Anderson adds e^(βLΔe)), and hopeless with bond or Frobenius norms (1e85–1e109).

Separately, the low-T purification of a periodic ring has an intrinsically large bond: χ_Y ~ χ_ψ² with χ_ψ ~ χ_OBC². At L = 6, 8, χ ≈ 270–460 is needed just for a single 1% truncation, and repeated truncation compounds it. Even the circular true η needs χ ≥ 512 at L = 8.

So the only certified route that works is comparison to the exact operator (A3a, circular), or a near-exact ground-state energy lower bound. Either way A2 is not removed, only renamed: compress-then-square certification reduces A2 to an E0 lower bound accurate to O(1/(βL)) per site, plus an e^(Θ(L)) high-T loss that no energy bound fixes. **Bare MPS compression is not a non-circular A2 path.**

## Labels and caveats
- **PROVED:** Z_exact; η_true; the Z_lo/Z_hi columns (subject to the IEEE standard model for the float Frobenius norm, as in thermal_arb float mode).
- **FLOAT:**
  - Anderson E0 bounds and ring E0 (float ED)
  - the a-priori recursions (float arithmetic on the bound)
  - the spectra
  - bootstrap-not-ok at n = 3, 4
- **PROXY:** every YES/NO verdict, judged against the spent log-slack 0.033 / 0.098 at n = 34. These small-L seeds do not close a bootstrap themselves.
- **ESTIMATE:** the L = 256 tolerance. It borrows the L = 8 per-site excitation free energy with e0∞ = −1.401484.
- **Not explored:** PBC-MPS/MPO formats, symmetric (U(1)/SU(2)) blocking, and non-triangle (a-posteriori) error bounds. The ρ_k mechanism applies to *any* a-priori Frobenius propagation through squaring, so a better format changes item 1 but not item 4.
- **TEBD at L = 8** was stopped after 4 chunks: about 2.5 h per run. At χ = 128 its true η was already 1.8% at τ = 0.77. The L = 8 table is ladder-only; partial logs are in results/partial/.
- No spin-2 claim is made.

## Artifacts (runs/fuzzy_mps/)
- Scripts: common.py, exact_arb.py, pipeline.py, anderson.py, run_t1.py, summarize.py, spectrum.py, tolerance.py, make_results.py
- Results: results/*.json|log, results/spectrum_L{6,8}.json, cache/, T1_proxy.json, T1_tolerance.json, **T1_results.json**
