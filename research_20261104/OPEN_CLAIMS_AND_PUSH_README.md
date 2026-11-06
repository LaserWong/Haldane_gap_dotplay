# Open claims and pushed uniform-gap bounds

Updated 2026-11-04 10:16 EST (America/New_York, UTC−5) / 2026-11-04 15:16 UTC.

Parent commit `a99fa2190ce8c30b33936c8e99af96cdc22e9b76`.

This note records two deposits. [open_claims/STATUS.md](open_claims/STATUS.md) is the claim-by-claim record for the tensor, plaquette, bilayer, and MPS checks. [push_bound/STATUS.md](push_bound/STATUS.md) is the record for the pushed uniform gap of the periodic spin-1 Heisenberg chain. Every number below is taken from those files or from the logs they name. Replaying a certificate here does not create a new gap theorem.

The uniform chain is the periodic Hamiltonian \(H_L=\sum_{i=1}^{L}\mathbf S_i\cdot\mathbf S_{i+1}\), with spin 1 and Hilbert-space dimension \(3^L\). The ordinary bilayer is the periodic square bilayer with rung exchange 1 and in-plane exchange \(g\). Those two models stay separate below.

## Tensor variants

The tensor checks are exact. They use integer or rational arithmetic, or arb balls with directed endpoints.

| Diagonal entry | \(R_{68}\) | Certified bound | Verdict |
| --- | --- | --- | --- |
| \(-289\) | \(-8.322178606774621\times 10^{-6}\) | \(6267/250000=0.025068\) at 10 windows | Confirmed |
| \(-288\) | \(6.620915480134449\times 10^{-5}\) | \(2897/125000=0.023176\) at 10 windows | Confirmed |
| \(-287\) | \(6.071603422304583\times 10^{-4}\) | \(1449/500000=0.002898\) at 10 windows | Partial |
| \(-285\) | \(3.1492687597611075\times 10^{-3}\) | The first window \(68\to 136\) fails at gap 0 | Confirmed as a failed start |

For \(-289\), the 10-window grid is \(10^{-600}\). The value \(0.025068\) passes and \(0.025069\) fails. The exact contraction matches the repository anchor output.

For \(-288\), 11 windows give \(0.023249\) and 12 windows give \(0.023286\).

For \(-287\), \(R_{68}\) matches the stated value. At 10 windows the certified bound is \(1449/500000=0.002898\). The stated bound \(0.003025=121/40000\) is reproduced at 13 windows, in `open_claims/tensor_gap_W13_extra.log`. The bounds at 8, 9, 11, 12, 14, and 15 windows are \(0.002607\), \(0.002772\), \(0.00297\), \(0.003007\), \(0.003034\), and \(0.003039\). The number \(0.003025\) is a valid bound at 13 windows. The window count is part of the claim.

For \(-285\), the leader \(\ell\) is admissible, and the first window still fails at gap 0.

Lengths below 34 in these tensor claims use the repository small-length certificate. The watertight all-sizes audit accepts that certificate at least up to \(0.025179\).

## Plaquette coefficient and the \(3\times 3\) bilayer

The plaquette coefficient is an exact rational identity. Exact Rayleigh-Schrödinger inclusion-exclusion gives vanishing coefficients of \(g^1\), \(g^2\), and \(g^3\), and the coefficient of \(g^4\) in \(W_{\mathrm{box}}\) is \(-15/32\). The single-edge energies are \(E_2=-3/8\) and \(E_4=-3/128\). The log is `open_claims/plaquette.log`.

The table of \(W/g^4\) is numerical. A 60-digit mpmath diagonalization of the \(S^z=0\) block gives

| \(g\) | \(W/g^4\) |
| --- | --- |
| \(0.0125\) | \(-0.475712349656\) |
| \(0.025\) | \(-0.482524747793\) |
| \(0.05\) | \(-0.495624287926\) |
| \(0.1\) | \(-0.519165518161\) |

The rounded chat figures \(-0.47571\), \(-0.48252\), \(-0.49562\), and \(-0.51917\) sit on these values. They are floating-point observations.

