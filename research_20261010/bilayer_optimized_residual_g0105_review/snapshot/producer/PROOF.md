# Complete residual of one optimized43D8x4 trial at g=.105

2026-10-10 22:54 UTC / 18:54 America/New_York. Producer physical result pending independent review. This is not an all-size gap certificate.

The proposed43D8x4 vector is the exact rational Rayleigh trial saved by the separately frozen bilayer_seed_error_budget study. It uses the existing accepted coupling-independent43D basis, with coefficient rounding at2^48. The physical model is the ordinary bilayer, H'=Q+(g/2)A, g=21/200. The complete integer action is T_int=400H'=400Q+21A.

The unchanged accepted residual_scalar.cpp engine and exact8x4 periodic geometry evaluate every fixed-origin q4 support(4,495) and q6 support(169,911). All three B,L,U coefficient families are saved in coefficients.txt; the vacuum coefficient remains in trial.json and is used in the separately assembled q0/q2 norm. The q8 norm is reconstructed from the complete CM norm plus SIGNED hard-core commutator expectation. Neither negative terms, cross terms nor nonzero images on M-zero supports are discarded. No q8 physical states are enumerated.

The exact Gram and first-Hamiltonian matrices at g=.105 are reconstructed from the accepted polynomial identities. Their q<=2 rows give the full low-sector image norm. Add all orthogonal q0,q2,q4,q6,q8 image norms, divide by400^2 times the exact trial norm, and subtract rho^2 to obtain the COMPLETE variance.

Result:

 complete variance = .0005240758184406096...,
 certified even-sector Temple ground lower = -.2801177779610626... .

The exact fractions, every sector norm and ground-identification/cutoff endpoints are in physical_result.json. The target variance from the error-budget study was .00039663744641237324..., so the chosen sufficient component target is NOT met. The actual result remains a valid improved candidate physical input and may be useful with another scalar allocation; it is not rejected simply because it misses that nonsharp target.

The mean remains below the global first-excited comparison. The97 retained denominator levels comprise this one even ground and96 independent odd modes. The existing fixed-z=.1 odd-family Gram and cutoff inequalities atg=.105 are unchanged. The new complete residual only changes the even ground lower. Any subsequent heat-trace calculation must retain all odd modes and the entire counted omitted tail.

## Arithmetic and resource bound

Source/binary/geometry/trial provenance is pinned in INITIAL_INPUT_SHA256.json and INPUT_SHA256.json. The engine retains its checked int64 geometry, checked128-bit scalar intermediates and arbitrary-precision quadratic sums. New coefficients have absolute value<=2^48; although the integer denominator is400 instead of40, coefficient×denominator magnitudes are less than10/256 of the previously justified conservative2^56,denominator40 envelope. The21A coefficient is likewise safely within that envelope after coefficient scaling. Explicit source overflow assertions remain enabled.

The full contraction ran onCPU3 under40CPU-second and100MiB address-space limits:4.74734 seconds,7,808KiB peakRSS. assemble.py is a separate pure-Python exact reconstruction under the same limits, without NumPy or eigensolvers. The command is saved in REPRODUCE.sh. Replay writes new output names and leaves this result frozen.

## Smallest saved4x4 enlargement, not yet contracted

The already accepted third-moment basis has16 columns: B(6)+L(5)+U(5), adding five H-applied directions to the11D B+L denominator family. outline_4x4.json contains an exact rational optimized trial mean and the complete-variance target for the selected sufficient ground endpoint. Its full image extends toq8, so a projected q<=6 residual would be insufficient.

A same-technique full residual would require455 fixed-origin q4 and3003 q6 supports, about56.6 times fewer q6 supports than8x4. A subsecond support pass plus startup is an estimate, not a measured run. A conservative initial40CPU-second/100MiB gate is proposed. No4x4 physical residual contraction is included here.
