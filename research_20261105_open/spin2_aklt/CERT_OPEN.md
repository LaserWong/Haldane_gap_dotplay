# CERT_OPEN — spin-2 AKLT (P3+P4) open-chain gap for ALL lengths

## Audit status
Hostile audit: `AUDIT_OPEN.md` (review record, snapshot and auditor scripts in `AUDIT_OPEN/`). Verdict: the theorem **STANDS** with the same bound; no load-bearing proof gap. Lemma LM′ (wrap-around coefficient C_M and Prop 4.6 at m ≥ n), exact F/G arithmetic, certified μ_n and kernel, trusted-base wording and all-m coverage were CONFIRMED. Two optional exposition fixes (F1: Def 4.2 / Prop 4.6 scope; F7: n = 6 residual sample) are applied below. Not audited: the KHH(1) corollary, and CERT_T0_ARB internals beyond its stated base.

Status labels: **PROVED** / **NUMERICAL** / **HEURISTIC**.

Trusted base: same as CERT_T0_ARB / CERT_ALLM. Exact rational bond data; residual/Cholesky inertia certificates whose floating-point error is bounded a priori under the IEEE-754 binary64 round-to-nearest model (Higham γ_k, E_build), correctness of NumPy/LAPACK/BLAS as IEEE-compliant, and python Fraction / sympy for all rational and Q(√21) steps. **Not** full interval / arb ball arithmetic for the load-bearing certificates (residual rechecks for n=7,8 use the CERT_T0_ARB path). Everything new lives in `open/`.

Paper used: Lemm–Mozgunov, *Spectral gaps of frustration-free spin systems with boundary*, arXiv:1801.08915 (fetched to `/workspace/papers/lm.{txt,html,pdf}`). **Not** arXiv:1810.02428 (that is NSY).

## 0. Result

**Theorem T_OPEN (PROVED, computer-assisted; IEEE trusted base).**
Let h = P3+P4 on neighbouring spin-2 pairs, and let H_m = Σ_{i=1}^{m−1} h_{i,i+1} be the open chain (Π₁ = Π_m = 0). Write γ_m for the gap above the entire null space (smallest positive eigenvalue). Then for every m ≥ 2,

γ_m ≥ 907760209/740162500000 ≈ 0.00122643.

Coverage (no uncovered m):
| m | method | certified lower bound |
|---|---|---|
| 2 | trivial (H = h projector) | 1 |
| 3 | direct cert | 16/100 = 0.16 |
| 4 | direct cert | 1495/10000 = 0.1495 |
| 5 | direct cert | 1339/10000 = 0.1339 |
| 6 | direct cert (CERT_T0) | 134/1000 = 0.134 |
| 7 | direct cert | 1254/10000 = 0.1254 |
| ≥ 8 | Lemma LM′ at n = 8 | **907760209/740162500000** |

For m ≥ 3 the null space is exactly 9-dimensional (two spin-1 edge spins); for m = 2 it is also 9. The gap is the distance from 0 to the first bulk excitation — there is no edge-state splitting for AKLT (exact degeneracy).

**Corollary (KHH(1), not re-audited).** The KHH(1) bond is 10(P3/7+P4) ≥ (10/7)(P3+P4) with the same kernel, so the open KHH(1) gap is ≥ (10/7)·907760209/740162500000 = 907760209/518113750000 ≈ 0.001752 for all m ≥ 2.

## 1. Published open-boundary criterion — Lemm–Mozgunov

### Theorem 2.5 (LM, quoted from the paper; alttext of (2.5))
Let m ≥ 8 and 4 ≤ n ≤ m/2. Then
γ_m ≥ (1/(2⁸ √(6n))) ( min{γ_n^B, γ_{n−1}^E} − 2√6 n^{−3/2} ).
(The load-bearing form we use is the sharper (4.17) with Rem 2.6(iii)’s G(n), not this coarse F ≥ 1/(2⁸√(6n)) lower bound.)

### Remark 2.6 (iii) (sharper threshold used here)
In (2.5) and (2.7) one may replace 2√6 n^{−3/2} by
G(n) = (1 + a_n² b_n) / (n − 1 + n^{3/2} a_n),
with a_n, b_n as in LM (4.20)–(4.21) / Rem 2.6(iii). For n = 8 this is
G(8) = −2/5 + 4√21/35 ≈ 0.123723
(LM table rounds up to 0.1238).

### Remark 2.6 (ii) (Π₁ = Π_m = 0)
If the boundary projections vanish, then γ_n = γ_n^B = γ_n^L = γ_n^R and
γ_m ≥ F(n) ( min_{1≤n'≤n} γ_{n'}^0 − G(n) ),
with F, G from the weighted construction (LM (4.17)–(4.20)). In particular μ_n = min_{2≤n'≤n} γ_{n'} (γ_1 is vacuous; γ_2 = 1).

