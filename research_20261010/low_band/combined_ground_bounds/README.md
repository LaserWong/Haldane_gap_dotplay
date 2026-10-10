# Combined ground endpoint certificates

Updated 2026-10-10 15:04 EDT / 19:04 UTC.

**Status: exact producer candidates, awaiting independent recombination review.**
The two physical endpoint packages are frozen and separately under independent
review. See `PROOF.md` for the precise conditional chain and input distinctions.

## Exact all-size candidates

Every number below includes the asymptotic recurrence, all required finite-size
windows, and the short-size bridge, for every integer square side L≥2. The
model is the ordinary spin-1/2 periodic square bilayer, with rung coupling 1.
The best scanned order is txy, transported to the canonical order.

| g | Full odd-trial numerator | Largest ground-only numerator |
|---|---:|---:|
| .03 | .341601445704 | .341601363665 |
| .04 | .272402896810 | .272402625840 |
| .05 | .203655275044 | .203654642229 |
| .06 | .164746706191 | .164744743967 |
| .07 | .093479385120 | .093477650352 |
| .08 | .023243965748 | .023241913957 |

At g=.08, β=197/20. Required finite-window gaps for n=8,16,32 are respectively
.085694716373, .052551882633, .038596267315; the asymptotic bound is the minimum.
The optional n=64 endpoint window is also recorded. The uniform short-size
bound exceeds .3078. g=.10 has no successful proposal in the tested
β=5,…,30 grid of step .05 across three orders; this is not an all-temperature
exclusion.

`combined/` uses full-pencil ground lower endpoints plus filtered ground upper
endpoints. `filter_only/` keeps the original ground lower endpoints, allowing
the two improvements to be separated. All triplet and tail data are unchanged.
The largest-ground-only result drops the optional odd numerator trial terms;
it still uses original largest second-moment data to certify the filter. It is
therefore distinct from the strict first-moment-only `../reduced_input` route.

## Inputs, dimensions, and computation

- Full physical spaces: 4^16, 4^32, 4^64.
- Original ground trial dimensions: 11,29,29; retained ground states: one each.
- The filtered state is implicit in span{ψ,Hψ}, generally outside that original
  ground trial family. No filtered sparse vector is constructed.
- Existing exact G/K/J and geometry are reused. No new physical moments, higher
  moments, or full-Hilbert eigenvectors are generated.
- The unchanged low band contains 1+3N states when the odd trial terms are used.

The code requires two frozen producer manifests, verifies their hashes, checks
all endpoint orderings, and records actual input digests. The current producer
manifests are:

- `../ground_moment_pencil/ENDPOINT_MANIFEST_SHA256.json`
- `../../variational_numerator_filter/FROZEN_MANIFEST.json`

The full pencil package also has `FROZEN_MANIFEST_SHA256.json`; the endpoint-only
manifest used here was frozen first and remains unchanged.

From the repository root:

```sh
ulimit -v 1048576
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python research_20261010/low_band/combined_ground_bounds/recombine.py \
  --pencil-manifest research_20261010/low_band/ground_moment_pencil/ENDPOINT_MANIFEST_SHA256.json \
  --filter-manifest research_20261010/variational_numerator_filter/FROZEN_MANIFEST.json
python research_20261010/low_band/combined_ground_bounds/recombine.py \
  --variant filter_only \
  --pencil-manifest research_20261010/low_band/ground_moment_pencil/ENDPOINT_MANIFEST_SHA256.json \
  --filter-manifest research_20261010/variational_numerator_filter/FROZEN_MANIFEST.json
```

These commands overwrite only their own candidate subdirectory. Do not rerun
in place after the final freeze; copy this producer directory first if needed.
