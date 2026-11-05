# Lead 2 paper-check: do SDP / entropy relaxations escape the ring ceiling?

Date: 2026-11-04 (America/Chicago). Scope: theory and literature only. No new computation (none was needed to settle the questions).
Status labels: **[proved]** means a short argument is given here. **[lit]** means quoted from the paper named. **[est]** means a heuristic order-of-magnitude estimate, not a bound.

## 0. Bottom line
* Every method in scope is a relaxation over local marginals on a window of size W, possibly compressed. A ring state, whether a ground state or a Gibbs state, of any size p ≥ W (≥ 2W for the entropy-constrained T = 0 variants) supplies a feasible point. So each relaxation is capped by a ring value: μ ≤ min_{p≥W_eff} E0(p)/p at T = 0, and the finite-T analogue holds as well. **None of them escapes the ceiling.** Extra constraints (entropy, EEB, NPA moments) only change which W_eff appears in the cap. [proved, §1]
* Kull et al. (arXiv:2212.03014) **state this ceiling themselves and observe that it is saturated**, for the spin-1 Haldane chain among other models (quote in §2).
* For spin-1, the best published rigorous TL lower bound is about 1.4e-4 per site (Kull et al., Fig. 5e, read off the plot). The target of 1e-6 is about 2 orders of magnitude beyond that. For spin-2, nothing is published. The estimated need is W_eff ≳ 250–500 with bond dimension in the hundreds, which is far out of reach.
* **Conversion to Z_L upper bounds:** an infinite-volume lower bound f_LB gives ln Z_L ≤ −βL f_LB + O(β‖h‖) (open chain: +β‖h̃‖; ring: +2β‖h̃‖). That is rigorous but the slack is 37 (spin-1, β = 12.25) or 640 (spin-2, β = 64), against a needed 0.025. Removing the slack requires the finite-size term itself, which is the spatial-gap (QTM) quantity. That is circular. A relaxation applied directly to the L-ring is capped by rings p ∈ [W, L), so it needs W ≈ L. [proved, §4]
* **Recommendation: do not pursue lead 2 for the proof.**

## 1. Ceiling per method [proved]
Notation: H = Σ h_{i,i+1}. e_p = E0(p)/p is the ring ground-energy density. f_p(β) = −ln Z_p^ring /(βp).

**(a1) Anderson / LTI hierarchy (Kull Eq. 5: ρ^(n) ≥ 0, Tr_L ρ^(n) = Tr_R ρ^(n)).** The n-site marginal of a ring ground state with p ≥ n sites is PSD and translation-consistent. So E_LTI(n) ≤ min_{p≥n} e_p.

**(a2) NPA / Lasserre / RDMT moment relaxations (Barthel–Hübener, Baumgratz–Plenio, Haim–Kueng–Refael, Wang et al.).** All constraints are of the form ⟨O†O⟩ ≥ 0 for O supported in a window of size W, plus TI. These are satisfied by the true expectation values of any ring state with p > W, because no constraint wraps around the ring. So the same cap applies with W = moment support.

**(a3) Kull–Schuch–Dive–Navascués coarse-grained relaxation.** This is a relaxation of LTI at level n (they state E^relax(n,D) ≤ E_LTI(n)). So it is capped by min_{p≥n} e_p. The point of the method is that n can be large (their n_eff ≈ 40–120) at polynomial cost. The cap is therefore harmless at spin-1, where the ring deficit at n = 50 is about 1e-6. The real limit is the compression loss at finite D.

**(b1) FFS finite-T energy-entropy balance (arXiv:2311.18706).** The constraints are ω(a*a) log(ω(a*a)/ω(aa*)) ≤ β ω(a*[H,a]) for a supported in Λ, with [H,a] supported in Λ̄, plus TI. These hold for any β-KMS state. A ring Gibbs state with p > |Λ̄| is KMS for H_p, and H_p agrees with H on Λ̄. So it is feasible. Lower bounds on u(β′) for β′ ≤ β integrate to a lower bound on βf = −ln d + ∫_0^β u, and each is capped by the ring value u_p(β′). So the bound on f is capped by f_p(β).

