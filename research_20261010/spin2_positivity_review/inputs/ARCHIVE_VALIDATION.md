# Validation argument and scope

This work is an extension of the uploaded *The periodic spin-one Haldane gap*,
not a proof of the spin-2 Haldane gap. Its new finite computations concern
H_n(theta)=sum_j S_j.S_(j+1) with spin 2 and a seam rotation about z, theta=0,pi,2pi/3.
The reference paper's spin-one thermal numbers are not used as spin-two data.

## 1. Complete finite spectra, not just small Ritz residuals

The exact Hamiltonian preserves total magnetization. A diagonal unitary distributes
the seam twist uniformly, giving hopping phase exp(i theta ds/n) on every bond.
Ordinary cyclic translation then commutes with it. Each word orbit of length p
contributes a normalized Fourier vector to momentum k exactly when kp=0 mod n.
If a hopping step takes a representative from an orbit of length p_i to the t-th
translate in an orbit of length p_j, its reduced coefficient is

    (sqrt(ladder_product)/2) sqrt(p_i/p_j)
       exp[2pi i k t/n + i theta ds/n].

This formula includes both ladder factors. For spin 2 the possible ladder products
are 16,24,36. The diagonal entries are integer sums of adjacent magnetic weights.
Each complex coefficient is enclosed with mpmath.iv at 60 decimal digits. Exact
Fraction comparisons verify that each real and imaginary floating coefficient is
within 2^-45 of its interval enclosure. Every column has at most 2n hopping
contributions. For n<=8 all partial entry sums have modulus below 512; thus an
error of 2^-42 per hopping contribution conservatively includes summation roundoff.
Consequently the physical-to-floating matrix error in Frobenius norm is bounded by

    eta0 = 2n (floor(sqrt(d))+1) 2^-42

in a d-dimensional translation block.

Reflection followed by complex conjugation is an antiunitary symmetry of each
momentum block. If reflection maps orbit i to the t-th translate of orbit j,
this antiunitary maps basis i to exp(2pi i kt/n) basis j. Pairing these orbits gives
a sparse unitary U with at most two entries in every row/column and converts the
exact Hamiltonian to a real symmetric matrix. The source code gives this U
explicitly; its coefficients use the same validated square-root/root-of-unity table.
The additional bound

    eta = eta0 + 256 (floor(sqrt(d))+1) 2^-42

covers errors in U and the two sparse matrix products. To see its conservative
scale, put eta_U=sqrt(d) 2^-43. The error from U alone is at most
(12n+1) eta_U (the physical norm is <=6n), the propagation of eta0 is at most
2 eta0, and the sparse product roundoff is <sqrt(d) 2^-36. Each inner product in
the transformation contains at most two terms, |U| has norm <2, and the absolute
row/column sums of the pretransformed matrix are below 256. For n<=8 these terms
are bounded by the displayed eta. Taking the real part is contractive relative
to the exactly real target and introduces no additional error.

For theta=0, reflection pairs k and -k at fixed magnetization. For theta=pi,
complex conjugation followed by the gauge transformation
exp[-(2pi i/n) sum_j j Sz_j] pairs k and -m-k mod n at magnetization m.
For any of the twists, spin flip followed by reflection pairs (m,k) with (-m,-k),
so k and -k also agree at m=0. Negative magnetization is included with multiplicity
two. Only symmetry-related blocks are omitted. Every completed data file checks
that all multiplicities sum to exactly 5^n. The pairing rules were also compared
against independently computed full momentum lists at n=4,5,6,7.

For n=2 the two edges are counted separately (H_2(0)=2 S_0.S_1). For n=3 the
usual triangular periodic ring is used. The same history-cycle identity extends
to these moments. The elementary bound ||H_n||<=6n is used, also at n=2.
No n=1 or order-zero spatial moment is assumed.

## 2. A posteriori eigenvalue inclusion

Let A be the exact real symmetric physical block, Ahat its computed matrix with
||A-Ahat||<=eta, and D=diag(theta_i) the computed eigenvalues. A *square* matrix
of all approximate eigenvectors is required. Freeze this matrix as a dyadic Q.
Verified bounds for

    epsilon >= ||Q^T Q-I||,   r >= ||A Q-Q D||

are computed. epsilon<1 is checked. The polar factor V of Q is orthogonal and

    ||Q-V|| <= epsilon/(1+sqrt(1-epsilon)) <= epsilon.

Hence

    ||A V-V D|| <= r+(||A||+||D||)epsilon = delta.

Weyl's theorem therefore gives, counting multiplicities and in sorted order,

    |lambda_i(A)-theta_i| <= delta   for EVERY i.

