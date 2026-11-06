# Proof-chain audit and independent thermal enclosures

Updated 2026-11-04 13:20 EST (America/New_York, UTC−5) / 2026-11-04 18:20 UTC.

For the periodic spin-1 Heisenberg chain, [proof_audit/PROOF_CHAIN.md](proof_audit/PROOF_CHAIN.md) records an end-to-end argument that the ground state is unique and the gap is at least $2497/100000$ for every integer length $L\ge 2$. Two steps that the repository had stated without a proof now have written proofs. [thermal_arb/STATUS.md](thermal_arb/STATUS.md) records an independent ball-arithmetic recomputation of all 18 thermal inputs. Each enclosure lies strictly inside the repository's refined interval, so those inputs no longer rest on the producer's C++ kernel. Uniqueness of the infinite-volume ground state remains unproved and is not claimed.

The deposited copies are [proof_audit/](proof_audit/) and [thermal_arb/](thermal_arb/). Citations inside `PROOF_CHAIN.md` that point into `research_20261010/` or into the watertight record are unchanged. This branch starts from commit `a99fa21`, the commit named in that audit. Nothing outside `research_20261104/` is modified.

## Hamiltonian and claim

The Hamiltonian is

$$
H_L=\sum_{i=1}^{L}\mathbf S_i\cdot\mathbf S_{i+1},
$$

with $\mathbf S_{L+1}=\mathbf S_1$, spin 1, and full Hilbert space $(\mathbb C^3)^{\otimes L}$. The gap $\Delta_L=E_1-E_0$ is the gap in that full space. No symmetry sector is omitted from the claim. The constants are $a=700741/500000$ and $\beta_0=49/4$, and the shifted trace is

$$
Z_L(\beta)=\operatorname{Tr}\exp\bigl(-\beta(H_L+aL)\bigr).
$$

The claim in `PROOF_CHAIN.md` is that for every integer $L\ge 2$ the ground state is unique and $\Delta_L\ge\gamma$ with $\gamma=2497/100000$. The repository itself certifies $31/1250=0.0248$ in [research_20261010/uniform_gap_0248_all_sizes_review](../research_20261010/uniform_gap_0248_all_sizes_review). The value $2497/100000$ is the 12-window rerun of the same $n=34$ chain, named there as `runs/seal12`. That rerun was accepted by the repository's `audit_scalar.py` and all-sizes `audit.py` in the $Z>1$ mode. `PROOF_CHAIN.md` states that the only edits were plumbing for an environment-selectable certificate, gap, output, and rounding grid $B$, and that in $Z>1$ mode the mathematical checks are byte-identical to the repository's.

## Proof chain

The statuses below are the statuses written in `PROOF_CHAIN.md`. The thermal recomputation in the next section removes the producer's C++ kernel from the trust statement of step 6. The other computer-checked steps were not rerun for this deposit.