**(b2) MED / Poulin–Hastings (arXiv:1012.2050) and FFS entropy constraints (arXiv:2305.06855).**
* T > 0: the TI relaxation is min e(ρ_W) − T c_W(ρ_W), with c_W = S(ρ_W) − S(ρ_{W−1}). The true infinite Gibbs marginal is feasible. So MED_W ≤ f_∞ − T (c_W^Gibbs − s_∞). The bracket equals the CMI tail Σ_{k≥W} I(k+1 : 1 | 2…k) ≥ 0. This intrinsic cap is MED's own truncation error and it binds before the ring cap does.
* T = 0: the entropy constraint S(W|1…W−1) ≥ 0 is sandwiched between LTI(W) and LTI(2W−1) (FFS 2305.06855, Thm 4.1, paraphrased: C^{loc,TI}_{2l−1} ⊂ C^{WM,TI}_l; abstract: the constraints are "implied by doubling the number of sites in the relaxation"). So the ceiling applies with W_eff ≤ 2W−1. Separately, a ring ground state with p ≥ 2W has c_W ≥ 0, because S_W is concave and symmetric about p/2. So min_{p≥2W} e_p is also a cap.
* Compressing the conditioning system B by a channel Φ is still valid by data processing (S(A|B) ≤ S(A|Φ(B))). So a Kull-style compressed MED is conceivable. It is not in the literature, and it would inherit the same caps plus compression loss.

**(c) Araki noncommutative transfer map (FFS–Scalet arXiv:2209.14989, also 2402.19030).** This is not a relaxation, so the ring ceiling does not apply. The certified error ε(L) decays superexponentially in L, but with constants that are triple-exponential in β‖h‖. In the abstract's words, the runtime hides "exp(exp(O(β)))". Their own numerics are dimerized XY only (d = 2, L = 11, about 13 s per point), as a non-certified approximation. At β‖h̃‖ ≈ 64·5 = 320 (spin-2), the rigorous bound is vacuous. So this route gives no usable certificate.

