# Independent certificate for a continuous fully frustrated perturbation interval

Updated October 10, 2026, at 14:01 EDT / 18:01 UTC.

The unit-rung spin-1/2 periodic square bilayer with crossed exchange `J=0.3` and straight exchange `J+epsilon` has a unique finite-volume ground state and a gap greater than **0.000768515509** throughout **0<=epsilon<=0.00855**, for every integer square side **L>=2**.
The independent review retains positive-direction adjacency multiplicities at period two.
On the smaller interval through `epsilon=0.0085`, the common bound improves to **0.001703099464**.

- [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) gives the statement, continuum proof, complete spectrum, signed-transfer windows, scope, and provenance.
- [audit_interval.py](audit_interval.py) checks the result without importing the certificate generator or other project code.
- [audit_results.json](audit_results.json) records the coefficients, 29 new finite windows, baseline replay, rational gap bounds, and input hashes.
- [REPRODUCE.sh](REPRODUCE.sh) runs the replay, whose successful output is saved in [audit.log](audit.log).

The checker reconstructs the physical-spin kernels and complete sparse polynomial actions on the saved rational vectors.
It verifies endpoint positive-semidefinite conditions, all occupation bins, correlated affine energy bounds, 224-bit heat enclosures, the exact recurrence, and every finite window.
It also replays the baseline interval and proves exact adjacency of the seven closed parameter pieces.

The result is a sufficient lower-bound certificate for square volumes.
It does not determine the physical gap, a maximal coupling, or coverage of arbitrary aspect ratios.
