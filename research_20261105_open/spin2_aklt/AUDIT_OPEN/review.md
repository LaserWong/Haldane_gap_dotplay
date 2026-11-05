# FOCUSED adversarial review: Lemma LM′ and CERT_OPEN (spin-2 AKLT open all-length gap)

Profile: **FOCUSED** (not paper-wide). Scope: CERT_OPEN.md §2 wrap-around steps 2–3; claim that LM Prop 4.6 never needs `n ≤ m/2`; certified inputs `μ`, `F_lo`, `G_up`; coverage of every `m ≥ 2`; trusted-base wording. Literature: Lemm–Mozgunov arXiv:1801.08915 (local `/workspace/papers/lm.{txt,pdf,html}`).

Read-only on CERT_OPEN.md. Auditor scripts/logs: `AUDIT_OPEN/auditor/` and `/workspace/audit_open_scratch/`. Snapshot: `AUDIT_OPEN/snapshot.json` (`snapshot_id` 7402a7df…).

**Overall verdict: the theorem STANDS. Bound and all-`m` coverage survive. No load-bearing proof error of the AUDIT_ALLM / GM-Lemma-4 kind. Minor exposition nits only.**

## Corrected / retained theorem

*Assume the IEEE-754 binary64 + Higham / E_build trusted base already stated in CERT_OPEN (same honesty as CERT_T0_ARB / post-audit CERT_ALLM). For every `m ≥ 2`, the open spin-2 AKLT chain `H_m = Σ_{i=1}^{m−1}(P3+P4)_{i,i+1}` has*

`γ_m ≥ 907760209/740162500000 ≈ 0.00122643`,

*with exact 9-fold null space for every `m ≥ 2` (two edge spin-1’s).*

Same bound and coverage as CERT_OPEN §0. No numerical change.

---

## Claim inventory (FOCUSED)

| ID | Claim | Role |
|---|---|---|
| C1 | Lemma LM′ (§2): for `m ≥ n ≥ 4`, if `C_M(e) ≤ q(1)` for all `2 ≤ e ≤ M−2` (`M=m+1`), then `γ_m ≥ F(μ_n − G)` with `F = c_0(Σc)/q(1)`, `G = (Σc²−q(1))/(c_0 Σc)` | load-bearing |
| C2 | Prop 4.6 extends to `m ≥ n` (bulk/edge `B² ≥ c_0 γ B`); proof does not use `n ≤ m/2` | load-bearing dependency |
| C3 | Wrap-around Knabe expansion (§2 steps 2–3): `Σ B²` coefficients are `C_M(e)`; adjacent cancel; `H²+βH ≥ α ΣB²` under `C_M` hyp | load-bearing |
| C4 | Exact `F`, `G`, `F_lo`, `G_up`, `bound_lo` at `n=8`; `C_M` for all `M ≥ 8` | load-bearing |
| C5 | `μ = 6261/50000 < γ_{n'}` for `n'=2..8`; `Σ kb = 3`; ker dim 9 | load-bearing |
| C6 | Every `m ≥ 2` covered (direct `m≤7`, LM′ `m≥8`) | load-bearing |
| C7 | Trusted base is IEEE+Higham/E_build, not full arb | wording |
| C8 | KHH(1) open corollary | **out of scope** (CERT_OPEN: not re-audited) |

---

## Finding F1 — Prop 4.6 / Def 4.2 stated with `n ≤ m/2`; extension is proof-inspection (exposition)

- **Kind:** exposition · **Severity:** minor · **Disposition:** confirmed · **refutes_claim:** false
- **Anchor:** LM Def 4.2 (lm.txt ~963), Prop 4.4 (~1041), Prop 4.6 (~1066); CERT_OPEN §2 step 4, §7 item 4.
- **Assertion:** The published statements literally require `n ≤ m/2`. CERT_OPEN’s claim that the *proof* of Prop 4.6 uses only `m ≥ n` is **correct** on inspection:
  - Bulk (i): needs nonempty `1 ≤ l ≤ m−n+1`, i.e. `m ≥ n`; then `B ≥ c_0 A` (Ass 4.1) and unitary equivalence of `A` to the open `n`-chain.
  - Edge (ii) + Lemma 4.7: sizes `m−l+1` and `l−2+n−m` lie in `{1,…,n−1}`; comparison to `γ^E_{n−1}` is by definition. No `m/2` step appears.
