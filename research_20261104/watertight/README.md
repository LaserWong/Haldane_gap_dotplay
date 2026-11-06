# Watertight record for the periodic spin-1 chain

This directory collects the transfer-operator argument, an independent arb enclosure of the n=8 heat-trace ratio, and checker runs for several uniform-gap candidates. The Hamiltonian is

$$
H_L=\sum_{i=1}^{L}\mathbf S_i\cdot\mathbf S_{i+1},
$$

with $\mathbf S_{L+1}=\mathbf S_1$, unit antiferromagnetic exchange, spin 1, and full Hilbert-space dimension $3^L$. The per-site shift is $a=700741/500000$. The shifted traces are $Z_L(\beta)=\operatorname{Tr}\exp(-\beta(H_L+aL))$. The source narrative is [WATERTIGHT_STATUS.md](WATERTIGHT_STATUS.md). The sealed checkout outside this directory is unchanged.

## Seal re-pin

The patched checker is [seal12/auditor_changes.diff](seal12/auditor_changes.diff). Applying it regenerates the manifest of `uniform_smaller_second_initialization_review` and replaces the review seal

`54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f`

with

`56a4f06665a0b980089e641b632e449c69cb1ba61e42817a3a515262861ddd84`.

Gap $25177/1000000$ and the decimal $0.025179$ are accepted only by that patched checker. The patch replaces the hypothesis $Z_{2n}>1$ by the Jensen bound $\operatorname{Tr}e^{-bH}\ge e^{-b\langle H\rangle}$ at the shifted Rayleigh quotient of the anchor. That inequality is valid. The checker that uses it is new code. The same diff raises the resource limits, reads the certificate name, output name, digit count, and gap from the environment, and compares the strong-tail gap as a fraction. An acceptance from this checker is a patched-checker acceptance. It is separate from an acceptance by the original `audit_scalar.py` and `audit.py`.

The statement that gap $0.025179$ fails is the 12-window case. With 13 windows and 700 digits the patched scalar checker accepts $25179/1000000$, and the original all-sizes `audit.py` accepts that output for every integer $L\ge 2$. The saved all-sizes log is [auditor/orig_allsizes_patchedfull25179.log](auditor/orig_allsizes_patchedfull25179.log).

## Status

| Item | Status | Statement |
| --- | --- | --- |
| Transfer operator | PROVEN | For each $\beta>0$ there is one real symmetric Hilbert–Schmidt operator $X_\beta$ with $Z_L(\beta)=\operatorname{Tr} X_\beta^L$ for every integer $L\ge 2$. The argument is [transfer_operator.md](transfer_operator.md). |
| Moment comparison | PROVEN | The same $X_{2b}$ and $\ell^p$ monotonicity give $Z_{16}(2b)\le Z_{12}(2b)^{4/3}$. This is the comparison used by the n=8 exclusion. Any even $m\le 16$ works. The certificate uses $m=12$. |
| Transfer numerics | CONSISTENT | A discretized kernel and a Monte Carlo sample at $\beta=1/2$ track exact diagonalization for $L=2,3,4$. Those runs are sanity checks. They are not the proof. |
| n=8 exclusion | PROVEN, computer-assisted | $\sup_{b>0} Z_{12}(2b)^{4/3}/Z_8(b)^4$ has arb upper endpoint $[0.099979201\pm 3.35\times 10^{-10}]$, which is below $1/2$. $W\le 1/2$ means the scalar $G$-iteration cannot start at $n=8$. It is silent about the physical gap. |
| $Z_{12}(49/4)$ | PROVEN, computer-assisted | The independent enclosure has upper endpoint $[1.90055706747398\pm 8.78\times 10^{-16}]$, which is below $1.900577$. |
| Block rebuild | PROVEN, computer-assisted | [indep_blocks.py](indep_blocks.py) rebuilds the Bloch blocks. Multiplicities total $3^{12}=531441$ and $3^8=6561$. Enclosed power sums contain $\operatorname{Tr} H^j$ for $j=1,2,3$. [cert_core.py](cert_core.py) adds an int64 wrap guard that the earlier limb recombination lacked. The guarded eigenvalues match the previous $2^{-30}$ grid. |
| Gap $2497/100000$ | PROVEN, original checker | Original `audit_scalar.py` and `audit.py`, with file-name, CPU-affinity, gap-literal, and rounding-grid substitutions only. This session reran it at 12 windows and $B=10^{700}$. Scalar and all-sizes ($L\ge 2$) both returned ACCEPTED. At $B=10^{140}$ the depth-11 defect, about $10^{-273}$, falls below the grid. |
| Gap $1/40$ | PROVEN, original checker | Fifteen windows and $B=10^{2500}$. Saved logs [auditor/orig_scan_F0_2500.log](auditor/orig_scan_F0_2500.log) and [auditor/orig_allsizes_scan_F0.log](auditor/orig_allsizes_scan_F0.log) record scalar and all-sizes acceptance for every $L\ge 2$. This session did not rerun that case. |
| Gap $25177/1000000$ and $0.025179$ | PROVEN only by the patched checker | Thirteen windows for $25179/1000000$. See the seal re-pin above. This session did not rerun the patched checker. |
| Tensor, plaquette, and MPS trials | OPEN | Tensor variants $-288$, $-287$, and $-285$, the plaquette value $-15/32$, and MPS bond dimensions $\chi=6,9,16$ were not checked. |

