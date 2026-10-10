# Independently verified continuous FF perturbation interval

Updated: 10 October 2026, 14:01 EDT / 18:01 UTC.

**PASS:** the unit-rung spin-1/2 periodic square bilayer with crossed exchange
`J=0.3` and straight exchange `J+epsilon` has a unique finite-volume ground state
and a gap greater than **0.000768515509**, uniformly for **0<=epsilon<=0.00855**
and every integer square side **L>=2**. Period-two positive-direction adjacency
multiplicities are retained. Through `epsilon=0.0085`, the stronger common bound
is **0.001703099464**.

- [Independent review](INDEPENDENT_REVIEW.md): exact statement, continuum proof,
  complete spectrum, signed-transfer windows, scope and provenance
- [Independent checker](audit_interval.py): no imported producer/project code
- [Exact audit output](audit_results.json): coefficients, all 29 new finite
  windows, baseline replay, rational gaps and input hashes
- [Replay command](REPRODUCE.sh) and [successful log](audit.log)

The checker freshly reconstructs physical-spin kernels, complete sparse
polynomial actions for fixed saved rational vectors, interval endpoint PSD,
all occupation bins, correlated affine energy bounds, 224-bit heat enclosures,
exact recurrence and every finite window. It also replays the baseline interval
and proves exact adjacency of the seven closed parameter pieces.

This is a sufficient square-volume certificate. It is not a physical gap
estimate, a maximal coupling claim or an arbitrary-aspect-ratio result.
