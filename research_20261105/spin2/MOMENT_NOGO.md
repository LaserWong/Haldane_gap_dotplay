# Moment-certificate no-go: final statement and proof (2026-11-04)

Status labels: PROVED, EXTERNAL-VERIFIED, PROVISIONAL, TESTED (float/estimate, NOT rigorous), DISPROVED, BLOCKED.
Scripts: `runs/spin2/moment_nogo/` (`data.py`, `make_fakes.py` [mp floats, proposes fakes], `verify.py` [exact Fractions only],
`toys.py` [exact], `spin2_rho.py` [estimate]). Fake spectra: `moment_nogo/fakes.json` (exact rationals); exact verdicts: `verify_out.json`.

**Summary.** The old §B1 claim, "ρ_m < 1 is necessary for a moment certificate", is replaced by three results:

- **Thm 1 (one-sided data): PROVED.** If the data bound the moments only from above, plus lower bounds at long lengths, then ρ_m^+ ≥ 1 rules out every certificate, and the best provable S is about 1/2.
- **Prop 2: the old claim is DISPROVED for exact two-sided data.**
- **Thm 3 (the actual spin-1 rigorous intervals): PROVED, by exact rational counterexamples.**
  - With lengths 4..M for M ∈ {6, 7, 8}, no certificate in the class can give S(32) > 1/√2 (the bootstrap seed).
  - The spectra that defeat it have S(32) = 0.500, 0.447 and 0.578.
  - With M = 10, the seed at n = 16 is ruled out, but n = 32 is not settled.

There is no general two-sided ρ-threshold theorem. That question is BLOCKED (see the ledger).

## 0. Setting and the certificate class (theorem contract)

**Fixed β; shifted transfer operator X = X_β.** Inputs counted as *structural facts* (true for the real operator, assumed by the repo):

- **(F1)** X is compact and self-adjoint, so its spectrum is real atoms with finite multiplicities accumulating only at 0. The traces Z_L = Tr X^L and the twisted traces P_L are finite for L ≥ 4 and are given by the transfer identity at every integer L ≥ 4.
- **(F2)** Sector split. J (multiplicity 1) and N (each atom counted 3 times, Klein-group triplet) satisfy Z_L = J_L + 3N_L and P_L = J_L − N_L, where J_L = Σ_{J-atoms} w λ^L and N_L = Σ_{N-atoms} w λ^L, with w ∈ ℤ_{≥1}. Atoms of either sign are allowed in both sectors.
- **(F3)** Perron–Frobenius. λ0 = ‖X‖ is a simple atom of J, and every other atom satisfies |λ| < λ0.
- **(F4)** Positivity of physical partition functions: Z_L > 0 and P_L > 0 for **every** integer L ≥ 4, odd lengths included. (P_L is the π-seam twisted-ring partition function.)

**Data D_M (spin-1, β = 49/4, shift a = 700741/500000)** is used exactly as in the repo:

- Rigorous rational intervals Z_k ∈ [z_k^−, z_k^+] and P_k ∈ [p_k^−, p_k^+] for 4 ≤ k ≤ M. These are parsed from `published_scalar_enclosures.py` exactly as `uniform_second_moment_optimization/explore.py` does. The widths are 1e-11 to 3e-5.
- Anchors Z_L ≥ exp(−β R_L) for L = 60, 64, 68, with the exact rational shifted-Rayleigh quotients R_L < 0 from `certificate_w12_Z1.json`.

**Certificate.** A *certificate in class 𝒞(D_M)* is any argument concluding a statement Φ(X) from D_M and (F1)–(F4) alone. Soundness means Φ must hold for every operator spectrum compatible with D_M + (F1)–(F4). Examples include:

- Hankel/Christoffel filters;
- packing bounds;
- SDP/moment relaxations;
- any β-grid of *other* temperatures, treated as separate operators (see W2).

**Targets Φ.**

- **Φ_seed(n):** S(n) := Z_{2n}/Z_n² > 1/√2.
- This is necessary for the repo's bootstrap seed K = S²T > 1/2, because T = Z_{2n}(2β)/Z_{2n}(β)² ≤ 1 holds always. So S ≤ 1/√2 forces K ≤ 1/2.

