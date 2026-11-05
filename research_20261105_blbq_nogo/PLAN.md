# Spin-2 BLBQ near AKLT: pivot plan (2026-11-05, America/Chicago)
Labels: PROVED / NUMERICAL (float, uncertified) / HEURISTIC.

## 1. Model
KHH(α) (runs/spin2_aklt/ed.py): h = x + α(2/9 x² + 1/63 x³ + 10/7), x = S_i·S_j (spin 2).
α=1: 10(P3/7+P4) = AKLT parent (VBS ξ = 1/ln((S+2)/S) = 1/ln2 ≈ 1.44, standard result); α=0: Heisenberg (ξ≈49.5).
"Near AKLT" target: ξ ≲ 5 ⇒ HEURISTIC window α ∈ [0.8, 1). ξ(α) is NOT yet measured (gap L≤8 ED is
even/odd-oscillating and not converged: α=0.8 Δ_8≈0.184, α=0.9 0.147, α=1 0.156; NUMERICAL, ed_KHH_*_3-8.json).

## 2. Obligation map (spin-1 pipeline → spin-2 BLBQ)
| spin-1 input | role | spin-2 BLBQ status |
|---|---|---|
| THEORY eq.13: Z_L = Tr X^L, X real self-adjoint HS, ∀L≥2 | LOAD-BEARING (all moment/positivity steps) | sufficient construction FAILS ∀α∈(0,1], every real structure (PROVED, spin2_aklt/SCOPING §3). QTM has stable complex multiplets at α∈{0.9,1}, |λ/λ0|≈0.05–0.15 (NUMERICAL, QTM_TEST.md) ⇒ eq.13 likely FALSE near AKLT. Absent (top-24/60) at α≤0.5. **Debt D1.** |
| rigorous two-sided Z_L up to L≈2ξ (spin-1: L=12, ξ=6) | load-bearing | needs L≈8–10 at ξ≲5: 5^10≈9.8e6 sector-ED, feasible (HEURISTIC) |
| seed S(n)>1/√2 (spin-1 n=34≈5.6ξ, 2n=68 via Hankel) | load-bearing | n≈28 at ξ=5 (HEURISTIC scaling) |
| β0 with βΔ≈5, T(β) bound | load-bearing | β≈25–35 (Δ≈0.15–0.2, NUMERICAL-ish) |
| anchors / window certificate (seal12, audit_scalar) | mechanical | re-run with new data once above exist |
| MOMENT_NOGO ρ_m<1 condition | gate | must recheck ρ_8, ρ_10 for KHH(α) (not done) |

## 3. Cheapest discriminating test (stated, not run)
Test D1-window: for α ∈ {0.6, 0.7, 0.8}:
 (a) ξ(α) from iDMRG/VUMPS (float, minutes);
 (b) QTM spectrum (qtm/qtm.py, N=2,3, β=2,4) — any complex multiplet in top-60?
YES (pivot alive) iff ∃α with ξ≲5–6 AND no complex QTM eigenvalues (consistent with eq.13).
NO iff complex multiplets appear wherever ξ≲6 → spin-1 pipeline cannot be reused as-is; need new theorem
(bootstrap tolerating a complex tail bounded by |r|^L — HEURISTIC fix, unproved) before any Z work.
Secondary (only if YES): exact sector ED at L=9,10 for that α and check ρ_m<1 (MOMENT_NOGO criterion).

## 4. Not done / no weaker silent method
No Z enclosures computed. No claim that T0 (GM bound, CERT_*) extends to α<1 — that is a separate,
stability-type route (T2 for Heisenberg failed; for α near 1 the local residual is O(1−α), so GM/Knabe at
α≈0.9 is a plausible *alternative* certified route, HEURISTIC).

**Discriminator result (2026-11-05): NO, see DISCRIMINATOR.md.** ξ≲6 only for α≳0.92, where the QTM top 60 has complex multiplets; α≤0.8 is real but ξ>9.

**Local-gap route for α<1 (2026-11-05): NO, see LOCAL_GAP_PLAN.md** (KHH(α<1) is frustrated; GM/Knabe need frustration-free).
