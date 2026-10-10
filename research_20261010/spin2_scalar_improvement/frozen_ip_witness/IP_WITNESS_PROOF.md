# A finite I/P moment obstruction, with exact rational atom data

Updated: 2026-10-10 14:28 EDT / 18:28 UTC.

## Result and precise scope

The saved beta-8 I/P moment boxes through order 10 cannot justify an
unconditional nontrivial-sector mass bound below one or a successful
numerator-one thermal certificate. This remains true if all their signed
Hankel constraints, unit atom multiplicities, and positivity of twisted traces
at every integer length L >= 2 are retained. The evidence is an explicit finite real spectrum, verified
using exact rational arithmetic. It is an obstruction to this specified
finite-moment inference, not to the physical Heisenberg gap.

The actual model remains the periodic, unit-coupling, isotropic spin-2 chain.
Input normalization is a0 = 5951/1250 = 4.7608, beta = 8. The present rational
spectrum is an adversarial abstract spatial transfer spectrum. It is NOT a
Hamiltonian spectrum or a construction of a local quantum transfer operator.

Important omissions: this exact integer-spectrum witness does not match the
available C-twist moments and does not impose beta/2beta semigroup consistency.
Neither omission can be silently dropped when interpreting the result. In
particular, this singlet/triplet realization gives C(8)=M_J(8) about 8.6054184342,
whereas the archived C trace is about 0.6267926, so that known C datum excludes
THIS integer witness.

## Exact data and moment verification

`full_integer_witnesses.json` lists 17 rational eigenvalue groups in each of two
lists J and N. Every decimal node is interpreted as the exact rational number
it spells; each count is a positive integer. There is no floating tolerance in
the interpretation of these atoms. Their total list dimensions are

- J: 1,752,765,679,903,846,037
- N: 1,752,713,560,036,067,552 (one of three identical nontrivial lists)

These are artificial spatial-spectrum dimensions, not physical Hilbert-space
or MPS dimensions. Large multiplicities near zero are allowed by the moment
hypotheses; they are the reason adding moments 2 and 3 does not rescue this case.

Write M_s(k) = sum_j n_(s,j) x_(s,j)^k. Set
Z_I(k) = M_J(k) + 3 M_N(k), Z_P(k) = M_J(k) - M_N(k).
The exact verifier checks the actual Z_I and Z_P rational values against the
archived rational trace intervals at EVERY order 2,...,8. It does not merely
compare with midpoints to a numerical tolerance. All 14 inclusions are strict.

For orders 9 and 10 the source is incomplete Ritz data, not a trace certificate.
The centers are reconstructed from the saved J/N decimals, using the same two
linear combinations. The reconstructed I9 center differs from the separately
saved Z9 decimal by about 3.95e-16, far below the proposed radius. The witness differs from both I/P centers by less than
10^-48. The prospective absolute error radii tested are

- order 9: 6/10^6
- order 10: 5/10^5.

These conservative radii exceed the audited beta-8 fixed-point heat-trace error
estimates 5.77072e-6 and 4.43571e-5, respectively, conditional on Z <= 100. Those
estimates are absolute errors, not unconditional validated intervals around the
Ritz centers. The counterexample is an obstruction if one uses THESE proposed boxes, or if
each future admitted interval still contains the corresponding witness moment.
A narrower certified subinterval merely lying within these boxes need not
contain the witness, and is not ruled out by this argument. An unknown omitted
Ritz contribution may move the true moments; this computation does not certify
that contribution.

Since these are actual unit-multiplicity atoms, every joint Hankel PSD condition
and every finite-atom-removal condition formed from them holds automatically.
The construction is stronger than checking a handful of PSD minors or assuming
that positive quadrature weights are integer multiplicities.

## Positivity at every length, without an unbounded numerical scan

The leading atoms are alpha = 103/100 in J and gamma = 51/50 in N, each with
multiplicity one. Every other atom has modulus strictly below r = 3/4.
Let C_J and C_N be the exact tenth moments of those remainder atoms.
For every integer k >= 10,

|remainder_J(k)| <= C_J r^(k-10),
|remainder_N(k)| <= C_N r^(k-10).

The verifier checks Z_I(k) > 0 and Z_P(k) > 0 exactly for 2 <= k < 32. At k=32
it checks both

alpha^32 + 3 gamma^32 - (C_J+3C_N) r^22 > 0,
alpha^32 - gamma^32 - (C_J+C_N) r^22 > 0.

The positive leading expressions increase with k; the remainders decrease.
For the second one use alpha > gamma > 1, so
alpha^(k+1)-gamma^(k+1) > alpha^k-gamma^k. This proves positivity for all k>=32.

The abstract spectrum may be organized into SU(2) singlets (J) and triplets
(N). For a rotation angle theta its character trace is
M_J(k) + (1+2 cos(theta)) M_N(k). As 1+2cos(theta) ranges over [-1,3], the two
proved endpoint inequalities even imply positivity at every rotation angle.
This does not make its C moments equal to the archived C moments.

## Failure of the present startup

After changing the shift to a1 = 4.76121, every atom is multiplied by
rho = exp[-8(a1-a0)] = exp[-0.00328]. Both leading atoms remain above one.
The exact verifier uses an odd Taylor lower bound for exp(-0.00328 L) to
certify Z_I(L;a1) >= rho^L(alpha^L+3 gamma^L).

At L=128 it proves Z_I > 53.761701. Thus any upper bound U deducible from the
stated moment hypotheses must allow U > 53.761701. The numerator-one thermal
certificate 1/U^2 can consequently be at most 0.000345983, very far from 7/8.
The actual spatial purity of this admissible spectrum is
S(64,8) in (0.273805237, 0.273805238). The nontrivial-sector leading contribution
alone exceeds 24.866 at L128. Therefore no UNCONDITIONAL N-sector upper bound
below one follows from these I/P boxes, even using all joint signed Hankel and
integer-atom information. This is not a counterexample to a conditional
atom-exclusion argument with an additional hypothesis that all J atoms have
modulus at most ell<1.03: this witness does not obey that additional hypothesis.
That conditional strategy must be assessed separately.

At L = 256,512,1024, the respective spatial purities are about
0.360188494, 0.656301667, 0.960713369. Their numerator-one thermal upper limits
are below 9.23e-7, 1.98e-12, 4.24e-24. Larger startup length does not solve the
single-trial numerator/denominator obstruction.

More generally, both rescaled leading atoms exceed one, so this witness has
Z_I(L;a1)>4 for every even L>=2. Thus no numerator-one thermal certificate
obtained solely from these boxes can exceed 1/16 at any such length.

These are limits on a sufficient proof construction. They are not upper bounds
on the actual spin-2 chain's thermal purity.

## Reproduce

Run `python verify_integer_witness.py` with one numerical thread. It uses only
the Python standard library and exact Fractions for acceptance. The root file
`exact_witness_verification.json` records every accepted interval check and the
all-length tail inequalities. `refine_full_witness.py` explains how the rational
candidate was found, but is not needed to verify it. No many-body diagonalization,
new trace campaign, installation, or MPS tensor rebuild was performed.
