# INTERVAL_SCOPING — explicit gap for KHH(α), α ∈ [1−δ, 1(+δ)]  (scoping only; no heavy runs)

Labels: PROVED / NUMERICAL / HEURISTIC. Paper claims below were checked against the fetched texts:
- GM: /workspace/papers/gm.txt
- Lemm–Mozgunov (LM): arXiv:1801.08915, fetched
- Moon–Nachtergaele (MN): arXiv:1804.04750, /workspace/papers/mn.txt
- NSY Part II: arXiv:2010.15337, abstract only
- Other items are marked "(literature, not re-read)".

## 1. Structure of the perturbation (PROVED, exact algebra)
- KHH(α) bond: h(α) = h(1) − (1−α) w, where
  - h(1) = 10(P3/7 + P4);
  - w = 6P0 + 5P1 + 3P2 + (10/7)P3 + 6P4 ≥ 0, with ‖w‖ = 6.
- w is not proportional to h(1) and does not annihilate the VBS state on every bond, because w has P0, P1 and P2 weight. So **KHH(α) is not frustration-free for α ≠ 1** (PROVED for α < 1: by the variational principle, E_0 ≤ −(1−α)·m·⟨w_bond⟩_VBS < 0, while every bond term has a kernel. For α > 1: the bond operator h(1) + |1−α|w is positive definite, because P0..P2 enter with positive weight, so no state minimises every bond).
- Both signs are handled the same way: α > 1 is ε := 1−α < 0.
- KHH(0) is the spin-2 Heisenberg chain. The interval [0,1] connects AKLT to Heisenberg, so a numerically large rigorous δ would be a significant step toward the S = 2 Haldane conjecture. Nothing below gets close to that.

## 2. What each candidate route actually gives

| route | applies to non-FF H(α)? | explicit constants? | verdict |
|---|---|---|---|
| Knabe / GM / LM finite-size criteria | **No.** LM §1, verbatim: "frustration-freeness is essential for this approach" | yes | dead for α ≠ 1. Still the tool for the α = 1 local-gap inputs below. |
| Direct operator inequality H(α) ≥ c·H_AKLT − K | gives E_1 ≥ c·gap·… + E_0(B), but E_0(H(α)) ≤ ⟨VBS\|B\|VBS⟩, so gap(H) ≥ c·ε − (⟨B⟩_VBS − E_0(B)) | yes | **dead.** The bracket is extensive (∝ m·(1−α)) unless B is itself FF with the VBS as ground state, which would make H(α) FF. Fixing it needs O(1)-accurate control of an extensive ground energy, which is the stability problem itself. |
| Yarotsky (2006, AKLT-type, cluster expansion) / Szehr–Wolf (2015 MPS) | yes | "exists ε_0" (literature, not re-read) | constants are never evaluated. Expected cluster-expansion losses are astronomically small (HEURISTIC, ~1e-15 or below). |
| BHM / Michalakis–Zwolak (periodic, spectral flow) | yes | MZ Prop 2 relative bound is explicit given local gaps γ(r) and LTQO, but the spectral-flow constants are only "exists" | possible, but messier than MN. |
| **Moon–Nachtergaele 2018, Thm 3.11 (1D, open and periodic-type intervals)** | yes | **yes, stated explicitly:** γ(H_Λ(ε)) ≥ γ0 − (m + 2M_D)ε for ε < γ0/(m + 2M_D). Here m = Σ_{\|n\|≥3} 20C(3\|n\|+2)[Ω((\|n\|−1)/2) + F0((\|n\|−3)/2)]^{1/2} + Σ_n C[Ω(\|n\|/2) + 2F0(⌊\|n\|/2⌋)] + 8(‖η‖_F + M_Int), with F0(x) = F^b(x/18 − R − 3/2) | **best candidate.** C comes from the spectral-flow decomposition (NSY Thm 6.3.4 / Part I). It depends on M, R, γ0, the Lieb–Robinson velocity and the filter decay; it is explicit but enormous. |
| NSY Part II (2021), general boundary conditions and symmetry breaking | yes | constants traceable, not evaluated | backup for periodic boundary conditions. |
| Lie–Schwinger block diagonalisation (Fröhlich–Pizzo, Del Vecchio–Fröhlich–Pizzo–Rossi, AKLT-type; literature, not re-read) | yes | t̄ "small enough", not numerical | possible, but the AKLT version requires rewriting the scheme with explicit constants. Cost ≫ MN route. |

## 3. Recommendation
**Route MN+**: Moon–Nachtergaele Thm 3.11, with every constant evaluated, fed by certified α = 1 inputs. For the ring, use the NSY Part II or MZ periodic version with the same inputs.

The required inputs and their cost:

