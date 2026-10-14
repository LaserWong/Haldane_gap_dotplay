# Complete 8x4 denominator residual and ordinary-bilayer g=.10 candidate

2026-10-10 17:51 EDT / 21:51 UTC.

The hard-core commutator calculation obtains the q8 norm without enumerating q8 configurations. The fixed 8x4 enlarged trial has complete variance .0003553876503424027 and actual Temple ground-energy lower bound -.2532914854282799. Independent physical replay has matched every component. The separate exact scalar candidate is

    gap >= .038976038275, every integer square L>=2, g=.10.

The all-size scalar review is pending. No continuous-coupling or infinite-volume uniqueness claim is made here.

The computation took 3.52 seconds on one CPU and used 7808 KiB RSS. It includes all q0/q2/q4/q6 image pieces and the exact q8 norm via a hard-core local commutator, with no q8 enumeration. The 8x4 q6 sum includes all 169,911 fixed-origin supports, including those where M vanishes. The two terms in the commutator norm identity are retained with their signs.

The 8×4 denominator contains 64 physical spins and has Hilbert-space dimension 2^64. Its 43-column ground-state search contributes one state to the 97-level denominator band. The largest 8×8 numerator contains 128 spins, with dimension 2^128, and retains one state from a 43D search. The 4×4 denominator, odd bands, and counted tails remain unchanged.

## Physical, scalar, and polynomial records

- PHYSICAL_MANIFEST.json: source, coefficients, geometry, sector norms, complete variance and actual Temple lower. SHA-256 7d6269e8b080301cf7f941f9c3b9fd9e3f1db339ce2587bd078ed3ded96def95
- SCALAR_MANIFEST.json: actual point trace inputs, all exact states/windows/short sizes. SHA-256 0c7abb4cee911bb2c42990c0402b00dd7ecf62e0d607775d1f1c69c205424555
- POLYNOMIAL_MANIFEST.json: exact fixed-vector norm, affine mean, quadratic complete second moment and variance, ready for a future interval calculation. SHA-256 96027b2dbe17e94c922a3884122ff96c525354a359e143e38328fbd3abbbc3ed

PHYSICAL_PROOF.md gives the full sector decomposition and integer guards. SCALAR_PROOF.md gives the point scope. COUPLING_POLYNOMIAL_PROOF.md derives the fixed-vector coupling coefficients by operator affinity, without fitting point values.

The candidate starts at beta_initial=47/5. Its early windows require gaps .052015820732 on sides 8–16, .054902632007 on 16–32, and .055049054532 on 32–64. The terminal bootstrap begins at side 64 and physical beta=752/5, giving the final minimum .038976038275. Sides 2–7 use the unchanged reviewed comparison.

Run bash REPRODUCE.sh to verify all seals, run a fresh physical contraction into a new replay directory, and compare every exact norm plus the scalar candidate. Earlier sealed files are not overwritten. Independent review is in ../bilayer_complete_residual_8x4_review. No repository root, earlier seal, or GitHub file was changed by this producer.