The periodic \(3\times 3\) bilayer gaps are numerical. Float64 `eigsh` in the \(S^z=0\) block, of dimension \(48620\), gives \(0.915256\) at \(g_x=g_y=0.1\) and \(0.958627\) at \(g_y=0\). The log is `open_claims/bilayer3x3.log`.

## Purification MPS

The transverse-field Ising trial uses \(J=1\), \(h=5\), \(n=2\), \(\beta=1/2\), and a purification MPS with 32 steps. The enclosed ideal gap printed in `open_claims/ising_mps_W8.log` is \(1.9733807294142025\). The status file records it as \(1.9733807294\).

The MPS tensor \(Y\) is computed in float64. Each entry is then converted exactly into an arb ball, \(\eta=\|Y-e^{-\beta H/2}\|_F\) is computed in arb, and the window recursion uses lower endpoints. Each printed gap is a rigorous lower bound for the \(L=2,4\) seed recursion relative to the repository window theory, given that \(Y\). It is a bound for that seed recursion.

With second-order Strang splitting, half field then \(ZZ\) then half field, and one SVD truncation per step, the twelve bond-order and truncation variants in `open_claims/ising_mps_chi9.log` give the following.

- Bond dimension \(\chi=6\) matches the claim \(1.492020\) on the nose for the step truncation. The printed value is \(1.4920200\).
- Bond dimension \(\chi=16\) prints \(1.9313050\). The claim \(1.931304\) is \(10^{-6}\) lower, so the claim sits on the safe side of this computation.
- Bond dimension \(\chi=9\) does not reproduce the claim \(1.714857\). The twelve printed values run from \(1.7040950\) to \(1.7347188\). The status file summarizes that range as \(1.7041\) to \(1.7347\). None of them equals \(1.714857\). The chat source is absent from this bundle, so the \(\chi=9\) digit is not pinned to one implementation.

Other Trotter splittings move all three bond dimensions. The bond-split second-order row in `open_claims/ising_mps_variants.log` prints \(1.494139\), \(1.726473\), and \(1.962222\).

## Pushed uniform gap

A row is certified when the scalar checker accepts it and the original all-sizes `audit.py` then accepts it for every integer \(L\ge 2\). The producers `produce_fast.py` and `chain_scan.py` are search tools. Checker acceptance is the certificate. Earlier certified values on this chain were \(1/40\) under the original logic and \(0.025179\) under the patched FULL checker.

| Logic | Gap | Windows | Grid | Scalar check | Folder |
| --- | --- | --- | --- | --- | --- |
| Original, \(R_{\mathrm{LIMIT,CPU}}=(60,60)\) left in place | \(250023/10000000=0.0250023\) | 15 | \(10^{3016}\) | \(18.7\,\mathrm{s}\) CPU | `push_bound/certs/orig_W15` |
| Original, CPU cap raised \(60\to 590\,\mathrm{s}\) | \(50009/2000000=0.0250045\) | 16 | \(10^{5632}\) | \(74\,\mathrm{s}\) CPU | `push_bound/certs/orig_W16` |
| Original, CPU cap raised \(60\to 590\,\mathrm{s}\) | \(250057/10000000=0.0250057\) | 17 | \(10^{10000}\) | \(330\,\mathrm{s}\) CPU | `push_bound/certs/orig_W17` |
| Patched FULL scalar checker | \(126049/5000000=0.0252098\) | 15 | \(10^{3016}\) | about \(78\,\mathrm{s}\) wall | `push_bound/certs/full_W15` |
| Patched FULL scalar checker | \(252121/10000000=0.0252121\) | 16 | \(10^{5632}\) | \(85\,\mathrm{s}\) CPU | `push_bound/certs/full_W16` |
| Patched FULL scalar checker | \(63033/2500000=0.0252132\) | 17 | \(10^{10000}\) | \(353\,\mathrm{s}\) CPU | `push_bound/certs/full_W17` |

Each certified gap is the largest passing point on a \(10^{-7}\) grid at that window count. The next grid point fails the asymptotic closure.

The three headline certificates are \(0.0250023\) at 15 windows with the original limits, \(0.0250057\) at 17 windows after the CPU-cap substitution, and \(0.0252132\) at 17 windows from the patched FULL checker.

### CPU-cap substitution

