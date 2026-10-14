# Matching existing research before starting a new calculation

The workflow can recognize the exact model covered by the project's historically accepted uniform bound 31/1250=0.0248. This avoids treating a well-studied model as a blank input while keeping historical evidence separate from a newly computed finite-size result.

The matching record concerns the untwisted periodic spin-one Heisenberg chain with unit bilinear exchange,

\[
H_L=\sum_{i=0}^{L-1}\boldsymbol S_i\cdot\boldsymbol S_{i+1\bmod L},
\qquad \hbar=1.
\]

At L=2 the sum has two adjacency terms between the same sites. The historical result states uniqueness and a gap at least 31/1250 for every integer L≥2. Its stronger bootstrap initialization is 34. A separately certified smaller initialization 30 belongs to the earlier bound 179/10000. Coverage beginning at two is not initialization two.

## Exact matching rules

`gapflow/catalog.py` provides `match_catalog(model,repository_root=None)`. It accepts a model specification or a validated `Model` instance. Matching requires a one-dimensional lattice of length at least two, periodic boundary conditions, the `positive_direction_multigraph` convention, spin one at every site, and exactly one unit isotropic bilinear interaction for each periodic adjacency term.

The matcher checks rational coefficients and interaction multiplicities rather than model names. A near-unit rational coefficient does not round to one. Open boundaries, other spins, simple-graph length-two normalization, omitted or duplicate bonds, scaled couplings, onsite terms, and other perturbations do not match. A zero-valued extra onsite term is also conservatively rejected rather than simplified automatically. Explicit graph declarations are outside this matcher even if they could be proved equivalent separately.

The model parser defines the spin operators and energy normalization. The catalog does not infer these conventions from a free-text label. Equivalent isotropic `xxz` terms may match after exact parsing because their operator coefficients are identical.

## Historical evidence and local availability

The strongest returned status is `HISTORICAL_CERTIFICATE_MATCH`. The result contains a separate `historical_claim` and sets `freshly_independently_replayed`, `new_uniform_family_claim`, and `computed_finite_bound_overridden` to false. It never mutates its input or overwrites a user's computed finite-size bound.

The historical review lives at the repository-relative directory `research_20261010/uniform_gap_0248_all_sizes_review`. Its original manifest has SHA-256

```text
5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf
```

The historical Git directory tree is `dace5286062605d3b4cfd0acf526bb1db06b06f7`. The pinned metadata in `gapflow/catalog_data/uniform_spin1_0248.json` contains 158 distinct raw dependency paths and SHA-256 digests assembled from that review's manifest and direct input list. It excludes Markdown and reStructuredText entries. Legitimate prose revisions therefore do not invalidate raw numerical identity checks.

The direct list is not a recursively complete closure of all upstream manifests. Verifying it would establish identity of those listed files, not reprove the mathematics or guarantee that every executable dependency is available.

Six raw files were recovered read-only from their pinned Git blobs into `catalog_sources/research_20261010/uniform_gap_0248_all_sizes_review`.

- `MANIFEST_SHA256.json`
- `INPUT_SHA256.json`
- `results.json`
- `CLAIM_VERDICTS.json`
- `SEAL.json`
- `audit.py`

Their byte identities were checked against the pinned source and manifest. The catalog snapshot currently verifies six entries and reports 152 unavailable raw entries. The recovered code was not executed. In particular, fetching `audit.py` does not mean that its physical contractions or scalar proof were rerun.

Pass the real project repository root to `match_catalog` to inspect whichever artifacts are present there. The optional local inspection reports one of four statuses.

- `NOT_INSPECTED` when no repository root was provided
- `ARTIFACTS_UNAVAILABLE` when some listed dependencies cannot be read
- `RAW_IDENTITY_MISMATCH` when an accessible raw artifact differs from its pinned digest
- `LISTED_RAW_IDENTITIES_VERIFIED` when all listed raw identities match

Every evidence path returned is repository-relative. Paths that escape the supplied root are rejected. Inspection is read-only and performs no remote fetches, compilation, execution, or publication. An unavailable or mismatched artifact remains visible beside the historical match and prevents any suggestion of a complete fresh replay.

## Historical proof scope

The reviewed composition covers analytic L=2,3, cached exact purity checks at L=4 through 25, fresh historical physical anchors at L=26 through 33, and the accepted all-integer tail from initialization 34. The historical code rechecks stronger-gap inequalities at the cached purities instead of inferring a stronger bound from a weaker old conclusion. The proof uses the physical spin-one model and its signed transfer bounds.

The historical direct L=25 resource-enforcement anomaly remains unresolved. Later guarded runs with consistent measurements do not retroactively erase it. Mathematical identity and resource compliance must remain separate fields.

## Tests and use

Seven focused tests pass. They cover exact model matching including L=2, incompatible models and perturbations, near-unit rational rejection, immutable inputs, six recovered raw identities with missing-artifact diagnostics, raw tampering without prose blocking, and dependency path escape.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p test_catalog.py -v
```

Use the catalog result as an independent context artifact before planning a fresh calculation. A finite-volume computation can produce a stronger bound at its specific size without changing the historical all-size statement. Conversely, a weak or inconclusive fresh finite computation does not erase the existing historical theorem. New perturbations require their own proof and cannot inherit 0.0248 through this matcher.
