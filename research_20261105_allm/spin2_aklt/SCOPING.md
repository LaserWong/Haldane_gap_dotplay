# Spin-2 chain near the AKLT point: scoping and feasibility (no production runs)

Date: 2026-11-04 (America/Chicago). Directory: `runs/spin2_aklt/`. Every number in this file comes from a script in this directory.

Labels:
- **PROVED**: exact or symbolic, with the argument given.
- **NUMERICAL**: float64 ED, uncertified.
- **HEURISTIC**: a reasoned estimate.

## 0. Verdict (read this first)

1. **The repo's bootstrap does not apply to the spin-2 AKLT/KHH family as it stands. (PROVED)**
   - The bootstrap needs THEORY.md eq. 13: Z_L = Tr X^L for every L ≥ 2, with X real self-adjoint Hilbert–Schmidt.
   - The only construction the repo has proved is the sufficient one: −h = Σ c_α A_α⊗A_α, with the A_α real in some real structure and c_α ≥ 0.
   - That construction fails for KHH(α) at every α ∈ (0,1], under **every** real structure J.
   - It fails for every VBS parent aP3 + bP4 (a, b ≥ 0) under every J. The only possible exception is the ray b = 35a/9, which the inertia count cannot exclude.
   - The proof is the inertia count in §3.
   - This extends, and agrees with, the SO(5) remark at `Haldane_extensions/REPORT.md:487`.
2. **Novel target T1 is blocked on a new theorem.** T1 is an explicit certified gap at α < 1, between AKLT and Heisenberg.
   - It needs a new self-adjoint transfer construction (debt D1), or else a different method.
   - Even if D1 were granted, ED-only seeds at n = 4 do not work. At α = 0.95, δ(4) = 0.124 ≈ Δ_8 = 0.138, so the conditions βδ ≪ 1 and βΔ ≳ 5 are incompatible. (NUMERICAL/HEURISTIC)
3. **Cheap, honest target T0: an explicit gap bound for the spin-2 AKLT chain via Gosset–Mozgunov.**
   - Result: ε_9(open) = 0.120065 > 6/90. GM Thm 3 then gives **Δ_m ≥ 0.0520 for every periodic m > 18**, for h = P3 + P4. (NUMERICAL today. It becomes PROVED once ε_9 is certified; cost in §5.)
   - The bound transfers to any VBS parent aP3 + bP4 as min(a,b)·0.0520. For KHH(1) = (10/7)P3 + 10P4 that is ≥ 0.0743.
   - Novelty is low. The method is standard (Knabe/GM/Nachtergaele/LTI), and I found no published explicit number for the 1D spin-2 chain. Absence is HEURISTIC; the search was not exhaustive.
4. **The models that do satisfy the sufficient construction are Heisenberg-like and gain nothing. (NUMERICAL)**
   - The sufficient cone is simplicial, and the Heisenberg chain is its corner closest to AKLT.
   - Moving into the cone (μ = 0.3 along each of the three other rays) raises δ(4) more than the gap.
   - These models therefore inherit the spin-2 Heisenberg blocker in `runs/spin2/FEASIBILITY.md`: L ≈ 250–600 at about 1e-6 per-site accuracy.

**Recommendation:**
- Do T0 now; it takes minutes to hours.
- Treat T1 as research debt D1. The first, cheap step is the QTM-reality test (§5, D1a). It decides whether eq. 13 can hold at all for KHH(α).
- Do **not** start a spin-2 bootstrap production run.

## 1. Model (PROVED)

Notation:
- x = S_i·S_j for spin 2, so x ∈ {−6, −5, −3, 0, 4} on J = 0..4.
- P_J are the bond-spin projectors. Their exact rational polynomials in x are in `poly.json` (`poly.py`). In particular:
  - P3 = 1 + (9/20)x − (7/360)x² − (1/36)x³ − (1/360)x⁴
  - P4 = (1/28)x + (1/40)x² + (1/180)x³ + (1/2520)x⁴
  - P3 + P4 = 1 + (17/35)x + (1/180)x² − (1/45)x³ − (1/420)x⁴. This is a projector; numerically, its eigenvalues are {0, 1} and ‖h² − h‖ = 2e-16.

