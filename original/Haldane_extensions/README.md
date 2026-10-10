# Haldane purity-bootstrap extensions

Read `REPORT.md` for the Chinese derivations, precise model definitions, proof scope, numerical results, and references.

## Main output

A general alternating spin-s chain has a uniform periodic gap at least **0.055688426272**, for every integer number of two-spin cells M≥2, when the intra-cell perturbation has spectral width at most 0.03 and satisfies the stated cell time-reversal and exchange symmetries. Half-odd-integer s gives a nontrivial SPT class when the protecting symmetry is retained. The proof uses an analytic two-cell seed and exact rational scalar checks, without full-spectrum diagonalization.

Two deterministic non-ED demonstrations are included: integer heat-trace moments, and exact inertia counts combined with a low-energy thermal tail.

Floating-point finite-chain results are stored separately and are not treated as certified eigenvalue lower bounds.

## Reproduction

Python 3 with NumPy, SciPy, and threadpoolctl is sufficient. The analytic certificate alone uses Python's standard library.

```bash
python code/analytic_certificates.py
python code/exact_heat_trace.py
python code/inertia_trace.py
python code/numerics.py bench
python code/numerics.py purity
python code/dimer_biquadratic.py
python code/aklt_low_spectrum.py 2 3 4 5 6 7
python code/aklt_low_spectrum.py 3 3 4 5 6
```

`exact_heat_trace.py` reuses its exact integer moment cache. Delete `results/integer_heat_trace_moments.json` to rebuild those moments from the Hamiltonian.

`numerics.py` reuses spectrum caches. Independent newly computed spectra begin with `spec_`. Files beginning with `archived_spin2_` are extracted floating spectra from the uploaded project and are used for comparison and the spin-2 eight-site diagnostic. They are not claimed as newly recomputed or newly certified. Their provenance is recorded in `sources/archive_provenance.json`.

The finite-chain code is a transparent small-system implementation. It enumerates the product basis and is not a memory-scalable production solver for arbitrarily large lengths.

## Verification scope

The original `bootstrap_scalar.py` is bundled unchanged. It is an arithmetic interface and correctly retains its conditional labels. The physical transfer-kernel hypotheses and the extension to all integer cell counts are proved in Sections 3 and 4 of `REPORT.md`.

No proof-assistant formalization, quantum-hardware experiment, or quantum-circuit simulation was performed. The uniform spin-2 and spin-3 Heisenberg gap is not a new conclusion of this package. The finite-U spin-2 projection model and the seven-site AKLT threshold crossing are floating diagnostics rather than completed long-chain certificates.
