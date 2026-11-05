# No-go deposit: fuzzy MPS and A2 upper-bound leads

Date: 2026-11-05 America/Chicago. Labels: PROVED / FLOAT / ESTIMATE / FAIL.

## Bottom line

| Route | Verdict | Pointer |
|---|---|---|
| Fuzzy Story A — compress-then-square MPS → Z upper (A2) | **FAIL** | `fuzzy_mps/T1_RESULTS.md` |
| Fuzzy Story B — naive AKLT parent → pure Heisenberg (B4) | **FAIL** | `fuzzy_mps/T2_RESULTS.md` |
| A2 lead (i) Collatz–Wielandt / local positive vectors | **FAIL** (prior) | `spin2_a2/CW_SPIN1_TEST.md` |
| A2 lead (ii) SDP / MED / LTI free-energy | **FAIL** (prior) | `spin2_a2/LEAD2_PAPERCHECK.md` |

Obligation map and combined note: `fuzzy_mps/OBLIGATIONS.md`, `fuzzy_mps/SUMMARY.md`.

## What this does / does not kill

- **Killed for proving pure Heisenberg (esp. spin-2):** bare MPS thermal truncation with a-priori error, AKLT→Heisenberg gap transfer, CW and SDP/MED as scalable Z uppers.
- **Alive / already proved elsewhere:** spin-1 thermal bootstrap (Opt1 deposit); spin-2 **AKLT** all-length periodic and open gaps (CERT_ALLM / CERT_OPEN). Exact-MPS parents still work.
- **Untouched:** a non-AKLT fuzzy parent of Heisenberg with a new coupling theorem; heroic spin-1-only Kull-type f_∞ (still converts poorly to Z_L).

## T1 in one paragraph

On spin-1 L=6/8, a TEBD / squaring ladder with truncation needs χ near a large fraction of full middle-cut rank before even the circular (exact-operator) η clears bootstrap slack. Non-circular a-priori η fails everywhere tested. Squaring amplifies relative error by ~10³ at L=8 and ~10³⁸ at L=256 (ESTIMATE), so a Xiao-style 1e-12 first-step loss misses the a-priori budget by ~28 decades.

## T2 in one paragraph

Best ‖H_Heis − c H_AKLT − αI‖ at L=8 is r≈2.45 vs γ_AKLT≈0.35 (ratio ~7). Local bond residual after matching S·S is exactly 1/2 > γ_AKLT. Stability only looks plausible in a thin BB neighborhood of AKLT.

## A2 leads in one paragraph

Local CW certificates are capped by min_p E0(p)/p (best certified error ~0.035/site). SDP/MED/LTI hit the same ring ceiling (Kull et al. saturate it); f_∞ → Z_L conversion has useless slack or needs W≈L.

## Artifacts

- `fuzzy_mps/`: scripts, T1/T2 results JSON, `results/` (no 507 MB `cache/`)
- `spin2_a2/`: CW_SPIN1_TEST, LEAD2_PAPERCHECK, `cw/` certificates
