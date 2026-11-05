# Spin-2 Heisenberg scoping and the spin-2 AKLT chain

Updated 2026-11-05 00:00 EST (America/New_York, UTC−5) / 2026-11-05 05:00 UTC.

This deposit adds [spin2/](spin2/) and [spin2_aklt/](spin2_aklt/) byte for byte from the supplied archive. Notes inside those trees refer to them as `runs/spin2` and `runs/spin2_aklt`. The status words below are the words written in those notes. This page does not rerun the calculations and does not strengthen any claim.

## Heat-trace bootstrap for the spin-2 Heisenberg chain

[spin2/FEASIBILITY.md](spin2/FEASIBILITY.md), [spin2/CW_SPIN1_TEST.md](spin2/CW_SPIN1_TEST.md), [spin2/LEAD2_PAPERCHECK.md](spin2/LEAD2_PAPERCHECK.md), and [spin2/NEW_IDEAS.md](spin2/NEW_IDEAS.md) screen the heat-trace bootstrap for the periodic spin-2 Heisenberg chain. With the methods checked there, the route is blocked.

`FEASIBILITY.md` states that no proof route closes with current tools. Lower bounds on \(Z_L\) are variational. The missing piece is a rigorous upper bound on \(Z_L\) at lengths about 250 to 600, at about \(10^{-6}\) per-site free-energy accuracy. Unless a line in that note says rigorous, its numbers are estimates from the three-magnon model or from floating-point diagonalization and Trotter products. Exact diagonalization is blocked past a full rigorous trace at \(L\le 8\). Lengths 9 and 10 are float only. Moment and Hankel extrapolation needs exact data near \(L\approx 100\) and is blocked. The ALT Trotter upper bound is valid in direction and blocked in evaluation. A matrix-product truncation can give a variational lower bound, while a rigorous upper bound is blocked. Schatten monotonicity, Berezin–Lieb, Temple–Kato, and the stated local-gate bound do not reach the required accuracy. Markov-entropy bounds are marked there as research.

`CW_SPIN1_TEST.md` records a failure of translation-invariant Collatz–Wielandt certificates on the Marshall-rotated spin-1 chain. The certificate is capped by the even-ring ground energy per site. The best certified bound in that test is \(e_0\ge -1.4362373172\), an error of \(3.48\times 10^{-2}\) per site against the nonrigorous reference. The note states that the method gives no usable upper bound on \(Z_L\). A \(10^{-6}\) per-site bound would need a support of at least about 47 sites for spin 1 and about 230 sites for spin 2.

`LEAD2_PAPERCHECK.md` uses the labels [proved], [lit], and [est]. The ring-ceiling argument for the local-marginal relaxations in scope is marked [proved] in that note. None of them escapes the ceiling. An infinite-volume free-energy lower bound converts to an upper bound on \(Z_L\) only with slack of order \(\beta\|h\|\), or else by using the spatial gap. The recommendation is to drop that route. The erratum leaves the verdicts unchanged.

`NEW_IDEAS.md` uses the labels PROVED, EXTERNAL-VERIFIED, PROVISIONAL, TESTED, DISPROVED, and BLOCKED. Log-convex interpolation is PROVED, and the spin-1 screen of that bound is TESTED and misses the purity the bootstrap needs. Packing sufficiency is PROVED in the spin-1 repository. Knabe, Gosset–Mozgunov, and Lemm–Mozgunov are EXTERNAL-VERIFIED and inapplicable to the Heisenberg chain because those criteria require frustration-free Hamiltonians. The best reformulation in that note still needs a rigorous finite-ring free-energy lower bound at lengths about 65 to 100, good to about \(10^{-5}\) per site, and that item is BLOCKED. The spin-2 residual ratios quoted there are TESTED.

## Moment no-go

[spin2/MOMENT_NOGO.md](spin2/MOMENT_NOGO.md) replaces the older claim that \(\rho_m<1\) is necessary for a moment certificate.

Theorem 1 is PROVED for one-sided data. If the data bound the relevant moments only from above, together with lower bounds at long lengths, and if \(\rho_M^+\ge 1\), then every certificate in the stated class is ruled out. Under the limits named in the theorem, the comparison spatial purity tends to \(1/2\). Short-length positivity of the twisted trace is a side condition of the statement.

Proposition 2 records that the old necessity claim is DISPROVED for exact two-sided data. The spectrum \(\{1\}\cup\{(9/10)\times 2\}\) has \(\rho_6=1.063\ge 1\) and is fixed by the exact moments \(m_4\), \(m_5\), and \(m_6\), so \(S(n)\) is determined. The check is exact in `toys.py`.

