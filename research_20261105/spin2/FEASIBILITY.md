# Spin-2 Haldane-gap bootstrap — Phase 1 feasibility (scoping only)

Status: **no proof route closes with current tools.** The lower-bound side looks feasible. The rigorous **upper bounds on Z_L at L≈250–600 with ~1e-6 per-site free-energy accuracy** are the blocker.
No long runs were launched. Unless a line says *rigorous*, every number below is an **ESTIMATE**: it comes from the free 3-magnon + Lüscher model (`model.py`) or from float ED/Trotter.

Inputs (literature, spin-2): e0 = −4.761248, Δ = 0.08917(4), ξ = 49.49(1) (Todo–Kato 2001); also Δ = 0.0876(13) (Wang–Qin–Yu 1999) and Δ = 0.085(5), ξ = 49(1) (Schollwöck et al. 1996); v = Δξ ≈ 4.41.
Spin-1 calibration: e0 = −1.401484, Δ = 0.41048, ξ = 6.0153, β0 = 49/4.

## 0. What the bootstrap consumes
- S = Z_2n(β)/Z_n(β)² (spatial purity), T = Z_2n(2β)/Z_2n(β)² (thermal purity).
- Recursion: S' = G(S²T), T' = G(T²S'). Window lemma gives C; then gap ≥ ln(C/(1−C))/β. Tail: u ≤ 0.01 ⇒ u' ≤ 5u².
- Rigorous **lower** bounds are needed on Z_2n(β) and Z_2n(2β). These are variational, i.e. easy in principle.
- Rigorous **upper** bounds are needed on Z_n(β) (it enters S squared) and on Z_2n(β) (it enters T squared). This is the hard side.
- Physics: 1−S ≈ 2Σ(λ_i/λ_0)^n requires n ≫ ξ, and 1−T requires βΔ ≫ 1. When L ≲ ξ, conformal field theory makes S and T functions of n/(vβ) alone, so the two cannot both be near 1. This is consistent with Lily's n=8 obstruction.

## 1. Required (n, β, accuracy) — ESTIMATES (`scan.py`, `tables.py`, `scan.json`, `tables.json`)
"Max slack" η is the largest uniform log-loss on both S and T for which the bootstrap still closes.

**Spin-2 scan.**

| n | β | max slack η |
|---|---|---|
| ≤150 | any | fails |
| 200 | 60 | 0.049 |
| 250 | 60 | 0.088 |
| 250 | 80 | 0.106 |
| 300 | 60 | 0.096 |
| 300 | 80 | 0.123 |
| 400 | 80 | 0.129 |

**Recommended start windows.**

| n | β | S | T | max η | gap cert. (at η/2) | windows | Z values needed |
|---|---|---|---|---|---|---|---|
| 256 | 64 | 0.9612 | 0.9640 | 0.098 | ≥0.0153 | 7 | Z_256(64)↑, Z_512(64)↑↓, Z_512(128)↓ |
| 256 | 80 | 0.9545 | 0.9922 | 0.109 | ≥0.0125 | 7 | Z_256(80)↑, Z_512(80)↑↓, Z_512(160)↓ |
| 280 | 60 | 0.9774 | 0.9424 | 0.094 | ≥0.0157 | 7 | Z_280(60)↑, Z_560(60)↑↓, Z_560(120)↓ |
| 300 | 80 | 0.9824 | 0.9909 | 0.123 | ≥0.0147 | 6 | Z_300(80)↑, Z_600(80)↑↓, Z_600(160)↓ |

(↑ = upper bound needed, ↓ = lower bound needed.)

- These windows scale like the spin-1 proof: n/ξ ≈ 5.6 and βΔ ≈ 5.
- **Accuracy.** Give the upper bounds a budget of η/4 ≈ 0.025 in ln Z. That means ln Z must be pinned to ≈ 0.025 absolute, out of |ln Z| ≈ βL|e0| ≈ 1.6e5, so the relative precision is **~3e-7**.
  - Per-site free-energy error: ≈ **1.3–1.5e-6 at L=n** and **6.5–7.5e-7 at L=2n**.
- **Lower bounds.** A single-state variational bound Z ≥ e^{−β⟨H⟩} drops the thermal factor ln(1+ε) (≈ 0.018 at n=256, β=64; ≈ 0.004 at β=80). Taking β = 80 makes one trial state nearly sufficient. The energy error must satisfy |ΔE| ≲ 0.03/β ≈ 4e-4 total on L=512 (~1e-6 per site).
- **Prefix L = 10..255** (gaps for the shorter chains). Each even L needs its own single-L purity certificate, i.e. its own two-sided Z bounds.
  - Target γ = 0.02: β ≈ 52–54, slack ≈ 0.24. Per-site accuracy runs from 1e-4 (L=16) to 5.8e-6 (L=254).
  - Target γ = 0.04: slack ≈ 0.06. Per-site accuracy runs from 2.3e-5 down to 1.3e-6.
  - For L ≲ 2ξ the model is crude, because it uses the infinite-volume dispersion. Treat the prefix numbers as order-of-magnitude.

## 2. Spin-1 sanity check of the method (task 3)
- **Model vs. the rigorous seeds** (n=34, β=12.25): the model gives S = 0.9778, T = 0.9188. The rigorous certificate (`seal12/certificate_w12_Z1.json`) has S ≥ 0.946471, T ≥ 0.833225. So the real proof spent log-slack ≈ 0.033 on S and 0.098 on T. The model's max uniform slack there is 0.080, and its minimal closing n is ≈ 24, which is consistent with the proof closing at 34.
- **ln Z_L, model vs. rigorous** (`thermal_arb`): L=12 gives 0.729 vs 0.642; L=10 gives 1.152 vs 0.976. The model Lüscher shift at L=12 is δ = −0.0579, against −0.0518 from ED. So the model is in the right ballpark and mildly pessimistic.
- **Lesson.** Spin-1 needed exact rigorous data up to L ≈ 2ξ (L=12) plus moment/Hankel extrapolation to n=34 and 2n=68. The spin-2 analogue needs exact data at L ≈ 100. Exact traces are impossible there (5^100 states).
- **Float ED for spin-2** (`ed_small.py`, Sz=0/1 Lanczos; E0/L and triplet gap):

  | L | E0/L | gap |
  |---|---|---|
  | 4 | −5.0 | 1.0 |
  | 5 | −4.2278 | 0.961 |
  | 6 | −4.86078 | 0.697 |
  | 7 | −4.52252 | 0.826 |
  | 8 | −4.815234 | 0.546 |
  | 9 | −4.63136 | 0.715 |
  | 10 | −4.794845 | 0.453 |

  The L=10 sector has dimension 856,945 and took 22 s in float. A full-spectrum rigorous Z, which is what the spin-1 route used, is realistic only for L ≤ 8 (5^8 = 390,625, comparable to spin-1 L=12). Lily's bound −4.81535 per site sits just below E0(8)/8. It is 0.054 per site from e0, about **4×10⁴ too loose** for our needs.
- **ALT/Trotter upper bound** (`alt_trotter.py`, float). Tr(e^{−τHe/2}e^{−τHo}e^{−τHe/2})^m ≥ Z holds for every m tested and converges as η(m) ≈ c·Lβ³/m².
  - Spin-1, β=12.25: c ≈ 0.138 (L=4), 0.097 (L=6), 0.088 (L=8). The float lnZ agrees with the repo's rigorous upper bound to 1e-11 at L=4, 6, 8.
  - Spin-2, L=4 (β=20, 60): c ≈ 0.85.
  - Spin-2 L=6 did not finish inside the time cap.
  - Required m = β^{3/2}·sqrt(cL/η_up) with c ≈ 0.85: **m ≈ 4.8e4 for (L=256, β=64)** and **≈ 6.8e4 for (512, 64)**.

## 3. Route comparison
| Route | Upper/lower | Status for spin-2 |
|---|---|---|
| (a) Exact diagonalization with symmetries (Sz, k, parity, SU(2)) under the 600 s cap | both, exact | L ≤ 8 rigorous; L = 9–10 float only. Covers <4% of the needed L. **Blocked.** |
| Moment/Hankel extrapolation (spin-1 method) | both | Needs exact data at L ≳ 2ξ ≈ 100. **Blocked.** |
| (b1) Golden–Thompson / ALT symmetric Trotter (2-color, even L) | **upper**, rigorous direction, monotone in m | The bound is fine, but evaluating the trace still costs either d^L (space) or d^{2m} with m ~ 5e4 (time). Higher-order splitting loses the ALT monotonicity. **Blocked.** |
| (b2) MPS/MPO/TEBD with a truncation-error budget | lower bound OK (variational); upper bound needs a rigorous error amplification that itself needs a sharp E0 lower bound, which is circular | **Lower bound feasible; upper bound blocked.** |
| (b3) Schatten monotonicity Z_L ≤ Z_k^{L/k}, Z_n ≤ ‖X‖^{n−k}Z_k | upper | Loses (e_k − e0)·βL. Useless unless k ≳ ξ. **Blocked.** |
| (b4) Berezin–Lieb (classical spin S+1) | upper | Exponentially loose. **No.** |
| (b5) Markov entropy decomposition / SDP free-energy lower bound (Poulin–Hastings type) | gives an upper bound on Z | Needs marginals of size ~ξ ≈ 50 sites at 1e-6 per site. **Research.** |
| (b6) Collatz–Wielandt on the Marshall-rotated (positive, stoquastic) transfer operator | upper on ‖X‖ / Z | Rigorous and cheap per test vector, but needs a near-optimal positive vector, plausibly from an MPS. Tightness unknown, likely loose. **Research lead.** |
| Temple/Kato eigenvalue bounds | lower bound on E0 | Need a gap lower bound, which is circular. **No.** |
| Quantum Monte Carlo | — | Not rigorous. Estimates only. |
| (c) Lily's local-gate route | energy lower bound ⇒ upper bound on Z | The present bound is 0.054 per site off. Spin-2 needs ~1e-6 per site, an extensive-accuracy barrier. **Blocked as stated.** |

## 4. Recommended plan (with costs)
1. **Do not launch production runs.** Every route fails at the upper-bound step, so compute spent now would not move the proof.
2. **Feasible now (cheap).**
   - Rigorous finite-L spin-2 data for L ≤ 8: interval-arithmetic full spectrum, about 1–3 h total split across many processes under the 600 s cap.
   - Variational MPS lower bounds on Z_512 at β = 64/80/128. Use bond dimension ~200–400 and a single or few trial states. Expect hours of CPU, but it splits only awkwardly under the 600 s per-process cap and needs checkpointing.
   - Neither is useful until the upper side exists, so treat both as optional.
3. **Research (the real blocker): a rigorous upper bound on Z_L, equivalently a lower bound on free energy / E0, accurate to ~1e-6 per site at L ~ 250–600.** Leads, in order:
   - (i) Collatz–Wielandt / positive-vector bounds on the Marshall-rotated transfer operator, with MPS test vectors;
   - (ii) SDP / Markov-entropy free-energy lower bounds that use ξ-scale marginals;
   - (iii) a sharpened local-gate (Lily) bound with large blocks plus an Anderson-type correction.

   A quick viability test for each lead: does it reproduce spin-1 e0 to ~1e-6 per site at modest cost? If not, it cannot work for spin-2.
4. **Intermediate milestones.**
   - Rigorous spin-2 finite-L gaps for L ≤ 8.
   - Rerun the full pipeline on a model with intermediate ξ (spin-1 bilinear–biquadratic tuned to ξ ≈ 10–20) to measure how the cost of the upper bounds scales with ξ.

## 5. Honest blockers
- Spin-2 has ξ ≈ 50, about 8× spin-1, so every required L grows ~8× and the d^L cost grows from 3^12 to an effective 5^100 or more.
- Upper bounds need relative precision ~3e-7 on ln Z at L = 256–600 and β = 60–80. No known rigorous method reaches that.
- Every prefix L ≤ 255 needs its own certificate at 1e-4 to 1e-6 per-site accuracy.
- The model numbers are estimates. The window estimates are fairly robust; the prefix estimates for L ≲ 100 are crude.
- Spin-2 L=6 ALT data is missing (timeout). The Trotter coefficient c ≈ 0.85 comes from L=4 only.
