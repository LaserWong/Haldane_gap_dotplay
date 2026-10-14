# Compact exact excited-MPS seed diagnostics

Updated 2026-10-10 17:34 EDT / 21:34 UTC.

The fixed archived D26 numerator cannot start the stated thermal-first,
joint-aware recipes at denominator lengths 14, 16, or 20, for any beta >= 0.
The proof uses only three fixed, orthogonal denominator witnesses. A fourth
longitudinal witness strengthens the bounds. These two stages have passed
independent review in `../mps_excited_seed_review`.

At length 24 the three-state necessary screen leaves the closed union
[13/2,45/4] inconclusive. A fourth witness shrinks that union to [31/4,11].
The completed momentum-resolved extension in `momentum_extension` retains 48
orthogonal states at n24 and narrows the unresolved closed interval to
[533/64,679/64]=[8.328125,10.609375]. Exact vanishing of the total-raising norm
then proves the fixed n24 state is a singlet and justifies all normalized
lowered partners. The separately frozen `singlet_completion` retains 70 states
and shrinks the interval to [539/64,339/32]=[8.421875,10.59375], without new
n24 contractions. These two later stages are frozen for independent review.
Surviving a screen does not supply denominator upper traces or a gap certificate.

## Dimensions and representation

- Physical model: periodic, unit-coupling spin-1 Heisenberg H=sum S_j dot S_(j+1).
- Original fixed MPS bond dimension: 26. Each one-operator tangent witness has
  a representation of bond dimension at most 52.
- Retained denominator span: 3,4 with the longitudinal extension, 48 in the
  initial n24 momentum extension, or 70 after the rigorously derived finite-n24
  singlet completion. Retained numerator span: 1. No variational coefficient
  search or eigensolver is used.
- Largest auxiliary charge-block side: 162. The two-source polynomial has
  299,372 integer matrix entries across its four charge-compatible coefficients.
- At n=24 the physical denominator dimension is 3^24=282,429,536,481. The
  numerator at 48 has dimension 3^48. Neither physical support is constructed.
- Only n=2,4,6 are expanded for direct exact physical fixtures. No eigensolver
  or full spectrum is used.

The n14/16 benchmark used 26.6 CPU s and 53.2 MiB. The recorded n24 projection
was 59.8 CPU s and 106.5 MiB. The actual complete contraction through 24 used
16.6 CPU s and 64.7 MiB. The longitudinal contraction used 18.7 CPU s/66.5 MiB.
Ordinary exact numerator contractions through 48 used 7.6 CPU s/18.8 MiB.
All 13 independent n24 displacement contractions used 231.44 CPU s/53.0 MiB.
The refined 48-state scalar coverage used 24.74 CPU s/11.1 MiB. Their remaining
displacements follow exact translation/reality symmetry, without assuming
reflection invariance or exact spin multiplets.
The 70-state completion used under 1 CPU s for the algebra/physical fixtures
and 37.55 CPU s for its refined scalar coverage.

## Review and reproduction

`PHYSICAL_MANIFEST_SHA256.json` freezes the three-state physical inputs.
`SCALAR_MANIFEST_SHA256.json` freezes their directed rational scalar replay.
`longitudinal_extension/MANIFEST_SHA256.json` separately freezes the fourth
state and the exact hypothetical trace-budget check. Do not rewrite frozen
outputs during review. Run `REPRODUCE.sh` only in a disposable sibling copy.
The momentum physical/scalar manifests and the singlet completion manifest
freeze each later stage separately. The root `MANIFEST_SHA256.json` and
`SEAL.json` seal the whole producer deliverable.

`PROOF.md` states the exact construction, all-temperature coverage, and scope.
`exact_witness_data.json` and `scalar_results.json` contain all rational data.
The extension's files use the same names within its own directory.

The three-state hypothetical 0.5% trace slack at n24, beta8 would give a scalar
success. However, the fourth state proves the physical trace is at least
1.01893421066 times that three-state sum there, so that premise is impossible.
This is an explicit illustration of why an optimistic lower-trace screen is
not an upper-trace certificate.

No conclusion here identifies exact low eigenvalues, proves a physical gap
or gaplessness, or establishes a universal minimum seed size. The fixed
numerator, stated denominator witnesses, and stated recursion are essential.