## Trust assumptions

The computer-assisted rows assume three things.

- python-flint 0.9.0 arb ball arithmetic is correct.
- IEEE float64 matrix multiplication uses no fast-math contraction and no Strassen product. The wrap guard in `cert_core.py` checks the int64 limb recombination against a float64 residual.
- The Bloch-block formula and the multiplicities for momentum $k$ with $L-k$, and for $S^z$ with $-S^z$, are the mathematical identifications in [transfer_operator.md](transfer_operator.md) and [WATERTIGHT_STATUS.md](WATERTIGHT_STATUS.md). The dimension count and the three power sums are the numerical cross-checks.

## How to reproduce

`verify_indep.py` reads the saved enclosures in `enc/` and does not write into the research tree. From this directory, with `python-flint==0.9.0`, `numpy`, and `scipy`, run

```sh
python verify_indep.py
```

The script locates `enc/` from its own path. A successful run reprints the $Z_{12}(49/4)$ endpoint near $1.90055706747398$ and the supremum ball near $0.099979201$. The run in this session took about 5 seconds.

Every auditor script that executes `audit_scalar.py` or `audit.py`, and every producer, writes JSON into a scratch copy. Set `WATERTIGHT_ORIG_AUDIT` to a writable copy of this repository, and `WATERTIGHT_AUDIT_COPY` to a writable copy whose sealed review files still match their manifests. On this fork the English documentation rewrite changed `README.md` and `RESOURCE_PROJECTION.md` inside the sealed uniform-chain folders. Those bytes still match the manifests at commit `3ec8d89`. Restore them in the scratch copy only. Leave the working tree untouched.

`paths.py` resolves the repository root from the script location. The default scratch directories are `scratch/orig_audit` and `scratch/audit_copy` under this folder. Scripts that require a scratch copy are `auditor/produce_w12.py`, `auditor/produce_patchedprefix.py`, `auditor/produce_allsizes_orig.py`, `auditor/run_orig_logic.py`, `auditor/run_patched.py`, `seal12/produce.py`, and `seal12/produce_allsizes.py`.

The original-logic checker is `auditor/run_orig_logic.py`. It substitutes file names, the CPU affinity, the gap literal in `audit.py`, and, when `DIGITS` is set, the rounding base $B=10^{140}$. `produce_w12.py` applies that same base substitution to the original prefix before building a row. The patched source is read from `WATERTIGHT_AUDIT_COPY` after `seal12/auditor_changes.diff` has been applied there. For an original-logic production the audit copy can be the restored tree with that diff left unapplied.

The gap $2497/100000$ rerun in this session used 12 windows, because that is the shortest original-recipe chain whose asymptotic margin is positive, and the final defect is the depth-11 size named in the status note. With both scratch variables pointed at one restored copy, the commands were

```sh
export WATERTIGHT_ORIG_AUDIT=/path/to/restored_copy
export WATERTIGHT_AUDIT_COPY=/path/to/restored_copy
export GAP=2497/100000 W=12 DIGITS=700 AUDIT_CERT=certificate_gap2497.json
python auditor/produce_w12.py
python auditor/run_orig_logic.py scalar gap2497
TAG=gap2497 GAP=2497/100000 python auditor/produce_allsizes_orig.py
DIGITS=700 python auditor/run_orig_logic.py allsizes gap2497 2497/100000
```

Scalar acceptance reported $n=34$, gap $2497/100000$, and `asymptotic_from` $69632$, in about 4.9 CPU seconds. All-sizes acceptance reported gap $2497/100000$ for every integer $L\ge 2$, in about 3.3 CPU seconds. The host used for the affinity substitution must contain CPU 6, which is the substituted affinity in `run_orig_logic.py`.

This session did not rerun the 15-window gap $1/40$, the patched $25179/1000000$ checker, the Monte Carlo or discretized-kernel scripts, or `run_enclose.py`. Those results remain the saved logs and enclosures.
