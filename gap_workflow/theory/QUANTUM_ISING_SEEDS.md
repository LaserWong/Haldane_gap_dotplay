# Exact finite quantum Ising traces and numerical canonical seeds

## Scope and result

Consider H_L = -J sum_(i=0)^(L-1) Z_i Z_(i+1) - h sum_i X_i, with J >= 0, real h, periodic indices, and L >= 2. Pauli matrices have eigenvalues +/-1. At L=2 the two positive-direction bonds both occur, giving -2J Z_0 Z_1. All formulas below use this convention. Global conjugation by the product of Z_i changes h to -h, so write g=|h|.

The complete finite partition function can be evaluated with two lists of L single-particle modes, without enumerating the 2^L many-body levels. The implementation evaluates an exact analytic formula numerically. Its outputs are explicitly NOT certified intervals and are not supplied as exact bounds to the bootstrap adapter.

A strongly interacting example, J=1, h=1.5, n=16, beta=8, has numerical canonical purities 0.99586104532973856665 and 0.99870423197679716273. The dedicated one-dimensional entry test u<=0.01 succeeds numerically, with candidate log(1/(5u))/beta = 0.48473426321237546909. This is an encouraging seed, not yet a uniform physical gap certificate.

## Exact parity formula

Define the NS and R momenta, each with L entries,

    K_NS = {2*pi*(m+1/2)/L : m=0,...,L-1},
    K_R  = {2*pi*m/L : m=0,...,L-1},
    eps(k) = 2*sqrt((J-g)^2 + 4*J*g*sin(k/2)^2).

For a momentum set a, put

    C_a = product_(k in K_a) 2*cosh(beta*eps(k)/2),
    S_a = product_(k in K_a) 2*sinh(beta*eps(k)/2).

Then for beta>=0,

    Z_L(beta) = (C_NS + S_NS + C_R - sign(g-J)*S_R)/2.       (1)

At g=J the R zero mode gives S_R=0; the sign convention at zero therefore has no effect. At J=g=0 use the same vanishing-product interpretation.

Derivation: rotate the spin axes to put the field along the fermion quantization axis and apply Jordan-Wigner. The physical even-fermion sector has antiperiodic (NS) momenta, while the odd sector has periodic (R) momenta. Paired nonzero Bogoliubov modes preserve parity. The NS vacuum has even parity for J,g>=0. In the R sector the zero-momentum unpaired mode changes the vacuum parity when g-J changes sign; a possible pi mode has positive coefficient g+J. Consequently the NS projection selects even quasiparticle occupation; the R projection selects odd occupation for g>J and even occupation for g<J. Trace with or without quasiparticle parity gives C and S, respectively, proving (1). At the zero mode, the two occupation parities have equal partition weight. This argument also covers odd L: the unpaired pi mode then lies in NS instead of R, with positive coefficient. Direct L=2 spin algebra confirms the doubled-bond convention.

