# CERT_ALLM — spin-2 AKLT (P3+P4) periodic-ring gap for ALL ring lengths

## Audit status
Hostile audit: `AUDIT_ALLM.md` (scripts/logs in `audit_allm/`). Verdict: the theorem **STANDS** with the same bound; one proof gap in Lemma GM′ step 1/4 was fixed (expectation form of GM Lemma 4, not the false operator form); trusted-base wording corrected to IEEE-754 binary64 + E_build (not arb); uniqueness restricted to m ≥ 3. Not audited: the KHH(1) corollary, and CERT_T0_ARB internals beyond its stated base.

Status labels: **PROVED** (a rigorous argument, plus exact or CERT_T0_ARB-certified computation), **NUMERICAL**, **HEURISTIC**.

Trusted base: same as CERT_T0_ARB. Exact rational bond data; residual/Cholesky inertia certificates whose floating-point error is bounded a priori under the IEEE-754 binary64 round-to-nearest model (Higham γ_k bounds for explicit matrix products/reductions, plus E_build), correctness of NumPy/LAPACK/BLAS as IEEE-compliant, and python Fraction for all rational steps. Not full interval arithmetic. Everything new lives in `allm/`.

## 0. Where we started
- Open chain, n = 8: ε_8 > 6261/50000 = 0.12522, with kernel dimension 9 (CERT_T0_ARB, **PROVED**).
- Gosset–Mozgunov (GM) Thm 3, re-read from the paper (`/workspace/papers/gm.txt`):
  - It covers **periodic, translation-invariant FF rings only**, and requires m > 2n.
  - Its bound is ε°_m ≥ (5/6)(n²+n)/(n²−4)·(ε_n − 6/(n(n+1))).
  - GM has **no** open-chain theorem.
  - With n = 8 it gives ε°_m ≥ 6283/150000 for m ≥ 17.
- Gap to close: rings with m ≤ 16.

## 1. Lemma GM′ (GM Thm 3 with general weights and m ≥ n) — PROVED
**Setting.**
- H°_m = Σ_{j∈Z_m} h_j, where h_j = (P3+P4)_{j,j+1} is a projector and H°_m is FF.
- ε_n is the gap of the open n-site chain.
- Weights c_0..c_{n−2} > 0.
- q(x) = Σ_j c_j c_{j+x}, with q(x) = 0 for x > n−2.
- C_m(e) = q(e) + q(m−e).

**Statement.** Suppose m ≥ n and C_m(e) ≤ q(1) for every 2 ≤ e ≤ m−2. Then

ε°_m ≥ F·(ε_n − G),  F = (Σc)²/((n−1)q(1)),  G = (n−1)(Σc² − q(1))/(Σc)².

**Proof.**
1. Let B_k = Σ_j c_j h_{k+j}, a window of n−1 consecutive bonds.
   - Because m ≥ n, the window covers n distinct sites, so B_k is unitarily equivalent to a weighted open n-chain.
   - GM Lemma 4: there is a normalized φ with H°_m φ = ε°_m φ and Tφ = e^{iθ}φ, such that ⟨φ|B_k²|φ⟩ ≥ (Σc/(n−1)) ε_n ⟨φ|B_k|φ⟩ for all k. This requires only translation invariance, c_j > 0 and m ≥ n. **Note: the operator form B_k² ≥ (Σc/(n−1)) ε_n B_k is false in general** (counterexamples in `AUDIT_ALLM.md` / `audit_allm/opform.py`); GM themselves state that the operator bound holds only with min_j c_j.
   - Summing over k and using Σ_k B_k = (Σc)H (each bond lies in exactly one position of each of n−1 windows, for m ≥ n−1) gives Σ_k ⟨φ|B_k²|φ⟩ ≥ (Σc)² ε_n/(n−1) · ⟨φ|H|φ⟩ = (Σc)² ε_n/(n−1) · ε°_m.
2. Expand Σ_k B_k².
   - Diagonal terms give Σc²·H.
   - An ordered pair of bonds at ring separation e gets coefficient C_m(e). The two orientations q(e) and q(m−e) are both counted, and q(m−1) = 0 needs m−1 > n−2 (true for m ≥ n).
3. Set α = 1/q(1) and β = αΣc² − 1. Then
   H² + βH − αΣ_k B_k² = Σ_{non-adjacent i≠j}(1 − αC_m(d(i,j))) h_i h_j.
   - The adjacent terms cancel exactly because C_m(1) = q(1). For m = n, C_m(1) = q(1) + q(m−1) = q(1) since m−1 = n−1 > n−2.
   - For non-adjacent pairs, h_i h_j is a product of commuting PSD operators, so it is PSD. The coefficient 1 − αC_m ≥ 0 by hypothesis.
   - Hence H² + βH ≥ α Σ_k B_k² as an operator inequality.
4. Take ⟨φ|·|φ⟩ of step 3: ε² + βε ≥ α Σ_k ⟨φ|B_k²|φ⟩ ≥ α (Σc)² ε_n ε/(n−1), where ε = ε°_m. Dividing by ε > 0 (frustration-freeness: the gap is the smallest positive eigenvalue) gives ε°_m ≥ F ε_n − β = F(ε_n − G).

When m ≥ 2n−3, the hypothesis reduces to q(x) ≤ q(1) for x = 2..n−2 (q(e) and q(m−e) can both be nonzero only if m ≤ 2n−4).

Hostile-audit points checked (see `AUDIT_ALLM.md`):
- the m = n edge case;
- the window/site counting;
- that Lemma 4 is used in its actual expectation form (not the false operator form);
- positivity of c;
- independent counterexample search (585 cases, zero violations).

