# Complete 8x4 denominator residual and ordinary-bilayer g=.10 candidate

2026-10-10 17:51 EDT / 21:51 UTC.

The q8-free hard-core commutator calculation succeeds. The fixed 8x4 enlarged trial has complete variance .0003553876503424027 and actual Temple ground lower -.2532914854282799. Independent physical replay has matched every component. The separate exact scalar candidate is

    gap >= .038976038275, every integer square L>=2, g=.10.

The all-size scalar review is pending. No continuous-coupling or infinite-volume uniqueness claim is made here.

The computation took3.52 seconds on one CPU,7808 KiB RSS. It includes all q0/q2/q4/q6 image pieces and the exact q8 norm via a hard-core local commutator, with no q8 enumeration. The 8x4 q6 sum includes all169,911 fixed-origin supports, including those where M vanishes. The two terms in the commutator norm identity are retained with their signs.

Dimensions remain distinct: 8x4 has64 physical spins and full Hilbert dimension2^64; the ground trial search has43 columns but contributes one ground state to the97-level denominator band. The largest8x8 numerator remains one state from a43D search,128 physical spins, full dimension2^128. The4x4 denominator, odd bands and counted tails remain unchanged.

## Separate freezes

- PHYSICAL_MANIFEST.json: source, coefficients, geometry, sector norms, complete variance and actual Temple lower; SHA-256 7d6269e8b080301cf7f941f9c3b9fd9e3f1db339ce2587bd078ed3ded96def95
- SCALAR_MANIFEST.json: actual point trace inputs, all exact states/windows/short sizes; SHA-256 0c7abb4cee911bb2c42990c0402b00dd7ecf62e0d607775d1f1c69c205424555
- POLYNOMIAL_MANIFEST.json: exact fixed-vector norm, affine mean, quadratic complete second moment and variance, ready for a future interval calculation; SHA-256 96027b2dbe17e94c922a3884122ff96c525354a359e143e38328fbd3abbbc3ed

PHYSICAL_PROOF.md gives the full sector decomposition and integer guards. SCALAR_PROOF.md gives the point scope. COUPLING_POLYNOMIAL_PROOF.md derives the fixed-vector coupling coefficients by operator affinity, without fitting point values.

The candidate uses beta_initial47/5. Required early window gaps are .052015820732 on8..16, .054902632007 on16..32, and .055049054532 on32..64. The terminal bootstrap starts at side64 with physical beta752/5 and supplies the final minimum .038976038275. Short sides2..7 use the unchanged reviewed comparison.

Run bash REPRODUCE.sh to verify all seals, run a fresh physical contraction into a new replay directory, and compare every exact norm plus the scalar candidate. Earlier sealed files are not overwritten. Independent review is in ../bilayer_complete_residual_8x4_review. No repository root, earlier seal, or GitHub file was changed by this producer.
