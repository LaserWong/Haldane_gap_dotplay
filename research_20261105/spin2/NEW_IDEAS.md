# Spin-2: new ideas for the missing upper-bound piece (screened on spin-1)

2026-11-04 (America/Chicago). Theory plus cheap arithmetic only. No long jobs; total CPU < 5 s.
Status labels: PROVED (argued here in full), EXTERNAL-VERIFIED (published result, checked), PROVISIONAL (argument sketched, gaps named), TESTED (float or estimate; NOT rigorous), DISPROVED, BLOCKED.
Notation: Z_L(β) = Tr X^L, where X = X_β is real symmetric Hilbert–Schmidt (transfer_operator.md), λ0 = ‖X‖, and r_i = λ_i/λ0. The repo splits X into twist sectors J = (Z+3P)/4 (multiplicity 1) and N = (Z−P)/4 (multiplicity 3).

## 0. Bottom line
- **No direction removes the need for rigorous upper data at length ≈ 1.3ξ–2ξ.** For spin-2 that means L ≈ 65–100. The best reformulation (§B2) reduces the requirement as follows:
  - Before (FEASIBILITY): Z_256, Z_512 to ≈1.5e-6 per site.
  - After: sector-resolved upper bounds on Z_m and P_m at m ≈ 65–100, β ≈ 50–60, with absolute ln-error ≈ 0.03–0.1, i.e. ≈ 5e-6–2e-5 per site.
  - The gain is about 3–10× in precision and 3–5× in length.
  - It is still far beyond any rigorous method we have: ED stops at L ≤ 8–10, and ring relaxations need W ≈ L (LEAD2).
- **New rigorous-in-principle obstruction (§B1; final status in MOMENT_NOGO.md: one-sided version PROVED, two-sided version DISPROVED, spin-1 dataset-level no-go for M ≤ 8 PROVED).** Take any certificate built only from upper bounds on sector moments Z_k, P_k for k ≤ m plus lower bounds at large L. It can give S(n) near 1 only if the true residual ratio ρ_m = Σ_{i≥1} r_i^m in each competing sector is < 1.
  - For spin-2 at m ≤ 8 and β ≳ 20: ln ρ_8 ≳ 8.6 (β=20) to 24 (β=56), TESTED. So exact small-L data can never seed a spin-2 proof by any filter, packing, Hankel or convexity trick.

## A. Reflection positivity / log-convexity / chessboard
- **A1 (PROVED).** X is self-adjoint, so ln Z_L is convex in even L. Then Z_n ≤ Z_m^θ Z_2n^{1−θ} with θ = n/(2n−m).
  - Consequence: S = Z_2n/Z_n² ≥ (Z_2n^m / Z_m^{2n})^{1/(2n−m)}.
  - This needs only Z_2n LOWER (variational) and Z_m UPPER (small L).
- **Loss.** ln S ≥ −imp_m·2n/(2n−m) − (variational loss), with imp_m = ln(Z_m/λ0^m) ≥ 0.
- **Spin-1 screen (TESTED).** imp_12 ≈ 0.635 (rigorous ln Z_12 ≤ 0.642; ln λ0 ≈ 6e-4/site). This gives S(34) ≳ e^{−0.77} ≈ 0.46, but the proof needs ≥ 0.946. **Fails.** It works only if imp_m ≲ 0.05, i.e. m ≳ 5ξ.
- **β-direction analogue.** T ≥ Z(2β)^{…}/Z(β1)^{…} loses the thermal impurity at β1, so it needs β1Δ ≳ ln(2n), and the upper data again sit at large L.
- **Time-direction RP/chessboard.** On the classical/Trotter side this reduces to the ring-ceiling Lüscher loss (LEAD2).
- **Spin-2 cost.** imp_8 ≈ 24–28 at β ≈ 56. Useless.
- **Verdict: DROP.** Convexity moves the upper-bound requirement to a smaller L but charges the full impurity there. Packing (B2) is strictly better.

