# Proof-chain audit: spin-1 periodic Heisenberg chain, gap >= 2497/100000 for all L >= 2

Repo: LaserWong/Haldane_gap_dotplay @ a99fa21 (untouched; nothing pushed; user's Mac not touched).
Paths below are relative to `research_20261010/` unless they start with another top-level directory.
Audit artifacts are in this directory (`runs/proof_audit/`).

## 0. What is claimed
- H_L = sum_{i=1}^{L} S_i.S_{i+1} (periodic, S_{L+1}=S_1), with spin 1, on (C^3)^{⊗L}.
- Δ_L = E_1 − E_0 in the full Hilbert space, with no symmetry sector restriction.
- **Claim:** for every L >= 2, the ground state is unique and Δ_L >= γ := 2497/100000.
- **Provenance of γ:** the repo itself certifies 31/1250 = 0.0248 (`uniform_gap_0248_all_sizes_review`). The value 2497/100000 is this bundle's 12-window rerun of the same n=34 chain (`runs/seal12`).
  - That rerun was ACCEPTED by the repo's own `audit_scalar.py` and all-sizes `audit.py`, in the Z>1 mode.
  - The only edits were plumbing: env-selectable certificate, gap, output and rounding grid B. The diff is in `seal12/auditor_changes.diff`.
  - In Z>1 mode the mathematical checks are byte-identical to the repo's.

Constants: a = 700741/500000, β0 = 49/4, Z_L(β) = Tr e^{−β(H_L + aL)}.

## 1. The chain

| # | Step | Status | Where / what it trusts |
|---|---|---|---|
| 1 | **L=2:** H_2 = S²−4, levels −4, −2, 2; unique ground state, gap 2. **L=3:** H_3 = (S²−6)/2, S = 0,1,2,3 with multiplicities 1,3,2,1; unique ground state, gap 1. | PROVEN (by hand, rechecked) | `uniform_small_lengths_completion_review/PROOF.md` |
| 2 | **Gap from purity.** Let w_i be the Gibbs weights and p = Σ w_i² ≤ w_max. If p ≥ C > 1/2, then w_max > 1/2, so the ground state is unique (a degenerate ground state would have weights ≤ 1/2). Also e^{−βΔ} ≤ (1−w_0)/w_0 ≤ (1−C)/C. So Δ ≥ γ whenever C − e^{βγ}(1−C) > 0, which is the audited "margin". Even and odd L are treated identically, in the full space. | PROVEN (written; repo PROOF files; rechecked) | margin lines in `uniform_gap_0248_all_sizes_review/audit.py` |
| 3 | **Variational numerators.** For any nonzero trial ψ, Z_L(2β) ≥ e^{−2βR_L}, where R_L = ⟨ψ,Hψ⟩/⟨ψ,ψ⟩ + La (by Jensen / the variational principle). The trial states are D=26 MPS anchors with H0_L, N0_L for L = 4..33, 48, 60, 64, 68. | PROVEN + PROVEN-BY-COMPUTER | Repo: sequential GMP contraction. **Independently recomputed by me** with an exact FLINT integer transfer matrix (`mps_anchor_check.py`): all 33 (H0, N0) pairs match exactly (`compare_anchors.json`). |
| 4 | **Transfer identity.** Z_L(β) = Tr X_β^L, with X_β a real symmetric Hilbert–Schmidt operator on bond histories (Dyson/Poisson expansion, S·S' = −Σ A_α⊗A_α, A_α real antisymmetric). Holds for all L ≥ 2. | PROVEN | `watertight/transfer_operator.md` (checked). It covers only untwisted Z_L. |
| 5 | **Twisted traces and sectors:** J_L = (Z_L + 3P_L)/4, N_L = (Z_L − P_L)/4, Z_L = J_L + 3N_L, where J and N are L-th power traces of two self-adjoint pieces X_0 and X_x of X. | Repo: STATED-WITHOUT-PROOF ("inherits"; `heat_trace/audit_inputs/APPENDIX_A_BRIDGE.md:23–35`, thermal PROOF). **GAP → CLOSED** by me (§2.1). | Hand derivation |
| 6 | **Thermal inputs.** 18 two-sided intervals for Z_L and P_L, L = 4..12, at β0. The P seam is the closing bond with S_x, S_y sign-flipped (π-rotation about z). Method: F = exp[98(R−I)] with R = (32 − 3L − 2H)/32. This gives ‖F‖_F² e^{(49/4)L(3/2 − a)} = Z, with ‖R‖ ≤ 1 for L ≤ 12 by H ≥ −3L/2 (three-site bound S_m·(S_l+S_r) ≥ −3, also valid at the twisted seam). Integer Horner with Poisson weights of degree 280, Q = 2^55, column error E_L = 281(d_L+1)+1, and Taylor degree 100 for e^x. | PROVEN-BY-COMPUTER | **Trusts the producer's C++ integer kernel** for every per-orbit norm² (no reviewer recomputes them), plus its int64/int128 guards. The reviewer rebuilt the matrices and orbit coverage and re-derived W → [lo, hi] exactly. **Replayed by me:** `check_matrices.py` PASS; `check_provenance.py` ACCEPTED; `check_completed.py` "PASS W/identity/coverage/enclosures" for all 18, though it then aborts at a campaign-ledger file-binding check (absolute path, accounting only). **Cross-checks (not proof):** an arb enclosure of Z8 and Z12 contains/intersects the repo intervals. A float64 dense ED (`sanity_thermal_float.py`) puts all 14 cases L = 4..10, I and P, inside the repo intervals; this also confirms the twist convention. |
| 7 | **Moment intervals and caps.** J, N moments for k = 4..12 come from step 6 via step 5. Hankel/Christoffel square filters give the support caps −0.6501774659 < λ_J < 1.0013390453 and −0.8710299903 < λ_N < 0.7502278231, plus the cap values B for the sectors. | PROVEN-BY-COMPUTER (exact rationals) | `uniform_second_moment_optimization/PROOF.md`; `uniform_second_moment_review/audit.py` **replayed by me: "CONDITIONALLY ACCEPTED"** (13.6 CPU s). The condition is the physical inputs, which step 6 discharges. |
| 8 | **Signed majorants.** Bernstein/de Casteljau: x⁴p(x) ≥ x^k on the closed caps, with odd orders kept signed. **Packing lemma:** for 0 ≤ y_i ≤ h, Σy_i ≤ m and r ≥ 1, Σ y_i^r ≤ pack(m, h, r), by Karamata. | PROVEN (lemma) + PROVEN-BY-COMPUTER (instances) | moment PROOF.md:78; `uniform_smaller_second_initialization_review/audit_scalar.py` (line-by-line sound) |
| 9 | **Dominant atom and seeds at n=34.** Forcing: if no eigenvalue of X_0 exceeded ell, packing would give Z_68 < 1, contradicting step 3 (R_68 < 0 ⇒ Z_68 ≥ 1). The seeds are S ≥ [1 + ((m_J − ell¹²)^{n/12} + 3B_N(n))/ell^n]^{−2} and T ≥ Q^{−2}, with Q = J_up(68) + 3N_up(68). | PROVEN-BY-COMPUTER | audit_scalar.py (rechecked) |
| 10 | **Recursion.** S' = G(S²T), T' = G(T²S'), G(x) = 1 − (1−x)²/(2x²), from the exchange identity at (2n, 2β). | PROVEN (repo proof; derivation rechecked) | moment REVIEW.md:127 |
| 11 | **Window lemma.** Given K = S²T > 1/2, set w = (1+√(2K−1))/2, ρ = (1−w)/w, d = T/(1+ρ²), C = (1−ρ)·min(S√d, d). Then purity ≥ C for every integer L ∈ [n, 2n] at β. | PROVEN (rechecked) | moment PROOF/REVIEW |
| 12 | **Windows and grid.** 12 dyadic windows n_j = 34·2^j (j = 0..11) at β_j = 2^j β0. Directed rounding on the grid B; a finer B is still sound because every rounding is outward. | PROVEN-BY-COMPUTER | `runs/seal12/audit_scalar_Z1.log` (ACCEPTED, gap 2497/100000, asymptotic from 69632) |
| 13 | **Asymptotic tail.** If u = max(1−S, 1−T) ≤ 1/100, then u_{j+1} ≤ 5u_j² and C ≥ 1 − 4u (my independent version gives 1 − 3.65u). So (1−C)/C ≤ 5u. Since 5u·e^{β*γ} < 1 at the last window, it holds for all later windows. Covers L ≥ 69632, and hence all L ≥ 34 together with step 12. | PROVEN (written) | moment REVIEW.md:90–102; the domain check `e = 1/100` is in audit_scalar.py |
| 14 | **Finite prefix L = 4..33.** Numerators from step 3. **L = 4..12:** denominators from the I-seam thermal inputs. **L = 13..23:** signed degree-8 majorants. **L = 24:** isolated window from the n=24 state, anchor 48 (C ≈ .681). **L = 25:** Cauchy–Schwarz Z_25² ≤ Z_24·Z_26 on the spectrum of X (C ≈ .7059). **L = 26..33:** own-length MPS numerators. Each L is checked against margin(γ). | PROVEN-BY-COMPUTER | Reviews `uniform_small_lengths_completion_review`, `uniform_n24_second_coverage_review` (audit.py 65–67), `uniform_direct25_coverage_review`, and `uniform_gap_0248_all_sizes_review/audit.py`. At γ = 2497/100000: `runs/seal12/audit_allsizes_Z1.log` ACCEPTED. **Note:** the direct-25 review carries an unresolved *resource* anomaly (25.96 CPU s against a 15 s limit); it is not mathematical. |
| 15 | **Union.** {2, 3} ∪ [4, 33] ∪ ⋃_j [n_j, 2n_j] ∪ tail = all L ≥ 2. | PROVEN | all-sizes audit.py `combined_claim` |
| 16 | **Thermodynamic limit.** **(a)** liminf_L Δ_L ≥ γ. **(b)** Every weak-* limit point ω of the periodic ground states has GNS Hamiltonian H_ω ≥ γ(1 − \|Ω⟩⟨Ω\|), i.e. a simple vacuum and gap ≥ γ. **(c)** Uniqueness of the infinite-volume ground state among all states, and convergence of ω_L. | **(a)** PROVEN (trivial). **(b)** Repo: absent (README:37 disclaims infinite volume). **GAP → CLOSED** by me (§2.2). **(c)** **NOT PROVEN**, and not claimed. | Hand proof plus standard theorems (Bratteli–Robinson analyticity, Nelson) |

Hypothesis matching:
- 3 → 9: R_68 ≈ −8.3e−6 < 0 is what forcing needs.
- 4 + 5 → 7, 8: the caps and majorants are statements about spec X_0 and spec X_x; Z = J + 3N.
- 6 → 7: exactly the 18 inputs that `check_provenance.py` maps to `moment_intervals`, with the equality asserted.
- 9 → 10 → 11: the seeds are at (n = 34, β0), and the recursion doubles both n and β.
- 11 → 2: C > 1/2 in every window.
- 13 needs u ≤ 1/100 at the last window; this is asserted.
- 14 uses β0 = 49/4 and the same margin test as 2.
- Periodic boundary conditions are essential: open chains have spin-1/2 edge states, and nothing here applies to them.

## 2. Gap closures

### 2.1 Twisted traces and the sector identity (closes step 5)
- **Setup.** Use the Cartesian basis, with (A_α)_{jk} = ε_{αjk} and S_α = −iA_α. Let R = diag(−1, −1, 1), the π-rotation about z. Then R A_α R^T = ε^z_α A_α with ε^z = (−1, −1, +1).
- **Seam factor.** The P seam is h^P_{L,1} = −Σ_α ε^z_α A_α^{(L)} ⊗ A_α^{(1)}. In the Dyson/Poisson expansion of step 4, each mark of label α on the seam bond picks up an extra factor ε^z_α. Hence Z^P_L = Tr[U_z X^L], where U_z is multiplication by ε^z(ω) = Π_marks ε^z_{α}.
- **U_z commutes with X.** The kernel F(ω, ω') is a site trace of a time-ordered product of A's from the marks of ω and ω'. Conjugating by R leaves the trace unchanged and multiplies the product by ε(ω)ε(ω'). So F = ε(ω)ε(ω')F, i.e. U_z X U_z = X, with U_z² = 1.
- **Klein group.** Likewise define U_x and U_y, with ε^x = (+, −, −) and ε^y = (−, +, −). Pointwise ε^x ε^y = ε^z, so {1, U_x, U_y, U_z} ≅ V4, a group of commuting involutions that commute with X.
- **Sector decomposition.** Split X = ⊕_χ X_χ over the four characters χ ∈ {0, x, y, z}. Let t_χ = Tr X_χ^L, so that Tr[U_g X^L] = Σ_χ χ(g) t_χ.
- **Equal nontrivial sectors.** The cyclic axis permutation is a proper rotation. It relabels marks and leaves F invariant, so it gives a unitary V with VXV* = X and V U_x V* = U_y, V U_y V* = U_z. Hence t_x = t_y = t_z =: N, and Tr[U_x X^L] = Tr[U_y X^L] = P.
- **Result.** Z = t_0 + 3N and P = t_0 + N(χ_x + χ_y + χ_z)(z) = t_0 − N. So J := t_0 = (Z + 3P)/4 and N = (Z − P)/4, which are the repo's formulas.
- **Physical check.** The C++ kernel's P_L equals Tr e^{−β(H^P + aL)} with this exact seam; float ED L = 4..10 lands inside every repo interval.

### 2.2 Gap in the thermodynamic limit (closes 16b; 16c stays open)
- **Finite volume.** Let ψ_L be the unique ground state and ω_L = ⟨ψ_L, · ψ_L⟩. For any A,
  ω_L(A*[H_L, A]) = ⟨Aψ_L, (H_L − E_L)Aψ_L⟩ ≥ γ(ω_L(A*A) − |ω_L(A)|²),
  because the gap is ≥ γ above the simple ψ_L (step 15).
- **Locality.** For A local on [−r, r] and L > 2r + 2, we have [H_L, A] = δ(A), the L-independent finite-range derivation.
- **Passing to the limit.** Embed local observables at sites mod L. Weak-* limit points ω exist by Banach–Alaoglu, and each one is translation-invariant and satisfies
  ω(A*δ(A)) ≥ γ(ω(A*A) − |ω(A)|²) for all local A.
- **GNS form inequality.** In the GNS triple (π, H_ω, Ω) the left side equals ⟨π(A)Ω, H_ω π(A)Ω⟩.
- **Core.** D = π(𝔄_loc)Ω is dense and invariant under H_ω. It consists of analytic vectors, because ‖δ^k(A)‖ ≤ ‖A‖ k! c^k for finite range (Bratteli–Robinson Thm 6.2.4). By Nelson's theorem D is a core.
- **Conclusion.** The form inequality extends to the form domain, so H_ω ≥ γ(1 − |Ω⟩⟨Ω|): ker H_ω = CΩ and spec H_ω ⊂ {0} ∪ [γ, ∞).
- **Not proven:** that ω is unique (e.g. among non-translation-invariant or other-boundary-condition ground states), that ω_L converges, or that ω is pure.

## 3. Trusted computing base
1. **CPython** int/Fraction arithmetic, plus the repo audit scripts (logic read line by line: audit_scalar.py and all-sizes audit.py; moment review audit replayed).
2. **The producer's C++ integer Horner kernel** (+ GMP, int64/int128 overflow guards) for the per-orbit squared norms behind all 18 thermal inputs. This is the single largest trust item: no reviewer, and not this audit, recomputes those integers. Only float64 and arb cross-checks (L ≤ 10, and L = 8, 12 untwisted) agree.
3. **The error-analysis lemma** for the integer Horner (E_L = 281(d_L+1)+1, Poisson truncation at 280). Repo-proven; I checked it for plausibility but did not re-derive it digit by digit.
4. **GMP sequential MPS contraction** in the repo for H0/N0. This is now redundant: FLINT fmpz_mat (python-flint 0.9.0) reproduces all 33 anchors exactly.
5. **SHA-256 seals** linking the reviewed artifacts. Note: at git HEAD, README/.md files were edited after sealing, so seal checks fail on a fresh checkout. The sealed archive copy (`watertight/auditor/orig_audit`) differs from HEAD only in .md files (`diff -rq` shows no non-.md differences); there all replays pass.
6. **Hand proofs:** L = 2, 3 spectra; the transfer identity; the V4 twist/sector lemma (§2.1); the packing, G, window and tail lemmas; purity ⇒ gap; Cauchy–Schwarz for L = 25; the thermodynamic-limit argument (§2.2, which uses standard Bratteli–Robinson and Nelson results).
7. **float64 eigh** appears only in the non-proof sanity checks.

## 4. Artifacts made by this audit
- `mps_anchor_check.py`, `mps_anchor_values.json`, `mps_anchor_check.log`: independent exact anchors (~39 s).
- `compare_anchors.py`, `compare_anchors.json`: 33/33 exact matches.
- `xcheck_Z_I.py`: arb enclosure of Z8 and Z12 (cross-check only).
- `sanity_thermal_float.py`, `sanity_thermal_float.json`: float ED of L = 4..10, I and P; 14/14 inside the repo intervals (sanity only).
- Replays were run in /tmp copies of the sealed archive. A temporary symlink `/workspace/shared/haldane_active` was created for `check_completed.py` and then removed.
