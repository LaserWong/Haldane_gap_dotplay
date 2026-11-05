# Fuzzy MPS — obligation map (Stories A and B)

Date: 2026-11-05 America/Chicago. Labels: PROVED / EXTERNAL / TESTED / HEURISTIC / BLOCKED / OPEN.
Sources: ChatGPT share 6aec8974…, Xiao screenshots (2026-11-05), runs/spin2/FEASIBILITY.md, open_claims/STATUS.md, spin1_opt2/PILOT.md, CERT_ALLM/OPEN (AKLT).

## 0. Two stories (do not mix)

| | Story A — fuzzy *thermal seeds* | Story B — fuzzy *ground-state / parent* |
|---|---|---|
| Input | Intervals for Z_n(β), Z_2n(β), Z_2n(2β) | Approximate MPS ψ ≈ GS; parent H_P; complement projector |
| Consumer | Existing purity bootstrap (S,T → G-recursion → γ) | Stability / FNW / NSY-type transfer from H_P to H_Heis |
| What “fuzzy” means | Certified error η on an approximate thermal operator / sampler | Certified distance of ψ (or H_P) from the exact object |
| Already known | Interface works (TFI purification PARTIALLY CONFIRMED in open_claims; alternating-chain table in the share) | Exact AKLT MPS parents work (spin-1 gap 0.1; our spin-2 AKLT all-m PROVED). Heisenberg is **not** an exact MPS GS |

---

## 1. Story A — load-bearing obligations

Consumer need (spin-1 recipe, already PROVED at γ≈0.0252): lower endpoints
  s ≤ S = A²/B , t ≤ T = B²/D
with A=Z_n(β), B=Z_2n(β), D=Z_2n(2β). Errors enter only at the seed.

### A1. Lower bounds on Z (easy side)
- Variational / single-state: Z ≥ e^{−β⟨H⟩_ψ}. PROVED direction.
- Spin-2 target (FEASIBILITY, ESTIMATE): |ΔE| ≲ 1e-6 per site at L~512, β~80.
- **Status:** OPEN as computation, **not** conceptually blocked.

### A2. Upper bounds on Z (hard side) — THE blocker
Needed for denominators of S and T. Equivalent to a free-energy / E0 lower bound.
- Exact ED: spin-1 to L=12 PROVED (now arb-only); spin-2 only L≲8 realistic. BLOCKED for L~ξ.
- ALT/Trotter: rigorous **upper** on Z, but evaluating Tr still costs d^L or huge 2D contraction. BLOCKED at scale.
- MPS/MPO/TEBD truncation: lower OK; **upper needs error amplification that typically needs a sharp E0 lower bound → circular** (FEASIBILITY b2). BLOCKED as stated.
- Collatz–Wielandt on Marshall-rotated transfer + MPS test vector: OPEN research lead.
- MED/SDP free-energy lower bounds: OPEN research; needs ~ξ-scale marginals at 1e-6/site.
- Monte Carlo: statistical upper only at a confidence level — not a PROVED deterministic seed unless the whole theorem is restated as high-probability.

### A3. Error through successive squaring / compression (Xiao’s L=256 claim)
Xiao reports first-step relative loss ~1.01e-12 (independently rechecked), then needs propagation under squaring to low T.
Discriminate:
- (A3a) Loss vs the **exact** short-time gate / Trotter step → can feed A2 if inequality direction is upper on Z.
- (A3b) Loss only vs the **previous approximate** iterate → does **not** close A2.
**Status:** OPEN; we do not have his code. Treat A3b as the default until proved otherwise.

### A4. Spin-1 recipe ceiling (local to improving spin-1 γ)
Option 2 pilot: even ideal L≤12 + float L=13/14 → γ≈0.027 (~1.07×). Binder is U≈1.0013, not seed noise.
**Conclusion:** Story A will not 1.5× the spin-1 bound under the present filters. Its payoff is **spin-2 / large-ξ models**.

### A5. Prefix lengths
Even with a large-n seed, every L < n needs its own two-sided Z bounds (or another finite-L argument). Spin-2 prefix to L~100 is a second copy of A2 at smaller L.

---

## 2. Story B — load-bearing obligations

Consumer need: γ(H_Heis) ≥ f(γ(H_P), ‖H_Heis−H_P‖, edge terms) > 0, uniform in L (or for all L≥L0).

