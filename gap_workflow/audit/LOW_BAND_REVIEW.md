# Independent review: unknown ground multiplicity and low-band certification

Review at 2026-10-14 19:52 UTC.

## Verdict

No mathematical soundness defect found in low_band.py. The code distinguishes a certified isolated low cluster from an exactly degenerate ground space. Neither user-provided g nor an exact ground energy is required for the new path. Claims remain finite-volume.

A small CLI wording issue was reported: a cluster-only result in a selected magnetization sector should explicitly say “selected sector only,” as ordinary gap results already do. Also, the initial CLI inference gate restricts use to dimensions <=16 even where Kramers could infer rank-two degeneracy above that size; this is a capability limitation, not an incorrect certificate.

## Endpoint and inertia audit

The valid low bracket requires no eigenvalues below a. An eigenvalue at a is allowed, and the closed Sturm interval includes it. The strict upper bracket b is required not to contain an eigenvalue, so the number strictly below b is exactly the cluster rank within [a,b]. Equality of negative counts at b and t excludes all eigenvalues in [b,t), while eigenvalues at t are allowed. Consequently all cluster energies are <b and all complementary energies are >=t, giving the conservative separation t-b.

A cluster covering the whole Hilbert space is not labeled as an excitation gap. Exact equality of all energies may still establish ground multiplicity equal to the full dimension; true_ground_gap_lower remains None.

## Exact root counting

For a positive diagonal metric W, W^-1 A is similar to the physical Hermitian matrix W^-1/2 A W^-1/2. Its characteristic polynomial therefore has the correct physical eigenvalues and is rational. Taking each squarefree part and their polynomial LCM forms the union of distinct roots across blocks. It avoids counting the same energy more than once across sectors.

Exactly one distinct root in the validated cluster bracket proves that every cluster state has the same energy. Since no state lies below a and the cluster is the bottom cluster, its counted rank is then the true ground multiplicity. More than one distinct root leaves true multiplicity and true-ground-gap fields unknown. No float tolerance enters equality decisions.

## Kramers inference

Time reversal squares to (-1)^(sum 2s_i). With odd parity and real coefficients, the supported bilinear exchanges and onsite Sz^2 are even. A nonzero field or odd spin product is rejected conservatively. Even spin products preserve time reversal; cancellation of symmetry-breaking terms is not inferred, which can cause false negatives but not false positives.

Kramers' theorem supplies only a double-degeneracy floor. An exhaustively covered rank-two bottom cluster must therefore be exactly one doublet, so its true ground multiplicity is two. A rank-four cluster is not automatically declared a fourfold ground space. The aggregate path requires conserved Sz, iterates every nonempty sector, verifies full dimension coverage, and fails on missing-sector budgets before invoking Kramers. The structural Kramers checker itself can apply without Sz conservation, but the sector certificate correctly rejects that case.

## Independent adversarial tests

Added tests/test_low_band_audit.py; six tests pass:

- Ground exactly at lower endpoint, eigenvalue at forbidden upper endpoint, complementary eigenvalue exactly at threshold.
- Unequal levels separated by 10^-100 remain two distinct roots, with no true-ground-gap claim.
- Weighted non-diagonal pencils with a doubly repeated irrational ground root.
- Half-integer parity, nonzero fields, odd/even spin products, and rejection of nonconserved sector restrictions.
- A rank-four Kramers-compatible cluster remains unresolved when root counting is budget-limited.
- Whole-space constant Hamiltonian has no excited-space gap.

Log: audit/low_band_adversarial_results.txt.

Two new actual CLI regressions also pass individually within the suite:

- unknown_degeneracy_chain.json contains no certificate, g, or E0 input and obtains true ground multiplicity two by exact root counting.
- Adding field 10^-10 creates an unequal rank-two cluster; the result is certified_low_energy_cluster with two distinct roots and no true ground multiplicity or true-ground-gap claim.

The first full 20-test CLI run had one unrelated expected source_or_environment_changed refusal while another agent edited source, rather than accepting mixed-version evidence. That provenance guard worked correctly. Stable rerun results are recorded separately in audit/cli_regression_results.txt.