1. **Uniform local gap γ0 for all open intervals of length > R (R = 2)** at α = 1. This is the main missing input, and it is not covered by CERT_ALLM.
   - Cheap path (scoped in CERT_ALLM §5, NUMERICAL): LM eq. (4.16) with certified ε_8 gives about **0.00123** (×10/7 for KHH units) for m ≥ 16. It also needs certified ε_3..ε_7 and a GM′-type extension of LM Prop 4.4 to m ≥ 8, plus ring-style certs for short open chains.
   - Cost: under 1 CPU-hour total, plus about a day of proof write-up.
   - Possible improvement: Nachtergaele's martingale method. It could give γ0 ~ 0.05 using exact 9×9 transfer-matrix ε-quantities, since the spin-2 VBS correlation ratio is 1/2. Cost: about a day. Recommended, because δ scales roughly like γ0 to a power ≥ 1.
2. **LTQO function Ω(r)** for spin-2 VBS, open boundary conditions with boundary cut-offs.
   - Form: Ω(r) = K·2^{−r}. This is exact MPS algebra (MN quote AKLT spin-1 with Ω = 3^{−r}; spin-2 should follow analogously; HEURISTIC until computed).
   - Cost: minutes of exact or arb computation.
3. **F-norm data** ‖η‖_F, M_Int, M_D for the nearest-neighbour perturbation, with F(x) = e^{−h(x)}L/(1+cx)^κ.
   - For a nearest-neighbour Φ this is trivial: ‖Φ‖_F ≈ ‖w‖·F(1)^{-1} = 6/F(1).
4. **The constant C of the decomposition theorem.** This is an explicit evaluation of Lieb–Robinson velocity bounds (‖h‖ = 10, R = 2), the quasi-adiabatic filter w_γ0 (Hastings–Wen/BMNS filter, decay depending on γ0), and the polynomial F^b tails.
   - Cost: pure bookkeeping, plus arb evaluation of 1D integrals and sums. Compute is minutes; analyst time is one to three weeks, because the hard part is reading NSY Part I §6 line by line.

**Plausible δ (HEURISTIC).** The MN formula has three severe losses:
- the argument shift F0(x) = F^b(x/18 − R − 3/2), so decay starts only beyond about 45 sites;
- only polynomial F^b tails under a square root;
- C scaling like (filter constants)·(LR velocity)/γ0^p.

These suggest m + 2M_D ~ 1e5–1e9 in KHH units. So δ ~ γ0/(m + 2M_D):
- **~1e-8 – 1e-12** with γ0 ≈ 0.0018 (LM route);
- maybe ~1e-6 – 1e-9 with γ0 ≈ 0.07 (martingale route).

The result is symmetric in ε, so it covers α ∈ [1−δ, 1+δ]. Gap bound on the interval: γ(α) ≥ γ0 − (m + 2M_D)|1−α|.

**Cheap complementary, fully rigorous result (PROVED per m, not uniform).**
- What: for fixed small rings, m ≤ 8, certify the KHH(α) gap on α ∈ [1−δ_m, 1+δ_m] with δ_m ~ 1e-2. Use the existing certificate at α = 1 plus Weyl/Kato perturbation: ‖ΔH‖ ≤ 6m|1−α|, together with second-order isolation of the 1-dim kernel.
- Cost: minutes.
- Value: data and sanity checks only, because it is not uniform in m.

**Novelty.** To our knowledge (literature, not exhaustively checked), no paper gives a *numerical* stability radius for any AKLT-type chain under a non-FF perturbation. MN and NSY say the constants "can be explicitly determined" but do not evaluate them. An evaluated δ, even 1e-10, would be a new, citable but modest result: mostly careful bookkeeping, with no new idea. Making δ physically meaningful (≫ 1e-3) would need a genuinely new non-FF finite-size criterion. None exists, and LM's remark explains why the Knabe-type mechanism cannot provide one.

## 4. Proof-debt ledger (Part B)
| item | status | cost |
|---|---|---|
| decomposition h(α) = h(1) − (1−α)w, ‖w‖ = 6 | PROVED (exact algebra) | done |
| FF criteria inapplicable for α ≠ 1 | PROVED for the method (LM statement plus the non-FF observation); not a no-go theorem | done |
| direct operator inequality insufficient | PROVED for that method (extensive-bracket argument above) | done |
| MN Thm 3.11 statement and constant m formula | verified from the paper text | done |
| uniform open-chain local gap γ0 at α = 1 | OPEN (LM route NUMERICAL ≈ 0.00123; martingale route untested) | ≤ 1 CPU-h + 1–2 days write-up |
| spin-2 VBS LTQO Ω(r) | OPEN (HEURISTIC K·2^{−r}) | minutes |
| explicit decomposition constant C (NSY Part I Thm 6.3.4) | OPEN, the main cost | 1–3 analyst-weeks |
| periodic-boundary version (NSY II / MZ) of MN bound | OPEN | +about 1 week |
| δ estimate 1e-8–1e-12 | HEURISTIC | — |
| per-m finite-ring interval certificates | OPEN, cheap | minutes |
