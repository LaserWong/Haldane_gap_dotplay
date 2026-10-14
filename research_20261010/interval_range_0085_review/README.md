# The bilayer interval [0,.085]

Updated 2026-10-10 17:05 EDT / 21:05 UTC.

The independent review establishes that the ordinary periodic spin-1/2 square bilayer has a unique finite-volume ground state and gap ≥ .001945771244 for every real 0≤g≤.085 and every integer square side L≥2.

The new sixteen pieces covering [.08,.085] have uniform gap ≥ .003365750386. They join the previous 33 accepted pieces. Seven ground-only pieces end at .082. Nine further pieces use complete odd bands on the 4×4 and 8×4 denominator patches. The largest 8×8 numerator still retains one filtered state, augmented dimension ≤30, full Hilbert dimension 2^128.

See REVIEW.md and results/SUMMARY.json. The audit checks literal affine/Q-eigenspace structure, physical normalization, bivariate cross-displacement identities, all full residuals and omitted-state counts, 432 odd mode endpoints, all 100 joint states/windows and 96 short-size rows. No producer modules, eigensolvers, new large support or moments above H² are used.

Run bash REPRODUCE.sh under the enforced one-CPU/1-GiB cap. Verify or preserve the sealed package first because reproduction changes timing-bearing results. PRODUCER_FREEZE.json and ACCEPTANCE_GATES.json pin the inputs. MANIFEST_SHA256.json seals this independent review.