### Proposition 4.4 (Knabe-type bound; published hypothesis n ≤ m/2)
On the artificial ring of M = m+1 sites (LM §4.1–4.3), with positive weights c_0,…,c_{n−2} satisfying Assumption 4.1,
Σ_{l=1}^{M} B_{n,l}² ≤ (Σ c_j²) H_m + (Σ c_j c_{j+1}) (Q+F).

### Proposition 4.6 (operator lower bounds on deformed windows)
Bulk windows: B² ≥ c_0 γ_n^B B. Edge windows: B² ≥ c_0 γ_{n−1}^E B. The proof (LM pp. 21–23) uses only positivity/monotonicity of the c_j (Ass 4.1), frustration-freeness, and the existence of bulk windows (m ≥ n). It does **not** use n ≤ m/2 beyond the theorem’s global hypothesis. LM Def 4.2 and Prop 4.6 are *stated* with n ≤ m/2, but that is Thm 2.5’s global hypothesis, not a step of the Prop 4.6 proof, which needs only m ≥ n; we extend Def 4.2 verbatim to all m ≥ n under the C_M hypothesis of Lemma LM′ (§2).

### Consequence at n = 8 (published range)
With LM’s optimal weights (4.18)+(4.20), F(8) = 49/250 + 17√21/125 ≈ 0.81923 and G(8) as above. For m ≥ 16 (i.e. n = 8 ≤ m/2) and μ = min_{2≤n'≤8} γ_{n'} > G(8),
γ_m ≥ F(8)(μ − G(8)).
This is the estimate quoted in CERT_ALLM §5 (~0.00123). It does **not** cover m = 8..15.

## 2. Lemma LM′ (this work) — PROVED

**Purpose.** Extend Prop 4.4 from n ≤ m/2 to all m ≥ n, under a C_M hypothesis on the artificial ring of size M = m+1, exactly as GM′ does for periodic rings.

**Setting.** Π₁ = Π_m = 0, so H_m = Σ_{i=1}^{m−1} h_i with h_i² = h_i. Artificial ring of M = m+1 sites as in LM (4.1)–(4.3), with the two artificial bonds equal to 0. Weights c_0,…,c_{n−2} > 0 satisfy Ass 4.1. q(x) = Σ_j c_j c_{j+x} (q(x) = 0 for x > n−2). C_M(e) = q(e) + q(M−e).

**Statement.** Let m ≥ n ≥ 4. Suppose C_M(e) ≤ q(1) for every 2 ≤ e ≤ M−2. Let μ_n = min_{2≤n'≤n} γ_{n'}. Then
γ_m ≥ F (μ_n − G),
where F = c_0 (Σ c) / q(1) and G = (Σ c² − q(1)) / (c_0 Σ c)
(same formulae as LM (4.17); equivalently G = (2c_0² + Σ(c_j−c_{j+1})²)/(2 c_0 Σ c)).

**Proof.**
1. *Window sum identity (LM).* Σ_{l=1}^M B_{n,l} = (Σ c) H_m, because each physical bond sits in every relative window slot exactly once on the artificial ring (artificial bonds are 0). Requires only M ≥ n (i.e. m ≥ n−1); we use m ≥ n.
2. *Knabe expansion with wrap-around (extends LM Prop 4.4 / App A).* Expanding Σ_l B_{n,l}² on the ring of size M yields
   Σ B² = (Σ c²) H + q(1)·(adjacent anticommutators) + Σ_{e≥2} C_M(e)·(hi hi' at ring distance e).
   When n ≤ m/2 one has C_M(e) = q(e) for every e that can appear, recovering LM (A.2). For general m ≥ n the wrap-around term q(M−e) may be nonzero; that is the only change.
3. *Operator inequality.* Set α = 1/q(1), β = α Σ c² − 1. Then
   H² + β H − α Σ B² = Σ_{e≥2} (1 − α C_M(e)) (PSD pair terms).
   - Adjacent cancellation: C_M(1) = q(1) + q(M−1) = q(1), since M−1 = m ≥ n−1 > n−2.
   - Non-adjacent coefficients are ≥ 0 by the C_M hypothesis, and hi hi' ≥ 0 for d(i,i') ≥ 2 (LM Lemma 4.5).
   - Hence H² + β H ≥ α Σ B² as operators.
