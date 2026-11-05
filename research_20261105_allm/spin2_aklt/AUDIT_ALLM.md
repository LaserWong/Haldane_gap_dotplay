# AUDIT_ALLM: hostile audit of CERT_ALLM.md (Lemma GM′ and the all-length spin-2 AKLT ring gap)

Auditor scripts and logs are in `audit_allm/` (synced from `/workspace/audit_allm/`). They were written independently: my own bond construction, ED, exact arithmetic and counterexample search. I re-ran the author's own code only for the item 4 spot-check.

**Overall verdict: the theorem STANDS, with one proof gap that has been fixed and two wording errors.**

## Corrected theorem
*Assume the IEEE-754 binary64 + E_build trusted base of CERT_T0_ARB (see item 5). For every m ≥ 2, the spin-2 AKLT ring H°_m = Σ_{j∈Z_m}(P3+P4)_{j,j+1} has a unique ground state for m ≥ 3, and its gap satisfies*

ε°_m ≥ 74814907/1776546625 ≈ 0.0421125.

This is the same statement as CERT_ALLM. Only the proof of Lemma GM′ (step 1/4) and the trusted-base wording change. For m = 2 the convention H = h_{01} + h_{10} = 2h is used. The gap is 2, but the kernel is 9-dimensional (a 2-site "ring" is degenerate), so the uniqueness claim is for m ≥ 3 only.

## Item 1: Lemma GM′ re-derived from GM 1512.00088 (Thm 3, Lemma 4). Verdict: GAP FOUND (fixable, fixed). The statement is TRUE.

**Error.** CERT_ALLM §1 step 1 quotes GM Lemma 4 as the operator inequality B_k ≥ (Σc/(n−1)) ε_n (1 − Π_ker), i.e. B_k² ≥ (Σc/(n−1)) ε_n B_k. That is **not** what Lemma 4 says. Lemma 4 (gm.txt l.362–448) is an *expectation* statement in one specific translation-eigenstate φ of the ε°_m eigenspace. GM themselves say (l.355–358) that the operator bound only holds with min_j c_j.

The operator form is **false**, even for the author's own weights. `opform.py` compares the weighted open-chain gap λ⁺_min(B) with avg(c)·ε_n for spin-1 AKLT:
| n | c | λ⁺_min(B) | avg(c)·ε_n |
|---|---|---|---|
| 6 | (.05,1,1,1,.05) | 0.0405 | 0.2470 |
| 6 | (.3,1,1,1,.3) | 0.2153 | 0.2869 |
| 8 | (465,771,944,1000,944,771,465) | 278.84 | 290.47 |
| 8 | (.1,1,…,1,.1) | 0.0808 | 0.2818 |

All four are VIOLATED. Step 4 ("on ker(H)^⊥ every eigenvalue λ satisfies …") rests on this false operator inequality.

**Fix (implemented as proof text).** Keep step 3, which is a true operator identity and inequality, H² + βH ≥ α Σ_k B_k². Then take its expectation in GM's state φ, where Hφ = ε φ with ε = ε°_m and Tφ = e^{iθ}φ:

ε² + βε ≥ α Σ_k ⟨φ|B_k²|φ⟩ ≥ α ε_n (Σc/(n−1)) Σ_k ⟨φ|B_k|φ⟩ = α ε_n (Σc)²/(n−1) · ε   (Lemma 4, then Σ_k B_k = (Σc)H).

Divide by ε > 0 to get ε ≥ F ε_n − β = F(ε_n − G). This is exactly GM's own route (their eqs. 23–26).

Lemma 4's proof (l.373–448) uses only:
- translation invariance;
- c_j > 0, so that G_{n,k} h_i = 0 and hence ⟨G⊥hG⊥⟩ = ⟨h⟩;
- the window covering n distinct sites, i.e. m ≥ n.

