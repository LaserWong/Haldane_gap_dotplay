# Whole-spectrum comparison with a stable quadratic boson Hamiltonian

2026-10-10 14:26 America/New_York / 18:26 UTC.

This is a separate proposed theorem extending the hard-core embedding in
`../bosonic_tail/BOSONIC_COMPARISON.md`. It does not modify any existing physical
input or released certificate. Independent review is required.

## 1. Physical operator and compression

Let H'=H+3N/4 be the ordinary spin-1/2 bilayer Hamiltonian with equal straight
in-layer couplings g>=0. The rung graph is a finite degree-four weighted periodic
torus, with every length-two parallel edge retained through its multiplicity.
Let Q count triplet rungs. The independently established local preserving-block
bound gives

    H'_pres >= alpha Q,       alpha=1-2g.

Embed the rung basis into the bosonic Fock space of D=3N modes, one triplet color
per mode at each rung. Let P project onto at most one boson per rung. Its range
has dimension 4^N and is exactly the physical rung Hilbert space. Let A be the
weighted adjacency matrix and let J be the real symmetric orthogonal triplet
singlet-pairing matrix J_00=1, J_+-=J_-+=-1. Define

    K=(g/2) A tensor J,
    B=(1/2) sum_(u,v) K_uv a_u^dagger a_v^dagger,
    L=alpha Q+B+B^dagger.

The physical number-changing part is exactly P(B+B^dagger)P. In quadratic form
sense on the finite-dimensional physical space,

    H' >= P L P.

No claim is made that P commutes with L. No physical triplet-number conservation
is assumed. Every physical basis vector has finitely many particles and lies in
the form domain of L.

## 2. Exact diagonalization of the comparison operator

The real symmetric matrix K has an orthogonal diagonalization with real
eigenvalues kappa_j. The mode rotation preserves total number and transforms L
into the sum of D independent operators

    alpha b_j^dagger b_j + (kappa_j/2)(b_j^dagger^2+b_j^2).

Writing b_j=(x_j+i p_j)/sqrt(2), with [x_j,p_j]=i, this is

    ((alpha+kappa_j)/2)x_j^2 + ((alpha-kappa_j)/2)p_j^2 - alpha/2.

Assume strictly alpha>||K||. Each coefficient is positive. A unitary dilation of
x_j,p_j reduces this operator to a harmonic oscillator of frequency

    omega_j=sqrt(alpha^2-kappa_j^2)>0.

Equivalently, the Hermite eigenfunctions after this dilation give the complete
one-mode spectrum (n+1/2)omega_j-alpha/2. Taking the tensor product of these
finite D one-mode unitary transformations gives a unitary U on bosonic Fock
space such that

    U L U^dagger = E_quad + sum_j omega_j n_j,
    E_quad = (1/2) sum_j (omega_j-alpha).

Because the graph has weighted degree four, ||A||=4 and ||K||=2g. Thus
alpha>||K|| is precisely g<1/4. Put

    delta=sqrt(alpha^2-4g^2)=sqrt(1-4g),
    v=(1/2)Tr(K^2)=(3g^2/4) sum_edges w_e^2.

Then omega_j>=delta, and

    E_quad = -(1/2) sum_j kappa_j^2/(alpha+omega_j)
            >= -v/(alpha+delta) = E_b.

The full operator comparison after the Bogoliubov unitary is therefore

    U L U^dagger >= E_b I + delta Q_b.

Here Q_b is the ordinary total-number operator in the transformed oscillator
basis. It is not the original physical triplet-number operator. In particular,
this argument does not presume that the actual first D excited levels of L are
all one-boson levels: varying frequencies can change their ordering. The
operator comparison with equal frequencies handles every ordered eigenvalue at
once.

## 3. Ordered spectral bounds under finite hard-core compression

The stable finite-mode oscillator has compact resolvent and a discrete spectrum
bounded below. Its form-domain min-max principle applies to the finite
hard-core trial subspace. For every 1<=j<=4^N,

    lambda_j(H') >= lambda_j(P L P|ran P)
                 >= lambda_j(L)
                 >= lambda_j(E_b+delta Q_b).

The last reference spectrum has energies E_b+q delta and exact multiplicities

    d_q = binomial(D+q-1,q),       q=0,1,2,...,

with d_0=1 and d_1=D=3N. In particular,

    lambda_1(H') >= E_b,
    lambda_2(H') >= E_b+delta,
    lambda_(2+3N)(H') >= E_b+2delta.

These are all-state counts. They do not rely on a chosen physical symmetry
sector or a trial residual. Once a complete trial band of dimension 1+3N lies
below the last cutoff, the already proved invariant-sector Temple or general
moment-pencil bounds apply unchanged.

## 4. Complete omitted heat trace

For beta>0, let z=exp(-beta delta). The full oscillator reference trace is

    exp(-beta E_b) (1-z)^(-D).

Its first 1+D ordered reference terms are exp(-beta E_b)(1+D z). Therefore the
physical tail after any certified full low band of that dimension satisfies

    sum_(j>1+D) exp(-beta lambda_j(H'))
      <= exp(-beta E_b) [(1-z)^(-D)-1-D z].

This uses the ordered min-max comparison, not a positivity-monotonicity claim
for matrix exponentials. The infinite series is finite for beta>0 and delta>0.
Its positivity and all its multiplicities are explicit.

There is also a useful finite overcount. The physical rung basis embeds into
the original boson number sectors q<=N, so

    4^N <= sum_(q=0)^N binomial(D+q-1,q).

The reference ordered list has at least 4^N entries before q exceeds N. Thus the
same physical omitted trace is bounded by the finite sum

    sum_(q=2)^N binomial(D+q-1,q) exp[-beta(E_b+q delta)].

This finite truncation is justified by an ordered dimension count; it does not
identify the physical subspace with q<=N after the Bogoliubov unitary. It may
overcount some reference levels in its last bin, which only weakens the bound.
The infinite formula remains valid and avoids any need for this truncation.

## 5. Exact arithmetic implementation conditions

Choose a rational delta_lower satisfying 0<delta_lower<=sqrt(1-4g), verified by
integer squares. Set E_b_lower=-v/(alpha+delta_lower). Then

    E_b_lower <= E_b,
    E_b_lower+q delta_lower <= E_b+q delta.

Consequently rational bins with these endpoints and the same bosonic
multiplicities are rigorous. No floating diagonalization of K, no many-body
spectrum, and no sparse-state construction are needed for these bins. Period-2
normalization enters v through the squared combined edge weights; replacing
sum w_e^2 by sum w_e on such a graph would be wrong.

For N=64, g=.06, alpha=.88, delta=sqrt(.76), v=.3456, this gives

    E_b approximately -.197285071,
    E_b+delta approximately .674494718,
    E_b+2delta approximately 1.546274507.

These illustrative decimal values are not acceptance endpoints. Any numerical
use must retain verified directed rational bounds and independent review.
