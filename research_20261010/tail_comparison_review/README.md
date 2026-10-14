# Independently verified spectral-tail combinations

Recorded October 10, 2026, at 14:40 America/New_York / 18:40 UTC.

The independent audit accepts all 36 complete-band patches and 35 successful exact all-size certificates.
For the ordinary periodic bilayer at g = .03, .04, .05, and .06, the strongest respective gap lower bounds are **.318085460990, .235117964607, .171822115684, and .103487228301**.
Each holds for every integer square side L>=2 and includes a unique finite-volume ground state.

[REVIEW.md](REVIEW.md) gives the proof, comparisons at fixed update order, dimensional distinctions, precision qualifications, and scope.
[REVIEW_STATUS.json](REVIEW_STATUS.json) records the accepted endpoints.
The physical moments and earlier tail theorems are reused only after all their sealed hashes are checked.
The new endpoints, traces, order conversions, recursions, and short-size bounds are independently recomputed.

The physical multiplicities C(N,q)3^q remain distinct from the oscillator multiplicities C(3N+q-1,q).
The three best time–x–y comparisons use the same temperature at each g, separating the smaller gain from the tail estimate from the larger gain due to the changed update order.
These are four discrete certified parameter points, rather than an interpolated interval or an optimum.

Run `bash REPRODUCE.sh`.
The replay changes no external state.