4. *Deformed-window lower bounds (LM Prop 4.6, operator form with min weight c_0).* For m ≥ n every bulk window is unitarily an open n-chain and B ≥ c_0 A, so B² ≥ c_0 γ_n B. Edge windows satisfy B² ≥ c_0 γ_{n−1}^E B. With Π = 0 one has γ_{n−1}^E = min_{2≤n'≤n−1} γ_{n'}, so overall Σ B² ≥ c_0 μ_n Σ B = c_0 μ_n (Σ c) H.
   **Note:** this is the valid min-weight operator bound (factor c_0). It is **not** the false equal-weight operator form of GM Lemma 4 (see AUDIT_ALLM).
5. Combine: H² + β H ≥ α c_0 μ_n (Σ c) H. On a positive-energy eigenvector, γ + β ≥ α c_0 (Σ c) μ_n, i.e. γ ≥ F(μ_n − G).

**Sanity.** For m ≥ 16, n = 8 ≤ m/2, LM′ reduces to published LM Rem 2.6(ii)+(iii). We apply LM′ only for m ≥ 8 (so that bulk windows exist at n = 8); short chains m ≤ 7 are certified directly.

## 3. Exact F, G and C_M at n = 8 — PROVED (`open/lm_prime.py`)

LM optimal weights (4.18)+(4.20) at n = 8:
c_j = 16√2 + x_8 ((6)j − j²), x_8 = −16√2/5 + 32√42/35.
Ass 4.1 (symmetry + mono to midpoint) holds exactly. All c_j > 0.

Closed forms (sympy):
- F = 49/250 + 17√21/125
- G = −2/5 + 4√21/35

Rational bounds via convergents 3524/769 < √21 < 6049/1320:
- F_lo = 157497/192250
- G_up = 1429/11550
- μ = 6261/50000 > G_up
- bound_lo = F_lo (μ − G_up) = **907760209/740162500000**

Autocorrelation q(1) ≥ … ≥ q(6): proved exactly by writing each difference as a + b√21 and checking a² ≥ 21 b² (or both nonnegative); witnesses in `lm_prime.json`.

C_M(e) ≤ q(1) for all M ≥ 8:
- M = 8..13: finite exact check (24 cases), each a² − 21 b² > 0.
- M ≥ 14: q has support only up to lag 6, so C_M(e) ∈ {0, q(e)} ≤ q(1) by autocorrelation.
- Spot-extended through M = 40: 0 failures.

## 4. Certified inputs μ_n — PROVED

**Claim.** γ_{n'} > 6261/50000 for every n' = 2..8.
- n' = 2: H = h, gap 1.
- n' = 3,4,5,7: Higham certificates in all four (R,F) blocks at t = 6261/50000 (`open/arb/cert_n*_t6261_50000.json`); Σ k_b = 3.
- n' = 6: CERT_T0 certificates at t = 134/1000 > μ (`cert_t0/cert_n6_*_t134_1000.json`); Σ k_b = 3.
- n' = 8: CERT_T0 / CERT_T0_ARB at t = 6261/50000; Σ k_b = 3.

Exact VBS kernel: for each n' = 3..8, `kernel_exact.py` / `kernel9_exact.py` produce 3 (resp. 9) integer VBS vectors annihilated by all bonds, exact rank 3 in Sz = 0 (resp. 9 overall). Combined with Σ k_b = 3, dim ker H_{n'} = 9 exactly.

Residual recheck (CERT_T0_ARB path): all four blocks at n = 7 and n = 8 CERTIFIED; sample +++ blocks at n = 3,4,5 CERTIFIED; at n = 6 the residual sample in `open/arb/` is only 2 blocks ((+,+) and (−,−) at t = 134/1000). The load-bearing n = 6 input is the full four-block Higham suite in `cert_t0/`. Smallest residual λ_min lowers: n = 8 (−−) ≈ 2.75e-6, n = 7 (+−) ≈ 4.07e-5.

Negative controls:
- n = 7, t = 1255/10000: block (+,−) fails (info ≠ 0); first excitation lives there.
- n = 6, t = 135/1000: blocks (+,+) and (−,−) fail (CERT_T0).
- n = 3, t = 1605/10000: one block fails (float gap ≈ 0.1605).

Tighter direct certificates (used in the coverage table of §0):

| n | t certified | float ED |
|---|---|---|
| 3 | 16/100 | 0.160503 |
| 4 | 1495/10000 | 0.149562 |
| 5 | 1339/10000 | 0.133931 |
| 6 | 134/1000 | 0.134498 |
| 7 | 1254/10000 | 0.125414 |
| 8 | 6261/50000 | 0.125230 |

Why n = 8, not larger: float γ_9 ≈ 0.12007 < G(8) ≈ 0.12372, so μ_9 would fall below the threshold. NUMERICAL confirmation that n = 8 is the right finite-size choice.

