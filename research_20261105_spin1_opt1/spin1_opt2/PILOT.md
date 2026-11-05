# Option 2 float pilot — can better seed data beat the ~0.0252 recipe ceiling?

**Label: NUMERICAL / HEURISTIC throughout. Not a certificate. Arb certification was not started.**

**Date:** 2026-11-05 (America/Chicago)  
**Workdir:** `runs/spin1_opt2/`  
**Verdict: NO — do not certify.** Best predicted γ ≈ **0.02706** (≈ **1.07×** current 0.0252132), far below the 1.5× warrant threshold γ ≳ 0.03782.

---

## Setup (existing recipe)

| Parameter | Value |
|---|---|
| Seed length n | 34 (also swept) |
| β₀ | 49/4 = 12.25 |
| Shift a | 700741/500000 = 1.401482 |
| Moment degree M | 12 (baseline); also 13, 14 |
| Caps U,V | repo Christoffel ≈ 1.001339 / 0.871030 |
| FULL forcing | R₆₈ ≈ −8.32×10⁻⁶ |
| Certified γ | 63033/2500000 ≈ 0.0252132 |
| Recipe ceiling (float repro) | ≈ 0.0252149 |
| Warrant threshold | 1.5 × 0.0252132 ≈ **0.037820** |

Pipeline (float mirror of `improve.py`): Hankel/Christoffel caps → Karamata packing → (S,T) → window C → dyadic chain → max γ.

Trusted base for this pilot: IEEE-754 float (NumPy/SciPy). Untrusted for any theorem.

---

## Results table

| Variant | M | n | C₀ | S | T | **γ** | vs 0.0252 | Effort to certify | Notes |
|---|---|---|---|---|---|---|---|---|---|
| baseline repo caps + long | 12 | 34 | 0.667 | 0.9465 | 0.8334 | **0.025215** | 1.00× | already certified | float repro of recipe |
| (i) ideal zero-err Hankel L≤12 + long | 12 | 34 | 0.668 | 0.9465 | 0.8337 | **0.025601** | 1.015× | low (re-run filters) | midpoints as exact |
| ideal L≤12, no long_bounds | 12 | 34 | 0.659 | 0.9410 | 0.8337 | 0.022056 | 0.88× | — | long_bounds matter |
| (iii) n-sweep ideal L12 (best) | 12 | **34** | 0.668 | 0.9465 | 0.8337 | **0.025601** | 1.015× | — | n=32 also ~1.00×; n≠34 worse |
| (ii) real float L=13, M=13, \|N\| | 13 | 32 | 0.660 | 0.9327 | 0.8424 | **0.027064** | **1.073×** | high (new L=13 arb thermal) | **best fair** |
| real L=13, M=13, n=34 | 13 | 34 | 0.671 | 0.9485 | 0.8337 | 0.026810 | 1.063× | high | |
| real L=14 partial, M=14, n=34+long | 14 | 34 | 0.668 | 0.9469 | 0.8337 | 0.025853 | 1.025× | very high | trunc ≪ 1e−8 |
| β₀=10 frozen moments | 12 | 34 | — | — | — | 0.03084 | 1.22× | needs full re-thermal | **HEURISTIC only** |
| oracle U=1.001 (same mj) | 12 | 34 | — | — | — | 0.06285 | 2.49× | — | shows T-binding |
| oracle U=1.0005 | 12 | 34 | — | — | — | 0.1155 | 4.58× | — | |
| oracle S=T=1 | — | 34 | 1.0 | 1 | 1 | ≥0.20 | ≥7.9× | — | chain cap in pilot |

All γ values are **NUMERICAL** predictions under the float packing/chain; none are proved.

---

## Variant details

### (i) Ideal (exact-spectrum) caps from L≤12

Re-optimized Christoffel square filters on thermal_arb midpoints with err=0.
- U: 1.001339 → 1.001336 (almost no move)
- γ: 0.025215 → **0.025601** (+1.5% relative)

**Conclusion:** Eliminating enclosure width at L≤12 does **not** approach 1.5×. The recipe ceiling with present M=12 data is ≈0.0256.

### (ii) Extra thermal at L=13,14 (float ED / Lanczos)

Method: per-Sz sparse Lanczos of `blocks.full_H` (NUMERICAL). Validated on L=10_I against thermal_arb midpoint (Z match to ~1e−12).

| L | twist | Z (float) | method | wall |
|---|---|---|---|---|
| 13 | I | 0.546336125522 | Sz-Lanczos k=100 | 471 s |
| 13 | P | 1.20302954116 | Sz-Lanczos k=100 | 470 s |
| 14 | I | ≈1.54036048 | partial sz≤2; higher Sz <1e−6 | killed ~585 s CPU |
| 14 | P | ≈0.86169234 | partial sz≤3 | killed ~581 s CPU |

Derived moments (NUMERICAL):
- J₁₃ ≈ 1.038856, \|N₁₃\| ≈ 0.164173
- J₁₄ ≈ 1.031359, \|N₁₄\| ≈ 0.169667

Packing uses `mn_up = |N|` (odd-L N is negative; using raw N under-counts contamination and falsely inflated γ to ~0.05 — corrected).

