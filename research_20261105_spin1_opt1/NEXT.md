# Spin-1 Haldane gap: state and next moves (screened Nov 5, 2026, America/Chicago)

Sources: runs/proof_audit/PROOF_CHAIN.md, runs/watertight/WATERTIGHT_STATUS.md, runs/push_bound/STATUS.md,
runs/thermal_arb/STATUS.md, runs/seal12, runs/a_uniform, runs/b_n8_rigorous_arb, runs/open_claims/STATUS.md,
repo LaserWong/Haldane_gap_dotplay @ a99fa21. Upstream PR list (checked live): LaserWong #2-#8 all OPEN, none merged
(#2 n=8 arb exclusion, #3 watertight transfer, #4 open claims + pushed bounds, #5 proof audit + thermal arb, #6-#8 spin-2).

## 1. Current status
Theorem: H_L = sum S_i.S_{i+1}, spin 1, periodic, full Hilbert space. For every L >= 2 the ground state is unique and the gap is at least gamma.

| gamma | logic | status |
|---|---|---|
| 2497/100000 = 0.02497 | repo checker, Z>1 mode, W=12 | PROVED (computer-assisted). Also independently re-derived in exact rationals (a_uniform/cert12.py) |
| 25177/1000000 = 0.025177 | FULL mode (Jensen bound for Z_2n, patched checker), W=12 | PROVED. Patched checker reviewed; independent cert12.py also passes |
| 1/40 = 0.025 | ORIGINAL logic, W=15 | PROVED (repo checker only) |
| 250057/10^7 = 0.0250057 | ORIGINAL, W=17, CPU cap raised 60 -> 590 s (resource-only edit) | PROVED (repo checker only) |
| 63033/2500000 = 0.0252132 | FULL, W=17 | PROVED (patched checker only); best certified |
| ~0.025007 / ~0.025214 | recipe ceilings as W -> infinity | HEURISTIC (extrapolated). More windows gain at most ~1e-6 |
| ~0.4105 | true gap (DMRG literature) | NUMERICAL |

Also PROVED: the transfer identity, the V4 twist/sector lemma (closes the "inherits" gap in step 5), and the
thermodynamic-limit statement 16b: every weak-* limit of the periodic ground states has a simple vacuum and gap >= gamma.

Trusted base (after thermal_arb): CPython ints/Fractions; python-flint/arb; the repo audit scripts (read line by line);
hand lemmas (packing, G-recursion, window, tail, purity => gap, Cauchy-Schwarz at L=25, V4, the limit argument with
Bratteli-Robinson and Nelson); and **IEEE-754 binary64 BLAS/scipy for the 54 L=12 float-mode blocks (Sz=0..3)**
in the thermal enclosures, using a-priori Higham bounds and assuming no Strassen. That case is the tightest:
radius 1.5e-6 against a margin of 6.9e-6. The producer's C++ Horner kernel is **no longer trusted**, and the MPS anchors were reproduced exactly with FLINT.

## 2. Open items and weaknesses
- **Bound strength:** the certified bound is about 6% of the true gap (0.0252 vs about 0.41), and the recipe is saturated. A back-of-envelope estimate (HEURISTIC): e^{-beta0*gamma} = (1-C)/C gives C ~ 0.58 at the first window (n=34, beta0=49/4). So the bound is limited by **seed purity**, not by window count. The forcing margin R_68 ~ -8.3e-6 is also razor-thin.
- **Trusted base:** IEEE float for the 54 L=12 blocks is the only non-arb numerical item that the theorem relies on. (The n=8 exclusion's IEEE limb arithmetic is not load-bearing for the gap.)
- **Checker provenance:** the W=17 pushed values rest on a single checker, with a CPU-limit edit (ORIGINAL) or new checker code (FULL). The independent exact re-derivation only reaches W=12 (0.02497 / 0.025177).
- **Seals and resources:** the SHA-256 seals fail on a fresh HEAD checkout, because .md files were edited after sealing (code is identical). The direct-25 review has a resource anomaly (26 s CPU against a 15 s cap); it is not mathematical.
- **Uniqueness in infinite volume (16c):** NOT PROVEN, and not claimed. This covers uniqueness among all infinite-volume ground states, convergence of omega_L, and purity. Closing it is research-level, because Heisenberg is not frustration-free.
- **Length coverage:** periodic chains are covered for all L >= 2 (PROVED). Open chains are not covered (spin-1/2 edge states; nothing is claimed).
- **Exposition:** the proof is spread across about 6 deposits and 4 unmerged upstream PRs. There is no single human-readable theorem plus proof plus trusted-base document.

## 3. Ranked next options (by rigor gain per effort)

### Option 1: Close the trusted base to arb-only and seal the headline (recommended first)
- **Goal:** the headline gap is PROVED with no IEEE assumption, and the result is confirmed by two independent checkers.
- **Method:**
  - (a) Re-certify the 54 float-mode L=12 blocks in exact or ball mode. Add SU(2) highest-weight plus reflection reduction so that every block has m <= 3000, then reuse the existing exact fmpz residual path. Alternatively, use chunked arb_mat products under the 600 s/process limit.
  - (b) Pick a headline that has two independent checks: 25177/1000000 (FULL) or 2497/100000. Then either extend a_uniform/cert12.py to W=15-17, or state that the extra 4e-5 is single-checker. Don't compute the W=18 digits (gain at most 1e-6).
  - (c) Re-seal at HEAD, and re-run direct-25 under its cap.
- **Effort:** about 1 day of agent time. The arb rerun of the L=12 blocks was about 3 CPU-h before.
- **Payoff:** the trusted base becomes FLINT/arb + CPython + hand lemmas. Exact mode was 500-2000x tighter than float mode, so the 6.9e-6 margin passes easily (HEURISTIC).
- **Blockage risk:** low. The SU(2) reduction code is new and needs the same dimension, trace and moment cross-checks.

### Option 2: Seed-strength pilot, then (if it pays) a bigger bound
- **Goal:** find out whether the bound can move well beyond the 0.0252 ceiling, and what drives it.
- **Method (pilot):** use float data only, through the untrusted producer. Replace the n=34 seed inputs by:
  - (i) ideal (exact-spectrum) caps from the L <= 12 data;
  - (ii) extra twisted and untwisted thermal moments at L=13 and 14, via SU(2) highest-weight blocks (the S=0 sector at L=14 is about 30k states, a few thousand per momentum);
  - (iii) re-optimized beta0, a and n.

  Report the gamma each variant would give. Only if a variant gives >= 1.5x, certify that variant: arb thermal enclosures at L=13 and 14, plus Hankel filters extended to degree 14.
- **Effort:** the pilot takes about 0.5 day. Certification, if warranted, takes 2-4 days.
- **Payoff:** unknown (HEURISTIC). With the same first-window formula, tripling gamma to about 0.075 needs C of about 0.72 (from about 0.58), and C = 0.9 would give about 0.18.
- **Blockage risk:** medium-high. The moment no-go Thm 3 shows that low-L data provably cannot certify strong seeds at moderate n, and that obstruction may persist at L=14. The pilot exists to detect this cheaply before any rigorous spend.

### Option 3: Consolidated proof document plus one superseding upstream PR
- **Goal:** one self-contained PROOF.md that LaserWong and referees can check. It would contain:
  - the theorem, with its exact scope (periodic, finite L, plus 16b);
  - the 16-step chain, with every hand lemma written out (V4, the limit argument, window and tail);
  - the trusted-base table and replay commands.

  It would ship as a new fork PR that references #2-#5.
- **Effort:** about 0.5-1 day. Mostly writing, with an adversarial read-through.
- **Payoff:** an exposition and reviewability gain. It is the step needed before anyone merges, or before a paper.
- **Blockage risk:** low. It is best done after Option 1, so the document states the final trusted base.

Not recommended now:
- 16c (infinite-volume uniqueness): research-level, no cheap route.
- Open-chain spin-1 gap: a different theorem, with edge states.
- More windows (W >= 18): at most +1e-6.

## 4. Recommendation
Do Option 1 now, and run Option 2's float pilot alongside it, since it is cheap and separate. Then write Option 3 as one
consolidated PR. Commit rigorous effort to a bigger bound only if the pilot shows a >= 1.5x gain.
