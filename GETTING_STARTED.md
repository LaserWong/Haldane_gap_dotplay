# Running the archived checks

The repository contains source code, exact inputs, numerical results, and the records used to assess them. The [research overview](README.md) states the strongest bounds and the missing dependencies. The [progress record](docs/PROGRESS.md) gives the complete numerical history.

## A short reproducibility check

Run the following command from the repository root with Python 3 and NumPy already installed.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261014/readme_audit/replay/run_fresh_certificate_audit.py
```

The script verifies 65 input hashes before running the archived checks. It tests the 625-dimensional Casimir benchmark and the alternating spin-1 certificate at weak coupling 1/20. The latter reproduces the lower bound 0.116303868802. A run took about nine seconds in the recorded environment. Results are written to a new timestamped directory, leaving the archived outputs unchanged. Do not run Python with optimization enabled because the original checks use assertions.

The [replay instructions](research_20261014/readme_audit/replay/README.md) list the inputs, output files, and scope. This command does not reproduce the uniform-chain proof, the bilayer certificates, or the late H³ calculation.

## Checking archive integrity

```sh
python verify_archive.py
```

This command compares 1,149 files with the original checkpoint manifest. It verifies historical file identity rather than mathematical validity. Run it on the original checkpoint to reproduce that integrity check. Documentation revised in place may differ from historical hashes without changing the scientific inputs. The original manifest is retained as provenance, not as a restriction on documentation edits.

## Reading the project

The [documentation index](docs/INDEX.md) links the English model notes, derivations, and research records at their original paths. Duplicate reading copies have been consolidated. The revised documentation preserves the scientific claims and historical dates. Raw code, numerical data, certificates, and manifests are unchanged.

The ordinary square bilayer, fully frustrated bilayer, large-D model, and alternating chain use different Hamiltonians. Their normalizations and boundary conventions are specified in the overview and model notes. Results from one model should be used with its own input files.

For the missing dependencies that prevent a complete late-stage replay, see the [recovery record](docs/PROGRESS.md#next-research-steps).