### B1. Approximate MPS ψ with controlled defect
- Exact VBS/AKLT: defect 0, PROVED parents (spin-1 classical; our spin-2 P3+P4 all-m).
- Fuzzy ψ: need ‖(H_Heis−E)ψ‖ or a local residual bound, certified. OPEN for Heisenberg.

### B2. Parent gap γ(H_P) > 0
Xiao: long-range parent uniform gap, independently rechecked. Treat as TESTED/claimed until we have the artifact.
Our CERT_ALLM/OPEN cover **exact** AKLT parents, not fuzzy parents of Heisenberg.

### B3. Complement / support energy bound
Xiao: L=8 local block on support complement, positive energy, rechecked. TESTED/claimed.
Must hold with constants compatible with B4.

### B4. Coupling / stability (THE missing step Xiao names)
Control matrix elements of H_Heis between support(ψ) and complement, plus boundary corrections, so that
  γ(H_Heis) ≥ γ(H_P) − C·coupling − edge
stays positive for all L (or all L≥L0).
- Near AKLT (small deformation): NSY / Moon–Nachtergaele style interval theorems exist in principle; our INTERVAL_SCOPING estimated δ~1e-8–1e-12 at spin-2 — weeks of bookkeeping, modest novelty.
- At pure Heisenberg (O(1) from AKLT): quantitative stability **BLOCKED** with current constants (NEW_IDEAS: “far from AKLT; DROP”).
- Martingale/FNW: needs exact MPS GS — DROP for Heisenberg.

### B5. Finite-size sector tools (Casimir / M=1 at L=16)
Useful for uniqueness / sector gaps at fixed L. Do **not** replace B4 for length-uniform γ.
Xiao: identity verified; remaining local spin sectors still running. OPEN computational.

### B6. Infinite-volume uniqueness (optional, harder)
Analog of our spin-1 16c. Not required for a finite-L uniform gap theorem.

---

## 3. Cross-dependencies

- A does not need B. B does not need the bootstrap.
- A’s only cheap half (A1) is useless without A2.
- B’s cheap halves (B2–B3 claims) are useless without B4.
- Spin-2 AKLT certificates we already have are **B-type exact**, not A and not Heisenberg.

---

## 4. Cheapest discriminating tests (ranked)

| ID | Test | Cost | What a YES means | What a NO means |
|---|---|---|---|---|
| **T1** | **Truncation→squaring amplification on a known Z.** Spin-1 L=6 or 8 (exact arb Z available): one short-time TEBD/MPO step with SVD rank χ; certify Frobenius (or op) error η₁ to the exact bond gate; amplify through k squarings to target β; check whether the resulting Z upper still leaves bootstrap slack η_slack. | ~0.5–1 day | Story A has a non-circular a priori upper path at small L; scale-up becomes an engineering/constant chase | Story A via “compress then square” fails even where exact comparison exists → Xiao’s L=256 needs a different inequality (ALT/CW/SDP), not bare MPS compression |
| **T2** | **Heisenberg−AKLT residual vs AKLT gap on L=8.** Exact or high-prec: ‖H_Heis − c H_AKLT‖ (or best local c) vs γ_AKLT on the same finite chain. | ~hours | If residual ≪ γ_AKLT, B4 might close with textbook stability; worth interval-theorem work | If residual ≳ γ_AKLT (expected at pure Heisenberg), naive parent transfer is dead; B only lives near AKLT or with a new mechanism |
| T3 | Logical audit of Xiao’s 1e-12 claim: A3a vs A3b (need his definition / code) | depends on access | Guides whether to invest in T1-scaleups | — |
| T4 | Collatz–Wielandt + MPS vector on spin-1 L=12: does it recover e0 to ~1e-6/site? | 1–2 days | Opens A2 research lead (i) | Kill CW for A2 |

**Recommendation:** run **T1 first** (discriminates Story A’s only scalable-looking path without needing Xiao’s private artifacts), then **T2** (kills or opens naive Story B for pure Heisenberg). Skip production spin-2 runs until T1/T2 say otherwise.

---

## 5. Out of scope for this map
- Improving spin-1 γ via more moments (already NO from Option 2).
- Claiming Xiao’s finite L=16 gap >0.139 as a uniform theorem.
- Upstream PR merges / paper writing.