Parity references: Bialonczyk, Gomez-Ruiz and del Campo derive finite spin-chain thermal quantities keeping both physical parity sectors, and explain why retaining only positive parity is an approximation [SciPost Phys. 11, 013 (2021)](https://arxiv.org/abs/2103.16322). The sign issue is explicitly discussed in the [supplement to Phys. Rev. Research 6, 043139 (2024), Eq. S5](https://journals.aps.org/prresearch/supplemental/10.1103/PhysRevResearch.6.043139/Zero2SM_r.pdf): the R sinh product enters with a minus sign on the disordered side. Equation (1), our implementation, and the independent ED audit agree with that correction. The rest of this note develops and tests our numerical seed construction.

## Cancellation-free evaluation

Directly subtracting C_R-S_R at low temperature loses precision. Let q_k=exp(-beta*eps(k)). Initialize E=1, O=0 and update once per mode:

    E_new = E + q_k*O,
    O_new = O + q_k*E.

The updates are simultaneous. E and O are the even and odd elementary-product sums, so

    E = [product(1+q_k)+product(1-q_k)]/2,
    O = [product(1+q_k)-product(1-q_k)]/2.

A sector contribution is exp(beta*sum eps/2) times the selected E or O. Both are sums of nonnegative terms. The code runs this recurrence in logarithmic coordinates using logaddexp and adds the two sector weights in the same way. It therefore does not subtract nearly equal parity products or overflow on extensive vacuum energies. The representation computes all occupations implicitly in O(L) arithmetic operations and O(1) auxiliary storage. Arbitrary precision still needs sufficient digits when subtracting extensive log Z values to obtain purities; agreement of two precisions is a diagnostic, not a rigorous error bound.

### Bounded-factor energy shift for interval arithmetic

Choose c=J+g and define Z_tilde_L(beta)=exp(-beta*c*L)*Z_L(beta). Since 0<=eps(k)/2<=c, the factors

    a_k=exp[-beta*(c-eps(k)/2)],
    b_k=exp[-beta*(c+eps(k)/2)]

are in (0,1]. Start E=1,O=0 and update simultaneously E_new=a_k*E+b_k*O, O_new=a_k*O+b_k*E. Select the same physical quasiparticle parity in each sector as before, then add the sectors. This directly gives Z_tilde, without huge exponential prefactors and without signed subtraction. For rational J and h, c is rational. The shift cancels exactly in BOTH canonical purity ratios, so Z_tilde can replace Z throughout (2). The function shifted_partition_mp implements this additional arbitrary-precision candidate API. An independent rational interval backend can apply the identical positive recurrence to outward-enclosed a_k,b_k.

## Canonical spatial and temporal seeds

For even n>=2 and beta>0, evaluate precisely these three traces:

    A=Z_n(beta), B=Z_(2n)(beta), C=Z_(2n)(2beta).

The canonical edges are

    P_x(n,beta) = B/A^2,
    P_beta(2n,beta) = C/B^2.                                (2)

The second edge is based at length 2n, not n. The homogeneous bond -J Z tensor Z satisfies the exact realignment eligibility criterion in TRANSFER_ELIGIBILITY.md, while -h X is a real symmetric onsite term. Thus the exact selfadjoint spatial history transfer exists; even n makes (2) its purity ratio. The temporal edge follows directly from exp(-beta H). This eligibility uses the exact continuous-time construction, with no finite Trotter approximation.

The survey uses n=2,4,8,16; h/J=0.5,1,1.5,2; J=1; and beta=0.125,0.25,0.5,1,2,4,8,16,32,64,128. Each of 176 seeds is evaluated at 80 and 120 decimal digits. No seed-generation step computes any many-body eigenpair. Each seed evaluates 10n single-particle modes in total. The benchmark also applies the numerical version of the existing sequential scalar recurrence; those results remain numerical candidates.

On this beta grid, best direct entry defects are:

| h/J | n=2 | n=4 | n=8 | n=16 |
|---|---:|---:|---:|---:|
| 0.5 | .507908 | .501002 | .500009 | .500000000316 |
| 1 | .565763 | .549110 | .545182 | .544214 |
| 1.5 | .427782 | .266522 | .0802881 | .00413895 |
| 2 | .345410 | .134386 | .0116738 | .0000619852 |

The n=16,h=2,beta=8 candidate bound is 1.00989721834117584054; beta=4 instead gives a larger candidate bound 1.12107204394813602595 despite a larger defect. Maximizing the candidate gap and minimizing the defect are different objectives. Numerical sequential replay also enters from n=8,h=1.5,beta=4 after two cycles (candidate gap 0.26702295679), and from n=4,h=2,beta=2 after three cycles (candidate gap 0.33133936589). These are minima over the listed beta grid only, not optimized or rigorous exclusion results.

## What fails on the ordered side

For 0<g<J the finite periodic ground state is unique, but the other parity sector lies exponentially close as L grows. There cannot be a uniform positive finite-volume gap above that single ground state across the family. The positive bulk quasiparticle mass 2|J-g| must not be substituted for that finite-volume spectral gap. At g=0 there are exactly two ground states for J>0; the rank-one thermal purity tends to 1/2. At criticality the finite-size gap also tends to zero. Hence failure of rank-one bootstrap entry in these regimes is physically appropriate and does not diagnose absence of a gap above a symmetry-broken ground-state manifold. No inference of gaplessness is made merely from a failed seed search.

## Analytic small-size bridge on the paramagnetic side

For g>J>=0, an independent integrable comparison proves

    gap(H_L) >= 2*(g-J)  for every integer L>=2.              (3)

This is a model-specific analytic bridge, not a conclusion inferred from the numerical seed. It is stronger than the displayed bootstrap candidates and also serves as an independent check of them. In particular it covers every early size below a chosen seed n, including odd sizes.

Here is a direct proof. Put omega(k)=eps(k)/2, a=g^2+J^2, b=2gJ, and define Fourier coefficients omega_hat(m)=(1/(2*pi))*integral_0^(2*pi) omega(k)*exp(-imk) dk. The elementary Laplace identity

    sqrt(x) = [1/(2*sqrt(pi))]*integral_0^infty (1-exp(-t*x))*t^(-3/2) dt

implies for every integer m!=0

    omega_hat(m) = -[1/(2*sqrt(pi))]*integral_0^infty
                    exp(-a*t)*I_|m|(b*t)*t^(-3/2) dt <= 0.  (4)

Indeed I_m(y)=(1/(2*pi))*integral exp(y*cos(k))*exp(-imk) dk has nonnegative series coefficients: for m>=0, I_m(y)=sum_(r>=0) (y/2)^(2r+m)/(r!*(r+m)!), and y>=0. Absolute convergence at infinity follows from a-b=(g-J)^2>0; at zero the nonconstant Fourier integrand is O(t^(|m|-3/2)), integrable for |m|>=1. One can first subtract the k-independent exp(-a*t) term to justify the Fourier/integral interchange. The case J=0 gives vanishing nonconstant coefficients directly.

Since g>J, omega is analytic in a nonzero strip around the real k axis, so its Fourier series converges absolutely. Sampling that series on the two momentum grids yields

    sum_NS omega - sum_R omega
      = -4*L*sum_(q>=1, q odd) omega_hat(q*L) >= 0.          (5)

The unprojected vacuum energies are E_a,vac=-sum_(k in K_a) omega(k), so (5) says E_R,vac>=E_NS,vac. The NS vacuum is physical and even. Every other physical NS state has at least two quasiparticles, each of energy eps(k)>=2(g-J), hence cost at least 4(g-J). In the R sector the physical states have odd quasiparticle number, so every physical R state has energy at least E_R,vac+2(g-J)>=E_NS,vac+2(g-J). This proves both ground-state uniqueness and (3).

The parity reasoning does not assume even L. If L is even, R has the unpaired zero and pi modes and NS has neither. If L is odd, R has the zero mode and NS has the pi mode. On the paramagnetic side both unpaired coefficients g-J and g+J are positive, so each unprojected vacuum is even; physical NS projection remains even and physical R projection remains odd. At L=2 the Jordan-Wigner dispersion and independently constructed Hamiltonian retain both directed bonds. For J=0 the same conclusion reduces to the independent-spin gap 2g.

Equation (3) provides the small-size bridge required by the particular quantum Ising family. It does not remove the need for interval seed enclosures or the separately reviewed bootstrap/interpolation theorem when claiming a bootstrap-derived result. It also should not be applied to 0<g<J: there the R vacuum parity flips, so the argument's R excitation-cost step is false.

## Independent audit and limits

The audit constructs spin-basis Hamiltonians independently, diagonalizes only L=2,...,8, and compares log traces for (J,h)=(1,.5),(1,1),(1,1.5),(1,2),(1,-1.5),(0,.7),(1,0),(0,0) at beta=0,.1,1,8. All 224 comparisons pass; maximum absolute log Z discrepancy is about 3.27e-13. This includes odd L and the doubled bond at L=2. ED is used only for this independent validation, never to produce the seeds.

Analytic limiting checks are

    J=0: Z_L=(2*cosh(beta*g))^L,
    h=0: Z_L=(2*cosh(beta*J))^L+(2*sinh(beta*J))^L,
    beta=0: Z_L=2^L.

Additional tests cover beta=1000 against arbitrary precision, both phases, criticality, and malformed parameters. Reproduce with:

    OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p test_quantum_ising.py -v
    OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python benchmarks/run_quantum_ising.py

## Certification follow-through and provenance

The numerical outputs in this note remain candidates. The separate implementation and review recorded in [QUANTUM_ISING_INTERVAL.md](QUANTUM_ISING_INTERVAL.md) complete the following certification steps for its explicitly supported inputs:

1. Enclose all algebraic/trigonometric single-particle energies and exponential factors with rigorous outward rational intervals. Apply the positive E/O recurrence using rational interval arithmetic; this is preferable to the cancellation-prone four-product form. Convert the resulting trace enclosures into P_x >= B_lower/A_upper^2 and P_beta >= C_lower/B_upper^2. No independent many-body spectrum enclosure is necessary.
2. Replay those certified rational lower bounds with the existing exact scalar adapter, retaining the canonical edge labels and parameters.
3. Compose the certified seed and exact replay with the reviewed signed interpolation and dedicated K=5 bootstrap theorem from the repository [seed_size/proofs/DERIVATIONS.md](../../seed_size/proofs/DERIVATIONS.md) and [two_d_theory/THEORY.md](../../two_d_theory/THEORY.md). These links are relative to the deployed gap_workflow/theory directory. The analytic paramagnetic bridge (3) covers all early sizes when g>J. Transfer eligibility alone does not establish these separate interpolation dependencies; their composition is documented in the interval companion.

The exact formula proves an O(L) reduction of the seed trace problem. The numerical artifacts do not yet prove any new uniform-gap theorem.