Theorem 3 is PROVED by exact rational counterexamples on the spin-1 intervals at \(\beta=49/4\). For data through length \(M\in\{6,7,8\}\), no certificate in the class proves \(S(32)>1/\sqrt{2}\). The comparison spectra have displayed values \(S(32)=0.50013\), \(0.4467\), and \(0.5780\). The summary line of the note rounds these to \(0.500\), \(0.447\), and \(0.578\). For \(M=10\), no certificate proves \(S(16)>1/\sqrt{2}\), and \(S(32)\) is not settled. `verify.py` checks the intervals, anchors, sector weights, positivity, and these purities in exact rational arithmetic.

A general two-sided threshold is BLOCKED. The spin-2 conclusion is an ESTIMATE. The note calls it a heuristic consequence. There are no rigorous spin-2 intervals, so Theorem 3 is not run there. The note estimates \(\ln\rho_8\) at about \(8.61\) for \(\beta=20\) and about \(24.18\) for \(\beta=56\). The ledger labels that line TESTED / ESTIMATE.

## Spin-2 AKLT chain

[spin2_aklt/SCOPING.md](spin2_aklt/SCOPING.md) uses the labels PROVED, NUMERICAL, and HEURISTIC. The family is

$$
H(\alpha)=\sum_i\left[x+\alpha\left((2/9)x^2+(1/63)x^3+10/7\right)\right],
$$

with \(x=\mathbf S_i\cdot\mathbf S_j\) for spin 2. Here \(\alpha=0\) is the Heisenberg chain and \(\alpha=1\) is the AKLT chain. The note records the exact identity \(H(1)=\sum 10(P_3/7+P_4)\).

The bootstrap's sufficient transfer construction is PROVED inapplicable to \(\mathrm{KHH}(\alpha)\) for every \(\alpha\in(0,1]\) and every real structure. The same inertia count excludes every valence-bond-solid parent \(aP_3+bP_4\) with \(a,b\ge 0\), except the ray \(b=35a/9\), which the count leaves open. A NUMERICAL search on that ray found no working structure and does not prove that none exists. The scoping note states that failure of this sufficient construction leaves the transfer identity itself open. Small-ring spectra in that note are NUMERICAL. The correlation-length reading and the claim of no published explicit one-dimensional spin-2 bound are HEURISTIC.

[spin2_aklt/CERT_T0.md](spin2_aklt/CERT_T0.md) and [spin2_aklt/CERT_T0_ARB.md](spin2_aklt/CERT_T0_ARB.md) certify the open chain with bond \(h=P_3+P_4\). The exact ground-space dimension is 9. The smallest positive eigenvalue of the open 8-site chain satisfies \(\varepsilon_8>6261/50000\). Gosset–Mozgunov, Theorem 3, then gives, for every periodic length \(m\ge 17\),

$$
\mathrm{gap}(H_m^\circ)\ge\varepsilon_8-1/12>6283/150000.
$$

For the \(\mathrm{KHH}(1)\) chain the same lengths satisfy \(\mathrm{gap}\ge 6283/105000\). A bond \(a_3P_3+a_4P_4\) is bounded by \(\min(a_3,a_4)\cdot 6283/150000\). Periodic lengths \(m\le 16\) remain OPEN. The infinite-volume reading is marked HEURISTIC-standard and is not written out.

The positivity step uses the trusted base in `CERT_T0_ARB.md`. That base assumes IEEE-754 binary64, round to nearest, for the explicit GEMMs and absolute sums named there, with Higham \(\gamma_n\) bounds and classical non-Strassen evaluation. The kernel dimension, the projector identity, the SU(2) reduction, and the Gosset–Mozgunov hypotheses stay on exact arithmetic or on the fetched paper statement. The LAPACK Cholesky rounding model is outside this trusted base.

[spin2_aklt/QTM_TEST.md](spin2_aklt/QTM_TEST.md) states that all of its results are NUMERICAL. In the recorded runs the leading quantum-transfer-matrix eigenvalues are real, while subleading complex-conjugate multiplets appear for \(\mathrm{KHH}(1)\), the ray \(b=35a/9\), and \(\mathrm{KHH}(0.9)\) at \(\beta=4\). Those multiplets strengthen under the Trotter refinements that were computed. The note calls a real self-adjoint finite transfer operator numerically contradicted for the full spectrum of \(\mathrm{KHH}(1)\) and that ray, at the finite \(\beta\) and slice numbers tested. The further remark that the discrepancy is exponentially small for a large-length bootstrap is labeled HEURISTIC. Inverse temperatures with \(\beta\Delta\gtrsim 5\) were not reached.

## Check performed for this deposit

The archive contained no `__pycache__` entry and no file above 50 MB. The largest deposited file is `spin2_aklt/spec_KHH_1_L7.npz`, at 690572 bytes. Every Python source under this directory was parsed with `python -m py_compile` on 2026-11-05. No spectrum, certificate, or search was rerun.