## B. Reformulations that avoid large-L upper bounds
### B1. What any moment certificate can and cannot do
- S depends only on the r_i, because λ0 cancels, so S is not extensive. But adding an atom raises every Z_k, so an upper bound on Z at *some* size is unavoidable.
- **Adversary (PROVISIONAL).** Start from the true spectrum and remove atoms i ≥ 1 with Σ r_i^m ≥ 1. Then (r_i/1)^k ≥ r_i^m for k ≤ m, so all moments k ≤ m decrease. Add one atom at λ0' ≈ λ0.
  - All upper bounds at k ≤ m still hold.
  - Large-L lower bounds still hold (they only rise).
  - The adversary has two near-top atoms, so S ≈ 1/2.
  - Hence **ρ_m < 1 (roughly) is necessary**. **[SUPERSEDED 2026-11-04: see MOMENT_NOGO.md. This holds (PROVED) for one-sided data with ρ^+ (Thm 1). It is DISPROVED as a general necessary condition for two-sided data (Prop 2). The dataset-level spin-1 no-go is PROVED for M ≤ 8 by exact fakes (Thm 3).]**
  - Gap to PROVED: odd/signed moments and the twist-sector bookkeeping. The same argument works per sector, with sign-matched atoms.
  - With exact two-sided moments, one can re-add small atoms to fix the lower k. I expect the same threshold but have not proved it.
- **Sufficiency (PROVED in the repo; uniform_smaller_second_initialization).** Integer multiplicities plus mass packing give
  - R_n ≤ (J_m^up − ℓ^m)^{n/m} + 3·N_n^up, and S(n) ≥ (1 + R_n/ℓ^n)^{−2},
  - where ℓ < λ0 comes from a variational anchor at 2n.
  - So ρ_m < 1 is amplified to ρ_m^{n/m}. This is far stronger than convexity.
- **Spin-1 calibration (TESTED arithmetic on rigorous intervals, moment_optimization/certificate.json, ℓ = 0.9999979746):**

  | m | 6 | 8 | 10 | 12 |
  |---|---|---|---|---|
  | ρ_J(m) | 2.43 | 0.54 | 0.17 | 0.066 |

  - At n = 32, (0.066)^{8/3} ≈ 7e-4 is negligible. S is limited by 3·N_32 ≈ 0.036 (the N-sector cap −0.871 vs λ0 ≈ 1), giving S ≥ 0.930.
  - T is limited by the λ0 cap: J+ cap 1.0013390, ln(cap/ℓ) = 1.34e-3, ×64 → Q_64 = 1.089, T ≥ 0.842.
  - So the spin-1 proof sits at m/ξ ≈ 2.0, and the ρ_J < 1 threshold is already met at m/ξ ≈ 1.3.

### B2. Most promising: universality-rescaled moment + cooling route (Appendix A)
- **Inputs:**
  - (i) Sector upper bounds J_m, N_m at m ≈ 1.3ξ–2ξ.
  - (ii) Polynomial or square-filter caps on λ0 and |λ_N| from those moments.
  - (iii) Variational MPS anchors at 2n (lower bounds; easy).
  - (iv) T via cooling: (q−1)^r with q = Z_2n(β0)^up. This tolerates q − 1 < 1, i.e. 2n·ln(cap/λ0) ≲ 0.5, versus ≈ 0.09 without cooling.
- **Spin-2 scaling (TESTED, using universality in m/ξ and βΔ; ξ = 49.5, Δ = 0.089):**
  - m ≈ 65–100, n ≈ 260, β0 ≈ 55.
  - Required absolute ln-precision on sector moments: ≈ 0.03 (without cooling) to ≈ 0.1 (with cooling). That is **≈ 5e-6–2e-5 per site** at m = 100, β = 55.
  - Anchors need ln(λ0/ℓ) ≲ 0.03/m, i.e. a trial energy within ≈ 5e-6/site (DMRG-easy).
- **What is still missing (BLOCKED):** rigorous lower bounds on the free energy of a finite spin-2 ring (twisted and untwisted), at L ≈ 65–100, good to ≈ 1e-5/site.
  - Rigorous ED: 5^65 states. Impossible.
  - Ring relaxations: by the LEAD2 ring ceiling they need W ≈ L. Impossible.
  - Trotter/ALT gives a rigorous upper bound on Z, but evaluating it is a 2D sign-free classical contraction of size L × (2β/τ). Its rigorous evaluation hits the same wall; CW was lead 1 and FAILED.
- **Verdict:** best available reformulation, but it **does not close**. Spin-2 cost is about 10× below FEASIBILITY's 1.5e-6, still beyond reach.

