# AUDIT_OPEN: hostile audit of CERT_OPEN.md (Lemma LM′ and the all-length spin-2 AKLT open-chain gap)

Auditor scripts and logs: `AUDIT_OPEN/auditor/` (and scratch `/workspace/audit_open_scratch/`). Independent bond/ED/exact arithmetic and counterexample search where feasible; author cert JSONs spot-checked for `kb` / `CERTIFIED` / negctl. Literature: Lemm–Mozgunov arXiv:1801.08915 read from `/workspace/papers/lm.txt` (Prop 4.4, 4.6, App A, Rem 2.6). Full FOCUSED record: `AUDIT_OPEN/{review.md,review-record.json,snapshot.json}`.

**Overall verdict: the theorem STANDS. Bound unchanged. No load-bearing proof gap.**

## Retained theorem
*Assume the IEEE-754 binary64 + Higham / E_build trusted base already stated in CERT_OPEN. For every m ≥ 2, the open spin-2 AKLT chain H_m = Σ_{i=1}^{m−1}(P3+P4)_{i,i+1} has gap*

γ_m ≥ 907760209/740162500000 ≈ 0.00122643,

*with exact 9-fold null space for every m ≥ 2.*

Same statement as CERT_OPEN §0. Coverage: m=2 trivial; m=3..7 direct certs; m≥8 Lemma LM′ at n=8.

## Item 1: Lemma LM′ vs LM 1801.08915 (Prop 4.4, 4.6, App A). Verdict: CONFIRMED (with minor exposition nit)

**Wrap-around (CERT_OPEN §2 steps 2–3).** Published Prop 4.4 / (A.2) uses coefficient q(d) at ring distance d. That equals C_M(d) only when q(M−d)=0, which holds under the published n ≤ m/2 but not always for n > m/2. LM′ correctly replaces the coefficient by C_M(e)=q(e)+q(M−e) and assumes C_M(e)≤q(1). Adjacent cancellation C_M(1)=q(1) holds for m ≥ n−1. Independent Knabe expansion (26/26 coeffs) and operator PSD checks on spin-1 (m=4..7, n=4 weights) confirm H²+βH ≥ α ΣB² when the hypothesis holds.

**Prop 4.6 without n ≤ m/2.** Def 4.2 / Prop 4.6 are *stated* with n ≤ m/2. The proof uses only: nonempty bulk range m ≥ n; Ass 4.1 (c_j ≥ c_0 ⇒ B ≥ c_0 A); frustration-freeness; edge size ≤ n−1. CERT_OPEN’s proof-inspection claim is correct. Nit: say explicitly that Def 4.2 is extended verbatim to m ≥ n.

**No GM-Lemma-4 regression.** Window lower bounds use the valid min-weight factor c_0 (LM Prop 4.6), not the false average-weight operator form that AUDIT_ALLM found in the GM′ draft. Step 5 on a positive-energy eigenvector is then legitimate.

**Cex search.** Spin-1 AKLT open, n=4,5,6, several weight families, m in [n,7] (mostly n > m/2): LM′ bound never exceeds the float gap (0 violations). Prop 4.6 numerical margins: 0 failures.

## Item 2: exact F, G, C_M, bound. Verdict: CONFIRMED
Independent Fraction arithmetic: F_lo = 157497/192250, G_up = 1429/11550, bound = **907760209/740162500000** exactly. Convergents 3524/769 < √21 < 6049/1320 verified by squares. Ass 4.1 and q-monotonicity hold on reconstructed LM n=8 weights. C_M(e)≤q(1) for M=8..40: 0 float failures; M=8 e=2 witness identity checked exactly.

## Item 3: certified μ and kernel. Verdict: CONFIRMED (IEEE base)
For n'=3,4,5,7,8 at t=6261/50000: all blocks CERTIFIED, **Σ kb = 3**. Tighter m=3..7 certs likewise. Negctl: n=7 t=1255/10000 fails in (+−); n=3 t=1605/10000 fails in (+−). Residual rechecks n=7,8 CERTIFIED. Float ED m=3..10 all ≫ 0.001226; γ_9≈0.12007 < G(8) explains why n=8 is maximal useful (NUMERICAL).

## Item 4: trusted base. Verdict: CONFIRMED honest
CERT_OPEN already says IEEE-754 + Higham/E_build, not full arb. No wording fix required (unlike CERT_ALLM).

## Item 5: all-m coverage. Verdict: CONFIRMED
No uncovered m. m=7 correctly refused for LM′ (no bulk window at n=8) and covered by direct cert.

## Optional edits to CERT_OPEN.md (non-blocking)
1. §2/§7: one sentence that Def 4.2 extends verbatim to m ≥ n; published n ≤ m/2 is Thm 2.5’s global hypothesis, not a Prop 4.6 proof step.
2. §4: note that n=6 residual sample in `open/arb` is two blocks; full Higham suite is in `cert_t0/`.

Not audited: open KHH(1) corollary; full arb-ball certificates beyond residual rechecks.

**Next (for parent / user):** optional exposition edits → sync `HaldaneGap_spin2_open.tgz` (or similar) to the Mac → new fork PR for open-chain + this audit. Do not change the bound.