The original `audit_scalar.py` sets `RLIMIT_CPU` to \((60,60)\). At 16 or more windows that process was killed at 60 seconds. The log is `push_bound/certs/orig_W16/2_scalar_check_ORIGINAL_cpu60_KILLED.log`.

`push_bound/run_orig_logic_cpu.py` is the original runner plus one counted substitution. The CPU limit becomes the environment value `CPU_LIMIT`, used here as 590 seconds. The 256 MB address-space cap stays. No arithmetic line and no acceptance line changes. File names, CPU affinity, and the rounding grid \(B\) remain the substitutions already used for the original checker. With the 60-second cap left untouched, the best original-logic result in this deposit is \(0.0250023\) at 15 windows.

### FULL checker and the seal re-pin

The FULL rows use a different scalar checker. `push_bound/certify.sh` sends them through the patched `audit_scalar.py` from the seal12 diff, with the FULL Jensen forcing `AUDIT_FULL_R68=1`, and then through the original all-sizes `audit.py`.

The seal12 diff is not in this deposit. In that diff the patched scalar checker replaces the hypothesis \(Z_{2n}>1\) by the Jensen bound \(\operatorname{Tr}e^{-bH}\ge e^{-b\langle H\rangle}\) at the shifted Rayleigh quotient of the anchor. The same diff re-pins the manifest seal of `uniform_smaller_second_initialization_review` inside the companion all-sizes `audit.py`, from

`54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f`

to

`56a4f06665a0b980089e641b632e449c69cb1ba61e42817a3a515262861ddd84`.

It also raises that patched scalar checker's own limits to 600 CPU seconds and a 1 GB address space, and it reads the certificate name, output name, digit count, and gap from the environment. An acceptance by this patched scalar checker is a patched-checker acceptance. The all-sizes logs stored next to the FULL certificates were produced by the original `audit.py`, whose pinned review seal is the first hash above.

### Eighteen windows

Eighteen windows are uncertified. The producer logs report original-logic \(125031/5000000=0.0250062\) and FULL \(126069/5000000=0.0252138\), at 19500 digits, in `push_bound/certs/orig_W18/1_producer.log` and `push_bound/certs/full_W18/1_producer.log`. The scalar checker for that depth was estimated at about 1400 CPU seconds from a \(d^{2.2}\) extrapolation, and the host kills a process after about 600 CPU seconds. No checker acceptance exists for these two producer outputs.

The ceiling extrapolation from the 15-through-18 window sequence is about \(0.0250067\) for the original logic and about \(0.0252144\) for the FULL checker. Both figures are estimates. They are not proofs.

## Replay in this session

On 2026-11-04 this session reran the original all-sizes `audit.py` on the six shipped scalar-result files. The scalar checker was left untouched, including the checks that take several minutes. Eighteen windows were not rerun, because those folders contain a producer log and no scalar acceptance.

The replay used a temporary copy of commit `a99fa2190ce8c30b33936c8e99af96cdc22e9b76`. Inside that copy only, `README.md` and `RESOURCE_PROJECTION.md` in the sealed uniform-chain folders were restored from commit `3ec8d89` so the manifest seals match. The working tree outside `research_20261104/` was not modified, and the scratch copy was not committed. The runner applied the original file-name, affinity, and gap-literal substitutions, then executed `audit.py` on each shipped `ORIG_scalar_results_*.json`.

Each rerun returned `ACCEPTED stronger uniform all-size gap` for every integer \(L\ge 2\). Wall time was about 3.3 seconds per certificate.

| Tag | Gap | Result |
| --- | --- | --- |
| `orig_W15` | \(250023/10000000\) | Accepted |
| `orig_W16` | \(50009/2000000\) | Accepted |
| `orig_W17` | \(250057/10000000\) | Accepted |
| `full_W15` | \(126049/5000000\) | Accepted |
| `full_W16` | \(252121/10000000\) | Accepted |
| `full_W17` | \(63033/2500000\) | Accepted |

The printed JSON is in [push_bound/rerun_allsizes_20261104](push_bound/rerun_allsizes_20261104). This replay checks the all-sizes bridge against the shipped scalar results. The scalar-checker logs remain the scalar evidence. The FULL rows remain patched-checker scalar acceptances followed by the original all-sizes checker.
