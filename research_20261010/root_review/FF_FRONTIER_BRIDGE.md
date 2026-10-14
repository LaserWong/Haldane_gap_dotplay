# Completion of the remaining fully frustrated perturbation size windows

Date: 10 October 2026, 13:36 EDT / 17:36 UTC.

The fixed-parameter physical inputs at epsilon=0.008 and 0.0085 were independently audited in `nonperturbative_audit`. Their saved scalar certificates covered respectively square sides L≥32 and L≥128. The signed-transfer finite-window lemma in `FINITE_WINDOW_INTERPOLATION.md` now closes all omitted integer side lengths.

The model is the same unit-rung spin-1/2 bilayer with J=0.3, straight couplings J+epsilon, crossed couplings J, and positive-direction periodic multiplicities. These statements concern square tori.

- epsilon=1/125: unique ground state and gap at least 0.008498663753 for every integer L≥2.
- epsilon=17/2000: unique ground state and gap at least 0.001984903734 for every integer L≥2.

These are individual certified parameter points. They do not certify all intermediate epsilon values or a maximal threshold.

`bridge_ff_frontier.py` reconstructs the initial n=2 canonical lower purities, then the n=4 correlated first update from the independently audited J1/J2/C endpoints using exactly the specified 128-bit downward rounding. Each subsequent stored state supplies the next dyadic finite window. The new interpolation lemma applies at every window and gives a gap larger than the corresponding final asymptotic bound. Thus the minimum stays equal to the previously certified asymptotic bound, while its size scope becomes all L≥2.

The best initial inverse temperatures remain 32 and 65/2. The exact final gaps are

- 1445972708809357228759498140402530393 / 170141183460469231731687303715884105728
- 675427740767930538083603620537361547 / 340282366920938463463374607431768211456

Every inverse-purity margin, rational square-root enclosure, finite-temperature gap and input hash is stored in `ff_frontier_finite_windows.json`. The calculation uses exact fractions and independent outward exponential tests. The interpolation lemma itself was independently reconstructed by the low-band reviewer. This size extension reuses the existing physical-seed audit and does not rerun an eigensolver.

Reproduce from the repository root:

```sh
python research_20261010/root_review/bridge_ff_frontier.py
```

The older checkpoint correctly records the scope before this new bridge. This document supplies the later scope extension without changing the underlying seed records.
