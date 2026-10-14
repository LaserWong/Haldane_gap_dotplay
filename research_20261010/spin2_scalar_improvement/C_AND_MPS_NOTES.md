# Additional bounded tests of C moments and existing MPS twists

Updated: 2026-10-10 14:31 EDT / 18:31 UTC.
These tests provide neither an accepted scalar startup nor a gap certificate.

## 1. Effect of the available C moments

The known C moments exclude the frozen integer I/P witness. We test whether
they also exclude the same unfavorable leading atoms in a PSD relaxation by
using the spin-0, spin-1 and spin-2 spectral measures S0,S1,S2. These satisfy

Z_identity=S0+3S1+5S2, Z_P=S0-S1+S2, Z_C=S0-S2,
I=S0, O=S2, N=S1+S2, J=S0+2S2.

A bounded finite-support linear program retained a fixed UNIT atom 1.03 in S0
and a fixed UNIT atom 1.02 in S1, and fitted all I/P/C moments 2..8 and the
exploratory I/P moments 9,10. After high-precision linear refinement, its nodes
and weights were written as exact rationals. A separate Fraction-only verifier
checks all 21 lower-order trace interval inclusions and errors below 10^-50
at orders 9,10. Every residual weight is strictly positive, with the smallest
about 0.0830. All implied Hankel and fixed-atom-removal PSD constraints hold.

The residual weights are positive rational masses, so this is NOT an
integer-multiplicity spectrum. The test imposes neither all-length trace
positivity nor cross-temperature consistency. It therefore shows only that
these additional moments do not exclude the specified unfavorable unit atoms
within this positive-measure relaxation. It does not establish a no-go theorem for a
stronger C-aware integer-spectrum method.

The first unscaled LP proposal was rejected because its moment residual, about
8.8e-4, was unacceptable. Rescaling the variables to fourth-moment mass removed
the conditioning problem caused by tiny coefficients. Only the final proposal,
verified with exact rational arithmetic, is reported as passing. The retained
final scripts reproduce it.

The supporting files are `c_aware_psd_rational_witness.json`, `c_aware_psd_verification.json`,
`verify_c_psd.py`. These are separate from the independently audited I/P packet.

## 2. A low-cost MPS extension with exact formulas

Let A_m be the recorded SU(2)-covariant physical MPS matrices, V_g the virtual
rotation, T the norm transfer, and O the ordinary two-site energy insertion.
The seam-matched trial state has amplitudes Tr(V_g A_(m1)...A_(mL)). Its norm
and total energy divided by L are obtained from

v_g(L)=Tr[(V_g tensor conjugate(V_g)) T^L],
u_g(L)=Tr[(V_g tensor conjugate(V_g)) T^(L-2) O],
e_g(L)=u_g(L)/v_g(L).

The covariance identity and cyclicity of the trace identify the seam-matched
twisted translation. After the prescribed seam rotation, all L bond
expectations are equal, which justifies the energy-density formula. A convention
may reverse the sign of the seam angle. This conjugation leaves the P and C
energies unchanged. A rigorous implementation must verify norm positivity and
retain the exact covariance assumptions. Ordinary periodic energies cannot
simply be relabeled as twisted energies.

In the existing highest-weight block decomposition, replace multiplicity 2j+1
by the character chi_j(g):

identity: 2j+1
pi twist: (-1)^j
2pi/3 twist: 1,0,-1 cyclically in j.

This substitution requires no new tensor optimization or physical diagonalization.
`mps_twist_screen.py` read the already frozen integer D124 blocks and performed
floating matrix powers, with maximum reduced dimension 423. It took about four
seconds on one numerical thread. The periodic energies reproduce the archived
Arb display values. These values are diagnostic and do NOT constitute a new interval certificate.

Selected floating-point energy densities are listed below.

| L | Identity | P | C |
|---|---:|---:|---:|
|128|-4.761255696888|-4.761205483003|-4.761218273414|
|256|-4.761218535854|-4.761218193517|-4.761218279113|
|512|-4.761218279125|-4.761218279109|-4.761218279113|
|1024|-4.761218279113|-4.761218279113|-4.761218279113|

At L128, the P trial misses the shift a=4.76121, while C passes numerically.
At beta8, combining the trial lower bounds with positive coefficients gives
J_128 >= (l_identity+3l_P)/4 approximately 1.008515 and
I_128 >= (l_identity+3l_P+8l_C)/12 approximately 1.008510.
Both combinations lie numerically above one despite the P-only failure.

A trace moment above one does NOT itself imply a single atom above one.
It must be combined with an upper lower-order moment as in the separate
atom-location lemma. The lemma already locates a positive trivial atom from the existing
total-trace MPS bound and global twist positivity, without requiring these
new contractions.

No Arb package was installed, and no new rigorous twist contraction was run.
No viable thermal certificate currently justifies that additional certification
effort. These formulas remain available for a bounded next step if a stronger
scalar-ratio proposal explains how it would use them.

## 3. Prospective-error sensitivity

`check_robust_hankel.py` uses exact rational determinants at all eight cached
betas 6,8,10,12,16,20,24,32. It removes a fixed J atom 1.03 and a fixed N atom
-1.02 at beta6 or +1.02 at the other betas, in the old a=4.7608 normalization.
The 4x4 signed Hankel remains positive definite for EVERY coordinate
perturbation |delta m_k|<=10^-4, k=4,...,10. Subtracting 4*10^-4 times the
identity leaves a positive-definite matrix, and row sums bound the entrywise
error norm.
The analogous 3x3 symmetric-support localizer also passes a rational row-sum
margin test with the proposed exploratory caps. Those caps are NOT promoted to
rigorous support bounds.

All these fixed atoms still have modulus above one at a=4.76121. The exact
algebra therefore establishes substantial slack. The fit is not near singular
in a way that the planned heat-trace rounding error alone would remove. It does not
certify the Ritz centers, their uncomputed truncation error, or a true physical
moment sequence at any of these temperatures.