Caps U,V carried from L≤12 (conservative: adding L=13,14 constraints can only shrink the allowed spectral support, so U₁₂ remains a valid upper on U₁₃). Recomputing Hankel at length 13 hit a float-pilot bug and was not required for the conservative bound.

**Best with L=13:** γ ≈ **0.02706** at (M,n)=(13,32) ≈ **1.07×**.  
**L=14:** no further gain (≈1.02–1.03×).

### (iii) Re-optimized β₀, a, n

- **n:** Sweep 28..41 on ideal L≤12. Optimum remains **n=34** (γ=0.02560); n=32 is a close second. Outside {32,34} the chain collapses or weakens.
- **a:** Locked into the thermal definition Z=Tr exp(−β(H+aL)). Sweeping a without regenerating all Z is invalid; not used as a primary lever.
- **β₀:** With **frozen** moments (HEURISTIC), β₀=10 gives γ≈0.0308 (1.22×) — still below 1.5×, and real moments at β₀=10 would change S,T. Full re-thermal at new β₀ was not run (cost).

---

## Binding constraint

The chain is **T-limited**, not S-limited, once S ≳ 0.93:
- Current U−1 ≈ 1.34×10⁻³ ⇒ T ≈ 0.833 ⇒ γ ≈ 0.0252
- To hit γ ≥ 0.0378 at n=34, M=12 need **U ≤ 1.0010** (oracle), i.e. shave ~25% off (U−1)
- Ideal L≤12 caps barely move U; L=13,14 float moments improve S via larger M but leave U (hence T) stuck

So the ~0.0252 ceiling is a **U/T ceiling** of the present recipe, not an artifact of enclosure width or n choice.

---

## Moment no-go (Thm 3) vs this ceiling

From `runs/spin2/MOMENT_NOGO.md` Thm 3 (**PROVED** on spin-1 intervals):
- For M ∈ {6,7,8}, no certificate in the class proves S(32) > 1/√2 (bootstrap seed)
- For M=10, kills S(16)>1/√2 but not necessarily S(32)
- At M=12 the repo already has S(32) ≳ 0.93 (PROVED); Thm 3 does **not** predict a hard γ=0.0252 purity ceiling

**Relation to this pilot:** Thm 3 constrains **seed existence** at short M, not the γ achievable once a seed exists. Our float L=13 path (M=13) is outside Thm 3’s killed set. The barrier we hit is the **transfer-edge / T** bottleneck (U≳1.0013), which Thm 3 does not address.

Bogus high-γ signals at M≤7 in early sweeps were invalid: Hankel optimizer left U stuck at the init target 1.00139 (no real root). Discarded.

---

## Warrant certification? **NO**

| Criterion | Result |
|---|---|
| Best fair predicted γ | 0.02706 |
| ≥ 1.5 × 0.0252132 = 0.03782? | **NO** (only 1.07×) |
| Ideal L≤12 alone | 1.015× |
| L=13/14 thermal | 1.07× max |
| n / a / β₀ reopt (fair) | ≤1.22× and β₀ is HEURISTIC |

**Recommendation:** Do **not** start arb certification of L=13/14 or a re-seed for Option 2. The float pilot shows the existing heat-trace recipe, even with exact L≤12 data and float L=13/14 moments, stays within ~7% of the current bound. Beating 1.5× would require a materially smaller U (new filters / new criterion), not more of the same moments.

Cheap leftover if ever revisited: tighten Christoffel edge (U→1) with a different filter family — that is a new method, not “more seed data.”

---

## Files

```
runs/spin1_opt2/
  PILOT.md                 ← this file
  scripts/
    pilot_core.py          packing / chain / Hankel float core
    thermal_L13.py         dense Bloch Z (used for L≤10 validate)
    thermal_sz_sparse.py   per-Sz Lanczos Z (L=13,14)
    thermal_sparse.py      full-H Lanczos (L=10 validate)
    reopt.py               early n/M sweeps
  cache/
    phaseA.json            baseline + ideal L12
    pilot_final.json       full table dump
    eval_L13.json          L13-focused eval
    sz_L13_{I,P}.json      real L=13 Z
    sz_L14_{I,P}_partial.json
    thermal_L10_I.json
  logs/
    phaseA.log, reopt*.log, eval_*.log
    sz_L13_*.log, sz_L14_*.log, sparse_L10_I.log
```

---

## Labels recap

| Claim | Status |
|---|---|
| Float baseline γ ≈ 0.025215 matches certified recipe | NUMERICAL |
| Ideal L≤12 ⇒ γ ≈ 0.02560 | NUMERICAL |
| L=13 Z_I/P as tabulated | NUMERICAL (IEEE Lanczos) |
| L=14 Z from sz≤3 partial | NUMERICAL (trunc ≪ 1e−8) |
| Best fair γ ≈ 0.02706 < 1.5× threshold | NUMERICAL |
| U≤1.001 needed for 1.5× at M=12 n=34 | NUMERICAL (oracle) |
| Thm 3 does not imply the 0.0252 γ ceiling | PROVED (no-go) + HEURISTIC (link) |
| Certification warranted? | **NO** |