### B3. Superadditivity / ratio form
- ln S ≥ −β[E_tr(2n) − 2E_lo(n)] − 2 ln Q_up.
- This needs 2E0(n) − E0(2n) certified to ≈ 0.03/β ≈ 5e-4 total at n ≈ 260. That is the Lüscher defect, i.e. certifying ξ itself.
- **Verdict: DROP.** Equivalent to the target.

### B4. Twists / Rayleigh quotients / sector ratios
- P/Z and other ratios cancel λ0, but a lower bound on a ratio still needs an upper bound on its denominator.
- Sector splitting gives at best the two-magnon decay e^{−2m/ξ} in J. That roughly halves m, and is already used in B2.
- **Verdict: absorbed into B2.**

### B5. Entropy-density form of T
- PROVED: 2β(f(β) − f(2β)) ≥ −s_max on [β, 2β], from df/dβ = s/β².
- So T needs only an upper bound s ≲ 0.5/(2n) ≈ 1e-3 on the thermal entropy density. This is a non-extensive target, with true s ≈ 2e-4 at β = 64.
- But a relaxation upper bound on s at energy u ≈ e0 + 3e-6 is spoiled by fake low-energy ring states (Lüscher deficit ε_W must be ≲ 3e-6), so W ≈ 200.
- **Verdict: DROP** (same wall). Recorded because the reduction itself is new.

## C. Knabe / Gosset–Mozgunov / Lemm–Mozgunov (EXTERNAL-VERIFIED)
- Thresholds:
  - Knabe: gap_n > 1/(n−1).
  - Gosset–Mozgunov (JMP 57, 091901): 6/(n(n+1)).
  - Lemm–Mozgunov (open BC; JMP 60, 051901): ~26 n^{−3/2}.
- All require **frustration-free** H. Gosset–Mozgunov note that the 1/n² threshold is specific to the frustration-free case, because frustrated gapless chains have Θ(1/n) gaps.
- Any frustrated analogue would need a threshold ≥ the critical-chain finite-size gap ~ v/n. Below L ~ ξ the spin-2 Heisenberg chain is indistinguishable from critical, so it needs n ≳ few·ξ again.
- The 1D gap is undecidable in general (Bausch–Cubitt–Lucia–Pérez-García, PRX 10, 031038).
- **Verdict: INAPPLICABLE.**

## D. Other
- **AKLT deformation / perturbative stability.** Heisenberg S=2 is far from the S=2 AKLT point; the bounds are not quantitative at O(1) distance. DROP.
  - Side note: a spin-2 bilinear–biquadratic model with ξ ≲ 5 would fit the existing machinery, with ED at L ≤ 8–10 ≈ 2ξ. That would prove *a* spin-2 Haldane gap, not Heisenberg. It is a possible pivot; the owner decides.
- **Martingale/FNW.** Needs an exact MPS ground state. DROP.
- **Birkhoff/Doeblin on the Marshall-positive kernel.** Infinite projective diameter for continuous-time histories; constants e^{O(β)}. Related to the failed CW lead. DROP.
- **Comparison no-go (TESTED heuristic).** The bootstrap is model-independent. For n ≪ ξ the spin-2 data match a critical chain, so no certificate can seed there. This is consistent with B1.

## Proof-debt ledger
| item | status |
|---|---|
| A1 log-convex interpolation S ≥ (Z_2n^m/Z_m^{2n})^{1/(2n−m)} | PROVED |
| B1 sufficiency (packing, ρ^{n/m}) | PROVED (repo, spin-1) |
| B1 necessity, one-sided data (Thm 1) | PROVED, see MOMENT_NOGO.md |
| B1 necessity as stated for two-sided data | DISPROVED (MOMENT_NOGO Prop 2) |
| Spin-1 D_6/D_7/D_8 cannot seed S(32)>1/√2 | PROVED, exact fakes (MOMENT_NOGO Thm 3) |
| B5 entropy reduction of T | PROVED |
| spin-1 ρ_J table, spin-2 ln ρ_8 ≥ 8.6–24 | TESTED |
| B2 spin-2 requirements (m 65–100, 5e-6–2e-5/site) | TESTED (universality estimate) |
| rigorous finite-ring spin-2 free-energy lower bound, L≈65–100, ~1e-5/site | **BLOCKED** |
| C criteria require frustration-freeness | EXTERNAL-VERIFIED |
