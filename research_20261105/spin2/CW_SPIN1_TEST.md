# Lead 1 filter test: Collatz–Wielandt (CW) bounds on the Marshall-rotated spin-1 chain

**Verdict: FAIL.** Translation-invariant local CW certificates have a provable ceiling:
μ ≤ min over even rings p ≥ (certificate support) of E0(p)/p.
- The optimal certificates I tested sit exactly at that ceiling.
- Reaching 1e-6 per site would need a support of ≳ 47 sites for spin-1, or ≳ 230 for spin-2. The certification state space grows as 3^(2k−1), so that is infeasible.
- Even a perfect E0 bound would not bound Z_L.

Reference value: e0 = −1.401484038971 (DMRG, **nonrigorous**).
Scripts and data are in `runs/spin2/cw/`.

## 1. Theory

**Sign rotation.** Let U = Π_{j odd} e^{iπS^z_j}. On odd sites it maps S^x → −S^x and S^y → −S^y.
- Each bond becomes h = S^zS^z − ½(S⁺S⁻ + S⁻S⁺).
- For spin-1, every off-diagonal element in the S^z basis equals −½·(√2·√2) = −1 ≤ 0. So H is stoquastic.
- The rotation needs a bipartite lattice: open chains, the infinite chain, or **even** periodic L. Odd rings are frustrated.

**CW inequality.**
- If H has nonpositive off-diagonals and v > 0 entrywise, then E0(H) ≥ min_x (Hv)_x / v_x.
- Proof: M = c − H is entrywise nonnegative and symmetric, so λ_max(M) = ρ(M) ≤ max_x (Mv)_x / v_x. No irreducibility is needed.

**Per-site version (Jastrow test vectors).**
- Take log v(x) = Σ_i θ(x_i … x_{i+k−1}), with 3^k free parameters.
- The bond term e_b(x) = z_i z_{i+1} − Σ_{flips x'} v(x')/v(x) depends only on the 2k sites around the bond. So the local energy (Hv)_x/v_x is a sum of local terms, and min_x is a minimum-mean-cycle problem on the de Bruijn graph whose states are windows of 2k−1 sites.
- The dual certificate is potentials φ with e(edge) + φ(src) − φ(dst) ≥ μ for every edge. Any closed walk then has mean ≥ μ.
- This gives E0(L) ≥ Lμ for every even L ≥ k+1, and hence e0 ≥ μ.
- **Maximizing μ over (θ, φ) is a convex program**, because every constraint has the form affine − Σ exp(affine) ≥ μ. The optimum within the Jastrow-k class is therefore global.

**No-go for translation-invariant local certificates (rigorous given the stated E0(p) values).**
- Suppose a certificate's local rules make sense on every ring of length p ≥ W. For Jastrow-k, W = k+1.
- A period-p configuration in the graph then *is* a valid CW certificate on ring p. So its mean is ≥ μ only if E0(p)/p ≥ μ.
- Hence **μ ≤ min_{even p ≥ W} E0(p)/p.**
- For even p, E0(p)/p lies below e0 (ED: −1.5, −1.43624, −1.41712, −1.40941, −1.40580 for p = 4…12). The finite-size (Lüscher) deficit decays like e^{−p/ξ}.
- Consequence: error ≥ e0 − E0(W)/W. A 1e-6 bound needs W ≳ 47 (spin-1; free-magnon model gives 6.5e-6 at p=40 and 1.3e-7 at p=60). Spin-2 needs W ≳ 230 (model gives 5.1e-6 at p=200 and 3.0e-8 at p=400).
- Nearest-neighbour hidden-variable (MPS-lift) certificates have W = 2. That is, v = Σ_a Π W(a_i, x_i, a_{i+1}) with local stochastic redistribution of the flip mass over the hidden variable. On a 2-site ring, H_2 = 2 S_1·S_2 has E0/site = −2, so these give **at best the trivial bound −2**. Product states (k=1) give exactly this; see the table.

## 2. Results (certified with python-flint arb at 128 bits; θ and φ rounded to exact dyadic rationals)