## 5. Float ED sanity (NUMERICAL, not used in the proof)

`open/float_ed_open_3to10.json` (Sz = 0, dense/sparse ED):

| m | dim Sz=0 | #zeros | γ_m (float) |
|---|---|---|---|
| 3 | 19 | 3 | 0.160503 |
| 4 | 85 | 3 | 0.149562 |
| 5 | 381 | 3 | 0.133931 |
| 6 | 1751 | 3 | 0.134498 |
| 7 | 8135 | 3 | 0.125414 |
| 8 | 38165 | 3 | 0.125230 |
| 9 | 180325 | 3 | 0.120065 |
| 10 | 856945 | 3 | 0.118825 |

All lie well above the uniform bound 0.001226; the bound’s weakness is the LM threshold gap μ − G ≈ 0.0015, not a defect in the certificates. Open-chain gaps are **not** monotone (γ_6 > γ_5).

## 6. Final assembly

- m = 2: gap 1 (PROVED, trivial).
- m = 3..7: direct certificates of §4, all ≫ bound_lo (PROVED).
- m ≥ 8: Lemma LM′ + μ = 6261/50000 + F_lo, G_up of §3 (PROVED).
- Published LM Rem 2.6 covers m ≥ 16 as a special case; LM′ is what closes m = 8..15.

**No uncovered m.**

## 7. Adversarial self-check (quick)

Attack points checked:
1. *Wrong paper id.* Task cited 1810.02428; the open FF criterion is 1801.08915. Corrected; statements read from the fetched paper, not memory.
2. *GM Lemma 4 operator form.* Not used. LM Prop 4.6 uses the valid min-weight factor c_0. (The false equal-weight form is documented in AUDIT_ALLM.)
3. *Prop 4.4 at n > m/2.* Only change is C_M = q(e)+q(M−e); adjacent cancellation still holds for m ≥ n; PSD of non-adjacent products unchanged. Finite C_M check + autocorrelation cover all M ≥ 8.
4. *Prop 4.6 at n > m/2.* Proof uses m ≥ n for bulk windows, not m/2. We require m ≥ 8 = n.
5. *m = 7 via LM′.* Rejected: no bulk window at n = 8. Covered by direct cert instead.
6. *Edge-state splitting.* AKLT open kernel is exactly 9-fold (VBS); certificates count eigenvalues ≤ t above that kernel. Gap = first bulk excitation.
7. *μ_n input.* All of γ_2..γ_8 certified > μ; float γ_9 < G(8) explains why n = 8 is maximal useful.
8. *Trusted base overclaim.* Stated as IEEE-754 + E_build / Higham / residual, not arb. Same honesty fix as AUDIT_ALLM.
9. *Rational F,G.* Independent sympy derivation matches LM closed forms; convergent bounds checked by Fraction arithmetic.
10. *Negctl direction.* Certificates fail when t exceeds the float gap in the block that holds the first excitation.

**Verdict.** Theorem T_OPEN stands at the stated bound. The bound is weak (~50× below the float open gap) because μ − G(8) is only ~1.5e-3; improving it needs either a better open-boundary weight family or a larger certified n with G(n) < γ_n (blocked at n = 9 by float). That is a research limitation, not a proof gap.

## 8. Not covered / limitations

- Full arb-ball certificates (beyond residual rechecks already in CERT_T0_ARB for n = 6,8 and here for n = 7).
- Open KHH(1) corollary not re-audited.
- No claim about the infinite-volume open gap beyond the uniform finite-m bound (the bound already applies for every finite m, hence passes to the limit inferior).
- Periodic rings are CERT_ALLM, not this note.
- Human audit recommended for: the LM′ wrap-around step (§2 steps 2–3) and the claim that Prop 4.6’s proof never uses n ≤ m/2.

## 9. Proof-debt ledger

| item | status |
|---|---|
| LM Thm 2.5 / Rem 2.6 / Prop 4.4 / 4.6 read from paper | PROVED (citation) |
| Lemma LM′ | PROVED (written argument §2) |
| F, G, C_M, F_lo, G_up, bound_lo at n = 8 | PROVED (exact; `lm_prime.json`) |
| γ_{n'} > 6261/50000 for n' = 2..8 | PROVED (IEEE trusted base) |
| dim ker = 9 for open n' = 3..8 | PROVED (exact VBS + Σ k_b = 3) |
| direct certs m = 3..7 | PROVED |
| LM′ ⇒ all m ≥ 8 | PROVED |
| float ED m = 3..10 | NUMERICAL (sanity only) |
| KHH(1) open corollary | PROVED algebraically; not re-audited |