Family (Katsura–Hirano–Hatsugai, arXiv:cond-mat/0702196, verified by fetch):
- H(α) = Σ_i [x + α((2/9)x² + (1/63)x³ + 10/7)].
- α = 0 is the S = 2 Heisenberg chain. α = 1 is the S = 2 AKLT chain.
- Exact identity, checked by hand from `poly.json`: H(1) = Σ 10(P3/7 + P4).
- Any Σ A_J P_J with A_3, A_4 > 0 (and A_0..A_2 = 0) has the VBS ground state, since the VBS has bond spin ≤ 2. (PROVED, standard)

Properties at α = 1:
- Frustration-free, with E0 = 0 for every L. ED confirms this for odd L as well.
- Unique periodic VBS ground state.
- ξ_VBS = 1/ln 2 ≈ 1.44, from transfer-matrix ratio 1/2.

Literature values at α = 0 (verified by fetch):
- Schollwöck–Jolicœur, cond-mat/9501115: Δ = 0.085(5), ξ = 49(1), e0 = −4.761248(1).
- Wang–Qin–Yu, cond-mat/9903035: Δ = 0.0876(13).
- Todo–Kato 2001 gives Δ = 0.08917(4) and ξ = 49.49(1), as quoted in `runs/spin2/FEASIBILITY.md`; I did not refetch it.

## 2. Small-ring ED (NUMERICAL, `ed.py`, logs `log_khh_*`, `log_p34_*`)

Periodic rings, gap Δ_L = E1 − E0 over all Sz sectors, normalization of H(α):

| α | Δ_3 | Δ_4 | Δ_5 | Δ_6 | Δ_7 | Δ_8 | δ(4) = E0(8) − 2E0(4) | E0(8)/8 |
|---|---|---|---|---|---|---|---|---|
| 1 (AKLT) | 8/7 | 0.12503 | 0.31214 | 0.14831 | 0.22650 | 0.15601 | 0 (exact) | 0 |
| 0.95 | 1.13571 | 0.16229 | 0.38459 | 0.14895 | 0.27237 | 0.13752 | 0.1242 | −0.2316 |
| 0.9 | 1.12857 | 0.20228 | 0.44648 | 0.16896 | 0.31568 | 0.14651 | 0.2143 | −0.46832 |
| 0.8 | 1.11429 | 0.28708 | 0.54643 | 0.22276 | 0.39404 | 0.18416 | 0.3686 | −0.94668 |
| 0.5 | 1.07143 | 0.55477 | 0.74498 | 0.40233 | 0.58286 | 0.32070 | 0.7942 | −2.39310 |
| 0 (Heis) | 1.0 | 1.0 | 0.96118 | 0.69729 | 0.82596 | 0.54557 | 1.4781 | −4.81523 |

The pure projector h = P3 + P4 gives, for L = 4..8: 0.07976, 0.21217, 0.09592, 0.15173, 0.10276.

Reading at α = 1:
- Even L rise from below and odd L fall from above.
- Hence Δ_∞(AKLT) ≈ 0.16–0.20 in KHH units, or ≈ 0.10–0.15 for P3 + P4. (HEURISTIC)
- ξ is about 1.4 sites. For α < 1, ξ must grow toward 49 at α = 0; L ≤ 8 cannot resolve it.

Open chains with h = P3 + P4 (`open_ed.py`, `log_open_p34*.txt`, Sz = 0 sector):
- Sz = 0 contains every integer-spin multiplet.
- There are 3 zero modes, from the edge spins 1⊗1 → J = 0, 1, 2 (9 states total).

| n | ε_n | Knabe (n−1)/(n−2)·(ε − 1/(n−1)) | GM (5/6)(n²+n)/(n²−4)·(ε − 6/(n(n+1))) |
|---|---|---|---|
| 5 | 0.133931 | < 0 | < 0 |
| 6 | 0.134498 | < 0 | −0.0091 |
| 7 | 0.125414 | < 0 | **0.0189** |
| 8 | 0.125230 | < 0 | **0.0419** |
| 9 | 0.120065 | < 0 (−0.0056) | **0.0520** |