| k (Jastrow window) | certified μ ≤ e0 | error vs e0 | ceiling min_{even p≥k+1} E0(p)/p (ED) | solve time |
|---|---|---|---|---|
| 1 | −2.0000000002 | 0.599 | −2 (p=2) | <0.1 s |
| 2 | −1.5436890137 | 0.142 | −1.5 (p=4) | <0.1 s |
| 3 | −1.5000000086 | 0.0985 | −1.5 (p=4), **saturated** | <0.1 s |
| 4 | −1.4406495833 | 0.0392 | −1.4362372 (p=6) | 2 s |
| 5 | −1.4362373172 | 0.0348 | −1.4362372 (p=6), **saturated to 1.2e-7** | 55 s |
| 6 | not obtained | — | ≤ −1.41712 (p=8); error would be ≥ 0.0156 | killed at 8 min (531k edges; memory/CPU cap) |

- **Best certified bound: e0 ≥ −1.4362373172 (k=5). Its error is 3.48e-2 per site**, about 3×10⁴ times too large.
- The optimizer drives the bound to the ring ceiling: the minimizing configurations are short-period, as the no-go predicts.
- Edges number 3^(2k), so k=6 is the practical limit under the 600 s cap.

## 3. Brute-force cross-check (float, sanity only)
- For each k and each even ring L = 4…10 with L ≥ k+1, I enumerated all 3^L configurations and computed min_x (Hv)_x / (L v_x).
- In all 18 cases, μ_cert ≤ ring minimum ≤ E0(L)/L from ED (`cw/bruteforce.json`). The ring minimum equals μ to ~1e-10, i.e. it is attained on short-period configurations.

## 4. Scaling and judgement
- **Accuracy is set by the support W, not by how expressive the vector is:** error ≈ e0 − E0(W)/W ~ e^{−W/ξ}.
- Exact min-plus certification costs ≥ 3^(2W−3) states for Jastrow. Hidden variables do not escape this: any certificate whose rules fit on a ring of length p is capped by E0(p)/p.
- For 1e-6 per site you need W ≳ 47 for spin-1 and ≳ 230 for spin-2. This is **infeasible by many orders of magnitude.**
- **Loophole (not tested).** Non-translation-invariant certificates with period q are valid only on rings whose length is a multiple of q, so their ceiling is E0(q)/q. But such a certificate must itself be a near-exact CW certificate on a ring of size q ≳ 47 (spin-1) or ≳ 230 (spin-2). That is the original finite-L E0 lower-bound problem again, with a worst-case (min over 3^q configurations) error criterion. No progress.
- **Z bounds.** CW controls only the spectral radius.
  - On e^{−βH} (nonnegative in the rotated basis for even L) it bounds λ_max = e^{−βE0} again.
  - On the spatial transfer operator X it bounds ‖X‖. Then Z_n ≤ ‖X‖^{n−k} Tr X^k loses about βk(e0 − E0(k)/k) unless k ≳ ξ·ln(1/ε). For spin-2, k = 8 gives a loss of about 28 in ln Z at β=64. A CW bound on X also hits the same ring obstruction.
  - With only an E0 bound, Z ≤ dim·e^{−βE0} loses L·ln 3 (spin-1) or L·ln 5 (spin-2) in ln Z.
  - **CW gives no usable Z_L upper bound.**

## 5. Recommendation
Drop lead 1. The no-go shows it is the same Lüscher/finite-size barrier as the Anderson and local-gate bounds, in exponential rather than 1/L form. Each certificate is still capped by its own ring size. If upper bounds are pursued, the next candidate is lead 2 (SDP / Markov-entropy free-energy bounds). It should be screened against the same ceiling before any compute is spent: a support-W relaxation that is exact on rings of size ≥ W is capped in exactly the same way.

Files in `runs/spin2/cw/`:
- `cw_jastrow.py`: convex solve.
- `cw_certify.py`: arb certificate.
- `cw_bruteforce.py`: L ≤ 10 check.
- `jastrow_k*.json`, `cert_k*.json`, `bruteforce.json`, `k6.log`.
