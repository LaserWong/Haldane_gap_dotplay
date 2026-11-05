# Fuzzy MPS discriminating tests — summary

Date: 2026-11-05 America/Chicago.

| Test | Question | Verdict |
|---|---|---|
| **T1** | Is compress-then-square MPS a non-circular route to rigorous Z **upper** bounds (A2)? | **NO** |
| **T2** | Can naive AKLT-parent transfer close a pure-Heisenberg gap (B4)? | **NO** |

Details: `T1_RESULTS.md`, `T2_RESULTS.md`, `OBLIGATIONS.md`.

## What survives

- **Story A interface** still works when Z intervals are obtained some other way (exact ED, ALT when tractable, CW/SDP research leads). Bare MPS truncation + a-priori squaring amplification does **not** supply A2; Xiao-style 1e-12 first-step loss at L~256 misses a-priori budget by ~28 decades (ESTIMATE).
- **Story B near AKLT** (small BB deformation) remains open/expensive; pure Heisenberg via AKLT parent is dead. A *non-AKLT* fuzzy parent of Heisenberg (Xiao’s claimed path) is untouched by T2 — still needs B4 for that parent.
- Spin-1 Opt1 deposit and spin-2 AKLT certificates are unaffected.

## Recommended next (not started)

1. If pursuing Story A: Collatz–Wielandt + MPS test vector on spin-1 L=12 (FEASIBILITY lead i) — cheap viability check for A2 without truncation ladders.
2. If pursuing Story B: demand Xiao’s parent definition + coupling estimate; do not spend compute on AKLT→Heisenberg transfer.
3. Otherwise: Option 3 PROOF.md for spin-1, or leave fuzzy parked.

## A2 follow-up (2026-11-05)

User asked to pursue A2. Checked prior work instead of re-running:

- **Lead (i) CW** (`runs/spin2/CW_SPIN1_TEST.md`): already **FAIL**. Translation-invariant local CW certificates are capped by min_p E0(p)/p; best certified μ = −1.436… (error 3.5e-2/site); 1e-6 needs W≳47 (infeasible). CW also does not give a usable Z_L upper.
- **Lead (ii) SDP/MED** (`runs/spin2/LEAD2_PAPERCHECK.md`): already **FAIL** for the proof. Same ring ceiling; Kull et al. saturate it; f_∞→Z_L conversion has useless slack or needs W≈L.

So A2 via the FEASIBILITY research leads is parked. Remaining A2 options are not cheap viability tests.