Sanity test (NUMERICAL, `allm/test_opineq*.json`): the operator identity/inequality of step 3, H² + βH − αΣB² ≥ 0, holds to −2.4e-13 when the hypothesis holds. This was checked in two spin-2 cases (n = 4, 5; m = 7). The negative control, with weights that violate the hypothesis, gives λ_min ≈ −20. (Spin-1 JSON entries are negative controls only.)

## 2. Exact application at n = 8 — PROVED (exact rational arithmetic, `allm/gm_general.py` → `gm_general.json`)
Input: ε_8 = 6261/50000, certified.

| weights | hypothesis | bound for m = 8..12 and all m ≥ 13 |
|---|---|---|
| GM optimal (GM29) | holds for every m ≥ 8 | ≥ 6283/150000 = 0.041887 |
| c = (465,771,944,1000,944,771,465) | holds for every m ≥ 8 | ≥ **74814907/1776546625 = 0.0421125…** |

Rerun with `python3 allm/gm_general.py "465,771,944,1000,944,771,465"`.

F = 14364800/14212373, G = 1200241/14364800 (exact; confirmed independently in the audit).

## 3. Short rings m = 3..7 — direct CERT_T0_ARB-style certificates, PROVED
How the certificates were built:
- Code: `allm/ring_kernel_exact.py` gives the exact periodic VBS vector, checked to be annihilated by all m bonds. `allm/cert_ring_block.py` is the periodic variant of `cert_arb_block.py`.
- Sector: Sz = 0. Integer total spin means every SU(2) multiplet has an Sz = 0 member, so this sector contains the whole spectrum.
- Blocks: four symmetry blocks (ring reflection R = ±1, spin flip F = ±1).
- Kernel: a rank-k_b update with the exact VBS vector. k_b summed over the blocks is 1, so the ring kernel is 1-dimensional for m = 3..7.
- Each certified t passes in all 4 blocks. The negative control at the next rational step fails in at least one block.

| m | certified: ε°_m > | negative control (fails) | float ED |
|---|---|---|---|
| 3 | 79/100 | 81/100 | 0.8 |
| 4 | 319/4000 | 7977/100000 | 0.079763 |
| 5 | 2121/10000 | 2122/10000 | 0.212170 |
| 6 | 959/10000 | 960/10000 | 0.095919 |
| 7 | 1517/10000 | 1518/10000 | 0.151733 |

Error budgets were E_build ≈ 1e-13, ρ ≤ 4e-11, F2 ≤ 4.3e-10. Logs: `allm/log_rings.txt`; certificates: `allm/arb/ring_arb_m*.json` (directory name historical; the certificates use the IEEE + E_build trusted base above, not arb ball arithmetic).

For m = 2, H = 2h, and the gap is 2 (trivial; kernel dim 9; uniqueness claimed for m ≥ 3 only).

## 4. Final statement (PROVED, at the CERT_T0_ARB trusted base)
For the periodic spin-2 ring H°_m = Σ_{j∈Z_m}(P3+P4)_{j,j+1}, for every m ≥ 2 the gap is at least 74814907/1776546625 ≈ 0.042112, and for every m ≥ 3 the ground state is unique:
- m ≥ 8: by Lemma GM′;
- m = 3..7: by the direct certificates in §3, all of which exceed this value, with Σk_b = 1;
- m = 2: the gap is 2 (kernel dim 9).

There is **no uncovered m** for the periodic gap.

**Corollary (KHH(1), not re-audited).** The KHH(1) bond is 10(P3/7 + P4) ≥ (10/7)(P3+P4), and the two have the same kernel. So the KHH(1) ring gap is ≥ (10/7)·0.042112 = **0.060161** for all m ≥ 2.

## 5. Not covered, and why
- **Open chains of general length.** GM gives nothing for open chains. Open-chain monotonicity also fails numerically (ε_6 > ε_5). The only certified open chain is n = 8.
  - NUMERICAL scoping (`allm/lm_open_scope.py`): Lemm–Mozgunov (arXiv:1801.08915) eq. (4.16) has threshold G(8) = 0.1238 < ε_8 = 0.12522. With optimised weights it would give an open-chain gap ≳ **0.00123** for m ≥ 16. This needs:
    1. certified ε_{n'} ≥ ε_8 for n' = 3..7 (cheap);
    2. exact arithmetic;
    3. for m < 16, a GM′-style extension of their Prop 4.4. This looks feasible, using an artificial-site ring of m+1 sites and the same C(e) ≤ q(1) check.
  - None of this has been done. It is the recommended next step, and it is also an input that Part B needs (see INTERVAL_SCOPING.md).
- **Ring ground-state uniqueness for m ≥ 8.** For m = 3..7 uniqueness follows from Σk_b = 1 in the certificates. For m ≥ 8 it is known in the literature and is not needed for the gap statement (smallest nonzero eigenvalue).

## 6. Proof-debt ledger
| item | status |
|---|---|
| ε_8 > 6261/50000 (open) | PROVED (CERT_T0_ARB) |
| Lemma GM′ | PROVED (written argument in §1; audited in AUDIT_ALLM.md) |
| GM′ hypothesis and bound at n = 8 | PROVED (exact rationals; audit-confirmed) |
| ring certificates m = 3..7 | PROVED (IEEE + E_build trusted base; audit-confirmed) |
| operator-inequality spot checks (step 3 only) | NUMERICAL (sanity only, not used) |
| KHH(1) corollary | PROVED algebraically from the ring gap; not re-audited |
| open-chain all-m | OPEN, with a cheap route sketched (§5) |
