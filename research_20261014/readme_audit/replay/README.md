# Certificate replay, 14 October 2026

This directory records a rerun of two archived independent verifiers. The original logs and JSON are unchanged. The checks cover the scalar benchmark and the alternating spin-1 dimer certificate described below.

## Run the checks

Run this command from the repository root with Python 3 and NumPy already installed.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261014/readme_audit/replay/run_fresh_certificate_audit.py
```

The wrapper finds the repository root from its own location, so it also works from another working directory. Each run creates a new `rerun_<timestamp>/` directory and preserves `fresh_results/` and the historical audit outputs. Optional arguments `--repo-root PATH` and `--output-dir PATH` select a repository and a new output directory. Do not use `python -O`, because the original verifiers rely on assertions.

The run took about nine seconds in the recorded environment. Runtime may differ elsewhere. The wrapper requires no network access or software installation and performs no remote publication or deletion.

## Inputs

[input_hashes.json](input_hashes.json) lists repository-relative paths, SHA-256 hashes and Git blob hashes for all 65 inputs. The wrapper checks every SHA-256 before running and stops if an input is missing or changed.

[current_main_input_identity.json](current_main_input_identity.json) records the Git blob hashes of these files on main as checked on 2026-10-14. All 65 matched the archived inputs used for the replay. They comprise two independent verifiers, the extension package's checksum table and its 59 entries, the spin-1 certificate, and two Ritz NPZ files. This comparison covers those inputs only. Later main-branch changes require another identity check.

The portable wrapper was tested with byte-identical checkpoint inputs, as recorded in [portable_wrapper_test.log](portable_wrapper_test.log). The test did not create a full main-branch checkout or run the entire project test suite.

## Results

- The alternating periodic spin-1 chain passed the checks for strong coupling 1 and weak coupling 1/20. For M=2 and M=4, these cover exact Hamiltonian action, residuals, full-space Weyl and Temple bounds, the complete spectral tail, and six temperature recursions. The full Hilbert dimensions are 81 and 6561. Each input retains one trial vector. The best stored certificate gives the lower bound 0.116303868802.
- The baseline benchmark passed its 625-dimensional Casimir spectrum enumeration, integer moments of orders 0 through 200, inertia counts, and thermal-trace envelopes at β=1 and 2. Its general scalar lower bound is 0.055688426272.
- Both input ZIPs passed CRC checks. All 1,149 checkpoint manifest entries and all 59 extension checksum entries matched. The ZIP bytes are not duplicated here.

The replay reran the historical independent verifiers. It did not include a new manual review of the physical transfer assumptions, all-integer-size interpolation or short-size bridges. The ordinary bilayer, large-D model, fully frustrated bilayer, uniform spin-1 Appendix A, Stage38 and g=.12 were outside this run. [AUDIT_SCOPE.json](AUDIT_SCOPE.json) gives the exact scope. These checks do not constitute a new gap discovery, a full-project reproduction or a complete Stage38 release.

## Records

- [archive_integrity.json](archive_integrity.json) records ZIP SHA-256 hashes, CRC results and entry counts.
- [manifest_integrity.json](manifest_integrity.json) compares the actual and expected SHA-256 for each manifest entry.
- [baseline_verification.json](fresh_results/baseline_verification.json) and the [spin-1 verification](fresh_results/certificate_s1_W1_g1d20_k0_audit.json) contain the replay results.
- [reproducible_replay.log](fresh_results/reproducible_replay.log) preserves the successful run's original log.
- [run_environment.json](fresh_results/run_environment.json) records the original environment, source hashes and runtime.

Absolute `/workspace/...` paths in the historical JSON and logs identify the original input and output locations. They are preserved for provenance. The portable wrapper uses the relative input manifest and the repository root derived from its own location.