- **Consequence:** Not a proof gap. Recommend one explicit sentence: “We extend Def 4.2 / Prop 4.6 *verbatim* to all `m ≥ n`; the published `n ≤ m/2` is only the global hypothesis of Thm 2.5.”
- **Independent check:** spin-1 AKLT open, Prop 4.6 numerical margins for `n ∈ {4,5}` and `m ∈ [n,7]` (including `n > m/2`): **0 failures**; equal-weight bulk margins ~0 (tight), symmetric weights positive (`attack_lm2` / partial `attack_lm3`).

## Finding F2 — Wrap-around Knabe (LM′ steps 2–3) replaces Prop 4.4; no GM-Lemma-4 regression

- **Kind:** (positive check; no defect) · recorded as informational confirmation
- **Anchor:** LM App A (A.1)–(A.2), Autocorrelation Lemma A.1; CERT_OPEN §2 steps 2–3, §7 item 2–3; contrast AUDIT_ALLM Item 1.
- **Assertion:** Published Prop 4.4 / (A.2) indexes pairs by ring distance `d` with coefficient `q(d)`. That equals `C_M(d)` only when `q(M−d)=0`, which is guaranteed under `n ≤ m/2` but **fails** for some pairs when `n > m/2`. LM′ correctly upgrades the coefficient to `C_M(e)=q(e)+q(M−e)` and assumes `C_M(e) ≤ q(1)`. Adjacent cancellation `C_M(1)=q(1)` holds for `m ≥ n−1` because `q(M−1)=q(m)=0` when `m > n−2`.
- **Operator lower bound on windows:** CERT_OPEN uses the **valid** min-weight form `B² ≥ c_0 γ B` (LM Prop 4.6), **not** the false equal-weight / average-weight operator form that AUDIT_ALLM found in the GM′ draft. Step 5 then applies the operator inequality on a positive-energy eigenvector — legitimate here.
- **Independent checks:**
  - Knabe coefficient expansion: 26/26 match (`knabe_expand.py`).
  - Operator PSD: `λ_min(H²+βH−αΣB²) ≥ −1e-14` (num. zero) for spin-1, `n=4` weights, `m=4..7` (`attack_lm3`).
  - LM′ bound vs float gaps, spin-1, several weight families (eq/sym/ramp/edgeheavy), `n=4,5,6`, `m` up through 7 with `n>m/2`: **0 violations** (`attack_lm3`).

## Finding F3 — Exact rationals `F_lo`, `G_up`, bound — CONFIRMED

- **Kind:** numerical / calculation confirmation · **Severity:** informational · **Disposition:** confirmed
- Independently: `3524/769 < √21 < 6049/1320` (square test); `F_lo = 157497/192250`; `G_up = 1429/11550`; `μ=6261/50000 > G_up`; `F_lo(μ−G_up) = 907760209/740162500000` exactly. Matches `lm_prime.json` and CERT_OPEN §3.
- Float `F,G` from reconstructed LM weights at `n=8` match closed forms to `~1e-15`.
- Ass 4.1 (symmetry + mono to midpoint) and `c_j > 0`: hold on reconstructed weights.
- Autocorrelation `q(1)≥…≥q(6)`: witnesses in `lm_prime.json`; float mono confirmed.
- `C_M(e) ≤ q(1)` for `M=8..40`: 0 float failures; finite exact witnesses for `M=8..13` spot-checked (`M=8,e=2` witness identity verified by Fraction).

## Finding F4 — Certified inputs `μ` and kernel — CONFIRMED (IEEE base)