- Knabe never closes for n ≤ 9.
- GM closes from n = 7. The statement of GM Theorem 3 (n > 2, m > 2n, projector terms) was verified by fetching arXiv:1512.00088.

## 3. Transfer-construction obstruction (PROVED; `rank_signs.py`, `jcheck.py`)

**Rank channels.** Write h = Σ_k γ_k Σ_q T^k_q ⊗ T^k_q†, with orthonormal irreducible tensor operators of rank k = 0..4. Exact CG arithmetic in sympy gives, for (γ0..γ4):

| term | γ |
|---|---|
| 1 | (5, 0, 0, 0, 0) |
| x | (0, 10, 0, 0, 0) |
| x² | (60, −5, 21, 0, 0) |
| x³ | (−30, 196, −42, 36, 0) |
| x⁴ | (1176, −305, 561, −180, 36) |
| P0 | (1/5, −1/5, 1/5, −1/5, 1/5) |
| P1 | (3/5, −1/2, 3/10, 0, −2/5) |
| P2 | (1, −1/2, −3/14, 4/7, 2/7) |
| P3 | (7/5, 0, −4/5, −1/2, −1/10) |
| P4 | (9/5, 6/5, 18/35, 9/70, 1/70) |

Sanity checks: spin-1 Heisenberg gives [0, 2, 0]. Spin-1 AKLT gives [4/3, 5/3, 1/3], and its even-rank channel has the wrong sign, which is the known failure.

**Standard real structure.** Use J = e^{−iπS_y}K, so that T^k is real symmetric for even k and antisymmetric for odd k. The sufficient construction then holds iff γ_k ≥ 0 for odd k and γ_k ≤ 0 for even k ≥ 2. k = 0 is a free shift.

**Inertia lemma, for every real structure J = VKV†.**
- Let W = V·M_5(ℝ)·V†. The construction requires the realigned form B(X,Y) = Tr[−h(X⊗Y)] to be PSD on W.
- Define Q(X) = Σ_{k≥1}(−γ_k)‖P_k X‖² on Hermitian X.
- The condition forces Q ≥ 0 on the 15-dimensional real space W∩Herm = V·Sym·V†, and Q ≤ 0 on the 10-dimensional space iW∩Herm = V·(i·Antisym)·V†.
- Both subspaces sit in the 24-dimensional traceless Hermitian space; the k = 0 direction is a free shift. So it is necessary that #{Q < 0 dims} ≤ 10 and #{Q > 0 dims} ≤ 15. Otherwise a dimension count forces a nonzero vector of the wrong sign.

**KHH(α).** γ(KHH) = (·, 10 + 2α, 4α, 4α/7, 0). For α > 0, Q < 0 on the k = 1, 2, 3 directions, which is 3 + 5 + 7 = **15 > 10** dimensions. ⇒ **No J works, for any α ∈ (0, 1].** At α = 0 the standard J works; that is the audited spin-2 Heisenberg construction in `spin2_positivity_review`.

**aP3 + bP4.** γ1 = 6b/5, γ2 = −4a/5 + 18b/35, γ3 = −a/2 + 9b/70, γ4 = −a/10 + b/70. The sign pattern by regime:

| regime | outcome |
|---|---|
| b < 14a/9 | Q > 0 on k = 2, 3, 4 (21 dims) |
| 14a/9 < b < 35a/9 | Q > 0 on 16 dims |
| 35a/9 < b < 7a | Q < 0 on k = 1, 2, 3 (15 dims) |
| b ≥ 7a | Q < 0 on ≥ 15 dims |

All four regimes are excluded. **The single surviving ray is b = 35a/9.** There γ = (·, 6a/5, 6a/5, 0, −2a/45): 8 negative dims and 9 positive. It fails for the standard J (min eigenvalue −1.2).

**Search over other J (NUMERICAL, `jsearch2.py`).** L-BFGS over V = V0·expm(iH) with 3 restarts:
- R35: best penalty 7.2. That is exactly the standard-J value 5·1.2², so nothing better was found.
- KHH1: penalty 337. Consistent with the theorem.
- This is not a proof that R35 fails.

