# Stronger ground lower bounds from the existing full moment space

Checkpoint: 2026-10-10 15:02 America/New_York (EDT) / 2026-10-10 19:02 UTC.
The exact candidates await independent review. Existing frozen inputs
and earlier accepted results are unchanged.

## Candidate bounds

All 21 patches (N=16,32,64 at g=.03,.04,.05,.06,.07,.08,.10) pass exact rational
G positivity, S positivity, indefinite K inertia, lower-endpoint inertia, and
an explicit integer negative-direction witness. The trial dimensions stay
11/29/29 and only one ground state is retained. No new physical states or
higher moments are computed.

The generalized theorem allows more trial directions than externally counted
low levels. In the ground case, a negative inertia of at least one for
B-(a+l)A+alG certifies l<lambda_ground. A-aG is indefinite. Requiring it to be
negative definite would wrongly discard these useful directions. See PROOF.md.

| g | Best newly replayed all-integer L>=2 gap | order | beta |
|---|---:|---|---|
| 0.03 | 0.318423498447 | txy | 259/20 |
| 0.04 | 0.236077925502 | txy | 47/4 |
| 0.05 | 0.171026464125 | txy | 99/10 |
| 0.06 | 0.107275412881 | txy | 51/5 |
| 0.07 | 0.032948924929 | txy | 49/5 |
| 0.08 | no accepted point on the bounded grid | not available | not available |
| 0.10 | no accepted point on the bounded grid | not available | not available |

At g=.05 the existing .171822115684 certificate remains valid. Sharper inputs
can cause the scalar implementation to stop one round earlier and report a
smaller constant. `previous_certificate_dominance.json` exactly verifies that
all 14 previously accepted first-purity triples are dominated at the same beta,
so the old recurrence witnesses can be reused by weakening the new inputs.
These producer checks do not replace independent review.

The .08/.10 failures concern beta=5,...,30 in increments .05 and three properly
transported orders. They are not all-beta exclusions or physical gaplessness
claims. A separate calculation recombines these stronger lower endpoints
with improved Rayleigh numerators. Its results are outside this package.

At .08, the 4x4/8x4/8x8 ground widths decrease to
.0001116790231/.0009872224688/.0065690332174. At .10 they decrease to
.0004460073907/.0036872263177/.0233006060591. The largest physical space remains
4^64=2^128, while its ground trial is 29-dimensional. Those dimensions are not
MPS bond dimensions.

## Files and reproduction

- `PROOF.md`: invariant-sector count, general k theorem, cutoff equality,
  direct polynomial proof, and domination of scalar Temple.
- `ground_*.json`: complete rational lower endpoint certificates and explicit
  integer negative-direction witnesses, with a hash for every physical source.
- `temple_*.json`: complete-band records with only the ground lower replaced.
- `ground_summary.json`, `scalar_summary.json`: machine-readable candidates.
- `validation.json`: 34 synthetic exact tests, singular-cutoff rejection and
  external-count counterexample.
- `previous_certificate_dominance.json`: exact retention of older certificates.
- `ENDPOINT_MANIFEST_SHA256.json`: frozen physical endpoint subset.
- `EXTERNAL_DEPENDENCIES_SHA256.json`: imported code and physical source hashes.
- `FROZEN_MANIFEST_SHA256.json`: full package freeze, excluding itself.

From the repository root, with one CPU and a 1.5 GiB virtual-memory cap:

    ulimit -v 1572864
    export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
    python research_20261010/low_band/ground_moment_pencil/certify.py
    python research_20261010/low_band/ground_moment_pencil/validate.py
    python research_20261010/low_band/ground_moment_pencil/scan.py
    python research_20261010/low_band/ground_moment_pencil/retain_previous.py
    python research_20261010/low_band/ground_moment_pencil/dependencies.py

These commands overwrite this directory's generated candidates. To preserve
the freeze, first copy the package and adjust output paths in a separate work
area. Per-run wall-clock telemetry is not deterministic. Exact acceptance never
uses floating eigensolver accuracy as evidence.

The final 21-patch endpoint run took 137.16 seconds of wall time summed over patches and peaked at 80.12 MiB RSS. Single-thread BLAS was enforced.
