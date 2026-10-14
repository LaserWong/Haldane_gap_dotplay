# Exact streamed heat traces

This directory reconstructs the finite thermal inputs used in Appendix A for the spin-1 Heisenberg chain. The deterministic calculation uses exact integer arithmetic and rigorous error bounds. It preserves the original archive and requires neither full diagonalization nor stochastic trace estimation. Printed large-integer totals are used only for comparison.

## Build and run

The calculation requires the Python 3 standard library, a C++17 compiler, and GMP development headers and libraries. The optional archived-reference comparison also needs NumPy and SciPy. No new package installation was needed on this host.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
g++ -O3 -std=c++17 -Wall -Wextra stream_horner.cpp -lgmpxx -lgmp -o stream_horner
python run_certificates.py --length 6 --twist I --orbits none
python run_certificates.py --length 6 --twist P --orbits none
python run_certificates.py --length 6 --twist C --orbits none
python validate_reference.py
python validate_symmetries.py
for n in 6 8 10; do
  for t in I P C; do
    python run_certificates.py --length "$n" --twist "$t" --orbits full
  done
done
python replay_appendix_a.py
```

Each invocation has one C++ child at a time. Matrix-vector arithmetic does not use threaded libraries. `--max-new-columns` gives a bounded benchmark. Chunks default to 16 representatives. Their atomically written checkpoints are reused after interruption. Repeating a finished command recomputes only the exact rational postprocessing. Do not change chunk size when resuming the same result directory, because chunk names encode the ranges.

## Files and results

- `PROOF.md`: independent spectral, Taylor, fixed-point, symmetry, norm, exponential, and integer-range justification.
- `results/A_L*_*/M*.json`: exact integer representative column norms, physical multiplicities, source/coefficient fingerprints, and chunk times.
- `results/A_L*_*/certificate.json`: exact rational thermal intervals and acceptance against the original center +/- 1e-5.
- `reference_validation.json`: all three L6 all-column totals exactly match a fresh in-memory run of the original dense implementation.
- `symmetry_validation.json`: exact magnetic-translation and antiunitary identities, plus independently enumerated orbit coverage, for L4/L6.
- `appendix_a_replay.json`: all nine physical heat interval obligations checked before replaying the original Proposition 5.4 scalar proof and five sequential scalar updates, with the freshly reconstructed N = 120 MPS anchor and the independently reviewed analytic bridge explicitly linked.
- `../audit/independent/streamed_heat_audit.json`: independent auditor's separate integer-Horner and rational-bound reconstruction.

For I, permutation covariance of floor makes the orbit and all-column totals bitwise identical. For P/C the exact heat-column norms have the symmetry, but the quantized columns need not. Differences from the printed integer totals are expected and controlled by the new per-column error proof. The printed totals are used only as diagnostics, never to compute an input.

The completed reconstructed route proves a unique ground state and gap >= 0.005908566393 for the spin-1 isotropic Heisenberg model with bilinear coefficient one, periodic boundary conditions, and every even L >= 1920. The absent original manuscript PDF was not directly reviewed. The separate analytic reconstruction is included. Larger Appendix B inputs remain outside this result.

The October 10 pause left the planning and prototype work in `spin2/` unfinished, with no new spin-2 heat input. `PAUSED_STATE.md` records those pending tasks. Current work follows the repository README and AGENTS.md.

The source/checkpoint manifest is generated after the completed replay. All floating-point quantities are labeled display/timing only. Acceptance uses exact integers and rational inequalities throughout.