**Cone of admissible models.** With e0 = 0, the cone in projector energies (e1..e4) is simplicial with rays:
- ray0 = Heisenberg (0.1, 0.3, 0.6, 1)
- ray1 = (7/22, 17/22, 1, 5/11)
- ray2 = (7/11, 1, 9/22, 15/22)
- ray3 = (1, 3/7, 9/14, 25/42)

**In-cone ED** (`cone_ed.py`, rays at μ = 0.3, ray-0 units; NUMERICAL):

| model | δ(4) | Δ_7 | Δ_8 |
|---|---|---|---|
| Heis | 0.148 | 0.0826 | 0.0546 |
| +ray1 | 0.249 | 0.0969 | 0.0840 |
| +ray2 | 0.276 | 0 (odd-L degeneracy) | 0.0837 |
| +ray3 | 0.270 | 0.0891 | 0.0743 |

Δ/δ does not improve. **No cheap in-cone model to target.**

**What is not proved.** Failure of the *sufficient* construction is not failure of eq. 13 itself.
- In 1D the nonzero spectrum of X is forced: it is the quantum-transfer-matrix (QTM) spectrum, by uniqueness of power sums.
- So eq. 13 holds iff the QTM of H(α) is diagonalizable with real spectrum and summable (HS).
- With signed channels, X = S·K (a sign grading times a symmetric matrix) is only Krein-self-adjoint, so complex pairs are possible.
- The Hankel-PSD test on small-L Z_L (`hankel.py`, KHH1) found no violation, but that test is weak. Inconclusive.

## 4. Literature (fetched and verified this task unless noted)

- Katsura–Hirano–Hatsugai, arXiv:cond-mat/0702196 (the KHH(α) family). The journal reference was not visible on the fetched page, so cite the arXiv id.
- Gosset–Mozgunov, arXiv:1512.00088 (Thm 3, used in T0). Knabe, J. Stat. Phys. 52, 627 (1988), quoted as Thm 1 there.
- *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, arXiv:2411.03680 (LTI SDP; spin-1 AKLT ≥ 0.34976 vs Knabe 0.24806; I saw no 1D spin-2 benchmark).
- Garcia-Saez–Murg–Wei, arXiv:1308.3631 (spin-1 AKLT 0.350; 2D spin-3/2 and spin-2; no 1D spin-2 bound).
- Schollwöck–Jolicœur, cond-mat/9501115; Wang–Qin–Yu, cond-mat/9903035 (S = 2 Heisenberg Δ, ξ).
- Cited from the bibliographies, not refetched:
  - AKLT, CMP 115, 477
  - FNW, CMP 144, 443
  - Nachtergaele, CMP 175, 565 (cond-mat/9410110)
  - Lemm–Mozgunov, arXiv:1801.08915
  - Pomata–Wei, arXiv:1911.01410
  - Yarotsky, and Michalakis–Zwolak (stability near AKLT/frustration-free points; ids not verified)
- **Not found:** an explicit lower bound for the 1D spin-2 AKLT gap, or any explicit certified gap anywhere on KHH(α < 1). (HEURISTIC absence.)

## 5. Plan and costs

**T0: certified GM bound for the spin-2 AKLT/VBS chain** (recommended now)
1. Certify ε_8 ≥ 0.125, which gives GM ≥ 0.0417, or ε_9 ≥ 0.12, which gives GM ≥ 0.0520.
   - Method: Sylvester inertia of H_n − tI. Show exactly 3 eigenvalues below t in Sz = 0, with the zero modes known exactly.
   - Split by reflection and spin-flip symmetry: n = 8 gives about 4 blocks of ~9.5k; n = 9 gives blocks of ~45k.
   - Arithmetic: float LDLᵀ plus a rigorous backward-error bound (margin ≥ 1e-3 ≫ error), or an arb/mpmath interval LDL.
   - Cost: n = 8 is about 1–5 CPU-min per block, so it fits the 600 s cap. n = 9 dense is too big (45k² floats ≈ 16 GB), so it needs a sparse/banded or MPS-structured inertia method, or stay at n = 8.
