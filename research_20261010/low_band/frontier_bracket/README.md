# A polynomial-input candidate at g=.085

Updated 2026-10-10 15:28 EDT / 19:28 UTC.

The saved physical inputs and exact scalar argument give a candidate gap bound of .027887084487 for the ordinary spin-1/2 periodic square bilayer at g=17/200=.085, covering every integer L≥2. Independent physical and scalar replay remained pending at this checkpoint.

The corresponding .09 bounded failure evidence is frozen separately in
`../frontier_g009`. Since .085 succeeds, the requested fallback .0825 point was
not needed. A successful point and a failed finite grid do not establish a
rigorous coupling threshold for the physical model or for every temperature.

## Inputs and dimensions

This reuses the saved g-independent F/S/V/W geometry and the same literal
affine translated trial family. The normalized displacement moments have
degrees 2/3/4 in g, as proved explicitly in
`../frontier_g009/POLYNOMIAL_INPUTS.md`. The different source integer
denominators are removed before exact interpolation. All 1,008 extra audited
point checks pass at each reconstructed geometry set.

No new physical support, full-Hilbert diagonalization, or higher moment is
computed. Exact G/K/J give the original ground data, the full inverse-moment
pencil gives ground lower endpoints, and the q-resolved variational filter
gives improved even-trial upper endpoints. The filtered state has no claimed
new residual. All original odd-triplet and oscillator-tail bounds are retained.

The three physical dimensions are 4^16, 4^32, and 4^64. The original ground-trial dimensions are 11, 29, and 29, and the retained low-band counts are 49, 97, and 193. One implicit
filtered ground state in span{ψ,Hψ} is used at each seed. At 8×8, the omitted
cutoff margin is .34061217521649695. Peak input-producer RSS was below 97 MiB.
Scripts pin one CPU and cap virtual memory at 1 GiB.

## Scalar results and earlier windows

The bounded grid β=5,…,25, step .05, finds 48 successful joint-aware txy
proposals and 183 deferred-transport proposals. xty/xyt have no successful
proposal in this grid. The best selected coupled route initially gives
.019519229940 at β=177/20.

`g17d200/extra_cycles_exact.json` then compares the same initial β and physical
inputs with complete txy cycles before canonical conversion, as shown below.

| Cycles before transport | Exact all-L≥2 gap lower |
|---:|---:|
| 4 | .019519229939 |
| 5 | .023775916983 |
| 6 | .026073433601 |
| 7 | .027276152074 |
| 8 | .027887084487 |

After eight cycles, the canonical spatial base is 2048 and inverse temperature is
4531.2. Every earlier window from spatial base 8 through 1024 is independently
bridged using the reviewed joint-aware interpolation lemma. The L=2,…,7
uniform comparison is also retained. The current-window diagnostic at 2048
does not constrain the minimum, because the asymptotic theorem already starts
there. Rounding precision increases for the extra cycles.

For the asymptotic cone, the exact acceptance test is
`exp_upper(beta*gap)*32*u <= 1`, with `0<u<=1/500`. This certifies the same
analytic logarithmic gap formula as the original recurrence, without forming
an unnecessarily large rational logarithm series. The scalar joint lemma and
its implementation are independently reviewed in `joint_ratio_review`.

## Reproduction

From the repository root, run

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python research_20261010/low_band/frontier_bracket/build_point.py --g 17/200
python research_20261010/low_band/frontier_bracket/scan_point.py --tag g17d200
python research_20261010/low_band/frontier_bracket/replay_extra_cycles.py
```

These commands overwrite their own producer outputs. Do not rerun in place
after the freeze. The separate `../third_moment_plan/ASSESSMENT.md` is a cost
assessment only. No new third-moment contraction was launched.
