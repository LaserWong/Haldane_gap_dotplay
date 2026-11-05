# CERT_T0: certified spectral-gap lower bound for the spin-2 AKLT (VBS) chain

Date: 2026-11-04. All scripts and logs are in `runs/spin2_aklt/cert_t0/`.

## 0. Result

**Theorem T0 (PROVED, computer-assisted; floating-point verified, with independent residual recheck in CERT_T0_ARB.md).**
Let h = P3 + P4 act on neighbouring spin-2 pairs, where P_J projects onto total pair spin J. Let H°_m = Σ_{j∈Z_m} h_{j,j+1} be the periodic chain.
- For every m ≥ 17: gap(H°_m) ≥ ε_8 − 1/12 > 6261/50000 − 1/12 = **6283/150000 ≈ 0.041887**.
- The KHH(1) bond is h = x + (2/9)x² + (1/63)x³ + 10/7 = 10(P3/7 + P4) (identity checked exactly). For this chain and every m ≥ 17: gap ≥ (10/7)·6283/150000 = **6283/105000 ≈ 0.059838**.
- More generally, for any a3, a4 > 0, the chain with bond a3P3 + a4P4 has gap ≥ min(a3, a4)·6283/150000.

The certified intermediate result is **ε_8 > 6261/50000 = 0.12522**, where ε_8 is the smallest nonzero eigenvalue of the open 8-site chain. The float value is 0.1252296…, so the certified margin is about 1e-5.

A second, earlier run also certified ε_8 > 313/2500 = 0.1252, i.e. Δ ≥ 157/3750 ≈ 0.041867 (see `log_cert_n8_t313_2500.txt`). That run used the Higham bound only; it is superseded by the 6261/50000 run, which applies both bounds.

## 1. Statement used: Gosset–Mozgunov, arXiv:1512.00088, Thm 3 (fetched and checked in the scoping task)

**Hypotheses:**
- Each term is a projector, and the terms are translation-invariant.
- H°_m is frustration-free, i.e. it has a nonempty null space.
- n > 2 and m > 2n.

**Conclusion:** ε°_m ≥ (5/6)·(n²+n)/(n²−4)·(ε_n − 6/(n(n+1))). Here ε_n is the smallest nonzero eigenvalue of the open n-chain H_n = Σ_{i<n} h_{i,i+1}, and ε°_m is the smallest nonzero eigenvalue of H°_m.

For n = 8 the prefactor is (5/6)(72/60) = 1 and the subtracted term is 6/72 = 1/12, so ε°_m ≥ ε_8 − 1/12 for m ≥ 17.

**How each hypothesis is met:**
- *Projector.* h² = h, checked exactly over Q(√6) (`exact_bond.py`). h has rank 16 = 7 + 9.
- *Translation-invariant.* Holds by construction.
- *Frustration-free (PROVED).* The periodic VBS polynomial ∏_{j∈Z_m}(a_j b_{j+1} − b_j a_{j+1})² is a product of nonzero polynomials in an integral domain, so it is nonzero. Each pair (j, j+1) in it carries the SU(2)-invariant factor singlet² times a polynomial of degree 2 in each of the two sites. Multiplication by an invariant polynomial is SU(2)-equivariant from spin-1⊗spin-1 into spin-2⊗spin-2, so the pair spin is ≤ 2, and therefore P3 + P4 annihilates it. This is standard AKLT; the open-chain instance is also checked exactly in §2.
- *Degeneracy.* ε_n and ε°_m are gaps above the **entire** null space, so the degenerate open-chain ground space (edge spins) is allowed. In GM's statement "smallest nonzero eigenvalue" is the definition.

**Not covered:** periodic sizes m ≤ 16 (ledger C4) and the infinite-volume statement (C5).

## 2. Exact ground space of the open 8-chain (PROVED, exact arithmetic)

- `kernel_exact.py 8` constructs the 3 Sz = 0 VBS vectors E(a1,b1)·∏_{i<8}(a_i b_{i+1} − b_i a_{i+1})²·F(a8,b8), with (E,F) ∈ {(a²,b²), (ab,ab), (b²,a²)}.
  - Each has 2187 integer coefficients.
  - It checks exactly that Σ_q h̃_{pq} c_q = 0 on all 7 bonds. Here h̃ = W h W, with W = diag of boson normalisations, is the rational rescaled bond matrix; h̃ is checked rational in `exact_bond.py`.
  - It checks exact rank 3.
  - Log: `log_kernel_exact.txt`. A negative control in the same log replaces singlet² by (a b' + b a')² and correctly fails.
