# Momentum-resolved compact tangent witnesses

## Exact convention and physical meaning

This extension fixes n=24 and the same archived real D26 state psi_n. Define

    v_j=(S_j^+/sqrt2) psi_n,
    C(r)=<v_0,v_r>, K(r)=<v_0,H_n v_r>.

Every v_j is in total Sz+1. Translation invariance of psi_n follows directly
from the cyclic trace of its MPS tensors. Commutation of H_n with translation
therefore gives the circulant integer matrices

    Gram_ij=C((j-i) mod n), Hform_ij=K((j-i) mod n).

Their symmetry and reality imply C(r)=C(n-r), K(r)=K(n-r). This does not
require reflection invariance or an exact SU(2) assignment. Thus13 independently
contracted displacements0,...,12 specify all24 at n=24.

## Exact energy accumulation and all overlapping terms

On each physical site, use B_s=A_(s-1), B_-1=0. The bra has a B insertion
only at site0, and the ket only at siter. All other bra/ket tensors are A.
If r=0, both insertions are on that same site. Let E_j denote the corresponding
one-site transfer. For a bond(j,j+1), O_(j,j+1) is built directly by summing
the physical h matrix against the two-site tensor products, putting B on
whichever bra/ket site is prescribed. There are nine needed local-H cases:
each bra/ket source is absent, on the first site, or on the second.

For a prefix of lengthl write P_l for the transfer product and Q_l for the
sum of all open-prefix bond insertions. With P_0=I and Q_1=0,

    P_l=P_(l-1) E_(l-1),
    Q_l=Q_(l-1) E_(l-1)+P_(l-2) O_(l-2,l-1).

The raw outputs are

    C(r)=Tr P_n,
    K(r)=Tr Q_n + Tr[E_1 ... E_(n-2) O_(n-1,0)].

The last term is the periodic seam, with the indicated bond order. Source
insertions touching an H bond, both sources on one site, sources on opposite
ends of a bond, and the n=2 doubled-bond convention are all included exactly.
Only charge-compatible rectangular auxiliary blocks are stored. Norm and
energy are GMP integers; local sparse transfer entries fit signed64-bit
integers, checked by the builder before serialization.

Direct full physical amplitudes and complete H actions at n=2,4,6 check every
displacement against this recurrence. At n24, the staggered Fourier sums are
also compared exactly to the previously frozen two-source polynomial results:

    n sum_r (-1)^r C(r)=||v_plus||^2,
    n sum_r (-1)^r K(r)=<v_plus,H_n v_plus>.

No physical support, many-body Hamiltonian matrix, or eigensolver at n24 is
constructed. The24-square Gram and H-form matrices are trial-space data,
not physical24-dimensional spectral blocks.

## Certified Fourier Rayleigh intervals

Let omega=exp(2pi i/24) and define

    Phi_k=sum_j omega^(k*j) v_j.

With translation T v_j=v_(j+1), Phi_k has eigenvalue omega^(-k). Distinct
nonzero modes are exactly orthogonal. Their norm and H numerators are

    ||Phi_k||^2=24 sum_r C(r) cos(k*r*pi/12),
    <Phi_k,H Phi_k>=24 sum_r K(r) cos(k*r*pi/12).

At multiples of15degrees the cosines are rational combinations of
sqrt2,sqrt3,sqrt6, obtained by the elementary angle-addition identities.
Each radical is enclosed by160-bit rational endpoints and checked by exact
squaring. Interval summation and division with a strictly positive lower
norm endpoint then certify a Rayleigh interval at every retained momentum.
The common factor24 cancels in each quotient.

The zero total-raising mode is omitted when its norm sum_r C(r) is exactly
zero. The H sum is independently checked to vanish there. Every other mode
must pass a strictly positive norm test; a merely rounded positive value
would not suffice. The k12 energy is required to equal exactly the frozen
staggered Rayleigh quotient, and opposite-momentum intervals must agree.

The spin flip F commutes with both H and translation, so each retained
Sz+1 mode supplies an exactly orthogonal Sz-1 partner with the same energy.
Adding psi_n and the frozen longitudinal momentum-pi state gives48 states
if all23 nonzero transverse modes pass. No unproved full spin-one multiplet
is counted. Each individual Fourier state has a site-dependent bond<=52
representation with the same two-by-two auxiliary source construction;
this is distinct from the48-dimensional retained denominator span.

## Scalar use and scope

For each certified momentum Rayleigh upper endpoint alpha_k^up, Jensen gives
a denominator term exp(-beta alpha_k^up). Combine these with psi and the
one longitudinal state. Opposite momenta and spin flips give multiplicity4
for representativesk1,...,11; the pi transverse pair plus longitudinal state
give multiplicity3 at k12. These are trial-state counts, not spectral
degeneracy claims.

The scalar verifier uses the same hot/cold proof and optimistic, joint-aware
recipe replay as the frozen three-state certificate, replacing its simple
denominator sum by these certified48 terms. Surviving coarse boxes are
subdivided into closed boxes of width1/64. Only exact nonpositive upper
updates prove exclusion; target-reaching or capped replays remain explicitly
inconclusive. Results are written separately in scalar_results.json.

This extension can rule out a particular fixed one-Rayleigh numerator and
seed recipe. It does not certify low eigenvalues, a physical gap or gaplessness,
or a universal minimum seed. It also does not supply the upper traces needed
for an actual successful bootstrap.

## Resources

All contraction processes use one pinned CPU and a700MiB address-space cap,
with600 CPU-second hard cap per process. The r0,1,12 n24 benchmark consumed
48.6 CPU seconds and52.9MiB peak. Its conservative13-displacement projection
was290.8 CPU seconds and105.9MiB. The other ten displacements were authorized
only after recording cost_gate.json. Actual resource totals are included in
the completed raw logs and final metadata. New large physical supports are
not part of this cost or this computation.