- **Kind:** numerical confirmation · **Severity:** informational · **Disposition:** confirmed
- All four `(R,F)` blocks CERTIFIED with `info=0` at `t=6261/50000` for `n=3,4,5,7` (Higham in `open/arb`) and `n=8` (Higham in `cert_t0/` + residual in `open/arb` and `cert_t0/arb`). **`Σ kb = 3`** in every suite checked (matches Sz=0 VBS multiplicity; total ker 9).
- Tighter direct certs `n=3..7` as in CERT_OPEN §0/§4: all CERTIFIED, `Σ kb=3`.
- Negctl direction: `n=7,t=1255/10000` fails in `(+−)`; `n=3,t=1605/10000` fails in `(+−)`. Matches CERT_OPEN.
- Residual rechecks `n=7,8`: all four blocks CERTIFIED (`method=residual_RTR_inv`).
- Float ED (`float_ed_open_3to10.json`): all `γ_m ≫ 0.001226`; `γ_9≈0.12007 < G(8)≈0.12372` explains maximal useful `n=8` (NUMERICAL).

## Finding F5 — Trusted-base wording — CONFIRMED honest

- **Kind:** exposition · **Severity:** informational · **Disposition:** confirmed (no edit required)
- CERT_OPEN header already states IEEE-754 binary64 + Higham/E_build + Fraction/sympy, **not** full arb. Avoids the CERT_ALLM wording bug. Filenames `cert_arb_*` remain slightly misleading (residual path, not ball arithmetic) but the prose is accurate.

## Finding F6 — Coverage of every `m ≥ 2` — CONFIRMED

- `m=2`: trivial projector gap 1.
- `m=3..7`: direct certs ≫ bound.
- `m≥8`: LM′ at `n=8` with verified `C_M` and `μ > G_up`.
- `m=7` correctly **excluded** from LM′ (no bulk window at `n=8`); covered by direct cert.
- Published LM Rem 2.6 recovers `m≥16` as the special case `n≤m/2`.

## Finding F7 — Minor clarity: `n=6` residual sample incomplete in `open/arb`

- **Kind:** exposition · **Severity:** informational · **Disposition:** confirmed · **refutes_claim:** false
- `open/arb` has residual JSON only for `n=6` blocks `(+,+)` and `(−,−)`. Load-bearing Higham certs for all four blocks live under `cert_t0/`. CERT_OPEN’s citation of CERT_T0 for `n=6` is correct; a reader looking only in `open/arb` might think two blocks are missing. Optional: copy or symlink the other two residual files, or say explicitly “`n=6` residual sample is two blocks; full Higham suite in `cert_t0/`.”

---

## Attacks that did **not** break the theorem

| Attack | Result |
|---|---|
| Use false GM Lemma 4 average-weight operator form | Not present in CERT_OPEN; min-weight `c_0` used |
| Prop 4.6 fails for `n > m/2` | No numerical failure on spin-1; proof text OK |
| Knabe PSD fails under wrap-around | PSD within `1e-14` when `C_M` holds |
| LM′ bound exceeds true gap (spin-1 cex) | 0 violations in tested suite |
| `C_M` fails for author weights `M≥8` | 0 failures through `M=40` |
| Bound arithmetic / convergent error | Exact match |
| `Σ kb ≠ 3` or CERTIFIED false at `μ` | All OK |
| Negctl certifies above float gap | Correctly fails |
| Apply LM′ at `m=7` | Author correctly refuses |

Limits of cex search: spin-1 open chains only through `m=7` (dim `3^7`); spin-2 dense Prop 4.6 at large `m` not re-run (author float ED + certs used). No theorem falsifier found in range.

---

## Decision

- **Outcome:** `no_blocker_found_in_checked_scope`
- **Coverage:** complete for FOCUSED requested scope (C1–C7). C8 KHH corollary not assessed.
- **Recommendation:** Accept Lemma LM′ and Theorem T_OPEN at the stated bound on the declared IEEE trusted base. Optional minor wording edits (F1, F7). **Do not** change the bound. Proceed to adversarial-repair edits only if desired for exposition; then sync / new PR as previously planned.

## Required edits to CERT_OPEN.md (optional, non-blocking)

1. §2 / §7: one sentence that Def 4.2 is extended verbatim to `m ≥ n`, and that `n ≤ m/2` in LM is the Thm 2.5 hypothesis, not a Prop 4.6 proof ingredient (F1).
2. §4: clarify `n=6` residual sample vs full Higham suite location (F7).

Not audited: open KHH(1) corollary; full arb-ball certificates beyond residual rechecks; infinite-volume statements beyond the uniform finite-`m` bound.