We use ||A||<=6n and explicitly check ||D||<6n+1. Thus delta is bounded by
r+(12n+1)epsilon, with a final exact upward dyadic rounding. This remains valid
for degenerate levels and does not infer spectral completeness from a small
residual. It is a deliberately elementary variant of full-eigensystem verification;
see Rump and Lange, JCAM 434 (2023), 115332, for substantially sharper general methods.

### Exact Gram products using ordinary BLAS

Q is frozen as Q=2^-26 Qh+2^-46 Ql, where Qh and Ql have integer entries.
The implementation verifies norm inequalities ensuring that each *absolute* dot
product sum in Qh^TQh, Qh^TQl, Ql^TQl is less than 2^53. Integer multiplication
and accumulation are then exact in IEEE binary64 (including FMA). Their scaled
combination gives the Gram defect. The final combining operations have a separate
roundoff allowance. Exact Python-integer Gram products independently test this
part of the verifier on four matrix sizes.

### Remaining arithmetic assumptions

For sparse products the standard error factor gamma_k=k u/(1-ku), u=2^-53, is
used with an enlarged coefficient (8(s+2)u for a real row of s entries). Nonnegative
row/column norm sums are checked with a 1.01 inflation. Frobenius norm displays
are multiplied by two before use as upper bounds; with the actual sizes, ranges
and nonnegative squared sums this dominates their accumulation error. The code
includes the Hamiltonian input error times ||Q||<2. It requires ordinary IEEE-754
binary64 arithmetic with no overflow, and the inclusion property of the interval
sqrt/trigonometric/exponential routines. This is NOT a Lean formalization, nor
an assertion that the scripts have been independently peer reviewed.

## 3. Thermal intervals at arbitrary beta

Binary floating theta_i values are exact dyadic inputs. They are grouped in dyadic
bins of width 2^-32; an additional outward spectral radius is included. Every
retained Boltzmann factor is evaluated with interval exponential arithmetic.
Energies whose entire *shifted* lower interval is at least 10 are omitted only with

    remainder <= (number omitted) exp(-10 beta).

Both eigenvalue error and thermal-tail error are therefore included. All finite
states are accounted for. Final endpoints are rounded outward as Fractions.
For n=4,beta=8 the new independent intervals are intersected with the previous
exact-integer polynomial certificates after confirming overlap.

## 4. Robust high-order spatial moment filters

For an even base b>=2 let M_j=sum_lambda lambda^j in one spatial symmetry list and
let H_ij=M_(b+i+j), i,j=0,...,r. Every atom satisfies

    H - lambda^b v(lambda)v(lambda)^T >= 0,   v=(1,x,...,x^r)^T.

Given rigorous intervals [c_j-e_j,c_j+e_j], form the midpoint Hankel matrix Hc and
D_ii=sum_j e_(b+i+j). Then H<=Hplus=Hc+D, by a row-sum bound on a symmetric error
matrix. Exact rational leading-principal-minor tests verify Hplus>0. It follows that

    lambda^b v(lambda)^T Hplus^-1 v(lambda) <= 1.

The inverse is computed in rational arithmetic. A proposed rational cap u is
accepted only after exact Sturm root counts show no zeros of
x^b v(x)^T Hplus^-1 v(x)-1 on either exterior ray, and its endpoint values are
strictly positive. Floating roots are proposals, not proof premises.
Odd moments are retained with their signs. There is no assumption that the spatial
transfer operator itself is positive. The order-10 screening uses unverified
truncated L=9,10 spectra and is explicitly labeled NON-CERTIFIED.

## 5. Higher-order thermal tails: what is and is not established

A separate exact angular-momentum argument proves for every z twist and m>=0

    E_min(H_n(theta)|M=m) >= (9/2)m-8n.

Indeed h12+h23 has eigenvalues
[J(J+1)-A(A+1)-6]/2, A=0,...,4, J=|A-2|,...,A+2.
After subtracting 3 Mtriad the minimum is -16. Summing all overlapping triads
with factor 1/2 gives H_n-(9/2)M>=-8n. The local z-axis gauge change removing
a seam does not change this field. Exact magnetization dimensions and interval
exponentials therefore bound the uncomputed |M|>=8 contribution for L=10,beta=8.
This high-magnetization tail bound is rigorous under the stated interval arithmetic.

In contrast, replacing the omitted in-sector energies by the last Ritz energy is
NOT rigorous without an independent eigenvalue count. The bundle reports that
quantity only as a conditional diagnostic. A possible next implementation would
use validated inertia counts at an energy cutoff, followed by
(d-r)exp[-beta(E_cut+a n)] for the remaining in-sector trace. Such inertia checks
have NOT been performed here.