- `kernel9_exact.py 8`: all 9 VBS vectors (E,F ∈ {a², ab, b²}) are exact zero modes with exact rank 9 (`log_kernel9_exact.txt`).
- **dim ker H_8 = 9 exactly (PROVED).**
  - §3 certifies dim(ker H_8 ∩ {Sz=0}) ≤ 3, and the exact vectors give ≥ 3, so it equals 3.
  - By SU(2) (below), ker H_8 is therefore a sum of exactly 3 multiplets.
  - The 9-dim VBS span is SU(2)-invariant (the VBS map is equivariant) and contains exactly 3 Sz = 0 vectors, so it is 3 multiplets (spins 0, 1, 2). Hence it is the whole kernel.

## 3. Certified count of eigenvalues ≤ t in Sz = 0 (PROVED modulo IEEE-754 arithmetic; original Higham/Rump path in this section, independent residual path in CERT_T0_ARB.md)

**SU(2) reduction (PROVED).** H_8 commutes with total S, which is checked exactly at the bond level (`comm_Sz`, `comm_Splus`). The site spins are integer, so every irrep has integer spin and contains an Sz = 0 vector. Hence spec(H_8) = spec(H_8|Sz=0) as sets, and the smallest nonzero eigenvalue can be read in Sz = 0 (dim 38165).

**Symmetry blocks.** R (site reflection) and F (|m⟩ → |−m⟩ on every site) commute with H_8. Bond swap and flip invariance of h are checked exactly with sympy in `cert_block.py`. The characters (r, f) ∈ {±1}² split Sz = 0 into blocks with V_b dimensions 9719, 9406, 9364, 9676, which sum to 38165.

**Basis matrix.** P_b has orthogonal columns with entries in {0, ±1}; column j is Σ_{y∈orbit} χ(g_y)|y⟩. Then Λ = P_bᵀP_b = diag(|orbit|) with |orbit| ∈ {1, 2, 4}, so ‖P_b‖₂² = 4.

**Logic for each block:**
1. A* := P_bᵀ H P_b − tΛ is congruent to (H − t)|V_b, via Q = P_bΛ^{-1/2} orthonormal. By Sylvester, A* has the same number of eigenvalues ≤ 0 as H|V_b has eigenvalues ≤ t.
2. U := Σ_{j≤k_b} ŵ_jŵ_jᵀ is exactly PSD of rank ≤ k_b, where ŵ_j = P_bᵀ q_j and q_j are float orthonormalised projections of the exact VBS vectors. Any float vectors would do for the logic. If A* + U ≻ 0 then, by Weyl/interlacing, A* has at most k_b eigenvalues ≤ 0.
3. The k_b used were 2, 0, 0, 1 (blocks ++, +−, −+, −−), total **3**.
4. Therefore #{eig(H_8|Sz=0) ≤ t} ≤ 3. The three exact zero modes account for all of them, so H_8 has no eigenvalue in (0, t]. Hence **ε_8 > t**.

**Certificate that A* + U ≻ 0.** Let Ã be the float matrix actually built.
- *Build error (rigorous).* ‖Ã − (A* + U)‖₂ ≤ E_build ≈ 1.4e-13. It is the sum of:
  - bond entries rounded to nearest, with |ĥ − h| ≤ u|h| entrywise, verified with 300-bit arb balls;
  - diagonal sums of ≤ 7 terms;
  - the sparse triple product, at most 16 summands per entry, in any order;
  - rounding of t and of the diagonal subtraction;
  - the dense rank-k additions.

  Each piece uses |fl(Σ) − Σ| ≤ γ_{k−1}Σ|·| and ‖|M|‖₂ ≤ max row sum for symmetric nonnegative M. See the comments in `cert_block.py`.
- *Shift.* Ã_c = fl(Ã − cI) with c = 2e-6. The diagonal rounding is δ ≤ u(max|a_ii| + c).
- *Factorisation.* LAPACK dpotrf (OpenBLAS 0.3.34) runs to completion: info = 0 in all four blocks. Two independent rigorous bounds were then applied:
  - **Higham**, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., Thm 10.3 (statement confirmed by search): R̂ᵀR̂ = Ã_c + ΔA with |ΔA| ≤ γ_{d+1}|R̂ᵀ||R̂|. This gives λ_min(Ã_c) ≥ −γ_{d+1}‖R̂‖_F². The bound holds for any summation order (Jeannerod–Rump 2013, Lemma 4.3), so blocked BLAS is covered. A generous underflow allowance is added.
  - **Rump**, BIT 46 (2006) 433, Thm 2.3, which allows underflow and depends only on diag(Ã_c) because α_ij ≤ γ_{d+1}: λ_min(Ã_c) > −(γ_{d+1}/(1−γ_{d+1}))·tr(Ã_c) − d·3(2d + max a_ii)·η.

