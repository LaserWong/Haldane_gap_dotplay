# Local-gap (Knabe / Gosset–Mozgunov) certificate for KHH(α<1): plan + discriminator (2026-11-05, America/Chicago)
Labels: PROVED / NUMERICAL / HEURISTIC. Sources: spin2_aklt/CERT_T0.md, CERT_ALLM.md (Lemma GM′), SCOPING.md, ed.py.

## Verdict: **NO** (structural, before any ε_n numerics)
Every local-gap theorem the repo uses (Knabe; GM Thm 3; GM′; Lemm–Mozgunov eq. 4.16) **assumes frustration-freeness**
(CERT_T0 §1 hypotheses, and the division by ε > 0 in CERT_ALLM step 4). KHH(α) is frustrated for every α∈[0,1).
So "ε_n(α) vs threshold" is not defined in a way that gives a gap; there is no threshold to clear.

## 1. Frustration (PROVED + NUMERICAL), ff_check.py / ff_check.log
Bond spectrum of h_α in J=0..4: h_α = x + α q(x), x = (J(J+1)−12)/2.
- α=1: (0,0,0,10/7,10) → bond ground space = J≤2, VBS lies in it on all bonds: frustration-free (known).
- α<1: J=0,1,2 split: α=0.95 → (−0.30, −0.25, −0.15, 1.357, 9.7); α=0.9 → (−0.60, −0.50, −0.30, 1.286, 9.4) (exact rationals by formula).
  The bond ground space is the J=0 singlet alone. A state with a singlet on both bonds (1,2) and (2,3) does not exist
  (the reduced state of site 2 would have to be maximally entangled with both 1 and 3, which is impossible). So for L≥3, E0 > L·min(h): **PROVED frustrated ∀α∈[0,1)**.
- Size (NUMERICAL, L=8 periodic ED): E0/site − min(h) = 0.068 (α=0.95), 0.132 (α=0.9). This is about the size of the gap itself (Δ_8≈0.14–0.15), not a small perturbation.

## 2. What would have to change (obligation map)
| GM/Knabe input | α=1 | α<1 |
|---|---|---|
| projector (or ≥0) terms with common kernel | ✓ | ✗ (shift h−min h ≥0 but no common kernel) |
| ε_n = smallest nonzero eigenvalue of open H_n, ground space = kernel | ✓ | ✗ ground space of open H_n is not the restriction of the global one |
| step "ε²+βε ≥ … ⟹ ε ≥ F(ε_n−G)" | uses H≥0, GS energy 0 | breaks: needs H−E0 with E0 unknown, nonlocal |
| P3/P4 weights (min(a3,a4)) | ✓ | not applicable: J=0,1,2 split |

## 3. Routes that are NOT silently substituted (owner decides)
- (R1) Stability of FF gapped phases (Michalakis–Zwolak; Bravyi–Hastings–Michalakis): rigorous but constants are non-explicit/very weak in practice; to give a number at 1−α = 0.1 would be a research project. HEURISTIC: unlikely to reach α=0.9.
- (R2) Explicit perturbation bound around AKLT: H(α) = c·H_AKLT + (1−α)V, needs ‖local V‖ ≲ gap fraction. Here (1−α)·‖V_bond‖ ≈ 0.6 at α=0.9 vs certified AKLT gap 0.06: fails by ~10× (HEURISTIC, crude). Maybe α ≳ 0.99 only.
- (R3) Find a different frustration-free parent in the same phase with weaker ξ: already done (VBS parents aP3+bP4, CERT_T0 covers them); that does not certify KHH(α<1) itself.

## 4. Status
- No all-m certificate started. No ε_n(α) "pseudo-threshold" run, since it would be a weaker method without a theorem.