**Elementary soundness lemma (PROVED).** If a single spectrum σ' satisfies D_M + (F1)–(F4) and S_{σ'}(n) ≤ 1/√2, then no certificate in 𝒞(D_M) proves Φ_seed(n).

*Proof.* A diagonal finite-rank operator with spectrum σ' is compact and self-adjoint. Declare its atoms' sectors as listed. Then it satisfies every premise and violates the conclusion. ∎

(Zero eigenvalues can be added freely. Adding infinitely many tiny eigenvalues of size ≤ ε changes each Z_L, L ≥ 4, by O(ε²) at most, so strict data margins survive; this covers "X has infinite rank" if one insists on it.)

## 1. Theorem 1 (one-sided data): PROVED

**Data class.** The data D⁺ consist of:

- upper bounds on every combination Σ c_k Y_k, where Y ∈ {Z, P, J} and c_J ≥ 0 (i.e. on quantities that are increasing in the J-sector moments), for k ≤ M;
- lower bounds only at lengths L ≥ L_1;
- arbitrary two-sided bounds on quantities that do not involve J.

**Statement.** Let σ be any spectrum satisfying D⁺ + (F1)–(F3). Let A be a finite set of *positive* J-atoms other than λ0, counted with multiplicity, and define ρ_M^+(A) := Σ_A (a/λ0)^M.

Fix t with 0 < t < λ0 and t^M ≤ Σ_A a^M (possible with t → λ0 exactly when ρ_M^+ ≥ 1). Define σ' = σ − A + δ_t (one J-atom at t). Then:

- **(i)** J'_k ≤ J_k for every 4 ≤ k ≤ M, odd k included. Hence every D⁺ upper bound still holds.
- **(ii)** Take t ≥ max A. Then L_1(t) := min{L : Σ_A a^L ≤ t^L} is finite (see proof). For every L ≥ L_1(t), J'_L ≥ J_L. Hence every lower bound at L ≥ L_1 still holds.
- **(iii)** (F1)–(F3) still hold. The bound S_{σ'}(n) ≤ (Z_{2n} + t^{2n}) / (Z_n + t^n − Σ_A a^n)² holds as well.
  - In particular, if Z_n/λ0^n → 1 and t = λ0(1 − ε) with εn → 0 and Σ_A (a/λ0)^n → 0, then S_{σ'}(n) → 1/2 and K' ≤ 1/4.

*Proof.*

- **(i)** All a > 0 and t > 0. By monotonicity of ℓ^p norms, ‖a‖_k ≥ ‖a‖_M ≥ t for k ≤ M. So Σ_A a^k ≥ t^k, and J'_k − J_k = t^k − Σ_A a^k ≤ 0 for k ≤ M. The N sector is unchanged. Z' − Z and P' − P equal the same nonpositive number, so the D⁺ upper bounds hold.
- **(ii)** Lower bounds are only imposed at L ≥ L_1, so the definition of L_1 is what matters. Because t ≥ max A, and t > max A unless A is a single atom equal to t (a trivial case), Σ_A (a/t)^L decreases to 0. So L_1 is finite and J'_L − J_L = t^L − Σ_A a^L ≥ 0 for all L ≥ L_1. Choosing t in [max A, λ0) with t^M ≤ Σ_A a^M is possible whenever ρ_M^+ ≥ 1 or ‖a‖_M ≥ max A, which always holds, because max A < λ0 (F3).
- **(iii)** (F1)–(F3) hold because t < λ0 and t is a single simple atom.
  - The S formula follows by substitution.
  - The limit follows from t^{2n}/λ0^{2n} → 1, t^n/λ0^n → 1, (Z_n/λ0^n) → 1 and (Z_{2n}/λ0^{2n}) → 1. ∎

**Caveats (all part of the statement):**

- (F4) positivity at short L < L_1 is *not* automatic. P'_L − P_L = t^L − Σ_A a^L < 0 there, so positivity must be checked or assumed with margin.
- The budget is ρ^+, which counts positive J-atoms only. Negative atoms cannot be traded this way, because odd moments would increase.
- Thm 1 does **not** cover two-sided bounds on J-moments at k ≤ M. The real repo data are two-sided, which is why Thm 3 is needed.

**Exact toy** (`toys.py`). J = {1, (19/20)×2, (−1/2)×3}, N = {(3/10)×2, −2/5}, M = 6, ρ_6^+ = 1.470, t = 99/100.

- All upper bounds for k ≤ 6 hold, the lower bounds for L ≥ L_1 = 17 hold, and positivity holds for 4 ≤ L < 400. The tail is monotone.
- S'(n) = 0.494, 0.503, 0.513 at n = 8, 16, 32, against true values 0.343, 0.392, 0.558.

## 2. Proposition 2: the old necessity claim is DISPROVED for exact two-sided data

Take σ = {1} ∪ {9/10 × 2}, so ρ_6 = 2(0.9)^6 = 1.063 ≥ 1. Suppose the data are the exact moments m_4, m_5, m_6, the anchor top ≥ 1, and (F3).

- For every compatible spectrum, Σ λ^4(λ − 9/10)² = m_6 − (9/5)m_5 + (81/100)m_4 = 1/100.
- Each term is ≥ 0, and the top term is ≥ (1)^4(1/10)² with equality only at top = 1.
- So top = 1 and every other atom lies in {0, 9/10}.
- m_4 then fixes the multiplicity, which comes out as exactly 2.

So the spectrum, and hence S(n), is determined exactly, even though ρ_6 ≥ 1 (verified exactly in `toys.py`). Two-sided data carry Christoffel/Chebyshev information that the ρ-budget ignores.

## 3. Theorem 3 (actual spin-1 rigorous intervals): PROVED (exact rational certificate)

**Statement.** For M ∈ {6, 7, 8}, no certificate in 𝒞(D_M) proves S(32) > 1/√2, nor S(16) > 1/√2. Hence none proves the bootstrap seed K(32) > 1/2.

For M = 10, no certificate in 𝒞(D_10) proves S(16) > 1/√2.

**Proof.** By the soundness lemma it suffices to exhibit, for each M, a spectrum σ'_M with the properties below. The spectra are in `fakes.json`; each J-sector has top λ0' = 100001/100000.

| M | J-sector big atoms | N-sector big atoms | bulk (integer-weight clusters) | S'(16) | S'(32) | S'(32)² (≥ K') |
|---|---|---|---|---|---|---|
| 6 | λ0', 999/1000 | none | 3 J clusters + 3 N clusters, weights 357–6771 | 0.49997 | 0.50013 | 0.2501 |
| 7 | λ0', 999/1000 | none | 4 + 4 clusters, incl. unit atoms −0.919 (J), −0.880 (N) | 0.3012 | 0.4467 | 0.1995 |
| 8 | λ0', 89/100 | 17/20, −93/100 | 5 + 5 clusters | 0.2473 | 0.5780 | 0.3341 |
| 10 | λ0' | −9/10 | 7 + 7 clusters, weights up to 2.9·10^6 | 0.4474 | 0.8249 | n=32 not killed |

`verify.py` checks every property in exact rational arithmetic (runtime 0.1 s). For each M:

- (a) Z'_k ∈ [z_k^−, z_k^+] and P'_k ∈ [p_k^−, p_k^+] for all 4 ≤ k ≤ M.
- (b) Anchors: Z'_L ≥ 1 + x + x² ≥ e^x, with x = −βR_L ∈ (0, 1), for L = 60, 64, 68.
- (c) (F3): the top is simple, lies in J, and |λ| < λ0' for every other atom.
- (d) (F2): integer multiplicities ≥ 1 and correct sector bookkeeping (Z = J + 3N, P = J − N).
- (e) (F4) for all L ≥ 4:
  - exact check of Z'_L > 0 and P'_L > 0 for 4 ≤ L < L*;
  - for L ≥ L*, use λ0'^L ≥ 1 > B(L), where B(L) is the total weight of the atoms that enter with a "bad" sign. B is decreasing in L. L* = 8, 13, 16, 12.
- (f) The S' values above, compared with 1/2 exactly.

All checks return True. ∎

**Where the positions come from.** The cluster positions were found with mpmath Newton at 50 digits, starting from an NNLS fit. They were then rounded to rationals with denominator 10^42. Only the exact checks constitute the proof; the floats play no logical role.

**Sanity checks on the threshold (TESTED, floats).**

- Each fake violates the next-length data badly. For example, the M = 8 fake has Z'_10 = 3.48 against an interval near 2.65. So these fakes are specific to D_M.
- Float cone-feasibility (NNLS, nodes in [−0.99, 0.99]) gives the largest single extra atom compatible with D_M:

  | M | J+ | J− | N+ | N− |
  |---|---|---|---|---|
  | 8 | 0.897 | −0.825 | 0.917 | −0.973 |
  | 10 | 0.797 | −0.696 | 0.806 | −0.900 |
  | 12 | 0.766 | −0.637 | 0.750 | −0.871 |

- At M = 12 these reproduce the repo's rigorous Christoffel caps: N+ 0.7502278, N− −0.8710300, and J− −0.6502. The J− value is slightly inside the cap because the float grid stops at the node limit.
- **Spin-1 consistency.** At M = 12 any single competitor is ≤ 0.871 in modulus. With multiplicity 3, 3·0.871^32 ≈ 0.036, so S(32) ≈ 0.93 is not obstructed. This is consistent with the repo's PROVED S(32) ≥ 0.930 from D_12 (two-sided intervals plus anchors).
- The gap between "obstructed" (M ≤ 8, PROVED) and "certified" (M = 12, repo PROVED) is open:
  - M = 9: float cone search finds a candidate with S(32) ≈ 0.60 (N atoms +0.83 and −0.93, J atom 0.85). The integer-weight exact fake was **not** constructed. Status: TESTED only.
  - M = 10, 11: open.
- **Crude ρ indicator** (TESTED; ρ_M ≈ Z_M^mid/λ0^M − 1 with λ0 ≈ 1):

  | M | 6 | 8 | 10 | 12 |
  |---|---|---|---|---|
  | ρ_M | 11.9 | 3.6 | 1.65 | 0.90 |

  The spin-1 transition between "faked" and "certified" sits around ρ ≈ 1–3, consistent with the heuristic but not equal to it (Prop 2).

## 4. Weakening: what the theorem does NOT cover (stated honestly)

- **W1. More structural facts.** Facts beyond (F1)–(F4) are excluded. If a certificate may use them, Thm 3 may fail. They are:
  - entrywise positivity or tensor-network representability of X (inverse-eigenvalue constraints);
  - finer degeneracy patterns, such as SU(2) multiplets inside J/N;
  - rigorous ED lower bounds Z_L ≥ e^{−β(E0(L)+aL)} at L > M.
- **W2. Cross-β structure.** Data at other temperatures are allowed, but only as a separate operator. Thm 3 changes only X_{β=49/4}, keeping the true spectra at other β. That is legitimate in 𝒞 because the data at different β are independent numbers.
  - **Not covered:** constraints linking temperatures for the *same* L, such as β ↦ ln Z_L(β) convex (Laplace transform) or monotonicity in β.
  - The fakes inflate Z_L(49/4) for 13 ≤ L ≤ 68 by a factor ≈ 2 (M = 6, 7) or 1.3 (M = 8). If the grid had rigorous upper bounds on Z_L at neighbouring β for such L, convexity could exclude them. The repo has no such inputs.
- **W3. Fixed-n targets.** Thm 3 kills S(32) only for M ≤ 8. For M = 10 it kills only n = 16. "No certificate for any n" is not claimed.
- **W4. Interlacing across L.** Not applicable: one operator X yields all L, and the fakes are single operators. This is satisfied automatically.

## 5. Spin-2 consequences (ESTIMATE, not rigorous)

There are no rigorous spin-2 intervals, so Thm 3 cannot be run. Thm 1 applies conditionally, if ρ_8^+ ≥ 1, which the estimates make overwhelming.

**Estimate.** Using `spin2_rho.py`:

ln ρ_8(β) ≳ ln(exp(β(8e0 − E0(8)) − 8βc(β)) − 1)

- 8e0 − E0(8) = 0.431885, with e0 = −4.761248 (Todo–Kato) and E0(8) = −38.5218691354 (float ED).
- βc = 3e^{−βΔ}√(2πΔ/β)/(2πv), with Δ = 0.08917 and v = 4.41 (magnon gas).

| β | ln ρ_8 (estimate) | range for c ×2 / c ÷2 |
|---|---|---|
| 10 | 4.22 | [4.14, 4.26] |
| 20 | 8.61 | [8.59, 8.63] |
| 30 | 12.95 | [12.94, 12.95] |
| 56 | 24.18 | [24.18, 24.19] |

The e0 error contributes about ±5e-4.

**Caveats.**

- ρ here counts all non-top atoms, both sectors. Thm 1 needs ρ^+ in J, and the E0(8) singlet is a J-sector state.
- Two-sided spin-2 data could in principle do better (Prop 2).
- Still, ρ_8 ~ e^{8.6} at β = 20, compared with spin-1's 3.6 at M = 8, where exact fakes exist. That makes a short-length spin-2 moment seed hopeless in practice. This is a heuristic consequence, not a theorem.

## 6. Hostile self-check

1. *Do the fakes use the real rigorous intervals, not J/N midpoints?* Yes. They are checked against the Z, P boxes directly, and the J/N intervals are never used.
2. *Odd L and signed sectors?* Checked:
   - all odd k ≤ M lie inside the data;
   - (F4) holds at all odd L ≥ 4. The first M = 8 attempt (N atom −0.97) **failed** with Z'_9 < 0 and was discarded.
3. *Anchors?* The exact rational R_L are used, with the inequality e^x ≤ 1 + x + x² for 0 ≤ x ≤ 1.
4. *PF?* λ0' = 1.00001 is simple, and every other atom has modulus ≤ 0.999.
5. *Is λ0' compatible with known e0 bounds?* It shifts f by about 8e-7 per site relative to f = −a. No rigorous input in the class excludes this, and anchors and data are verified.
6. *Is T ≤ 1 really universal?* T = Z_{2n}(2β)/Z_{2n}(β)² ≤ 1 holds for any trace of e^{−2βH} vs (Tr e^{−βH})², with nonnegative eigenvalues of e^{−βH}. So S ≤ 1/√2 ⇒ K ≤ 1/2 regardless of the 2β data.
7. *Rounding?* All verdicts are exact. No float appears in `verify.py` except for printing.
8. *Does Thm 1's proof secretly need a < t?* The proof handles this case explicitly (ii).

## Proof-debt ledger

| item | status | basis |
|---|---|---|
| Soundness lemma (fake spectrum ⇒ no certificate) | PROVED | §0 |
| Thm 1, one-sided ρ^+ ≥ 1 ⇒ no certificate; S → 1/2 | PROVED (with stated short-L positivity side condition) | §1, exact toy |
| Old "ρ_m < 1 necessary" for two-sided data | DISPROVED | Prop 2, exact |
| Thm 3, spin-1 D_6, D_7, D_8 cannot certify S(32) > 1/√2; D_10 cannot certify S(16) > 1/√2 | PROVED | exact Fractions, `verify.py` |
| D_9 fake with S(32) ≈ 0.60 | TESTED (float cone only) | `feas.py` search |
| D_10/D_11 certify S(32)? | open | none |
| General two-sided threshold (Christoffel-type) | BLOCKED | depends on the unknown spectrum |
| Robustness to cross-β convexity (W2) and extra structural facts (W1) | open; theorem stated without them | §4 |
| Spin-2 ln ρ_8(β) | TESTED / ESTIMATE | `spin2_rho.py` |