**Results at t = 6261/50000** (`log_cert_n8_t6261_50000.txt`, `summary_n8_t6261_50000.txt`):

| block (r,f) | dim | k_b | Higham term | Rump term | certified λ_min(A*+U) ≥ |
|---|---|---|---|---|---|
| (+,+) | 9719 | 2 | 1.70e-7 | 1.70e-7 | 1.83e-6 |
| (+,−) | 9406 | 0 | 1.62e-7 | 1.62e-7 | 1.84e-6 |
| (−,+) | 9364 | 0 | 1.61e-7 | 1.61e-7 | 1.84e-6 |
| (−,−) | 9676 | 1 | 1.69e-7 | 1.69e-7 | 1.83e-6 |

All four blocks are CERTIFIED under both bounds. The margin is more than 10× the error terms.

**Negative controls (the test is not vacuous):**
- n = 8, t = 0.1253 > ε_8: Cholesky fails in block (−,−), where the first excited multiplet lies, and passes elsewhere (`log_negctl_n8.txt`).
- n = 6, t = 0.135 > ε_6 = 0.134498: fails in (+,+) and (−,−) (`log_negctl_n6.txt`); t = 0.134 passes everywhere.

## 4. KHH(1) and general (a3, a4) (PROVED)

- a3P3 + a4P4 ≥ min(a3,a4)(P3 + P4) bondwise, with the same bond kernel (pair spin ≤ 2). So the global kernels coincide; both are ∩ of the bond kernels.
- ker^⊥ is invariant for both Hamiltonians. On it, H_{a} ≥ min(a)·H_{P34} ≥ min(a)·gap(H_{P34}).
- The exact identity KHH(1) = 10(P3/7 + P4) is in `exact_bond.py` (check `KHH1_eq_10(P3/7+P4)`). Taking min = 10/7 gives the bound in §0.

## 5. Proof-debt ledger

| id | item | status |
|---|---|---|
| C1 | GM Thm 3 statement and hypotheses (projector, TI, FF, m > 2n, gap above full kernel) | PROVED/checked (paper fetched in scoping) |
| C2 | Floating-point model for *construction* of Ab and for the *explicit* residual GEMMs of the arb recheck (IEEE-754 double, round-to-nearest, classical non-Strassen GEMM) | ASSUMED (see CERT_T0_ARB.md §4); the LAPACK dpotrf rounding model itself is no longer load-bearing |
| C3 | Cited theorems: Higham Thm 10.3 / Rump 2006 Thm 2.3 for dpotrf | SUPERSEDED for the positivity step by CERT_T0_ARB.md (residual + approx-inverse); kept only as the original discovery path |
| C4 | Periodic sizes m ≤ 16 | OPEN (not needed for m ≥ 17; can be done by the same certified inertia method on periodic Sz=0 blocks up to m ≈ 8, while 9–16 need other means) |
| C5 | Thermodynamic limit (gap of the infinite-chain GNS ground state) | HEURISTIC-standard (uniform bound for all m ≥ 17 plus the unique VBS ground state; not written out) |
| C6 | Better constant (n = 9 gives about 0.052) | NOT DONE: dense blocks of ~45k would need ~16 GB per block |
| C7 | Independent residual / approx-inverse recheck of all 4 blocks (no dpotrf error model) | DONE — see CERT_T0_ARB.md; all 4 blocks CERTIFIED; negctl t=0.1253 rejects in (−,−) |

## 6. Files

- `cert_t0/exact_bond.py` → `bond_exact.json`: exact h, rational h̃, the float ĥ with a rounding certificate, and all exact checks.
- `cert_t0/kernel_exact.py`, `kernel9_exact.py` → `kernel_vectors_n8.json`, `log_kernel_exact.txt`, `log_kernel9_exact.txt`.
- `cert_t0/cert_block.py`. Usage: `n r f t_num t_den c`. Writes `cert_n8_r±1_f±1_t6261_50000.json`.
- Logs: `log_cert_n8_t6261_50000.txt`, `summary_n8_t6261_50000.txt`, `log_cert_n8_t313_2500.txt` (earlier, Higham-only), `log_negctl_n8.txt`, `log_negctl_n6.txt`.
- Runtime: about 20 s total for 4 blocks with OPENBLAS_NUM_THREADS=4; peak memory about 2.5 GB.

## 7. Independent residual recheck

See `CERT_T0_ARB.md`. All four blocks re-certified at t = 6261/50000 without trusting the dpotrf rounding model; negative control t = 0.1253 rejects in block (−,−).