| Step | Statement | Status in `PROOF_CHAIN.md` |
| --- | --- | --- |
| 1 | $L=2$ has $H_2=S^2-4$, levels $-4$, $-2$, and $2$, a unique ground state, and gap $2$. $L=3$ has $H_3=(S^2-6)/2$, total spin $0,1,2,3$ with multiplicities $1,3,2,1$, a unique ground state, and gap $1$. | PROVEN (by hand, rechecked) |
| 2 | If the purity $p$ satisfies $p\ge C>1/2$, the ground state is unique, and $\Delta\ge\gamma$ whenever $C-e^{\beta\gamma}(1-C)>0$. Even and odd $L$ are treated in the full space. | PROVEN (written, repository proof files, rechecked) |
| 3 | For any nonzero trial state, $Z_L(2\beta)\ge e^{-2\beta R_L}$. The trials are bond-dimension $26$ matrix-product anchors, with pairs $(H0_L,N0_L)$ at $L=4,\ldots,33,48,60,64,68$. An independent FLINT transfer matrix matches all $33$ pairs exactly. | PROVEN and PROVEN-BY-COMPUTER |
| 4 | $Z_L(\beta)=\operatorname{Tr} X_\beta^L$ for a real symmetric Hilbert–Schmidt operator $X_\beta$, for every $L\ge 2$. The cited write-up covers only the untwisted trace. | PROVEN |
| 5 | $J_L=(Z_L+3P_L)/4$, $N_L=(Z_L-P_L)/4$, and $Z_L=J_L+3N_L$. The repository stated this without a proof. | Closed by the written argument in section 2.1 of `PROOF_CHAIN.md` |
| 6 | Eighteen two-sided intervals for $Z_L$ and $P_L$, at $L=4,\ldots,12$ and $\beta_0$. The $P$ seam flips the signs of $S^x$ and $S^y$ on the closing bond. | PROVEN-BY-COMPUTER, at that writing still trusting the producer's C++ integer kernel |
| 7 | Sector moments for powers $4$ through $12$, and the support caps $-0.6501774659<\lambda_J<1.0013390453$ and $-0.8710299903<\lambda_N<0.7502278231$. The moment-review replay returned CONDITIONALLY ACCEPTED in $13.6$ CPU seconds. The condition is the physical input from step 6. | PROVEN-BY-COMPUTER (exact rationals) |
| 8 | Bernstein and de Casteljau majorants on the closed caps, and the packing lemma for powers of bounded nonnegative summands. | PROVEN (lemma) and PROVEN-BY-COMPUTER (instances) |
| 9 | At $n=34$, if no eigenvalue of $X_0$ exceeded the trial threshold, packing would give $Z_{68}<1$. That contradicts step 3, because $R_{68}<0$ implies $Z_{68}\ge 1$. The forcing value recorded with the chain is $R_{68}\approx -8.3\times 10^{-6}$. | PROVEN-BY-COMPUTER |
| 10 | The exchange recursion $S'=G(S^2 T)$ and $T'=G(T^2 S')$, with $G(x)=1-(1-x)^2/(2x^2)$, at $(2n,2\beta)$. | PROVEN (repository proof, derivation rechecked) |
| 11 | From $K=S^2 T>1/2$, the window formulas give purity at least $C$ for every integer length in $[n,2n]$. | PROVEN (rechecked) |
| 12 | Twelve dyadic windows $n_j=34\cdot 2^j$ for $j=0,\ldots,11$, at $\beta_j=2^j\beta_0$, with outward rounding on the grid $B$. The seal12 log is accepted for gap $2497/100000$, with the asymptotic regime beginning at length $69632$. | PROVEN-BY-COMPUTER |
| 13 | If $u=\max(1-S,1-T)\le 1/100$, then $u_{j+1}\le 5u_j^2$ and $C\ge 1-4u$. Together with step 12 this covers every $L\ge 34$. The tail statement itself covers $L\ge 69632$. | PROVEN (written) |
| 14 | The finite prefix $L=4,\ldots,33$ meets the same margin test at $\gamma$. Lengths $4$ through $12$ use the untwisted thermal inputs. Lengths $13$ through $23$ use signed degree-$8$ majorants. Length $24$ uses the isolated $n=24$ window and anchor $48$, with $C\approx 0.681$. Length $25$ uses Cauchy–Schwarz on the spectrum of $X$, with $C\approx 0.7059$. Lengths $26$ through $33$ use their own matrix-product numerators. The all-sizes log is accepted. The direct-$25$ review has an unresolved resource anomaly of $25.96$ CPU seconds against a $15$ second limit. That anomaly is not mathematical. | PROVEN-BY-COMPUTER |
| 15 | The union of $\{2,3\}$, $[4,33]$, the twelve windows, and the tail is every integer $L\ge 2$. | PROVEN |
| 16 | (a) $\liminf_L\Delta_L\ge\gamma$. (b) Every weak-$*$ limit of the periodic ground states has GNS gap at least $\gamma$. (c) Uniqueness of the infinite-volume ground state among all states, and convergence of the finite-volume ground states. | (a) PROVEN. (b) Closed by the written argument in section 2.2 of `PROOF_CHAIN.md`. (c) NOT PROVEN, and not claimed |

The links recorded with the chain are these. Step 3 feeds step 9 through $R_{68}\approx -8.3\times 10^{-6}<0$. Steps 4 and 5 identify the caps as statements about the spectra of the sector operators, with $Z=J+3N$. Step 6 supplies exactly the $18$ inputs that `check_provenance.py` maps to the moment intervals. Steps 9 through 11 start at $n=34$ and $\beta_0$, and the recursion doubles both the length and the inverse temperature. Step 11 feeds step 2 because $C>1/2$ in every window. Step 13 uses $u\le 1/100$ at the last window. Step 14 uses $\beta_0=49/4$ and the margin test of step 2. Periodic boundary conditions are essential. Open chains have spin-$1/2$ edge states, and nothing in this chain applies to them.

## Two closed steps

### Twisted trace and sector decomposition

`PROOF_CHAIN.md` records that the repository had stated the identities of step 5 by inheritance, without a proof, at `heat_trace/audit_inputs/APPENDIX_A_BRIDGE.md` lines 23–35 and in the thermal proof. The written closure uses the Cartesian basis $(A_\alpha)_{jk}=\varepsilon_{\alpha jk}$ and $S_\alpha=-i A_\alpha$. The diagonal matrix $R=\operatorname{diag}(-1,-1,1)$ is the $\pi$-rotation about $z$. The twisted seam inserts the sign $\varepsilon^z=(-1,-1,+1)$ on each seam mark, so the twisted trace is $\operatorname{Tr}(U_z X^L)$.

The same conjugation shows that $U_z$ commutes with $X$ and that $U_z^2=1$. The three sign patterns $\varepsilon^x=(+,-,-)$, $\varepsilon^y=(-,+,-)$, and $\varepsilon^z=(-,-,+)$ give commuting involutions $\{1,U_x,U_y,U_z\}$ isomorphic to the Klein four-group, and each commutes with $X$. The cyclic permutation of the axes is a proper rotation. It preserves the kernel and cycles the three nontrivial sectors, so those three sector traces are equal. The resulting identities are the repository formulas $J=(Z+3P)/4$ and $N=(Z-P)/4$.

### Gap for every weak-$*$ limit in infinite volume

`PROOF_CHAIN.md` records that the repository README had disclaimed an infinite-volume statement, so part (b) of step 16 was absent. The written closure starts from the unique finite-volume ground state $\psi_L$ and the state $\omega_L=\langle\psi_L,\cdot\,\psi_L\rangle$. For every observable $A$,

$$
\omega_L(A^*[H_L,A])\ge\gamma\bigl(\omega_L(A^*A)-|\omega_L(A)|^2\bigr),
$$

because the finite-volume gap is at least $\gamma$ above the simple ground state. For $A$ supported on an interval of radius $r$ and for $L>2r+2$, the commutator equals the length-independent finite-range derivation. Weak-$*$ limit points exist by Banach–Alaoglu. Each such limit $\omega$ is translation invariant and inherits the quadratic-form inequality. In the GNS representation the local vectors are analytic for the GNS Hamiltonian, by the finite-range bound in Bratteli–Robinson, Theorem 6.2.4, and they form a core by Nelson's theorem. The form inequality therefore extends, and

$$
H_\omega\ge\gamma\bigl(1-|\Omega\rangle\langle\Omega|\bigr).
$$

The kernel is the vacuum line, and the spectrum lies in $\{0\}\cup[\gamma,\infty)$.

Part (c) stays open. The argument does not prove that $\omega$ is the only infinite-volume ground state, including states that are not translation invariant or that come from other boundary conditions. It does not prove that $\omega_L$ converges, and it does not prove that $\omega$ is pure. Those statements are not claimed.

## Independent thermal inputs

`thermal_arb/STATUS.md` records a separate recomputation of

$$
Z_L^g=\operatorname{Tr}\exp\bigl(-\beta_0(H_L^g+aL)\bigr)
$$

for $L=4,\ldots,12$ and $g\in\{I,P\}$, with the same $\beta_0=49/4$ and $a=700741/500000$. The untwisted seam is $I$. The twisted seam $P$ is the closing bond with the signs of $S^x S^x$ and $S^y S^y$ flipped. The status of that recomputation is that all $18$ rigorous enclosures lie strictly inside the repository `refined_rounded_interval` values, and therefore inside the coarse windows of half-width $3\times 10^{-5}$.

The sparse integer Hamiltonians were rebuilt as the repository byte streams $D=(32-3n)I-2H$. They reproduce every SHA-256 in [research_20261010/uniform_second_thermal_full_review](../research_20261010/uniform_second_thermal_full_review) `matrix_L4.json` through `matrix_L12.json`, for both seams and every moment order $M\ge 0$. The comparison is `digest_check.py` together with `digest_moments.json`. The integer matrices are therefore the repository matrices. Exact integer moments $\operatorname{Tr}(H^g)^j$ from the full sparse matrix, with $j\le 4$ for $L\le 10$ and $j\le 3$ for $L=11,12$, lie in the enclosed power sums of the certified spectra.

Each enclosure is a theorem given FLINT and arb, together with exact integer arithmetic. The blocks are exact Bloch blocks at $128$ bits. Weyl and Ostrowski supply one enclosure per eigenvalue from a trial pair $(V,\Lambda)$, using $\lVert B+L/2\rVert\le 3L/2$. That operator bound holds because every bond, twisted or not, has spectrum $\{-2,-1,1\}$. Three modes compute the Gram and residual defects. The `hp` mode covers $333$ blocks with dimension at most $40$, using an mpmath trial and an exact `fmpz_mat` defect. The `exact` mode covers $359$ blocks with dimension from $41$ through $3000$, using a LAPACK trial and an exact `fmpz_mat` defect. The `float` mode covers the remaining $54$ blocks, all at $L=12$ with $S^z\in\{0,1,2,3\}$ and dimension above $3000$. Those $54$ blocks use IEEE binary64 products. Their error bounds are a priori. The trial vectors are not trusted. Only the exact defects, or the a priori float bounds, enter the theorem.

The table below is the results table in `thermal_arb/STATUS.md`. The relative margins are $(Z_{\mathrm{lo}}-\mathrm{repo\_lo})/\mathrm{repo\_hi}$ and $(\mathrm{repo\_hi}-Z_{\mathrm{hi}})/\mathrm{repo\_hi}$.

| case | repo refined interval | our rigorous enclosure | our rel. radius | margin lo / hi | contained | suffices downstream |
| --- | --- | --- | --- | --- | --- | --- |
| L4_I | [124.8853798264238, 124.8853798268525] | [124.885379826638506, 124.885379826638506] | 8.4e-37 | 1.7e-12 / 1.7e-12 | yes | yes |
| L4_P | [0.06575703547748390, 0.06575703548732130] | [0.06575703548240392, 0.06575703548240392] | 9.2e-37 | 7.5e-11 / 7.5e-11 | yes | yes |
| L5_I | [0.002925182678780198, 0.002925182688159524] | [0.00292518268346975, 0.00292518268346975] | 2.1e-36 | 1.6e-09 / 1.6e-09 | yes | yes |
| L5_P | [2.960742995594862, 2.960742995893260] | [2.96074299574405557, 2.96074299574405557] | 2.1e-36 | 5.0e-11 / 5.0e-11 | yes | yes |
| L6_I | [12.87061404889128, 12.87061405228679] | [12.8706140505890111, 12.8706140505890111] | 3.4e-36 | 1.3e-10 / 1.3e-10 | yes | yes |
| L6_P | [0.2865996490525385, 0.2865996495592301] | [0.28659964930588783, 0.28659964930588783] | 3.7e-36 | 8.8e-10 / 8.8e-10 | yes | yes |
| L7_I | [0.05406952271997903, 0.05406952383788854] | [0.05406952327876386, 0.05406952327909726] | 3.1e-12 | 1.0e-08 / 1.0e-08 | yes | yes |
| L7_P | [1.920414791860990, 1.920414798523347] | [1.92041479518593435, 1.92041479519817387] | 3.2e-12 | 1.7e-09 / 1.7e-09 | yes | yes |
| L8_I | [4.639283417984037, 4.639283475100072] | [4.63928344651155430, 4.63928344657308013] | 6.6e-12 | 6.1e-09 / 6.1e-09 | yes | yes |
| L8_P | [0.5101407266224009, 0.5101407455622971] | [0.51014073608878410, 0.51014073609598714] | 7.1e-12 | 1.9e-08 / 1.9e-08 | yes | yes |
| L9_I | [0.1954550355787458, 0.1954550986348204] | [0.19545506710424221, 0.19545506710944440] | 1.3e-11 | 1.6e-07 / 1.6e-07 | yes | yes |
| L9_P | [1.514846900354352, 1.514847075899103] | [1.51484698810480648, 1.51484698814846758] | 1.4e-11 | 5.8e-08 / 5.8e-08 | yes | yes |
| L10_I | [2.654822445716474, 2.654823714326909] | [2.65482307994627326, 2.65482308009727472] | 2.8e-11 | 2.4e-07 / 2.4e-07 | yes | yes |
| L10_P | [0.6754193864435276, 0.6754200263217818] | [0.67541970636489511, 0.67541970640051203] | 2.6e-11 | 4.7e-07 / 4.7e-07 | yes | yes |
| L11_I | [0.3776280450198119, 0.3776306448351835] | [0.37762934490240360, 0.37762934495077063] | 6.4e-11 | 3.4e-06 / 3.4e-06 | yes | yes |
| L11_P | [1.314541759963492, 1.314546610583277] | [1.31454418518940770, 1.31454418535468830] | 6.3e-11 | 1.8e-06 / 1.8e-06 | yes | yes |
| L12_I | [1.900531549299379, 1.900563579253822] | [1.90054472271147625, 1.90055040440590852] | 1.5e-06 | 6.9e-06 / 6.9e-06 | yes | yes |
| L12_P | [0.7873950532568925, 0.7874156698136163] | [0.78740418547160484, 0.78740653657015269] | 1.5e-06 | 1.2e-05 / 1.2e-05 | yes | yes |

Every row is contained, and every row suffices for the downstream inequalities. The tightest row is `L12_I`. Its relative radius is $1.5\times 10^{-6}$, from the float mode, and the margin on each side is $6.9\times 10^{-6}$.

Because every enclosure lies inside the refined endpoints, the downstream comparisons in `check_provenance.py` and in `uniform_second_moment_optimization` hold independently of the producer's C++ integer kernel. Those comparisons use the $J$ and $N$ moment intervals built from the refined endpoints. The kernel and its outputs $W$ and the endpoints remain comparison targets only. They are no longer part of the trusted base for these $18$ inputs.

The original production took about $1$ hour $25$ minutes of wall time, from 10:50 to 12:15 CST on 4 November 2026, on $4$ to $6$ single-threaded processes, and about $4.7$ CPU hours. About $3.1$ of those hours were the $L=12$ eigensolver, and about $1.6$ hours were block building and certification. This deposit did not rerun that eigensolver.

### Reassembly from the saved block certificates

`STATUS.md` states that `python3 assemble.py` rebuilds $Z$ from the saved block certificates in seconds. On 2026-11-04 this checkout ran that command in `research_20261104/thermal_arb/`, with `HALDANE_REPO` set to the repository root. The interpreter had python-flint 0.9.0, which is the version named in `STATUS.md`. The run finished in $1.896$ seconds and did not call the eigensolver.

All $18$ cases printed `INSIDE`. The script rewrote `results.json`. That rewrite matched the deposited file on all $18$ records, including `inside_refined`, `inside_coarse_window`, `moments_contain_exact`, and `digests_match`. The deposited file was left in place. Its SHA-256 is `ef967d1f4dc8cf84bccff9ad638ed05877724fc772d354089b396fe2f445359c`. The $L=12$ mode counts in the reprint were $28$ float blocks for $I$ and $26$ float blocks for $P$, which is the count of $54$ float-mode blocks in `STATUS.md`.

## Remaining trusted base

After the thermal recomputation, `STATUS.md` leaves the following trusted for the $18$ inputs.

- FLINT and arb through python-flint 0.9.0, for ball arithmetic and for `fmpz_mat`.
- CPython integers. mpmath is used only to build trial vectors in the `hp` mode, and those trials are not trusted.
- The NumPy and SciPy integer sparse construction of $H$. It is cross-checked against the repository SHA-256 digests, so the residual trust is that a SHA-256 collision does not occur.
- The symmetry reduction in `blocks.py`. Its algebra is checked by exact integer identities for the twisted translation, the spin flip, and $S^z$ conservation, by the count of block dimensions times multiplicities against each sector and against $3^L$, by containment of the exact moments, and by a floating-point full-spectrum match at $L=4$ and $L=5$.
- For the $54$ blocks at $L=12$ with dimension above $3000$, correctly rounded IEEE-754 binary64 arithmetic, including `dgemm`, and the absence of a Strassen-type product in OpenBLAS 0.3.34. The stated model is Higham's standard model. It bounds $|\mathrm{fl}(x^\top y)-x^\top y|$ by $\gamma_n |x|^\top|y|+n\cdot 2^{-1074}$ for any summation order, with or without fused multiply-add. Sums of squares are bounded by $\mathrm{fl}/(1-\gamma_N)+N\cdot 2^{-1074}$. The diagonal subtraction is exact by Sterbenz, and that identity is asserted. On $4$ blocks with dimensions from $323$ to $902$, the float-mode enclosures intersect the exact-mode enclosures and are $500$ to $2000$ times wider.
- The Weyl and Ostrowski theorem, and the bond-spectrum bound used to control $\lVert B+L/2\rVert$.

`PROOF_CHAIN.md` still records a separate trusted base for the non-thermal steps. That base is CPython `int` and `Fraction` arithmetic, the repository audit scripts read line by line, the hand proofs named in its section 3, and the SHA-256 seals discussed below. The sequential GMP contraction of the $33$ anchors is redundant for the anchor check, because python-flint 0.9.0 reproduces every pair. Floating-point `eigh` appears only in the non-proof sanity checks, which put all $14$ traces at $L=4,\ldots,10$, for both seams, inside the repository intervals. `PROOF_CHAIN.md` records the integer Horner error lemma, with column error $E_L=281(d_L+1)+1$ and Poisson truncation at degree $280$, as repository-proved for the older thermal method. The audit checked that lemma for plausibility and did not re-derive it digit by digit. The enclosures in `thermal_arb/` do not use that kernel.

## Seal checks on a fresh checkout

`PROOF_CHAIN.md` states that seal checks fail on a fresh checkout of git HEAD, because README and other Markdown files were edited after sealing. The sealed archive copy `watertight/auditor/orig_audit` differs from HEAD only in Markdown files. A recursive quick diff showed no non-Markdown differences, and the replays pass on that sealed copy. Replaying a sealed certificate is not a new gap theorem.

## Where this pull request meets the watertight record

This branch does not contain `research_20261104/watertight/`. That tree is the open watertight pull request. Two citations in `PROOF_CHAIN.md` point there.

Step 4 cites `watertight/transfer_operator.md` for the untwisted identity $Z_L(\beta)=\operatorname{Tr} X_\beta^L$. On the watertight branch that file is `research_20261104/watertight/transfer_operator.md`.

Steps 12 and 14 cite `runs/seal12/audit_scalar_Z1.log` and `runs/seal12/audit_allsizes_Z1.log` for the acceptance of gap $2497/100000$. On the watertight branch those logs are `research_20261104/watertight/seal12/audit_scalar_Z1.log` and `research_20261104/watertight/seal12/audit_allsizes_Z1.log`. `PROOF_CHAIN.md` states that this acceptance is the $Z>1$ mode and that its mathematical checks are byte-identical to the repository checker. The watertight record calls the same acceptance an original-checker acceptance, with file-name, affinity, gap-literal, and rounding-grid substitutions only.

The patched checker is a different program. The watertight record identifies it as `seal12/auditor_changes.diff`. That patch replaces the hypothesis $Z_{2n}>1$ by the Jensen bound at the anchor Rayleigh quotient, and the watertight record states that gap $25177/1000000$ and the decimal $0.025179$ are accepted only by that patched checker. `PROOF_CHAIN.md` and `STATUS.md` do not assign $\gamma=2497/100000$ to the patched checker. This pull request depends on the patched checker only for a statement that one of those sources, or the watertight record they cite, explicitly assigns to the patched checker. The gap $2497/100000$ is not such a statement.

## What was deposited

Both uploaded archives were extracted in full under `research_20261104/`. Neither archive contained `__pycache__`, a `cache/` directory, or a scratch repository copy. No file was omitted for size. The largest deposited file is `thermal_arb/enc/I_L12_sz0_q8.json`, at $296196$ bytes, which is far below $50$ MB. A `__pycache__` directory created locally by importing `blocks.py` during the reassembly was deleted and is not part of the deposit.

The proof-audit files are the chain write-up, the anchor checker and its $33$ exact comparisons, the untwisted arb cross-check, and the floating-point sanity check for $L=4,\ldots,10$. The thermal files are the block and certificate code, `enc/` with one JSON certificate per block, `results.json`, the digest and mode-validation outputs, and the run logs. Rebuilding any one block, which deletes its certificate and reruns the eigensolver, was not done.