2. Finite periodic m ≤ 16 (or 18), if all sizes are wanted: certified ED up to m = 8. Sizes 9–18 need a separate argument, e.g. the m-independent Knabe-type version, or simply restrict the statement to m > 2n plus the thermodynamic limit.
3. Write-up. Estimated total, a few CPU-hours: Δ_AKLT(S = 2, P3 + P4) ≥ 0.0417 (n = 8), or ≥ 0.052 (n = 9).
4. Optional upgrade: LTI SDP (arXiv:2411.03680) at n = 6–7 would likely get much closer to ≈ 0.1. The cost is an SDP of dimension 5^n; HEURISTIC.

**T1: explicit gap at α < 1** (research; blocked on D1)
- D1a, **QTM-reality test** (NUMERICAL, cheap): Trotter QTM for KHH(α), N = 3–4 slices, dim 5^{2N} ≤ 390,625, matrix-free Arnoldi for the leading ~30 eigenvalues, at β = 1–4, α ∈ {0.9, 1}.
  - Complex leading pairs ⇒ eq. 13 is very likely false and the bootstrap is dead for this family.
  - A real spectrum ⇒ go looking for a proof (Krein/PT-type argument, or 2-site blocking).
  - Cost: about 10–30 CPU-min per point. Control the Trotter artifacts with α = 0 (Heisenberg, known to be real).
- Even with D1, the seeds need n ≫ ξ(α). ξ(α) is unknown for α < 1, and L ≤ 8 ED cannot give useful seeds. We would need either MPS-based two-sided Z bounds (the upper side is blocked, per `runs/spin2/FEASIBILITY.md` §3) or a perturbative ε-argument from α = 1.
- Alternative T1': a stability theorem with explicit constants from AKLT, in the style of Michalakis–Zwolak or Nachtergaele–Sims–Young (ids not verified). It would give a gap for 1 − α ≤ ε0, with ε0 likely tiny. Cost: analytic work, unknown; low computation.

## 6. Proof-debt ledger

| id | item | status | blocks |
|---|---|---|---|
| D1 | Self-adjoint transfer (eq. 13) for KHH(α > 0) / VBS parents | **OPEN**. Sufficient construction PROVED impossible (except the R35 ray) | T1 entirely |
| D1a | QTM real-spectrum test | not run | decides whether D1 can be true |
| D1b | R35 ray b = 35a/9: exists J? | NUMERICAL no (3 restarts); unproved | only that ray |
| D2 | Certified ε_8 (or ε_9) for P3 + P4 | NUMERICAL value; certification not done | T0 |
| D3 | GM hypotheses: projector terms ✓, translation-invariant ✓, frustration-free ✓ (VBS), m > 2n | PROVED / checked | T0 |
| D4 | Small periodic m ≤ 2n for T0 | open, optional | T0 "all sizes" |
| D5 | Certified ED L ≤ 8 (periodic) | NUMERICAL only | T0 prefix, T1 |
| D6 | Twist / odd-L conventions; V4 symmetry sectors | not needed for T0; needed for any bootstrap | T1 |
| D7 | α-grid continuity lemma (gap at a grid ⇒ interval) | not started | T1 |
| D8 | Literature absence of a spin-2 1D explicit bound | HEURISTIC | novelty claim of T0 |

## 7. Files

Scripts:
- `poly.py`, `poly.json`: exact polynomials.
- `rank_signs.py`, `rank_proj.py`: exact rank vectors.
- `jcheck.py`: standard-J check.
- `jsearch2.py`: J search; logs `log_j_*`.
- `ed.py`: periodic ED; outputs `ed_*.json`, `log_khh_*`, `log_p34_*`.
- `open_ed.py`: open chains, GM/Knabe; logs `log_open_p34*`.
- `cone_ed.py`: in-cone models; outputs `cone_*.json`.
- `zfull.py`: full spectra; outputs `spec_KHH_1_L2..7.npz`.
- `hankel.py`: Hankel test.

Superseded: `jsearch.py`'s first search used the wrong basis. Its helpers are reused by later scripts.