It uses neither monotonicity nor m > 2n. In GM, m > 2n is used only at eq. (20), to kill the wrap-around terms c_r c_{r+m−d}. GM′ keeps those terms in C_m(e) = q(e) + q(m−e), so dropping m > 2n is legitimate.

**Independent re-derivation of the counting.**
- Each bond lies in exactly one position of each of n−1 windows, so Σ_k B_k = (Σc)H for m ≥ n−1.
- The coefficient of h_a h_b + h_b h_a at separation e is q(e) + q(m−e). This also holds at e = m/2, where the two orientations come from distinct windows.
- C_m(1) = q(1) because q(m−1) = 0 for m ≥ n.
- With α = 1/q(1) and β = αΣc² − 1: H² + βH − αΣB² = Σ_{nonadjacent}(1 − αC_m)h_a h_b. The adjacent terms cancel exactly, and each nonadjacent h_a h_b is a commuting PSD product.
- F = (Σc)²/((n−1)q(1)) and G = (n−1)(Σc² − q(1))/(Σc)². Both are as stated, and both reduce to GM (27)–(28) for GM's weights.
- The m ≥ 2n−3 reduction is correct, since q(e) and q(m−e) can both be nonzero only if m ≤ 2n−4.

**Counterexample search (none found).** `cex_search.py`, `cex2.py`, `cex3.py`, logs `cex2_part1.log` and `cex3.log`:
- **Models:** q-deformed XXZ ferro projectors (q = .1–.7), spin-1 AKLT, spin-2 AKLT, and 20 random real projector bonds (d = 2,3, ranks 1–7, generally not FF).
- **Sizes:** n = 3..8 and m ∈ [n, 2n], so mostly n ≤ m < 2n.
- **Weights:** random, log-normal and non-monotone. A hill-climb then pushed the bound as high as the hypothesis allows. This is a hostile choice.
- **Result:** 585 (model,n,m) cases, 273 of them with a positive bound. There were zero violations.
- **Sharpness:** n = 3 with equal weights is tight to about 1e-8 (XXZ). So the lemma is sharp and still never violated, which makes it a meaningful test.
- **Spin-2 checks:**
  - n = 8, m = 8: hill-climbed bound 0.0415 ≤ ε°_8 = 0.1028.
  - n = 7, m = 8: 0.0189 ≤ 0.1028.

## Item 2: exact rationals (m = 8..12, m ≥ 13, constant). Verdict: CONFIRMED
`exact_gm.py` is independent code, using Fraction throughout.
- min_e(1 − αC_m(e)) = 533397/4060678 > 0 at m = 8.
- For m = 9..13 it is 374811/2030339, and it stays constant at 0.18461 > 0 for all m ≥ 14. I checked m ≤ 39 directly, and m ≥ 2n−3 = 13 is covered by the reduction.
- F = 14364800/14212373 and G = 1200241/14364800.
- With ε_8 = 6261/50000: F(ε_8 − G) = **74814907/1776546625** exactly. This matches gm_general.json.
- min over the cases is the GM′ bound, because the m = 3..7 certified values (≥ 0.07975) and m = 2 (gap 2) all exceed 0.0421125.

## Item 3: float ED. Verdict: CONFIRMED (the bound lies below every value)
I built my own P3+P4 from the S₁·S₂ spectrum. It equals the author's `hhat` to 7e-16, in both digit orientations. Results are in the Sz = 0 sector (ED is `ed_rings.py`):
| ring m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| ε°_m | 0.800000 | 0.0797626 | 0.2121699 | 0.0959192 | 0.1517335 | 0.1027599 | 0.1315761 | 0.1049036 |
| ker (Sz=0) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

- Open n = 8: ε_8 = 0.12522965, with Sz=0 kernel 3, consistent with total kernel 9.
- 6261/50000 = 0.12522 lies below it, with margin 9.6e-6.
- All ring values are well above 0.0421125. Each certified m = 3..7 value lies below its ED value, and each NEG value lies above it.