## 2. Literature numbers (real quotes; TL = thermodynamic-limit rigorous lower bound)
| Ref | Model | Rigorous TL? | Accuracy / cost |
|---|---|---|---|
| Kull, Schuch, Dive, Navascués, arXiv:2212.03014 (PRX 2024) | **spin-1 Heisenberg (model e)** | yes (certified dual, Sec. IV.3) | Fig. 5e, read off the plot: ΔE ≈ 4e-2 (D=2), 1.6e-2 (3), 5.5e-3 (4), 2.2e-3 (5), ~1e-3 (6), ~4.5e-4 (7), ~2e-4 (8), **~1.4e-4 (D=9, n≈50)**. Exact LTI only to n≈8 (ΔE≈1.5e-2). For D=6–9: "our own matrix-free implementation of SCS ... to produce the results for bond dimensions 6 through 9"; interior point "prevented us from going to bond dimensions higher than 7". |
| same | spin-1/2 Heisenberg | yes | n_eff(7)≈60. Compared with Barthel–Hübener (TI, infinite): "errors … 2×10^-3 for Δ=1 … We obtained 3×10^-4". |
| same, ceiling statement | models b–f, incl. spin-1 | — | "The LTI energy density E_LTI(n) is thus upper bounded by the smallest ground state energy density for any ring of size m≥n, min_{m≥n} E_PBC(m)" and "Remarkably, we find that for models b through f … E_LTI(n)=min_{m≥n}E_PBC(m) (up to solver precision)". **The ceiling is saturated.** Cross-check with our ED: Fig. 5e LTI points ≈ 0.098 (n=4), 0.035 (6), 0.0156 (8), against e0 − e_p = 0.0985, 0.0348, 0.0156. |
| Barthel–Hübener PRL 108, 200404 (arXiv:1106.4966) | spin-1/2 XXZ, infinite TI | yes | 2e-3 (Δ=1), 3e-3 (Δ=2), <1e-4 (Δ=0), as quoted by Kull. |
| Baumgratz–Plenio NJP 14, 023027 | spin-1/2 Heisenberg rings ≤ 50 | no (finite ring) | "energy densities 10^-2 below the true infinite-system value" (Kull's summary). |
| Haim–Kueng–Refael arXiv:2001.06510 | TFI / XXZ rings | no | "errors of the order 10^-2 and 10^-1" (Kull's summary). |
| Wang et al. PRX 14, 031006 (arXiv:2310.05844) | spin-1/2 Heisenberg, ring L=100 | no (finite ring) | "error of 4×10^-4" (Kull's summary). |
| FFS arXiv:2305.06855 (JMP 65, 032201) | spin-1/2 XY, XXZ(Δ=−2), TFI | yes (T=0) | Sizes up to l≈8 (about 900 s). Gain is at most "a quadratic improvement in terms of the matrix sizes". No spin-1 data. |
| FFS arXiv:2311.18706 (finite-T EEB) | TFI only (⟨Z0⟩, ⟨Z0Z1⟩, L=4,5 regions) | yes | No Heisenberg or spin-1 numbers. Exponential convergence proven only for commuting H. |
| Poulin–Hastings arXiv:1012.2050; Scalet et al. arXiv:2504.17405 | — | MED is a rigorous lower bound on F | 2504.17405 proves MED convergence in 1D at any T ("polynomial … time approximation algorithms"). No spin-1 or spin-2 accuracy numbers. |
| arXiv:2604.01555 | finite square lattices up to 16×16 | finite-size only | Not a TL bound; for rings it is capped by E0(N) anyway. The "<1e-5" figure from search was **not verified**, so it is not used here. |

No rigorous lower bound for the spin-2 Heisenberg chain at any accuracy was found.

## 3. Block-size estimates for 1e-6 per site [est]
Inputs: ξ_T ≈ min(ξ, vβ). Spin-1: β = 12.25, vβ ≈ 30 > ξ ≈ 6, so ξ_T ≈ 6. Spin-2: β = 64, vβ ≈ 280 > ξ ≈ 50, so ξ_T ≈ 50. The ceiling term uses the Lüscher deficit m e^{−p/ξ_T}/(βp) with triplet m = 3.
* **Ring / finite-T ceiling alone:**
  * spin-1: W ≳ 50 (T=0 Lüscher model from lead 1: deficit 6.5e-6 at p=40 and 1.25e-7 at p=60);
  * spin-2: W ≳ 230 (T=0) and ≳ 260 (finite T, solving 3e^{−p/50}/(64p) = 1e-6).
* **MED intrinsic cap T·(c_W − s):** the target is c_W − s ≤ 1.2e-5 (spin-1) and ≤ 6.4e-5 (spin-2). With c_W − s ≈ A e^{−W/ξ_CMI}, A ~ 1, and ξ_CMI ∈ [ξ_T/2, ξ_T]:
  * spin-1: W ≈ 35–70;
  * spin-2: W ≈ 250–500.
* **Kull-type compression:** at spin-1 the ring cap is not binding (about 1e-6 at n≈50). The D-loss is. Extrapolating the Fig. 5e trend (a factor of about 2.3 per unit of D) from 1.4e-4 to 1e-6 gives roughly D ≈ 15–20 without SU(2) symmetry. The PSD blocks are d²D² ≈ 2000–3600 dimensional, times about 100 levels, and the dual must be certified to about 1e-6. That is a frontier computation about 2 orders past the published result. It is conceivable but expensive. At spin-2 (ξ=50), n_eff ≳ 250 and MPS accuracy of 1e-6 needs D in the hundreds. Blocks of dimension 25D² ≳ 1e6 are infeasible.

## 4. Conversion direction [proved]
* **Ring, transfer-matrix picture:** Z_L = Tr X^L ≥ λ0^L, so ln Z_L ≥ −βL f_∞. An f lower bound pushes the other way, and the finite-size excess ln(1 + Σ_{i≥1}(λ_i/λ0)^L) is exactly the spatial-gap quantity. That is circular for the bootstrap.
* **What is rigorously available:**
  * Let h̃ = h − c·1, with c chosen to minimise ‖h̃‖. The shift changes ln Z_L by an exactly known amount: half-spread ‖h̃‖ = 1.5 (spin-1) and 5 (spin-2).
  * By |ln Z_{m+n} − ln Z_m − ln Z_n| ≤ β‖h̃‖ (one bond, via the Peierls–Bogoliubov / Golden–Thompson bound), ln Z_m − β‖h̃‖ is superadditive.
  * Fekete's lemma then gives ln Z_L^open ≤ −βL f_∞ + β‖h̃‖ and ln Z_L^ring ≤ −βL f_∞ + 2β‖h̃‖.
  * So ln Z_L ≤ −βL f_LB + 2β‖h̃‖ is valid. The slack is 36.75 (spin-1) or 640 (spin-2), against a requirement of about 0.025. It is useless.
* **Relaxations applied directly to the L-ring (finite system):** marginals of rings p ∈ [W+1, L) remain feasible. So the bound on −ln Z_L/β is capped by L·min_p f_p. Spin-2 at L = 256 needs (3·256/W)e^{−W/50} ≲ 0.025, so W ≳ 245 ≈ L. That is equivalent to solving the full problem.

## 5. Verdicts
| Method | Escapes ring ceiling? | Spin-1 1e-6 plausible? | Spin-2 1e-6 plausible? | Finite-L Z_L upper bound? |
|---|---|---|---|---|
| Anderson / LTI | no (saturates it, Kull) | no (n≈8 max exact) | no | only with W≈L |
| NPA / RDMT (BH, BP, HKR, Wang) | no | no (best ~1e-3–1e-4, spin-1/2) | no | finite-ring only, capped by W≈L |
| Kull et al. coarse-grained | no (capped by n; cap harmless at spin-1) | marginal: ~2 orders beyond the published 1.4e-4; D≈15–20 research project | no (D in the hundreds, n≳250) | no |
| FFS EEB (finite T) | no | no data; uncompressed W≈50 infeasible | no | no |
| MED / FFS entropy | no (plus intrinsic CMI cap) | uncompressed W≈35–70 infeasible | no (W≈250–500) | no |
| Araki transfer map (FFS 2022) | n/a (not a relaxation) | certified bound vacuous | vacuous | no |

**Recommendation:** drop lead 2 as a route to the proof. Even a heroic spin-1 Kull-type computation would yield only an f_∞ lower bound. That converts to a Z_L upper bound only with O(β‖h‖) slack, or else requires the circular spatial-gap term. This does not depend on how accurate the f bound is.

## Erratum to §4 (2026-11-04)
The slack in the f_∞ → Z_L conversion is not 2β‖h̃‖. For even L and m, Z_L ≤ ‖X‖^{L−m} Z_m holds (PROVED: Z_L = Σ|λ_i|^{L−m}|λ_i|^m ≤ ‖X‖^{L−m} Z_m), with ‖X‖ = e^{−β(f_∞+a)}. So an f_∞ lower bound with error δf, combined with exact Z_m, gives ln Z_L^up − ln Z_L ≲ Lβδf + imp_m.
- Spin-1: imp_12 ≈ 0.635.
- Spin-2: imp_8 ≈ 24–28.
The verdicts are unchanged (see NEW_IDEAS.md §A, §B1).