## Item 4: m = 3..7 certificates and m = 2. Verdict: CONFIRMED (conditional on the item 5 trusted base)
**Blocks and symmetries.**
- Block dimensions sum to the Sz = 0 dimension. For example, m = 4 gives 29+16+14+26 = 85, and m = 6 gives 1751.
- Σk_b = 1 for every m. Since every SU(2) multiplet has an Sz = 0 member, the kernel is a singlet and dim ker = 1.
- The un-phased flip |m⟩ → |−m⟩ equals e^{iπS_y} times the constant (−1)^{2L} on Sz = 0, so it is a valid symmetry. Ring reflection is valid too.
- The logic "at most Σk_b eigenvalues ≤ t, and 0 is an exact eigenvalue (the VBS vector is checked exactly in `log_ring_kernel.txt`)" implies that every nonzero eigenvalue is > t.

**Reproduction.** I re-ran m = 4 (CERT 7975/1e5 and NEG 7977/1e5) and m = 6 (CERT 959/1e4), log `rerun_rings.log`.
- The results match log_rings.txt.
- The NEG at m = 4 fails in block (−,−), with tightest margin 1.37e-5. At m = 6 the tightest margin is 9.5e-6.
- This re-run rewrote `allm/arb/ring_arb_m4_*` and `ring_arb_m6_r*_t959_10000.json` with identical deterministic content.

**m = 2.** Gap 2, trivially. See the uniqueness caveat above.

## Item 5: trusted base honesty. Verdict: GAP FOUND (wording, fix below)
The CERT_ALLM header says the trusted base is "python-flint/arb ball arithmetic …". This is inaccurate:
- `cert_ring_block.py`, like CERT_T0_ARB's own description, uses NumPy/LAPACK IEEE-754 binary64 with Higham-γ a-priori bounds for the explicit GEMMs and reductions, plus the E_build model.
- arb is used only for bond rounding.
- The "arb/ring_arb_*.json" file names are misleading for the same reason.

**Replacement text:**
> Trusted base: same as CERT_T0_ARB. Exact rational bond data; residual/Cholesky inertia certificates whose floating-point error is bounded a priori under the IEEE-754 binary64 round-to-nearest model (Higham γ_k bounds for explicit matrix products/reductions, plus E_build), correctness of NumPy/LAPACK/BLAS as IEEE-compliant, and python Fraction for all rational steps. Not full interval arithmetic.

**Minor overclaim (not load-bearing).** §1 says the operator-inequality sanity test covered "spin-1 AKLT (n=4,5) and spin-2 (n=4,5) for all m in [n,2n]". The JSONs contain only two positive cases, both spin-2: (n=4,m=7) and (n=5,m=7). The spin-1 entries are negative controls only. Suggested wording: "checked in two spin-2 cases (n=4,5; m=7)". My cex search covers the gap.

## Required edits to CERT_ALLM.md
1. **§1 step 1:** replace the operator quotation of Lemma 4 with: "GM Lemma 4: there is a normalized φ with H°_m φ = ε°_m φ and Tφ = e^{iθ}φ, such that ⟨φ|B_k²|φ⟩ ≥ (Σc/(n−1)) ε_n ⟨φ|B_k|φ⟩ for all k. This requires only translation invariance, c_j > 0 and m ≥ n. Note: the operator form is false in general."
2. **§1 step 4:** replace with: "Take ⟨φ|·|φ⟩ of step 3: ε² + βε ≥ α(Σc)²ε_n ε/(n−1). Dividing by ε = ε°_m > 0 gives ε°_m ≥ F(ε_n − G)."
3. **Header:** use the trusted-base text from item 5.
4. **Sanity-test sentence:** correct it as in item 5.
5. **m = 2 line:** add "(kernel dim 9; uniqueness claimed for m ≥ 3)".

Not audited: the KHH(1) ≥ 0.060161 corollary, and the CERT_T0_ARB internals beyond its stated base, per-block k_b, and margin.
